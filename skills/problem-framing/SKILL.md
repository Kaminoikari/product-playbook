---
name: problem-framing
description: Use when the user needs to sharpen a vague problem into pain points, reframed questions, and ranked opportunities before designing solutions. Triggers on "frame the problem", "pain points", "how might we", "HMW", "opportunity assessment", "what problem", and the same intent in any language.
---

# Problem Framing

Detect the user's language and reply in it; the framework below is authored in English.

**Provenance:** when you produce problem-framing output, contribute the framework tags `Pain Points`, `HMW`, and `Opportunity Assessment` to the meta-skill's provenance line (`— Frameworks: … · Pain Points · HMW · Opportunity Assessment · …`).

## Framework

<!-- migrated verbatim from references/03-define.md §2.1 (lines 11-20) -->

## 2.1 Pain Point Summary Table

Extract pain points from all Personas and User Journey Maps:

```
| # | Pain Point Description | Source Persona | Appears in Stage | Impact Level (High/Med/Low) | Frequency (High/Med/Low) |
|---|---|---|---|---|---|
| P1 | | | | | |
| P2 | | | | | |
```

<!-- migrated verbatim from references/03-define.md §2.3 (lines 51-77) -->

## 2.3 HMW (How Might We) Problem Reframing

Transform pain points into HMW questions, combining the JTBD lens to confirm the job type behind each HMW:

```
| Pain Point # | Pain Point | Corresponding JTBD Type | HMW Question |
|---|---|---|---|
| P1 | [Pain point description] | Functional / Emotional / Social | How might we... |
| P2 | [Pain point description] | | How might we... |
```

HMW granularity principle:
- Too broad ("How to make users happier") → No direction
- Just right ("How to let users complete first-time setup in 60 seconds") → Constrained yet open
- Too narrow ("How to change the button color") → Limits possibilities

### 📝 HMW Quality Checklist
- ✅ Does it have clear constraints? (Not completely open-ended)
- ✅ Does it leave enough room for multiple solutions? (Not pointing to a single answer)
- ✅ Can it be directly mapped to a JTBD or pain point?
- ✅ Can the team start brainstorming solutions upon seeing this HMW?
- ❌ Common issues: Too broad (restates the vision), too narrow (specifies the solution), multiple problems mixed together

**Examples:**
- ❌ Too broad: "How might we make users more satisfied?"
- ✅ Just right: "How might we help first-time homebuyers calculate their affordable mortgage amount in 3 minutes?"
- ❌ Too narrow: "How might we add a mortgage calculator to the homepage?"

<!-- migrated verbatim from references/03-define.md §2.4 (lines 79-107) -->

## 2.4 Opportunity Assessment Table

Prioritize HMW questions:

```
| HMW Question | Affected Persona | Persona Size | User Impact (1-5) | Business Value (1-5) | Feasibility (1-5) | Total | Priority |
|---|---|---|---|---|---|---|---|
| | [List affected Personas] | [Large/Med/Small] | | | | | |
```

**Scoring Scale Definitions:**

| Score | User Impact | Business Value | Feasibility |
|-------|-----------|---------------|-------------|
| 1 | Minor inconvenience for few users | Indirect, long-term payoff at best | Requires entirely new technology or extensive R&D |
| 2 | Some users encounter occasionally | May indirectly move some metrics | Requires significant new capability building (3+ months) |
| 3 | Core TA encounters regularly | Positive impact on key metrics | Requires some new development but technically feasible (1-3 months) |
| 4 | Many users encounter frequently | Directly drives user growth or retention | Within current team capabilities, 2-4 weeks |
| 5 | Many users can't complete core tasks daily | Directly drives revenue or significantly impacts North Star Metric | Current team can complete within two weeks |

**Shreyas Doshi's Opportunity Cost Thinking:**

Don't ask "What's the ROI of this feature?" Instead, ask:

> "If I invest resources in A, I'm giving up the opportunity to invest in B. Am I sure A is more worthwhile than B?"

ROI thinking evaluates whether a single opportunity is worth pursuing; opportunity cost thinking helps you make better choices across all opportunities.

**0-to-1 Focus Reminder:** After completing the opportunity assessment, it's recommended to pick **only one top-priority HMW question** as the MVP core. (Facebook: college students → high schoolers → everyone; profile page → photos → news feed)

---
