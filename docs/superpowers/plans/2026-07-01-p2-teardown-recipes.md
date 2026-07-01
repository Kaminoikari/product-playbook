# P2 — Orchestration Teardown + Recipes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Clear the legacy 6-mode orchestration layer now that all 16 lens skills exist, and replace its "带路" value with 4 optional recipe reference docs the meta-skill suggests situationally.

**Architecture:** The new system (meta-skill + 16 lens skills + SessionStart inject hook + guardrail hooks) is already decoupled from the old orchestration except for one link: the meta-skill's `references/`/`agents/` fallback line. P2 removes that link, deletes the mode-spine files + the specialist-dispatch hook + the discovery-specialist agent + the old slash commands, adapts the two remaining guardrail hooks off their deleted dependencies, and adds `references/recipes/*.md`. Packaging-coupled artifacts (root `SKILL.md`, `install.sh`, READMEs, i18n) stay for P3/P4.

**Tech Stack:** Python 3 `unittest` (run: `python3 -m unittest discover tests -v`); `scripts/validate_skill.py`.

## Global Constraints

- **Test runner is `unittest`, never pytest.** Discoverable by `python3 -m unittest discover tests`.
- **The full suite is 116 tests before P2 and must stay green** after each task (except where a task intentionally updates an assertion, called out in that task).
- **Guardrails stay non-blocking.** The two retained hooks (`pre-write-planning-gate.py`, `user-prompt-detect-topic-switch.py`) must remain advisory (emit `systemMessage`, never set a blocking `permissionDecision`), per spec §4.5 relative-guardrails.
- **New/edited prose follows the copy rules** (no mid-sentence em-dash except headings/`— Frameworks:`; no "rather than"/"instead of"/"X, not Y"; full-width CJK for CJK).
- **Do NOT touch packaging/i18n artifacts** (root `SKILL.md`, `install.sh`, `README*.md`, `i18n/`, `plugin.json`, `marketplace.json`): those are P3/P4. Deleting P2 files may leave dangling references inside those P3/P4 files; that is expected and acceptable.
- **Recipe form is decided:** 4 reference docs under `references/recipes/`, suggested by the meta-skill. NOT slash commands, NOT skill files.
- **Deletion scope is decided (spec-aligned full teardown):** delete the specialist-dispatch hook, `agents/discovery-specialist.md`, all `commands/*.md`, and the 11 mode-spine reference files listed in Task 2.

---

## Task 1: Delete the specialist-dispatch hook + discovery-specialist agent

**Files:**
- Delete: `hooks/user-prompt-detect-specialist-dispatch.py`, `agents/discovery-specialist.md`
- Modify: `hooks/hooks.json` (remove the specialist-dispatch entry from `UserPromptSubmit`, leaving `user-prompt-detect-topic-switch.py`)
- Test: `tests/test_p2_teardown.py` (new)

**Interfaces:** The new system does not reference `discovery-specialist` outside the dispatch hook (verified). `pre-mortem-runner` and `strategy-critic` agents are KEPT (they are framework subagents, now also lenses; dedup is a later decision).

- [ ] **Step 1: Write failing test** `tests/test_p2_teardown.py`:

```python
import json, pathlib, unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class TestP2Teardown(unittest.TestCase):
    def test_dispatch_hook_deleted(self):
        self.assertFalse((ROOT / "hooks" / "user-prompt-detect-specialist-dispatch.py").exists())

    def test_discovery_specialist_deleted(self):
        self.assertFalse((ROOT / "agents" / "discovery-specialist.md").exists())

    def test_hooks_json_valid_and_no_dispatch(self):
        cfg = json.loads((ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8"))
        blob = json.dumps(cfg)
        self.assertNotIn("specialist-dispatch", blob)
        # topic-switch and the two session-start hooks + planning-gate remain
        self.assertIn("user-prompt-detect-topic-switch.py", blob)
        self.assertIn("session-start-inject-metaskill.py", blob)
```

- [ ] **Step 2:** Run `python3 -m unittest tests.test_p2_teardown -v` → expect FAIL (files still exist).
- [ ] **Step 3:** `git rm hooks/user-prompt-detect-specialist-dispatch.py agents/discovery-specialist.md`. Edit `hooks/hooks.json`: remove the `{ "type": "command", "command": "…user-prompt-detect-specialist-dispatch.py", "timeout": 5 }` object from the `UserPromptSubmit` hooks array (keep the topic-switch object). Keep valid JSON.
- [ ] **Step 4:** Run the test → PASS. Run `python3 -m unittest discover tests` → still green (existing hook tests unaffected).
- [ ] **Step 5: Commit** `refactor: remove 6-mode specialist-dispatch hook + discovery-specialist agent`

