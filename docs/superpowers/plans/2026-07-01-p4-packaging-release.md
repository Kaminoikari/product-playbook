# P4 — Packaging & Release Prep Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the published package reflect the lens architecture: bump to 2.0.0 across the three manifests with an outcome-first description, rewrite `install.sh` to the skills-directory-plugin model, delete the superseded root `SKILL.md`, make runtime cross-file skill references resolve under a plugin install, and overhaul `README.md`.

**Architecture:** The plugin is delivered two ways: marketplace (`.claude-plugin/*.json` + auto-discovered `skills/`, `hooks/`, `agents/`) and a `curl | bash` `install.sh`. Post-refactor, the cleanest manual install is a **skills-directory plugin**: copy the whole repo (which already carries `.claude-plugin/plugin.json`) into `~/.claude/skills/product-playbook/`; Claude Code then loads it in place as a full personal-scoped plugin (`/product-playbook:<lens>`), with `hooks/hooks.json`, `agents/`, and `references/` all working and `${CLAUDE_PLUGIN_ROOT}` resolving normally. This removes all per-skill / i18n / commands copy logic from `install.sh`.

**Tech Stack:** Python 3 `unittest` (run: `python3 -m unittest discover tests`); Bash installer; JSON manifests.

## Global Constraints

- **Test runner is `unittest`, never pytest.** The full suite (132 after P3) must be green after each task, except where a task intentionally updates/repoints an install-smoke assertion (called out in that task).
- **This is a release-PREP phase, not a release.** Do NOT merge, push, publish to npm, or publish to the marketplace. Bumping the version in-branch is safe because the branch stays unmerged; the npm/marketplace publish is triggered by the maintainer merging to main, which is the user's call. Do not run `npm publish` or `git push`.
- **Version target is exactly `2.0.0`** (major; breaking). It must be identical in all three: `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `package.json`.
- **The description is the skill-triggering text** — keep the `MUST use when …` trigger prefix. Remove the obsolete claims `22 PM frameworks`, `6 modes`, `multi-language`. Use the outcome-first wording given in Task 1 verbatim, identical in all three manifests.
- **`~/.claude/skills/product-playbook` stays the install target** (the skills-directory-plugin dir). `test_install_smoke.py::test_targets_documented_skill_dir` asserts this string — keep it true.
- **Do NOT touch** the lens skill bodies, hooks, recipes, or eval suite (those are P0-P3, done). Task 4 edits only the two runtime cross-file read INSTRUCTIONS (not the migration-provenance HTML comments).
- **New/edited prose follows the copy rules** (no mid-sentence em-dash except headings/`— Frameworks:`/nameplate ` — `; no "rather than"/"instead of"/"X, not Y"; full-width CJK for CJK). README is English.

---

## Task 1: Bump to 2.0.0 + outcome-first description across the three manifests

**Files:**
- Modify: `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `package.json`
- Test: `tests/test_p4_packaging.py` (new)

