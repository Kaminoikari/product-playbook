# Stage 2: Define — Converging on the Problem

> **Note: Which steps to execute per mode is authoritatively defined by the "Mode Step Sequences" in SKILL.md. The following is for reference only.**

**Full mode / high completeness → Do all (2.1 ~ 2.4)**
**Medium completeness → 2.1 + 2.3 + 2.4**
**Quick mode / low completeness → Only 2.3 (one core HMW)**

Before entering this stage, confirm the three core product questions: Who is it for? / Why build it? / What is it?

## 2.1 Pain Point Summary Table

Extract pain points from all Personas and User Journey Maps:

```
| # | Pain Point Description | Source Persona | Appears in Stage | Impact Level (High/Med/Low) | Frequency (High/Med/Low) |
|---|---|---|---|---|---|
| P1 | | | | | |
| P2 | | | | | |
```

## 2.2 April Dunford's Positioning Framework

**Applicable: Medium/high completeness / audience is executives/sales/marketing**

Positioning is not a tagline — it's deciding where you compete and for whom:

```
| Positioning Element | Question | Your Answer |
|---------------------|----------|-------------|
| Competitive Alternatives | If your product didn't exist, what would users use? (The real answer, not who you think your competitors are) | |
| Unique Attributes | What do you have that competitive alternatives don't? | |
| Value for Users | What tangible value do these unique attributes deliver to users? | |
| Target Market Characteristics | Which users care most about this value? (The more specific, the better) | |
| Market Category | What market frame best positions your product? (The frame determines the competitive criteria) | |
```

Most common positioning mistakes:
- Treating features as positioning ("We have AI!" is not positioning)
- Positioning too broadly — covering everyone means covering no one
- Using your perceived competitors as the reference rather than the user's actual alternatives

### 📝 Positioning Quality Checklist
- ✅ Are "competitive alternatives" from the user's perspective? (What users actually use instead, not who you think your competitors are)
- ✅ Are "unique attributes" things competitive alternatives can't do or can't do well? (Not things you both have)
- ✅ Is "value for users" stated in user language or product language? ("Saves 2 hours" vs. "AI-powered automation")
- ✅ Is the "target market" specific enough to actually find these people?
- ✅ Are all five positioning elements logically consistent?
- ❌ Common issues: Disconnect between unique attributes and value, wrong market category leading to being judged by wrong criteria

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

## 📎 File Integration Tips for This Stage

| Uploaded Content | Integrate Into | Integration Action |
|-----------------|----------------|-------------------|
| Competitor screenshots / competitive analysis reports | 2.2 Positioning | Fill in "competitive alternatives" and "unique attributes" fields; compare differentiation |
| Market reports (PDF) | 2.4 Opportunity Assessment | Use market data to validate Persona size and business value scores |
| NPS / satisfaction survey data | 2.1 Pain Point Summary | Replace assumed impact levels and frequencies with actual scores |
| Customer support / ticket summaries | 2.1 Pain Point Summary + 2.3 HMW | Count pain point frequency; convert high-frequency tickets directly into HMW questions |
