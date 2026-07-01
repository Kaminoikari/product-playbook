# P0 Foundation — Walking Skeleton Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stand up the outcome-first lens architecture end-to-end — meta-skill + SessionStart injection + provenance + relative guardrails + 3 representative lens skills — proving single-lens use, multi-lens blending, and a guardrail firing, with the legacy `references/` still reachable as fallback so nothing breaks.

**Architecture:** A single lean `product-playbook` meta-skill is injected at session start by a hook (mirroring superpowers' `session-start`). It reads the user's desired outcome, selects one or several framework lenses, produces the outcome, and tags provenance. Framework knowledge lives in per-lens `skills/<name>/SKILL.md` files; for frameworks not yet migrated, the meta-skill falls back to the existing `references/NN-*.md`. This plan migrates 3 lenses (`jtbd`, `pre-mortem`, `solution-prioritization`) as the walking skeleton; P1 migrates the remaining 13.

**Tech Stack:** Markdown skills (Claude Code plugin `skills/` convention), Python 3 hooks (`${CLAUDE_PLUGIN_ROOT}` + `hooks/hooks.json`), unittest for structural validation, existing JSON eval harness for behavioral checks.

## Global Constraints

- Single English source of truth; every skill body includes a runtime language-detection line: detect the user's language and reply in it, content authored in English.
- `description` frontmatter states triggering conditions only ("Use when …, before …"); it MUST NOT summarize the skill's internal workflow or steps.
- Frontmatter carries only `name` and `description`; whole frontmatter block ≤ 1024 characters; `name` matches `^[a-z0-9-]+$`.
- Provenance: end every planning output with one line `— Frameworks: X · Y`; names only by default; per-framework breakdown only when asked; omit if the user says so.
- Relative guardrails are proportional, non-blocking, one-line; they never hard-stop the flow.
- User-facing copy rules (apply to all skill output): no em-dash as a mid-sentence pause (use ，：；。（）); no contrast constructions (「不是 X 而是 Y」/「X 而非 Y」/"not X but Y"/"rather than"/"instead of"); full-width CJK punctuation for CJK text.
- Planning phase produces documents, never source code; only write code once the user explicitly moves to build.
- Skill files live at `skills/<skill-name>/SKILL.md`. The meta-skill is `skills/product-playbook/SKILL.md` (currently a symlink to root `SKILL.md` — Task 2 replaces the symlink with a real file).
- **Tests use `unittest.TestCase`, runnable by this repo's real command `python3 -m unittest discover tests -v`** (also `package.json` `test:all` and CI). Do NOT use pytest-only features (bare `test_*` functions, `tmp_path`); unittest discovery silently skips them and pytest is not a declared dependency. Use `tempfile.TemporaryDirectory` + `self.addCleanup` where a temp file is needed.

---

### Task 1: Skill-structure validator (the reusable test harness)

**Files:**
- Create: `scripts/validate_skill.py`
- Test: `tests/test_skill_structure.py`

**Interfaces:**
- Produces: `validate_skill(path: str) -> list[str]` returning a list of human-readable violation strings (empty list = valid). Consumed by every later task's test.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_skill_structure.py
import textwrap, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from validate_skill import validate_skill

def _write(tmp_path, body):
    p = tmp_path / "SKILL.md"
    p.write_text(body, encoding="utf-8")
    return str(p)

def test_valid_skill_has_no_violations(tmp_path):
    body = textwrap.dedent("""\
        ---
        name: jtbd
        description: Use when you need to understand the job a user hires the product to do, before designing a solution.
        ---
        # JTBD
        Detect the user's language and reply in it.
        Append the framework tag `JTBD` to the provenance line.
        """)
    assert validate_skill(_write(tmp_path, body)) == []

def test_missing_provenance_flagged(tmp_path):
    body = "---\nname: jtbd\ndescription: Use when ...\n---\n# JTBD\nDetect the user's language.\n"
    assert any("provenance" in v.lower() for v in validate_skill(_write(tmp_path, body)))

def test_bad_name_flagged(tmp_path):
    body = "---\nname: JTBD_Skill\ndescription: Use when ...\n---\n# x\nprovenance tag\nlanguage\n"
    assert any("name" in v.lower() for v in validate_skill(_write(tmp_path, body)))

def test_workflow_leak_in_description_flagged(tmp_path):
    body = "---\nname: jtbd\ndescription: Step 1 gather interviews, then write the job statement, then rank.\n---\n# x\nprovenance\nlanguage\n"
    assert any("workflow" in v.lower() for v in validate_skill(_write(tmp_path, body)))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_skill_structure -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'validate_skill'`

- [ ] **Step 3: Write minimal implementation**

```python
# scripts/validate_skill.py
import re, pathlib

_FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
_NAME = re.compile(r"^name:\s*(.+?)\s*$", re.MULTILINE)
_DESC = re.compile(r"^description:\s*(.+?)\s*$", re.MULTILINE | re.DOTALL)
_WORKFLOW_LEAK = re.compile(r"\bstep\s*1\b|\bthen\b.*\bthen\b", re.IGNORECASE)

def validate_skill(path: str) -> list[str]:
    text = pathlib.Path(path).read_text(encoding="utf-8")
    out = []
    m = _FRONTMATTER.match(text)
    if not m:
        return ["frontmatter: missing leading --- ... --- block"]
    fm, body = m.group(1), text[m.end():]
    if len(m.group(0)) > 1024:
        out.append("frontmatter: block exceeds 1024 characters")
    name_m = _NAME.search(fm)
    if not name_m:
        out.append("name: missing")
    elif not re.fullmatch(r"[a-z0-9-]+", name_m.group(1)):
        out.append(f"name: '{name_m.group(1)}' must match ^[a-z0-9-]+$")
    desc_m = _DESC.search(fm)
    if not desc_m:
        out.append("description: missing")
    elif _WORKFLOW_LEAK.search(desc_m.group(1)):
        out.append("description: appears to summarize workflow (found step/then sequence)")
    if "provenance" not in body.lower():
        out.append("body: missing provenance instruction")
    if "language" not in body.lower():
        out.append("body: missing runtime language-detection line")
    return out
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_skill_structure -v`
Expected: PASS (4 passed)

- [ ] **Step 5: Commit**

```bash
git add scripts/validate_skill.py tests/test_skill_structure.py
git commit -m "test: add skill-structure validator for lens skills"
```

---

### Task 2: Meta-skill `product-playbook` (lean, outcome-first)

**Files:**
- Create: `skills/product-playbook/SKILL.md` (first remove the existing symlink at that path)
- Test: `tests/test_metaskill.py`

**Interfaces:**
- Consumes: `validate_skill` from Task 1.
- Produces: the meta-skill body containing the anchor strings later tasks/tests assert on: `## Relative guardrails`, `— Frameworks:`, `references/`, `Available lenses`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_metaskill.py
import unittest, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from validate_skill import validate_skill

META = "skills/product-playbook/SKILL.md"

class TestMetaSkill(unittest.TestCase):
    def test_is_a_real_file_not_symlink(self):
        p = pathlib.Path(META)
        self.assertTrue(p.is_file() and not p.is_symlink())

    def test_passes_validator(self):
        self.assertEqual(validate_skill(META), [])

    def test_has_required_anchors(self):
        body = pathlib.Path(META).read_text(encoding="utf-8")
        for anchor in ["## Relative guardrails", "— Frameworks:", "references/",
                       "Available lenses", "Ground in evidence", "Sources:"]:
            self.assertIn(anchor, body, f"missing anchor: {anchor}")

    def test_has_no_mode_menu(self):
        body = pathlib.Path(META).read_text(encoding="utf-8")
        self.assertNotIn("Quick Mode", body)
        self.assertNotIn("Full Mode", body)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_metaskill -v`
Expected: FAIL (`test_is_a_real_file_not_symlink` — path is currently a symlink)

- [ ] **Step 3: Replace the symlink and write the meta-skill**

```bash
rm skills/product-playbook/SKILL.md   # remove symlink -> ../../SKILL.md
```

Then create `skills/product-playbook/SKILL.md` with exactly this content:

```markdown
---
name: product-playbook
description: Use when the user wants to plan, scope, validate, or strategize a product or feature, before producing any planning artifact. Routes the request to the minimal set of PM framework lenses that produce the outcome, single or blended. Triggers on "plan a feature", "add a feature", "is this worth building", "product strategy", "MVP", "PMF", "North Star", and the same intent in any language ("規劃新功能", "新機能を企画").
---

# Product Playbook

## Overview

The only success metric is the outcome the user actually wants. Frameworks are lenses you apply to reach a better outcome. Framework coverage and process completeness are not goals.

Default flow is four steps and nothing more:

1. Read the outcome
2. Select lens(es)
3. Produce the outcome
4. Tag provenance

## Step 1 — Read the outcome

Identify the concrete deliverable the user wants (a PR-FAQ, a go/no-go call, a metric set, a full plan). If it is unclear, ask ONE focused clarifying question, then proceed. Detect the user's language and reply in it; framework content is authored in English.

## Step 2 — Select lens(es)

A narrow, well-defined deliverable takes a single lens. A decision needing several perspectives blends multiple lenses into one integrated answer; do not walk each framework as a separate step.

| Situation | Lens(es) |
|---|---|
| "Write me a PR-FAQ" | pr-faq |
| "Is this feature worth building?" | jtbd + solution-prioritization + pre-mortem, blended into one go/no-go |
| "What should our North Star be?" | success-metrics |
| "Plan this whole new product" | suggest the full-product-plan recipe |
| "Does this positioning hold up?" | strategy-critic |

Available lenses: strategy-kernel, persona-journey, jtbd, opportunity-solution-tree, problem-framing, positioning, pr-faq, pre-mortem, solution-prioritization, mvp-scoping, success-metrics, pmf-gtm, prd-and-handoff, document-export, product-spec-summary, strategy-critic.

Fallback during migration: if a framework you need has no lens skill yet, read the matching `references/NN-*.md` and apply it inline. (This line is removed once migration completes.)

## Ground in evidence (research)

When the outcome depends on real-world facts the user has not provided (competitor behavior, market size, pricing benchmarks, whether a problem is validated outside this conversation), gather evidence before answering; do not rely on memory alone. Proportional, like the guardrails:

- A light single lookup (one competitor's page, one data point): just do it with WebSearch / WebFetch.
- A heavy multi-source competitive deep-dive: offer it in one line first ("want me to pull real data on the top 3 competitors? ~a minute"), then, on yes, fan out parallel research agents, verify adversarially, and synthesize with citations.

Cite real sources and add a count to the provenance line: `— Frameworks: … | Sources: N cited`. The full parallel `market-research` orchestration and `competitive-analysis` lens ship in a dedicated later plan; here you own the judgment of when to reach for evidence.

## Step 3 — Produce (process minimalism)

Do NOT do by default: mode menus, progress indicators, step-by-step confirmation, per-step self-review, or asking "shall I start?". Deliver the outcome directly, without filler.

## Step 4 — Tag provenance

End the output with one line: `— Frameworks: X · Y`. Names only by default. Expand a per-framework breakdown only when asked. Omit only if the user says so.

## Relative guardrails

Dormant by default. Surface only when the outcome would be materially harmed by the user's current path. When one fires, use a single line and let the user override in one word. Never hard-stop.

| Trigger | One-line nudge |
|---|---|
| Jumping straight to a solution/PRD with no problem statement | "There's no problem statement yet. Want me to clarify it in a minute, or do you already have one to hand me?" |
| A rationalization that would hurt the outcome (e.g. skipping discovery on a 0-to-1) | name the risk in one sentence, then let the user decide |
| Feature touches payments / permissions / data migration | one line to add the security lens (prd-and-handoff security section) |
| About to write source code during planning | keep to documents; write code only once the user moves to build |
| A directional change ripples into already-produced artifacts | one line naming the impact scope, user picks patch-only or cascade |

## Optional depth — recipes

If the user explicitly wants a full end-to-end walk-through, or the task is a large whole-product plan, suggest one recipe: full-product-plan, quick-validation, product-revision, or feature-extension. Suggest it; never force it. Recipes stay out of the slash-command surface.
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_metaskill -v`
Expected: OK (4 tests). Also confirm the meta-skill body contains the `## Ground in evidence (research)` section from the spec §4.8 (proportional research: light lookups auto, heavy deep-dives offered first; sources counted in provenance).

- [ ] **Step 5: Commit**

```bash
git add skills/product-playbook/SKILL.md tests/test_metaskill.py
git commit -m "feat: lean outcome-first product-playbook meta-skill"
```

---

### Task 3: SessionStart hook injecting the meta-skill

**Files:**
- Create: `hooks/session-start-inject-metaskill.py`
- Modify: `hooks/hooks.json` (add one SessionStart entry alongside the existing one)
- Test: `tests/test_inject_hook.py`

**Interfaces:**
- Consumes: reads `skills/product-playbook/SKILL.md` relative to `${CLAUDE_PLUGIN_ROOT}`.
- Produces: prints a JSON object `{"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "<sentinel-wrapped meta-skill>"}}` to stdout.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_inject_hook.py
import json, os, subprocess, pathlib, unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class TestInjectHook(unittest.TestCase):
    def test_hook_emits_metaskill_in_additional_context(self):
        env = {**os.environ, "CLAUDE_PLUGIN_ROOT": str(ROOT)}
        proc = subprocess.run(
            ["python3", str(ROOT / "hooks" / "session-start-inject-metaskill.py")],
            input="{}", capture_output=True, text=True, env=env, timeout=10,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        ctx = payload["hookSpecificOutput"]["additionalContext"]
        self.assertIn("PRODUCT-PLAYBOOK-METASKILL", ctx)
        self.assertIn("Read the outcome", ctx)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_inject_hook -v`
Expected: FAIL/ERROR (`No such file or directory` for the hook script)

- [ ] **Step 3: Write the hook**

```python
# hooks/session-start-inject-metaskill.py
import json, os, sys, pathlib

def main():
    sys.stdin.read()  # consume hook input; content unused
    root = pathlib.Path(os.environ.get("CLAUDE_PLUGIN_ROOT", "."))
    skill = root / "skills" / "product-playbook" / "SKILL.md"
    try:
        body = skill.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:  # never crash the session on a bad read
        print(f"session-start-inject-metaskill: cannot read meta-skill: {exc}", file=sys.stderr)
        sys.exit(0)  # never block the session
    wrapped = (
        "<PRODUCT-PLAYBOOK-METASKILL>\n"
        "The product-playbook meta-skill is active this session. Follow it for any "
        "product/feature planning request.\n\n" + body + "\n</PRODUCT-PLAYBOOK-METASKILL>"
    )
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": wrapped,
    }}))

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Register the hook in `hooks/hooks.json`**

