# Stage 1: Discovery — Building Personas

### 🚫 Discovery Output Scope (Hard Gate)

When the orchestrator is asked to perform Discovery work (Persona, JTBD, OST, Journey Map, Continuous Discovery), the output MUST stay **inside the Discovery scope**. Discovery answers _who the users are_ and _what unmet need they are trying to satisfy_ — nothing else. The following downstream artifacts must NOT appear in a Discovery deliverable, even if they feel natural to mention:

- **Define-stage artifacts**: positioning statements, HMW (How Might We) questions, named pain-point matrices that double as solution prompts
- **Develop-stage artifacts**: PR-FAQ drafts, pre-mortem scenarios, RICE tables, MVP scope definitions, PRD sections, feature lists
- **Deliver-stage artifacts**: North Star metric definitions, PMF criteria, GTM plans, business-model canvas blocks, product-spec tables
- **Strategy-stage artifacts**: Strategy Blocks, Rumelt diagnosis/guiding-policy/coherent-action, DHM Model breakdowns, OKR ladders

If the Discovery findings strongly suggest a downstream artifact (e.g., the JTBD analysis surfaces a clear positioning angle), note it as a one-line *open question* or *next-step pointer* at the very end — never produce the artifact itself. The next stage in the planning flow has its own dedicated step for it.

Failing example: ending a JTBD analysis with a populated RICE table, an MVP scope list, or a "Recommended Positioning" paragraph. That output FAILS this Hard Gate even if all the other Discovery sub-sections are correct.

---

## Continuous Discovery Habits (Teresa Torres)

Build one key habit: **Talk to at least one target user every week.** Discovery is not a one-time ritual — it's an ongoing system.

> "Product discovery should be a continuous habit, not a one-time ceremony before a project starts." — Teresa Torres

## 1.1 Build the Persona Table

Personas are not segmented by age and gender, but by **purpose / task / motivation** to distinguish different types of users.

### 🏢 B2B Hard Gate — Buyer Persona ≠ User Persona

For any B2B (or B2B2C) product, the **buyer** (signs the contract, controls budget, owns vendor risk) and the **daily user** (touches the product every day) are almost always different roles with **different goals, pain points, and decision criteria**. Treating them as one persona conflates two distinct Jobs and produces analysis that cannot drive product decisions.

Hard Gate rule:
- Produce **two separate Persona blocks** labeled `Buyer` and `User` whenever the product is B2B and the two roles are distinct (the default assumption).
- If they are the same person (rare — usually founder-led tools or sole-proprietor B2B), state explicitly in one sentence WHY the buyer is also the daily user in this specific scenario.
- Cross-link the two personas: note where the Buyer's evaluation criteria depend on what the User actually does daily (e.g., "Buyer's audit-readiness criterion depends on User completing the leave-request form on the same day rather than batching them").

Failing example: producing only one persona ("HR Manager") that conflates approving budget AND filing daily leave forms — two different Jobs forced into one fuzzy archetype. That output FAILS this Hard Gate.

```
| Field | Persona 1: [Nickname] | Persona 2: [Nickname] | Persona 3: [Nickname] |
|---|---|---|---|
| Purpose / Task / Motivation | | | |
| Size (SCALE) | | | |
| Problems / Challenges / Drivers | | | |
| Current Approach & Rationale | | | |
| Frequency | | | |
| Information Sources | | | |
| Adoption / Execution Barriers | | | |
```

Explain the segmentation logic; check for MECE (mutually exclusive, collectively exhaustive); identify the primary TA and secondary TA.

### 🎯 Persona Prioritization Reasoning (Hard Gate)

Identifying "primary TA" without explicit reasoning fails this gate. The prioritization statement MUST name one Persona as primary AND explain why **in terms specific to the product's go-to-market dynamics**, not generic frequency-of-use claims.

For **B2B products with multiple user personas**, the reasoning MUST reference **at least one** of these B2B-specific dynamics by name (using these or clearly equivalent terms):

- **Champion vs Buyer** — who internally advocates for adoption versus who signs the contract; champion-led adoption usually wins B2B prioritization even when buyer is the "more senior" persona
- **Adoption multiplier** — who, by adopting, unlocks adoption for the rest of the org (e.g., HR Specialist's daily use seeds the system-of-record other personas later depend on)
- **Switching-trigger ownership** — which persona feels the pain that justifies switching from the incumbent tool; whoever owns the switching trigger is the prioritization candidate even if they aren't the heaviest user
- **Budget authority** — who controls the line item; relevant when buyer ≠ user and the buyer's evaluation criteria dominate the initial-deal decision
- **Audit / compliance pressure ownership** — whose role is on the line when audit findings hit; compliance-pressured personas often dominate prioritization in regulated B2B segments

A pure "Persona X uses it more often" or "Persona Y has more users" reasoning FAILS this Hard Gate for B2B products. Frequency is necessary, never sufficient — B2B switching is driven by org-level pressure, not individual usage rates.

For **B2C products**, the reasoning MUST reference at least one of: switching-trigger ownership, JTBD severity differential, network-effect seeding, or willingness-to-pay differential. Pure frequency-of-use reasoning also fails for B2C.

### 📝 Persona Quality Checklist
- ✅ Is the segmentation based on "purpose/task/motivation" rather than demographics?
- ✅ Are Personas MECE (mutually exclusive and collectively exhaustive of the target market)?
- ✅ Is the primary TA vs. secondary TA clearly identified?
- ✅ Are each Persona's "problems/challenges" based on real observations or reasonable inferences?
- ✅ Is "current approach & rationale" specific enough to identify workarounds?
- ❌ Common issues: Segmenting by age/gender, minimal differences between Personas, pain points too vague

## 1.2 Build Persona Cards

```
## [Persona Nickname]: [One-line description]

**Basic Info**: Age / Gender / Occupation / Location / Personality traits
**Background**: [Product-relevant background description]
**Goals / Tasks**: [Goal 1], [Goal 2]
**Current Approach & Rationale**: [What they currently do and why]
**Information Sources**: [Where they get relevant information]
**Barriers / Problems / Challenges / Frustrations**: [Pain point 1], [Pain point 2], [Pain point 3]
```

---

## 📎 File Integration Tips for This Stage

If the user uploads files during this stage, Claude integrates according to these rules:

| Uploaded Content | Integrate Into | Integration Action |
|-----------------|----------------|-------------------|
| User interview transcripts / audio transcriptions | 1.1 Persona + 1.3 JTBD | Extract: user background → Persona fields; pain points + current approach → JTBD deep-dive questions; emotional reactions → emotional/social Jobs |
| User research report (PDF) | 1.1 + 1.2 + 1.3 | Extract quantitative data (user segment proportions) into Persona size; extract qualitative insights into JTBD |
