# tests/test_lens_product_spec_summary.py
import unittest, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from validate_skill import validate_skill

SKILL = "skills/product-spec-summary/SKILL.md"

class TestProductSpecSummaryLens(unittest.TestCase):
    def test_passes_validator(self):
        self.assertEqual(validate_skill(SKILL), [])

    def test_declares_tag_and_substance(self):
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertIn("`Risk Register`", body)
        self.assertIn("blind spot", body.lower())
        self.assertIn("spec", body.lower())
        self.assertGreater(len(body), 3000)
