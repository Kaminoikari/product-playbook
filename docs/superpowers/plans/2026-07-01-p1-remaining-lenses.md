# P1 — Remaining 13 Framework Lenses Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate the remaining 13 framework lenses (spec §4.3) from `references/` into standalone `skills/<name>/SKILL.md` lens skills, so the meta-skill can reach every framework directly instead of via the `references/NN-*.md` fallback.

**Architecture:** Each lens = frontmatter (triggering-only `description`) + a runtime language-detection line + a provenance instruction (contributes the framework tag(s)) + a `## Framework` body migrated from the mapped reference section(s). P0 already shipped `jtbd`, `pre-mortem`, `solution-prioritization` and the meta-skill/validator/hook. This phase reuses that exact pattern. After all 13 land, all 16 lenses exist; removing the meta-skill's `references/` fallback line is P2, not this phase.

**Tech Stack:** Python 3 `unittest` (run: `python3 -m unittest discover tests -v`); `scripts/validate_skill.py` `validate_skill(path)->list[str]`.

## Global Constraints

- **Test runner is `unittest`, never pytest.** Every test is a `unittest.TestCase`, discoverable by `python3 -m unittest discover tests`. pytest is not a dependency and will silently collect nothing.
- **`description` states TRIGGERING CONDITIONS ONLY**, never a workflow summary or step sequence (the validator's no-workflow-leak heuristic and the spec's borrowed rule). Keep frontmatter ≤1024 chars.
- **Every lens body contains, in order:** a runtime language-detection line ("Detect the user's language and reply in it; the framework below is authored in English."), a `**Provenance:**` instruction naming the framework tag(s) it contributes to the meta-skill's `— Frameworks:` line, and a `## Framework` section with the migrated content.
- **`validate_skill("skills/<name>/SKILL.md")` must return `[]`** for every lens.
- **P1 migration is migrate + soften, NOT verbatim.** The three transforms P1 applies, and nothing else:
  1. **Add the wrapper** (frontmatter + language line + provenance instruction). New wrapper prose follows the copy rules (no mid-sentence em-dash except headings/`— Frameworks:` label; no "rather than"/"instead of"/"X, not Y"; full-width CJK for CJK).
  2. **Drop deprecated-6-mode glue:** the `## 📎 File Integration Tips for This Stage` boilerplate blocks (chat-upload workflow) and the `**Applicable: <mode>/<completeness>/<audience>**` gating lines. These reference the mode system being removed; they do not belong in a lens.
  3. **Reframe always-on enforcement into proportional self-checks** (spec §8 P1 decision item): convert "Hard Gate", "contract failure", "MUST … or FAIL", "mandatory" always-on-blocking framing into proportional quality self-checks the lens applies when the output's quality needs it. Keep the substantive checklist CONTENT (what to check); remove the always-on-blocking FRAMING. When you rewrite a line to soften it, write the replacement copy-rule-compliant.
- **Everything else is migrated faithfully.** Pre-existing copy-rule issues (em-dash, contrast constructions) inside verbatim framework body, template YAML, or CSS are OUT OF SCOPE for P1 (a separate cleanup pass owns them, spec §8). Do not rewrite template placeholders, Mermaid/YAML examples, or CSS.
- **The authoritative source coordinates are the Source Map below**, verified against the repo. Where the spec's §4.3 prose and this map disagree (e.g. 05a split, 04b §3.6), the map governs.
- **No meta-skill edit in P1.** `skills/product-playbook/SKILL.md` already lists all 16 lens names in "Available lenses". Do not touch it; the fallback-line removal is P2.
- **Provenance tag string per lens is fixed by this plan** (see each task) so tests are deterministic.

---

## Authoritative Source Map (verified 2026-07-01, overrides spec §4.3 prose where they differ)

