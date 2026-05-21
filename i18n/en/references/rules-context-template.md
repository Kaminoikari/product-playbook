# 📦 Product Context — Templates and Detailed UX Scripts

> Lazy-loaded reference. Triggered per the trigger table in `rules-context.md` §8. Contains only the verbose YAML/markdown formats and UX scripts that aren't needed for routine session startup.

## File Format

```markdown
# Product Context
<!-- Auto-maintained by product-playbook. Do not delete. -->
<!-- last-updated: [ISO timestamp] -->

## Identity
- **Product name**: [name]
- **Product type**: [B2C / B2B / B2B2C / Internal tool]
- **One-liner**: [One-sentence description]
- **Target audience**: [Primary Persona summary]

## Core Strategy
- **Core JTBD**: [Target Customer] + wants to [Job] + in [Context]
  - Functional: [...]
  - Emotional: [...]
  - Social: [...]
- **Positioning (April Dunford)**:
  - Real competitive alternatives: [...]
  - Unique attributes: [...]
  - Core value: [...]
  - Target market: [...]
  - Market category: [...]
- **North Star Metric**: [Metric name + definition]
- **Aha Moment**: [Description]

## Architecture & Tech Stack
- **Tech stack**: [Languages, frameworks, infrastructure]
- **Key modules**: [List of key modules]
- **Data model highlights**: [Core data entities, if known]

## Decision History
<!-- Append-only. Add one entry each time a flow is completed. -->

### [ISO date] - [Flow type: Full/Quick/Revision/Feature Extension/Custom/Build]
- **Scope**: [Planning/change scope]
- **Key decisions**: [Major decisions]
- **Risks identified**: [Risks]
- **MVP boundary**: [What to do / What not to do]
- **Success metrics**: [Success metrics + target values]

## Language Preference
- **Installed language**: [auto-detected from .lang file or user's language]
- **User's preferred language**: [the language the user communicates in]

## Accumulated Insights
- **Known pain points**: [Pain point list, with sources]
- **User feedback themes**: [Feedback themes across sessions]
- **PMF status**: [Most recent assessment level + date]
- **Security posture**: [Auth/authorization methods, known vulnerabilities]
- **Technical debt**: [Technical debt accumulated across sessions]
```

---

## Bootstrap (Scenario 2 only)

When the user enters **Feature Extension** or **Revision Mode** with no `.product-context.md`, insert "Step 0" before S1.

**Presentation:**
```
📦 This is your first time using the product planning tool in this project. To make the subsequent flow more efficient,
I'll collect some basic product information first (about 2-3 minutes). It will be saved automatically for future use.
```

### Progressive Collection (do not ask all at once)

**Round 1 (required for all modes):**
- What is the product called?
- Describe what it does in one sentence.
- Product type? (B2C / B2B / B2B2C / Internal tool)

**Round 2 (required for Feature Extension, optional for Revision):**
- What tech stack do you use? (Languages, frameworks, databases, infrastructure)
- What are the key modules or services?

**Round 3 (required for Revision, optional for Feature Extension):**
- Do you have DAU/MAU or retention rate data?
- What is the most common user feedback or complaint?
- Are there any known security issues or technical debt?

### Tech Stack Auto-Detection

Bootstrap can read project files (read-only, no Hard Gate violation):

| File | Detection Content |
|------|------------------|
| `package.json` | Node.js ecosystem, frameworks, dependencies |
| `Cargo.toml` | Rust |
| `go.mod` | Go |
| `requirements.txt` / `pyproject.toml` | Python |
| `Dockerfile` / `docker-compose.yml` | Containerized architecture |
| Project root structure (`src/`, `app/`, `lib/`, etc.) | Module inference |

Confirmation style:
```
I detected that your project uses:
- Tech stack: Next.js 14 + TypeScript + PostgreSQL + Redis
- Key modules: auth/, billing/, dashboard/, api/
Is this correct? Anything to add or correct?
```

Write only after user confirms.

### Bootstrap → S1 Sequencing (Hard Gate — Bootstrap does NOT block flow)

- **Default**: Bootstrap and S1 MUST execute in the **same turn** as S0 → S1. Pause is fixed **after S1 completion**, not between S0 and S1.
- **If user message already provides required fields** → confirm in a table, proceed to S1.
- **If fields missing** → surface known/pending table in same turn, enter S1 with placeholders, fold pending into S1 confirmation question.
- **Forbidden**: pausing between S0 and S1 to wait for Round 1 answers. If S1 shows `⬜ pending` while waiting for user input, you have failed this rule.

After Bootstrap: write to `.product-context.md` (even with placeholders), then enter S1 in same turn.

---

## Partial Context UX (Scenario 3)

```
📦 I have records from your previous [N] planning sessions:
- Tech stack: [Known stack merged from Decision History]
- Previously modified modules: [Affected modules merged from Decision History]
- Core product strategy has not been recorded yet.

Would you like to:
  1️⃣ Start directly (use known information, skip strategy section)
  2️⃣ Fill in strategy information first (JTBD, Positioning, North Star Metric)
  3️⃣ This information is incorrect — let me fix it
```

**Auto-rebuild attempt**: Scan Decision History, extract recurring product names, tech stacks, module names from `Affected modules`, `Scope`, `Key decisions`. Auto-fill into `Architecture & Tech Stack`. Mark with `<!-- inferred from decision history -->`.

---

## Append Templates

**General template:**
```markdown
### [ISO date] - [Flow type]
- **Scope**: [...]
- **Key decisions**: [...]
- **Risks identified**: [...]
- **MVP boundary**: [...]
- **Success metrics**: [...]
```

**Feature Extension variant:**
```markdown
### [ISO date] - Feature Extension: [Feature name]
- **Problem**: [One-sentence problem statement]
- **Chosen solution**: [Selected solution + rationale]
- **Affected modules**: [Affected modules]
- **Scope**: [What to do / What not to touch]
- **Acceptance criteria**: [Acceptance criteria]
```

---

## Conflict UX (codebase vs context)

```
⚠️ Inconsistency detected:
- Context records: [value from context]
- Project codebase: [value detected from code]
Which one is correct?
  1️⃣ Use codebase as source of truth (update context)
  2️⃣ Use context as source of truth (may be in the middle of a migration)
  3️⃣ Both are incomplete — let me explain
```

- Do not auto-overwrite — let user decide
- If migration: annotate Architecture as `[Migrating] React → Vue 3`
- Log conflict in Decision History
