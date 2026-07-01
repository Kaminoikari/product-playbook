# tests/test_lens_pmf_gtm.py
import unittest, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from validate_skill import validate_skill

SKILL = "skills/pmf-gtm/SKILL.md"

class TestPmfGtmLens(unittest.TestCase):
    def test_passes_validator(self):
        self.assertEqual(validate_skill(SKILL), [])

    def test_declares_framework_tags_and_substance(self):
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertIn("`PMF`", body)                       # provenance tag
        self.assertIn("`GTM`", body)                       # provenance tag
        self.assertIn("product-market fit", body.lower())  # migrated substance
        self.assertIn("pricing", body.lower())              # migrated substance
        self.assertGreater(len(body), 3500)
