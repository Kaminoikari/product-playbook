# Phase 1: Discovery — JTBD Analysis

## 1.3 JTBD (Jobs to Be Done) Analysis

> "The unit of analysis is not the consumer, but the job the consumer is trying to get done." — Clayton Christensen

**JTBD Three-Layer Coverage (Hard Gate — all three layers required):**

Every JTBD analysis MUST surface **all three layers explicitly**: **Functional** (the task being completed), **Emotional** (how the user wants to feel during/after), and **Social** (how the user wants to be perceived). Producing only the Functional layer is the most common JTBD failure — Emotional and Social Jobs are routinely the real switching triggers, especially in B2B. If a single Persona genuinely has no meaningful Emotional or Social Job for the product, state that explicitly with one sentence of reasoning rather than silently omitting the row.

**JTBD Canonical Form (Hard Gate — three-clause structure required):**

Every JTBD statement (Primary, Functional, Emotional, Social — every layer) MUST be written as a complete three-clause sentence in the canonical form. All three clauses are required:

```
When [situation], I want to [motivation], so [outcome].
```

**Failing examples** (fragments inside a table cell, missing clauses):
- ❌ "Quickly capture key takeaways" (missing When; missing so)
- ❌ "Jot down ideas during commute" (missing I want to; missing so outcome)

**Passing example** (all three clauses present):
- ✅ "**When** I've just finished reading an article and the key insight is still fresh, **I want to** capture one takeaway in 5 seconds, **so** weeks later I can still find it and connect it to a new idea."

Example: **When** comparing mortgage options late at night and can't reach a bank, a first-time homebuyer **wants to** quickly estimate monthly payments, **so** they can walk their partner through their financial plan.

**JTBD Four-Type Analysis Table:**

Every cell (Persona 1 / Persona 2) MUST contain a complete three-clause JTBD sentence. **Short phrases like "Feel like I'm still showing up for myself", "log workouts daily", "track progress easily" all FAIL the Hard Gate.** Use the worked example below as the literal shape — every cell must read like a sentence with `When …, I want to …, so …`.

Worked example (B2C fitness habit tracker, single Persona — replicate this shape for every cell):

| JTBD Type | Definition | Persona: Busy Professional |
|-----------|------------|-----------|
| Functional Job | Completing a specific task or achieving a functional goal | **When** I get home after a long workday and have 20 minutes before my next commitment, **I want to** log the workout I just did and see what's recommended next, **so** I can keep the streak going without spending mental energy planning. |
| Emotional Job | How they feel or want to feel | **When** I miss a planned workout two days in a row, **I want to** feel that I'm still on track rather than starting over, **so** I don't fall into the all-or-nothing spiral that kills my consistency. |
| Social Job | How they want to be perceived by others | **When** a friend asks how my training is going, **I want to** show a clean record of recent activity, **so** I'm seen as someone who follows through on commitments to themselves. |
| Job Context | Under what circumstances they need to get this job done | **When** my schedule is volatile across the week (early meetings, evening calls), **I want to** fit workouts into 15–45 minute windows wherever they land, **so** training adapts to my life instead of competing with it. |

Empty table (fill each cell with full `When …, I want to …, so …` sentences — do NOT shorten to phrases):

```
| JTBD Type | Definition | Persona 1 (must use "When … I want to … so …" full form) | Persona 2 (same) |
|-----------|------------|-----------|-----------|
| Functional Job | Completing a specific task or achieving a functional goal | | |
| Emotional Job | How they feel or want to feel | | |
| Social Job | How they want to be perceived by others | | |
| Job Context | Under what circumstances they need to get this job done | | |
```

**JTBD Deep-Dive Five Questions:**
1. **Root Problem**: Behind what users express as their need, what are they really trying to solve?
2. **Current Constraints**: What solutions have been ruled out due to certain limitations?
3. **Current Workarounds**: How are users coping today? What workarounds have they built?
4. **Gap**: Where do current workarounds fall short? (This gap is your opportunity)
5. **Ideal Solution**: If constraints were removed, what would their ideal solution look like?

**Teresa Torres User Interview Best Practices:**
- Focus on users' **actual past behavior**, not hypothetical future behavior
- Ask "Last time you ran into this problem, what did you do?" instead of "What features would you like?"
- Most common mistakes: asking hypothetical questions, introducing solution bias, not probing for details

