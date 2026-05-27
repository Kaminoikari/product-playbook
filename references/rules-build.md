# ⚡ Build Mode Step Sequence (7 Steps + Final Output)

> This file is the authoritative step definition for Build Mode. Loaded by the SKILL.md core dispatcher.

> ⚠️ Required reminder: "Skipping the user research phase means your solution is built on assumptions. We recommend conducting Continuous Discovery as soon as possible after execution to validate."

## Step Sequence

```
S1. Confirm problem statement (one sentence)
S2. PR-FAQ → Read references/04a-prfaq.md
S3. Parallel solutions → Read references/04b-solutions.md → 3.2
S4. Pre-mortem → Read references/04b-solutions.md → 3.3
S5. GEM + RICE Prioritization → Read references/04b-solutions.md → 3.4 + 3.5
S6. MVP + Not Doing List → Read references/04c-mvp.md
S7. North Star + Aha Moment → Read references/05a-northstar-aha.md
────
Final Output → Engineer-oriented execution summary
```

## Reference Loading Instructions

| Step | Reference File |
|------|---------------|
| S1 | No external reference needed (directly guide the user to state the problem) |
| S2 | `references/04a-prfaq.md` |
| S3-S5 | `references/04b-solutions.md` |
| S6 | `references/04c-mvp.md` |
| S7 | `references/05a-northstar-aha.md` |

## Final Output Format

**Engineer-oriented execution summary**: Solution decisions → MVP boundary → Success metrics → Key risks

After completion, follow `references/rules-end-of-flow.md` to execute the end-of-flow rules.

---

## 🔧 Feature Extension Quick Path (4 Steps)

> Automatically switches to this path when the user is **adding a single feature to an existing product**.
> Trigger conditions: User description includes phrases like "add a feature," "new feature," "add XX functionality," "on the existing system," "existing product needs," etc.

**Differences from the full Build Mode (7 steps)**: An existing product already has a North Star, Aha Moment, and product positioning — no need to redefine them. A single feature does not require a PR-FAQ press release or full GEM+RICE re-prioritization. The focus is on "what to add, how to add it, and whether it will break existing functionality."

### Feature Extension Step Sequence

```
S1. Problem + existing system context
S2. Three parallel solutions + pros/cons + AI recommendation → Read references/04b-solutions.md → 3.2
S3. Risk assessment (regression + compatibility) → Read references/04b-solutions.md → 3.3
S4. Execution scope (what to do / what not to touch / acceptance criteria) → Read references/04c-mvp.md
────
Final Output → Feature development spec
```

### S1 Pre-step: Product Context Loading

Before entering S1, read `references/rules-context.md` and check `.product-context.md`:

- **Complete context available (Scenario 1)**: Automatically bring in product name, tech stack, key modules, and the 3 most recent Decision History entries. Change S1 guidance to **confirmation-style**: "Your product is [name], using [tech stack], with key modules including [module list]. What feature do you want to add? Which modules will be affected?" (Questions 2 and part of question 3 are pre-filled — just needs confirmation)
- **No context (Scenario 2)**: Trigger Context Bootstrap (`rules-context.md` Section 4), then proceed to the standard S1 below
- **Partial context (Scenario 3)**: Bring in known tech stack and modules (merged from Decision History), and collect the missing parts. For example: "Besides [known modules], are there other modules that might be affected?"

### S1 Guidance Content (Problem + Existing System Context)

Claude needs to collect the following information (guide step by step — do not ask all questions at once. If context has pre-filled some answers, confirm rather than re-collect):

```
1. What feature do you want to add? What problem does it solve?
2. Current product architecture overview (tech stack, key modules) ← context can pre-fill
3. Which existing modules will this feature affect? ← context can partially pre-fill
4. Is there any user feedback or data supporting this requirement?
```

### S2 Guidance Content (Three Parallel Solutions + AI Recommendation)

```
| HMW | Solution A (Conservative / minimal change) | Solution B (Balanced) | Solution C (Bold / refactor) |
|-----|-------------------------------------------|----------------------|----------------------------|
| [Problem] | | | |

| Solution | Pros | Cons | Impact Scope | Implementation Complexity |
|----------|------|------|-------------|--------------------------|
| A | | | | |
| B | | | | |
| C | | | | |

🤖 AI Recommendation: Solution [X]
Rationale: [Comprehensive judgment based on impact scope, complexity, and risk]
```

### S3 Guidance Content (Risk Assessment — Focused on Regression & Compatibility)

```
| Risk Type | Specific Risk | Likelihood | Mitigation |
|-----------|--------------|------------|------------|
| Regression risk | [Areas where existing features may be affected] | | |
| Compatibility risk | [Conflicts with existing architecture/data/APIs] | | |
| Performance risk | [Impact of the new feature on system performance] | | |
| Security risk | [Security considerations introduced by the new feature] | | |
```

### S4 Guidance Content (Execution Scope)

```
**What to do (Scope)**:
- [Specific feature items to add]
- [Existing modules that need modification]

**Do Not Touch**:
- [Modules and features explicitly not to modify]
- [Reason for not touching them]

**Acceptance Criteria**:
- [ ] [Specific testable condition]
- [ ] [Regression test: confirm existing features are unaffected]
```

### Feature Extension Final Output Format

**Feature development spec**: Problem statement → Selected solution + rationale → Impact scope → Execution scope + acceptance criteria → Risk list

### Incremental Document Output (when source document is available)

If the user uploaded a source document (PRD, spec, etc.) during the process:

1. **Incremental version** (default when source document exists):
   - Insert/modify sections in the original document structure
   - Maintain the original file's format, style, and naming conventions
   - New content marked with `[NEW]`
   - Modified content marked with `[UPDATED]` with original preserved as reference
   - Sections unrelated to the new feature remain completely untouched

2. **Standalone version** (when no source document):
   - Use the standard Feature development spec format (as defined above)

3. **Ask the user before generating**:
   "I detected that you uploaded a [document type]. How would you like the output?
    A) Incremental update on the original document (recommended)
    B) Standalone feature development spec"

### Reference Loading Instructions

| Step | Reference File |
|------|---------------|
| S1 | No external reference needed |
| S2 | `references/04b-solutions.md` → 3.2 |
| S3 | `references/04b-solutions.md` → 3.3 |
| S4 | `references/04c-mvp.md` |

After completion, follow `references/rules-end-of-flow.md` to execute the end-of-flow rules.
