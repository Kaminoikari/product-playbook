# tests/test_lens_mvp_scoping.py
import unittest, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from validate_skill import validate_skill

SKILL = "skills/mvp-scoping/SKILL.md"

class TestMvpScopingLens(unittest.TestCase):
    def test_passes_validator(self):
        self.assertEqual(validate_skill(SKILL), [])

    def test_declares_tags_and_substance(self):
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertIn("`MVP`", body)
        self.assertIn("`User Story`", body)
        self.assertIn("not doing", body.lower())
        self.assertIn("parallel", body.lower())
        self.assertGreater(len(body), 1200)
