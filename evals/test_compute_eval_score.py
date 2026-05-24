"""Unit tests for compute_eval_score.

Run from repo root:    python3 -m unittest evals.test_compute_eval_score
Or from evals/:        python3 -m unittest test_compute_eval_score
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from compute_eval_score import (  # noqa: E402
    SEVERITY_WEIGHTS,
    compute_score,
    score_band,
    should_fail,
)


def _exp(severity: str, passed: bool, **extra) -> dict:
    base = {"severity": severity, "passed": passed}
    base.update(extra)
    return base


class TestScoreBand(unittest.TestCase):
    def test_healthy_boundary(self):
        self.assertEqual(score_band(100), "healthy")
        self.assertEqual(score_band(90), "healthy")
        self.assertEqual(score_band(89), "needs-attention")

    def test_needs_attention_boundary(self):
        self.assertEqual(score_band(70), "needs-attention")
        self.assertEqual(score_band(69), "at-risk")

    def test_at_risk_floor(self):
        self.assertEqual(score_band(0), "at-risk")


class TestComputeScore(unittest.TestCase):
    def test_all_pass(self):
        results = [_exp("critical", True), _exp("warning", True), _exp("info", True)]
        summary = compute_score(results)
        self.assertEqual(summary["score"], 100)
        self.assertEqual(summary["band"], "healthy")
        self.assertEqual(summary["critical_failures"], 0)
        self.assertEqual(summary["passed_expectations"], 3)
        self.assertEqual(summary["total_expectations"], 3)

    def test_single_critical_fail(self):
        # 100 - 15 = 85, falls into needs-attention
        results = [_exp("critical", False)]
        summary = compute_score(results)
        self.assertEqual(summary["score"], 85)
        self.assertEqual(summary["band"], "needs-attention")
        self.assertEqual(summary["critical_failures"], 1)

    def test_two_criticals_drop_to_at_risk(self):
        # 100 - 30 = 70 → boundary → needs-attention
        # 100 - 45 = 55 → at-risk
        results = [_exp("critical", False) for _ in range(3)]
        summary = compute_score(results)
        self.assertEqual(summary["score"], 55)
        self.assertEqual(summary["band"], "at-risk")
        self.assertEqual(summary["critical_failures"], 3)

    def test_only_warnings(self):
        # 4 warnings × 5 = 20 → score 80
        results = [_exp("warning", False) for _ in range(4)]
        summary = compute_score(results)
        self.assertEqual(summary["score"], 80)
        self.assertEqual(summary["band"], "needs-attention")
        self.assertEqual(summary["warning_failures"], 4)
        self.assertEqual(summary["critical_failures"], 0)

    def test_only_infos(self):
        results = [_exp("info", False) for _ in range(5)]
        summary = compute_score(results)
        self.assertEqual(summary["score"], 95)
        self.assertEqual(summary["band"], "healthy")
        self.assertEqual(summary["info_failures"], 5)

    def test_score_clamped_at_zero(self):
        # 100 criticals would deduct 1500 → must clamp to 0
        results = [_exp("critical", False) for _ in range(100)]
        summary = compute_score(results)
        self.assertEqual(summary["score"], 0)
        self.assertEqual(summary["band"], "at-risk")

    def test_unknown_severity_treated_as_warning(self):
        results = [_exp("mystery", False)]
        summary = compute_score(results)
        self.assertEqual(summary["score"], 100 - SEVERITY_WEIGHTS["warning"])

    def test_breakdown_preserves_extras(self):
        results = [_exp("critical", False, eval_id=11, eval_name="strategy", expectation_text="x")]
        summary = compute_score(results)
        item = summary["breakdown"][0]
        self.assertEqual(item["eval_id"], 11)
        self.assertEqual(item["eval_name"], "strategy")
        self.assertEqual(item["expectation_text"], "x")


class TestShouldFail(unittest.TestCase):
    def _summary(self, critical=0, warning=0, info=0):
        results = (
            [_exp("critical", False) for _ in range(critical)]
            + [_exp("warning", False) for _ in range(warning)]
            + [_exp("info", False) for _ in range(info)]
        )
        return compute_score(results)

    def test_none_never_fails(self):
        self.assertFalse(should_fail(self._summary(critical=10), "none"))

    def test_critical_only_on_critical(self):
        self.assertFalse(should_fail(self._summary(warning=5), "critical"))
        self.assertFalse(should_fail(self._summary(info=5), "critical"))
        self.assertTrue(should_fail(self._summary(critical=1), "critical"))

    def test_any_fails_on_any(self):
        self.assertFalse(should_fail(self._summary(), "any"))
        self.assertTrue(should_fail(self._summary(info=1), "any"))
        self.assertTrue(should_fail(self._summary(warning=1), "any"))
        self.assertTrue(should_fail(self._summary(critical=1), "any"))

    def test_unknown_mode_raises(self):
        with self.assertRaises(ValueError):
            should_fail(self._summary(), "bogus")


if __name__ == "__main__":
    unittest.main()