Add a second object to the existing `SessionStart` array (keep `session-start-load-progress.py`; add matcher `startup|resume|compact` so the meta-skill re-injects after compaction):

```json
{
  "matcher": "startup|resume|compact",
  "hooks": [
    {
      "type": "command",
      "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/session-start-inject-metaskill.py",
      "timeout": 10
    }
  ]
}
```

- [ ] **Step 5: Run test to verify it passes**

Run: `python3 -m unittest tests.test_inject_hook -v`
Expected: OK (1 test)

- [ ] **Step 6: Verify the JSON is still well-formed**

Run: `python3 -c "import json; json.load(open('hooks/hooks.json')); print('hooks.json OK')"`
Expected: `hooks.json OK`

- [ ] **Step 7: Commit**

```bash
git add hooks/session-start-inject-metaskill.py hooks/hooks.json tests/test_inject_hook.py
git commit -m "feat: inject product-playbook meta-skill at session start (incl. compact)"
```

---

### Task 4: Lens skill `jtbd` (single-lens proof, migrated from 02b)

**Files:**
- Create: `skills/jtbd/SKILL.md`
- Test: `tests/test_lens_jtbd.py`

**Interfaces:**
- Consumes: `validate_skill` from Task 1; framework body from `references/02b-jtbd.md`.
- Produces: a lens skill whose output appends the tag `JTBD` to the provenance line.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_lens_jtbd.py
import unittest, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from validate_skill import validate_skill

