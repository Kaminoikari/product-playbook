#!/usr/bin/env python3
"""Translate behavioral-eval failures into a per-file fix backlog.

This is Stage 1 of the self-improvement closed loop. The eval suite
already tells us *what* is failing; the gap is turning that into *which
file the writer should open and what to look at*. This script does that
mapping deterministically — no LLM call — so attribution stays auditable.

Input:  evals/eval-results.behavioral.json (default; --input overrides)
Output: docs/eval-debt-<YYYY-MM-DD>.md       (default; --output overrides)

Notes:
- Mapping from `eval_name` to candidate source files is a hand-curated
  dict (EVAL_ATTRIBUTION). If new evals are added, extend that dict —
  the script intentionally errors on unknown names so attribution can
  never silently rot.
- Clusters are ranked by total severity weight (critical=15, warning=5,
  info=1) so the top of the report is the highest-leverage place to
  invest time.
- We never propose a patch here. Stage 2 will do that, gated by humans.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path


try:
    from _config import SEVERITY_WEIGHTS as SEVERITY_WEIGHT  # K1: centralised
except ImportError:
    SEVERITY_WEIGHT = {"critical": 15, "warning": 5, "info": 1}
SEVERITY_EMOJI = {"critical": "🔴", "warning": "🟡", "info": "🔵"}

# Judge "reasons" beginning with these prefixes indicate the test harness
# itself broke (claude subprocess timeout, judge couldn't parse output) —
# not a real product-playbook regression. We split these into their own
# section so the writer doesn't waste hours "fixing" a JTBD rule when the
# real action is "re-run the eval".
INFRA_ERROR_PREFIXES = ("response error:", "judge error:")


EVAL_ATTRIBUTION: dict[str, dict] = {
    "lens-selection-single": {
        "primary": ["skills/product-playbook/SKILL.md"],
        "secondary": ["skills/jtbd/SKILL.md"],
        "hint": "Step 2 lens-selection table: a narrow ask takes exactly one lens.",
    },
    "lens-blend": {
        "primary": ["skills/product-playbook/SKILL.md"],
        "secondary": ["skills/solution-prioritization/SKILL.md", "skills/pre-mortem/SKILL.md"],
        "hint": "Step 2 blended-lens rule: several perspectives merge into one integrated answer; staged sections are wrong here.",
    },
    "provenance-format": {
        "primary": ["skills/product-playbook/SKILL.md"],
        "secondary": [],
        "hint": "Step 4 provenance tag: exact `— Frameworks: X` line, names only by default.",
    },
    "guardrail-proportional": {
        "primary": ["skills/product-playbook/SKILL.md"],
        "secondary": [],
        "hint": "Relative guardrails table: single-line, non-blocking nudge for missing problem statement.",
    },
    "jtbd-depth": {
        "primary": ["skills/jtbd/SKILL.md"],
        "secondary": ["references/02b-jtbd.md"],
        "hint": "Per-persona JTBD; Five Whys Q5 emotion vocab; B2B organisation-level Jobs.",
    },
    "prfaq-quality": {
        "primary": ["skills/pr-faq/SKILL.md"],
        "secondary": ["references/04a-prfaq.md"],
        "hint": "PR-FAQ solution paragraph opens with user experience; External FAQ names a real competitor advantage.",
    },
    "security-awareness": {
        "primary": ["skills/prd-and-handoff/SKILL.md"],
        "secondary": [
            "references/08-security-checklist.md",
            "references/07a-handoff-core.md",
        ],
        "hint": "Handoff: auth/CORS/CSP coverage; security tasks in the task list; concrete .gitignore body.",
    },
    "strategy-critic-teardown": {
        "primary": ["skills/strategy-critic/SKILL.md"],
        "secondary": [],
        "hint": "Rumelt diagnosis identification; quote specific sentence; no-rewrite enforcement.",
    },
    "pre-mortem-scenarios": {
        "primary": ["skills/pre-mortem/SKILL.md"],
        "secondary": [],
        "hint": "≥10 scenarios spanning all 5 categories; leading indicators; top-3 ranking.",
    },
    # Trigger eval — different attribution shape (it tests the SKILL.md
    # trigger description and routing, not the framework rule files).
    "trigger-eval": {
        "primary": ["SKILL.md"],
        "secondary": [".claude-plugin/plugin.json"],
        "hint": "YAML frontmatter description / language-detect / DO-NOT-trigger list.",
    },
}


def severity_weight(sev: str) -> int:
    return SEVERITY_WEIGHT.get(sev, SEVERITY_WEIGHT["warning"])


def is_infra_error(item: dict) -> bool:
    """Heuristic: does the judge's first reason look like a harness error?"""
    reasons = item.get("reasons") or []
    if not reasons:
        return False
    first = (reasons[0] or "").strip().lower()
    return first.startswith(INFRA_ERROR_PREFIXES)


