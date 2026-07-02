---
name: persona-journey
description: Use when the user needs to understand who the users are and how they move through an experience. Triggers on "persona", "target user", "buyer vs user", "user journey", "journey map", "touchpoints", and the same intent in any language.
---

# Persona & Journey

Detect the user's language and reply in it; the framework below is authored in English.

**Provenance:** when you produce persona or journey-map output, contribute the framework tags `Persona` and `Journey Map` to the meta-skill's provenance line (`— Frameworks: … · Persona · Journey Map · …`).

## Framework

<!-- migrated from references/02a-persona.md (full, lines 1-99; the File Integration Tips block dropped) and references/02c-ost-journey.md §1.5 User Journey Map (lines 27-54; the Applicable gating line and the shared File Integration Tips dropped); always-on gate / MUST / FAILS enforcement framing softened into proportional self-checks per the P1 soften pass -->

# Stage 1: Discovery — Building Personas

### 🚫 Discovery Output Scope

When the lens is applied to Discovery work (Persona, JTBD, OST, Journey Map, Continuous Discovery), check that the output stays inside the Discovery scope. Discovery answers _who the users are_ and _what unmet need they are trying to satisfy_, nothing else. The following downstream artifacts don't belong in a Discovery deliverable, even if they feel natural to mention:

- **Define-stage artifacts**: positioning statements, HMW (How Might We) questions, named pain-point matrices that double as solution prompts
- **Develop-stage artifacts**: PR-FAQ drafts, pre-mortem scenarios, RICE tables, MVP scope definitions, PRD sections, feature lists
- **Deliver-stage artifacts**: North Star metric definitions, PMF criteria, GTM plans, business-model canvas blocks, product-spec tables
- **Strategy-stage artifacts**: Strategy Blocks, Rumelt diagnosis/guiding-policy/coherent-action, DHM Model breakdowns, OKR ladders

If the Discovery findings strongly suggest a downstream artifact (e.g., the JTBD analysis surfaces a clear positioning angle), note it as a one-line *open question* or *next-step pointer* at the very end. Producing the artifact itself belongs to the next stage in the planning flow, which has its own dedicated step for it.

Self-check example: a JTBD analysis that ends with a populated RICE table, an MVP scope list, or a "Recommended Positioning" paragraph has drifted out of Discovery scope, even if the other sub-sections are solid.

---

## Continuous Discovery Habits (Teresa Torres)

Build one key habit: **Talk to at least one target user every week.** Discovery is an ongoing system; a one-time ritual won't sustain it.

> "Product discovery should be a continuous habit, not a one-time ceremony before a project starts." — Teresa Torres

## 1.1 Build the Persona Table

Personas are segmented by **purpose / task / motivation** to distinguish different types of users; age and gender don't define the segments.

### 🏢 B2B: Buyer Persona vs User Persona

For any B2B (or B2B2C) product, the **buyer** (signs the contract, controls budget, owns vendor risk) and the **daily user** (touches the product every day) are almost always different roles with **different goals, pain points, and decision criteria**. Treating them as one persona conflates two distinct Jobs and produces analysis that cannot drive product decisions.

Self-check:
- Produce **two separate Persona blocks** labeled `Buyer` and `User` whenever the product is B2B and the two roles are distinct (the default assumption).
- If they are the same person (rare, usually founder-led tools or sole-proprietor B2B), state explicitly in one sentence why the buyer is also the daily user in this specific scenario.
- Cross-link the two personas: note where the Buyer's evaluation criteria depend on what the User actually does daily (e.g., "Buyer's audit-readiness criterion depends on User completing the leave-request form the same day it's submitted").

Self-check example: a single persona ("HR Manager") that conflates approving budget and filing daily leave forms is forcing two different Jobs into one fuzzy archetype. Watch for this shape and split it before finalizing.

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

### 🎯 Persona Prioritization Reasoning

Naming a "primary TA" needs explicit reasoning behind it. A solid prioritization statement names one Persona as primary and explains why **in terms specific to the product's go-to-market dynamics**, beyond generic frequency-of-use claims.

For **B2B products with multiple user personas**, check that the reasoning references **at least one** of these B2B-specific dynamics by name (using these or clearly equivalent terms):

- **Champion vs Buyer** — who internally advocates for adoption versus who signs the contract; champion-led adoption usually wins B2B prioritization even when buyer is the "more senior" persona
- **Adoption multiplier** — who, by adopting, unlocks adoption for the rest of the org (e.g., HR Specialist's daily use seeds the system-of-record other personas later depend on)
- **Switching-trigger ownership** — which persona feels the pain that justifies switching from the incumbent tool; whoever owns the switching trigger is the prioritization candidate even if they aren't the heaviest user
- **Budget authority** — who controls the line item; relevant when buyer ≠ user and the buyer's evaluation criteria dominate the initial-deal decision
- **Audit / compliance pressure ownership** — whose role is on the line when audit findings hit; compliance-pressured personas often dominate prioritization in regulated B2B segments

A pure "Persona X uses it more often" or "Persona Y has more users" reasoning is a weak signal for B2B products: frequency matters, but B2B switching is driven mostly by org-level pressure; individual usage rates are a weak predictor.

For **B2C products**, check that the reasoning references at least one of: switching-trigger ownership, JTBD severity differential, network-effect seeding, or willingness-to-pay differential. Pure frequency-of-use reasoning is similarly weak for B2C.

### 📝 Persona Quality Checklist
- ✅ Is the segmentation based on "purpose/task/motivation"? (Demographics-only segmentation fails this check)
- ✅ Are Personas MECE (mutually exclusive and collectively exhaustive of the target market)?
- ✅ Is the primary TA vs. secondary TA clearly identified?
- ✅ Are each Persona's "problems/challenges" based on real observations or reasonable inferences?
- ✅ Is "current approach & rationale" specific enough to identify workarounds?
- Common issues to watch for: segmenting by age/gender, minimal differences between Personas, pain points too vague

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

## 1.5 User Journey Map

**Step 1: Overview Table**

```
**[Persona Name] — Task: [Task description]**

| Stage | Core Behavior | Emotion | Key Pain Point |
|---|---|---|---|
| [Stage 1] | [One-line description of primary behavior] | [Emotion + emoji] | [The most important pain point] |
```

**Step 2: Expand Each Stage in Detail**

```
> **Stage: [Stage Name]**
> - **Doing**: [What the user actually does at this stage]
> - **Thinking**: [What's going through the user's mind, ideally in first-person voice]
> - **Feeling**: [Emotional state and why]
> - **Stakeholder**: [Who is involved at this stage]
> - **Problem**: [Specific difficulties or frustrations]
```

**Step 3: Grouping**
- If stages are too granular, merge them into larger stage groups
- Consolidate pain points across stages, flag which are core pain points