SKILL = "skills/jtbd/SKILL.md"

class TestJtbdLens(unittest.TestCase):
    def test_passes_validator(self):
        self.assertEqual(validate_skill(SKILL), [])

    def test_declares_framework_tag_and_substance(self):
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertIn("`JTBD`", body)          # provenance tag
        self.assertIn("job", body.lower())     # migrated substance, not a stub
        self.assertGreater(len(body), 1500)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_lens_jtbd -v`
Expected: FAIL/ERROR (skill file does not exist)

- [ ] **Step 3: Create the lens skill by migrating the framework body**

1. Write the frontmatter + wrapper below into `skills/jtbd/SKILL.md`.
2. Under the `## Framework` heading, paste the full body of `references/02b-jtbd.md` (its three-layer JTBD, canonical three-clause form, B2B Org-Level Jobs, Deep-Dive questions, and Quality Checklist). The B2B/quality checklists are lens-quality checks; keep them verbatim (they judge output quality, they are not process gates).

```markdown
---
name: jtbd
description: Use when you need to understand the job a user hires the product to do, before designing or evaluating a solution. Triggers on "jobs to be done", "JTBD", "what job", "user motivation", "why would they use this", "customer needs", and the same intent in any language.
---

# Jobs To Be Done

Detect the user's language and reply in it; the framework below is authored in English.

**Provenance:** when you produce JTBD output, contribute the framework tag `JTBD` to the meta-skill's provenance line (`— Frameworks: … · JTBD · …`).

## Framework

<!-- migrated verbatim from references/02b-jtbd.md -->
[PASTE references/02b-jtbd.md BODY HERE]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_lens_jtbd -v`
Expected: PASS (2 passed)

