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
2. Generate CLAUDE.md (Claude Code project memory)
3. Generate TASKS.md (feature breakdown + phased releases + acceptance criteria)
4. Generate TICKETS.md (ticket list)
5. Generate docs/ARCHITECTURE.md (directory structure + DB Schema + API Endpoints)
6. Generate docs/PRD.md + docs/PRODUCT-SPEC.md
7. Generate scripts/setup.sh (one-click initialization)
8. Display Claude Code transition guide

If no product planning content exists in the conversation, prompt the user to run a product planning flow first.
