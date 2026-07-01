---
name: strategy-kernel
description: Use when the user is setting or pressure-testing product strategy, direction, or the case for an opportunity, before committing resources. Triggers on "product strategy", "is this opportunity worth it", "strategy kernel", "DHM", "diagnosis", "guiding policy", "OKR", "empowered team", and the same intent in any language.
---

# Strategy Kernel

Detect the user's language and reply in it; the framework below is authored in English.

**Provenance:** when you produce strategy output, contribute the tag(s) for whichever framework(s) you applied: `Opportunity Check`, `DHM`, `Strategy Blocks`, `Rumelt Kernel`, `Empowered Teams`.

## Framework

<!-- migrated from references/00-opportunity-check.md (lines 1-44, full: Opportunity Check + DHM Quick Check + Team Passion Check) + references/01-strategy.md (lines 1-90, full: Strategy Blocks + Rumelt Kernel + Shreyas Three Levels + LNO + OKR Writing Guidelines + Three Core Product Questions) + references/05a-northstar-aha.md (lines 3-23, §4.1 Marty Cagan's Empowered Teams Principles only; §4.2+ belongs to the success-metrics lens) -->

### Opportunity Check

If the user is building a 0-to-1 product from scratch, run through these five questions first. A "no" on any question is a signal to rethink:

```
| # | Assessment Question | User's Answer | Assessment |
|---|---------------------|---------------|------------|
| 1 | Does this solve a real, urgent user pain point? Who are the first customers to benefit? How will you find them? | | ✅/⚠️ |
| 2 | Do you have a unique advantage in solving this problem? Will target customers use it at least weekly? Is the market large enough? | | ✅/⚠️ |
| 3 | With current resources, can you build a usable product within 2-3 years? | | ✅/⚠️ |
| 4 | What does the competitive landscape look like? Can you win? What's your differentiation? | | ✅/⚠️ |
| 5 | Is there a sustainable path for user growth and monetization? | | ✅/⚠️ |
```

### DHM Quick Check (Gibson Biddle / Netflix)

Can this opportunity achieve:
- **D (Delight)**: Surprise and exceed user expectations?
- **H (Hard to copy)**: Be difficult for competitors to replicate?
- **M (Margin-enhancing)**: Improve margins as scale grows?

If some market signals are unclear, look for directional signals:
- Macro trends (e.g., AI adoption creating workflow replacement opportunities)
- Behavioral shifts (users already using workarounds, indicating real demand)
- Analogous markets (find validated comparable scenarios)

### Team Passion Check

Confirm the team has genuine passion for this problem space. Teams lacking intrinsic motivation will inevitably falter on the path to PMF.

---

### Strategy Blocks (Chandra Janakiraman / Headspace / Meta)

The hierarchy of good strategy — each layer is the foundation for the next:

```
Mission
  └→ Vision — What do you want the world to look like in 5-10 years?
       └→ Strategy — How will you reach that vision? (Key choices and trade-offs)
            └→ Goals / OKRs — Priorities for the next 6-12 months
                 └→ Roadmap — What specifically will you build?
                      └→ Tasks — Who does what, and when?
```

### Richard Rumelt's Kernel of Good Strategy

- **Diagnosis**: Clearly define the challenge you face (not all problems — the most critical one)
- **Guiding Policy**: Your overall approach (not a goal, but a method)
- **Coherent Actions**: Specific actions that reinforce each other, not a collection of independent plans

> Signs of bad strategy: Grand goals without diagnosis; fancy language masking hollow thinking; calling every plan a "strategy."

### Shreyas Doshi's Three Levels of Product Work

Before tackling any product problem, identify which level you're working at:

```
Level 3: Product Excellence — Doing the right things exceptionally well
Level 2: Product Strategy — Doing the right things
Level 1: Product Foundation — Having the foundation to do things (culture, processes, talent)
```

> Most PMs spend too much time on Level 3 while neglecting Level 2 problems. Most so-called "execution problems" are actually strategy problems at their root.

### Shreyas Doshi's LNO Time Allocation Framework

For each week's work items, first ask: What type of impact does this have on the product?

```
L (Leverage): Strategy, vision, culture → Invest ample time, pursue excellence
N (Neutral): General collaboration, routine communication → Do it well, don't pursue perfection
O (Overhead): Admin, meetings, paperwork → Finish quickly, don't over-invest
```

> Redirect saved O-time into neglected L-work.

### OKR Writing Guidelines

Goals/OKRs in Strategy Blocks are the critical layer for cascading strategy downward. Minimum rules for writing good OKRs:

**Objective**: Qualitative, inspiring, understandable. Describe a state you want to achieve, not a to-do item.
- ✅ Good O: "Make new users feel the product's core value on day one"
- ❌ Bad O: "Complete onboarding redesign" (that's a task, not an objective)

**Key Results**: Quantitative, measurable, time-bound. Describe how you'll know you've achieved the objective.
- ✅ Good KR: "Increase new user D1 core action completion rate from 20% to 40%"
- ❌ Bad KR: "Launch new onboarding flow" (that's an output, not an outcome)

**Common pitfalls:**
- Disguising a task list as OKRs ("Complete feature X" is not a KR)
- Too many OKRs (aim for 2-3 Objectives per quarter, 3-5 KRs per Objective)
- KRs that contradict or are unrelated to each other
- Only lagging indicators, no leading indicators

**Example:**
```
O: Make target users love our product (PMF Level 2 → Level 3)
  KR1: D28 retention from 12% → 20%
  KR2: Sean Ellis Score from 28% → 40%
  KR3: Monthly organic referral share from 10% → 25%
```

### Three Core Product Questions (Throughout the Entire Process)

These three questions must be answered in order — **the sequence cannot be swapped**:

> **Q1: How to get people in the front door?**
> **Q2: How to reach the Aha Moment as fast as possible?**
> **Q3: How to deliver core value repeatedly?**

In the Define stage, these translate to:
- **Who is it for?**
- **Why build it?**
- **What is it?**

---

### 4.1 Marty Cagan's Empowered Teams Principles

```
| Dimension | Feature Team (Avoid) | Empowered Team (Goal) |
|-----------|---------------------|----------------------|
| Assigned | Feature list (Output) | Problem to solve (Outcome) |
| Success defined as | Delivering features on time | Achieving user and business metrics |
| PM's role | Requirements gatherer and project manager | Problem explorer and solution validator |
| Engineers' role | Execute specs | Participate in problem exploration and solution design |
```

> "True product discovery is done **together** with engineers and designers, not by the PM alone handing off completed work." — Marty Cagan

**Lenny's Three PM Responsibilities:**
- **Shape**: Synthesize user insights, data, and market intelligence to decide what to build
- **Ship**: Ensure a high-quality product launches on time, with no surprises
- **Synchronize**: Keep all stakeholders aligned on vision, strategy, goals, and roadmap