### 📝 JTBD Quality Checklist

Claude must self-check after producing JTBD output (each item must be marked ✅ or ❌; ❌ items must include how to improve):
- [ ] Are **all three layers** (Functional / Emotional / Social) written in the full "When … I want to … so …" canonical form? (Any layer missing a clause → mark ❌)
- [ ] Does it include a specific context? (Not "anytime, anywhere" — but "late at night when they can't reach a bank")
- [ ] Does it focus on a single core job? (Not three jobs crammed into one sentence)
- [ ] Can it be used to evaluate "Does this solution actually address this job?"
- [ ] Does it include "current workarounds" and "gap"? (Gap = opportunity)
- [ ] Does Q5 of the Deep-Dive **explicitly use at least one canonical-vocabulary word** (`fear`, `anxiety`, `shame`, `worry`, `dread`, `self-doubt`, `sense of loss`, `threat to identity`, `embarrassment`, `guilt`)? Paraphrased consequences like "credibility at risk" or "reputation damaged" FAIL this item — they describe outcomes, not the felt emotion.

**Execution Rules (Hard Gate):**
- Must mark each item ✅ or ❌ — blank [ ] or unexplained ✅ lists are not allowed
- **The checklist MUST contain at least one ❌** (see `references/rules-quality-review.md` "Mandatory Critique" rule). A ⚠️ warning marker cannot replace ❌; a "weakest aspect" note appended outside the checklist cannot replace a ❌ inside it. If after honest review every item still feels like a pass, lower the bar and find the item most worth marking ❌, then specify how to strengthen it.
- ❌ Common issues: incomplete three-clause form (missing When / I want to / so), too abstract, too many jobs merged, missing context, substituting product features for job descriptions, Q5 staying at the functional level

---

### 🏢 B2B Product Deep-Dive Requirements (Hard Gate)

**Hard Gate — for any B2B (or B2B2C) product, the following three sub-analyses are all REQUIRED. Skipping any of them is a contract failure regardless of whether the user explicitly asked.** If the product type is ambiguous, ask one clarification question; do not silently default to B2C.

#### Organizational-Level Job Analysis (Hard Gate — cover at least 2 levels)

A B2B JTBD analysis that stays purely at the individual-user level FAILS this gate. Organizational-level Jobs (compliance auditing, cross-department approval workflows, cost control, headcount-policy alignment, audit-trail integrity) are needs that exist beyond any single user's daily task and routinely dominate B2B switching decisions. The table below MUST be produced and at least 2 of the 3 levels MUST contain non-empty B2B-specific Jobs (not generic productivity statements).

| Level | Description | Examples |
|-------|-------------|----------|
| **Strategic Job** | Cross-departmental needs at the org/management level | Compliance audits, cost control, workforce optimization |
| **Operational Job** | Coordination needs at the process/department manager level | Approval workflow management, cross-team information sync |
| **Task Job** | Day-to-day operational needs of individual users | Filling out forms, checking status, exporting reports |

#### Buyer vs. User Analysis (Hard Gate)

For B2B products, the buyer (signs the contract, controls budget) and the daily user (touches the product every day) are almost always different roles with **different Jobs**. Treating them as one persona is the single most common B2B Discovery failure. Hard Gate rule:

- If buyer ≠ user (default assumption for B2B), produce **two separate Persona+JTBD blocks**: one for the Buyer (ROI justification, risk reduction, compliance, vendor-consolidation, audit-readiness) and one for the User (efficiency, error reduction, day-in-the-life context). Cross-link them: note where the buyer's Job depends on the user's Job (e.g., "buyer's compliance Job depends on user actually filing the report each cycle").
- If buyer = user (exceptional, e.g., founder-led tools), state explicitly in one sentence WHY the decision-maker is also the daily user in this specific scenario — do not assume.
- Failing example: producing only one persona ("HR Manager") that conflates both budgeting authority and daily form-filling. That collapses two distinct Jobs into one fuzzy persona and the analysis cannot drive product decisions.

#### Deep-Dive Five Questions — B2B Enhanced Version (Hard Gate)