| Lens | Source(s) → lines | Provenance tag(s) | Ceremony to soften | Notes |
|---|---|---|---|---|
| `strategy-kernel` | `00-opportunity-check.md` 1–44 (full) + `01-strategy.md` 1–90 (full) + `05a-northstar-aha.md` 3–23 (§4.1 Empowered Teams only) | `Opportunity Check` `DHM` `Strategy Blocks` `Rumelt Kernel` `Empowered Teams` | none blocking (❌ at 01:59,63 are pedagogical OKR examples; keep) | 05a §4.1 belongs here, §4.2–4.4 belong to success-metrics |
| `persona-journey` | `02a-persona.md` 1–99 (full) + `02c-ost-journey.md` 27–54 (§1.5 Journey Map) | `Persona` `Journey Map` | HEAVY in 02a: Hard Gate ×4 (L3,28,32,53), MUST ×5 (L5,55,57,65,67), ❌ (L75), FAILS (L14,37,65) | drop 02c shared tips row (58–65) |
| `opportunity-solution-tree` | `02c-ost-journey.md` 3–25 (§1.4 OST) | `OST` | none | smallest source (880 chars); migrate faithfully, do not pad |
| `problem-framing` | `03-define.md` 11–20 (§2.1) + 51–77 (§2.3) + 79–107 (§2.4) | `Pain Points` `HMW` `Opportunity Assessment` | none | drop file glue 1–9 and tips 111–118 |
| `positioning` | `03-define.md` 22–49 (§2.2) | `Positioning` | none | 5 pre-existing copy issues in body → leave (deferred) |
| `pr-faq` | `04a-prfaq.md` 1–148 (full) | `PR-FAQ` | Hard Gate (L42), must ×5 (L34,52,65,71,83), mandatory (L65), ❌ (L34,46,54,89) | whole file is framework; no glue to drop |
| `mvp-scoping` | `04b-solutions.md` 3–16 (§3.2 Parallel Prototyping) + 91–99 (§3.6 User Story Table) + `04c-mvp.md` 1–21 (full: MVP + Not Doing List) | `MVP` `Not Doing List` `User Story` `Parallel Prototyping` | none | §3.6 is User Story (NOT Not Doing List); Not Doing List + MVP come from 04c. Pull from all three ranges. |
| `success-metrics` | `05a-northstar-aha.md` 25–93 (§4.2 + §4.4; EXCLUDE §4.1 lines 1–24) | `North Star` `Aha Moment` `Sean Ellis` | ❌ (L55), "must be achieved in order" (L57) | §4.1 is Empowered Teams → strategy-kernel, not here |
| `pmf-gtm` | `05b-pmf-gtm.md` 1–102 (full) | `PMF` `GTM` | none | drop Applicable gating (L22,59) + tips (97–102) |
| `product-spec-summary` | `05c-validation-spec.md` 1–117 (full, incl. §4.5 Hypothesis Validation Plan + §4.6 Spec Summary) | `Spec Summary` `Risk Register` | "must proactively add" (L61) | drop Applicable (L5) + tips (112–117) |
| `prd-and-handoff` | `04b-solutions.md` 103–259 (PRD template + Mermaid artifacts) + `07a-handoff-core.md` 1–152 (full) + `07b-tasks-tickets.md` 1–215 (full) + `07c-architecture-setup.md` 1–199 (full) + `08-security-checklist.md` 1–246 (full) | `PRD` `Handoff` `Security` | 08 is the primary target: reframe the two Hard Gate blocks (L210, L223) + FAIL/PASS example ceremony into a proportional security guardrail (silent by default, surfaces on payments/auth/PII signals). Fold triggers into the description. | ~978 lines; body split into 5 sub-sections (PRD, CLAUDE.md, TASKS/TICKETS, ARCHITECTURE/setup, Security). Drop tips (04b 261–269) + Applicable/Integration-Timing (08 201–208) + old-runtime "Claude Chat/Cowork" framing (07c 157–188 → adapt). |
| `document-export` | `06-html-report.md` 1–128 (full) + `rules-export-document.md` 1–346 (full) + COPY `templates/report-style.css` + `templates/prd-style.css` into `skills/document-export/assets/` | `HTML Report` `PDF Export` | none | update inline CSS read-paths in body to `assets/…`; first lens with bundled assets |
| `strategy-critic` | `agents/strategy-critic.md` 1–227 (full) | `Strategy Critique` | keep the "critic, not author" hard rule (role-identity constraint, not a user gate) | adapt subagent→lens: drop YAML `tools:`/`model:`, reword `summary_for_main_agent`/"orchestrator" → "critique output"/"user language", drop `recommended_handler` routing |

**Canonical test template** (each task instantiates this; document-export adds an asset check):

