---
description: 產出開發交接包 — 生成 CLAUDE.md + TASKS.md + TICKETS.md + ARCHITECTURE.md + setup.sh，可直接在 Claude Code 中開始開發
---

請讀取 ~/.claude/skills/product-playbook/SKILL.md。
然後依序讀取以下 reference 檔：
1. `references/07a-handoff-core.md`（CLAUDE.md 模板 + 技術棧確認）
2. `references/07b-tasks-tickets.md`（TASKS.md + TICKETS.md 模板）
3. `references/07c-architecture-setup.md`（ARCHITECTURE.md + setup.sh + 使用者引導）

根據目前對話中已完成的產品規劃內容，產出完整的開發交接包：
1. 確認技術棧（如使用者未指定，根據產品特性推薦）
2. 產出 CLAUDE.md（Claude Code 專案記憶）
3. 產出 TASKS.md（功能拆解 + Phase 分期 + 驗收標準）
4. 產出 TICKETS.md（開票清單）
5. 產出 docs/ARCHITECTURE.md（目錄結構 + DB Schema + API Endpoints）
6. 產出 docs/PRD.md + docs/PRODUCT-SPEC.md
7. 產出 scripts/setup.sh（一鍵初始化）
8. 顯示 Claude Code 銜接引導

如果對話中尚無產品規劃內容，提示使用者先執行產品規劃流程。
