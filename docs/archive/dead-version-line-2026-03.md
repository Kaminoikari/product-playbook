# Archived release notes — abandoned 2.x version line (2026-03)

These GitHub releases came from an earlier, abandoned versioning line (March 2026, an i18n / multi-language install feature series). The project was later renumbered — its version was reset in `package.json` and it restarted at 1.2.x → 2.0.0 → 2.1.0 → 2.3.0 (the current dev-discipline line). The old tags collided with the current line's version numbers and caused the release workflow to silently skip creating a real GitHub release (it saw the tag already existed). The stale tags and releases were deleted on 2026-07-19 to clear that trap; their notes are preserved here so the history stays viewable. The underlying commits remain in `main`'s history — `git show <commit>` restores the exact state each release shipped.

| Tag | Title | Published | Commit |
|-----|-------|-----------|--------|
| v2.4.0 | v2.4.0 — Auto Version Check + Silent Language Switching | 2026-03-23 | `a43d5e5` |
| v2.5.0 | v2.5.0 — SKILL.md Copy Audit & Mode Selection Fix | 2026-03-23 | `5367765` |
| v2.5.1 | v2.5.1 — Root Files Sync | 2026-03-23 | `55e43f9` |
| v2.5.2 | v2.5.2 — Legacy v1.x Upgrade Detection | 2026-03-23 | `8367332` |
| v2.5.3 | v2.5.3 — Incremental Document Output | 2026-03-23 | `d3141d7` |
| v2.6.0 | v2.6.0 — Multi-Format Document Import/Export | 2026-03-23 | `f9a6f57` |
| v2.6.1 | v2.6.1 — Decision Consistency Check | 2026-03-24 | `fd0a8db` |
| v2.6.2 | v2.6.2 — Decision Consistency Check + Pipeline Audit | 2026-03-24 | `0fc71f1` |

> Also deleted from the same line: **v2.2.0** ("6 Languages, 22 Frameworks, Full i18n") and the original **v2.3.0** ("Install All Languages by Default"), removed before this archive was written; only their titles were captured. v2.3.0 was recreated as the real dev-discipline release.

---

## v2.4.0 — v2.4.0 — Auto Version Check + Silent Language Switching

*Published 2026-03-23 · commit `a43d5e5`*

## What's New

### 📦 Automatic Version Check
- Skill silently checks npm for newer versions at startup (3s timeout)
- Shows update prompt only when a newer version exists
- Non-blocking: never prevents skill from loading, gracefully degrades offline
- Localized update message in all 6 languages

### 🌐 Silent Language Switching (improved from v2.3.0)
- No more confirmation dialog — detects user's language and switches automatically
- Also responds to explicit requests ("please use Japanese")

### 🔧 Version Tracking
- `.version` file now stores semver (e.g., `2.4.0`) instead of git hash
- Enables accurate comparison with npm registry

### Full Changelog
https://github.com/Kaminoikari/the-product-playbook/compare/v2.3.0...v2.4.0

---

## v2.5.0 — v2.5.0 — SKILL.md Copy Audit & Mode Selection Fix

*Published 2026-03-23 · commit `5367765`*

## What's Changed

### 📋 SKILL.md Comprehensive Copy Audit
- **6 numbered modes**: Mode selection now shows 6 numbered options (was 5 bullet items)
- **Feature Extension Mode**: Promoted from "Build Mode variant" to independently selectable mode
- **Prompt text**: Added "Select a mode (enter a number or name), or tell me about your product"
- **Naming consistency**: EN version renamed "Skip to Solution Mode" → "Build Mode" (matches rules-build.md)
- **Mode Dispatcher**: Added Feature Extension Mode entry
- **Startup flow**: Fixed numbering conflict between version check and progress check

All changes applied across all 6 languages.

### Full Changelog
https://github.com/Kaminoikari/the-product-playbook/compare/v2.4.0...v2.5.0

---

## v2.5.1 — v2.5.1 — Root Files Sync

*Published 2026-03-23 · commit `55e43f9`*

### Fix
- Sync root SKILL.md, commands/, references/ with i18n/zh-TW/ (was outdated, missing v2.x features)

### Full Changelog
https://github.com/Kaminoikari/the-product-playbook/compare/v2.5.0...v2.5.1

---

## v2.5.2 — v2.5.2 — Legacy v1.x Upgrade Detection

*Published 2026-03-23 · commit `8367332`*

### Fix
- Detect legacy v1.x installations (git hash in .version file) and force upgrade
- Shows warning: "Detected legacy installation (v1.x). Upgrading to v2.5.2..."
- Semver-based version comparison for v2.x installations

