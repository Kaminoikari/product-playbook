# Development Handoff — TASKS.md + TICKETS.md

## 📄 TASKS.md Template

Core principles for feature breakdown:
- Start from the MVP must-haves (P0 features)
- Each Task maps to a User Story
- Phases have clear dependencies: Phase N+1 depends on Phase N outputs
- Each Task includes acceptance criteria that Claude Code can self-verify

```markdown
# [Product Name] — Development Task List

## Phase 0: Project Initialization
> Goal: Establish a runnable blank project skeleton

- [ ] **T0.1** Initialize project (`scripts/setup.sh` or manual)
  - Acceptance:
    - [ ] `npm run dev` / `python manage.py runserver` or equivalent command starts successfully
    - [ ] `.gitignore` created, includes `.env`, `.env.local`, `node_modules/`, `.product-playbook-progress.md`, `.product-dev-active`, and other sensitive files
    - [ ] `.env.example` created (key names only, no actual values)
- [ ] **T0.2** Set up linter + formatter
  - Acceptance: lint passes with no errors
- [ ] **T0.3** Set up database + run initial migration
  - Acceptance: Database is connectable, base tables are created
- [ ] **T0.4** Set up base routing structure
  - Acceptance: All main page routes are accessible (returning blank pages is fine)

## Phase 1: Core Flow (Aha Moment Path)
> Goal: Let users complete the shortest path from entry to the Aha Moment
> Corresponds to User Stories: [US-001, US-002, ...]

- [ ] **T1.1** [Feature name]
  - User Story: As a [Persona], I want to [action], so that [value]
  - Acceptance Criteria:
    - [ ] [Specific testable condition 1]
    - [ ] [Specific testable condition 2]
  - Technical Notes: [Required APIs / third-party services / special logic]

- [ ] **T1.2** [Feature name]
  - User Story: ...
  - Acceptance Criteria: ...

> **Phase 1 Completion Checkpoint**: User can complete [Aha Moment action]. If not, do not proceed to Phase 2.

## Phase 2: Complete MVP
> Goal: Fill in all remaining P0 features not covered in Phase 1
> Corresponds to User Stories: [US-003, US-004, ...]

- [ ] **T2.1** [Feature name]
  - ...

> **Phase 2 Completion Checkpoint**: All P0 User Story acceptance criteria pass.

## Phase 3: Quality & Experience
> Goal: Error handling, edge cases, loading states, basic security

- [ ] **T3.1** Global error handling
- [ ] **T3.2** Form validation + edge cases
- [ ] **T3.3** Loading states + empty states
- [ ] **T3.4** Security check (verify each item per `references/08-security-checklist.md`)
  - Acceptance:
    - [ ] OWASP Top 10 related items addressed (input validation, authentication, XSS protection, CSRF protection)
    - [ ] Security headers configured (CSP, X-Frame-Options, HSTS, etc.)
    - [ ] CORS policy configured (no wildcard *)
    - [ ] Sensitive API endpoints have rate limiting
    - [ ] API error responses don't leak internal information
- [ ] **T3.5** Responsive design (if Web)

## Phase 4: Deployment
> Goal: Make the app accessible to external users

- [ ] **T4.1** Environment variable management
- [ ] **T4.2** Deployment configuration
- [ ] **T4.3** Basic monitoring + logging
```

---

## 📄 TICKETS.md Template

TICKETS.md takes the feature breakdown from TASKS.md and produces structured content that can be directly used to create tickets in project management tools. Each ticket contains all the information a PM needs.

> **Design goal**: PMs can copy each ticket's content directly into Jira / Asana / Linear or other tools to create tickets. Future versions will support automatic ticket creation via API.

