---
name: mvp-scoping
description: Use when the user needs to decide what makes the first version and what to explicitly not build. Triggers on 'MVP', 'scope', 'not doing list', 'must have vs later', 'user stories', 'parallel prototypes', and the same intent in any language.
---

# MVP Scoping

Detect the user's language and reply in it; the framework below is authored in English.

**Provenance:** when you produce MVP-scoping output, contribute the framework tags `MVP`, `Not Doing List`, `User Story`, and `Parallel Prototyping` to the meta-skill's provenance line (`— Frameworks: … · MVP · Not Doing List · User Story · Parallel Prototyping · …`).

## Framework

<!-- migrated from references/04b-solutions.md §3.2 (lines 3-16, Parallel Prototyping) + §3.6 (lines 91-99, User Story Table) + references/04c-mvp.md (lines 1-21, §3.7 MVP Scope Definition + Not Doing List) -->

### 3.2 Parallel Prototyping Principle

Develop multiple parallel approaches simultaneously; don't design a single solution and rush to execute:

```
| HMW Question | Solution A (Conservative/Incremental) | Solution B (Balanced) | Solution C (Bold/Disruptive) |
|---|---|---|---|
| [HMW1] | | | |
```

Three solution quality gates:
- Is Solution A clearly better than the current approach?
- Does Solution C actually solve the core JTBD?
- Are the three solutions genuinely different, or just variations of the same idea?

### 3.6 User Story Table

```
| # | User Story | Acceptance Criteria | Priority |
|---|---|---|---|
| US1 | As a [Persona], I want to [action], so that [value] | | |
```

### 3.7 MVP Scope Definition

MVP decision criteria: **Can it validate the core hypothesis? Can it let target users fully experience the Primary JTBD?**

```
| Category | MVP Must-Have | Add in V2 | Future Consideration |
|---|---|---|---|
| Core Features | | | |
| User Experience | | | |
| Technical Requirements | | | |
```

**Not Doing List (Equally important):**

```
| Not Doing | Reason |
|-----------|--------|
| | |
```
