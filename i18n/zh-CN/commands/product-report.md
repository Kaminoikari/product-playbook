---
description: 产出 HTML 企划报告 — 将所有产品规划内容整合为单一可离线阅读的 HTML 报告
---

请读取 ~/.claude/skills/product-playbook/SKILL.md 及其 references/06-html-report.md。

根据目前对话中已完成的产品规划内容，依照 06-html-report.md 的设计规范产出完整的 HTML 企划报告：
- 单一 HTML 文件（CSS + JS 内嵌，Google Fonts CDN 载入 Noto Sans TC）
- 依已完成的阶段动态呈现，未完成的阶段直接跳过
- 包含 Sticky 目录导航、卡片式排版、互动效果

如果对话中尚无产品规划内容，提示使用者先执行产品规划流程。
