---
description: 功能扩展模式 — 在现有产品上新增单一功能，4 步精简流程
argument-hint: <功能描述>
---

触发 product-playbook skill。
然后读取 references/rules-build.md，直接跳到「🔧 Feature Extension Quick Path」段落。
执行各步骤时，依该段落中的 Reference 载入指示读取对应的 reference 档。

执行模式：🔧 功能扩展模式
功能描述：$ARGUMENTS

依照 Feature Extension 步骤序列（S1 → S4）执行。先依 rules-context.md 载入产品上下文。每步骤显示进度指示器。

**S0 → S1 顺序（重要）**：若 Context Bootstrap（S0）因 `.product-context.md` 不存在而触发，必须在**同一回合**内完成 Bootstrap 与 S1，然后**在 S1 完成后**暂停等待使用者确认进入 S2。**不要**在 S0 与 S1 之间暂停——即使部分 Bootstrap 栏位仍缺失，也要先以 placeholder 写入 baseline `.product-context.md`、进入 S1、并把缺失栏位作为 S1 confirmation question 的一部分询问。详见 `references/rules-context.md`「Bootstrap 与 S1 的顺序」。
