# P3 — Machinery Layer: i18n Cut + Outcome-First Eval Rewrite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the file-mirror i18n subsystem (the new approach is runtime language detection, already in every lens skill) and replace the 12 mode-bound behavioral eval cases with a focused outcome-first suite that scores the lens architecture.

**Architecture:** Two independent groups. **Group A (i18n cut)** deletes `i18n/` + its 2 scripts + 5 translated READMEs + the zh-TW eval mirror + the dedicated CI workflow, then fixes the handful of consumers that would hard-fail and cleans the loop-machinery code that references the deleted scripts. **Group B (eval rewrite)** rewrites `evals/evals.json` into ~9 outcome-first cases and reconciles the hand-curated `EVAL_ATTRIBUTION` map so the self-improvement loop still covers the new names. The runtime per-skill "Detect the user's language and reply in it" line STAYS — that is the i18n mechanism now.

**Tech Stack:** Python 3 `unittest` (run: `python3 -m unittest discover tests`); the eval runners are manual (`npm run eval:*`, quota-gated, never CI-auto per project policy).

## Global Constraints

- **Test runner is `unittest`, never pytest.** The full suite (128 before P3) must be green after each task, except where a task intentionally deletes an obsolete test (called out in that task).
- **No CI auto-eval.** `eval-gate.yml` stays `workflow_dispatch`-only. Do not add auto-fire eval triggers. The behavioral eval JSON is a spec-of-correct-behavior + manual QA artifact, not a live gate.
- **Runtime language detection stays.** Do NOT remove the "Detect the user's language and reply in it" line from any `skills/*/SKILL.md`. Only the `i18n/` file mirrors + drift machinery go.
- **No bijection is enforced** between `evals.json` case names and `EVAL_ATTRIBUTION` keys, and none must be added. Updating the map is for report quality + patch coverage, not to satisfy a test.
- **Every evals.json case MUST have `id` and `name` keys** (missing either crashes `run_behavioral_eval.py`'s error handler). Required per-case fields: `id`, `name`, `prompt`, `expectations` (list of `{text, severity}`); `severity` ∈ {`critical`, `warning`, `info`}. `expected_output` is documentation-only.
- **New/edited prose follows the copy rules** (no mid-sentence em-dash except headings/`— Frameworks:`; no "rather than"/"instead of"/"X, not Y"; full-width CJK for CJK).
- **Do NOT touch packaging in P3** (`install.sh`, `.claude-plugin/*.json`, version, root `SKILL.md`): that is P4. Group A edits `package.json` ONLY to remove the 3 dangling i18n npm scripts + the 6 dangling `files` entries — no version/description change here.

---

## Task A1: Atomic i18n cut (delete mirrors + fix hard-fail consumers)

Deletion and its mandatory consumer-fixes land together so the suite never goes red at a commit boundary.

**Files:**
- Delete: `i18n/` (whole dir, 225 files), `scripts/i18n-drift-report.py`, `scripts/i18n-mirror-apply.py`, `README.es.md`, `README.ja.md`, `README.ko.md`, `README.zh-CN.md`, `README.zh-TW.md`, `evals/evals-zh-TW.json`, `.github/workflows/i18n-drift-check.yml`
- Modify: `tests/test_closed_loop.py`, `tests/test_install_smoke.py`, `package.json`
- Test: `tests/test_p3_i18n_cut.py` (new)

**Interfaces:** `install.sh` (references `i18n/` at lines ~213/294-296) is NOT touched here — its rewrite + `SUPPORTED_LANGS`/`--lang` removal is P4. `README.md` (English) stays. The cross-links inside `README.md` pointing at the deleted translations become stale prose — acceptable, README overhaul is P4.

- [ ] **Step 1: Write the failing test** `tests/test_p3_i18n_cut.py`:

```python
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
```

- [ ] **Step 2:** Run `python3 -m unittest tests.test_p3_i18n_cut -v` → expect FAIL.
- [ ] **Step 3: Delete** with `git rm`: `git rm -r i18n` ; `git rm scripts/i18n-drift-report.py scripts/i18n-mirror-apply.py README.es.md README.ja.md README.ko.md README.zh-CN.md README.zh-TW.md evals/evals-zh-TW.json .github/workflows/i18n-drift-check.yml`.
- [ ] **Step 4: Fix `tests/test_closed_loop.py`** (both would ERROR/FAIL on the deleted `i18n-mirror-apply.py`):
  - Delete the entire `class TestA3MirrorValidation(unittest.TestCase):` and all its methods (it lives around lines 87-116; its `setUp` does `_load("mm", "i18n-mirror-apply.py")` which now raises `FileNotFoundError`).
  - Delete the method `test_i18n_mirror_rejects_negative_max` (around lines 493-498). Keep its siblings `test_patch_proposer_rejects_negative_max` and `test_loop_tick_rejects_negative_max_patches`.
- [ ] **Step 5: Fix `tests/test_install_smoke.py`:**
  - Delete the method `test_all_5_readmes_present` (around lines 116-120).
  - In `test_required_user_facing_dirs_in_allowlist` (around lines 41-48), remove the `"i18n/"` element from the tuple `(".claude-plugin/", "skills/", "SKILL.md", "agents/", "references/", "i18n/")` so it becomes `(".claude-plugin/", "skills/", "SKILL.md", "agents/", "references/")`.
- [ ] **Step 6: Fix `package.json`:**
  - Delete the three script lines: `"i18n:drift": ...`, `"i18n:mirror": ...`, `"eval:zh-TW": ...`.
  - In the `"files"` array, delete the six entries: `"i18n/"`, `"README.zh-TW.md"`, `"README.ja.md"`, `"README.zh-CN.md"`, `"README.es.md"`, `"README.ko.md"`. Keep the JSON valid.
- [ ] **Step 7:** Run `python3 -m unittest tests.test_p3_i18n_cut -v` → PASS. Run `python3 -m unittest discover tests` → all green (deletions of the obsolete tests are intentional; net count drops by the removed methods + rises by 3 new).
- [ ] **Step 8: Commit** `refactor: cut i18n file-mirror subsystem (dir, scripts, READMEs, zh-TW eval, CI); runtime language detection stays`

## Task A2: Clean the loop-machinery references to the deleted i18n scripts

These are GRACEFUL (no crash) but leave dead code that spawns doomed subprocesses every tick (`loop-tick.py`) or dead branches referencing deleted files. Clean them so no live script names a deleted i18n script.

**Files:**
- Modify: `scripts/loop-tick.py`, `scripts/loop-status.py`, `scripts/_config.py`, `scripts/_freshness.py`, `scripts/eval-lift-report.py`
- Test: extend `tests/test_p3_i18n_cut.py`

**Interfaces:** `_config.WATCHED` is imported only by `_freshness.py`. `loop-tick.py` Stage 4 (drift-report) runs on every tick unconditionally — removing it stops permanent doomed-subprocess spawns. `_trim-skill-for-claude-ai.py` and `build-claude-ai-bundle.sh` only carry stale *comments* (no code path touches `i18n/`); a comment refresh there is optional and out of this task's test scope.

- [ ] **Step 1: Add failing test** to `tests/test_p3_i18n_cut.py`:

```python
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
```

- [ ] **Step 2:** Run → FAIL.
- [ ] **Step 3: Edit the files:**
  - `scripts/loop-tick.py`: remove the `MIRROR_APPLY` / `DRIFT_REPORT` constants (~lines 59-60), the Stage 3 mirror-apply block (~323-349) and Stage 4 drift-report block (~351-372), and the Stage 3/4 lines in the module docstring (~15-18, 38). Renumber remaining stage comments if they are numbered.
  - `scripts/loop-status.py`: remove `_read_drift()` (~58-84), the `"i18n_drift": drift or None` entry (~169), the i18n dashboard-row print (~194-200), the i18n-mirror suggestion text in `_next_action()` (~112-114), and the i18n docstring mentions (~5, 11).
  - `scripts/_config.py`: change `WATCHED = ["references", "agents", "i18n", "SKILL.md", "evals/evals.json"]` → `WATCHED = ["references", "agents", "SKILL.md", "evals/evals.json"]`.
  - `scripts/_freshness.py`: change the fallback `WATCHED = ["references", "agents", "i18n", "SKILL.md", "evals/evals.json"]` (~line 31) → drop `"i18n"`; update the docstring list (~5, 17) to not name `i18n/`.
  - `scripts/eval-lift-report.py`: drop `"i18n/"` from the `git log` pathspec (~358) and from the three generated-markdown command lines (~378, 388, 394).
- [ ] **Step 4:** Run `python3 -m unittest tests.test_p3_i18n_cut -v` → PASS. Run `python3 -m unittest discover tests` → green (the closed-loop severity/freshness tests still pass — `WATCHED` still contains `evals/evals.json`, which `TestFreshness.test_watched_includes_eval_spec` requires).
- [ ] **Step 5: Commit** `refactor: remove dead i18n-drift/mirror references from loop machinery`

## Task B1: Rewrite `evals/evals.json` into a focused outcome-first suite

Replace the 12 mode-bound cases with ~9 cases that score the lens architecture. Model the style on the existing `evals/skeleton-eval.json` (the P0 outcome-first seed) and keep the substantive quality expectations from the survivors.

**Files:**
- Modify: `evals/evals.json` (replace the `evals` array; keep `skill_name` + `_notes`)
- Test: `tests/test_p3_eval_suite.py` (new)

**Interfaces:** Case schema (de-facto, enforced by `run_behavioral_eval.py`): each case is `{"id": <int>, "name": "<kebab>", "prompt": "<str>", "expected_output": "<str, doc-only>", "expectations": [{"text": "<str>", "severity": "critical"|"warning"|"info"}, ...]}`. Top level stays `{"skill_name", "evals": [...], "_notes": {...}}`. `EVAL_ATTRIBUTION` reconciliation is Task B2 — this task just names the cases; B2 maps them.

**The 9-case blueprint** (ids 1-9; author full graded expectations for each, 3-6 per case, mixing severities; the new-system behaviors are: right lens(es) selected, provenance line `— Frameworks: …`, proportional non-blocking guardrails, and per-lens output quality):

1. `lens-selection-single` — a single clear outcome ("help me understand what job users hire my note app for") → the jtbd lens is applied, output is JTBD analysis, and the provenance line names `JTBD`. Expectations assert: JTBD structure present (critical), provenance line present naming JTBD (critical), no unrequested other-lens artifacts leaked (warning).
2. `lens-blend` — a situation needing two lenses ("should we build this feature? weigh it and check what could go wrong") → solution-prioritization + pre-mortem are blended, provenance names BOTH (`— Frameworks: … · …`). Expectations: both frameworks' output present (critical each), provenance names both tags (critical).
3. `provenance-format` — any planning request → output ends with a provenance line in the exact `— Frameworks: X` shape (leading em-dash label allowed). Expectations: line present (critical), uses framework names only, not process names (warning).
4. `guardrail-proportional` — user asks to jump straight to a solution with no problem stated → a guardrail surfaces the missing problem framing as ONE non-blocking line that is overridable, and still proceeds if the user pushes. Expectations: guardrail is advisory not a hard stop (critical), it is one line not a gate ceremony (warning), it does not block the user's request (critical).
5. `jtbd-depth` — (reframed survivor, keep the strong expectations) two personas, independent JTBD each, Five Whys ≥5 layers, Q5 uses explicit psychological/emotional vocabulary (fear/anxiety/shame/…), B2B org-level jobs, canonical "When… I want to… so I can…" clause. Reuse the substantive expectation texts from the old `eval-jtbd-depth`, minus any mode/hard-gate framing.
6. `prfaq-quality` — (reframed survivor) a PR-FAQ request → Amazon working-backwards PR + FAQ, customer-obsessed headline, measurable claims. Reuse old `eval-prfaq-output` substance.
7. `security-awareness` — (kept) a dev-handoff/PRD request that involves secrets/config → the output flags secret handling / `.gitignore` / no hardcoded keys. Reuse old `eval-security-awareness` substance.
8. `strategy-critic-teardown` — (reframed from `eval-subagent-strategy-critic`) user presents a weak strategy (goals-as-strategy) → the strategy-critic lens dismantles it (diagnosis/guiding-policy/coherent-action gaps, fluff called out), returns a critique. Drop any "dispatch"/orchestrator-marker language.
9. `pre-mortem-scenarios` — (reframed from `eval-subagent-premortem`) "imagine this launched and failed — why?" → pre-mortem lens produces ≥10 failure scenarios across categories with leading indicators, ranked. Drop mode-step framing.

Retired (no direct successor case): `eval-mode-selection`, `eval-quick-mode-jtbd`, `eval-revision-mode`, `eval-quality-hardgate`, `eval-feature-extension`, `eval-context-bootstrap`, `eval-subagent-discovery` (their intent is covered by 1-4 above or is obsolete mode behavior).

- [ ] **Step 1: Write the failing test** `tests/test_p3_eval_suite.py`:

```python
import json, pathlib, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "evals" / "evals.json").read_text(encoding="utf-8"))
CASES = DATA["evals"]
NAMES = {c["name"] for c in CASES}
VALID_SEV = {"critical", "warning", "info"}

class TestP3EvalSuite(unittest.TestCase):
    def test_case_count_focused(self):
        self.assertGreaterEqual(len(CASES), 8)
        self.assertLessEqual(len(CASES), 10)

    def test_every_case_has_required_fields(self):
        seen_ids = set()
        for c in CASES:
            self.assertIn("id", c); self.assertIn("name", c)
            self.assertIn("prompt", c); self.assertIn("expectations", c)
            self.assertNotIn(c["id"], seen_ids, f"dup id {c['id']}"); seen_ids.add(c["id"])
            self.assertTrue(c["expectations"], c["name"])
            for e in c["expectations"]:
                self.assertIn("text", e); self.assertIn(e["severity"], VALID_SEV, e)

    def test_new_outcome_first_cases_present(self):
        for required in ("lens-selection-single", "lens-blend", "provenance-format",
                         "guardrail-proportional"):
            self.assertIn(required, NAMES, required)

    def test_obsolete_mode_cases_gone(self):
        for gone in ("eval-mode-selection", "eval-quick-mode-jtbd", "eval-revision-mode",
                     "eval-quality-hardgate", "eval-subagent-discovery"):
            self.assertNotIn(gone, NAMES, gone)

    def test_no_mode_scoping_language_in_expectations(self):
        blob = json.dumps(DATA, ensure_ascii=False)
        # the obsolete Discovery/Develop/Deliver mode-scoping vocabulary must be gone
        for banned in ("Discovery mode", "Develop/Deliver", "Full Mode", "Quick Mode",
                       "Revision Mode", "Hard Gate"):
            self.assertNotIn(banned, blob, banned)

    def test_provenance_expectation_exists(self):
        blob = json.dumps(DATA, ensure_ascii=False)
        self.assertIn("Frameworks:", blob)  # at least one case scores the provenance line
```

- [ ] **Step 2:** Run `python3 -m unittest tests.test_p3_eval_suite -v` → expect FAIL (old suite).
- [ ] **Step 3:** Rewrite `evals/evals.json`'s `evals` array per the 9-case blueprint. For each case write a realistic `prompt`, a short doc-only `expected_output`, and 3-6 graded `expectations`. For the reframed survivors (5-9), lift the substantive expectation texts from the old cases (visible in git: `git show HEAD~2:evals/evals.json`) and strip mode/hard-gate framing. Keep `skill_name` and `_notes` (update `_notes` to say the suite is outcome-first, interactive-only, not CI-gated).
- [ ] **Step 4:** Run `python3 -m unittest tests.test_p3_eval_suite -v` → PASS. Run `python3 -m unittest discover tests` → green. Sanity-check the JSON parses: `python3 -c "import json;json.load(open('evals/evals.json'))"`.
- [ ] **Step 5: Commit** `refactor: rewrite behavioral eval suite to outcome-first lens cases`

## Task B2: Reconcile `EVAL_ATTRIBUTION` with the new eval names

Point the self-improvement loop at the new suite so `patch-proposer.py` covers the new names and `eval-debt-report.py` stops emitting "(unknown)" placeholders. No test enforces a bijection; this task adds a soft coverage check.

**Files:**
- Modify: `scripts/eval-debt-report.py` (the `EVAL_ATTRIBUTION` dict)
- Test: extend `tests/test_p3_eval_suite.py`

**Interfaces:** `EVAL_ATTRIBUTION` is `dict[str, {"primary": [paths], "secondary": [paths], "hint": str}]`. `tests/test_closed_loop.py::TestA1AttributionPaths` asserts every primary/secondary PATH exists on disk — so new entries must point at real files (lens skills `skills/<name>/SKILL.md`, recipe docs `references/recipes/<name>.md`, kept references like `references/02b-jtbd.md`, `references/04a-prfaq.md`, or the meta-skill `skills/product-playbook/SKILL.md`). Keep the existing `"trigger-eval"` key. This task also resolves the P2-review Minor about 2 stale hint strings.

- [ ] **Step 1: Add failing test** to `tests/test_p3_eval_suite.py`:

```python
    def test_attribution_covers_new_eval_names(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "edr", str(ROOT / "scripts" / "eval-debt-report.py"))
        edr = importlib.util.module_from_spec(spec); spec.loader.exec_module(edr)
        keys = set(edr.EVAL_ATTRIBUTION.keys())
        # every current evals.json case name has an attribution entry (patch coverage)
        for name in NAMES:
            self.assertIn(name, keys, f"{name} missing from EVAL_ATTRIBUTION")
        # retired names no longer linger as dead keys (trigger-eval is the one allowed non-case key)
        for retired in ("eval-mode-selection", "eval-subagent-discovery", "eval-revision-mode"):
            self.assertNotIn(retired, keys, retired)
```

- [ ] **Step 2:** Run → FAIL.
- [ ] **Step 3:** Edit `EVAL_ATTRIBUTION` in `scripts/eval-debt-report.py`: remove the 12 retired mode-bound keys, add one entry per new eval name (1-9 from B1) with `primary` pointing at the lens/recipe/reference file that most directly governs that behavior and a `hint` describing the CURRENT behavior (not deleted-file behavior). Keep the `"trigger-eval"` key. Suggested primaries: `lens-selection-single`→`skills/product-playbook/SKILL.md`; `lens-blend`→`skills/product-playbook/SKILL.md`; `provenance-format`→`skills/product-playbook/SKILL.md`; `guardrail-proportional`→`skills/product-playbook/SKILL.md`; `jtbd-depth`→`skills/jtbd/SKILL.md`; `prfaq-quality`→`skills/pr-faq/SKILL.md`; `security-awareness`→`skills/prd-and-handoff/SKILL.md`; `strategy-critic-teardown`→`skills/strategy-critic/SKILL.md`; `pre-mortem-scenarios`→`skills/pre-mortem/SKILL.md`. Verify each path exists before writing.
- [ ] **Step 4:** Run `python3 -m unittest tests.test_p3_eval_suite tests.test_closed_loop -v` → PASS (A1 path check still green). Run `python3 -m unittest discover tests` → all green.
- [ ] **Step 5: Commit** `refactor: reconcile EVAL_ATTRIBUTION with outcome-first eval names`

---

## After all 4 tasks

- [ ] **Final whole-branch review** (superpowers:requesting-code-review, most capable model) over the P3 range. Focus: no live script/test/CI references a deleted i18n file; runtime language-detection lines untouched in `skills/`; the new eval suite is valid, focused, and free of mode-scoping vocabulary; `EVAL_ATTRIBUTION` paths all resolve and cover the new names; the loop machinery still runs (no dead doomed-subprocess stages).
- [ ] Fix Critical/Important via one fix subagent; record Minors in the ledger.
- [ ] Do NOT run `finishing-a-development-branch` yet — P4 (packaging) follows in the same branch; finish after P4.
- Deferred to P4: `install.sh` rewrite + `SUPPORTED_LANGS`/`--lang` removal, `README.md` overhaul (stale translation cross-links), `.claude-plugin/*.json` + `package.json` version/description, root `SKILL.md` deletion.

## Self-Review (author checklist, done)

- **Spec coverage:** §5 P3 (i18n cut; rewrite mode-bound evals to outcome-first; closed-loop attribution map → new skills) all mapped: A1+A2 = i18n cut with verified blast-radius fixes, B1 = eval rewrite, B2 = attribution reconciliation. ✓
- **Blast-radius safety:** every HARD-FAIL consumer from the investigation (test_closed_loop TestA3 + negative-max, test_install_smoke 5-readmes + allowlist, package.json 3 scripts + 6 files) is fixed inside A1 atomically; GRACEFUL loop-machinery dead code cleaned in A2 with a grep gate. ✓
- **Eval-coupling safety:** no bijection assumed; every case keeps `id`+`name`; B2 keeps `trigger-eval`; A1 path check stays green because new attribution primaries point at existing skill files. ✓
- **Packaging boundary:** install.sh / .claude-plugin / version / root SKILL.md / README overhaul explicitly deferred to P4; P3's package.json edit is limited to removing dangling i18n entries. ✓
