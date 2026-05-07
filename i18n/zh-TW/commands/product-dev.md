---
description: 產出開發交接包 — 生成 CLAUDE.md + TASKS.md + TICKETS.md + ARCHITECTURE.md + setup.sh，可直接在 Claude Code 中開始開發
---

觸發 product-playbook skill。
然後依序讀取以下 reference 檔：
1. `references/07a-handoff-core.md`（CLAUDE.md 模板 + 技術棧確認）
2. `references/07b-tasks-tickets.md`（TASKS.md + TICKETS.md 模板）
3. `references/07c-architecture-setup.md`（ARCHITECTURE.md + setup.sh + 使用者引導）

根據目前對話中已完成的產品規劃內容，產出完整的開發交接包：
1. 確認技術棧（如使用者未指定，根據產品特性推薦）
2. 在專案根目錄建立 `.product-dev-active` 標記檔（空檔即可），並將 `.product-dev-active` 寫入專案的 `.gitignore`（檔案不存在就新建，已存在就 append；不要重複加）。此檔向 plugin 的 PreToolUse hook 宣告專案已正式進入開發交接階段，後續寫入原始碼不再被 hook 攔截提醒。
3. 產出 CLAUDE.md（Claude Code 專案記憶）
4. 產出 TASKS.md（功能拆解 + Phase 分期 + 驗收標準）
5. 產出 TICKETS.md（開票清單）
6. 產出 docs/ARCHITECTURE.md（目錄結構 + DB Schema + API Endpoints）
7. 產出 docs/PRD.md + docs/PRODUCT-SPEC.md
8. 產出 scripts/setup.sh（一鍵初始化）
9. 顯示 Claude Code 銜接引導

如果對話中尚無產品規劃內容，提示使用者先執行產品規劃流程。

註：`.product-dev-active` 為 session-local 標記，不應被 commit — 步驟 2 已確保它列入專案自身的 `.gitignore`。若專案未來回到純規劃模式，刪除此標記檔即可。
