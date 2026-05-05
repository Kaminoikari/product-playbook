# 📦 Full Mode Step Sequence (8 Core + 1 Default-ON + 2 Optional, total 9–11 steps)

> Authoritative step definition for Full Mode. Dispatched from SKILL.md.

**Slimmed from the original 20-step flow (v1.0.x) by merging redundant frameworks and gating optional ones behind trigger conditions.** See `references/rules-optional-trigger.md` for trigger logic and Phase Decision Point format.

**Note on Journey Map (S3)**: Default ON. Persona-Journey is a bundled pair regardless of whether the product is 0-to-1 or an existing product — the relevant variable is whether the user's Job spans multiple stages. Skip only when the situation is genuinely too simple (single API/button, flow ≤2 steps, or user explicitly requests skip).

## Step Sequence

```
Phase 0: Strategy
  S1.  Strategy Diagnosis  [Core]
       → references/00-opportunity-check.md + references/01-strategy.md
       (Merged: Opportunity + DHM + Strategy Blocks + Rumelt Kernel)

Phase 1: Discovery
  S2.  Persona (Table + Cards)  [Core]
       → references/02a-persona.md
  S3.  User Journey Map  [Default ON — skip only if situation is too simple]
       → references/02c-ost-journey.md
  S4.  JTBD Analysis  [Core]
       → references/02b-jtbd.md

Phase 2: Define
  S5.  Pain Points + HMW + Opportunity Ranking  [Core]
       → references/03-define.md
       (Merged: Pain Points Summary + HMW + Opportunity Assessment;
        OST tree visualization is an optional sub-format inside this step)
  S6.  April Dunford Positioning  [Optional — see triggers]
       → references/03-define.md

Phase 3: Develop
  S7.  PR-FAQ (Working Backwards)  [Core]
       → references/04a-prfaq.md
  S8.  Solution Evaluation  [Core]
       → references/04b-solutions.md
       (Merged: Parallel Prototypes + Pre-mortem + GEM + RICE)
  S9.  MVP + Not Doing List  [Core]
       → references/04c-mvp.md

Phase 4: Deliver
  S10. North Star + Three-Layer Signals + Aha Moment  [Core]
       → references/05a-northstar-aha.md
  S11. PMF + GTM + Business Model + Hypothesis Validation Plan  [Optional — see triggers]
       → references/05b-pmf-gtm.md + references/05c-validation-spec.md

────
Final output → Product Spec Summary (references/05c-validation-spec.md → 4.6) + Best Entry Point Analysis
```

> When the audience is Executives or Cross-functional Alignment, prepend the Empowered Teams framework before S10.

## Optional Trigger Rules

Read `references/rules-optional-trigger.md` for the authoritative trigger conditions and Phase Decision Point output format.

**Quick reference:**
- **S3 Journey Map** (Default ON): proceed unless single interaction point / flow ≤2 steps / user requests skip
- **S6 Positioning** (Default OFF): trigger on new product launch / repositioning / audience includes Sales-BD-Marketing
- **S11 PMF/GTM/BM/Validation** (Default OFF): trigger on product launch / audience is Exec or Data Scientist / user requests validation plan

## Phase Decision Point Requirement

Before entering Phase 1, Phase 2, and Phase 4, render the Phase Decision Point block (format defined in `rules-optional-trigger.md`). Phase 0 and Phase 3 contain only Core steps and skip the decision point.

## Reference Loading Instructions

Load each reference file ONLY when entering its corresponding step (do not pre-load all references):

| Step | Reference File |
|------|---------------|
| S1 | `references/00-opportunity-check.md` + `references/01-strategy.md` |
| S2 | `references/02a-persona.md` |
| S3 (if triggered) | `references/02c-ost-journey.md` |
| S4 | `references/02b-jtbd.md` |
| S5 | `references/03-define.md` |
| S6 (if triggered) | `references/03-define.md` |
| S7 | `references/04a-prfaq.md` |
| S8 | `references/04b-solutions.md` |
| S9 | `references/04c-mvp.md` |
| S10 | `references/05a-northstar-aha.md` |
| S11 (if triggered) | `references/05b-pmf-gtm.md` + `references/05c-validation-spec.md` |
| Final output | `references/05c-validation-spec.md` |

## Step Count Summary

| Scenario | Steps |
|----------|-------|
| Default (8 Core + S3 Journey ON) | **9** |
| Simple flow (S3 skipped) | 8 |
| 1 Default-OFF Optional triggered (S6 or S11) | 10 |
| All Optionals triggered | 11 |
| (Legacy 20-step flow) | 20 |

## Final Output Format

**Best Entry Point Analysis** (full reasoning chain) + **Product Spec Summary**.

The Product Spec Summary MUST disclose any skipped Optional steps and offer a one-command path to add them back (per `rules-optional-trigger.md` Section 6).

After completion, follow `references/rules-end-of-flow.md` for end-of-flow rules.
