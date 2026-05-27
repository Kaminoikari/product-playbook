# Development Handoff — Core Handoff Package

> Triggered when the user says "start development," "produce a dev handoff package," "set up my project," or "connect to Claude Code."
> Read this file, consolidate the outputs from the entire product planning process, and generate a development handoff package that can be used directly in the Claude Code CLI.

## Environment Constraints & Handoff Strategy

**Key fact: Claude Chat / Cowork and Claude Code are separate runtime environments — you cannot launch Claude Code from within Chat.**

The handoff strategy is therefore: **Produce a structured development handoff package (a set of files)** that the user downloads, places in their project folder, and can kick off the entire development workflow with a single prompt in Claude Code.

The handoff method depends on the user's environment:

| User Environment | Handoff Method |
|-----------------|----------------|
| **Claude Chat (Web/App)** | Produce a zip file for download; user extracts to project directory then opens Claude Code |
| **Claude Cowork (Desktop)** | Same as above, but can write files directly to a user-specified local path |
| **Already in Claude Code** | Create all files directly in the project directory (in this scenario, this skill is likely referenced from CLAUDE.md) |

---

## Development Handoff Package Contents

Produce the following file set, all placed in the project root:

```
[project-name]/
├── .gitignore             # Version control exclusions (.env, secrets, progress files, etc. — template in references/07c-architecture-setup.md)
├── CLAUDE.md              # Claude Code's project memory: product context + development guidelines
├── TASKS.md               # Feature breakdown + Phase milestones + per-Task acceptance criteria
├── TICKETS.md             # Ticket content: title, description, acceptance criteria per ticket — PM can create tickets directly
├── docs/
│   ├── PRD.md             # Full PRD (consolidated from 04-develop.md output format)
│   ├── ARCHITECTURE.md    # Technical architecture: directory structure + DB schema + API endpoints + security architecture
│   └── PRODUCT-SPEC.md    # Product Spec Summary (consolidated from 05-deliver.md → 4.6)
└── scripts/
    └── setup.sh           # One-click initialization script (create directories + install dependencies)
```

---

## 📄 CLAUDE.md Template

CLAUDE.md is Claude Code's project memory file — Claude Code automatically reads it on every startup. It must include:

```markdown
# [Product Name] — Project Guide

## Product Context

**One-liner**: [PR-FAQ headline]
**Target Users**: [Persona in one sentence]
**Core JTBD**: [Target Customer] wants to [Job] in the context of [Job Context]
**Aha Moment**: When the user completes [action], they experience the core value
**North Star Metric**: [Metric name + definition]

## Tech Stack

- **Frontend**: [Framework + version]
- **Backend**: [Framework + version]
- **Database**: [Type + version]
- **Deployment**: [Platform]
- **Package Manager**: [Tool]

## Development Guidelines

- Develop in [language]
- Follow [style guide / lint rules]
- Commit message format: `[type]: [description]` (type: feat / fix / refactor / docs / test)
- Branch strategy: [main / develop / feature-xxx]
- Every feature must reference its User Story number (see TASKS.md)

## MVP Boundaries

**Must-Have (P0)**:
- [Feature 1]
- [Feature 2]
- [Feature 3]

**Explicitly Not Doing**:
- [Exclusion 1] — Reason: [rationale]
- [Exclusion 2] — Reason: [rationale]

## Key Decision Log

| Decision | Choice | Rationale | Date |
|----------|--------|-----------|------|
| [e.g., Database selection] | [PostgreSQL] | [Needs relational queries + JSON support] | [Date] |

## Risk Alerts (from Pre-mortem)

- ⚠️ [Risk 1]: [Preventive measure]
- ⚠️ [Risk 2]: [Preventive measure]

## Security Notes

> Full security checklist at `references/08-security-checklist.md`. Below are this product's key security decisions:

- Authentication: [JWT / Session / OAuth]
- CORS policy: [Allowed origins]
- Rate Limiting: [Strategy summary]
- Sensitive data: [Handling approach]

## Development Workflow

Follow the Phase order in `TASKS.md`. After completing each Phase:
1. Verify all Task acceptance criteria pass
2. Ask the user whether to proceed to the next Phase
3. If architectural questions arise, refer to `docs/ARCHITECTURE.md`
```

---

## Tech Stack Confirmation Flow

Before producing the handoff package, the tech stack must be confirmed. If the user hasn't specified, ask in this order:

### Must-Ask (Affects all outputs)

```
1. What type of application is this?
   □ Web App (browser)
   □ Mobile App (iOS / Android / cross-platform)
   □ Desktop App
   □ API / Backend Service
   □ CLI Tool
   □ Other

2. Do you have a preferred tech stack?
   (If not, I'll recommend one based on the product characteristics)
```

### Recommendation Logic (When user hasn't specified)

| Application Type | Recommended Stack | Rationale |
|-----------------|-------------------|-----------|
| Web App (fast MVP validation) | Next.js + Tailwind + Supabase | Full-stack in one, easy deployment, built-in Auth |
| Web App (complex backend logic) | React + Node.js/Express + PostgreSQL | High flexibility, mature ecosystem |
| Web App (Python team) | React + FastAPI/Django + PostgreSQL | Python ecosystem, Django has built-in Admin |
| Mobile App (cross-platform) | React Native / Flutter | Single codebase covers both platforms |
| API Service | FastAPI / Express / Go | Lightweight, high performance |

> Claude should explain the rationale when recommending and remind the user they can override the recommendation.

### Optional (Follow-up based on product needs)

```
3. Do you need user authentication? (Affects Auth approach selection)
4. Any real-time requirements? (WebSocket / SSE)
5. Need file upload/processing? (Affects storage choice)
6. Where do you plan to deploy? (Vercel / Railway / AWS / self-hosted)
```
