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


if __name__ == "__main__":
    unittest.main()
