---
description: Generate Dev Handoff Package — Produces CLAUDE.md + TASKS.md + TICKETS.md + ARCHITECTURE.md + setup.sh, ready to start development in Claude Code
---

Invoke the product-playbook skill.
Then read the following reference files in order:
1. `references/07a-handoff-core.md` (CLAUDE.md template + tech stack confirmation)
2. `references/07b-tasks-tickets.md` (TASKS.md + TICKETS.md templates)
3. `references/07c-architecture-setup.md` (ARCHITECTURE.md + setup.sh + user guidance)

Based on the product planning content completed in the current conversation, generate the full dev handoff package:
1. Confirm the tech stack (if not specified by the user, recommend one based on product characteristics)
2. Create the `.product-dev-active` marker file at the project root (empty file). This signals the plugin's PreToolUse hook that the project has officially entered the dev-handoff phase, so subsequent source-code writes are no longer gated.
3. Generate CLAUDE.md (Claude Code project memory)
4. Generate TASKS.md (feature breakdown + phased releases + acceptance criteria)
5. Generate TICKETS.md (ticket list)
6. Generate docs/ARCHITECTURE.md (directory structure + DB Schema + API Endpoints)
7. Generate docs/PRD.md + docs/PRODUCT-SPEC.md
8. Generate scripts/setup.sh (one-click initialization)
9. Display Claude Code transition guide

If no product planning content exists in the conversation, prompt the user to run a product planning flow first.

Note: `.product-dev-active` is a session-local marker (gitignored by the plugin). Delete it if the project ever returns to planning-only mode.