```python
import unittest, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from validate_skill import validate_skill

SKILL = "skills/<name>/SKILL.md"

class Test<Name>Lens(unittest.TestCase):
    def test_passes_validator(self):
        self.assertEqual(validate_skill(SKILL), [])

    def test_declares_tag_and_substance(self):
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertIn("`<PRIMARY_TAG>`", body)
        self.assertIn("<keyword1>", body.lower())
        self.assertIn("<keyword2>", body.lower())
        self.assertGreater(len(body), <threshold>)
```

---

## Task 1: `positioning` lens (simplest single-section, do first to reconfirm the pattern)

**Files:**
- Create: `skills/positioning/SKILL.md`
- Test: `tests/test_lens_positioning.py`

**Interfaces:**
- Consumes: `validate_skill`; framework body from `references/03-define.md` §2.2 lines 22–49 (April Dunford Positioning + Positioning Quality Checklist).
- Produces: a lens contributing the tag `Positioning`.

- [ ] **Step 1: Write the failing test** — `tests/test_lens_positioning.py` from the canonical template with `SKILL="skills/positioning/SKILL.md"`, `PRIMARY_TAG=Positioning`, keywords `"positioning"` and `"alternative"`, threshold `1200`.
- [ ] **Step 2: Run** `python3 -m unittest tests.test_lens_positioning -v` → expect FAIL (file missing).
- [ ] **Step 3: Create the lens.** Frontmatter `name: positioning` + this triggering-only description: "Use when the user needs to position a product against the alternatives customers actually consider. Triggers on 'positioning', 'competitive alternatives', 'differentiation', 'April Dunford', 'market category', and the same intent in any language." Add the language line + provenance instruction (tag `Positioning`). Under `## Framework`, migrate `references/03-define.md` lines 22–49 faithfully. No ceremony to soften; leave the section's pre-existing copy issues as-is.
- [ ] **Step 4: Run** the test → expect PASS. Then `python3 -m unittest discover tests` → no regressions.
- [ ] **Step 5: Commit** `feat: migrate April Dunford positioning to positioning lens skill`

## Task 2: `pr-faq` lens

**Files:** Create `skills/pr-faq/SKILL.md`; Test `tests/test_lens_pr_faq.py`
**Interfaces:** Consumes `validate_skill`; body from `references/04a-prfaq.md` lines 1–148 (whole file). Produces tag `PR-FAQ`.

- [ ] **Step 1:** Test from template: `PRIMARY_TAG=PR-FAQ`, keywords `"working backwards"` and `"press release"`, threshold `4000`.
- [ ] **Step 2:** Run → FAIL.
- [ ] **Step 3:** Create lens. `name: pr-faq`; description: "Use when the user wants to define a product by writing its launch press release and FAQ before building. Triggers on 'PR-FAQ', 'press release', 'working backwards', 'Amazon PR FAQ', 'write the launch announcement', and the same intent in any language." Migrate the whole file. **Soften:** reframe line 42 "Execution Rules (Hard Gate)" and the "must … FAIL / mandatory" self-verify language (L34,52,65,71,83) into a proportional "Quality self-check" (keep every check item; drop the FAIL/gate framing). Leave verbatim prose copy issues.
- [ ] **Step 4:** Run test → PASS; full suite → no regressions.
- [ ] **Step 5: Commit** `feat: migrate Working Backwards PR-FAQ to pr-faq lens skill`

## Task 3: `success-metrics` lens

**Files:** Create `skills/success-metrics/SKILL.md`; Test `tests/test_lens_success_metrics.py`
**Interfaces:** Consumes `validate_skill`; body from `references/05a-northstar-aha.md` lines **25–93 only** (§4.2 Success Metrics + §4.4 Aha Moment). EXCLUDE lines 1–24 (§4.1 Empowered Teams → strategy-kernel). Produces tag `North Star`.

- [ ] **Step 1:** Test from template: `PRIMARY_TAG=North Star`, keywords `"aha moment"` and `"sean ellis"`, threshold `2500`.
- [ ] **Step 2:** Run → FAIL.
- [ ] **Step 3:** Create lens. `name: success-metrics`; description: "Use when the user needs to define how success is measured: a North Star, supporting signals, and the activation moment. Triggers on 'North Star metric', 'success metrics', 'signals', 'aha moment', 'activation', 'Sean Ellis', and the same intent in any language." Migrate ONLY lines 25–93. **Soften:** line 57 "must be achieved in order" and line 55 ❌ into proportional guidance. Provenance instruction lists `North Star`, `Aha Moment`, `Sean Ellis`.
- [ ] **Step 4:** test PASS; full suite green.
- [ ] **Step 5: Commit** `feat: migrate North Star/Aha/Sean-Ellis to success-metrics lens skill`

