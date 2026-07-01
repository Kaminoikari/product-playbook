# tests/test_lens_prd_and_handoff.py
import unittest, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from validate_skill import validate_skill

SKILL = "skills/prd-and-handoff/SKILL.md"

class TestPrdAndHandoffLens(unittest.TestCase):
    def test_passes_validator(self):
        self.assertEqual(validate_skill(SKILL), [])

    def test_declares_tags_and_substance(self):
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertIn("`PRD`", body)
        self.assertIn("`Handoff`", body)
        self.assertIn("tasks.md", body.lower())
        self.assertIn("architecture", body.lower())
        self.assertGreater(len(body), 20000)

    def test_security_reframed_not_hard_gate(self):
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertIn("security", body.lower())          # content kept
        self.assertNotIn("Hard Gate", body)               # always-on framing removed


if __name__ == "__main__":
    unittest.main()
