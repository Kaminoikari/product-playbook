#!/usr/bin/env python3
"""Loop trajectory summary — convergence judgement across ticks.

L5 (rebadged from the originally-skipped L1) of the closed-loop initiative.
Reads `docs/loop-history.jsonl` and emits a markdown trajectory: how the
suite score, band, failure counts, and patch-proposal volume have moved
across ticks, plus a one-line convergence verdict for the human reading
the latest report.

This is the "zoom out" view that complements per-tick reports:
  - eval-lift-report shows what changed THIS tick
  - attribution-check shows whether THIS tick's patches transferred
  - loop-summary shows where the loop is trending OVER N ticks

Convergence rules (in priority order):
  1. ✅ Converged   — latest record has critical_failures == 0
                     AND band == healthy
  2. ⚠️  Stalled    — last 2 ticks each (a) net score change |Δ| < 5
                     AND (b) same critical_failures count
                     (suggests the proposer is hitting the same wall)
  3. 🔴 Regressing — latest score < N-1 score by >= 5 OR
                     critical_failures increased
  4. 🟡 Improving  — score trending up, criticals trending down
  5. ⚪ Insufficient data — fewer than 2 ticks

Why no LLM here:
  Pure data summary — the human is the reader. An LLM would just add noise.
  Loop-history.jsonl is structured; we read it directly.

Exit codes:
  0  converged or improving — no escalation needed
  1  stalled or regressing — surface to human
  2  insufficient data — append more ticks before judging
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

DEFAULT_HISTORY = Path("docs") / "loop-history.jsonl"


def load_history(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    out = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError as e:
                # bad line → log and skip rather than abort the whole report
                print(f"⚠️  skipping malformed history line: {e}", file=sys.stderr)
    return out


def _score(rec: dict) -> int | None:
    return (rec.get("before_summary") or {}).get("score")


def _criticals(rec: dict) -> int | None:
    return (rec.get("before_summary") or {}).get("critical_failures")


def _warnings(rec: dict) -> int | None:
    return (rec.get("before_summary") or {}).get("warning_failures")


def _band(rec: dict) -> str | None:
    return (rec.get("before_summary") or {}).get("band")


def judge(history: list[dict]) -> dict:
    """Return verdict dict: {status, reason, score_trend, criticals_trend}."""
    if len(history) < 2:
        last = history[-1] if history else {}
        return {
            "status": "insufficient-data",
            "icon": "⚪",
            "reason": "Need at least 2 ticks to judge trend. Run more ticks before trusting this summary.",
            "n_ticks": len(history),
            "latest_score": _score(last),
            "latest_band": _band(last),
        }

    last, prev = history[-1], history[-2]
    score_now, score_prev = _score(last), _score(prev)
    crit_now, crit_prev = _criticals(last), _criticals(prev)
    band_now = _band(last)

    if crit_now == 0 and band_now == "healthy":
        return {
            "status": "converged",
            "icon": "✅",
            "reason": f"latest tick has zero criticals at score {score_now} "
                      f"(band: healthy). Loop has reached a healthy plateau — "
                      f"stop iterating until eval set or thresholds change.",
            "n_ticks": len(history),
            "latest_score": score_now,
            "latest_band": band_now,
        }

    if score_now is not None and score_prev is not None:
        delta = score_now - score_prev
        if delta <= -5 or (crit_now is not None and crit_prev is not None and crit_now > crit_prev):
            return {
                "status": "regressing",
                "icon": "🔴",
                "reason": f"score dropped {score_prev} → {score_now} ({delta:+d}) "
                          f"or criticals climbed ({crit_prev} → {crit_now}). "
                          f"Investigate the most recent patch — see eval-lift-report's "
                          f"Regression Rescue section.",
                "n_ticks": len(history),
                "latest_score": score_now,
                "latest_band": band_now,
            }

    if len(history) >= 3:
        # stall detection: last 2 deltas both small AND criticals unchanged
        s2 = _score(history[-3])
        c2 = _criticals(history[-3])
        if (score_now is not None and score_prev is not None and s2 is not None
                and abs(score_now - score_prev) < 5 and abs(score_prev - s2) < 5
                and crit_now is not None and crit_prev is not None and c2 is not None
                and crit_now == crit_prev == c2 and crit_now > 0):
            return {
                "status": "stalled",
                "icon": "⚠️",
                "reason": f"last 3 ticks all hovered around score {s2}→{score_prev}→{score_now} "
                          f"with criticals stuck at {crit_now}. The proposer is hitting "
                          f"the same wall — run attribution-check.py to see whether the "
                          f"patches are missing their target, and consider updating "
                          f"EVAL_ATTRIBUTION or rewriting the Hard Gate by hand.",
                "n_ticks": len(history),
                "latest_score": score_now,
                "latest_band": band_now,
            }

    return {
        "status": "improving",
        "icon": "🟡",
        "reason": f"score moved {score_prev} → {score_now} "
                  f"({(score_now - score_prev):+d}) and criticals "
                  f"{crit_prev} → {crit_now}. Keep iterating.",
        "n_ticks": len(history),
        "latest_score": score_now,
        "latest_band": band_now,
    }


SPARK_CHARS = "▁▂▃▄▅▆▇█"


def _sparkline(values: list[int | float]) -> str:
    """N6: ASCII sparkline of numeric values, normalised to 8 levels.

    Returns empty string for fewer than 2 values (no trend to show).
    """
    if len(values) < 2:
        return ""
    nums = [v for v in values if isinstance(v, (int, float))]
    if len(nums) < 2:
        return ""
    lo, hi = min(nums), max(nums)
    span = hi - lo
    if span == 0:
        return SPARK_CHARS[3] * len(nums)  # flat line in the middle
    out = []
    for v in nums:
        idx = int((v - lo) / span * (len(SPARK_CHARS) - 1))
        out.append(SPARK_CHARS[idx])
    return "".join(out)


def render_trajectory(history: list[dict]) -> str:
    """Markdown table of score/band/failure counts per tick + N6 sparkline."""
    if not history:
        return "_(no history)_\n"
    scores = [(rec.get("before_summary") or {}).get("score") for rec in history]
    crits = [(rec.get("before_summary") or {}).get("critical_failures") for rec in history]
    spark_score = _sparkline([s for s in scores if s is not None])
    spark_crit = _sparkline([c for c in crits if c is not None])

    preamble = []
    if spark_score:
        score_seq = " → ".join(str(s) for s in scores if s is not None)
        preamble.append(f"**Score trend**: `{spark_score}`  ({score_seq})")
    if spark_crit:
        crit_seq = " → ".join(str(c) for c in crits if c is not None)
        preamble.append(f"**Criticals trend**: `{spark_crit}`  ({crit_seq})")
    if preamble:
        preamble.append("")

    lines = preamble + [
        "| # | When | Mode | Score | Band | ✗crit | ✗warn | Patches | Note |",
        "|--:|------|------|------:|------|------:|------:|--------:|------|",
    ]
    for i, rec in enumerate(history, 1):
        bs = rec.get("before_summary") or {}
        when = rec.get("timestamp", "?")[:16].replace("T", " ")
        mode = rec.get("mode", "?")
        patches = rec.get("patches_proposed_count", "?")
        note = (rec.get("convergence") or "")[:50]
        lines.append(
            f"| {i} | {when} | {mode} | {bs.get('score', '?')} | "
            f"{bs.get('band', '?')} | {bs.get('critical_failures', '?')} | "
            f"{bs.get('warning_failures', '?')} | {patches} | {note} |"
        )
    return "\n".join(lines)


def render_markdown(history: list[dict], verdict: dict) -> str:
    lines = [
        f"# Loop Trajectory Summary — {date.today().isoformat()}",
        "",
        f"**Verdict:** {verdict['icon']} **{verdict['status']}** "
        f"(after {verdict['n_ticks']} tick(s))",
        "",
        verdict["reason"],
        "",
        "## Trajectory",
        "",
        render_trajectory(history),
        "",
    ]

    if verdict["status"] in ("stalled", "regressing"):
        lines += [
            "## Suggested Next Action",
            "",
        ]
        if verdict["status"] == "stalled":
            lines += [
                "1. Run `python3 scripts/attribution-check.py --after-eval <latest>.json` "
                "to see whether recent patches actually transferred.",
                "2. If suspects show **attribution gap** (patched file not in primary): "
                "edit `scripts/eval-debt-report.py` `EVAL_ATTRIBUTION` to point the eval "
                "at the right file before the next tick.",
                "3. If suspects show **patch wording insufficient**: hand-edit the Hard "
                "Gate in the primary file — the proposer is producing diffs the orchestrator "
                "doesn't act on.",
                "",
            ]
        else:
            lines += [
                "1. Read the most recent `docs/eval-lift-*.md` — there is a "
                "**Regression Rescue** section with `git revert` candidates.",
                "2. Before reverting, verify the regression isn't `--runs 1` LLM "
                "variance: re-run the eval with `--runs 3` and compare.",
                "3. If the regression is real, `git revert <SHA>` and re-tick.",
                "",
            ]

    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--history", type=Path, default=DEFAULT_HISTORY)
    ap.add_argument("--output", type=Path, default=None,
                    help="Markdown output path (default: docs/loop-summary-<date>.md)")
    ap.add_argument("--json", action="store_true",
                    help="Emit JSON verdict to stdout instead of markdown to file")
    args = ap.parse_args()

    history = load_history(args.history)
    verdict = judge(history)

    if args.json:
        out_json = {"verdict": verdict, "ticks": len(history)}
        json.dump(out_json, sys.stdout, indent=2, ensure_ascii=False)
        print()
    else:
        out = args.output or Path("docs") / f"loop-summary-{date.today().isoformat()}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_markdown(history, verdict), encoding="utf-8")
        print(f"wrote {out}  ({verdict['icon']} {verdict['status']})", file=sys.stderr)

    return {
        "converged": 0,
        "improving": 0,
        "stalled": 1,
        "regressing": 1,
        "insufficient-data": 2,
    }[verdict["status"]]


if __name__ == "__main__":
    sys.exit(main())