## Task 4: `pmf-gtm` lens

**Files:** Create `skills/pmf-gtm/SKILL.md`; Test `tests/test_lens_pmf_gtm.py`
**Interfaces:** body from `references/05b-pmf-gtm.md` lines 1–102 (full). Produces tags `PMF`, `GTM`.

- [ ] **Step 1:** Test: assert BOTH `` `PMF` `` and `` `GTM` `` present; keywords `"product-market fit"` and `"pricing"`; threshold `3500`.
- [ ] **Step 2:** Run → FAIL.
- [ ] **Step 3:** Create lens. `name: pmf-gtm`; description: "Use when the user is assessing product-market fit or planning go-to-market and pricing. Triggers on 'PMF', 'product market fit', 'go to market', 'GTM', 'acquisition channels', 'pricing', 'business model', and the same intent in any language." Migrate the whole file. **Drop:** Applicable gating lines 22, 59 and the File Integration Tips block 97–102. No Hard Gate to soften.
- [ ] **Step 4:** test PASS; full suite green.
- [ ] **Step 5: Commit** `feat: migrate PMF/GTM/pricing to pmf-gtm lens skill`

## Task 5: `product-spec-summary` lens

**Files:** Create `skills/product-spec-summary/SKILL.md`; Test `tests/test_lens_product_spec_summary.py`
**Interfaces:** body from `references/05c-validation-spec.md` lines 1–117 (full: §4.5 Hypothesis Validation Plan + §4.6 Spec Summary + Risk Register + Gaps). Produces tags `Spec Summary`, `Risk Register`.

- [ ] **Step 1:** Test: `PRIMARY_TAG=Risk Register`; keywords `"blind spot"` and `"spec"`; threshold `3000`.
- [ ] **Step 2:** Run → FAIL.
- [ ] **Step 3:** Create lens. `name: product-spec-summary`; description: "Use when the user needs to consolidate planning into a final spec with a risk register and blind-spot review. Triggers on 'spec summary', 'final spec', 'risk register', 'gaps and blind spots', 'validation plan', 'wrap up the plan', and the same intent in any language." Migrate whole file. **Soften:** line 61 "must proactively add the following three sections" into "add these three sections by default (Risk Register, Gaps & Blind Spots, Additional Recommendations)". **Drop:** Applicable line 5 + tips 112–117.
- [ ] **Step 4:** test PASS; full suite green.
- [ ] **Step 5: Commit** `feat: migrate final spec summary to product-spec-summary lens skill`

## Task 6: `problem-framing` lens

**Files:** Create `skills/problem-framing/SKILL.md`; Test `tests/test_lens_problem_framing.py`
**Interfaces:** body from `references/03-define.md` §2.1 (11–20) + §2.3 (51–77) + §2.4 (79–107). Produces tags `Pain Points`, `HMW`, `Opportunity Assessment`.

- [ ] **Step 1:** Test: `PRIMARY_TAG=HMW`; keywords `"pain point"` and `"how might we"`; threshold `2500`.
- [ ] **Step 2:** Run → FAIL.
- [ ] **Step 3:** Create lens. `name: problem-framing`; description: "Use when the user needs to sharpen a vague problem into pain points, reframed questions, and ranked opportunities before designing solutions. Triggers on 'frame the problem', 'pain points', 'how might we', 'HMW', 'opportunity assessment', 'what problem', and the same intent in any language." Migrate the three ranges in order (2.1, 2.3, 2.4). **Drop** the file preamble 1–9 and tips 111–118. No Hard Gate to soften (zero ceremony).
- [ ] **Step 4:** test PASS; full suite green.
- [ ] **Step 5: Commit** `feat: migrate pain-point/HMW/opportunity to problem-framing lens skill`

## Task 7: `opportunity-solution-tree` lens

**Files:** Create `skills/opportunity-solution-tree/SKILL.md`; Test `tests/test_lens_ost.py`
**Interfaces:** body from `references/02c-ost-journey.md` lines 3–25 (§1.4 OST). Produces tag `OST`.

