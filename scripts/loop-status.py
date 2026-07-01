#!/usr/bin/env python3
"""Single-pane status dashboard for the closed-loop harness.

B6 of the optimisation pass. Aggregates the key numbers from across the
deterministic stages (eval-debt + loop-history + loop-summary) into one
screen so you don't have to remember 3-4 separate commands every time you
want to know "where are we".

What it shows:
  - Latest eval: score, band, pass/fail counts (from --eval-results JSON)
  - Last tick: timestamp, mode, patches applied/proposed, stage durations
  - Trajectory verdict: from loop-summary.judge() (✅/🟡/⚠️/🔴/⚪)
  - Next action: a single sentence tailored to the verdict

No LLM, no subprocess overhead. Pure read-and-format.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import date
from pathlib import Path

SCRIPTS = Path(__file__).parent


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _read_eval(eval_path: Path) -> dict:
    if not eval_path.is_file():
        return {}
    try:
        data = json.loads(eval_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    s = data.get("summary", {})
    return {
        "path": str(eval_path),
        "score": s.get("score"),
        "band": s.get("band"),
        "passed": s.get("passed_expectations"),
        "total": s.get("total_expectations"),
        "critical": s.get("critical_failures"),
        "warning": s.get("warning_failures"),
    }


def _read_history(history_path: Path) -> list[dict]:
    if not history_path.is_file():
        return []
    out = []
    for line in history_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def _verdict(history: list[dict]) -> dict:
    if not history:
        return {"status": "insufficient-data", "icon": "⚪",
                "reason": "no loop ticks recorded yet"}
    summary_mod = _load_module("loop_summary", SCRIPTS / "loop-summary.py")
    return summary_mod.judge(history)


def _next_action(verdict: dict, eval_data: dict) -> str:
    status = verdict.get("status", "")
    if status == "converged":
        return "✅ healthy plateau — stop iterating, ship when ready"
    if status == "improving":
        return ("🟡 keep iterating: `python3 scripts/loop-tick.py "
                "--eval-results <latest>.json --apply`, then re-eval manually")
    if status == "stalled":
        return ("⚠️  run `npm run eval:attribution -- --after-eval <latest>.json` "
                "to find suspects, then either edit EVAL_ATTRIBUTION or "
                "hand-write the Hard Gate")
    if status == "regressing":
        return ("🔴 read the most recent docs/eval-lift-*.md Regression Rescue "
                "section; verify with --runs 3 before reverting")
    crit = (eval_data or {}).get("critical", 0) or 0
    if not eval_data:
        return "⚪ baseline run needed — `npm run eval:behavioral` first"
    if crit > 0:
        return f"⚪ run a tick: {crit} critical failure(s) to address"
    return ("⚪ score looks healthy but not enough trajectory data — run "
            "another tick to confirm convergence formally")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--eval-results", type=Path,
                    default=Path("evals/eval-results.behavioral.json"))
    ap.add_argument("--history", type=Path,
                    default=Path("docs/loop-history.jsonl"))
    ap.add_argument("--json", action="store_true",
                    help="Emit JSON to stdout instead of human box (for tooling)")
    args = ap.parse_args()

    eval_data = _read_eval(args.eval_results)
    history = _read_history(args.history)
    verdict = _verdict(history)
    last_tick = history[-1] if history else {}
    next_action = _next_action(verdict, eval_data)

    # M2: stale-eval warning — if the eval JSON is older than the latest
    # authored-file change, the score on this dashboard reflects pre-change
    # behavior. Don't silently report a "verdict" that's based on stale data.
    stale_reason = None
    if eval_data:
        fspec = importlib.util.spec_from_file_location(
            "_freshness", SCRIPTS / "_freshness.py")
        fmod = importlib.util.module_from_spec(fspec)
        fspec.loader.exec_module(fmod)
        is_fresh, reason = fmod.check_eval_freshness(args.eval_results, Path.cwd())
        if not is_fresh:
            stale_reason = reason

    if args.json:
        payload = {
            "eval": eval_data or None,
            "last_tick": last_tick or None,
            "verdict": verdict,
            "next_action": next_action,
            "stale_eval": stale_reason,
        }
        json.dump(payload, sys.stdout, indent=2, ensure_ascii=False, default=str)
        print()
        return {
            "converged": 0, "improving": 0,
            "stalled": 1, "regressing": 1,
            "insufficient-data": 2,
        }.get(verdict.get("status", ""), 2)

    print(f"┌─ closed-loop status ─────────────────────────────────────────")
    if stale_reason:
        print(f"│ ⚠️  STALE EVAL — score below reflects PRE-CHANGE behavior")
        print(f"│    {stale_reason[:80]}...")
    if eval_data:
        print(f"│ eval     {eval_data['score']} ({eval_data['band']})  "
              f"{eval_data['passed']}/{eval_data['total']} passed  "
              f"crit={eval_data['critical']} warn={eval_data['warning']}  "
              f"← {eval_data['path']}")
    else:
        print(f"│ eval     (no eval results at {args.eval_results})")
    if last_tick:
        ts = last_tick.get("timestamp", "?")[:16].replace("T", " ")
        mode = last_tick.get("mode", "?")
        prop = last_tick.get("patches_proposed_count", "?")
        applied = len(last_tick.get("patches_applied") or [])
        durations = last_tick.get("stage_durations") or {}
        dur_str = ""
        if durations:
            dur_str = "  ⏱ " + " ".join(f"{k}={v}s" for k, v in durations.items())
        print(f"│ tick     {ts}  mode={mode}  proposed={prop} applied={applied}{dur_str}")
    else:
        print(f"│ tick     (no history at {args.history})")
    print(f"│ verdict  {verdict.get('icon', '⚪')} {verdict.get('status', '?')}  "
          f"({verdict.get('reason', '')[:80]})")
    print(f"└──────────────────────────────────────────────────────────────")
    print()
    print(f"Next: {next_action}")

    return {
        "converged": 0, "improving": 0,
        "stalled": 1, "regressing": 1,
        "insufficient-data": 2,
    }.get(verdict.get("status", ""), 2)


if __name__ == "__main__":
    sys.exit(main())
