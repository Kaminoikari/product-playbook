# 🔄 Revision Mode Step Sequence (6 Core + 2 Optional, total 6–8 steps)

> Authoritative step definition for Revision Mode. Dispatched from SKILL.md.

**Slimmed from the original 12-step flow (v1.0.x) by merging redundant frameworks and gating optional ones behind trigger conditions.** See `references/rules-optional-trigger.md` for trigger logic and Phase Decision Point format.

## Step Sequence

```
Phase 0: Current State Analysis
  S1.  Current State Review + JTBD Re-validation  [Core]
       (Merged: data inventory + which existing Jobs are done well/poorly)

Phase 1: Problem Convergence
  S2.  User Pain Points Collection  [Core]
       (Retention/churn analysis + feedback synthesis + behavior data)
  S3.  Pain Points + HMW + Opportunity Ranking  [Core]
       → references/03-define.md
       (Merged: Pain Points Summary + HMW + Opportunity Assessment Table)
  S4.  Positioning Re-assessment  [Optional — see triggers]
       → references/03-define.md

Phase 2: Solution Design
  S5.  PR-FAQ (post-revision experience)  [Core]
       → references/04a-prfaq.md
  S6.  Pre-mortem  [Optional — see triggers]
       → references/04b-solutions.md
  S7.  MVP + Not Doing List  [Core]
       → references/04c-mvp.md

Phase 3: Validation
  S8.  North Star + Aha (before/after comparison) + Hypothesis Validation Plan  [Core]
       → references/05a-northstar-aha.md + references/05c-validation-spec.md
       (Merged: any revision must validate hypotheses; tightly coupled)

────
Final output → Product Spec Summary (revision edition)
```

### S1 Pre-step: Product Context Loading

Before entering S1, read `references/rules-context.md` and check `.product-context.md`:

- **Full context (Scenario 1)**: Auto-fill PMF level, North Star, known pain points, security posture, last 3 Decision History entries. Switch S1 to **diff-style prompting**: "Last assessment had your PMF level at [X] and North Star at [Y]. Have these changed? What are the latest DAU/MAU and retention numbers?" — historical decisions and known pain points do not need to be re-collected.
- **No context (Scenario 2)**: Trigger Context Bootstrap (`rules-context.md` Section 4, Round 1 + 3), then enter standard S1 data collection.
- **Partial context (Scenario 3)**: Pull feature change history from Decision History (which modules have been touched, which risks have been identified), but ask about overall product strategy and metrics (previously only feature extension was done — global view is missing).

### S1 Standard Prompting

> Revision Mode's S1 actively asks the user for existing product data: DAU/MAU, retention, primary user feedback, key decisions from past versions, etc. If context already pre-fills some answers, switch to confirmation rather than re-collection.
> S1 also collects current security posture: existing auth/authz mechanisms, known security gaps or tech debt, recent security incidents. This data feeds into revision risk assessment and Pre-mortem (if triggered).

### S1 Output Requirements (Hard Gates)

Every Revision Mode S1 response MUST contain ALL FOUR of:

1. **Frame this as revision, not 0-to-1** — open with one or two sentences calling out that this is an *existing-product* analysis: we are re-validating existing JTBD against current data, comparing baseline metrics, and reading `.product-context.md` for prior decisions. This differs from 0-to-1 Discovery (which starts from a blank user model). Without this framing, the user can't tell why the questions are different.

2. **Use the user's actual numbers verbatim** — quote MAU, retention drop %, cohort sizes, dates from the user's prompt back to them in your analysis (e.g. "the drop from 85% to 72% last quarter, against the 2,800 MAU base, means roughly N affected users…"). Generic discussion that ignores the numbers FAILS this gate.

3. **Treat the user's stated cause as H1, not as fact** — when the user names a likely cause ("retention drop is caused by feature complexity"), label it H1 explicitly and surface at least TWO rival hypotheses (H2, H3) drawn from the same data. Example rival hypotheses to consider: cohort mix shift, onboarding regression, pricing change, competitive launch, support-quality drop, feature deprecation, seasonal effect. **Uncritically accepting the user's stated cause FAILS this gate** — Revision Mode's value is hypothesis discipline.

4. **Data gaps list with at least one segmentation-oriented gap** — list specifically what additional data is needed to discriminate between H1/H2/H3. **At least one item MUST be a segmentation gap**: cohort (signup month), tier (free/paid), role (admin/user), feature-usage segment. Generic "more user interviews" alone FAILS — name *which segment* you'd interview and *what specifically* you'd ask.

### S1 Closing Format (Hard Gate)

End the S1 response with a numbered CTA menu, NEVER an open-ended question. Use this exact shape:

```
What's next? Pick one:
  1️⃣ Share the requested data so we can move to S2 (pain-point convergence with hypothesis testing)
  2️⃣ Refine the hypothesis list before collecting data (suggest more H_n candidates)
  3️⃣ Skip to S3 if you already have enough data to converge on a top hypothesis
  4️⃣ Pause and resume later (progress will be saved to .product-playbook-progress.md)
```

Responses ending with "Any thoughts?" / "Let me know what you think" / "Share what you have" without a numbered menu FAIL the contract — the user needs a clear handle for the next move.

### Fast Path

When the user provides sufficient data in S1 (with feedback, metrics, priorities), S3 may be produced in a single back-and-forth instead of multiple confirmations. Trigger condition: the pain point list collected in S2 already has explicit priorities and data backing. Hard Gate rules remain — each step's output must still be presented in full; only the confirmation cadence accelerates.

## Optional Trigger Rules

Read `references/rules-optional-trigger.md` for the authoritative trigger conditions and Phase Decision Point output format.

**Quick reference:**
- **S4 Positioning Re-assessment** triggers when: user mentions "positioning drift" / "market changed" / audience includes Sales/Marketing
- **S6 Pre-mortem** triggers when: change scope ≥30% of existing functionality / touches payments-permissions-data migration

## Phase Decision Point Requirement

Before entering Phase 1 and Phase 2, render the Phase Decision Point block (format defined in `rules-optional-trigger.md`). Phase 0 and Phase 3 contain only Core steps and skip the decision point.

## Reference Loading Instructions

| Step | Reference File |
|------|---------------|
| S1–S2 | (no external reference; direct user-data collection) |
| S3 | `references/03-define.md` |
| S4 (if triggered) | `references/03-define.md` |
| S5 | `references/04a-prfaq.md` |
| S6 (if triggered) | `references/04b-solutions.md` |
| S7 | `references/04c-mvp.md` |
| S8 + final output | `references/05a-northstar-aha.md` + `references/05c-validation-spec.md` |

## Step Count Summary

| Scenario | Steps |
|----------|-------|
| Default (Core only) | **6** |
| All Optional triggered | 8 |
| (Legacy 12-step flow) | 12 |

## Final Output Format

**Revision Product Spec Summary**: before/after comparison + what's changing / what's not + success metrics.

The summary MUST disclose any skipped Optional steps and offer a one-command path to add them back (per `rules-optional-trigger.md` Section 6).

After completion, follow `references/rules-end-of-flow.md` for end-of-flow rules.
