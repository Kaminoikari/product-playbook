---
name: solution-prioritization
description: Use when you have several solution options or features and need to decide what to do first, before scoping an MVP. Triggers on "prioritize", "RICE", "GEM", "impact vs effort", "which should we build first", "rank these", and the same intent in any language.
---

# Solution Prioritization

Detect the user's language and reply in it; the framework below is authored in English.

**Provenance:** when you produce prioritization output, contribute the framework tag `RICE` (and `GEM` when the GEM lens is applied) to the meta-skill's provenance line.

## Framework

<!-- migrated verbatim from references/04b-solutions.md §3.4 (GEM) + §3.5 (RICE) + Impact/Effort -->

### 3.4 Gibson Biddle's GEM Prioritization Model (Netflix)

```
| Feature | G (Growth) | E (Engagement) | M (Monetization) | Overall Priority |
|---------|-----------|----------------|------------------|-----------------|
| | | | | |
```

**Impact / Effort Matrix:**

```
| Feature / Solution | Impact (High/Med/Low) | Effort Required (High/Med/Low) | Quadrant |
|---|---|---|---|
| | | | Quick Win / Strategic / Fill-in / Avoid |
```

### 3.5 RICE Quantitative Prioritization

**Applicable: High completeness / audience is data scientists/executives**

```
RICE Score = (Reach × Impact × Confidence) / Effort

| Feature | Reach (users impacted/mo) | Impact (0.25/0.5/1/2/3) | Confidence (%) | Effort (person-months) | RICE Score |
|---------|--------------------------|------------------------|----------------|----------------------|------------|
| | | | | | |
```

**Impact Scale Definitions:**
| Score | Level | Criteria |
|-------|-------|----------|
| 3 | Massive | Fundamentally changes the user experience; directly solves the core JTBD |
| 2 | High | Significantly improves user experience; clear positive impact on the North Star Metric |
| 1 | Medium | Noticeable improvement; helpful for some users or some scenarios |
| 0.5 | Low | Minor improvement; nice-to-have |
| 0.25 | Minimal | Barely noticeable difference; maintenance-level work |

**Confidence Judgment Reference:**
- 100%: Supported by quantitative data (A/B tests, user data)
- 80%: Supported by qualitative data (user interviews, competitive validation)
- 50%: Reasonable hypothesis but unvalidated
- 20%: Pure intuition or guesswork

> "Don't prioritize features — prioritize problems. Features are solutions, and they only matter after you've confirmed the priority of the problems." — Shreyas Doshi