def cluster_failures(breakdown: list[dict]) -> tuple[dict[str, dict], list[dict]]:
    """Group failing expectations by eval_name; aggregate severity weight.

    Returns (clusters, infra_errors). infra_errors is a flat list of items
    whose failure mode looks like a test harness problem, not a real
    skill regression — kept separate so attribution doesn't get polluted.
    """
    clusters: dict[str, dict] = {}
    infra_errors: list[dict] = []
    for item in breakdown:
        if item.get("passed"):
            continue
        if is_infra_error(item):
            infra_errors.append(item)
            continue
        name = item.get("eval_name") or "unknown"
        cluster = clusters.setdefault(
            name,
            {
                "eval_id": item.get("eval_id"),
                "eval_name": name,
                "failures": [],
                "weight": 0,
                "critical": 0,
                "warning": 0,
                "info": 0,
            },
        )
        cluster["failures"].append(item)
        sev = item.get("severity", "warning")
        cluster["weight"] += severity_weight(sev)
        cluster[sev] = cluster.get(sev, 0) + 1
    return clusters, infra_errors


def render_cluster(cluster: dict) -> str:
    name = cluster["eval_name"]
    attribution = EVAL_ATTRIBUTION.get(name)
    if attribution is None:
        # Surface this loudly — unknown eval means EVAL_ATTRIBUTION needs
        # an entry, otherwise reports will silently miss the file pointer.
        attribution = {
            "primary": ["(unknown — extend EVAL_ATTRIBUTION in scripts/eval-debt-report.py)"],
            "secondary": [],
            "hint": "No attribution entry exists for this eval.",
        }

    lines: list[str] = []
    lines.append(f"### {name}  (weight {cluster['weight']})\n")
    sev_summary = []
    if cluster.get("critical"):
        sev_summary.append(f"🔴 {cluster['critical']} critical")
    if cluster.get("warning"):
        sev_summary.append(f"🟡 {cluster['warning']} warning")
    if cluster.get("info"):
        sev_summary.append(f"🔵 {cluster['info']} info")
    lines.append(f"**Severity:** {' · '.join(sev_summary)}")
    lines.append("")
    lines.append("**Where to look:**")
    for p in attribution["primary"]:
        lines.append(f"- `{p}` *(primary)*")
    for s in attribution["secondary"]:
        lines.append(f"- `{s}` (secondary)")
    lines.append("")
    lines.append(f"**Likely root cause:** {attribution['hint']}")
    lines.append("")
    lines.append("**Failing expectations:**")
    for f in cluster["failures"]:
        emoji = SEVERITY_EMOJI.get(f.get("severity", "warning"), "•")
        expectation = (f.get("expectation_text") or "").strip()
        lines.append(f"- {emoji} {expectation}")
        reasons = f.get("reasons") or []
        if reasons:
            # First reason is usually enough — it's the judge's quote.
            lines.append(f"  - _judge:_ {reasons[0].strip()}")
    lines.append("")
    return "\n".join(lines)


def render_top3(clusters: list[dict]) -> str:
    top = clusters[:3]
    if not top:
        return "All clusters clean — nothing to prioritise.\n"
    lines = ["**Top 3 to fix first** (highest severity-weight):", ""]
    for i, c in enumerate(top, 1):
        attribution = EVAL_ATTRIBUTION.get(c["eval_name"], {})
        files = ", ".join(f"`{p}`" for p in attribution.get("primary", []))
        lines.append(
            f"{i}. **{c['eval_name']}** (weight {c['weight']}) → {files or '?'}"
        )
        if attribution.get("hint"):
            lines.append(f"   {attribution['hint']}")
    lines.append("")
    return "\n".join(lines)


def render_infra_errors(items: list[dict]) -> str:
    if not items:
        return ""
    by_eval: dict[str, list[dict]] = {}
    for item in items:
        by_eval.setdefault(item.get("eval_name") or "unknown", []).append(item)
    lines = [
        "## ⚠️ Infrastructure errors (re-run before fixing)",
        "",
        f"{len(items)} failing expectation(s) across {len(by_eval)} eval(s) "
        "look like **test-harness** failures (claude subprocess timeout, "
        "judge couldn't parse output) — NOT real skill regressions. "
        "Re-run the eval before treating these as work items.",
        "",
    ]
    for name, group in sorted(by_eval.items()):
        lines.append(f"- **{name}** — {len(group)} expectation(s) affected")
        first_reason = (group[0].get("reasons") or [""])[0].strip()
        snippet = first_reason[:140] + ("…" if len(first_reason) > 140 else "")
        lines.append(f"  - _signature:_ `{snippet}`")
    lines.append("")
    return "\n".join(lines)


