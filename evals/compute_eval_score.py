"""Deterministic scoring for product-playbook eval results.

Single source of truth: both run_trigger_test.py and run_behavioral_eval.py
import compute_score from here. No scoring logic anywhere else.
"""

from __future__ import annotations

SEVERITY_WEIGHTS = {
    "critical": 15,
    "warning": 5,
    "info": 1,
}

BAND_THRESHOLDS = [
    (90, "healthy"),
    (70, "needs-attention"),
    (0, "at-risk"),
]


def severity_weight(severity: str) -> int:
    return SEVERITY_WEIGHTS.get(severity, SEVERITY_WEIGHTS["warning"])


def score_band(score: float) -> str:
    for threshold, band in BAND_THRESHOLDS:
        if score >= threshold:
            return band
    return "at-risk"


def compute_score(eval_results: list[dict]) -> dict:
    """Compute an aggregate eval score from a flat list of expectation results.

    Each item in eval_results must contain at least:
        - severity: "critical" | "warning" | "info"
        - passed: bool (final pass/fail after any majority vote)

    Optional fields are preserved verbatim and surfaced in the breakdown:
        - eval_id, eval_name, expectation_text, reasons, runs, passes

    Returns:
        {
            "score": int (0-100),
            "band": "healthy" | "needs-attention" | "at-risk",
            "critical_failures": int,
            "warning_failures": int,
            "info_failures": int,
            "total_expectations": int,
            "passed_expectations": int,
            "breakdown": [ ...original items with derived fields... ],
        }
    """
    critical_failures = 0
    warning_failures = 0
    info_failures = 0
    passed = 0
    deduction = 0

    for item in eval_results:
        sev = item.get("severity", "warning")
        ok = bool(item.get("passed", False))
        if ok:
            passed += 1
            continue
        deduction += severity_weight(sev)
        if sev == "critical":
            critical_failures += 1
        elif sev == "info":
            info_failures += 1
        else:
            warning_failures += 1

    score = max(0, min(100, 100 - deduction))
    band = score_band(score)

    return {
        "score": score,
        "band": band,
        "critical_failures": critical_failures,
        "warning_failures": warning_failures,
        "info_failures": info_failures,
        "total_expectations": len(eval_results),
        "passed_expectations": passed,
        "breakdown": eval_results,
    }


def should_fail(summary: dict, fail_on: str) -> bool:
    """Decide whether a runner should exit non-zero given a --fail-on mode.

    fail_on:
        "critical": fail iff any critical expectation failed
        "any":      fail iff any expectation failed
        "none":     never fail (informational mode)
    """
    if fail_on == "none":
        return False
    if fail_on == "critical":
        return summary["critical_failures"] > 0
    if fail_on == "any":
        return summary["critical_failures"] + summary["warning_failures"] + summary["info_failures"] > 0
    raise ValueError(f"unknown fail_on mode: {fail_on!r}")


def format_summary_markdown(summary: dict, title: str = "Eval Results") -> str:
    """Render a GitHub-Actions-friendly Markdown summary."""
    band_emoji = {
        "healthy": "🟢",
        "needs-attention": "🟡",
        "at-risk": "🔴",
    }
    emoji = band_emoji.get(summary["band"], "⚪")
    lines = [
        f"## {title}",
        "",
        f"**Score:** {summary['score']}/100 {emoji} `{summary['band']}`",
        "",
        f"- Passed: **{summary['passed_expectations']} / {summary['total_expectations']}** expectations",
        f"- Critical failures: **{summary['critical_failures']}** (−{SEVERITY_WEIGHTS['critical']} each)",
        f"- Warning failures: **{summary['warning_failures']}** (−{SEVERITY_WEIGHTS['warning']} each)",
        f"- Info failures: **{summary['info_failures']}** (−{SEVERITY_WEIGHTS['info']} each)",
        "",
        "### Bands",
        "- 🟢 `healthy` ≥ 90",
        "- 🟡 `needs-attention` ≥ 70",
        "- 🔴 `at-risk` < 70",
    ]
    failures = [item for item in summary["breakdown"] if not item.get("passed", False)]
    if failures:
        lines += ["", "### Failed expectations"]
        for item in failures:
            sev = item.get("severity", "warning")
            sev_tag = {"critical": "🔴", "warning": "🟡", "info": "🔵"}.get(sev, "⚪")
            eid = item.get("eval_id", "?")
            ename = item.get("eval_name", "")
            text = item.get("expectation_text", "")
            lines.append(f"- {sev_tag} **[{eid}] {ename}** — {text[:160]}")
    return "\n".join(lines)
