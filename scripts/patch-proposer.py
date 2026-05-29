#!/usr/bin/env python3
"""Hard Gate patch proposer. P2.6 of closed-loop self-correction.

Reads a manual eval run's eval-results.behavioral.json, groups failing
expectations by attributed reference file (using EVAL_ATTRIBUTION from
eval-debt-report.py), and asks claude -p to propose a Hard Gate block
that — if added to the reference — would push the orchestrator to
produce output satisfying the failing expectation.

Always dry-run unless --apply is passed. Default --max 3 caps blast radius.

What the LLM is asked to produce (the Hard Gate pattern that has worked
across Stage 2.{1,2,3,4}):

  **[Description] (Hard Gate)**: [imperative rule statement]

  ❌ FAIL examples (anti-patterns the eval judge would reject):
  - …
  - …

  ✅ PASS examples (concrete patterns that satisfy the expectation):
  - …
  - …

Why full-file rewrite (not block-only injection):
  Insertion point determination is the hardest part — the LLM needs to
  pick the right section heading to live under, and that's much easier
  inside a full-file rewrite than as a separate "where to insert" step.
  Diff-against-current still shows exactly what changed.

Why severity-weighted prioritization:
  Critical failures (×15) dominate; warning (×5) come next; info (×1) are
  often noise. The script processes in this order so the highest-leverage
  patches come out of a small --max budget.

Safety:
  - Default dry-run. --apply required to write.
  - --max N (default 3) caps how many reference files get touched per run.
  - Subprocess timeout from _config.CLAUDE_TIMEOUT_SECONDS (default 600s,
    overridable via PRODUCT_PLAYBOOK_CLAUDE_TIMEOUT_SECONDS env var).
  - Skips files where source + prompt context would exceed MAX_INPUT_CHARS.
  - Post-hoc check: rejects output that drops existing headings (over-write
    catastrophe) by counting `^#`/`^##`/`^###` before and after.
"""

from __future__ import annotations

import argparse
import difflib
import importlib.util
import json
import re
import subprocess
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

