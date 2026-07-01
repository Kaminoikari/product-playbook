"""K9: install.sh / plugin shipping smoke test.

Pure-structural checks on the artifacts that get shipped to end users —
catches the class of bug where a refactor accidentally moves a file out of
the npm package's `files` allowlist or breaks the plugin manifest.

Does NOT actually run `install.sh` (it would mutate ~/.claude/skills). The
goal is "would a fresh install have what it needs?", verified by inspecting
the repo state.

Runs alongside the closed-loop tests via:
  python3 -m unittest tests/test_install_smoke.py
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestPackageShape(unittest.TestCase):
    def setUp(self):
        self.pkg = json.loads((REPO_ROOT / "package.json").read_text())

    def test_version_is_semver(self):
        v = self.pkg["version"]
        self.assertRegex(v, r"^\d+\.\d+\.\d+(-[\w.]+)?$",
                          f"version {v!r} is not semver")

    def test_files_allowlist_excludes_dev_artifacts(self):
        # closed-loop dev artifacts must NOT ship to npm consumers
        files = self.pkg["files"]
        for forbidden in ("docs/", "scripts/", "logs/", "evals/", "tests/"):
            self.assertFalse(any(f.startswith(forbidden) for f in files),
                              f"{forbidden!r} should not be in package.json files")

    def test_required_user_facing_dirs_in_allowlist(self):
        files = self.pkg["files"]
        # canonical user-facing entry points; if any of these go missing,
        # the plugin install will silently break
        for required in (".claude-plugin/", "skills/", "SKILL.md",
                          "agents/", "references/"):
            self.assertIn(required, files,
                           f"{required!r} missing from package.json files — "
                           f"plugin consumers won't get it")


class TestPluginManifest(unittest.TestCase):
    def test_plugin_json_parses(self):
        manifest_path = REPO_ROOT / ".claude-plugin" / "plugin.json"
        self.assertTrue(manifest_path.is_file(), "plugin.json missing")
        data = json.loads(manifest_path.read_text())
        # minimum required keys for a plugin
        self.assertIn("name", data)
        self.assertIn("version", data)

    def test_marketplace_json_parses(self):
        m = REPO_ROOT / ".claude-plugin" / "marketplace.json"
        self.assertTrue(m.is_file(), "marketplace.json missing")
        json.loads(m.read_text())

    def test_plugin_version_matches_package_version(self):
        plugin = json.loads(
            (REPO_ROOT / ".claude-plugin" / "plugin.json").read_text())
        pkg = json.loads((REPO_ROOT / "package.json").read_text())
        self.assertEqual(plugin.get("version"), pkg["version"],
                          "plugin.json version drifted from package.json — "
                          "users will see inconsistent version strings")


class TestInstallScriptShape(unittest.TestCase):
    def setUp(self):
        self.install_sh = (REPO_ROOT / "install.sh").read_text()

    def test_has_shebang_and_strict_mode(self):
        self.assertTrue(self.install_sh.startswith("#!/usr/bin/env bash"),
                          "install.sh must have bash shebang")
        self.assertIn("set -euo pipefail", self.install_sh,
                       "install.sh must run in strict mode")

    def test_supports_uninstall(self):
        # users rely on `bash install.sh --uninstall` for a clean removal
        self.assertIn("--uninstall", self.install_sh,
                       "install.sh missing --uninstall flag")

    def test_targets_documented_skill_dir(self):
        # MUST install into ~/.claude/skills/product-playbook
        self.assertIn("HOME", self.install_sh)
        self.assertIn(".claude/skills/product-playbook", self.install_sh,
                       "install.sh skill directory has changed — update docs "
                       "or the install script")

    def test_installs_as_skills_directory_plugin(self):
        # new model: copy the whole plugin (incl. its manifest) into the skills dir
        self.assertIn(".claude/skills/product-playbook", self.install_sh)
        self.assertNotIn("--lang", self.install_sh)   # i18n installer logic removed
        self.assertNotIn("COMMANDS_DIR", self.install_sh)  # no slash commands to copy


class TestCriticalUserFacingFiles(unittest.TestCase):
    def test_skill_md_exists(self):
        self.assertTrue((REPO_ROOT / "SKILL.md").is_file(),
                         "SKILL.md is the entry point — must exist")

    def test_skill_md_has_frontmatter(self):
        # Claude Code skill loader requires YAML frontmatter
        text = (REPO_ROOT / "SKILL.md").read_text()
        self.assertTrue(text.startswith("---\n"),
                         "SKILL.md must begin with YAML frontmatter")
        self.assertIn("\n---\n", text[3:],
                       "SKILL.md frontmatter must be closed by ---")


if __name__ == "__main__":
    unittest.main()
