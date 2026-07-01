# tests/test_lens_problem_framing.py
import unittest, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from validate_skill import validate_skill

SKILL = "skills/problem-framing/SKILL.md"

class TestProblemFramingLens(unittest.TestCase):
    def test_passes_validator(self):
        self.assertEqual(validate_skill(SKILL), [])

    def test_declares_framework_tag_and_substance(self):
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertIn("HMW", body)
        self.assertIn("pain point", body.lower())
        self.assertIn("how might we", body.lower())
        self.assertGreater(len(body), 2500)

    def test_excludes_positioning_lens_scope(self):
        # §2.2 (positioning / April Dunford) must not be pulled into this lens.
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertNotIn("April Dunford", body)


if __name__ == "__main__":
    unittest.main()