- [ ] **Step 1:** Test: `PRIMARY_TAG=OST`; keywords `"opportunity"` and `"outcome"`; threshold `800`.
- [ ] **Step 2:** Run → FAIL.
- [ ] **Step 3:** Create lens. `name: opportunity-solution-tree`; description: "Use when the user wants to connect a desired outcome to opportunities and candidate solutions in a structured tree. Triggers on 'opportunity solution tree', 'OST', 'map opportunities', 'outcome to solutions', 'Teresa Torres', and the same intent in any language." Migrate lines 3–25 faithfully (keep the ASCII tree + core principles). This is the smallest source; do NOT pad with invented content. Provenance instruction: tag `OST`.
- [ ] **Step 4:** test PASS; full suite green.
- [ ] **Step 5: Commit** `feat: migrate Teresa Torres OST to opportunity-solution-tree lens skill`

## Task 8: `mvp-scoping` lens

**Files:** Create `skills/mvp-scoping/SKILL.md`; Test `tests/test_lens_mvp_scoping.py`
**Interfaces:** body from `references/04b-solutions.md` §3.2 (3–16, Parallel Prototyping) + §3.6 (91–99, User Story Table) + `references/04c-mvp.md` (1–21, MVP + Not Doing List). Produces tags `MVP`, `Not Doing List`, `User Story`, `Parallel Prototyping`.

- [ ] **Step 1:** Test: assert BOTH `` `MVP` `` and `` `User Story` `` present; keywords `"not doing"` and `"parallel"`; threshold `1200`.
- [ ] **Step 2:** Run → FAIL.
- [ ] **Step 3:** Create lens. `name: mvp-scoping`; description: "Use when the user needs to decide what makes the first version and what to explicitly not build. Triggers on 'MVP', 'scope', 'not doing list', 'must have vs later', 'user stories', 'parallel prototypes', and the same intent in any language." Migrate the three ranges as `## Framework` sub-sections (Parallel Prototyping / User Story / MVP scope + Not Doing List). NOTE: §3.6 is the User Story Table; the Not Doing List and MVP scope table come from 04c. No Hard Gate to soften.
- [ ] **Step 4:** test PASS; full suite green.
- [ ] **Step 5: Commit** `feat: migrate MVP/Not-Doing/User-Story/parallel-proto to mvp-scoping lens skill`

## Task 9: `strategy-kernel` lens (composite, 3 sources)

**Files:** Create `skills/strategy-kernel/SKILL.md`; Test `tests/test_lens_strategy_kernel.py`
**Interfaces:** body from `references/00-opportunity-check.md` (1–44, full) + `references/01-strategy.md` (1–90, full) + `references/05a-northstar-aha.md` (3–23, §4.1 Empowered Teams). Produces tags among `Opportunity Check`, `DHM`, `Strategy Blocks`, `Rumelt Kernel`, `Empowered Teams`.

- [ ] **Step 1:** Test: assert `` `Rumelt Kernel` `` and `` `DHM` `` present; keywords `"strategy"` and `"empowered"`; threshold `5000`.
- [ ] **Step 2:** Run → FAIL.
- [ ] **Step 3:** Create lens. `name: strategy-kernel`; description: "Use when the user is setting or pressure-testing product strategy, direction, or the case for an opportunity, before committing resources. Triggers on 'product strategy', 'is this opportunity worth it', 'strategy kernel', 'DHM', 'diagnosis', 'guiding policy', 'OKR', 'empowered team', and the same intent in any language." Migrate the three sources as `## Framework` sub-sections (Opportunity Check + DHM; Strategy Blocks / Rumelt / Shreyas three-layer / LNO / OKR / Three Core Questions; Empowered Teams). Provenance instruction: "contribute the tag(s) for whichever you applied: `Opportunity Check`, `DHM`, `Strategy Blocks`, `Rumelt Kernel`, `Empowered Teams`." Keep the ❌ OKR examples (01:59,63) as pedagogical good/bad examples (not gate ceremony).
- [ ] **Step 4:** test PASS; full suite green.
- [ ] **Step 5: Commit** `feat: migrate strategy kernel (opportunity/DHM/Rumelt/blocks/empowered) to lens skill`

## Task 10: `persona-journey` lens (composite, highest ceremony)

**Files:** Create `skills/persona-journey/SKILL.md`; Test `tests/test_lens_persona_journey.py`
**Interfaces:** body from `references/02a-persona.md` (1–99, full) + `references/02c-ost-journey.md` (27–54, §1.5 Journey Map). Produces tags `Persona`, `Journey Map`.

