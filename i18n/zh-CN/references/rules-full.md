# 📦 完整模式步骤序列（8 Core + 1 预设 ON + 2 Optional，共 9–11 步）

> 此文件为完整模式的权威步骤定义。由 SKILL.md 核心派发载入。

**从原本 20 步流程（v1.0.x）精简而来**：合并冗余框架，并将可选框架以触发条件控管。详见 `references/rules-optional-trigger.md` 取得触发逻辑与 Phase 决策点格式。

**关于 Journey Map（S3）**：预设 ON。Persona-Journey 是一个捆绑组合，无论产品是 0-to-1 还是既有产品 —— 真正相关的变量是使用者的 Job 是否横跨多个阶段。仅在情境真的过于简单时跳过（单一 API／按钮、流程 ≤2 步，或使用者明确要求跳过）。

## 步骤序列

```
Phase 0：Strategy
  S1.  Strategy Diagnosis  [Core]
       → references/00-opportunity-check.md + references/01-strategy.md
       （合并：机会评估 + DHM + Strategy Blocks + Rumelt 策略内核）

Phase 1：Discovery
  S2.  Persona（Table + 卡片）  [Core]
       → references/02a-persona.md
  S3.  User Journey Map  [预设 ON — 仅在情境过于简单时跳过]
       → references/02c-ost-journey.md
  S4.  JTBD 分析  [Core]
       → references/02b-jtbd.md

Phase 2：Define
  S5.  痛点 + HMW + 机会排序  [Core]
       → references/03-define.md
       （合并：痛点汇整表 + HMW + 机会评估表；
        OST 树状视觉化为本步骤内的可选子格式）
  S6.  April Dunford 定位  [Optional — 见触发条件]
       → references/03-define.md

Phase 3：Develop
  S7.  PR-FAQ（Working Backwards）  [Core]
       → references/04a-prfaq.md
  S8.  解法评估  [Core]
       → references/04b-solutions.md
       （合并：平行原型 + Pre-mortem + GEM + RICE）
  S9.  MVP + Not Doing List  [Core]
       → references/04c-mvp.md

Phase 4：Deliver
  S10. North Star + 三层讯号 + Aha Moment  [Core]
       → references/05a-northstar-aha.md
  S11. PMF + GTM + 商业模式 + 假设验证计划  [Optional — 见触发条件]
       → references/05b-pmf-gtm.md + references/05c-validation-spec.md

────
最终产出 → 产品规格摘要（references/05c-validation-spec.md → 4.6）+ 最佳切入点分析
```

> 当产出对象为高层或跨部门对齐时，于 S10 之前加入 Empowered Teams 框架。

## Optional 触发规则

阅读 `references/rules-optional-trigger.md` 取得权威的触发条件与 Phase 决策点输出格式。

**速查：**
- **S3 Journey Map**（预设 ON）：除非单一交互点／流程 ≤2 步／使用者要求跳过，否则执行
- **S6 Positioning**（预设 OFF）：触发条件 — 新产品上市／重新定位／产出对象包含 Sales-BD-行销
- **S11 PMF/GTM/BM/Validation**（预设 OFF）：触发条件 — 产品准备上市／产出对象为高层或数据科学家／使用者明确要求验证计划

## Phase 决策点要求

进入 Phase 1、Phase 2、Phase 4 之前，渲染 Phase 决策点区块（格式定义于 `rules-optional-trigger.md`）。Phase 0 与 Phase 3 仅含 Core 步骤，不需要决策点。

## Reference 载入指示

进入各步骤时，仅读取对应的 reference 文件（不要预先全部载入）：

| 步骤 | Reference 文件 |
|------|---------------|
| S1 | `references/00-opportunity-check.md` + `references/01-strategy.md` |
| S2 | `references/02a-persona.md` |
| S3（若触发） | `references/02c-ost-journey.md` |
| S4 | `references/02b-jtbd.md` |
| S5 | `references/03-define.md` |
| S6（若触发） | `references/03-define.md` |
| S7 | `references/04a-prfaq.md` |
| S8 | `references/04b-solutions.md` |
| S9 | `references/04c-mvp.md` |
| S10 | `references/05a-northstar-aha.md` |
| S11（若触发） | `references/05b-pmf-gtm.md` + `references/05c-validation-spec.md` |
| 最终产出 | `references/05c-validation-spec.md` |

## 步骤数总览

| 情境 | 步骤数 |
|----------|-------|
| 预设（8 Core + S3 Journey 启用） | **9** |
| 流程过于简单（S3 跳过） | 8 |
| 1 个预设 OFF 的 Optional 触发（S6 或 S11） | 10 |
| 全部 Optional 触发 | 11 |
|（旧版 20 步流程） | 20 |

## 最终产出格式

**最佳切入点分析**（完整逻辑链）＋ **产品规格摘要**。

产品规格摘要**必须**揭露本次跳过的 Optional 步骤，并提供单一指令补回的路径（依 `rules-optional-trigger.md` 第 6 节）。

完成后，依 `references/rules-end-of-flow.md` 执行流程结束规则。