# Reuse EVAL_ATTRIBUTION from eval-debt-report.py to keep one source of truth.
def _load_attribution() -> dict:
    path = Path(__file__).parent / "eval-debt-report.py"
    spec = importlib.util.spec_from_file_location("eval_debt_report", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.EVAL_ATTRIBUTION


try:
    from _config import SEVERITY_WEIGHTS as SEVERITY_WEIGHT  # K1
except ImportError:
    SEVERITY_WEIGHT = {"critical": 15, "warning": 5, "info": 1}
# K1: import centralised tunables, but keep patch-proposer's larger
# MAX_INPUT_CHARS (single-source-file mode tolerates more headroom than
# mirror-apply's source+target mode)
try:
    from _config import CLAUDE_TIMEOUT_SECONDS  # noqa: F401
except ImportError:
    CLAUDE_TIMEOUT_SECONDS = 600
MAX_INPUT_CHARS = 40_000

PROMPT_TEMPLATE = """You are extending a product-management skill's English source-of-truth reference file with a new Hard Gate block. Each Hard Gate is an enforcement-style addition that pushes the orchestrator to produce output satisfying a specific behavioral eval expectation that is currently failing.

<REFERENCE_FILE path="{file_path}">
{file_content}
</REFERENCE_FILE>

<FAILING_EXPECTATIONS>
{failing_expectations}
</FAILING_EXPECTATIONS>

<ATTRIBUTION_HINT>
{hint}
</ATTRIBUTION_HINT>
{prior_attempt_block}
Your task: produce an updated REFERENCE_FILE that adds one Hard Gate block per failing expectation (or one combined Hard Gate block if the expectations cluster naturally). The Hard Gate must follow this pattern that has worked across Stage 2 uplifts:

  **[Description] (Hard Gate)**: [imperative rule statement that names what must be present in the output and what specifically counts as failing it]

  ❌ FAIL examples (anti-patterns the eval judge would reject):
  - …concrete, quoted, paraphrased from real failure modes
  - …

  ✅ PASS examples (concrete patterns that satisfy the expectation):
  - …concrete, quoted
  - …

Rules:
1. Preserve ALL existing content. The new Hard Gate is an ADDITION — do not rewrite or remove existing rules, headings, or examples. The diff against the current file should show only insertions.
2. Place the new Hard Gate under the most semantically appropriate existing section (look at the heading structure). If no good section exists, insert near a related rule.
3. Use the keyword "Hard Gate" verbatim and "FAIL" verbatim — these are detected by downstream tooling.
4. Each FAIL example must be a concrete anti-pattern, not abstract ("vague" / "weak"). At least 2 FAIL and 2 PASS examples per Hard Gate.
5. Keep the file's heading structure intact (same ##, ###, ## count).
6. Preserve ALL code-fenced (```) block contents VERBATIM.
7. Output ONLY the full rewritten reference file content, wrapped in <UPDATED_REFERENCE> ... </UPDATED_REFERENCE> tags. No preamble, no diff, no explanation outside the tags.

Begin output now."""


def load_eval_results(path: Path) -> dict:
    with path.open() as f:
        return json.load(f)


def group_failures_by_file(eval_data: dict, attribution: dict,
                            multi_file: bool = False) -> dict[str, list[dict]]:
    """Return {file_path: [failure_dict, ...]} for failing expectations only.

    K6: when ``multi_file=True``, fan out each failing expectation across ALL
    primary files (not just primary[0]). Trade-off: one failing eval with N
    primary files becomes N patch attempts. Useful when you suspect the
    expectation's behavior is split across multiple files and want the
    proposer to try each — at the cost of more LLM calls. Default False
    preserves the single-target behavior.
    """
    failures: dict[str, list[dict]] = defaultdict(list)
    for b in eval_data.get("breakdown", []):
        if b.get("passed", True):
            continue
        attr = attribution.get(b["eval_name"], {})
        primary = attr.get("primary", [])
        if not primary:
            continue
        targets = primary if multi_file else [primary[0]]
        for target in targets:
            failures[target].append({
                "eval_name": b["eval_name"],
                "expectation_text": b.get("expectation_text", ""),
                "severity": b.get("severity", "warning"),
                "passes": b.get("passes", 0),
                "runs": b.get("runs", 0),
                "reasons": b.get("reasons", []),
                "hint": attr.get("hint", ""),
            })
    return failures


def cluster_weight(failures: list[dict]) -> int:
    return sum(SEVERITY_WEIGHT.get(f["severity"], 5) for f in failures)


def build_failing_block(failures: list[dict]) -> str:
    lines = []
    for i, f in enumerate(failures, 1):
        lines.append(f"Failure #{i} [{f['severity']}, {f['passes']}/{f['runs']} passing]")
        lines.append(f"  Eval: {f['eval_name']}")
        lines.append(f"  Expectation: {f['expectation_text']}")
        if f["reasons"]:
            lines.append(f"  Judge reasons (why it failed):")
            for r in f["reasons"][:3]:
                lines.append(f"    - {r[:280]}")
        lines.append("")
    return "\n".join(lines)


def call_claude(prompt: str, *, max_attempts: int = 2) -> str:
    """Invoke claude -p with one automatic retry on transient subprocess failure.

    O5: transient claude -p failures (network blip, sandbox eviction, transient
    rate limit) are common enough that aborting the whole batch on a single
    failure is annoying. One retry with no backoff is enough to recover most
    flake-class failures without burning meaningful extra budget.

    Timeouts are still raised (not retried) — a 600s timeout is structural
    (prompt too big / claude stuck) and a retry would just burn another 600s.
    """
    last_err: RuntimeError | None = None
    for attempt in range(1, max_attempts + 1):
        result = subprocess.run(
            ["claude", "-p", "--output-format", "text"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=CLAUDE_TIMEOUT_SECONDS,
        )
        if result.returncode == 0:
            return result.stdout
        last_err = RuntimeError(
            f"claude -p exited {result.returncode} (attempt {attempt}/{max_attempts})"
            f"\nstderr: {result.stderr[:500]}"
        )
        if attempt < max_attempts:
            print(f"  ⚠️  call_claude attempt {attempt} failed (rc={result.returncode}), "
                  f"retrying...", file=sys.stderr)
    raise last_err


def extract_updated(raw: str) -> str:
    m = re.search(r"<UPDATED_REFERENCE>\s*\n(.*?)\n\s*</UPDATED_REFERENCE>", raw, re.DOTALL)
    if not m:
        raise ValueError(
            "Could not find <UPDATED_REFERENCE> tags in output. First 500 chars:\n"
            + raw[:500]
        )
    return m.group(1)


def post_hoc_validate(original: str, updated: str) -> list[str]:
    warnings = []
    o_h2 = len(re.findall(r"^## ", original, re.M))
    u_h2 = len(re.findall(r"^## ", updated, re.M))
    if u_h2 < o_h2:
        warnings.append(f"## headings dropped: {o_h2} → {u_h2} (over-write may have removed sections)")

    o_h3 = len(re.findall(r"^### ", original, re.M))
    u_h3 = len(re.findall(r"^### ", updated, re.M))
    if u_h3 < o_h3:
        warnings.append(f"### headings dropped: {o_h3} → {u_h3}")

    o_fences = original.count("```")
    u_fences = updated.count("```")
    if u_fences < o_fences:
        warnings.append(f"code fences dropped: {o_fences} → {u_fences}")

    o_hg = len(re.findall(r"Hard Gate", original))
    u_hg = len(re.findall(r"Hard Gate", updated))
    if u_hg <= o_hg:
        warnings.append(f"Hard Gate count did not increase: {o_hg} → {u_hg} (LLM may not have added a new gate)")

    return warnings


def validate_hard_gate_structure(original: str, updated: str) -> str | None:
    """A2: strict structural check on newly-added Hard Gate blocks.

    Returns None if OK, else an error string explaining what's missing.

    Contract: if updated adds a new `Hard Gate` block (count went up), the
    delta must also contain (a) at least one `FAIL` example and (b) at least
    one ✅ PASS marker. A Hard Gate without FAIL/PASS examples is a sentence
    the orchestrator can ignore — it provides no behavioral anchor.

    Why fatal vs warning: post_hoc_validate already returns soft warnings for
    similar concerns; those don't block apply. This check blocks apply, so
    malformed Hard Gates never land on disk. patch-proposer returns
    status="malformed" instead of "applied" in that case.
    """
    o_hg = original.count("Hard Gate")
    u_hg = updated.count("Hard Gate")
    if u_hg <= o_hg:
        return None  # no new gate added — nothing to validate

    o_fail = len(re.findall(r"(?<![A-Za-z])FAILS?(?![A-Za-z])", original))
    u_fail = len(re.findall(r"(?<![A-Za-z])FAILS?(?![A-Za-z])", updated))
    o_pass = original.count("✅")
    u_pass = updated.count("✅")

    if u_fail <= o_fail:
        return (f"new Hard Gate added (count {o_hg} → {u_hg}) but FAIL examples "
                f"did not increase ({o_fail} → {u_fail}). A Hard Gate without a "
                f"FAIL example is unenforceable — patch rejected.")
    if u_pass <= o_pass:
        return (f"new Hard Gate added (count {o_hg} → {u_hg}) but ✅ PASS markers "
                f"did not increase ({o_pass} → {u_pass}). A Hard Gate needs a "
                f"PASS counter-example for the orchestrator to learn the shape "
                f"— patch rejected.")
    return None


def render_diff(file_path: str, current: str, updated: str) -> str:
    return "".join(difflib.unified_diff(
        current.splitlines(keepends=True),
        updated.splitlines(keepends=True),
        fromfile=f"a/{file_path}",
        tofile=f"b/{file_path}",
        n=3,
    ))


def _load_prior_suspects() -> dict[tuple[str, str], dict]:
    """D9: read the latest attribution-check report's JSON twin (if any).

    Returns mapping {(patched_file, eval_name): suspect_record} for
    'patch-wording-insufficient' suspects only — i.e., the patched file IS
    in EVAL_ATTRIBUTION.primary but the eval still fails. For those, the
    next proposer call gets a "previous attempt was insufficient" pep talk
    in the prompt so the LLM doesn't generate a near-identical weak gate.

    Reads the most recent docs/attribution-check-*.md by surfacing the
    structured JSON via re-running with --json. Falls back to no-op if
    none exists. Skipped silently — feedback is a nice-to-have, not a hard
    dependency.
    """
    docs = Path("docs")
    if not docs.is_dir():
        return {}
    reports = sorted(docs.glob("attribution-check-*.md"), reverse=True)
    if not reports:
        return {}
    # we can't reparse the markdown reliably; instead recompute JSON from the
    # latest patch log + the most recent after-eval the user pointed at. but
    # that's brittle — for v1, just parse the markdown headers for the
    # "patched file → eval" pairs in the Suspect section with hypothesis
    # "attribution looks right but patch wording was insufficient".
    latest = reports[0]
    suspects: dict[tuple[str, str], dict] = {}
    try:
        text = latest.read_text(encoding="utf-8")
    except OSError:
        return {}
    # crude but bounded: split on '### N. `<file>` → eval `<name>`'
    pattern = re.compile(
        r"###\s+\d+\.\s+`([^`]+)`\s+→\s+eval\s+`([^`]+)`.*?"
        r"\*\*Patched file in primary\?\*\*\s+✅",
        re.DOTALL,
    )
    for m in pattern.finditer(text):
        suspects[(m.group(1), m.group(2))] = {"source": str(latest)}
    return suspects


def process_cluster(file_path: Path, failures: list[dict], root: Path,
                    apply: bool,
                    prior_suspects: dict[tuple[str, str], dict] | None = None) -> dict:
    target = root / file_path
    if not target.is_file():
        return {"file": str(file_path), "status": "missing",
                "reason": f"target file does not exist: {target}"}

    original = target.read_text(encoding="utf-8")
    failing_block = build_failing_block(failures)
    hint = failures[0]["hint"]

    prior_attempt_block = ""
    if prior_suspects:
        relevant = [f for f in failures
                    if (str(file_path), f["eval_name"]) in prior_suspects]
        if relevant:
            evals = ", ".join(sorted({f["eval_name"] for f in relevant}))
            prior_attempt_block = (
                f"\n<PRIOR_ATTEMPT_WARNING>\n"
                f"A previous patch on this file targeted these same eval(s) "
                f"({evals}) and the expectation(s) STILL FAILED in the after-eval. "
                f"That means the prior Hard Gate wording was not strong enough to "
                f"change orchestrator behavior. For this attempt:\n"
                f"  - Do NOT produce a near-identical Hard Gate to whatever's already "
                f"in the file.\n"
                f"  - Try a sharper angle: split the rule into multiple smaller gates, "
                f"add more concrete FAIL examples that match the actual failure modes "
                f"in the eval reasons, or call out a specific anti-pattern "
                f"the orchestrator is currently producing.\n"
                f"</PRIOR_ATTEMPT_WARNING>\n"
            )

    prompt = PROMPT_TEMPLATE.format(
        file_path=str(file_path),
        file_content=original,
        failing_expectations=failing_block,
        hint=hint or "(none provided)",
        prior_attempt_block=prior_attempt_block,
    )

    total_chars = len(prompt)
    if total_chars > MAX_INPUT_CHARS:
        return {"file": str(file_path), "status": "skipped",
                "reason": f"prompt too large ({total_chars} > {MAX_INPUT_CHARS} chars)"}

    # O1: when validate_hard_gate_structure rejects the first attempt, retry
    # once with the failure reason embedded — gives the LLM one chance to fix
    # the specific structural defect (missing FAIL or ✅) rather than giving up.
    used_prompt = prompt
    updated: str | None = None
    structural_error: str | None = None
    diff: str = ""
    warnings: list[str] = []
    for attempt in (1, 2):
        try:
            raw = call_claude(used_prompt)
        except subprocess.TimeoutExpired:
            return {"file": str(file_path), "status": "timeout",
                    "reason": f"claude -p exceeded {CLAUDE_TIMEOUT_SECONDS}s"}
        except RuntimeError as e:
            return {"file": str(file_path), "status": "error", "reason": str(e)}

        try:
            updated = extract_updated(raw)
        except ValueError as e:
            return {"file": str(file_path), "status": "parse-error", "reason": str(e)}

        warnings = post_hoc_validate(original, updated)
        diff = render_diff(str(file_path), original, updated)

        if not diff.strip():
            return {"file": str(file_path), "status": "no-change",
                    "reason": "LLM produced identical output (no patch proposed)"}

        structural_error = validate_hard_gate_structure(original, updated)
        if structural_error is None:
            break  # passed structural validation — proceed to apply / dry-run

        if attempt == 1:
            print(f"  ⚠️  attempt 1 produced malformed Hard Gate "
                  f"({structural_error[:80]}...) — retrying with sharpened prompt",
                  file=sys.stderr)
            used_prompt = prompt + (
                f"\n\n<RETRY_REASON>\nYour previous output FAILED structural "
                f"validation: {structural_error}\n\nFix the specific defect: if "
                f"FAIL examples didn't increase, add at least one new concrete "
                f"`FAIL` example next to the new Hard Gate. If ✅ PASS markers "
                f"didn't increase, add at least one new concrete `✅ PASS` "
                f"example. Re-emit the full updated reference file with the fix "
                f"applied.\n</RETRY_REASON>\n"
            )

    if structural_error is not None:
        return {"file": str(file_path), "status": "malformed",
                "reason": f"structural validation failed after retry: {structural_error}",
                "diff": diff,
                "diff_lines": diff.count("\n"),
                "warnings": warnings,
                "retry_attempted": True}

    # N5: no-op patch detection. The diff is non-empty (we'd have returned
    # "no-change" earlier otherwise), and structural validation passed (so a
    # Hard Gate header IS being added). But if the diff doesn't actually
    # introduce new behavioral anchors — same `Hard Gate` count, same `FAIL`
    # count, same `## ` heading count — it's a cosmetic reorder that the
    # orchestrator won't behave differently for. Flag as applied-cosmetic so
    # downstream attribution-check doesn't expect a flip.
    def _count(text: str, pat: str) -> int:
        return len(re.findall(pat, text))
    delta_hg = _count(updated, r"Hard Gate") - _count(original, r"Hard Gate")
    delta_fail = (_count(updated, r"(?<![A-Za-z])FAILS?(?![A-Za-z])")
                  - _count(original, r"(?<![A-Za-z])FAILS?(?![A-Za-z])"))
    delta_h2 = (_count(updated, r"^## ") - _count(original, r"^## "))
    if delta_hg == 0 and delta_fail == 0 and delta_h2 == 0:
        return {"file": str(file_path), "status": "applied-cosmetic",
                "reason": "diff exists but no new Hard Gate / FAIL / ## heading was "
                          "introduced — likely a reorder or whitespace change with no "
                          "behavioral consequence. Not applying to avoid misleading "
                          "downstream attribution-check.",
                "diff": diff,
                "diff_lines": diff.count("\n"),
                "warnings": warnings,
                "addressed": [{
                    "eval_name": f["eval_name"],
                    "expectation_text": f["expectation_text"],
                    "severity": f["severity"],
                    "before_passes": f["passes"],
                    "before_runs": f["runs"],
                } for f in failures]}

    if apply:
        target.write_text(updated, encoding="utf-8")
        status = "applied"
    else:
        status = "dry-run"

    return {"file": str(file_path), "status": status, "diff": diff,
            "warnings": warnings, "diff_lines": diff.count("\n"),
            "n_failures_addressed": len(failures),
            "addressed": [{
                "eval_name": f["eval_name"],
                "expectation_text": f["expectation_text"],
                "severity": f["severity"],
                "before_passes": f["passes"],
                "before_runs": f["runs"],
            } for f in failures]}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results", type=Path, required=True,
                    help="Path to eval-results.behavioral.json from a manual eval run")
    ap.add_argument("--root", type=Path, default=Path.cwd())
    ap.add_argument("--apply", action="store_true",
                    help="Write proposed changes (default: dry-run, diff only)")
    ap.add_argument("--max", type=int, default=3,
                    help="Cap on reference files patched per invocation (default 3)")
    ap.add_argument("--file", type=str, default=None,
                    help="Restrict to one reference file path substring")
    ap.add_argument("--severity", choices=["critical", "warning", "info"],
                    default="critical",
                    help="Minimum severity to address (default: critical only)")
    ap.add_argument("--force", action="store_true",
                    help="Skip eval-freshness check (eval JSON older than authored files)")
    ap.add_argument("--one-at-a-time", action="store_true",
                    help="Apply at most ONE patch this invocation regardless of --max; "
                         "designed for precise regression attribution (L2 cleanup)")
    ap.add_argument("--multi-file", action="store_true",
                    help="K6: fan out each failing eval across ALL its EVAL_ATTRIBUTION "
                         "primary files (not just primary[0]). N× more patch attempts.")
    args = ap.parse_args()

    if args.max < 0:
        print(f"❌ --max must be >= 0 (got {args.max}). Negative caps "
              f"produce wrong arithmetic in the deferred-count message.",
              file=sys.stderr)
        return 2

    root = args.root.resolve()

    import importlib.util
    fspec = importlib.util.spec_from_file_location("_freshness",
                                                    Path(__file__).parent / "_freshness.py")
    fmod = importlib.util.module_from_spec(fspec)
    fspec.loader.exec_module(fmod)
    is_fresh, reason = fmod.check_eval_freshness(args.results, root)
    if not is_fresh and not args.force:
        print(f"❌ stale eval: {reason}", file=sys.stderr)
        return 2

    print(f"loading eval results from {args.results}...", file=sys.stderr)
    eval_data = load_eval_results(args.results)
    attribution = _load_attribution()

    grouped = group_failures_by_file(eval_data, attribution,
                                       multi_file=args.multi_file)
    if args.multi_file:
        print(f"K6: multi-file mode — failing evals fanned out across all primary files",
              file=sys.stderr)
    sev_min = {"critical": 3, "warning": 2, "info": 1}[args.severity]
    sev_rank = {"critical": 3, "warning": 2, "info": 1}

    # M7: load suppressions
    try:
        sup_spec = importlib.util.spec_from_file_location(
            "_suppressions", Path(__file__).parent / "_suppressions.py")
        sup_mod = importlib.util.module_from_spec(sup_spec)
        sup_spec.loader.exec_module(sup_mod)
        suppressed = sup_mod.load_suppressions()
    except (ImportError, OSError, AttributeError):
        suppressed = set()

    # filter by minimum severity per failure, then drop empty clusters
    filtered = {}
    sup_skipped = 0
    for f, fails in grouped.items():
        keep = []
        for x in fails:
            if sev_rank.get(x["severity"], 1) < sev_min:
                continue
            if (f, x["eval_name"]) in suppressed:
                sup_skipped += 1
                continue
            keep.append(x)
        if keep:
            filtered[f] = keep
    if sup_skipped:
        print(f"M7: skipped {sup_skipped} suppressed (file, eval) pair(s) "
              f"from docs/loop-suppressions.jsonl", file=sys.stderr)
    if args.file:
        filtered = {f: v for f, v in filtered.items() if args.file in f}

    if not filtered:
        print(f"no failing expectations at severity ≥ {args.severity}", file=sys.stderr)
        return 0

    # rank clusters by total severity weight
    ranked = sorted(filtered.items(), key=lambda kv: -cluster_weight(kv[1]))
    print(f"eligible reference files: {len(ranked)} (cap {args.max})", file=sys.stderr)
    for f, fs in ranked:
        print(f"  {f} — weight {cluster_weight(fs)}, {len(fs)} failure(s)", file=sys.stderr)

    effective_cap = 1 if args.one_at_a_time else args.max
    selected = ranked[:effective_cap]
    if args.one_at_a_time and len(ranked) > 1:
        print(f"  one-at-a-time mode: processing only the top-weighted cluster; "
              f"{len(ranked) - 1} deferred to next invocation after re-eval",
              file=sys.stderr)
    elif len(ranked) > effective_cap:
        print(f"  (deferring {len(ranked) - effective_cap} — raise --max if intended)",
              file=sys.stderr)

    prior_suspects = _load_prior_suspects()
    if prior_suspects:
        print(f"D9: prior attribution-check flagged {len(prior_suspects)} "
              f"(file, eval) pair(s) as wording-insufficient — prompt will warn",
              file=sys.stderr)

    results = []
    for i, (f, fs) in enumerate(selected, 1):
        print(f"\n[{i}/{len(selected)}] {f} (weight {cluster_weight(fs)}, {len(fs)} failures)",
              file=sys.stderr)
        r = process_cluster(Path(f), fs, root, args.apply, prior_suspects)
        results.append(r)
        print(f"  status: {r['status']}", file=sys.stderr)
        if r.get("warnings"):
            for w in r["warnings"]:
                print(f"  ⚠️  {w}", file=sys.stderr)
        if r.get("diff"):
            print(f"\n--- diff for {f} ---")
            print(r["diff"])
        elif r.get("reason"):
            print(f"  reason: {r['reason']}", file=sys.stderr)

    log_path = root / "logs" / f"patch-proposer-{date.today().isoformat()}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(
        json.dumps({"date": date.today().isoformat(),
                    "apply": args.apply,
                    "results": results}, indent=2, default=str),
        encoding="utf-8",
    )
    print(f"\nlog: {log_path}", file=sys.stderr)

    # M3: surface cosmetic vs real applies in the summary print, so the user
    # doesn't read "3 applied" and assume 3 real Hard Gates landed when one
    # was actually a no-op reorder.
    real = sum(1 for r in results if r["status"] == "applied")
    cosmetic = sum(1 for r in results if r["status"] == "applied-cosmetic")
    malformed = sum(1 for r in results if r["status"] == "malformed")
    if args.apply:
        print(f"\nsummary: applied={real}  applied-cosmetic={cosmetic}  malformed={malformed}",
              file=sys.stderr)
        if cosmetic > 0:
            print(f"⚠️  {cosmetic} cosmetic-only patch(es) skipped — see status "
                  f"'applied-cosmetic' in the log; downstream attribution-check "
                  f"will not expect these to flip any expectation",
                  file=sys.stderr)

    if not args.apply and any(r["status"] == "dry-run" for r in results):
        print("\nto write these changes: re-run with --apply", file=sys.stderr)

    has_failures = any(r["status"] in ("timeout", "error", "parse-error") for r in results)
    return 1 if has_failures else 0


if __name__ == "__main__":
    sys.exit(main())