## Task 2: Delete old slash commands + mode-spine reference files

**Files:**
- Delete: `commands/product-build.md`, `commands/product-dev.md`, `commands/product-feature.md`, `commands/product-full.md`, `commands/product-prd.md`, `commands/product-quick.md`, `commands/product-report.md`, `commands/product-revision.md`
- Delete (11 mode-spine reference files): `references/rules-full.md`, `references/rules-quick.md`, `references/rules-revision.md`, `references/rules-custom.md`, `references/rules-build.md`, `references/rules-product-type.md`, `references/rules-optional-trigger.md`, `references/rules-progress.md`, `references/rules-end-of-flow.md`, `references/rules-subagent-dispatch.md`, `references/rules-commands.md`
- Test: extend `tests/test_p2_teardown.py`

**Interfaces:** KEEP these reference files (still used by the new system / guardrails / lenses, not mode-spine): `rules-change-propagation.md` (used by `user-prompt-detect-topic-switch.py`), `rules-export-document.md`, `rules-quality-review.md`, `rules-context*.md`, `rules-document-tools.md`, `rules-file-integration.md`, `rules-import-document.md`, and the framework content files `00-08*.md` / `02a-c*.md` (redundant post-migration but out of P2 orchestration scope). The kept `rules-change-propagation.md` must remain reachable.

- [ ] **Step 1: Add failing tests** to `tests/test_p2_teardown.py`:

```python
    def test_slash_commands_deleted(self):
        self.assertFalse((ROOT / "commands").exists() and any((ROOT / "commands").glob("product-*.md")))

    def test_mode_spine_refs_deleted(self):
        gone = ["rules-full", "rules-quick", "rules-revision", "rules-custom", "rules-build",
                "rules-product-type", "rules-optional-trigger", "rules-progress",
                "rules-end-of-flow", "rules-subagent-dispatch", "rules-commands"]
        for name in gone:
            self.assertFalse((ROOT / "references" / f"{name}.md").exists(), name)

    def test_change_propagation_kept(self):
        self.assertTrue((ROOT / "references" / "rules-change-propagation.md").exists())

    def test_new_system_has_no_reference_to_deleted_orchestration(self):
        # The runtime new system (skills/) must not reference any deleted mode-spine file.
        # NOTE: grep skills/ ONLY — test files legitimately name the deleted files to assert
        # their absence, and hooks/ still references rules-progress until Task 4 adapts it.
        import subprocess
        pattern = r"rules-(full|quick|revision|custom|build|product-type|optional-trigger|progress|end-of-flow|subagent-dispatch|commands)\b"
        hits = subprocess.run(["grep", "-rlE", pattern, str(ROOT / "skills")],
                              capture_output=True, text=True).stdout.strip()
        self.assertEqual(hits, "", f"dangling ref in skills/: {hits}")
```

- [ ] **Step 2:** Run `python3 -m unittest tests.test_p2_teardown -v` → expect FAIL.
- [ ] **Step 3:** `git rm` the 8 command files and the 11 mode-spine reference files. (Task 3 and Task 4 remove the retained hooks' references to `rules-progress`; if you run Task 2's `test_new_system_has_no_reference` before Task 4, `hooks/` is excluded from the grep here — only `skills` and `tests` are checked — so ordering is safe. `commands/` may be removed as a whole dir.)
- [ ] **Step 4:** Run the tests → PASS. Run `python3 -m unittest discover tests` → still green.
- [ ] **Step 5: Commit** `refactor: delete 6-mode slash commands + mode-spine reference files`

## Task 3: Adapt `pre-write-planning-gate.py` off the deleted `/product-dev` command

**Files:** Modify `hooks/pre-write-planning-gate.py`; Test: extend `tests/test_p2_teardown.py`

**Interfaces:** This is the codebase-safety guardrail (§4.5). It must stay advisory/non-blocking. It currently keys "dev has started" off a `.product-dev-active` marker that the deleted `/product-dev` command created. Keep the marker as the silence signal, but remove all `/product-dev` command references from the docstring and the emitted message.

- [ ] **Step 1: Add failing test** to `tests/test_p2_teardown.py`:

```python
    def test_planning_gate_no_product_dev_command_ref(self):
        src = (ROOT / "hooks" / "pre-write-planning-gate.py").read_text(encoding="utf-8")
        self.assertNotIn("/product-dev", src)
        self.assertNotIn("permissionDecision", src)  # stays non-blocking
```

