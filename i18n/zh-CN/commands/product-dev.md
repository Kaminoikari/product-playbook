---
description: 产出开发交接包 — 生成 CLAUDE.md + TASKS.md + TICKETS.md + ARCHITECTURE.md + setup.sh，可直接在 Claude Code 中开始开发
---

请读取 ~/.claude/skills/product-playbook/SKILL.md。
然后依序读取以下 reference 档：
1. `references/07a-handoff-core.md`（CLAUDE.md 模板 + 技术栈确认）
2. `references/07b-tasks-tickets.md`（TASKS.md + TICKETS.md 模板）
3. `references/07c-architecture-setup.md`（ARCHITECTURE.md + setup.sh + 使用者引导）

根据目前对话中已完成的产品规划内容，产出完整的开发交接包：
1. 确认技术栈（如使用者未指定，根据产品特性推荐）
2. 产出 CLAUDE.md（Claude Code 专案记忆）
3. 产出 TASKS.md（功能拆解 + Phase 分期 + 验收标准）
4. 产出 TICKETS.md（开票清单）
5. 产出 docs/ARCHITECTURE.md（目录结构 + DB Schema + API Endpoints）
6. 产出 docs/PRD.md + docs/PRODUCT-SPEC.md
7. 产出 scripts/setup.sh（一键初始化）
8. 显示 Claude Code 衔接引导

如果对话中尚无产品规划内容，提示使用者先执行产品规划流程。
