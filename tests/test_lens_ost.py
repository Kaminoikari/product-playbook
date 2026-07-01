# tests/test_lens_ost.py
import unittest, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from validate_skill import validate_skill

SKILL = "skills/opportunity-solution-tree/SKILL.md"

class TestOstLens(unittest.TestCase):
    def test_passes_validator(self):
        self.assertEqual(validate_skill(SKILL), [])

    def test_declares_framework_tag_and_substance(self):
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertIn("OST", body)                # provenance tag
        self.assertIn("opportunity", body.lower())
        self.assertIn("outcome", body.lower())
        self.assertGreater(len(body), 800)

    def test_excludes_journey_map_scope(self):
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertNotIn("Journey Map", body)


if __name__ == "__main__":
    unittest.main()
