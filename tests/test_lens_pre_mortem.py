# tests/test_lens_pre_mortem.py
import unittest, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from validate_skill import validate_skill

SKILL = "skills/pre-mortem/SKILL.md"

class TestPreMortemLens(unittest.TestCase):
    def test_passes_validator(self):
        self.assertEqual(validate_skill(SKILL), [])

    def test_declares_tag_and_substance(self):
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertIn("`Pre-mortem`", body)
        self.assertIn("failed", body.lower())
        self.assertIn("scenario", body.lower())
