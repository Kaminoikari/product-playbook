# 📦 Product Context Accumulation Rules

> This file defines the format, read/write rules, scenario handling, and conflict resolution for `.product-context.md`.
> Loaded by the SKILL.md startup flow or by each mode's S1 pre-step.

## 1. File Location & Lifecycle

- **Path**: `.product-context.md` in the project root directory (same level as `.product-playbook-progress.md`)
- **Permanently retained**: This file is **not deleted** when the flow ends — it persists and accumulates across sessions
- **On first creation**, remind the user: "⚠️ We recommend adding `.product-context.md` to `.gitignore` — this file may contain sensitive product strategy information."

---

## 2. File Format

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

## 3. Three Scenario Detection

At startup (after progress file check, before mode selection), detect the state of `.product-context.md`:

| Condition | Scenario | Action |
|-----------|----------|--------|
| File exists, `Core Strategy` section has actual content (not empty / not placeholder) | **Scenario 1: Complete context** | Silently load. Display: "📦 Detected product context for **[product name]** — it will serve as the baseline for this planning session." |
| File does not exist | **Scenario 2: No context** | Record this state. Trigger Context Bootstrap when entering Feature Extension or Revision Mode (see Section 4) |
| File exists, `Core Strategy` is blank or contains only placeholders, but `Decision History` has at least one entry | **Scenario 3: Partial context** | Display a summary of known information and offer supplementation options (see Section 5) |

**Detection logic**:
1. Does the file exist?
2. Does the `Identity` section have a Product name (not a placeholder)?
3. Does the `Core Strategy` section have a Core JTBD (not a placeholder)? → Yes = Scenario 1
4. Does the `Decision History` section have any `###` entries? → Yes but 3 is No = Scenario 3

---

## 4. Context Bootstrap (Scenario 2 Only)

When the user enters **Feature Extension** or **Revision Mode** but there is no `.product-context.md`, insert "Step 0" before the mode's S1.

**Presentation**:
```
📦 This is your first time using the product planning tool in this project. To make the subsequent flow more efficient,
I'll collect some basic product information first (about 2-3 minutes). It will be saved automatically for future use.
```

### Progressive Collection (do not ask all questions at once)

**Round 1 (required for all modes)**:
- What is the product called?
- Describe what it does in one sentence.
- Product type? (B2C / B2B / B2B2C / Internal tool)

**Round 2 (required for Feature Extension, optional for Revision)**:
- What tech stack do you use? (Languages, frameworks, databases, infrastructure)
- What are the key modules or services?

**Round 3 (required for Revision, optional for Feature Extension)**:
- Do you have DAU/MAU or retention rate data?
- What is the most common user feedback or complaint?
- Are there any known security issues or technical debt?

### Tech Stack Auto-Detection

In addition to the user's verbal input, Bootstrap can **read project files** to assist detection (read-only — does not violate the Hard Gate):

| File | Detection Content |
|------|------------------|
| `package.json` | Node.js ecosystem, frameworks, dependencies |
| `Cargo.toml` | Rust |
| `go.mod` | Go |
| `requirements.txt` / `pyproject.toml` | Python |
| `Dockerfile` / `docker-compose.yml` | Containerized architecture |
| Project root directory structure (`src/`, `app/`, `lib/`, etc.) | Module inference |

After detection, present in **confirmation style**:
```
I detected that your project uses:
- Tech stack: Next.js 14 + TypeScript + PostgreSQL + Redis
- Key modules: auth/, billing/, dashboard/, api/
Is this correct? Anything to add or correct?
```

Only write to `.product-context.md` after the user confirms.

### After Bootstrap Completion

Write the collected information to `.product-context.md`, leave uncollected sections empty (using placeholders), then proceed to the mode's formal S1.

---

## 5. Partial Context Handling (Scenario 3)

When `.product-context.md` exists but Core Strategy is empty, with only Decision History entries:

**Presentation**:
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

**Auto-rebuild attempt**: Scan all Decision History entries, extract recurring product names, tech stacks, and module names from `Affected modules`, `Scope`, and `Key decisions`, and auto-fill into `Architecture & Tech Stack`. Mark with `<!-- inferred from decision history -->` to indicate the inferred source.

---

## 6. Context Auto-Read Rules

When loading context at each mode's S1 pre-step, **only inject relevant sections** — do not display the full file contents to the user:

| Mode + Step | Injected Context Sections |
|-------------|--------------------------|
| Feature Extension S1 | Identity, Architecture & Tech Stack, 3 most recent Decision History entries |
| Revision S1 | Identity, Core Strategy, Accumulated Insights (pain points, PMF, security), 3 most recent Decision History entries |
| Full/Quick/Build S1 | Identity only (product name, type, one-liner) |
| Pre-mortem in any mode | Security posture + Technical debt (from Accumulated Insights) |