**Hard Gate — Q5 MUST explicitly use at least one psychological/emotional vocabulary word from this canonical list**: `fear`, `anxiety`, `shame`, `worry`, `dread`, `self-doubt`, `sense of loss`, `threat to identity`, `embarrassment`, `guilt`. Paraphrased functional outcomes ("credibility at risk", "reputation damaged", "metric drops", "users churn", "loses trust", "career impact") FAIL this gate even when they describe genuine B2B stakes — they describe *consequences*, not the *felt emotion* the persona is moving away from.

A Q5 that scores the persona's deepest motivation in functional language fails the Discovery contract: the entire purpose of Q5 is to surface the felt fear/anxiety that drives switching, because functional outcomes alone can be solved with incrementally better tools, while felt fear/anxiety is what gets a B2B buyer to override organizational inertia and sign a new contract.

**Passing examples** (each contains an underlined canonical-vocabulary word):
- ✅ Professional identity: "She **fears** looking incompetent in front of leadership when this report represents her department's credibility"
- ✅ Emotional motivation: "He carries quiet **anxiety** that his direct reports will catch him not having a firm grasp of the numbers"
- ✅ Psychological fear: "Her biggest **dread** is the auditor catching a process gap — she was already warned once before, and the **shame** of a second incident would mark her file permanently"
- ✅ Identity threat: "He feels a **threat to identity** when external consultants out-explain him on his own team's metrics in front of the board"

**Failing examples** (functional / consequential, no canonical vocabulary):
- ❌ "He needs a better tool to improve efficiency" (functional)
- ❌ "Her credibility with leadership is at risk" (consequence, not felt emotion)
- ❌ "She might lose her job if this report is wrong" (outcome, not felt emotion — what does she *feel* about that possibility?)
- ❌ "His reputation in the organization would suffer" (consequence — replace with `embarrassment`, `shame`, or `dread`)

If the persona's deepest motivation genuinely doesn't map to any of the canonical-vocabulary words after honest analysis, mark the JTBD Quality Checklist Q5 item as `❌` with the explanation "Q5 currently lives at the consequence layer; need one more interview question that probes felt emotion" — do not paraphrase the vocabulary list to make a checkmark appear.

#### Competitive Alternatives Analysis (Required)

List the alternatives users are actually using today:
- At least 2 named existing tools (e.g., Slack / Excel / paper forms / email / verbal communication)
- For each tool, explain its "fundamental flaw": not that the features are weak, but "why this flaw has been accepted and left unsolved" (organizational inertia? switching costs? leadership doesn't care?)

### 📋 User Interview Plan Template

```
## User Interview Plan

**Research Goal**: Understand how [target Persona] deals with [specific problem] in [Job Context]
**Screening Criteria**:
  - Must have experienced [specific behavior] within the past [X days/weeks]
  - Exclude: [who is not a fit — e.g., internal employees, known power users]

**Core Questions (5–7)**:
1. Last time you ran into [problem], can you walk me through how you handled it? (Behavioral recall)
2. During that process, what was the most frustrating or time-consuming part? (Pain point identification)
3. Have you tried other approaches? Why or why not? (Current alternatives)
4. If that part could be better, what would "better" look like to you? (Ideal state)
5. How often does this happen? When was the last time? (Frequency and urgency)
6. Besides you, who else is affected by this problem? (Stakeholder mapping)
7. On a scale of 1–10, how severe is this problem for you? Why? (Quantifying the pain)

**Follow-up Strategies**:
  - When the interviewee says "Usually I..." → Ask "What specifically happened last time?"
  - When the interviewee mentions an emotion → Ask "Can you describe that feeling more specifically?"
  - When the interviewee mentions a tool/method → Ask "What made you choose that approach?"

**Documentation Format**:
  - Verbatim transcript or recording
  - Within 24 hours post-interview, tag: key quotes / pain points / surprising findings / contradictions to assumptions
```

---

## 📎 File Integration Notes for This Phase

If the user uploads files during this phase, Claude integrates them as follows:

| Uploaded Content | Integrate Into | Integration Action |
|-----------------|----------------|-------------------|
| User interview transcripts / recording text | 1.1 Persona + 1.3 JTBD | Extract: user background → Persona fields; pain points + current workarounds → JTBD Deep-Dive Five Questions; emotional reactions → Emotional / Social Jobs |
| Competitor app screenshots | 1.3 JTBD (current workarounds) | Identify as user's "current alternative," analyze workarounds and gaps |