- [ ] **Step 1:** Test: assert BOTH `` `Persona` `` and `` `Journey Map` `` present; keywords `"buyer"` and `"journey"`; threshold `6000`.
- [ ] **Step 2:** Run → FAIL.
- [ ] **Step 3:** Create lens. `name: persona-journey`; description: "Use when the user needs to understand who the users are and how they move through an experience. Triggers on 'persona', 'target user', 'buyer vs user', 'user journey', 'journey map', 'touchpoints', and the same intent in any language." Migrate 02a (full) + 02c §1.5. **Soften (heaviest pass in this phase):** reframe every Hard Gate label (02a L3,28,32,53), the MUST/FAILS enforcement (L5,14,37,55,57,65,67), and ❌ (L75) into proportional self-checks. KEEP the substantive content: B2B Buyer≠User distinction, persona prioritization reasoning, the persona quality checklist items. **Drop** the 02c shared File Integration Tips row.
- [ ] **Step 4:** test PASS; full suite green.
- [ ] **Step 5: Commit** `feat: migrate persona + user-journey to persona-journey lens skill`

## Task 11: `strategy-critic` lens (subagent → lens adaptation)

**Files:** Create `skills/strategy-critic/SKILL.md`; Test `tests/test_lens_strategy_critic.py`
**Interfaces:** body adapted from `agents/strategy-critic.md` (1–227). Produces tag `Strategy Critique`. Do NOT modify `agents/strategy-critic.md`.

- [ ] **Step 1:** Test: `PRIMARY_TAG=Strategy Critique`; keywords `"critic"` and `"diagnosis"`; threshold `6000`.
- [ ] **Step 2:** Run → FAIL.
- [ ] **Step 3:** Create lens. `name: strategy-critic`; description: "Use immediately after the user writes or revises a strategy artifact (strategy kernel, DHM, strategy blocks, empowered-team charter) to stress-test it before it propagates. Triggers on 'critique this strategy', 'is this strategy any good', 'poke holes', 'red team the strategy', and the same intent in any language." Migrate the METHOD (posture, scope, classify-before-critique, the four critique frameworks, blind-spot detection, structured output, self-check). **Adapt subagent→lens:** drop YAML `tools:`/`model:` frontmatter; reword `summary_for_main_agent` and "orchestrator" to "the critique output" / "the user's language"; drop the `recommended_handler` routing (replace "refuse cleanly to another subagent" with "if the artifact is not yet a strategy, say so and point to the relevant lens"). **KEEP** the "critic, not author" hard rule verbatim (it is the role-identity constraint that makes this a critic, not an always-on user gate).
- [ ] **Step 4:** test PASS; full suite green.
- [ ] **Step 5: Commit** `feat: adapt strategy-critic subagent into a strategy-critic lens skill`

## Task 12: `document-export` lens (bundled CSS assets)

**Files:**
- Create: `skills/document-export/SKILL.md`, `skills/document-export/assets/report-style.css`, `skills/document-export/assets/prd-style.css`
- Test: `tests/test_lens_document_export.py`

**Interfaces:** body from `references/06-html-report.md` (1–128) + `references/rules-export-document.md` (1–346); assets copied from `references/templates/{report-style,prd-style}.css`. Produces tags `HTML Report`, `PDF Export`.

- [ ] **Step 1:** Write the test — canonical template with `PRIMARY_TAG=HTML Report`, keywords `"pdf"` and `"report"`, threshold `6000`, PLUS an asset check:

```python
    def test_css_assets_bundled(self):
        self.assertTrue(pathlib.Path("skills/document-export/assets/prd-style.css").exists())
        self.assertTrue(pathlib.Path("skills/document-export/assets/report-style.css").exists())
```

- [ ] **Step 2:** Run `python3 -m unittest tests.test_lens_document_export -v` → FAIL.
- [ ] **Step 3:** Copy both CSS files verbatim into `skills/document-export/assets/`. Create the lens. `name: document-export`; description: "Use when the user wants the plan rendered as an interactive HTML report or exported to PDF/DOCX/PPTX. Triggers on 'HTML report', 'export to PDF', 'export document', 'downloadable report', 'PDF/DOCX/PPTX', and the same intent in any language." Migrate 06 + rules-export-document bodies. **Update** the inline CSS read-instructions (they point at `references/templates/prd-style.css`) to the new `assets/prd-style.css` / `assets/report-style.css` paths. No Hard Gate to soften.
- [ ] **Step 4:** test PASS (incl. asset check); full suite green.
- [ ] **Step 5: Commit** `feat: migrate HTML report + PDF export (with CSS assets) to document-export lens skill`

