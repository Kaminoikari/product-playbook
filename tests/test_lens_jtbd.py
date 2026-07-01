# tests/test_lens_jtbd.py
import unittest, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from validate_skill import validate_skill

SKILL = "skills/jtbd/SKILL.md"

class TestJtbdLens(unittest.TestCase):
    def test_passes_validator(self):
        self.assertEqual(validate_skill(SKILL), [])

    def test_declares_framework_tag_and_substance(self):
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertIn("`JTBD`", body)          # provenance tag
        self.assertIn("job", body.lower())     # migrated substance, not a stub
        self.assertGreater(len(body), 1500)
        self.assertNotIn("Hard Gate", body)    # softened to a proportional quality self-check