### Full Changelog
https://github.com/Kaminoikari/the-product-playbook/compare/v2.5.1...v2.5.2

---

## v2.5.3 — v2.5.3 — Incremental Document Output

*Published 2026-03-23 · commit `d3141d7`*

### New Feature: Incremental Document Output

When using **Feature Extension** or **Revision Mode**, you can now upload your existing PRD/spec and get an **incremental update** instead of a standalone document:

- Source document auto-detected during S1 context collection
- Document structure, format, and style preserved
- New content marked with `[NEW]`, modifications marked with `[UPDATED]`
- Choose between incremental update (recommended) or standalone spec
- Extended Output Prompt shows incremental option first

Applied across all 6 languages.

### Full Changelog
https://github.com/Kaminoikari/the-product-playbook/compare/v2.5.2...v2.5.3

---

## v2.6.0 — v2.6.0 — Multi-Format Document Import/Export

*Published 2026-03-23 · commit `f9a6f57`*

### New Features

#### 📄 Multi-Format Document Import/Export
- Import existing documents (PRD, specs, architecture docs) during planning
- Auto-detect document format and structure
- Incremental update output: new content marked `[NEW]`, modifications marked `[UPDATED]`
- Export to multiple formats: Markdown, HTML report, PRD package, dev handoff

#### 📎 Source Document Identification (v2.5.3)
- Auto-detect uploaded source documents in Feature Extension / Revision mode
- Choose between incremental update (recommended) or standalone output
- Original document format, style, and naming preserved

### Fixes
- Legacy v1.x installation detection and forced upgrade (v2.5.2)
- Root SKILL.md/commands/references synced with i18n/zh-TW (v2.5.1)
- SKILL.md: 6 numbered modes, Feature Extension as independent mode (v2.5.0)

### Full Changelog
https://github.com/Kaminoikari/the-product-playbook/compare/v2.5.3...v2.6.0

---

## v2.6.1 — v2.6.1 — Decision Consistency Check

*Published 2026-03-24 · commit `fd0a8db`*

### New: Decision Consistency Check (Mode-Specific)

Before generating final output, scans completed steps for cross-step consistency:

- **Quick Mode**: 2 checks (JTBD ↔ PR-FAQ, PR-FAQ ↔ North Star)
- **Full Mode**: 7 checks (all core decisions)
- **Revision Mode**: 4 checks (JTBD ↔ pain points ↔ positioning, etc.)
- **Build Mode**: 4 checks (problem ↔ PR-FAQ, solution ↔ MVP, etc.)
- **Feature Extension**: 3 checks (problem ↔ solution ↔ scope)
- **Custom Mode**: dynamic (only checks executed steps)

If inconsistencies found → lists issues, asks user to fix or proceed.

### Pipeline Audit Fixes
- 🔧 Feature Extension fully integrated as standalone mode (not variant)
- Mode names and emojis consistent across all files
- Feature Extension dependency graph added to change propagation
- Feature Extension progress template added
- Feature Extension context skip logic added
- Feature Extension trigger description in commands

Applied across all 6 languages + root references.

### Full Changelog
https://github.com/Kaminoikari/the-product-playbook/compare/v2.6.0...v2.6.1

---

## v2.6.2 — v2.6.2 — Decision Consistency Check + Pipeline Audit

*Published 2026-03-24 · commit `0fc71f1`*

### New: Decision Consistency Check (Mode-Specific)

Before generating final output, scans completed steps for cross-step consistency:

- **Quick Mode**: 2 checks (JTBD ↔ PR-FAQ, PR-FAQ ↔ North Star)
- **Full Mode**: 7 checks (all core decisions)
- **Revision Mode**: 4 checks (JTBD ↔ pain points ↔ positioning, etc.)
- **Build Mode**: 4 checks (problem ↔ PR-FAQ, solution ↔ MVP, etc.)
- **Feature Extension**: 3 checks (problem ↔ solution ↔ scope)
- **Custom Mode**: dynamic (only checks executed steps)

### Pipeline Audit Fixes
- 🔧 Feature Extension fully integrated as standalone mode (not variant)
- Mode names and emojis consistent across all files
- Feature Extension dependency graph added to change propagation
- Feature Extension progress template, context skip logic, trigger description added
- All cross-file references verified

Applied across all 6 languages + root references.

### Full Changelog
https://github.com/Kaminoikari/the-product-playbook/compare/v2.6.0...v2.6.2

---
