#!/usr/bin/env python3
"""Closed-loop self-correction orchestrator — one tick of the loop.

L0 of the closed-loop initiative. Chains the existing tooling into a single
command so a "tick" of the loop runs as one invocation instead of 6+ manual
steps. The human stays in the loop via the `--apply` gate and the manual
eval boundaries (this script never runs eval — it consumes existing eval
results and suggests when to run the next one).

What one tick does:

  Reads:   evals/eval-results.behavioral.json (or --eval-results <path>)
  Stage 1: scripts/eval-debt-report.py            (no LLM)
  Stage 2: scripts/patch-proposer.py              (LLM; dry-run unless --apply)
  Stage 3: scripts/i18n-mirror-apply.py           (LLM; runs only if --apply,
                                                   because mirroring nothing
                                                   new makes no sense)
  Stage 4: scripts/i18n-drift-report.py           (no LLM; verifies clean)
  Stage 5: append iteration record to docs/loop-history.jsonl
  Stage 6: print recommended next manual action (re-eval + lift)

Why no internal eval call:
  Per the no-ci-auto-eval policy memory, eval runs must be human-initiated.
  Orchestrator boundaries respect that: tick reads from existing eval JSON,
  applies fixes, recommends running the next manual eval. The "loop"
  closes between manual eval runs — each tick = one rotation around the
  fix → re-verify → measure-lift cycle.

Convergence (delegated to loop-summary.judge):
  This tick fast-paths "0 patches needed → converged" without history. For
  anything else, it loads loop-summary.py and asks judge() for the verdict
  across all prior ticks. That keeps L0 and L5 aligned on the single
  question "are we done?"  Loop history lives in docs/loop-history.jsonl
  (one record per tick).

Safety:
  - Dry-run by default. --apply is the single gate that turns on writes
    for BOTH patch-proposer (EN) and i18n-mirror-apply (i18n).
  - Each subprocess timeout: 900s (matches longest underlying script).
  - Exit codes: 0 success, 1 subprocess failure, 2 nothing to do.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SCRIPTS = Path(__file__).parent
EVAL_DEBT = SCRIPTS / "eval-debt-report.py"
PATCH_PROPOSER = SCRIPTS / "patch-proposer.py"
MIRROR_APPLY = SCRIPTS / "i18n-mirror-apply.py"
DRIFT_REPORT = SCRIPTS / "i18n-drift-report.py"

DEFAULT_HISTORY = Path("docs") / "loop-history.jsonl"
SUBPROCESS_TIMEOUT = 900


def run_cmd(cmd: list[str], description: str) -> tuple[int, str, str]:
    """Run subprocess, capture output, return (returncode, stdout, stderr)."""
    print(f"\n━━━━━ {description}", file=sys.stderr)
    print(f"  $ {' '.join(cmd)}", file=sys.stderr)
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return 124, "", f"timed out after {SUBPROCESS_TIMEOUT}s"
    if result.stderr.strip():
        print(result.stderr, file=sys.stderr, end="")
    return result.returncode, result.stdout, result.stderr


def summarize_eval(eval_path: Path) -> dict:
    data = json.loads(eval_path.read_text())
    summary = data.get("summary", {})
    return {
        "path": str(eval_path),
        "score": summary.get("score"),
        "band": summary.get("band"),
        "passed": summary.get("passed_expectations"),
        "total": summary.get("total_expectations"),
        "critical_failures": summary.get("critical_failures"),
        "warning_failures": summary.get("warning_failures"),
        "info_failures": summary.get("info_failures"),
    }


def count_proposed_patches(eval_path: Path, severity: str) -> int:
    """Quick dry-run patch-proposer to count how many files would be touched."""
    cmd = [
        "python3", str(PATCH_PROPOSER),
        "--results", str(eval_path),
        "--severity", severity,
        "--max", "999",
    ]
    # we don't actually need to call the LLM — patch-proposer prints the
    # eligible-files line to stderr before the first LLM call. But for v1
    # we just read the eval JSON ourselves and count failing attributions.
    data = json.loads(eval_path.read_text())
    sev_rank = {"critical": 3, "warning": 2, "info": 1}
    min_rank = sev_rank.get(severity, 3)

    # mirror the patch-proposer grouping logic at a high level
    import importlib.util
    spec = importlib.util.spec_from_file_location("eval_debt_report", SCRIPTS / "eval-debt-report.py")
    debt_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(debt_mod)
    attribution = debt_mod.EVAL_ATTRIBUTION

    files = set()
    for b in data.get("breakdown", []):
        if b.get("passed", True):
            continue
        if sev_rank.get(b.get("severity", "warning"), 2) < min_rank:
            continue
        attr = attribution.get(b["eval_name"], {})
        if attr.get("primary"):
            files.add(attr["primary"][0])
    return len(files)


def read_history(history_path: Path) -> list[dict]:
    if not history_path.is_file():
        return []
    out = []
    for line in history_path.read_text().splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def append_history(history_path: Path, record: dict) -> None:
    history_path.parent.mkdir(parents=True, exist_ok=True)
    with history_path.open("a") as f:
        f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")


def detect_convergence(history: list[dict], current_patches: int) -> str | None:
    """Return a convergence note string, or None if loop should keep going.

    Delegates the cross-tick verdict to loop-summary.judge() — that is the
    single source of truth for convergence judgement (opt #1). Adds the
    tick-local fast path: if current_patches == 0, this tick contributed
    nothing, so flag as converged without needing N ticks of history.
    """
    if current_patches == 0:
        return "✅ Converged: no critical failures in current eval results."
    if not history:
        return None

    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "loop_summary", Path(__file__).parent / "loop-summary.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    verdict = mod.judge(history)

    if verdict["status"] in ("converged", "improving", "insufficient-data"):
        return None  # loop should keep going (or wait for more ticks)

    if verdict["status"] == "stalled":
        return ("⚠️  " + verdict["reason"])
    if verdict["status"] == "regressing":
        return ("🔴 " + verdict["reason"])
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--eval-results", type=Path, required=True,
                    help="Path to eval-results.behavioral.json (the 'before' state)")
    ap.add_argument("--apply", action="store_true",
                    help="Apply patches AND mirrors (default: dry-run for both)")
    ap.add_argument("--severity", choices=["critical", "warning"], default="critical",
                    help="Minimum severity for patch-proposer (default: critical)")
    ap.add_argument("--max-patches", type=int, default=3,
                    help="Cap on patch-proposer --max (default 3)")
    ap.add_argument("--history", type=Path, default=DEFAULT_HISTORY,
                    help="Loop history JSONL path (default docs/loop-history.jsonl)")
    ap.add_argument("--force", action="store_true",
                    help="Skip eval-freshness check (eval older than authored files)")
    args = ap.parse_args()

    if not args.eval_results.is_file():
        print(f"❌ --eval-results not found: {args.eval_results}", file=sys.stderr)
        return 1

    import importlib.util
    fspec = importlib.util.spec_from_file_location(
        "_freshness", Path(__file__).parent / "_freshness.py")
    fmod = importlib.util.module_from_spec(fspec)
    fspec.loader.exec_module(fmod)
    is_fresh, reason = fmod.check_eval_freshness(args.eval_results, Path.cwd())
    if not is_fresh and not args.force:
        print(f"❌ stale eval: {reason}", file=sys.stderr)
        return 2

    started = datetime.now().isoformat(timespec="seconds")
    print(f"\n╔══════════════════════════════════════════════════════════════╗", file=sys.stderr)
    print(f"║ closed-loop tick — {started}", file=sys.stderr)
    print(f"║ mode: {'APPLY' if args.apply else 'DRY-RUN'}  severity≥{args.severity}  max-patches={args.max_patches}", file=sys.stderr)
    print(f"╚══════════════════════════════════════════════════════════════╝", file=sys.stderr)

    before = summarize_eval(args.eval_results)
    print(f"\nBefore: score {before['score']} ({before['band']})  "
          f"{before['passed']}/{before['total']} passed  "
          f"crit={before['critical_failures']} warn={before['warning_failures']}",
          file=sys.stderr)

    proposed_count = count_proposed_patches(args.eval_results, args.severity)
    print(f"\nFailing reference files at severity≥{args.severity}: {proposed_count}", file=sys.stderr)

    history = read_history(args.history)
    convergence_note = detect_convergence(history, proposed_count)
    if proposed_count == 0:
        print(convergence_note, file=sys.stderr)
        append_history(args.history, {
            "timestamp": started, "mode": "noop",
            "before_summary": before,
            "patches_proposed_count": 0,
            "convergence": convergence_note,
        })
        return 2

    # --- Stage 1: eval-debt-report ---
    debt_rc, debt_out, _ = run_cmd(
        ["python3", str(EVAL_DEBT), "--input", str(args.eval_results)],
        "Stage 1: eval-debt-report (deterministic)",
    )
    if debt_rc != 0:
        print(f"❌ eval-debt-report failed (rc={debt_rc})", file=sys.stderr)
        return 1

    # --- Stage 2: patch-proposer ---
    patch_cmd = [
        "python3", str(PATCH_PROPOSER),
        "--results", str(args.eval_results),
        "--severity", args.severity,
        "--max", str(args.max_patches),
    ]
    if args.apply:
        patch_cmd.append("--apply")
    patch_rc, patch_out, _ = run_cmd(patch_cmd, "Stage 2: patch-proposer (LLM)")
    if patch_rc != 0:
        print(f"❌ patch-proposer failed (rc={patch_rc})", file=sys.stderr)
        return 1
    # patch-proposer prints diffs to stdout when dry-run / applied
    print(patch_out)

    patches_applied_files: list[str] = []
    if args.apply:
        # read the log it wrote to identify which files actually changed
        from datetime import date as _date
        log_path = Path("logs") / f"patch-proposer-{_date.today().isoformat()}.log"
        if log_path.is_file():
            try:
                log = json.loads(log_path.read_text())
                patches_applied_files = [
                    r["file"] for r in log.get("results", [])
                    if r.get("status") == "applied"
                ]
            except json.JSONDecodeError:
                pass

    # --- Stage 3: i18n-mirror-apply --- (only meaningful when patches were applied)
    mirror_applied = False
    if args.apply and patches_applied_files:
        # widen --max to cover all i18n langs for each touched EN file
        mirror_max = max(10, len(patches_applied_files) * 5 + 2)
        mirror_rc, mirror_out, _ = run_cmd(
            ["python3", str(MIRROR_APPLY),
             "--include-warnings", "--max", str(mirror_max), "--apply"],
            "Stage 3: i18n-mirror-apply (LLM)",
        )
        if mirror_rc != 0:
            print(f"⚠️  i18n-mirror-apply failed (rc={mirror_rc}) — EN patches "
                  "are already applied; drift will surface what was missed.",
                  file=sys.stderr)
        else:
            mirror_applied = True
            # show only the summary line, not all diffs (would flood output)
            for line in mirror_out.splitlines():
                if line.startswith("[") or "status:" in line:
                    print(line)
    elif args.apply:
        print("\n━━━━━ Stage 3: i18n-mirror-apply — SKIPPED (no patches applied)",
              file=sys.stderr)
    else:
        print("\n━━━━━ Stage 3: i18n-mirror-apply — SKIPPED (dry-run mode)",
              file=sys.stderr)

    # --- Stage 4: i18n-drift-report (always) ---
    drift_rc, drift_json, _ = run_cmd(
        ["python3", str(DRIFT_REPORT), "--json"],
        "Stage 4: i18n-drift-report (deterministic)",
    )
    drift_summary = None
    if drift_rc in (0, 1, 2):
        try:
            drift = json.loads(drift_json)
            drift_summary = drift.get("summary", {})
            crit = sum(1 for c in drift["clusters"]
                       for d in c["drifts"] if d["severity"] == "critical")
            warn = sum(1 for c in drift["clusters"]
                       for d in c["drifts"] if d["severity"] == "warning")
            print(f"  drift: {drift_summary.get('clean')}/{drift_summary.get('total_pairs')} clean, "
                  f"critical={crit}, warning={warn}", file=sys.stderr)
        except json.JSONDecodeError:
            pass

    # --- Stage 5: append history ---
    record = {
        "timestamp": started,
        "mode": "apply" if args.apply else "dry-run",
        "before_summary": before,
        "patches_proposed_count": proposed_count,
        "patches_applied": patches_applied_files,
        "mirrors_applied": mirror_applied,
        "drift_after": drift_summary,
        "convergence_note": convergence_note,
    }
    append_history(args.history, record)
    print(f"\n  → history appended to {args.history}", file=sys.stderr)

    # --- Stage 6: next-action suggestion ---
    print(f"\n╔══════════════════════════════════════════════════════════════╗", file=sys.stderr)
    print(f"║ Next action", file=sys.stderr)
    print(f"╚══════════════════════════════════════════════════════════════╝", file=sys.stderr)
    if not args.apply:
        print(f"""
This was a DRY-RUN. Review the proposed diffs above. To apply:
  python3 scripts/loop-tick.py --eval-results {args.eval_results} --apply
""".strip(), file=sys.stderr)
    elif patches_applied_files:
        next_eval = "evals/eval-results.behavioral.json"
        print(f"""
{len(patches_applied_files)} EN file(s) patched, mirrors {'applied' if mirror_applied else 'NOT applied'}.

To verify lift, run the next manual eval, then compute the delta:
  python3 evals/run_behavioral_eval.py --runs 1 --fail-on none \\
    --json {next_eval} --markdown evals/eval-results.behavioral.md
  python3 scripts/eval-lift-report.py \\
    --before {args.eval_results} --after {next_eval}
""".strip(), file=sys.stderr)
        if convergence_note:
            print(f"\n{convergence_note}", file=sys.stderr)
    else:
        print("No patches applied (patch-proposer returned nothing).", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
