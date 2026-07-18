# product-playbook

Claude Code plugin: 16 product-planning lenses + a dev-discipline layer (six gates, dual reviewers, deterministic hooks).

- Tests: `python3 -m unittest discover tests` (must be green before any finish-branch step).
- Docs entry point: `docs/INDEX.md` — one line per document; read only the file(s) that match your question.
- The ACTIVE local install is the skills-dir copy at `~/.claude/skills/product-playbook`; it refreshes ONLY via `bash install.sh --update` after a version bump (plugin cache keys on version — any content change needs a bump).
- Pushing a `package.json` version change to `main` triggers npm auto-publish and a GitHub release; never push without the user choosing to release.
- Eval suites (`npm run eval:*`) call the real API — never wire them into CI on push/PR (workflow_dispatch only).