**Bloat control**: Decision History defaults to injecting only the 3 most recent entries. The user can request more.

---

## 7. Empty Sections Skip Rules

When the context file exists but some sections are empty, determine whether to skip or collect based on the **mode**:

| Section | Feature Extension | Revision Mode | Full/Quick/Build |
|---------|------------------|---------------|-----------------|
| Identity | Required (Bootstrap if missing) | Required (Bootstrap if missing) | The flow itself will produce this — no pre-loading needed |
| Core Strategy | **Can skip** | Required (quick Q&A collection within S1 if missing) | The flow itself will produce this |
| Architecture & Tech Stack | Required (Bootstrap or auto-detect if missing) | Can skip | The flow itself will produce this |
| Decision History | Can skip | Include if available, skip if not | The flow itself will produce this |
| Accumulated Insights | Can skip | Include if available, skip if not | The flow itself will produce this |

| Feature Extension | Identity (confirm only), Architecture & Tech Stack (required), Core Strategy (skip allowed) |

**Principle**: Empty sections **do not block the flow**. Only sections that are "required" for the current mode and are empty will trigger collection.

---

## 8. Context Auto-Write Rules (Extraction at Flow End)

At the end of a flow (in sync with the end condition check in `rules-end-of-flow.md`), automatically extract context:

| Flow Type | Sections Written/Updated |
|-----------|-------------------------|
| Quick | Identity, Core Strategy (JTBD + North Star), append to Decision History |
| Full | **All sections** (overwrite Identity/Strategy/Insights, append to History) |
| Revision | Update Core Strategy (if repositioned), update Insights, append to History |
| Feature Extension | Merge Architecture, append to Decision History (feature-specific template) |
| Custom | Update sections corresponding to completed steps |
| Build (7 steps) | Identity, Core Strategy (partial), append to History |

### Write Strategy

| Section | Strategy | Notes |
|---------|----------|-------|
| Identity | **Overwrite with latest** | Always overwrite with the most recent flow's data |
| Core Strategy | **Overwrite with latest** | Same as above. Post-revision strategy replaces pre-revision strategy |
| Architecture & Tech Stack | **Merge** | New modules are added without deleting old ones. New tech items are appended |
| Decision History | **Append only** | Never delete previous entries. Append one entry each time a flow is completed |
| Accumulated Insights | **Merge and deduplicate** | Pain points and feedback themes are deduplicated and appended. PMF and Security are overwritten with latest values |

### Decision History Append Template

**General template**:
```markdown
### [ISO date] - [Flow type]
- **Scope**: [...]
- **Key decisions**: [...]
- **Risks identified**: [...]
- **MVP boundary**: [...]
- **Success metrics**: [...]
```

**Feature Extension template**:
```markdown
### [ISO date] - Feature Extension: [Feature name]
- **Problem**: [One-sentence problem statement]
- **Chosen solution**: [Selected solution + rationale]
- **Affected modules**: [Affected modules]
- **Scope**: [What to do / What not to touch]
- **Acceptance criteria**: [Acceptance criteria]
```

### Completion Notification

```
✅ Product context has been updated in `.product-context.md` — it will be automatically loaded in your next planning session.
```

---

## 9. Conflict Resolution

### User corrects existing context

Fully allowed. User-provided corrections directly overwrite the corresponding section (latest wins).

### User-provided data conflicts with codebase

When the S1 pre-step reads both `.product-context.md` and project files (e.g., `package.json`) and finds inconsistencies:

```
⚠️ Inconsistency detected:
- Context records: [value from context]
- Project codebase: [value detected from code]
Which one is correct?
  1️⃣ Use codebase as source of truth (update context)
  2️⃣ Use context as source of truth (may be in the middle of a migration)
  3️⃣ Both are incomplete — let me explain
```

**Handling principles**:
- **Do not auto-overwrite** — let the user decide
- Update `.product-context.md` after the user chooses
- If "in the middle of a migration" is selected, annotate in the Architecture section: `[Migrating] React → Vue 3`
- Log the conflict in Decision History

### New data from the flow overrides context

If data produced during a flow differs from old data in the context (e.g., Revision Mode redefines the JTBD), **flow data takes priority**. It is automatically overwritten at the end of the flow.

---

## 10. Language Preference

When `.product-context.md` is created or updated, record the language preference in the `Language Preference` section:

- **Installed language**: Detected from the `.lang` file in the skill installation directory, or from the user's locale.
- **User's preferred language**: The language the user communicates in during the session.

**Loading rule**: When loading an existing `.product-context.md`, if a language preference is recorded, continue the session in that language.

**Write timing**: Language preference is written during Context Bootstrap (Section 4) or at the end of the first flow that creates the context file. It is updated whenever the user explicitly switches language mid-session.