- [ ] **Step 5: Commit**

```bash
git add skills/jtbd/SKILL.md tests/test_lens_jtbd.py
git commit -m "feat: migrate JTBD framework to jtbd lens skill"
```

---

### Task 5: Lens skill `pre-mortem` (blend member, migrated from 04b §3.3)

**Files:**
- Create: `skills/pre-mortem/SKILL.md`
- Test: `tests/test_lens_pre_mortem.py`

**Interfaces:**
- Consumes: `validate_skill`; framework body from `references/04b-solutions.md` §3.3 (Shreyas Doshi pre-mortem).
- Produces: a lens whose output contributes the tag `Pre-mortem`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_lens_pre_mortem.py
import unittest, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from validate_skill import validate_skill

SKILL = "skills/pre-mortem/SKILL.md"

class TestPreMortemLens(unittest.TestCase):
    def test_passes_validator(self):
        self.assertEqual(validate_skill(SKILL), [])

    def test_declares_tag_and_substance(self):
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertIn("`Pre-mortem`", body)
        self.assertIn("failed", body.lower())
        self.assertIn("scenario", body.lower())
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_lens_pre_mortem -v`
Expected: FAIL (file missing)

- [ ] **Step 3: Create the lens skill**

Write `skills/pre-mortem/SKILL.md` with this frontmatter + wrapper, then paste the §3.3 pre-mortem body (imagine-it-failed, 15+ scenarios across 5 categories, leading indicators, the "at least one security scenario" quality check) from `references/04b-solutions.md`:

```markdown
---
name: pre-mortem
description: Use when you need to surface how a product, feature, or plan could fail before committing to it, especially before a go/no-go decision. Triggers on "pre-mortem", "what could go wrong", "failure modes", "risks", "how might this fail", and the same intent in any language.
---

