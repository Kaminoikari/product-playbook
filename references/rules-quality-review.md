# Quality Review Rules

> Loaded after each step.

## Protocol

After each step output:

1. Mark each checklist item with one of exactly two markers: ✅ (passes) or ❌ (fails). **Blank checkboxes, ⚠️, "partial", "could be improved", "needs work" are all FORBIDDEN substitutes.** If you want to flag a soft concern, the marker is still ❌ — the severity goes in the "Gap" text.

2. **≥1 ❌ required on a substantive content gap** (Hard Gate). The ❌ must be on:
   - A missing required element (e.g. JTBD missing emotional layer)
   - A weak/generic answer where a sharper one is needed (e.g. Persona pain point that's a category label not an observed behaviour)
   - A logical inconsistency between sub-parts of the output
   - NOT acceptable as ❌: formatting, wording polish, "could be more detailed", "minor typo". Cosmetic flags fail the Hard Gate.

3. Each ❌ MUST include all three of these in its line:
   - **Gap**: what specifically is missing or weak (quote the offending line if applicable)
   - **Impact on downstream artifact**: name a specific later step or artifact that this gap will break or weaken (e.g. "blocks PR-FAQ writing because the solution paragraph won't know which emotional pain to open on", "will produce a vague North Star metric because we don't yet know the core outcome the user values"). Vague "this needs improvement" fails.
   - **Fix direction**: concrete next action the user (not you) should take

4. Format exactly:
   ```
   📝 Quality Self-Check:
   - ✅ [checklist item]
   - ❌ [checklist item] → Gap: …  ·  Impact: blocks [downstream step]  ·  Fix: [concrete action]
   ```

**Self-check on self-check**: scan your own output before sending. If zero ❌ → lower the bar and re-review. If ❌ exists but has no "Impact: blocks/weakens [specific downstream artifact]" clause → rewrite that line. Every artifact has a weakest dimension; a checklist of all ✅ is a sign the reviewer is the wrong person, not that the artifact is perfect.

---

## Checklists per framework

**Persona**: 1) by purpose/motivation not demographics, 2) MECE, 3) core vs secondary TA clear, 4) pain points from real obs/inference, 5) "current approach + rationale" specific enough to identify workarounds.

**JTBD**: 1) specific context (not "anytime"), 2) single core job, 3) functional + emotional + social all present, 4) usable to evaluate solutions, 5) "current approach + gap" stated, 6) **five-why Q5 uses explicit emotional vocabulary** — at least one of: *fear, anxiety, shame, worry, dread, self-doubt, sense of loss, threat to identity, embarrassment, guilt*. Functional consequences ("HR credibility suffers", "users churn", "metric drops") FAIL this item — they describe outcomes, not the felt emotion. ✅ example: "HR fears being held personally accountable in an audit"; ❌ example: "HR's credibility with leadership is at risk".

**Positioning (April Dunford)**: 1) competitive alternative from user perspective, 2) unique attribute competitors can't match, 3) value in user language not product language, 4) target market specific enough to find them, 5) 5 elements logically consistent.

**HMW**: 1) clear constraints, 2) solution space wide, 3) maps to JTBD/pain, 4) team can start ideating.

**PR-FAQ**: 1) headline user-perspective ("Users can now X"), 2) first paragraph delivers "why this matters" in 10s, 3) pain from real scenario, 4) solution opens with user feeling, 5) quote sounds human, 6) FAQ has sharp questions vs existing tools.

**North Star**: 1) reflects user value (not revenue/DAU), 2) can grow continuously, 3) team knows what to do on seeing it, 4) guardrails if gameable, 5) B2B: organisation-level value.

**Aha Moment**: 1) specific trackable behaviour, 2) tied to JTBD functional job, 3) target time reasonable (B2C: first use; B2B: trial period), 4) onboarding designable to accelerate.

**Security** (full: `08-security-checklist.md`): 1) auth explicitly chosen, 2) ≥3 security headers planned, 3) rate limit tailored not template, 4) `.gitignore` covers all sensitive files.

**Document Export** (full: `rules-export-document.md`): 1) no residual Markdown syntax in HTML, 2) table rows/columns match original.

---

## Cross-Step Consistency (at flow end only)

Detailed: `rules-end-of-flow.md`.

| # | Dimension | Question |
|---|-----------|----------|
| 1 | Target user | JTBD, Positioning, PR-FAQ point to same people? |
| 2 | Core problem | PR-FAQ addresses JTBD problem? MVP solves it? |
| 3 | Solution ↔ Scope | Selected solution consistent with MVP scope? |
| 4 | Metric ↔ Value | North Star measures JTBD outcomes? |
| 5 | Risk timeliness | Pre-mortem risks still relevant to final solution? |
