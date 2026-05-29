# Eval Lift Report — 2026-05-29

- **Before**: `docs/sprint1-local-eval-2026-05-28.json` (score **0**, band `at-risk`)
- **After**:  `evals/post-closed-loop-eval.json` (score **0**, band `at-risk`)
- **Score Δ**: 0 → 0 (**+0**)
- **Net hard lift**: **+95** points ✅ (gain +125 / loss -30)

## Movement Summary

| Class | Count |
|-------|------:|
| 🟢 Improved (fail → pass) | 17 |
| 🔴 Regressed (pass → fail) | 2 |
| ⚪ Unchanged-pass | 11 |
| ⚪ Unchanged-fail | 1 |
| 〰️ Soft moves (still failing but ratio shifted) | 0 |
| ➕ Added expectations | 51 |
| ➖ Removed expectations | 2 |

## 🟢 Improved (highest-leverage wins)

| Eval | Severity | Expectation | Before | After |
|------|----------|-------------|-------:|------:|
| eval-jtbd-depth | 🔴 critical | B2B analysis includes organization-level Jobs (e.g., compliance auditing, cross-department | 0/1 | 1/1 |
| eval-subagent-discovery | 🔴 critical | For this B2B product, the buyer persona and the daily-user persona are treated as separate | 0/1 | 1/1 |
| eval-subagent-discovery | 🔴 critical | JTBD analysis includes all three layers explicitly: functional, emotional, and social | 0/1 | 1/1 |
| eval-subagent-discovery | 🔴 critical | Output stays within Discovery scope — does NOT contain named Develop/Deliver/Strategy arti | 0/1 | 1/1 |
| eval-jtbd-depth | 🟡 warning | Quality self-review checklist contains at least 1 explicit cross/fail marker (warning mark | 0/1 | 1/1 |
| eval-jtbd-depth | 🟡 warning | Clearly states which Persona to prioritize and provides specific reasoning | 0/1 | 1/1 |
| eval-jtbd-depth | 🟡 warning | Prioritization reasoning references B2B-specific dynamics (champion vs buyer, adoption mul | 0/1 | 1/1 |
| eval-jtbd-depth | 🟡 warning | Quality self-review checklist marks each item as pass or fail (using checkmark or cross ma | 0/1 | 1/1 |
| eval-jtbd-depth | 🟡 warning | Includes a complete Five Whys deep-dive with at least 3-5 progressively deeper 'why' quest | 0/1 | 1/1 |
| eval-prfaq-output | 🟡 warning | PR-FAQ is internally consistent: numbers cited in the Lead match what the Solution promise | 0/1 | 1/1 |
| eval-prfaq-output | 🟡 warning | Internal FAQ section is present and identifies a riskiest / weakest assumption with a conc | 0/1 | 1/1 |
| eval-prfaq-output | 🟡 warning | Quality self-review checklist contains at least 1 explicit cross/fail marker (warning mark | 0/1 | 1/1 |
| eval-prfaq-output | 🟡 warning | External FAQ contains at least 1 pointed challenge comparing to existing tools (e.g., 'Why | 0/1 | 1/1 |
| eval-prfaq-output | 🟡 warning | The first sentence of the solution paragraph starts with user experience or a usage scenar | 0/1 | 1/1 |
| eval-subagent-discovery | 🟡 warning | Persona is built on motivations and context (goals, pain points, triggering events) rather | 0/1 | 1/1 |
| eval-subagent-discovery | 🟡 warning | Because no user research was provided, low-evidence claims are explicitly flagged as low c | 0/1 | 1/1 |
| eval-subagent-discovery | 🟡 warning | JTBD statements use the canonical 'When [situation], I want to [motivation], so I can [out | 0/1 | 1/1 |

## 🔴 Regressed (action required — patch reverted gains)

| Eval | Severity | Expectation | Before | After |
|------|----------|-------------|-------:|------:|
| eval-subagent-premortem | 🔴 critical | Produces a substantial set of failure scenarios, targeting 15 or more, with at least 2 sce | 1/1 | 0/1 |
| eval-subagent-premortem | 🔴 critical | Coverage spans all five failure categories: product/UX, market/demand, team/execution, ope | 1/1 | 0/1 |

## ➕➖ Expectation Set Changes

**Added** (typically new harness coverage):
- `eval-revision-mode` [warning]: Uses the specific data provided in the prompt (MAU 2,800, retention drop from 85% to 72%) in the response
- `eval-feature-extension` [warning]: Pauses after S1 completion AND makes an explicit commitment not to advance to S2 without confirmation (e.g., 'I will not
- `eval-quick-mode-jtbd` [info]: Displays a progress indicator at the beginning of the response that shows all three Quick Mode steps (S1, S2, S3) with e
- `eval-context-bootstrap` [critical]: Identifies this as a feature extension scenario (adding a new feature to an existing product)
- `eval-quick-mode-jtbd` [critical]: Response contains no code creation, file creation, or development commands (Hard Gate compliance: development operations
- `eval-security-awareness` [critical]: Developer handoff package includes a security-related section covering at least 4 of: authentication/authorization, inpu
- `eval-subagent-strategy-critic` [warning]: At least one blind spot is surfaced (e.g. no explicit trade-offs, no competitive landscape, no invalidating assumption, 
- `eval-mode-selection` [warning]: Does not push a single mode as the answer before the user picks — a brief 'these two might suit you' note is fine, but a
- `eval-security-awareness` [warning]: At least one security task lists concrete numeric or configuration values (e.g., password hashing parameters like argon2
- `eval-security-awareness` [warning]: Raises security considerations specific to social platforms (at least 1 of: XSS protection, user-uploaded content filter
- `eval-context-bootstrap` [critical]: Enters the 4-step feature extension flow (not the full 9–11 step Full Mode or 6–8 step Revision Mode)
- `eval-quality-hardgate` [warning]: Quality self-review checklist uses explicit pass or fail markers for each item (no blank checkboxes allowed)
- `eval-quick-mode-jtbd` [warning]: Output stays scoped to S1 — no PR-FAQ press release, no External FAQ, no North Star Metric definition, and no other S2/S
- `eval-quality-hardgate` [critical]: All three JTBD layers (Functional, Emotional, Social) are present and each uses the canonical 'When [situation], I want 
- `eval-context-bootstrap` [warning]: Bootstrap is sequenced as Step 0 BEFORE feature extension S1 (not interleaved with S1) — the response clearly shows Boot
- `eval-security-awareness` [critical]: No artifacts are promised in the handoff file tree but missing from the actual output (e.g., PRD.md or PRODUCT-SPEC.md l
- `eval-revision-mode` [info]: Displays a Revision Mode progress indicator at the beginning of the response (including the step sequence)
- `eval-feature-extension` [warning]: Includes a quality self-check that identifies a specific weakness in the current S1 work (e.g., an assumption not yet va
- `eval-context-bootstrap` [info]: Mentions that product context will be saved for future use AND references the persistence file path (.product-context.md
- `eval-quick-mode-jtbd` [warning]: The post-S1 question is a meaningful question about JTBD decisions (not a generic 'Any thoughts?' but rather a confirmat
- `eval-quick-mode-jtbd` [warning]: Surfaces confidence or validation status for the JTBD claims (e.g., flags assumptions, marks unvalidated claims for user
- `eval-quality-hardgate` [warning]: Quality self-review checklist contains at least 1 explicit cross/fail marker on a SUBSTANTIVE content gap (a cosmetic fl
- `eval-mode-selection` [info]: Responds in English
- `eval-revision-mode` [critical]: Treats 'feature complexity' as a hypothesis to validate (H1), not as a confirmed root cause; surfaces at least one rival
- `eval-mode-selection` [critical]: Has not started executing any product framework analysis (no JTBD, Persona, PR-FAQ, etc. output produced)
- `eval-mode-selection` [critical]: Response presents modes as a clear selection menu (numbered options or table) and lists at least the six modes Quick, Fu
- `eval-security-awareness` [warning]: Handoff includes an actual .gitignore file body (or explicit file content block) with concrete entries for .env, *.pem /
- `eval-mode-selection` [warning]: This turn only asks about mode selection, does not simultaneously ask about product type or completeness level (three-st
- `eval-quality-hardgate` [warning]: The final question in the Five Whys (Q5) uses explicit emotional vocabulary (e.g., fear, anxiety, shame, worry, dread, s
- `eval-subagent-strategy-critic` [critical]: The overall verdict is not 'strong' — the response clearly identifies this as a weak strategy or not yet a strategy
- `eval-quality-hardgate` [warning]: Failed items include a specific improvement explanation that references a downstream step or artifact dependent on the f
- `eval-subagent-strategy-critic` [critical]: The response returns strengthening questions for the writer and does NOT rewrite the strategy on the user's behalf. The 
- `eval-revision-mode` [critical]: Clearly identifies this as an existing product revision scenario, not a 0-to-1 new product
- `eval-revision-mode` [warning]: After S1, provides the user with clear action options (numbered menu or specific CTAs), not an open-ended question (e.g.
- `eval-revision-mode` [warning]: Explains how Revision Mode differs from a 0-to-1 Discovery workflow (e.g., references re-validating existing JTBD, basel
- `eval-feature-extension` [critical]: Identifies this as a feature extension scenario (not Full Mode or Revision Mode) and activates the 4-step fast path
- `eval-context-bootstrap` [warning]: Before feature planning, collects or confirms basic product information (product name TaskPro, product type B2B/B2C, one
- `eval-context-bootstrap` [warning]: Confirms or references the tech stack already provided by the user (React + Node.js + MongoDB) without asking for re-des
- `eval-security-awareness` [critical]: TASKS.md or the task list includes security-related tasks (not just a vague description buried in the last phase)
- `eval-revision-mode` [warning]: Lists additional data or information that needs to be collected, including at least one segmentation-oriented gap (cohor
- `eval-feature-extension` [warning]: Analyzes which existing modules the Wishlist feature would affect (mentions at least cart and catalog)
- `eval-quick-mode-jtbd` [critical]: Includes at least three JTBD types: Functional, Emotional, and Social
- `eval-subagent-strategy-critic` [critical]: The critique scores the diagnosis as missing or weak, explaining that the strategy names no central challenge (it states
- `eval-feature-extension` [warning]: Confirms or references the tech stack already provided by the user (Next.js + PostgreSQL + Redis) and the module list, w
- `eval-quick-mode-jtbd` [warning]: JTBD analysis includes concrete usage scenario descriptions (not abstract feature lists)
- `eval-revision-mode` [warning]: Does not propose a specific revision or feature change at S1 — stays in problem-framing, not jumping to a solution like 
- `eval-subagent-strategy-critic` [warning]: Each critique points at a specific quoted sentence from the strategy and cites which principle is violated, rather than 
- `eval-quick-mode-jtbd` [warning]: After completing S1, asks the user for confirmation or feedback; does not automatically proceed to S2
- `eval-feature-extension` [info]: Displays the feature extension progress indicator at the beginning of the response (S1/S4, not S1/S7 or S1/S12)
- `eval-quick-mode-jtbd` [warning]: JTBD statements use the canonical 'When [situation], I want to [motivation], so [outcome]' template with all three claus
- `eval-feature-extension` [critical]: Does not ask the user to provide JTBD, Persona, North Star, or other global product strategy elements unrelated to featu

**Removed** (typically harness pruning):
- `eval-subagent-premortem` [critical]: The orchestrator explicitly delegates to the pre-mortem-runner sub-agent — either via a real Task tool call with subagen
- `eval-subagent-discovery` [critical]: The orchestrator explicitly delegates to the discovery-specialist sub-agent — either via a real Task tool call with suba
