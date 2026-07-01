import json, pathlib, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
NEW_DESC_HEAD = "MUST use when the user wants to plan, strategize, validate, or scope"
BANNED = ("22 PM frameworks", "6 modes", "multi-language")

def _load(p): return json.loads((ROOT / p).read_text(encoding="utf-8"))

class TestP4Packaging(unittest.TestCase):
    def test_all_three_versions_are_2_0_0(self):
        self.assertEqual(_load("package.json")["version"], "2.0.0")
        self.assertEqual(_load(".claude-plugin/plugin.json")["version"], "2.0.0")
        mkt = _load(".claude-plugin/marketplace.json")
        self.assertEqual(mkt["plugins"][0]["version"], "2.0.0")

    def test_descriptions_are_outcome_first_and_synced(self):
        p = _load(".claude-plugin/plugin.json")["description"]
        m = _load(".claude-plugin/marketplace.json")["plugins"][0]["description"]
        k = _load("package.json")["description"]
        self.assertEqual(p, m); self.assertEqual(p, k)
        self.assertTrue(p.startswith(NEW_DESC_HEAD), p[:60])
        for banned in BANNED:
            self.assertNotIn(banned, p, banned)

    def test_meta_skill_recipe_path_uses_plugin_root(self):
        body = (ROOT / "skills/product-playbook/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("${CLAUDE_PLUGIN_ROOT}/references/recipes/", body)

    def test_document_export_assets_use_skill_dir(self):
        body = (ROOT / "skills/document-export/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("${CLAUDE_SKILL_DIR}/assets/", body)
        # the runtime read instruction no longer uses a bare assets/ path
        import re
        self.assertNotRegex(body, r"reads `assets/prd-style\.css`")
