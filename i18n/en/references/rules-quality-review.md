# Quality Review Rules

> Loaded when each step is completed. This file separates the "review process" from the "review criteria," ensuring the quality self-check mechanism truly works.

## Review Process (Common to All Modes)

After producing the output for each step, Claude must execute the following review process:

### Step 1: Item-by-Item Self-Check

1. Find the quality checklist corresponding to the current step (see the "Review Criteria" section below)
2. Mark each item as ✅ or ❌
3. Items marked ❌ must include a specific explanation of "how to improve"

### Step 2: Mandatory Critique

- **Not all items may be ✅**: If all items pass, you must proactively identify "the weakest aspect of this output" and explain how to strengthen it
- This isn't nitpicking — it ensures that the self-review doesn't become a rubber stamp
- Following the Amazon PR-FAQ spirit: quality comes from finding problems, not from confirming there are none

### Step 3: Presentation Format

```
📝 Quality Self-Check:
- ✅ [Check item]
- ✅ [Check item]
- ❌ [Check item] → Improvement direction: [specific explanation]
⚠️ Weakest aspect: [description] → Strengthening suggestion: [specific action]
```

---

## Review Criteria (By Step)

> Below are the independent checklists for each framework output. The review process stays the same — just swap in the corresponding checklist.

### Persona

| # | Check Item |
|---|-----------|
| 1 | Is the segmentation based on "purpose/task/motivation" rather than demographics? |
| 2 | Are the Personas MECE (mutually exclusive and collectively exhaustive of the target market)? |
| 3 | Is the core TA vs. secondary TA clearly identified? |
| 4 | Are each Persona's "problems/challenges" derived from real observations or reasonable inferences? |
| 5 | Is "current approach and rationale" specific enough to identify workarounds? |

Common issues: Segmenting by age/gender, Personas that are too similar to each other, pain points that are too vague

### JTBD (Jobs to Be Done)

| # | Check Item |
|---|-----------|
| 1 | Does it include a specific context? (Not "anytime, anywhere" but "late at night when I can't contact the bank") |
| 2 | Does it focus on a single core job? (Not three jobs merged into one sentence) |
| 3 | Are functional, emotional, and social jobs all identified? |
| 4 | Can it be used to evaluate "does this solution solve this job"? |
| 5 | Does it include the "current approach" and the "gap"? (gap = opportunity) |
| 6 | Does the Q5 of the five-why deep dive touch on emotional motivation/professional identity/psychological fear? (Not a functional description) |

### Positioning

| # | Check Item |
|---|-----------|
| 1 | Is "competitive alternative" from the user's perspective? (What users actually use as a substitute, not what you think the competitor is) |
| 2 | Is the "unique attribute" something that competitive alternatives can't do or do poorly? |
| 3 | Is "value to the user" expressed in user language or product language? ("Save 2 hours" vs. "AI-driven automation") |
| 4 | Is "target market" specific enough that you could find these people? |
| 5 | Are the five positioning elements logically consistent with each other? |

Common issues: Disconnect between unique attribute and value, wrong market category leading to being judged by incorrect standards

### HMW (How Might We)

| # | Check Item |
|---|-----------|
| 1 | Does it have clear constraints? (Not completely open-ended) |
| 2 | Does it leave enough solution space? (Not pointing to a single solution) |
| 3 | Does it map directly to a JTBD or pain point? |
| 4 | Can the team start ideating solutions upon seeing this HMW? |

Common issues: Too broad (restating the vision), too narrow (specifying the solution), multiple problems mixed together

### PR-FAQ (Press Release + FAQ)

| # | Check Item |
|---|-----------|
| 1 | Is the headline written from the user's perspective? ("Users can now do X" vs. "We launched feature Y") |
| 2 | Can the reader understand "why this matters" within the first 10 seconds of the first paragraph? |
| 3 | Is the pain point description from a real user scenario? |
| 4 | Does the first sentence of the solution section start with user feeling/scenario (not a functional verb)? |
| 5 | Does the user quote sound like something a real person would say? |
| 6 | Does the FAQ include sharp questions comparing against existing tools? |

Common issues: Headline reads like a product announcement not news, solution section becomes a feature list, FAQ questions are all easy to answer

### North Star Metric

| # | Check Item |
|---|-----------|
| 1 | Does it reflect the value users receive? (Not revenue, not DAU) |
| 2 | Can it grow continuously? (Won't naturally hit a ceiling) |
| 3 | Does everyone on the team know what to do when they see this metric? |
| 4 | Can it be gamed? (If so, guardrail metrics are needed) |
| 5 | For B2B products: does it reflect value at the customer organization level, not just individual users? |

Common issues: Using revenue as North Star (revenue is a result, not a driver), metric is too composite to be actionable

### Aha Moment

| # | Check Item |
|---|-----------|
| 1 | Is it a specific, trackable behavior? (Not "feels like the product is useful") |
| 2 | Is it directly related to the functional job in JTBD? |
| 3 | Is the target time-to-reach reasonable? (B2C should be within first use; B2B may be within trial period) |
| 4 | Can onboarding be designed to guide users to reach it faster? |

### Security Check

> For detailed criteria, see `references/08-security-checklist.md`. Below is a quality self-check summary:

| # | Check Item |
|---|-----------|
| 1 | Authentication method has been explicitly selected, not left as "TBD" |
| 2 | At least 3 security headers have been planned |
| 3 | Rate limiting strategy has been tailored to the product's characteristics (not a copy-pasted template) |
| 4 | .gitignore includes all sensitive files |

### Document Export

> For detailed criteria, see `references/rules-export-document.md`.

| # | Check Item |
|---|-----------|
| 1 | No residual Markdown syntax in the HTML (`**`, `##`, `|---|`) |
| 2 | All table rows and columns match the original content |

---

## Cross-Step Consistency Review

> Loaded at the end of the flow. For detailed mode-specific check items, see `references/rules-end-of-flow.md`.

The cross-step consistency review is a second-layer review independent from single-step quality self-checks, executed after all steps are completed. Its purpose is to catch downstream inconsistencies caused by upstream modifications during iteration.

### Quick Check Items (Common to All Modes)

| # | Check Dimension | Verification Question |
|---|----------------|----------------------|
| 1 | Target user consistency | Do JTBD, Positioning, and PR-FAQ point to the same group of people? |
| 2 | Core problem consistency | Does the PR-FAQ address the problem stated in JTBD? Does the MVP solve it? |
| 3 | Solution ↔ Scope | Is the selected solution consistent with the MVP scope? |
| 4 | Metric ↔ Value | Does the North Star measure JTBD outcomes? |
| 5 | Risk timeliness | Are Pre-mortem risks still relevant to the final solution? |

---

## Design Principles

This file follows the Reviewer design pattern: **review criteria and review process are maintained separately**.

- **Process stays the same**: Step 1 (item-by-item self-check) → Step 2 (mandatory critique) → Step 3 (presentation format)
- **Criteria are swappable**: When adding new frameworks, just add the corresponding checklist under the "Review Criteria" section
- **Independent loading**: Each reference file retains its embedded checklist as an inline reminder; this file serves as the unified review entry point