# Pre-mortem

Detect the user's language and reply in it; the framework below is authored in English.

**Provenance:** when you produce pre-mortem output, contribute the framework tag `Pre-mortem` to the meta-skill's provenance line.

## Framework

<!-- migrated from references/04b-solutions.md §3.3 -->
[PASTE the §3.3 pre-mortem body HERE]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_lens_pre_mortem -v`
Expected: PASS (2 passed)

- [ ] **Step 5: Commit**

```bash
git add skills/pre-mortem/SKILL.md tests/test_lens_pre_mortem.py
git commit -m "feat: migrate pre-mortem framework to pre-mortem lens skill"
```

---

### Task 6: Lens skill `solution-prioritization` (blend member, migrated from 04b §3.4/3.5)

**Files:**
- Create: `skills/solution-prioritization/SKILL.md`
- Test: `tests/test_lens_prioritization.py`

**Interfaces:**
- Consumes: `validate_skill`; framework bodies from `references/04b-solutions.md` §3.4 (GEM) and §3.5 (RICE), plus Impact/Effort.
- Produces: a lens whose output contributes the tag `RICE` (and `GEM` when GEM is applied).

- [ ] **Step 1: Write the failing test**

```python
# tests/test_lens_prioritization.py
import unittest, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from validate_skill import validate_skill

