---
description: 產出開發交接包 — 生成 CLAUDE.md + TASKS.md + TICKETS.md + ARCHITECTURE.md + setup.sh，可直接在 Claude Code 中開始開發
---

請讀取 ~/.claude/skills/the-product-playbook/SKILL.md 及其 references/07-dev-handoff.md。

根據目前對話中已完成的產品規劃內容，依照 07-dev-handoff.md 的規格產出完整的開發交接包：
1. 確認技術棧（如使用者未指定，根據產品特性推薦）
2. 產出 CLAUDE.md（Claude Code 專案記憶）
3. 產出 TASKS.md（功能拆解 + Phase 分期 + 驗收標準）
4. 產出 TICKETS.md（開票清單：每張票含標題、描述、驗收標準、優先級、預估工時、依賴關係，PM 可直接在 Jira/Asana/Linear 開票）
5. 產出 docs/ARCHITECTURE.md（目錄結構 + DB Schema + API Endpoints）
6. 產出 docs/PRD.md + docs/PRODUCT-SPEC.md
7. 產出 scripts/setup.sh（一鍵初始化）
8. 顯示 Claude Code 銜接引導

如果對話中尚無產品規劃內容，提示使用者先執行產品規劃流程。
