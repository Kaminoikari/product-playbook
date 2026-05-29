#!/usr/bin/env python3
"""Attribution sanity check — did each applied patch actually fix its target?

L3 of the closed-loop initiative. After a patch-proposer run + manual
re-eval, this script reads:

  1. The patch-proposer log (logs/patch-proposer-<date>.log) — knows which
     file each patch was applied to AND which failing expectations the
     patch was attempting to address (the "addressed" array per result).
  2. A post-apply eval JSON — knows whether those expectations are now
     passing or still failing.
  3. EVAL_ATTRIBUTION from eval-debt-report.py — knows which file each
     eval is currently mapped to as primary attribution.

For each (patched_file, addressed_expectation) pair where the expectation
STILL FAILED after the patch, this script surfaces it as a suspect
attribution: the patch landed but didn't move the eval. Two possible root
causes worth investigating:

  - **Attribution wrong**: the failing behavior actually depends on a
    different file that the orchestrator loads. The patch in the
    nominally-correct file is invisible at runtime. Action: extend
    EVAL_ATTRIBUTION[eval_name].primary to include the real target.
  - **Patch insufficient**: attribution is right but the Hard Gate
    wording didn't actually push the orchestrator hard enough. Action:
    iterate on the patch wording, or split the rule into multiple
    smaller gates with sharper FAIL examples.

Why this matters:
  Without this check, patch-proposer can produce convincing-looking diffs
  that ship without ever actually fixing the failures they claim to. The
  loop appears to be making progress (commits land, version bumps) while
  the underlying score stays flat.

Output:
  Markdown report at docs/attribution-check-<date>.md (or --output PATH).
  --json emits structured suggestions to stdout for tooling.

Exit codes:
  0  every patched expectation flipped to passing — attribution looks healthy
  1  one or more suspect attributions — investigate before next tick
  2  ran but had nothing to check (no patch log or no matching eval results)
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from datetime import date
from pathlib import Path


def load_patch_log(log_path: Path) -> dict:
    with log_path.open() as f:
        return json.load(f)


def load_eval(eval_path: Path) -> dict:
    with eval_path.open() as f:
        return json.load(f)


def load_attribution() -> dict:
    path = Path(__file__).parent / "eval-debt-report.py"
    spec = importlib.util.spec_from_file_location("eval_debt_report", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.EVAL_ATTRIBUTION


def index_eval(eval_data: dict) -> dict[tuple[int | None, str], dict]:
    """Index breakdown by (eval_name, expectation_text) for cross-source matching."""
    out: dict[tuple[str, str], dict] = {}
    for b in eval_data.get("breakdown", []):
        key = (b["eval_name"], b["expectation_text"])
        out[key] = b
    return out


def analyze(patch_log: dict, after_eval: dict, attribution: dict,
             suppressions: set[tuple[str, str]] | None = None) -> dict:
    after_idx = index_eval(after_eval)
    suspects: list[dict] = []
    flipped: list[dict] = []
    untrackable: list[dict] = []
    suppressed_count = 0
    suppressions = suppressions or set()

    for result in patch_log.get("results", []):
        if result.get("status") != "applied":
            continue
        patched_file = result["file"]
        for addressed in result.get("addressed", []):
            # M7: skip pairs the human has manually marked as off-limits
            if (patched_file, addressed["eval_name"]) in suppressions:
                suppressed_count += 1
                continue
            key = (addressed["eval_name"], addressed["expectation_text"])
            after = after_idx.get(key)
            if after is None:
                # the expectation isn't in the after-eval (maybe pruned, maybe
                # name changed) — can't verify
                untrackable.append({
                    "patched_file": patched_file,
                    "eval_name": addressed["eval_name"],
                    "expectation_text": addressed["expectation_text"],
                    "severity": addressed["severity"],
                    "reason": "expectation not present in after-eval (renamed or pruned?)",
                })
                continue

            if after.get("passed", False):
                flipped.append({
                    "patched_file": patched_file,
                    "eval_name": addressed["eval_name"],
                    "expectation_text": addressed["expectation_text"],
                    "severity": addressed["severity"],
                    "before": f"{addressed['before_passes']}/{addressed['before_runs']}",
                    "after": f"{after.get('passes', '?')}/{after.get('runs', '?')}",
                })
            else:
                attr = attribution.get(addressed["eval_name"], {})
                primary = attr.get("primary", [])
                attribution_match = patched_file in primary
                suspects.append({
                    "patched_file": patched_file,
                    "eval_name": addressed["eval_name"],
                    "expectation_text": addressed["expectation_text"],
                    "severity": addressed["severity"],
                    "before": f"{addressed['before_passes']}/{addressed['before_runs']}",
                    "after": f"{after.get('passes', '?')}/{after.get('runs', '?')}",
                    "after_reasons": after.get("reasons", [])[:2],
                    "current_primary_attribution": primary,
                    "patched_file_in_primary": attribution_match,
                    "hypothesis": (
                        "attribution may be wrong — patched file is NOT in EVAL_ATTRIBUTION primary"
                        if not attribution_match
                        else "attribution looks right but patch wording was insufficient — iterate on the Hard Gate"
                    ),
                })

    return {
        "generated": date.today().isoformat(),
        "patch_log_date": patch_log.get("date"),
        "summary": {
            "patches_applied": sum(1 for r in patch_log.get("results", [])
                                    if r.get("status") == "applied"),
            "expectations_addressed": len(flipped) + len(suspects) + len(untrackable),
            "expectations_flipped": len(flipped),
            "expectations_suspect": len(suspects),
            "expectations_untrackable": len(untrackable),
            "expectations_suppressed": suppressed_count,
        },
        "flipped": flipped,
        "suspects": suspects,
        "untrackable": untrackable,
    }


def render_markdown(report: dict) -> str:
    s = report["summary"]
    lines = [
        f"# Attribution Check — {report['generated']}",
        "",
        f"Patch log date: `{report['patch_log_date']}`",
        "",
        "## Summary",
        "",
        f"- Patches applied: **{s['patches_applied']}**",
        f"- Expectations addressed by those patches: **{s['expectations_addressed']}**",
        f"- 🟢 Flipped to passing: **{s['expectations_flipped']}**",
        f"- 🔴 Suspect (patch landed but expectation still fails): **{s['expectations_suspect']}**",
        f"- ⚪ Untrackable (expectation pruned/renamed in after-eval): **{s['expectations_untrackable']}**",
        "",
    ]

    if report["flipped"]:
        lines += [
            "## 🟢 Confirmed Fixes",
            "",
            "These expectations were addressed by an applied patch AND are now passing in the after-eval.",
            "",
            "| Patched File | Eval | Severity | Expectation | Before | After |",
            "|--------------|------|----------|-------------|-------:|------:|",
        ]
        for f in report["flipped"]:
            text = (f["expectation_text"] or "")[:80].replace("|", "\\|")
            lines.append(
                f"| `{f['patched_file']}` | {f['eval_name']} | {f['severity']} | "
                f"{text} | {f['before']} | {f['after']} |"
            )
        lines.append("")

    if report["suspects"]:
        lines += [
            "## 🔴 Suspect Attributions",
            "",
            "These expectations got a patch applied to a file but **still fail** in the after-eval. Two possible root causes — the hypothesis column suggests which to investigate first.",
            "",
        ]
        for i, s in enumerate(report["suspects"], 1):
            text = (s["expectation_text"] or "").replace("\n", " ")
            lines += [
                f"### {i}. `{s['patched_file']}` → eval `{s['eval_name']}`",
                "",
                f"**Severity**: {s['severity']}  ·  **Before**: {s['before']}  ·  **After**: {s['after']}",
                "",
                f"**Expectation**: {text}",
                "",
                f"**Current `EVAL_ATTRIBUTION[{s['eval_name']!r}].primary`**: `{s['current_primary_attribution']}`",
                "",
                f"**Patched file in primary?** {'✅ yes' if s['patched_file_in_primary'] else '❌ NO — likely attribution gap'}",
                "",
                f"**Hypothesis**: {s['hypothesis']}",
                "",
            ]
            if s["after_reasons"]:
                lines.append("**Judge reasoning from after-eval:**")
                for r in s["after_reasons"]:
                    lines.append(f"> {r[:280]}")
                lines.append("")
            if not s["patched_file_in_primary"]:
                lines += [
                    "**Suggested action**: open `scripts/eval-debt-report.py`, locate "
                    f"`EVAL_ATTRIBUTION[\"{s['eval_name']}\"]`, and consider adding "
                    f"`\"{s['patched_file']}\"` to the `primary` list — the patch you "
                    "applied there did NOT fix this expectation, which is one signal "
                    "that the real target file is elsewhere.",
                    "",
                ]
            else:
                lines += [
                    "**Suggested action**: re-run patch-proposer on this single "
                    f"expectation with `--severity {s['severity']}` and the same eval "
                    "results, and inspect the new Hard Gate wording. The attribution "
                    "is consistent; the previous patch text wasn't strong enough.",
                    "",
                ]

    suggestion = render_attribution_patch(report)
    if suggestion:
        lines += suggestion

    if report["untrackable"]:
        lines += [
            "## ⚪ Untrackable",
            "",
            "These addressed expectations don't appear in the after-eval — they may "
            "have been renamed in `evals/evals.json` or pruned. Verify manually.",
            "",
        ]
        for u in report["untrackable"]:
            text = (u["expectation_text"] or "")[:90]
            lines.append(f"- `{u['eval_name']}` [{u['severity']}]: {text}")
        lines.append("")

    return "\n".join(lines)


def render_attribution_patch(report: dict) -> list[str]:
    """O3: synthesize a copy-pasteable EVAL_ATTRIBUTION edit for attribution gaps.

    For every suspect where `patched_file_in_primary` is False, collect
    (eval_name → set of patched_files NOT yet in primary). Render as a single
    code block the user can read and adapt — not as a literal diff because
    EVAL_ATTRIBUTION's Python literal formatting is hand-maintained.

    Returns [] when no gap suspects exist (nothing to suggest).
    """
    gaps: dict[str, dict] = {}
    for s in report["suspects"]:
        if s["patched_file_in_primary"]:
            continue
        entry = gaps.setdefault(s["eval_name"], {
            "current_primary": s["current_primary_attribution"],
            "to_add": set(),
        })
        entry["to_add"].add(s["patched_file"])
    if not gaps:
        return []

    block = ["", "## 🔧 Suggested `EVAL_ATTRIBUTION` Edits", "",
             "The suspects above show **patched files that are NOT in the "
             "current `primary` list**. Below is a copy-pasteable edit for "
             "`scripts/eval-debt-report.py`'s `EVAL_ATTRIBUTION` mapping. "
             "Apply only after confirming each suggestion matches the actual "
             "orchestrator behavior (a wrong-target patch isn't always "
             "evidence the mapping is wrong — sometimes the patch just "
             "missed).", "",
             "```python", "EVAL_ATTRIBUTION = {",
             "    # ...existing entries unchanged...", ""]
    for eval_name, entry in sorted(gaps.items()):
        merged = sorted(set(entry["current_primary"]) | entry["to_add"])
        added_only = sorted(entry["to_add"])
        block.append(f"    {eval_name!r}: {{")
        block.append(f"        # added by attribution-check: {added_only}")
        block.append(f"        \"primary\": {merged!r},")
        block.append(f"        # ...keep existing secondary + hint unchanged...")
        block.append(f"    }},")
    block += ["}", "```", ""]
    return block


def auto_apply_attribution_patch(report: dict, debt_source_path: Path,
                                   dry_run: bool = True) -> dict:
    """M4: edit eval-debt-report.py's EVAL_ATTRIBUTION literal in place.

    For every gap suspect (patched_file NOT in primary), find the matching
    `"<eval_name>": {` block in the source file and append patched_file to
    that entry's `"primary": [...]` list.

    Safety:
      - ast.parse() the source before AND after the edit; abort on syntax break
      - Only modifies the `"primary": [...]` line within each matched entry
      - Idempotent: skips entries where patched_file is already in primary
      - Default dry-run; --apply writes the file

    Returns a dict describing what changed.
    """
    import ast as _ast
    src = debt_source_path.read_text(encoding="utf-8")
    # baseline parse
    _ast.parse(src)

    # collect (eval_name, files_to_add)
    edits: dict[str, list[str]] = {}
    for s in report.get("suspects", []):
        if s.get("patched_file_in_primary"):
            continue
        edits.setdefault(s["eval_name"], []).append(s["patched_file"])

    if not edits:
        return {"action": "noop", "reason": "no gap suspects to apply",
                "edits": {}, "dry_run": dry_run}

    changes: list[dict] = []
    new_src = src
    for eval_name, files_to_add in edits.items():
        pattern = re.compile(
            r'("' + re.escape(eval_name) + r'":\s*\{[^{}]*?"primary":\s*)'
            r'(\[[^\]]*\])',
            re.DOTALL,
        )
        m = pattern.search(new_src)
        if not m:
            changes.append({"eval": eval_name, "status": "not-found-in-source",
                            "files_to_add": files_to_add})
            continue
        original_list_literal = m.group(2)
        try:
            current = _ast.literal_eval(original_list_literal)
        except (ValueError, SyntaxError):
            changes.append({"eval": eval_name, "status": "list-parse-failed",
                            "files_to_add": files_to_add})
            continue
        added = [f for f in files_to_add if f not in current]
        if not added:
            changes.append({"eval": eval_name, "status": "already-present",
                            "files_to_add": files_to_add})
            continue
        new_list = current + added
        # format with double-quoted strings to match repo convention
        formatted = "[" + ", ".join(repr(p).replace("'", '"') for p in new_list) + "]"
        new_src = new_src[:m.start(2)] + formatted + new_src[m.end(2):]
        changes.append({"eval": eval_name, "status": "edited",
                        "added": added, "now_primary": new_list})

    # verify resulting source still parses
    try:
        _ast.parse(new_src)
    except SyntaxError as e:
        return {"action": "abort", "reason": f"post-edit syntax error: {e}",
                "edits": changes, "dry_run": dry_run}

    if dry_run:
        # show diff to stderr
        import difflib
        diff = "".join(difflib.unified_diff(
            src.splitlines(keepends=True),
            new_src.splitlines(keepends=True),
            fromfile=f"a/{debt_source_path.name}",
            tofile=f"b/{debt_source_path.name}",
        ))
        print(diff, file=sys.stderr)
        return {"action": "dry-run", "edits": changes, "dry_run": True}

    debt_source_path.write_text(new_src, encoding="utf-8")
    return {"action": "applied", "edits": changes, "dry_run": False}


def find_latest_patch_log(logs_dir: Path) -> Path | None:
    if not logs_dir.is_dir():
        return None
    candidates = sorted(logs_dir.glob("patch-proposer-*.log"), reverse=True)
    return candidates[0] if candidates else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--patch-log", type=Path, default=None,
                    help="Path to patch-proposer log (default: latest in logs/)")
    ap.add_argument("--after-eval", type=Path, required=True,
                    help="Path to eval-results.behavioral.json from a re-eval AFTER the patches were applied")
    ap.add_argument("--output", type=Path, default=None,
                    help="Markdown report path (default: docs/attribution-check-<date>.md)")
    ap.add_argument("--json", action="store_true",
                    help="Emit JSON to stdout instead of markdown to file")
    ap.add_argument("--force", action="store_true",
                    help="Skip eval-freshness check on --after-eval")
    ap.add_argument("--auto-apply", action="store_true",
                    help="Edit scripts/eval-debt-report.py EVAL_ATTRIBUTION in place "
                         "for every gap suspect (M4); shows diff in dry-run mode")
    ap.add_argument("--auto-apply-write", action="store_true",
                    help="With --auto-apply, actually write changes (default is dry-run)")
    args = ap.parse_args()

    log_path = args.patch_log or find_latest_patch_log(Path("logs"))
    if log_path is None or not log_path.is_file():
        print(f"❌ no patch-proposer log found (looked at {log_path or 'logs/'})",
              file=sys.stderr)
        return 2
    if not args.after_eval.is_file():
        print(f"❌ --after-eval not found: {args.after_eval}", file=sys.stderr)
        return 2

    fspec = importlib.util.spec_from_file_location("_freshness",
                                                    Path(__file__).parent / "_freshness.py")
    fmod = importlib.util.module_from_spec(fspec)
    fspec.loader.exec_module(fmod)
    is_fresh, reason = fmod.check_eval_freshness(args.after_eval, Path.cwd())
    if not is_fresh and not args.force:
        print(f"❌ stale --after-eval: {reason}", file=sys.stderr)
        return 2

    # N4: pair sanity — if patch log is newer than after-eval, the patches in
    # the log were applied AFTER the eval ran, so the eval can't have observed
    # their effects. The resulting "suspect / flipped" classification would be
    # nonsense. Warn loudly (not fatal — user may know better).
    try:
        log_mtime = log_path.stat().st_mtime
        eval_mtime = args.after_eval.stat().st_mtime
        if log_mtime > eval_mtime and not args.force:
            delta_min = (log_mtime - eval_mtime) / 60
            print(f"⚠️  pair sanity: patch log `{log_path}` is NEWER than after-eval "
                  f"`{args.after_eval}` by {delta_min:.1f} min. The patches in this log "
                  f"were applied AFTER the eval was run, so the eval cannot reflect "
                  f"their effects — every patch will look 'suspect'. Did you forget "
                  f"to re-run eval after applying patches? --force to proceed anyway.",
                  file=sys.stderr)
            return 2
    except OSError:
        pass  # filesystem oddity — fall through, the actual analysis will surface real issues

    patch_log = load_patch_log(log_path)
    after = load_eval(args.after_eval)
    attribution = load_attribution()

    # M7: load suppressions if available
    try:
        sup_spec = importlib.util.spec_from_file_location(
            "_suppressions", Path(__file__).parent / "_suppressions.py")
        sup_mod = importlib.util.module_from_spec(sup_spec)
        sup_spec.loader.exec_module(sup_mod)
        suppressions = sup_mod.load_suppressions()
    except (ImportError, OSError, AttributeError):
        suppressions = set()

    report = analyze(patch_log, after, attribution, suppressions)

    if args.json:
        json.dump(report, sys.stdout, indent=2, ensure_ascii=False, default=str)
        print()
    else:
        out = args.output or Path("docs") / f"attribution-check-{report['generated']}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_markdown(report), encoding="utf-8")
        s = report["summary"]
        print(f"wrote {out}", file=sys.stderr)
        print(f"  flipped={s['expectations_flipped']}  "
              f"suspect={s['expectations_suspect']}  "
              f"untrackable={s['expectations_untrackable']}", file=sys.stderr)

    if args.auto_apply:
        debt_src = Path(__file__).parent / "eval-debt-report.py"
        result = auto_apply_attribution_patch(report, debt_src,
                                              dry_run=not args.auto_apply_write)
        print(json.dumps(result, ensure_ascii=False, indent=2,
                          default=lambda o: list(o) if isinstance(o, set) else str(o)),
              file=sys.stderr)

    if report["summary"]["expectations_addressed"] == 0:
        return 2
    return 1 if report["summary"]["expectations_suspect"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
