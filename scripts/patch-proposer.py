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
  - Subprocess timeout 600s per call.
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


SEVERITY_WEIGHT = {"critical": 15, "warning": 5, "info": 1}
MAX_INPUT_CHARS = 40_000
CLAUDE_TIMEOUT_SECONDS = 600

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


def group_failures_by_file(eval_data: dict, attribution: dict) -> dict[str, list[dict]]:
    """Return {file_path: [failure_dict, ...]} for failing expectations only."""
    failures: dict[str, list[dict]] = defaultdict(list)
    for b in eval_data.get("breakdown", []):
        if b.get("passed", True):
            continue
        attr = attribution.get(b["eval_name"], {})
        primary = attr.get("primary", [])
        if not primary:
            continue
        target = primary[0]
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


def call_claude(prompt: str) -> str:
    result = subprocess.run(
        ["claude", "-p", "--output-format", "text"],
        input=prompt,
        capture_output=True,
        text=True,
        timeout=CLAUDE_TIMEOUT_SECONDS,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"claude -p exited {result.returncode}\nstderr: {result.stderr[:500]}"
        )
    return result.stdout


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


def render_diff(file_path: str, current: str, updated: str) -> str:
    return "".join(difflib.unified_diff(
        current.splitlines(keepends=True),
        updated.splitlines(keepends=True),
        fromfile=f"a/{file_path}",
        tofile=f"b/{file_path}",
        n=3,
    ))


def process_cluster(file_path: Path, failures: list[dict], root: Path,
                    apply: bool) -> dict:
    target = root / file_path
    if not target.is_file():
        return {"file": str(file_path), "status": "missing",
                "reason": f"target file does not exist: {target}"}

    original = target.read_text(encoding="utf-8")
    failing_block = build_failing_block(failures)
    hint = failures[0]["hint"]

    prompt = PROMPT_TEMPLATE.format(
        file_path=str(file_path),
        file_content=original,
        failing_expectations=failing_block,
        hint=hint or "(none provided)",
    )

    total_chars = len(prompt)
    if total_chars > MAX_INPUT_CHARS:
        return {"file": str(file_path), "status": "skipped",
                "reason": f"prompt too large ({total_chars} > {MAX_INPUT_CHARS} chars)"}

    try:
        raw = call_claude(prompt)
    except subprocess.TimeoutExpired:
        return {"file": str(file_path), "status": "timeout",
                "reason": "claude -p exceeded 600s"}
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
    args = ap.parse_args()

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

    grouped = group_failures_by_file(eval_data, attribution)
    sev_min = {"critical": 3, "warning": 2, "info": 1}[args.severity]
    sev_rank = {"critical": 3, "warning": 2, "info": 1}

    # filter by minimum severity per failure, then drop empty clusters
    filtered = {}
    for f, fails in grouped.items():
        keep = [x for x in fails if sev_rank.get(x["severity"], 1) >= sev_min]
        if keep:
            filtered[f] = keep
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

    selected = ranked[: args.max]
    if len(ranked) > args.max:
        print(f"  (deferring {len(ranked) - args.max} — raise --max if intended)",
              file=sys.stderr)

    results = []
    for i, (f, fs) in enumerate(selected, 1):
        print(f"\n[{i}/{len(selected)}] {f} (weight {cluster_weight(fs)}, {len(fs)} failures)",
              file=sys.stderr)
        r = process_cluster(Path(f), fs, root, args.apply)
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

    if not args.apply and any(r["status"] == "dry-run" for r in results):
        print("\nto write these changes: re-run with --apply", file=sys.stderr)

    has_failures = any(r["status"] in ("timeout", "error", "parse-error") for r in results)
    return 1 if has_failures else 0


if __name__ == "__main__":
    sys.exit(main())
