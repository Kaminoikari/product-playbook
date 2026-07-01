# tests/test_lens_positioning.py
import unittest, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from validate_skill import validate_skill

SKILL = "skills/positioning/SKILL.md"

class TestPositioningLens(unittest.TestCase):
    def test_passes_validator(self):
        self.assertEqual(validate_skill(SKILL), [])

    def test_declares_tag_and_substance(self):
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertIn("`Positioning`", body)
        self.assertIn("positioning", body.lower())
        self.assertIn("alternative", body.lower())
        self.assertGreater(len(body), 1200)
