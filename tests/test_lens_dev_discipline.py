import pathlib
import re
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_skill import validate_skill

SKILL_PATH = ROOT / "skills" / "dev-discipline" / "SKILL.md"


class TestDevDisciplineLens(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SKILL_PATH.read_text(encoding="utf-8")

    def test_passes_shared_skill_validator(self):
        self.assertEqual(validate_skill(str(SKILL_PATH)), [])

    def test_frontmatter_name_and_trigger_description(self):
        self.assertRegex(self.text, r"name:\s*dev-discipline")
        self.assertIn("Use when", self.text)

    def test_tdd_gate_demands_a_failing_test_first(self):
        self.assertIn("failing test", self.text)
        self.assertIn("watch it fail", self.text)

    def test_bug_fixes_start_from_a_reproduction_test(self):
        self.assertRegex(self.text, re.compile(r"bug fix.*failing", re.IGNORECASE | re.DOTALL))

    def test_scope_gate_forbids_silent_expansion(self):
        self.assertIn("Scope integrity", self.text)
        self.assertIn("out-of-scope", self.text.lower())

    def test_security_gate_covers_secrets_and_boundaries(self):
        self.assertIn(".env", self.text)
        self.assertIn("secret", self.text.lower())
        self.assertIn("boundar", self.text.lower())

    def test_subagent_policy_defaults_to_inline(self):
        self.assertIn("Subagent", self.text)
        self.assertIn("inline", self.text.lower())

    def test_review_gate_requires_fresh_context_reviewers(self):
        self.assertIn("Independent review", self.text)
        self.assertIn("fresh context", self.text.lower())

    def test_review_gate_dispatches_code_and_spec_reviewers(self):
        self.assertIn("code reviewer", self.text.lower())
        self.assertIn("spec reviewer", self.text.lower())

    def test_spec_reviewer_checks_diff_against_agreed_scope(self):
        self.assertRegex(
            self.text,
            re.compile(r"spec reviewer.*(scope|agreed|requirement)", re.IGNORECASE | re.DOTALL),
        )

    def test_finish_branch_offers_user_the_close_out_choice(self):
        self.assertIn("Finish the branch", self.text)
        self.assertIn("merge", self.text.lower())
        self.assertIn("PR", self.text)

    def test_tdd_gate_bans_test_theater_by_name(self):
        self.assertIn("test theater", self.text.lower())
        for cheat in (
            "hard-code the expected value",
            "start past the thing under test",
            "re-implement the code under test",
        ):
            self.assertIn(cheat, self.text.lower())

    def test_tdd_gate_draws_the_honest_mock_boundary(self):
        self.assertRegex(
            self.text,
            re.compile(r"environment boundary.*(honest|legitimate)", re.IGNORECASE | re.DOTALL),
        )

    def test_right_sizing_gates_plan_mode_on_architectural_ambiguity(self):
        self.assertIn("Right-sizing", self.text)
        self.assertRegex(
            self.text,
            re.compile(r"plan mode only.*(architectur|approaches)", re.IGNORECASE | re.DOTALL),
        )

    def test_small_change_valve_skips_reviewer_subagents(self):
        self.assertRegex(
            self.text,
            re.compile(r"30 lines.*(skip|inline)", re.IGNORECASE | re.DOTALL),
        )

    def test_plan_contract_has_required_sections(self):
        for marker in ("Acceptance criteria", "Non-goals", "Verification plan", "Deviations"):
            self.assertIn(marker, self.text)

    def test_plan_contract_is_outcome_based_not_architecture(self):
        self.assertRegex(
            self.text,
            re.compile(r"observable outcome", re.IGNORECASE),
        )

    def test_spec_reviewer_receives_plan_diff(self):
        self.assertRegex(
            self.text,
            re.compile(r"spec reviewer.*(diff of the plan|plan file.*diff|git diff.*plan)",
                       re.IGNORECASE | re.DOTALL),
        )

    def test_review_gate_carries_anti_ratchet_rule(self):
        self.assertIn("does not rise between rounds", self.text.lower())
        self.assertIn("prior", self.text.lower())

    def test_review_gate_forbids_inventing_requirements(self):
        self.assertRegex(
            self.text,
            re.compile(r"inventing requirements", re.IGNORECASE),
        )

    def test_reviewers_audit_saved_evidence_not_rebuild(self):
        self.assertRegex(
            self.text,
            re.compile(r"audit.*evidence", re.IGNORECASE | re.DOTALL),
        )
        self.assertIn("scratch", self.text.lower())

    def test_review_verdict_sentinel_is_fail_closed(self):
        self.assertIn("VERDICT:", self.text)
        self.assertRegex(
            self.text,
            re.compile(r"missing verdict.*fail", re.IGNORECASE | re.DOTALL),
        )

    def test_review_loop_is_bounded_at_three_rounds(self):
        self.assertRegex(self.text, re.compile(r"three rounds", re.IGNORECASE))

    def test_finish_branch_requires_entry_point_launch_check(self):
        self.assertRegex(self.text, re.compile(r"entry.point launch", re.IGNORECASE))
        self.assertIn("screenshot", self.text.lower())
        self.assertRegex(self.text, re.compile(r"run it twice", re.IGNORECASE))


if __name__ == "__main__":
    unittest.main()
