# tests/test_lens_prioritization.py
import unittest, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from validate_skill import validate_skill

SKILL = "skills/solution-prioritization/SKILL.md"

class TestPrioritizationLens(unittest.TestCase):
    def test_passes_validator(self):
        self.assertEqual(validate_skill(SKILL), [])

    def test_declares_tags_and_substance(self):
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertIn("`RICE`", body)
        self.assertIn("`GEM`", body)
        self.assertIn("reach", body.lower())
        self.assertIn("effort", body.lower())
