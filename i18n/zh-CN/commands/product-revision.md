---
description: 改版模式产品规划 — 针对既有产品改版优化，有用户数据和功能基础
argument-hint: <产品名称与改版目标>
---

触发 product-playbook skill。
然后读取 references/rules-revision.md 取得步骤序列。
执行各步骤时，依 rules-revision.md 中的 Reference 载入指示读取对应的 reference 档。

执行模式：🔄 改版模式
产品描述：$ARGUMENTS

依照 rules-revision.md 的步骤序列(S1 → S8,Optional 步骤由 rules-optional-trigger.md 中的触发条件决定是否执行)执行。S1 会主动询问既有产品数据(DAU/MAU、留存率、主要用户反馈等)。在含 Optional 步骤的 phase 开始前输出 Phase 决策点,每步骤显示进度指示器。