```markdown
# [Product Name] — Ticket List

> Generated: [timestamp]
> Corresponds to TASKS.md version: [version/timestamp]
> Total: [N] tickets

---

## Ticket Overview

| Ticket # | Title | Phase | Priority | Estimated Hours | Dependencies |
|----------|-------|-------|----------|----------------|-------------|
| TKT-001 | [Title] | Phase 0 | P0 | [X]h | — |
| TKT-002 | [Title] | Phase 1 | P0 | [X]h | TKT-001 |
| ... | | | | | |

---

## TKT-001: [Title]

**Phase**: Phase 0 — Project Initialization
**Corresponding Task**: T0.1
**Priority**: P0
**Estimated Hours**: [X] hours
**Dependencies**: None
**Assignee**: [Role/team, e.g., Backend Engineer]

### Description

[1-3 paragraphs describing what this ticket accomplishes, including business context and technical goals]

### User Story

As a [Persona], I want to [action], so that [value]

### Acceptance Criteria

- [ ] [Specific testable condition 1]
- [ ] [Specific testable condition 2]
- [ ] [Specific testable condition 3]

### Technical Notes

- [Implementation considerations]
- [Required APIs / third-party services]
- [Related file paths or modules]

### Suggested Labels

`[Phase 0]` `[backend]` `[setup]`

---

## TKT-002: [Title]

[Same format, expanded for each ticket]
```

### Ticketing Rules

1. **Ticket-to-Task mapping**: Each Task in TASKS.md maps to one ticket (TKT-001 ↔ T0.1); overly large Tasks may be split into multiple tickets
2. **Priority inheritance**: Phase 0-1 default to P0, Phase 2 defaults to P1, Phase 3-4 default to P2 — adjustable based on RICE scores
3. **Dependencies**: Explicitly mark ticket-to-ticket dependencies to prevent engineers from skipping steps
4. **Estimated hours**: Based on the Task granularity principle (1-4 hours), provide reasonable estimates
5. **Suggested labels**: Include Phase, technical domain (frontend / backend / database / infra), feature module

### Project Management Tool Integration (Reserved)

> The following is a reserved interface design for future automatic ticketing. The current version only produces TICKETS.md for manual PM ticket creation.

TICKETS.md's structured format reserves the following fields for future API import:

| Field | Jira Mapping | Asana Mapping | Linear Mapping |
|-------|-------------|--------------|----------------|
| Ticket # | Issue Key | Task ID | Issue ID |
| Title | Summary | Task Name | Title |
| Description | Description | Description | Description |
| Priority | Priority | Custom Field | Priority |
| Estimated Hours | Story Points / Time Estimate | Custom Field | Estimate |
| Dependencies | Linked Issues | Dependencies | Relations |
| Labels | Labels + Components | Tags | Labels |
| Phase | Epic | Section | Project |
| Assignee | Assignee | Assignee | Assignee |
| Acceptance Criteria | Acceptance Criteria (Description) | Subtasks | Sub-issues |

---

## Feature Breakdown Logic

Rules for converting MVP features into Tasks:

### Phase Division Principles

```
Phase 0: Project skeleton (required for all modes)
  → Initialization, linter, DB, base routing

Phase 1: Shortest path to Aha Moment (most important)
  → Minimum features needed from user entry to Aha Moment
  → Only includes P0 features on this path

Phase 2: Complete MVP
  → Fill in remaining P0 features not covered in Phase 1
  → Secondary flows, supporting pages

Phase 3: Quality & Experience
  → Error handling, edge cases, loading/empty states
  → Basic security, responsive design

Phase 4: Deployment
  → Environment variables, deployment config, monitoring
```

### Task Granularity Principle

- Each Task should be completable in **1-4 hours**
- Too large → Split into sub-Tasks (T1.1a, T1.1b)
- Too small → Merge into a related Task
- Each Task must have at least one testable acceptance criterion

### User Story → Task Mapping

```
A single User Story may map to 1-3 Tasks:
  US-001: As a new user, I want to register an account, so I can start using the product
    → T1.1: Registration page UI
    → T1.2: Registration API + data validation
    → T1.3: Email verification flow (if needed for MVP)
```