- [ ] **Step 2:** Run → FAIL (`/product-dev` still in the file).
- [ ] **Step 3:** Edit `hooks/pre-write-planning-gate.py`: in the module docstring and the emitted `systemMessage` text, remove the `/product-dev` command references. Reword the message so the gate stays useful without the command, e.g. the advisory says the session looks like planning and this write looks like source code, so finish the planning artifacts first, and if development has genuinely started, create a `.product-dev-active` file in the working directory (or just proceed, since this is advisory). Keep the marker check (`.product-dev-active`) as the silence signal. Do not add any blocking `permissionDecision`.
- [ ] **Step 4:** Run the new test → PASS. Run `python3 -m unittest discover tests` → green.
- [ ] **Step 5: Commit** `refactor: decouple planning-gate guardrail from the deleted /product-dev command`

## Task 4: Adapt `user-prompt-detect-topic-switch.py` (drop off-topic branch, keep change-propagation)

**Files:** Modify `hooks/user-prompt-detect-topic-switch.py`; Test: extend `tests/test_p2_teardown.py`

**Interfaces:** The change-propagation branch (points to `references/rules-change-propagation.md`, the consistency guardrail §4.5) is KEPT. The off-topic branch references the deleted `references/rules-progress.md` and the old mode SKILL.md "continue/pause/end" menu; that ceremony is gone in the lean system, so remove the off-topic branch entirely. Hook stays advisory.

- [ ] **Step 1: Add failing test** to `tests/test_p2_teardown.py`:

```python
    def test_topic_switch_change_propagation_kept_offtopic_dropped(self):
        src = (ROOT / "hooks" / "user-prompt-detect-topic-switch.py").read_text(encoding="utf-8")
        self.assertIn("rules-change-propagation", src)   # consistency guardrail kept
        self.assertNotIn("rules-progress", src)          # deleted file no longer referenced
        self.assertNotIn("continue/pause/end", src)      # old mode menu removed
        self.assertNotIn("permissionDecision", src)      # stays non-blocking
```