**Interfaces:** `package.json` also carries the `files` allowlist — the `"SKILL.md"` entry is removed in Task 3 (with the root file's deletion), NOT here. This task changes only `version`, `description`, and `keywords`.

**The exact new description** (identical string in all three manifests):
```
MUST use when the user wants to plan, strategize, validate, or scope a product or feature. Composable product-thinking lenses (JTBD, PR-FAQ, positioning, pre-mortem, RICE, North Star, MVP, GTM, and more) that snap to the outcome and blend when the situation needs it, from raw idea to dev handoff.
```

- [ ] **Step 1: Write the failing test** `tests/test_p4_packaging.py`:

```python
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
```

- [ ] **Step 2:** Run `python3 -m unittest tests.test_p4_packaging -v` → expect FAIL.
- [ ] **Step 3:** Edit the three files: set `version` to `"2.0.0"` (in marketplace.json it is `plugins[0].version`); set `description` to the exact new string above in all three (in marketplace.json it is `plugins[0].description`); in `.claude-plugin/plugin.json` update `keywords` from `[..., "i18n"]` to drop `"i18n"` and add `"strategy"` and `"pr-faq"` → `["product-management", "planning", "pm", "jtbd", "prd", "mvp", "strategy", "pr-faq"]`. Keep all other fields (name, author, homepage, repository, license, source) unchanged. Keep valid JSON.
- [ ] **Step 4:** Run `python3 -m unittest tests.test_p4_packaging -v` → PASS. Run `python3 -m unittest discover tests` → green (`test_install_smoke.py::test_plugin_version_matches_package_version` now confirms 2.0.0 == 2.0.0).
- [ ] **Step 5: Commit** `chore: bump to 2.0.0 + outcome-first description across the three manifests`

## Task 2: Rewrite `install.sh` to the skills-directory-plugin model

**Files:**
- Modify: `install.sh`, `tests/test_install_smoke.py`
- Test: `tests/test_install_smoke.py` (its `TestInstallScriptShape` class)

**Interfaces:** The rewritten installer copies the WHOLE repo tree (which already contains `.claude-plugin/plugin.json`, `skills/`, `hooks/`, `agents/`, `references/`, `LICENSE`) into `$HOME/.claude/skills/product-playbook/`, then instructs the user to restart or run `/reload-plugins`. It no longer copies individual skills, commands, or agents to separate locations, and has no i18n/language logic. Keep: `#!/usr/bin/env bash`, `set -euo pipefail`, the `--uninstall` flag (removes the install dir), `--help`, `--update`, the local-repo-vs-remote-clone source detection, and the `.version` up-to-date check. Drop: `--lang`, `SUPPORTED_LANGS`, `detect_language()`, the bilingual `msg()` table (English-only messages now), `COMMANDS_DIR` + slash-command copy, the separate `~/.claude/agents/` copy, the `i18n/` copy, and the root-`SKILL.md` copy.

- [ ] **Step 1: Update the install-smoke tests first.** In `tests/test_install_smoke.py`:
  - Delete `test_supports_lang_selection` (the `--lang` flag is removed).
  - Add a new test to `TestInstallScriptShape` asserting the new model:

```python
    def test_installs_as_skills_directory_plugin(self):
        # new model: copy the whole plugin (incl. its manifest) into the skills dir
        self.assertIn(".claude/skills/product-playbook", self.install_sh)
        self.assertNotIn("--lang", self.install_sh)   # i18n installer logic removed
        self.assertNotIn("COMMANDS_DIR", self.install_sh)  # no slash commands to copy
```

  Keep `test_has_shebang_and_strict_mode`, `test_supports_uninstall`, `test_targets_documented_skill_dir` unchanged.
- [ ] **Step 2:** Run `python3 -m unittest tests.test_install_smoke -v` → expect FAIL (old install.sh still has `--lang`/`COMMANDS_DIR`).
- [ ] **Step 3:** Rewrite `install.sh`. Structure:
  - Header comment + usage examples (drop the `--lang` lines).
  - Colors, constants (`REPO_URL`, `TMP_DIR`, `SKILL_DIR="$HOME/.claude/skills/product-playbook"`; drop `COMMANDS_DIR`, `SUPPORTED_LANGS`, `INSTALL_LANG`).
  - English-only `info/ok/warn/err` helpers; drop `detect_language()` and `msg()`.
  - `usage()` documents `install` / `--update` / `--uninstall` / `--help`; paths line shows only `Skill/plugin → ~/.claude/skills/product-playbook/`.
  - `do_uninstall()`: `rm -rf "$SKILL_DIR"` (no commands loop).
  - `do_install()`: detect source dir (local repo if the script sits next to `.claude-plugin/plugin.json`, else `git clone --depth 1` to `TMP_DIR`); read `pkg_version` from `package.json`; `.version` up-to-date short-circuit; `rm -rf "$SKILL_DIR"` then `mkdir -p`; copy the whole tree EXCLUDING dev artifacts (`.git`, `node_modules`, `docs`, `logs`, `tests`, `evals`, `scripts`, `.superpowers`) into `$SKILL_DIR` (a `cp -R` of the needed top-level entries — at minimum `.claude-plugin`, `skills`, `hooks`, `agents`, `references`, `LICENSE`, `README.md`, `package.json`); write `.version`; print success + the `/reload-plugins`-or-restart instruction and a `/product-playbook` usage hint.
  - `main()`: arg parsing WITHOUT `--lang`; dispatch `--uninstall` / `--update` / `--help` / default install.
- [ ] **Step 4:** Run `python3 -m unittest tests.test_install_smoke -v` → PASS. Lint the script parses: `bash -n install.sh` (expect no output, exit 0). Run `python3 -m unittest discover tests` → green.
- [ ] **Step 5: Commit** `refactor: rewrite install.sh as a skills-directory plugin installer (drop per-skill/i18n/commands copy)`

## Task 3: Delete the superseded root `SKILL.md` + repoint its consumers

**Files:**
- Delete: `SKILL.md` (repo root)
- Modify: `package.json` (the `files` allowlist), `tests/test_install_smoke.py`
- Test: `tests/test_install_smoke.py`

**Interfaces:** The root `SKILL.md` is the old 6-mode orchestrator. Plugin discovery loads skills from `skills/` only, so the root file is never loaded as a skill — it is dead weight, and its `name: product-playbook` duplicates the meta-skill `skills/product-playbook/SKILL.md`. The real entry point is the meta-skill. After Task 2, `install.sh` no longer copies the root file.

- [ ] **Step 1: Update the tests first.** In `tests/test_install_smoke.py`:
  - In `test_required_user_facing_dirs_in_allowlist`, remove `"SKILL.md"` from the `required` tuple → `(".claude-plugin/", "skills/", "agents/", "references/")`.
  - Repoint `TestCriticalUserFacingFiles` to the meta-skill: change both methods to target `skills/product-playbook/SKILL.md` instead of the root `SKILL.md`:

```python
class TestCriticalUserFacingFiles(unittest.TestCase):
    META = "skills/product-playbook/SKILL.md"
    def test_meta_skill_exists(self):
        self.assertTrue((REPO_ROOT / self.META).is_file(),
                         "meta-skill is the entry point — must exist")
    def test_meta_skill_has_frontmatter(self):
        text = (REPO_ROOT / self.META).read_text()
        self.assertTrue(text.startswith("---\n"))
        self.assertIn("\n---\n", text[3:])
```

- [ ] **Step 2:** Run `python3 -m unittest tests.test_install_smoke -v` → expect FAIL if root `SKILL.md` is still listed as required, or PASS-then-verify (delete drives it). Actually run after Step 3 to see it go green.
- [ ] **Step 3:** `git rm SKILL.md`. In `package.json`, remove the `"SKILL.md",` entry from the `files` array. Keep valid JSON.
- [ ] **Step 4:** Run `python3 -m unittest tests.test_install_smoke -v` → PASS. Run `python3 -m unittest discover tests` → green. Confirm nothing else references the root file: `grep -rn "src_dir/SKILL.md\|REPO_ROOT / \"SKILL.md\"\|\"SKILL.md\"" install.sh package.json tests/` should show no live consumer expecting the ROOT file (skills/ paths are fine).
- [ ] **Step 5: Commit** `refactor: delete superseded root SKILL.md (old 6-mode orchestrator); meta-skill is the entry point`

## Task 4: Make runtime cross-file skill references resolve under a plugin install

**Files:**
- Modify: `skills/product-playbook/SKILL.md`, `skills/document-export/SKILL.md`
- Test: `tests/test_p4_packaging.py` (extend)

**Interfaces:** Only TWO runtime read INSTRUCTIONS point at sibling files; both currently use a bare relative path that the model cannot resolve to an absolute path under a plugin cache. Fix them with the documented substitutions: `${CLAUDE_PLUGIN_ROOT}` (plugin root) for the recipe docs at repo root, and `${CLAUDE_SKILL_DIR}` (the skill's own dir) for `document-export`'s bundled `assets/`. Do NOT touch the `<!-- migrated from references/… -->` provenance comments (audit trail, never read at runtime). `validate_skill` must still return `[]` for both.

- [ ] **Step 1: Add failing test** to `tests/test_p4_packaging.py`:

```python
    def test_meta_skill_recipe_path_uses_plugin_root(self):
        body = (ROOT / "skills/product-playbook/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("${CLAUDE_PLUGIN_ROOT}/references/recipes/", body)

    def test_document_export_assets_use_skill_dir(self):
        body = (ROOT / "skills/document-export/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("${CLAUDE_SKILL_DIR}/assets/", body)
        # the runtime read instruction no longer uses a bare assets/ path
        import re
        self.assertNotRegex(body, r"reads `assets/prd-style\.css`")
```

- [ ] **Step 2:** Run → FAIL.
- [ ] **Step 3:** Edit:
  - `skills/product-playbook/SKILL.md` (~line 72): change the sentence so the recipe path reads `${CLAUDE_PLUGIN_ROOT}/references/recipes/<name>.md` (keep the four filenames + the "read once the user accepts" guidance).
  - `skills/document-export/SKILL.md` (~lines 179, 187): change `Claude reads \`assets/prd-style.css\`` → `Claude reads \`${CLAUDE_SKILL_DIR}/assets/prd-style.css\``, and the inline-CSS instruction `Read the full contents of assets/prd-style.css` → `Read the full contents of ${CLAUDE_SKILL_DIR}/assets/prd-style.css`. Apply the same to any `assets/report-style.css` runtime read instruction in this file. Leave the migration-provenance comment untouched.
- [ ] **Step 4:** Run `python3 -m unittest tests.test_p4_packaging -v` → PASS. Verify both skills still validate: `python3 -c "import sys; sys.path.insert(0,'scripts'); from validate_skill import validate_skill; print(validate_skill('skills/product-playbook/SKILL.md'), validate_skill('skills/document-export/SKILL.md'))"` → expect `[] []`. Run `python3 -m unittest discover tests` → green.
- [ ] **Step 5: Commit** `fix: resolve runtime cross-file skill refs via CLAUDE_PLUGIN_ROOT / CLAUDE_SKILL_DIR`

## Task 5: Overhaul `README.md` for the lens architecture

**Files:**
- Modify: `README.md`
- Test: `tests/test_p4_packaging.py` (extend)

**Interfaces:** The current README describes the old system (6 modes, `/product-full`-style slash commands, 22 frameworks, multi-language, the deleted translated READMEs). Rewrite it to describe the lens architecture. It stays English-only (translations were deleted in P3).

**Required README content** (author full prose; this is the outline, not placeholder text):
- Title + one-line positioning: outcome-first product-thinking lenses for Claude Code.
- What it is: a plugin of composable lens skills (name JTBD, PR-FAQ, positioning, pre-mortem, RICE/solution-prioritization, North Star/success-metrics, MVP scoping, PMF/GTM, strategy-kernel, and the rest) plus a meta-skill that reads the user's outcome, picks the lens(es) — single or blended — and tags a provenance line (`— Frameworks: …`). Mention the relative, non-blocking guardrails and runtime language detection.
- Install: (1) marketplace / `/plugin` install (recommended), (2) `curl | bash install.sh` which installs it as a personal skills-directory plugin into `~/.claude/skills/product-playbook/` (then `/reload-plugins`). Show the uninstall command.
- Usage: just describe the outcome ("help me figure out what job users hire my app for") and the right lens triggers; the four recipes (full-product-plan / quick-validation / product-revision / feature-extension) as optional depth.
- Remove: all `/product-*` slash-command references, the "6 modes" section, the "22 frameworks" count framing, the multi-language / translated-README cross-links.

- [ ] **Step 1: Add failing test** to `tests/test_p4_packaging.py`:

```python
    def test_readme_is_lens_architecture(self):
        body = (ROOT / "README.md").read_text(encoding="utf-8")
        # obsolete system vocabulary is gone
        for banned in ("/product-full", "/product-quick", "6 modes", "22 PM frameworks",
                       "README.zh-TW.md", "README.ja.md"):
            self.assertNotIn(banned, body, banned)
        # new architecture is described
        for needed in ("lens", "provenance", "reload-plugins"):
            self.assertIn(needed, body, needed)
```

- [ ] **Step 2:** Run → FAIL.
- [ ] **Step 3:** Rewrite `README.md` per the outline above. Follow the copy rules. Keep the badge/header block if present but update any version/mode text.
- [ ] **Step 4:** Run `python3 -m unittest tests.test_p4_packaging -v` → PASS. Run `python3 -m unittest discover tests` → all green.
- [ ] **Step 5: Commit** `docs: overhaul README for the lens architecture (drop modes/slash-commands/i18n)`

---

## After all 5 tasks

- [ ] **Final whole-branch review** (superpowers:requesting-code-review, most capable model) over the P4 range. Focus: 2.0.0 synced in all three manifests with a clean outcome-first description; `install.sh` is a correct skills-directory-plugin installer that parses (`bash -n`), copies the manifest + skills + hooks + agents + references, excludes dev artifacts, and still supports uninstall; no live consumer references the deleted root `SKILL.md`; the two runtime cross-file refs use the substitution vars and both skills validate; README has no obsolete-system vocabulary.
- [ ] Fix Critical/Important via one fix subagent; record Minors in the ledger.
- [ ] **superpowers:finishing-a-development-branch** — this is the LAST implementation phase; present the finish options. Do NOT publish/merge without the user's explicit choice (the merge is what triggers npm + marketplace publish).
- Deferred beyond P4 (not release-blocking): the copy-cleanup pass for verbatim lens-body copy-rule issues (spec §8); the doc-only `discovery-specialist` mentions in `agents/pre-mortem-runner.md` + `strategy-critic.md` frontmatter and the dedup decision for those two agents vs their lens versions; `scripts/suppress-pair.py` / `_suppressions.py` docstring examples; P-research external-research fan-out.

## Self-Review (author checklist, done)

- **Spec coverage:** §5 P4 (version bump + description rewrite across 3 manifests; install.sh layout; delete old root SKILL.md; README) all mapped to Tasks 1-5, plus the ${CLAUDE_PLUGIN_ROOT} correctness fix (Task 4) surfaced by the install-mechanics investigation. ✓
- **Release safety:** every task explicitly stays in-branch; no publish/merge/push; the finish gate is deferred to the user's choice. The npm-publish-on-merge coupling is called out. ✓
- **Test-coupling safety:** each install-smoke assertion that P4 invalidates (`--lang`, root `SKILL.md` existence + allowlist) is updated in the SAME task that invalidates it, tests-first; the version-sync test guards the 2.0.0 bump. ✓
- **No placeholders:** exact version string, exact description string, exact keywords, exact test code, README outline with concrete required/banned tokens, exact commit messages. ✓
