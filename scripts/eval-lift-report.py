#!/usr/bin/env python3
"""Compute per-expectation lift between two eval-results.behavioral.json runs.

After a manual eval round, this turns the "before" and "after" JSON into a
file-attributed scoreboard so the maintainer can see exactly which
expectations moved, by how much, and whether the lift covers the cost of
the patch that was applied.

Inputs:
  --before <path>   Older eval-results.behavioral.json (the baseline)
  --after  <path>   Newer eval-results.behavioral.json (post-patch)
Output:
  --output <path>   Markdown report (default: docs/eval-lift-<date>.md)
  --json            Emit JSON to stdout instead of markdown to file

Matching:
  Pairs by (eval_id, expectation_text). An expectation that appears in only
  one file is reported under "added" / "removed" (typically harness changes
  like the dispatch_expectations_removed_2026_05_28 cleanup).

Severity weights match evals/compute_eval_score.py:
  critical=15, warning=5, info=1.

Lift score = Σ(weight if improved) − Σ(weight if regressed). Positive means
the patch lifted the suite; negative means it regressed. Pass-rate delta
(passes/runs ratio per expectation, when both still failing) is reported
separately as "soft lift" — a 0/3 → 1/3 is movement even though both runs
count as fail under strict majority.

Exit codes:
  0  net lift ≥ 0 (no regression worse than gains)
  1  net lift < 0 (regression dominates — patch made things worse)
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

SEVERITY_WEIGHTS = {"critical": 15, "warning": 5, "info": 1}
SEVERITY_EMOJI = {"critical": "🔴", "warning": "🟡", "info": "🔵"}
SEVERITY_ORDER = {"info": 0, "warning": 1, "critical": 2}


def load(path: Path) -> dict:
    with path.open() as f:
        return json.load(f)


def index_breakdown(data: dict) -> dict[tuple[int, str], dict]:
    """Index breakdown by (eval_id, expectation_text) for cross-run matching."""
    return {
        (b["eval_id"], b["expectation_text"]): b
        for b in data.get("breakdown", [])
    }


def classify_pair(before: dict, after: dict) -> str:
    bp = before.get("passed", False)
    ap = after.get("passed", False)
    if bp and ap:
        return "unchanged-pass"
    if not bp and not ap:
        return "unchanged-fail"
    if not bp and ap:
        return "improved"
    return "regressed"


def soft_lift(before: dict, after: dict) -> int:
    """Pass count delta when neither side flipped strict-majority status."""
    return after.get("passes", 0) - before.get("passes", 0)


def compute(before_data: dict, after_data: dict) -> dict:
    before = index_breakdown(before_data)
    after = index_breakdown(after_data)
    all_keys = set(before) | set(after)

    paired = []      # both sides present
    added = []       # in after only
    removed = []     # in before only
    for k in all_keys:
        b = before.get(k)
        a = after.get(k)
        if b and a:
            paired.append((k, b, a))
        elif a:
            added.append((k, a))
        else:
            removed.append((k, b))

    improved, regressed = [], []
    unchanged_pass, unchanged_fail = [], []
    soft_moves = []   # both failing but passes/runs ratio moved
    for k, b, a in paired:
        cls = classify_pair(b, a)
        if cls == "improved":
            improved.append({"key": k, "before": b, "after": a})
        elif cls == "regressed":
            regressed.append({"key": k, "before": b, "after": a})
        elif cls == "unchanged-pass":
            unchanged_pass.append({"key": k, "before": b, "after": a})
        else:
            unchanged_fail.append({"key": k, "before": b, "after": a})
            sl = soft_lift(b, a)
            if sl != 0:
                soft_moves.append({"key": k, "before": b, "after": a, "delta": sl})

    def hard_score(items: list[dict], sign: int) -> int:
        return sum(
            sign * SEVERITY_WEIGHTS.get(it["after"].get("severity", "warning"), 5)
            for it in items
        )

    lift_gain = hard_score(improved, +1)
    lift_loss = hard_score(regressed, -1)   # already negative
    net_lift = lift_gain + lift_loss        # both already signed
    soft_gain = sum(m["delta"] for m in soft_moves if m["delta"] > 0)
    soft_loss = sum(m["delta"] for m in soft_moves if m["delta"] < 0)

    return {
        "generated": date.today().isoformat(),
        "summary": {
            "before_score": before_data.get("summary", {}).get("score"),
            "after_score": after_data.get("summary", {}).get("score"),
            "score_delta": (after_data.get("summary", {}).get("score", 0)
                            - before_data.get("summary", {}).get("score", 0)),
            "before_band": before_data.get("summary", {}).get("band"),
            "after_band": after_data.get("summary", {}).get("band"),
            "paired": len(paired),
            "added": len(added),
            "removed": len(removed),
            "improved": len(improved),
            "regressed": len(regressed),
            "unchanged_pass": len(unchanged_pass),
            "unchanged_fail": len(unchanged_fail),
            "soft_moves": len(soft_moves),
            "lift_gain": lift_gain,
            "lift_loss": lift_loss,
            "net_lift": net_lift,
            "soft_pass_gain": soft_gain,
            "soft_pass_loss": soft_loss,
        },
        "improved": improved,
        "regressed": regressed,
        "soft_moves": soft_moves,
        "added": [{"key": k, "item": a} for k, a in added],
        "removed": [{"key": k, "item": b} for k, b in removed],
    }


def render_markdown(report: dict, before_path: str, after_path: str) -> str:
    s = report["summary"]
    score_arrow = "↑" if s["score_delta"] > 0 else ("↓" if s["score_delta"] < 0 else "→")
    lift_emoji = "✅" if s["net_lift"] >= 0 else "❌"
    lines = [
        f"# Eval Lift Report — {report['generated']}",
        "",
        f"- **Before**: `{before_path}` (score **{s['before_score']}**, band `{s['before_band']}`)",
        f"- **After**:  `{after_path}` (score **{s['after_score']}**, band `{s['after_band']}`)",
        f"- **Score Δ**: {s['before_score']} {score_arrow} {s['after_score']} (**{s['score_delta']:+d}**)",
        f"- **Net hard lift**: **{s['net_lift']:+d}** points {lift_emoji} (gain {s['lift_gain']:+d} / loss {s['lift_loss']:+d})",
        "",
        "## Movement Summary",
        "",
        "| Class | Count |",
        "|-------|------:|",
        f"| 🟢 Improved (fail → pass) | {s['improved']} |",
        f"| 🔴 Regressed (pass → fail) | {s['regressed']} |",
        f"| ⚪ Unchanged-pass | {s['unchanged_pass']} |",
        f"| ⚪ Unchanged-fail | {s['unchanged_fail']} |",
        f"| 〰️ Soft moves (still failing but ratio shifted) | {s['soft_moves']} |",
        f"| ➕ Added expectations | {s['added']} |",
        f"| ➖ Removed expectations | {s['removed']} |",
        "",
    ]

    def render_items(title: str, items: list[dict], show_delta: bool = False) -> list[str]:
        if not items:
            return []
        out = [f"## {title}", "", "| Eval | Severity | Expectation | Before | After |",
               "|------|----------|-------------|-------:|------:|"]
        # sort by severity desc then by eval_id
        items.sort(key=lambda it: (
            -SEVERITY_ORDER.get(it["after"].get("severity", "warning"), 1),
            it["after"].get("eval_id", 0),
        ))
        for it in items:
            sev = it["after"].get("severity", "warning")
            emoji = SEVERITY_EMOJI.get(sev, "")
            eval_name = it["after"].get("eval_name", "?")
            text = (it["after"].get("expectation_text") or "")[:90].replace("|", "\\|")
            bp = it["before"]
            ap = it["after"]
            b_str = f"{bp.get('passes', '?')}/{bp.get('runs', '?')}"
            a_str = f"{ap.get('passes', '?')}/{ap.get('runs', '?')}"
            out.append(
                f"| {eval_name} | {emoji} {sev} | {text} | {b_str} | {a_str} |"
            )
        out.append("")
        return out

    lines += render_items("🟢 Improved (highest-leverage wins)", report["improved"])
    lines += render_items("🔴 Regressed (action required — patch reverted gains)", report["regressed"])

    if report["soft_moves"]:
        lines += [
            "## 〰️ Soft Moves (pass-rate shifted but still failing)",
            "",
            "These didn't flip strict-majority pass, but the underlying pass ratio moved. Worth investigating — small wording uplifts can sometimes push a 1/3 to 2/3 in the next round.",
            "",
            "| Eval | Severity | Expectation | Before | After | Δ |",
            "|------|----------|-------------|-------:|------:|--:|",
        ]
        report["soft_moves"].sort(key=lambda m: (-m["delta"], m["after"].get("eval_id", 0)))
        for m in report["soft_moves"]:
            sev = m["after"].get("severity", "warning")
            emoji = SEVERITY_EMOJI.get(sev, "")
            eval_name = m["after"].get("eval_name", "?")
            text = (m["after"].get("expectation_text") or "")[:90].replace("|", "\\|")
            bp = m["before"]
            ap = m["after"]
            lines.append(
                f"| {eval_name} | {emoji} {sev} | {text} | "
                f"{bp.get('passes', '?')}/{bp.get('runs', '?')} | "
                f"{ap.get('passes', '?')}/{ap.get('runs', '?')} | "
                f"{m['delta']:+d} |"
            )
        lines.append("")

    if report["added"] or report["removed"]:
        lines += render_set_evolution(report)

    rescue = render_regression_rescue(report)
    if rescue:
        lines.append(rescue)

    return "\n".join(lines)


def render_set_evolution(report: dict) -> list[str]:
    """B5: dedicated panel for expectation-set changes.

    Separates the "score moved" attribution into two buckets:
      (a) behavior moved — paired expectations went from fail → pass or vice versa
      (b) set moved      — expectations were added/removed between runs

    Surfaces an inflation warning when *removed* expectations carried more
    severity weight than *added* — that's a signal the score went up because
    the harness got easier, not because the behavior improved.

    Why this section exists: stage-2-1 → 2-3 once saw +25 nominal score with
    only +5 hard-lift. The other +20 was 6 failing expectations that got
    pruned (some criticals among them). Without this surfaced, that kind of
    score inflation reads as a real win when it isn't.
    """
    added = report["added"]
    removed = report["removed"]
    added_critical = [a for a in added if a["item"].get("severity") == "critical"]
    added_warning = [a for a in added if a["item"].get("severity") == "warning"]
    removed_critical = [r for r in removed if r["item"].get("severity") == "critical"]
    removed_warning = [r for r in removed if r["item"].get("severity") == "warning"]

    # phantom_lift: severity-weighted score impact purely from set changes,
    # assuming added expectations are failing (worst-case for harness) and
    # removed expectations were failing (best-case score inflation if true).
    # This is an UPPER BOUND on how much of score_delta could be set-driven.
    phantom_loss = (len(added_critical) * SEVERITY_WEIGHTS["critical"]
                    + len(added_warning) * SEVERITY_WEIGHTS["warning"])
    phantom_gain = (len(removed_critical) * SEVERITY_WEIGHTS["critical"]
                    + len(removed_warning) * SEVERITY_WEIGHTS["warning"])
    phantom_net = phantom_gain - phantom_loss

    lines = ["## ➕➖ Expectation Set Changes", ""]
    lines.append(
        f"- Added: **{len(added)}** total "
        f"(crit={len(added_critical)}, warn={len(added_warning)})"
    )
    lines.append(
        f"- Removed: **{len(removed)}** total "
        f"(crit={len(removed_critical)}, warn={len(removed_warning)})"
    )
    lines.append(
        f"- Phantom lift upper bound: **{phantom_net:+d}** "
        f"(gain {phantom_gain:+d} from removals / loss {phantom_loss:+d} from additions)"
    )
    lines.append("")

    if phantom_net >= 5:
        lines += [
            "### ⚠️  Expectation Set Inflation Warning",
            "",
            f"Up to **{phantom_net} points** of the score delta "
            f"({report['summary']['score_delta']:+d}) could come from removed "
            f"expectations rather than improved behavior. Compare this against "
            f"net hard lift ({report['summary']['net_lift']:+d}); if hard lift "
            f"is much smaller than score delta, the suite got *easier*, not better. "
            f"Decide whether removals were principled (drifted out of scope) or "
            f"accidental (eval renames) before celebrating the score.",
            "",
        ]

    if added:
        lines.append("**Added** (typically new harness coverage):")
        for a in added:
            sev = a["item"].get("severity", "?")
            lines.append(f"- `{a['item'].get('eval_name', '?')}` [{sev}]: "
                         f"{(a['item'].get('expectation_text') or '')[:120]}")
        lines.append("")
    if removed:
        lines.append("**Removed** (typically harness pruning):")
        for r in removed:
            sev = r["item"].get("severity", "?")
            lines.append(f"- `{r['item'].get('eval_name', '?')}` [{sev}]: "
                         f"{(r['item'].get('expectation_text') or '')[:120]}")
        lines.append("")
    return lines


def render_regression_rescue(report: dict) -> str:
    """L2: print actionable rescue info when the patch regressed the suite.

    Triggers when net_lift < 0 OR there's any regression at critical severity.
    Does NOT auto-revert — surfaces the recent authored-file commits and the
    exact git commands so a human can decide.
    """
    has_critical_regression = any(
        it["before"].get("severity") == "critical" or it["after"].get("severity") == "critical"
        for it in report.get("regressed", [])
    )
    if report["summary"]["net_lift"] >= 0 and not has_critical_regression:
        return ""

    try:
        log = subprocess.check_output(
            ["git", "log", "--oneline", "-10", "--",
             "references/", "SKILL.md", "agents/", "i18n/"],
            text=True, stderr=subprocess.DEVNULL,
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        log = "(could not read git log — not a git repo?)"

    net = report["summary"]["net_lift"]
    n_reg = len(report.get("regressed", []))
    crit_reg = sum(1 for it in report.get("regressed", [])
                   if it["after"].get("severity") == "critical")

    lines = [
        "## 🚨 Regression Rescue",
        "",
        f"**Net hard lift is {net:+d}** with **{n_reg} regressed expectation(s)** "
        f"({crit_reg} critical). The most recent patch may have made things worse "
        "than the baseline — inspect the regressed list above before deciding.",
        "",
        "**Recent commits touching authored files** (`references/`, `SKILL.md`, "
        "`agents/`, `i18n/`):",
        "",
        "```",
        log,
        "```",
        "",
        "**If you decide to revert** (review carefully — do NOT auto-execute):",
        "",
        "```bash",
        "# Inspect what the most recent authored-file commit changed:",
        "git show HEAD -- references/ SKILL.md agents/ i18n/ | less",
        "",
        "# Revert that single commit (creates a new revert commit, preserves history):",
        "git revert <SHA>",
        "",
        "# OR (rarely needed) discard the changes locally without a commit:",
        "git checkout HEAD~1 -- references/ SKILL.md agents/ i18n/",
        "```",
        "",
        "**Before committing a revert**, re-run the eval that produced the regression "
        "to confirm the revert actually flips the failing expectations back to passing "
        "— LLM variance on `--runs 1` can produce false-positive regressions that "
        "majority vote (`--runs 3`) would wash out.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--before", type=Path, required=True,
                    help="Baseline eval-results.behavioral.json")
    ap.add_argument("--after", type=Path, required=True,
                    help="Post-patch eval-results.behavioral.json")
    ap.add_argument("--output", type=Path, default=None,
                    help="Markdown report path (default: docs/eval-lift-<date>.md)")
    ap.add_argument("--json", action="store_true",
                    help="Emit JSON to stdout instead of markdown to file")
    ap.add_argument("--force", action="store_true",
                    help="Skip eval-freshness check on --after (eval older than authored files)")
    args = ap.parse_args()

    if not args.before.is_file():
        raise SystemExit(f"--before file not found: {args.before}")
    if not args.after.is_file():
        raise SystemExit(f"--after file not found: {args.after}")

    import importlib.util
    fspec = importlib.util.spec_from_file_location("_freshness",
                                                    Path(__file__).parent / "_freshness.py")
    fmod = importlib.util.module_from_spec(fspec)
    fspec.loader.exec_module(fmod)
    is_fresh, reason = fmod.check_eval_freshness(args.after, Path.cwd())
    if not is_fresh and not args.force:
        print(f"❌ stale --after eval: {reason}", file=sys.stderr)
        return 2

    before = load(args.before)
    after = load(args.after)
    report = compute(before, after)

    if args.json:
        json.dump(report, sys.stdout, indent=2, ensure_ascii=False, default=str)
        print()
    else:
        out = args.output or Path("docs") / f"eval-lift-{report['generated']}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_markdown(report, str(args.before), str(args.after)),
                       encoding="utf-8")
        print(f"wrote {out}", file=sys.stderr)
        s = report["summary"]
        print(f"net hard lift: {s['net_lift']:+d}  (improved {s['improved']}, "
              f"regressed {s['regressed']}, soft moves {s['soft_moves']})", file=sys.stderr)
        if s["net_lift"] < 0 or s["regressed"] > 0:
            print(f"⚠️  Regression detected — see 'Regression Rescue' section at the "
                  f"end of {out} for revert suggestions.", file=sys.stderr)

    return 0 if report["summary"]["net_lift"] >= 0 else 1


if __name__ == "__main__":
    sys.exit(main())