## Task 13: `prd-and-handoff` lens (heavy composite, 5 sources, security-guardrail reframe)

**Files:** Create `skills/prd-and-handoff/SKILL.md`; Test `tests/test_lens_prd_and_handoff.py`
**Interfaces:** body from `references/04b-solutions.md` (103–259, PRD template + Mermaid artifacts) + `07a-handoff-core.md` (1–152) + `07b-tasks-tickets.md` (1–215) + `07c-architecture-setup.md` (1–199) + `08-security-checklist.md` (1–246). Produces tags `PRD`, `Handoff`, `Security`.

- [ ] **Step 1:** Test: assert `` `PRD` `` and `` `Handoff` `` present; keywords `"tasks.md"` and `"architecture"`; threshold `20000`. Also assert the security content survived but the gate framing did not:

```python
    def test_security_reframed_not_hard_gate(self):
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertIn("security", body.lower())          # content kept
        self.assertNotIn("Hard Gate", body)              # always-on framing removed
```

- [ ] **Step 2:** Run → FAIL.
- [ ] **Step 3:** Create lens. `name: prd-and-handoff`; description: "Use when the user needs an engineer-ready PRD or a development handoff package (CLAUDE.md, TASKS, TICKETS, ARCHITECTURE, setup). Triggers on 'PRD', 'product requirements doc', 'handoff to engineering', 'dev handoff', 'TASKS.md', 'TICKETS', 'architecture doc', and the same intent in any language." Migrate the five sources as five `## Framework` sub-sections: (1) PRD template + Mermaid artifacts, (2) CLAUDE.md + handoff overview + tech-stack flow, (3) TASKS.md + TICKETS.md + breakdown logic, (4) ARCHITECTURE.md + .gitignore + setup.sh, (5) Security checkpoint. **Soften (primary target of this task):** reframe 08's two Hard Gate blocks (L210 "Always Ship … Security Section", L223 "TASKS.md Must Contain … Security Tasks") and the FAIL/PASS example ceremony into a proportional security guardrail: the security section is produced by default and surfaces prominently when the feature touches payments/auth/PII, keeping the substantive checklist (the 5 named areas, the OWASP reference) but dropping the "never refuse/block/defer … MUST … or FAIL" gate framing. **Drop:** 04b tips (261–269), 08 Integration-Timing table (201–208, references old mode names), and adapt 07c "Claude Chat/Cowork" runtime framing (157–188) to lens-neutral wording.
- [ ] **Step 4:** test PASS (incl. both custom assertions); full suite green.
- [ ] **Step 5: Commit** `feat: migrate PRD + dev-handoff + security into prd-and-handoff lens skill`

---

## After all 13 tasks

- [ ] **Final whole-branch review** (superpowers:requesting-code-review, most capable model). Package: `scripts/review-package $(git merge-base main HEAD) HEAD`. Focus: source-map fidelity (right lines migrated, nothing double-claimed, 05a/02c/03/04b splits correct), the soften-pass consistency (no always-on Hard Gate framing survived in migrated bodies, substantive content kept), document-export assets present and paths updated, strategy-critic adaptation (no subagent plumbing leaked), and that all 16 lenses now validate.
- [ ] Fix Critical/Important via one fix subagent; record Minors in the ledger.
- [ ] **superpowers:finishing-a-development-branch.**
- Note: removing the meta-skill's `references/`/`agents/` fallback line, deleting the legacy 6-mode dispatch hook, and i18n cut are P2, not this phase.

## Self-Review (author checklist, done)

- **Spec coverage:** all 13 remaining lenses from spec §4.3 have a task; the 3 P0 lenses are excluded. ✓
- **Source accuracy:** coordinates verified by three independent source-mapping passes; spec-vs-repo discrepancies (05a split, 04b §3.6 = User Story, prd source = 04b 103–259) are resolved in the map, which governs. ✓
- **Type/interface consistency:** every task uses `validate_skill`, the canonical unittest template, and a fixed provenance tag string. ✓
- **No placeholders:** every task has exact source lines, exact description text, exact test values, exact commit message. ✓
