---
description: 產出 HTML 企劃報告 — 將所有產品規劃內容整合為單一可離線閱讀的 HTML 報告
---

請讀取 ~/.claude/skills/product-playbook/SKILL.md 及其 references/06-html-report.md。

根據目前對話中已完成的產品規劃內容，依照 06-html-report.md 的設計規範產出完整的 HTML 企劃報告：
- 單一 HTML 檔案（CSS + JS 內嵌，Google Fonts CDN 載入 Noto Sans TC）
- 依已完成的階段動態呈現，未完成的階段直接跳過
- 包含 Sticky 目錄導航、卡片式排版、互動效果

如果對話中尚無產品規劃內容，提示使用者先執行產品規劃流程。
