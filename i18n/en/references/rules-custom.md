# ✏️ Custom Mode Step Sequence

> Authoritative step definition for Custom Mode. Dispatched from SKILL.md.

Choose a completeness level (or hand-pick steps):

## 🔴 Lean — 4 steps

```
S1. JTBD Statement → references/02b-jtbd.md
S2. One HMW → references/03-define.md
S3. PR-FAQ → references/04a-prfaq.md
S4. North Star → references/05a-northstar-aha.md
(Any step can be swapped by the user for a different framework.)
────
Final output → Product Spec Summary (unexecuted fields marked "not run")
```

## 🟡 Standard — 8 steps (auto-expands to 9 when Journey Map is needed)

> An 8-step subset of Full Mode: Full Core minus Strategy Diagnosis, plus Positioning. Standard users typically need market positioning earlier than deep strategy diagnosis, hence the swap.
>
> **Persona-Journey Conditional Insert**: After completing S1 (Persona), the AI runs the Persona-Journey evaluation per `rules-optional-trigger.md` Section 2. If skip conditions do NOT hold (i.e., the Job spans multiple stages), AI **proactively inserts Journey Map as S1.5**, making this a 9-step run. User can reply `-journey` to revert to 8 steps. If skip conditions hold (single interaction point / flow ≤2 steps), silently skip and disclose at final output.

```
S1.   Persona (Table + Cards) → references/02a-persona.md
S1.5  User Journey Map [Inserted by default; skip only when situation is too simple]
      → references/02c-ost-journey.md
S2.   JTBD Analysis → references/02b-jtbd.md
S3.   Pain Points + HMW + Opportunity Ranking → references/03-define.md
S4.   April Dunford Positioning → references/03-define.md
S5.   PR-FAQ → references/04a-prfaq.md
S6.   Solution Evaluation (Parallel + Pre-mortem + GEM + RICE) → references/04b-solutions.md
S7.   MVP + Not Doing List → references/04c-mvp.md
S8.   North Star + Three-Layer Signals + Aha Moment → references/05a-northstar-aha.md
```

## 🟢 Comprehensive — 11 steps

> Full Mode Core + all Default-OFF Optionals triggered (Positioning + PMF/GTM/BM/Validation). **S2 Persona is immediately followed by S3 User Journey Map** per the Persona-Journey bundling rule. S3 may be skipped if the situation is genuinely simple — reply `-S3` after Persona to revert to 10 steps.

```
S1.  Strategy Diagnosis → references/00-opportunity-check.md + references/01-strategy.md
S2.  Persona (Table + Cards) → references/02a-persona.md
S3.  User Journey Map → references/02c-ost-journey.md   ← bundled with S2 (default ON)
S4.  JTBD Analysis → references/02b-jtbd.md
S5.  Pain Points + HMW + Opportunity Ranking → references/03-define.md
S6.  April Dunford Positioning → references/03-define.md
S7.  PR-FAQ → references/04a-prfaq.md
S8.  Solution Evaluation (Parallel + Pre-mortem + GEM + RICE) → references/04b-solutions.md
S9.  MVP + Not Doing List → references/04c-mvp.md
S10. North Star + Three-Layer Signals + Aha Moment → references/05a-northstar-aha.md
S11. PMF + GTM + BM + Hypothesis Validation Plan → references/05b-pmf-gtm.md + references/05c-validation-spec.md
```

## Reference Loading Rule

Load each reference file ONLY when entering its corresponding step (do not pre-load all references). Each step has its reference path annotated above.

## Persona-Journey Bundling

Per `references/rules-optional-trigger.md` Sections 2 and 6, whenever a Custom preset includes a Persona step, Journey Map is **default ON**:

- **Comprehensive**: Journey Map is hard-coded as S3 (already in the sequence above). User may reply `-S3` after Persona to skip.
- **Standard**: Journey Map is auto-inserted as **S1.5** when skip conditions don't hold (multi-stage Job). When the situation is too simple (single interaction point, flow ≤2 steps, user requests skip), Journey Map is silently skipped and disclosed at final output.
- **Lean**: No Persona step, so this rule does not apply.

Skip conditions (any one holds → skip Journey):
1. Single interaction point (API, single button, backend service, config tool)
2. Flow has only 1–2 steps
3. User explicitly requests skip

## Final Output Format

**Product Spec Summary** (only integrates completed steps; unexecuted fields marked "not run").

After completion, follow `references/rules-end-of-flow.md` for end-of-flow rules.
