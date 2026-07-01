---
name: product-spec-summary
description: Use when the user needs to consolidate planning into a final spec with a risk register and blind-spot review. Triggers on "spec summary", "final spec", "risk register", "gaps and blind spots", "validation plan", "wrap up the plan", and the same intent in any language.
---

# Product Spec Summary

Detect the user's language and reply in it; the framework below is authored in English.

**Provenance:** when you produce Product Spec Summary output, contribute the framework tags `Spec Summary` and `Risk Register` to the meta-skill's provenance line (`— Frameworks: … · Spec Summary · Risk Register · …`).

## Framework

<!-- migrated from references/05c-validation-spec.md lines 1-117 -->

# Stage 4: Deliver — Hypothesis Validation + Product Spec Summary

## 4.5 Hypothesis Validation Plan

```
| Core Hypothesis | Validation Method | Validation Timing | Success Criteria | If hypothesis is wrong, we will... |
|----------------|-------------------|-------------------|-----------------|----------------------------------|
| | Alpha user interviews / data | | | |
```

Principles: Qualitative validation (user interviews, diary studies) + quantitative validation (data) carry equal weight; stay alert to your own confirmation bias.

## 4.6 Product Spec Summary

The Product Spec Summary is the final deliverable across all modes (Quick mode produces a one-page directional summary — different structure but same spirit).
The Product Spec Summary has three sections, corresponding to different reading depths:

### Section 1: Decision Summary (Readable in 30 seconds)

```
**Product One-liner**: [PR-FAQ headline]
**For Whom**: [Target Persona in one sentence]
**Core Value**: [JTBD functional job + emotional job, in one sentence]
**North Star Metric**: [Metric name + definition]
**Current PMF Level**: [Level 1-4 + one-sentence explanation]
```

### Section 2: Execution Boundaries (Readable in 2 minutes)

```
**Core JTBD Statement**: [Target Customer] + wants to [Job] + in the context of [Job Context]
**Aha Moment**: When the user completes [action], they experience the core value. Target: reach it within [X].
**MVP Must-Haves**: [3-5 most critical features/capabilities]
**Not Doing (Deliberately excluded from this version)**: [Explicit exclusions + reasons]
**Key Hypotheses**: [2-3 core hypotheses that need validation]
**Pre-mortem Top Risks**: [2-3 most likely causes of failure]
**Hero Metric**: [1-2 most important success metrics + target values]
```

### Section 3: Deep Reference (Consult when needed)

```
**JTBD Breakdown**:
  - Functional Job:
  - Emotional Job:
  - Social Job:
**April Dunford Positioning**:
  - Real competitive alternatives:
  - Our unique attributes:
  - Core value for target users:
  - Target market characteristics:
  - Market category:
**Core HMW Question**: [From the Define stage]
**Solution Description**: [From PR-FAQ summary]
**Business Model**: [Revenue model + pricing strategy, if completed]
**GTM Strategy**: [Initial acquisition channel + launch strategy, if completed]
```

By default, also add these three sections (Risk Register, Gaps & Blind Spots, Additional Recommendations):

---

### ⚠️ Risk Register

Consolidate all risks identified throughout the planning process (sources: Pre-mortem + Opportunity Assessment + Hypothesis Validation):

```
| Risk Type | Risk Description | Severity (High/Med/Low) | Mitigation in Place? |
|-----------|-----------------|------------------------|---------------------|
| Market risk | | | |
| User assumption risk | | | |
| Technical risk | | | |
| Competitive risk | | | |
| Execution risk | | | |
```

---

### 🔍 Gaps & Blind Spots

Claude proactively identifies the following types of gaps based on the entire conversation flow:

```
| Type | Description | Recommended Next Step |
|------|------------|----------------------|
| Unexecuted steps | [Which frameworks were skipped and what blind spots this may cause] | |
| Insufficient data | [Which decisions are based on assumptions rather than real user data] | |
| Logical leaps | [Where the reasoning lacks intermediate evidence] | |
| Unvalidated hypotheses | [List all core hypotheses without a validation method yet] | |
| Unclear definitions | [Which concepts need more precise definition before execution] | |
```

---

### 💡 Additional Recommendations

Claude provides 3-5 specific, actionable recommendations based on the product's characteristics, stage, and known risks:

```
1. [Top priority]: [Specific action] — Rationale: [Why this matters most]
2. [Second priority]: [Specific action] — Rationale:
3. [Third priority]: [Specific action] — Rationale:
...
```

Recommendations may cover: user validation methods, MVP boundary adjustments, competitive strategy, metric design, team allocation, next milestone priorities.
