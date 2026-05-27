# Stage 1: Discovery — OST + Journey Map

## 1.4 Opportunity Solution Tree (OST)

**Applicable: Full mode / high completeness**

The OST starts from the product goal and systematically connects opportunities to solutions:

```
[Product Goal / Desired Outcome]
    │
    ├── [Opportunity 1: User pain point or need]
    │       ├── [Solution 1a]
    │       └── [Solution 1b]
    ├── [Opportunity 2: User pain point or need]
    │       └── [Solution 2a]
    └── [Opportunity 3: User pain point or need]
            └── [Solution 3a]
```

Core principles:
- The goal (Outcome) is a measurable result, not a feature or output
- Opportunities come from user research, not internal brainstorming
- Solutions map to opportunities — don't skip opportunities and jump straight to solutions
- Go broad, then deep: list all opportunities first, then explore solutions one by one

## 1.5 User Journey Map

**Applicable: Full mode / high completeness / audience is designers**

**Step 1: Overview Table**

```
**[Persona Name] — Task: [Task description]**

| Stage | Core Behavior | Emotion | Key Pain Point |
|---|---|---|---|
| [Stage 1] | [One-line description of primary behavior] | [Emotion + emoji] | [The most important pain point] |
```

**Step 2: Expand Each Stage in Detail**

```
> **Stage: [Stage Name]**
> - **Doing**: [What the user actually does at this stage]
> - **Thinking**: [What's going through the user's mind, ideally in first-person voice]
> - **Feeling**: [Emotional state and why]
> - **Stakeholder**: [Who is involved at this stage]
> - **Problem**: [Specific difficulties or frustrations]
```

**Step 3: Grouping**
- If stages are too granular, merge them into larger stage groups
- Consolidate pain points across stages, flag which are core pain points

---

## 📎 File Integration Tips for This Stage

If the user uploads files during this stage, Claude integrates according to these rules:

| Uploaded Content | Integrate Into | Integration Action |
|-----------------|----------------|-------------------|
| Whiteboard / hand-drawn flow diagrams | 1.5 Journey Map | Recognize the flow and convert to structured table; preserve original emotion markers |
| User behavior data (CSV) | 1.4 OST + 1.5 Journey Map | Use data to validate which behavior paths are most common and which stages have the highest drop-off |
