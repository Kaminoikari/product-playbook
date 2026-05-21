# 📦 Product Context Accumulation Rules

> Loaded by SKILL.md startup. Contains all decision logic (when/which/how). Verbose YAML formats and full UX scripts live in `rules-context-template.md` (lazy-loaded only when actually writing the file or running Bootstrap).

## 1. File Lifecycle

- **Path**: `.product-context.md` in project root (same level as `.product-playbook-progress.md`)
- **Permanently retained**: Persists across sessions
- **On first creation**: remind user to add to `.gitignore` (may contain sensitive strategy info)

---

## 2. Three Scenario Detection (at startup)

After progress file check, before mode selection:

| Condition | Scenario | Action |
|-----------|----------|--------|
| File exists, `Core Strategy` has actual content | **1. Complete** | Silently load. Display: "📦 Detected product context for **[product name]** — baseline for this session." |
| File does not exist | **2. None** | Record state. Trigger Bootstrap when entering Feature/Revision. → Load template §Bootstrap |
| File exists, Core Strategy empty/placeholder, Decision History has ≥1 entry | **3. Partial** | Show known-info summary + supplementation options. → Load template §Partial |

**Detection logic:**
1. File exists?
2. `Identity` has Product name (not placeholder)?
3. `Core Strategy` has Core JTBD (not placeholder)? → Yes = Scenario 1
4. `Decision History` has any `###` entries? → Yes but step 3 No = Scenario 3

---

## 3. Auto-Read Rules (at each mode's S1 pre-step)

**Only inject relevant sections** — do not display full file to user:

| Mode + Step | Injected Sections |
|-------------|------------------|
| Feature Extension S1 | Identity, Architecture & Tech Stack, 3 most recent Decision History |
| Revision S1 | Identity, Core Strategy, Accumulated Insights (pain points, PMF, security), 3 most recent Decision History |
| Full/Quick/Build S1 | Identity only (product name, type, one-liner) |
| Pre-mortem in any mode | Security posture + Technical debt (from Accumulated Insights) |

**Bloat control**: Decision History defaults to 3 most recent entries. User can request more.

---

## 4. Empty Sections Skip Rules

| Section | Feature Extension | Revision | Full/Quick/Build |
|---------|------------------|----------|-----------------|
| Identity | Required (Bootstrap if missing) | Required (Bootstrap if missing) | Flow produces it |
| Core Strategy | Can skip | Required (quick Q&A in S1 if missing) | Flow produces it |
| Architecture & Tech Stack | Required (Bootstrap or auto-detect) | Can skip | Flow produces it |
| Decision History | Can skip | Include if available, skip if not | Flow produces it |
| Accumulated Insights | Can skip | Include if available, skip if not | Flow produces it |

**Principle**: Empty sections do not block flow. Only "required" + empty triggers collection.

---

## 5. Auto-Write Rules (at flow end)

Sync with `rules-end-of-flow.md` end condition. Auto-extract context:

| Flow Type | Sections Written/Updated |
|-----------|-------------------------|
| Quick | Identity, Core Strategy (JTBD + North Star), append History |
| Full | All sections (overwrite Identity/Strategy/Insights, append History) |
| Revision | Update Core Strategy (if repositioned), update Insights, append History |
| Feature Extension | Merge Architecture, append History (feature template) |
| Custom | Update sections corresponding to completed steps |
| Build | Identity, Core Strategy (partial), append History |

### Write strategy per section

| Section | Strategy |
|---------|----------|
| Identity | Overwrite with latest |
| Core Strategy | Overwrite with latest (post-revision replaces pre-revision) |
| Architecture & Tech Stack | Merge (new modules added, old kept) |
| Decision History | Append only (never delete previous) |
| Accumulated Insights | Merge & deduplicate (pain points/feedback dedupe; PMF/Security overwrite) |

When writing for the first time (creating the file) or appending Decision History → **load `rules-context-template.md` §File Format / §Append Templates**.

On completion display: `✅ Product context has been updated in '.product-context.md' — auto-loaded next session.`

---

## 6. Conflict Handling (summary)

| Conflict type | Resolution |
|---------------|-----------|
| User corrects existing context | Latest wins — direct overwrite |
| Context conflicts with codebase (e.g., package.json differs) | Do not auto-overwrite — ask user. → Load template §Conflict UX |
| Flow data differs from old context | Flow data wins — auto-overwrite at flow end |

---

## 7. Language Preference (summary)

Record in `Language Preference` section when context is created/updated:
- **Installed language**: from `.lang` file or user locale
- **User's preferred language**: language user communicates in

On load: if recorded, continue session in that language.
On write: written during Bootstrap or end of first flow that creates the file. Updated when user switches language mid-session.

---

## 8. When to load `rules-context-template.md`

Only when ONE of these triggers fires:

| Trigger | Template section |
|---------|------------------|
| Scenario 2 + entering Feature Extension / Revision | §Bootstrap, §File Format |
| Scenario 3 (Partial context) | §Partial Context, §File Format |
| Writing context for the first time | §File Format |
| Appending Decision History at flow end | §Append Templates |
| Codebase conflict detected | §Conflict UX |
| Bootstrap finished → writing baseline | §File Format |

Do NOT pre-load the template at startup.