SKILL = "skills/solution-prioritization/SKILL.md"

class TestPrioritizationLens(unittest.TestCase):
    def test_passes_validator(self):
        self.assertEqual(validate_skill(SKILL), [])

    def test_declares_tags_and_substance(self):
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertIn("`RICE`", body)
        self.assertIn("`GEM`", body)
        self.assertIn("reach", body.lower())
        self.assertIn("effort", body.lower())
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_lens_prioritization -v`
Expected: FAIL (file missing)

- [ ] **Step 3: Create the lens skill**

Write `skills/solution-prioritization/SKILL.md` with this frontmatter + wrapper, then paste the GEM and RICE bodies from `references/04b-solutions.md` §3.4 and §3.5:

```markdown
---
name: solution-prioritization
description: Use when you have several solution options or features and need to decide what to do first, before scoping an MVP. Triggers on "prioritize", "RICE", "GEM", "impact vs effort", "which should we build first", "rank these", and the same intent in any language.
---

# Solution Prioritization

Detect the user's language and reply in it; the framework below is authored in English.

**Provenance:** contribute the framework tag `RICE` (and `GEM` when the GEM lens is applied) to the meta-skill's provenance line.

## Framework

<!-- migrated from references/04b-solutions.md §3.4 (GEM) + §3.5 (RICE) + Impact/Effort -->
[PASTE the GEM + RICE + Impact/Effort bodies HERE]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_lens_prioritization -v`
Expected: PASS (2 passed)

- [ ] **Step 5: Run the full structural suite**

Run: `python3 -m unittest discover tests -v`
Expected: PASS (all tests from Tasks 1–6)

- [ ] **Step 6: Commit**

```bash
git add skills/solution-prioritization/SKILL.md tests/test_lens_prioritization.py
git commit -m "feat: migrate RICE/GEM prioritization to solution-prioritization lens skill"
```

---

### Task 7: Behavioral skeleton eval (end-to-end proof, quota-aware)

**Files:**
- Create: `evals/skeleton-eval.json`
- Reuse: `evals/run_behavioral_eval.py` (existing runner)

**Interfaces:**
- Consumes: the runner's existing `{cases: [{name, prompt, expect}]}` shape (mirror `evals/evals.json`'s structure exactly — inspect it first and copy the field names).

- [ ] **Step 1: Inspect the existing eval shape**

Run: `python3 -c "import json; d=json.load(open('evals/evals.json')); print(list(d.keys())); print(json.dumps(d[list(d.keys())[0]][:1] if isinstance(d[list(d.keys())[0]], list) else d, ensure_ascii=False, indent=2)[:600])"`
Expected: prints the JSON keys and one sample case so you can match field names exactly.

- [ ] **Step 2: Write `evals/skeleton-eval.json` with four cases**

Match the field names discovered in Step 1. The four cases assert the walking skeleton works end to end:

1. **single-lens** — prompt: "Write me a JTBD statement for a habit-tracking app." → expect: output applies JTBD and ends with a provenance line containing `JTBD`.
2. **blend** — prompt: "Is a dark-mode feature worth building for our note app?" → expect: a single integrated go/no-go whose provenance line contains `JTBD`, `RICE`, and `Pre-mortem` (blended, not three separate step-by-step sections).
3. **provenance-names-only** — prompt: "Give me a North Star metric for a food-delivery app." → expect: a provenance line present with framework name(s) only, no per-framework breakdown unless asked.
4. **guardrail-fires** — prompt: "Write the full PRD now." (no problem statement given) → expect: a one-line nudge about the missing problem statement, non-blocking, and it still offers to proceed.

- [ ] **Step 3: Run the eval (manually, quota-aware)**

Run: `python3 evals/run_behavioral_eval.py evals/skeleton-eval.json`
Expected: 4/4 pass. Note: this invokes `claude -p` and consumes quota; run once locally, do not wire into CI (repo policy: eval-gate is workflow_dispatch only).

- [ ] **Step 4: Commit**

```bash
git add evals/skeleton-eval.json
git commit -m "test: end-to-end behavioral eval for lens walking skeleton"
```

---

## Self-Review

**Spec coverage (against the design spec §4):**
- §4.1 three-layer structure → Tasks 2 (meta-skill), 3 (hook), 4–6 (lens skills). ✓
- §4.2 four actions + situational table + single/blend → meta-skill body (Task 2) + blend eval case (Task 7). ✓
- §4.3 lens skills → 3 of 16 migrated here (jtbd, pre-mortem, solution-prioritization); remaining 13 are P1. ✓ (scope-limited by design)
- §4.4 provenance names-only + breakdown-on-request → validator check (Task 1), meta-skill rule (Task 2), per-lens tags (Tasks 4–6), eval case 3 (Task 7). ✓
- §4.5 relative guardrails → meta-skill guardrail table (Task 2) + eval case 4 (Task 7). ✓
- §4.6 recipes as suggestion, not command → meta-skill "Optional depth" section (Task 2). ✓ (recipe skills themselves are P2)
- §4.7 runtime language detection → global constraint + validator check for "language" line (Task 1) + each skill body. ✓

**Deferred to later plans (not gaps in P0):**
- P1: migrate the remaining 13 lens skills (strategy-kernel, persona-journey, opportunity-solution-tree, problem-framing, positioning, pr-faq, mvp-scoping, success-metrics, pmf-gtm, prd-and-handoff, document-export, product-spec-summary, strategy-critic).
- P2: delete the 5 mode spine files + orchestration cross-files + specialist-dispatch hook; author the 4 recipe skills; remove the meta-skill's legacy `references/` fallback line.
- P3: remove i18n mirror (225 files) + 2 i18n scripts + 5 READMEs; rewrite the 24 mode-bound behavioral evals to outcome/lens/provenance assertions; repoint closed-loop `EVAL_ATTRIBUTION`.
- P4: update plugin.json / marketplace.json / package.json (version + description), fix install.sh layout, bump version.

**Placeholder scan:** the `[PASTE … HERE]` markers in Tasks 4–6 are explicit migration instructions (move an existing, named source body), not unresolved content; source file and section are named exactly. No "TBD"/"add error handling"/"similar to Task N" present.

**Type consistency:** `validate_skill(path) -> list[str]` is defined in Task 1 and consumed identically in Tasks 2, 4, 5, 6. Provenance tags are consistent: `JTBD` (Task 4), `Pre-mortem` (Task 5), `RICE`/`GEM` (Task 6), all asserted against the same eval in Task 7. Hook output key `additionalContext` matches the test in Task 3.
