# tests/test_lens_document_export.py
import unittest, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from validate_skill import validate_skill

SKILL = "skills/document-export/SKILL.md"

class TestDocumentExportLens(unittest.TestCase):
    def test_passes_validator(self):
        self.assertEqual(validate_skill(SKILL), [])

    def test_declares_framework_tag_and_substance(self):
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertIn("`HTML Report`", body)   # provenance tag
        self.assertIn("pdf", body.lower())     # migrated substance, not a stub
        self.assertIn("report", body.lower())  # migrated substance, not a stub
        self.assertGreater(len(body), 6000)

    def test_css_assets_bundled(self):
        self.assertTrue(pathlib.Path("skills/document-export/assets/prd-style.css").exists())
        self.assertTrue(pathlib.Path("skills/document-export/assets/report-style.css").exists())

    def test_old_asset_path_is_gone(self):
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertNotIn("references/templates/", body)
