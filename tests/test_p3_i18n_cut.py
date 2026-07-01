import json, pathlib, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]

class TestP3I18nCut(unittest.TestCase):
    def test_i18n_dir_and_scripts_gone(self):
        for p in ["i18n", "scripts/i18n-drift-report.py", "scripts/i18n-mirror-apply.py",
                  "evals/evals-zh-TW.json", ".github/workflows/i18n-drift-check.yml"]:
            self.assertFalse((ROOT / p).exists(), p)

    def test_translated_readmes_gone_english_kept(self):
        self.assertTrue((ROOT / "README.md").is_file())
        for suffix in (".es", ".ja", ".ko", ".zh-CN", ".zh-TW"):
            self.assertFalse((ROOT / f"README{suffix}.md").exists(), suffix)

    def test_package_json_no_dangling_i18n(self):
        pkg = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        for s in ("i18n:drift", "i18n:mirror", "eval:zh-TW"):
            self.assertNotIn(s, pkg.get("scripts", {}), s)
        files = pkg.get("files", [])
        for f in ("i18n/", "README.zh-TW.md", "README.ja.md", "README.zh-CN.md",
                  "README.es.md", "README.ko.md"):
            self.assertNotIn(f, files, f)

    def test_loop_machinery_no_dead_i18n_script_refs(self):
        for rel in ["scripts/loop-tick.py", "scripts/loop-status.py",
                    "scripts/eval-lift-report.py"]:
            src = (ROOT / rel).read_text(encoding="utf-8")
            self.assertNotIn("i18n-mirror-apply", src, rel)
            self.assertNotIn("i18n-drift-report", src, rel)

    def test_watched_lists_drop_i18n(self):
        for rel in ["scripts/_config.py", "scripts/_freshness.py"]:
            src = (ROOT / rel).read_text(encoding="utf-8")
            # the WATCHED list must no longer contain a bare "i18n" path entry
            self.assertNotIn('"i18n"', src, rel)