- [ ] **Step 2:** Run → FAIL.
- [ ] **Step 3:** Edit `hooks/user-prompt-detect-topic-switch.py`: remove the off-topic-detection branch (its patterns, its message referencing SKILL.md's off-topic rule and `rules-progress.md`, and the `continue/pause/end` menu). Keep the change-propagation branch intact (its keyword patterns + the `rules-change-propagation.md` reminder). Update the module docstring to describe a single change-propagation guardrail. Keep it advisory.
- [ ] **Step 4:** Run the new test → PASS. Run `python3 -m unittest discover tests` → green.
- [ ] **Step 5: Commit** `refactor: trim topic-switch hook to the change-propagation guardrail only`

## Task 5: Create the 4 recipe reference docs

**Files:**
- Create: `references/recipes/full-product-plan.md`, `references/recipes/quick-validation.md`, `references/recipes/product-revision.md`, `references/recipes/feature-extension.md`
- Test: extend `tests/test_p2_teardown.py`

**Interfaces:** Each recipe is a suggested LENS SEQUENCE (using the 16 real lens names), from spec §4.6. Recipes are suggested by the meta-skill, never forced, and are not slash commands. Map spec §4.6's "persona → journey-map" to the single `persona-journey` lens.

Sequences (recommended order; `(optional)` steps may be skipped; jump-backs allowed):
- **full-product-plan:** strategy-kernel → persona-journey → opportunity-solution-tree (optional) → jtbd → problem-framing → positioning (optional) → pr-faq → solution-prioritization → mvp-scoping → success-metrics → pmf-gtm (optional) → prd-and-handoff (optional).
- **quick-validation:** jtbd → pr-faq → success-metrics (a one-page direction).
- **product-revision:** current-state inventory (surface assumptions) → problem-framing → pr-faq → pre-mortem (optional) → mvp-scoping → success-metrics (before/after).
- **feature-extension:** problem-framing (with existing-system context) → solution-prioritization → pre-mortem (regression/compatibility) → mvp-scoping.

- [ ] **Step 1: Add failing test** to `tests/test_p2_teardown.py`:

```python
    def test_recipe_docs_exist_with_sequences(self):
        rec = ROOT / "references" / "recipes"
        expected = {
            "full-product-plan.md": ["strategy-kernel", "jtbd", "mvp-scoping", "success-metrics"],
            "quick-validation.md": ["jtbd", "pr-faq", "success-metrics"],
            "product-revision.md": ["problem-framing", "mvp-scoping", "success-metrics"],
            "feature-extension.md": ["problem-framing", "solution-prioritization", "pre-mortem", "mvp-scoping"],
        }
        for fname, lenses in expected.items():
            body = (rec / fname).read_text(encoding="utf-8")
            for lens in lenses:
                self.assertIn(lens, body, f"{fname} missing {lens}")
```

- [ ] **Step 2:** Run → FAIL (files missing).
- [ ] **Step 3:** Create the four docs. Each contains: a one-line "when to suggest this" (mapped from the old mode), the ordered lens sequence with optional steps marked and jump-backs allowed, and a closing line that it is a suggestion (never forced) and not a slash command. Follow the copy rules.
- [ ] **Step 4:** Run the test → PASS. Run `python3 -m unittest discover tests` → green.
- [ ] **Step 5: Commit** `feat: add 4 recipe reference docs (full/quick/revision/feature) as optional depth`

## Task 6: Update the meta-skill — remove the fallback line, point recipes at the docs

**Files:** Modify `skills/product-playbook/SKILL.md`, `tests/test_metaskill.py`; Test: extend `tests/test_p2_teardown.py`

**Interfaces:** All 16 lenses now exist, so the migration fallback line is dead. The `Available lenses` list and the situational table stay. `test_metaskill.py:17` currently asserts a generic `references/` anchor (satisfied today by the fallback line); after removal, the meta-skill's recipe section must reference `references/recipes/` so the anchor stays meaningful, and the test asserts that specific anchor instead.

- [ ] **Step 1: Update `tests/test_metaskill.py`.** In the anchors list (line ~17), replace `"references/"` with `"references/recipes/"`. Add a new test asserting the fallback is gone:

```python
    def test_migration_fallback_removed(self):
        body = pathlib.Path(META).read_text(encoding="utf-8")
        self.assertNotIn("no lens skill yet", body)
        self.assertNotIn("Fallback during migration", body)
```

- [ ] **Step 2: Add a failing test** to `tests/test_p2_teardown.py`:

```python
    def test_metaskill_recipes_point_to_docs(self):
        body = (ROOT / "skills" / "product-playbook" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("references/recipes/", body)
        self.assertNotIn("Fallback during migration", body)
```

- [ ] **Step 3:** Run `python3 -m unittest tests.test_metaskill tests.test_p2_teardown -v` → expect FAIL (fallback line still present, no recipes path).
- [ ] **Step 4:** Edit `skills/product-playbook/SKILL.md`:
  - Delete the "Fallback during migration: …" line entirely.
  - In the "## Optional depth — recipes" section, keep the "suggest, never force, not slash commands" guidance and add that each recipe's lens sequence lives in `references/recipes/<name>.md` (name the four), to be read when the user accepts.
  - Do not change the `Available lenses` list or the situational table.
  - Ensure `validate_skill("skills/product-playbook/SKILL.md")` still returns `[]` and the frontmatter stays ≤1024 chars.
- [ ] **Step 5:** Run `python3 -m unittest tests.test_metaskill tests.test_p2_teardown -v` → PASS. Run `python3 -m unittest discover tests` → all green.
- [ ] **Step 6: Commit** `refactor: drop meta-skill migration fallback, point recipes at references/recipes/`

---

## After all 6 tasks

- [ ] **Final whole-branch review** (superpowers:requesting-code-review, most capable model) over the P2 range. Focus: the new system is fully decoupled (no skill/hook/test references a deleted file), both retained guardrail hooks stay advisory/non-blocking and reference only kept files, recipes carry the correct lens sequences, and the meta-skill still validates with no dead fallback.
- [ ] Fix Critical/Important via one fix subagent; record Minors in the ledger.
- [ ] **superpowers:finishing-a-development-branch.**
- Deferred to P3/P4 (do NOT do here): root `SKILL.md`, `commands/` registration in packaging, `install.sh` layout, READMEs, i18n cut, redundant framework content reference files (`00-08`, `02a-c`), and `rules-quality-review.md`'s always-on "Mandatory Critique" (a content-cleanup decision).

## Self-Review (author checklist, done)

- **Spec coverage:** §5 P2 row (delete mode-spine + optional-trigger/progress/end-of-flow + dispatch hook; rewrite 6-mode into 4 recipes; delete discovery-specialist) all mapped to tasks; the meta-skill fallback removal is added as the decoupling step. ✓
- **Dependency safety:** the two retained hooks are adapted off their deleted dependencies (`/product-dev`, `rules-progress`) in Tasks 3–4; `rules-change-propagation.md` is explicitly kept; the `test_new_system_has_no_reference` grep scopes to `skills`+`tests` so hook-adaptation ordering is safe. ✓
- **No placeholders:** exact file lists, exact test code, exact commit messages. ✓
- **Packaging boundary:** root SKILL.md / install.sh / READMEs / i18n / plugin.json explicitly deferred to P3/P4. ✓
