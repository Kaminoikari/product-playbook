import pathlib
import sys
import tempfile
import textwrap
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from validate_skill import validate_skill


class TestSkillStructure(unittest.TestCase):
    def setUp(self):
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        self.tmp_path = pathlib.Path(tmpdir.name)

    def _write(self, body: str) -> str:
        p = self.tmp_path / "SKILL.md"
        p.write_text(body, encoding="utf-8")
        return str(p)

    def test_valid_skill_has_no_violations(self):
        body = textwrap.dedent("""\
            ---
            name: jtbd
            description: Use when you need to understand the job a user hires the product to do, before designing a solution.
            ---
            # JTBD
            Detect the user's language and reply in it.
            Append the framework tag `JTBD` to the provenance line.
            """)
        self.assertEqual(validate_skill(self._write(body)), [])

    def test_missing_provenance_flagged(self):
        body = "---\nname: jtbd\ndescription: Use when ...\n---\n# JTBD\nDetect the user's language.\n"
        violations = validate_skill(self._write(body))
        self.assertTrue(any("provenance" in v.lower() for v in violations))

    def test_bad_name_flagged(self):
        body = "---\nname: JTBD_Skill\ndescription: Use when ...\n---\n# x\nprovenance tag\nlanguage\n"
        violations = validate_skill(self._write(body))
        self.assertTrue(any("name" in v.lower() for v in violations))

    def test_workflow_leak_in_description_flagged(self):
        body = "---\nname: jtbd\ndescription: Step 1 gather interviews, then write the job statement, then rank.\n---\n# x\nprovenance\nlanguage\n"
        violations = validate_skill(self._write(body))
        self.assertTrue(any("workflow" in v.lower() for v in violations))

    def test_workflow_leak_in_block_scalar_description_flagged(self):
        # `description: |` block scalars (the style used by this repo's real
        # SKILL.md files) must have their continuation lines joined before
        # the workflow-leak heuristic runs, not be reduced to the literal "|".
        body = textwrap.dedent("""\
            ---
            name: jtbd
            description: |
              Step 1 gather interviews,
              then write the job statement, then rank.
            ---
            # x
            provenance
            language
            """)
        violations = validate_skill(self._write(body))
        self.assertTrue(any("workflow" in v.lower() for v in violations))

    def test_oversized_frontmatter_flagged(self):
        padding = "x" * 1100
        body = (
            "---\n"
            "name: jtbd\n"
            "description: Use when ...\n"
            f"# {padding}\n"
            "---\n"
            "# x\nprovenance\nlanguage\n"
        )
        violations = validate_skill(self._write(body))
        self.assertTrue(any("1024" in v for v in violations))

    def test_missing_language_line_flagged(self):
        body = "---\nname: jtbd\ndescription: Use when ...\n---\n# x\nprovenance tag only, no runtime detection mentioned\n"
        violations = validate_skill(self._write(body))
        self.assertTrue(any("language" in v.lower() for v in violations))


if __name__ == "__main__":
    unittest.main()
