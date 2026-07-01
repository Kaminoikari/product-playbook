import unittest, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from validate_skill import validate_skill

META = "skills/product-playbook/SKILL.md"

class TestMetaSkill(unittest.TestCase):
    def test_is_a_real_file_not_symlink(self):
        p = pathlib.Path(META)
        self.assertTrue(p.is_file() and not p.is_symlink())

    def test_passes_validator(self):
        self.assertEqual(validate_skill(META), [])

    def test_has_required_anchors(self):
        body = pathlib.Path(META).read_text(encoding="utf-8")
        for anchor in ["## Relative guardrails", "— Frameworks:", "references/",
                       "Available lenses", "Ground in evidence", "Sources:"]:
            self.assertIn(anchor, body, f"missing anchor: {anchor}")

    def test_has_no_mode_menu(self):
        body = pathlib.Path(META).read_text(encoding="utf-8")
        self.assertNotIn("Quick Mode", body)
        self.assertNotIn("Full Mode", body)
