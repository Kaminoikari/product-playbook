# Stage 1: Discovery — Building Personas

## Continuous Discovery Habits (Teresa Torres)

Build one key habit: **Talk to at least one target user every week.** Discovery is not a one-time ritual — it's an ongoing system.

> "Product discovery should be a continuous habit, not a one-time ceremony before a project starts." — Teresa Torres

## 1.1 Build the Persona Table

Personas are not segmented by age and gender, but by **purpose / task / motivation** to distinguish different types of users.

```
| Field | Persona 1: [Nickname] | Persona 2: [Nickname] | Persona 3: [Nickname] |
|---|---|---|---|
| Purpose / Task / Motivation | | | |
| Size (SCALE) | | | |
| Problems / Challenges / Drivers | | | |
| Current Approach & Rationale | | | |
| Frequency | | | |
| Information Sources | | | |
| Adoption / Execution Barriers | | | |
```

Explain the segmentation logic; check for MECE (mutually exclusive, collectively exhaustive); identify the primary TA and secondary TA.

### 📝 Persona Quality Checklist
- ✅ Is the segmentation based on "purpose/task/motivation" rather than demographics?
- ✅ Are Personas MECE (mutually exclusive and collectively exhaustive of the target market)?
- ✅ Is the primary TA vs. secondary TA clearly identified?
- ✅ Are each Persona's "problems/challenges" based on real observations or reasonable inferences?
- ✅ Is "current approach & rationale" specific enough to identify workarounds?
- ❌ Common issues: Segmenting by age/gender, minimal differences between Personas, pain points too vague

## 1.2 Build Persona Cards

```
## [Persona Nickname]: [One-line description]

**Basic Info**: Age / Gender / Occupation / Location / Personality traits
**Background**: [Product-relevant background description]
**Goals / Tasks**: [Goal 1], [Goal 2]
**Current Approach & Rationale**: [What they currently do and why]
**Information Sources**: [Where they get relevant information]
**Barriers / Problems / Challenges / Frustrations**: [Pain point 1], [Pain point 2], [Pain point 3]
```

---

## 📎 File Integration Tips for This Stage

If the user uploads files during this stage, Claude integrates according to these rules:

| Uploaded Content | Integrate Into | Integration Action |
|-----------------|----------------|-------------------|
| User interview transcripts / audio transcriptions | 1.1 Persona + 1.3 JTBD | Extract: user background → Persona fields; pain points + current approach → JTBD deep-dive questions; emotional reactions → emotional/social Jobs |
| User research report (PDF) | 1.1 + 1.2 + 1.3 | Extract quantitative data (user segment proportions) into Persona size; extract qualitative insights into JTBD |
