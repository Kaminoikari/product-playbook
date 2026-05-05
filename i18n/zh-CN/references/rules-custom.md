# ✏️ 自订模式步骤序列

> 此文件为自订模式的权威步骤定义。由 SKILL.md 核心派发载入。

请选择完整性等级（或自行挑选步骤）：

## 🔴 低（Lean）— 共 4 步

```
S1. JTBD 陈述 → references/02b-jtbd.md
S2. HMW 一个 → references/03-define.md
S3. PR-FAQ → references/04a-prfaq.md
S4. North Star → references/05a-northstar-aha.md
（任一步骤可由使用者替换为其他框架）
────
最终产出 → 产品规格摘要（未执行栏位标记「未执行」）
```

## 🟡 中（Standard）— 共 8 步（需要 Journey Map 时自动扩为 9 步）

> Full Mode 的 8 步子集：Full Core 去掉 Strategy Diagnosis、加入 Positioning。Standard 使用者通常比深度策略诊断更早需要市场定位，因此做此调整。
>
> **Persona-Journey 条件式插入**：完成 S1（Persona）后，AI 依 `rules-optional-trigger.md` 第 2 节执行 Persona-Journey 评估。若跳过条件**不**成立（亦即 Job 横跨多个阶段），AI **主动将 Journey Map 以 S1.5 插入**，本次执行变为 9 步。使用者可回复 `-journey` 还原为 8 步。若跳过条件成立（单一交互点／流程 ≤2 步），静默跳过并于最终产出揭露。

```
S1.   Persona（Table + 卡片）→ references/02a-persona.md
S1.5  User Journey Map [预设插入；仅在情境过于简单时跳过]
      → references/02c-ost-journey.md
S2.   JTBD 分析 → references/02b-jtbd.md
S3.   痛点 + HMW + 机会排序 → references/03-define.md
S4.   April Dunford 定位 → references/03-define.md
S5.   PR-FAQ → references/04a-prfaq.md
S6.   解法评估（平行原型 + Pre-mortem + GEM + RICE）→ references/04b-solutions.md
S7.   MVP + Not Doing List → references/04c-mvp.md
S8.   North Star + 三层讯号 + Aha Moment → references/05a-northstar-aha.md
```

## 🟢 高（Comprehensive）— 共 11 步

> Full Mode Core + 全部预设 OFF 的 Optional（Positioning + PMF/GTM/BM/Validation）。**S2 Persona 之后立刻接 S3 User Journey Map**，依 Persona-Journey 捆绑规则。若情境真的过于简单，可在 Persona 之后回复 `-S3` 跳过 Journey Map，还原为 10 步。

```
S1.  Strategy Diagnosis → references/00-opportunity-check.md + references/01-strategy.md
S2.  Persona（Table + 卡片）→ references/02a-persona.md
S3.  User Journey Map → references/02c-ost-journey.md   ← 与 S2 捆绑（预设 ON）
S4.  JTBD 分析 → references/02b-jtbd.md
S5.  痛点 + HMW + 机会排序 → references/03-define.md
S6.  April Dunford 定位 → references/03-define.md
S7.  PR-FAQ → references/04a-prfaq.md
S8.  解法评估（平行原型 + Pre-mortem + GEM + RICE）→ references/04b-solutions.md
S9.  MVP + Not Doing List → references/04c-mvp.md
S10. North Star + 三层讯号 + Aha Moment → references/05a-northstar-aha.md
S11. PMF + GTM + BM + 假设验证计划 → references/05b-pmf-gtm.md + references/05c-validation-spec.md
```

## Reference 载入规则

进入各步骤时，仅读取对应的 reference 文件（不要预先全部载入）。各步骤旁已标注对应的 reference 路径。

## Persona-Journey 捆绑

依 `references/rules-optional-trigger.md` 第 2 节与第 6 节，自订模式只要预设组包含 Persona 步骤，Journey Map 即**预设 ON**：

- **Comprehensive**：Journey Map 硬编码为 S3（已包含于上方序列）。使用者可在 Persona 之后回复 `-S3` 跳过。
- **Standard**：跳过条件不成立时（Job 横跨多阶段），Journey Map 自动以 **S1.5** 插入。情境过于简单时（单一交互点、流程 ≤2 步、使用者要求跳过），Journey Map 静默跳过，并于最终产出揭露。
- **Lean**：不含 Persona 步骤，此规则不适用。

跳过条件（任一成立 → 跳过 Journey）：
1. 单一交互点（API、单一按钮、后端服务、设定工具）
2. 流程仅有 1–2 步
3. 使用者明确要求跳过

## 最终产出格式

**产品规格摘要**（仅整合已完成的步骤，未执行的栏位标记为「未执行」）。

完成后，依 `references/rules-end-of-flow.md` 执行流程结束规则。