def render_report(results: dict, source_path: Path) -> str:
    summary = results.get("summary", {})
    breakdown = results.get("breakdown", []) or []

    clusters, infra_errors = cluster_failures(breakdown)
    ranked = sorted(clusters.values(), key=lambda c: -c["weight"])

    header = [
        f"# Eval Debt Report — {date.today().isoformat()}",
        "",
        f"> Source: `{source_path}`  ·  Kind: `{results.get('kind', 'behavioral')}`",
        "",
        "## Snapshot",
        "",
        f"- **Score:** {summary.get('score', '?')}/100  ·  Band: `{summary.get('band', '?')}`",
        f"- **Passed:** {summary.get('passed_expectations', '?')} / {summary.get('total_expectations', '?')}",
        f"- **Critical / Warning / Info failures:** "
        f"{summary.get('critical_failures', 0)} / "
        f"{summary.get('warning_failures', 0)} / "
        f"{summary.get('info_failures', 0)}",
        f"- **Genuine failing clusters:** {len(ranked)}"
        + (f"  ·  ⚠️ Infra errors: {len(infra_errors)}" if infra_errors else ""),
        "",
    ]

    sections: list[str] = []
    if infra_errors:
        sections.append(render_infra_errors(infra_errors))

    if ranked:
        sections.append("## Where to invest first\n\n" + render_top3(ranked))
        sections.append("## All failing clusters (ranked by severity weight)\n")
        sections.extend(render_cluster(c) for c in ranked)
    else:
        sections.append("_No genuine skill failures after filtering infra errors._\n")

    footer = [
        "---",
        "",
        "## Notes",
        "",
        "- This report is **deterministic attribution**, not patch generation. "
        "Stage 2 of the self-improvement loop will propose actual diffs, "
        "still gated by human PR review.",
        "- Infra errors (claude subprocess timeout, judge non-JSON) are "
        "split out so they don't pollute fix backlog — re-run the eval "
        "to confirm whether they were transient.",
        "- If an eval lacks a `Where to look` pointer, it means "
        "`EVAL_ATTRIBUTION` in `scripts/eval-debt-report.py` needs an entry.",
        "- Judge quotes show the first reason only; the full per-run "
        "reasoning lives in the source JSON.",
        "",
    ]
    return "\n".join(header + sections + footer)


def _check_attribution_paths(root: Path) -> list[str]:
    """A1: assert every primary/secondary path in EVAL_ATTRIBUTION still exists.

    EVAL_ATTRIBUTION is hand-written hardcoded strings. When source files get
    renamed or refactored, those strings go stale silently — debt-report keeps
    "working" but the attribution it computes is wrong, and patch-proposer
    targets nonexistent files. This catches the drift up front.
    """
    missing: list[str] = []
    for eval_name, entry in EVAL_ATTRIBUTION.items():
        for kind in ("primary", "secondary"):
            for p in entry.get(kind, []):
                if not (root / p).is_file():
                    missing.append(f"{eval_name}.{kind}: {p}")
    return missing


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--input",
        default="evals/eval-results.behavioral.json",
        help="Path to behavioral eval JSON (default: evals/eval-results.behavioral.json).",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Path to write Markdown report (default: docs/eval-debt-<today>.md).",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Write report to stdout instead of a file.",
    )
    parser.add_argument(
        "--skip-attribution-check",
        action="store_true",
        help="Skip EVAL_ATTRIBUTION path existence check (debug only).",
    )
    args = parser.parse_args()

    if not args.skip_attribution_check:
        missing = _check_attribution_paths(Path.cwd())
        if missing:
            print("❌ EVAL_ATTRIBUTION references nonexistent file(s):",
                  file=sys.stderr)
            for m in missing:
                print(f"  - {m}", file=sys.stderr)
            print("\nUpdate EVAL_ATTRIBUTION in this file after the rename/refactor, "
                  "or pass --skip-attribution-check to bypass.", file=sys.stderr)
            return 2

    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"ERROR: input not found: {input_path}", file=sys.stderr)
        return 1

    try:
        results = json.loads(input_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: input is not valid JSON ({exc})", file=sys.stderr)
        return 1

    report = render_report(results, input_path)

    if args.stdout:
        sys.stdout.write(report)
        return 0

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path("docs") / f"eval-debt-{date.today().isoformat()}.md"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
