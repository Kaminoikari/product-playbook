# tests/test_lens_pr_faq.py
import unittest, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from validate_skill import validate_skill

SKILL = "skills/pr-faq/SKILL.md"

class TestPrFaqLens(unittest.TestCase):
    def test_passes_validator(self):
        self.assertEqual(validate_skill(SKILL), [])

    def test_declares_framework_tag_and_substance(self):
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertIn("`PR-FAQ`", body)                 # provenance tag
        self.assertIn("working backwards", body.lower())
        self.assertIn("press release", body.lower())
        self.assertGreater(len(body), 4000)

    def test_always_on_gate_framing_is_softened(self):
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertNotIn("Hard Gate", body)
