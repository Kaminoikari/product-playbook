# 🔄 改版模式步骤序列（6 Core + 2 Optional，共 6–8 步）

> 此文件为改版模式的权威步骤定义。由 SKILL.md 核心派发载入。

**从原本 12 步流程（v1.0.x）精简而来**：合并冗余框架，并将可选框架以触发条件控管。详见 `references/rules-optional-trigger.md` 取得触发逻辑与 Phase 决策点格式。

## 步骤序列

```
Phase 0：现况分析
  S1.  现况回顾 + JTBD 重新检验  [Core]
       （合并：数据盘点 + 既有 Job 哪些做得好／不好）

Phase 1：问题收敛
  S2.  用户痛点收集  [Core]
       （留存／流失分析 + 用户反馈汇整 + 行为数据）
  S3.  痛点 + HMW + 机会排序  [Core]
       → references/03-define.md
       （合并：痛点汇整表 + HMW + 机会评估表）
  S4.  Positioning 重新评估  [Optional — 见触发条件]
       → references/03-define.md

Phase 2：解法设计
  S5.  PR-FAQ（描述改版后的体验）  [Core]
       → references/04a-prfaq.md
  S6.  Pre-mortem  [Optional — 见触发条件]
       → references/04b-solutions.md
  S7.  MVP + Not Doing List  [Core]
       → references/04c-mvp.md

Phase 3：验证
  S8.  North Star + Aha（改版前后对照）+ 假设验证计划  [Core]
       → references/05a-northstar-aha.md + references/05c-validation-spec.md
       （合并：任何改版都必须验证假设；两者紧密耦合）

────
最终产出 → 产品规格摘要（改版版）
```

### S1 前置：产品上下文载入

进入 S1 前，读取 `references/rules-context.md` 并检查 `.product-context.md`：

- **有完整上下文（情境 1）**：自动带入 PMF 等级、North Star、已知痛点、安全现况、近 3 笔 Decision History。S1 引导改为**差异式**：「上次评估时，你的 PMF 等级为 [X]，北极星指标为 [Y]。目前这些有变化吗？最新的 DAU/MAU 和留存率是多少？」— 已有的历史决策和已知痛点不需要重新收集。
- **无上下文（情境 2）**：触发 Context Bootstrap（`rules-context.md` Section 4，Round 1 + 3），完成后再进入下方标准 S1 数据收集。
- **部分上下文（情境 3）**：从 Decision History 带入功能变更历史（知道哪些模组被改过、有哪些风险被识别过），但需询问整体产品策略和指标（之前只做过功能扩充，缺全局视角）。

### S1 标准引导

> 改版模式的 S1 会主动询问使用者提供既有产品数据：DAU/MAU、留存率、主要用户反馈、过去版本的关键决策等。若 context 已预填部分答案，改为确认而非重新收集。
> S1 同时收集安全现况：现有认证／授权机制、已知安全漏洞或技术债、近期安全事件。这些资讯会影响改版的风险评估和 Pre-mortem（若触发）。

### 快速路径

当使用者在 S1 已提供充分数据（含用户反馈、指标、痛点），S3 可在单次对话中产出，而非多次确认。触发条件：S2 收集到的痛点清单已有明确的优先级和数据支持。Hard Gate 规则不变 — 每个步骤的产出仍须完整呈现，只是确认节奏加快。

## Optional 触发规则

阅读 `references/rules-optional-trigger.md` 取得权威的触发条件与 Phase 决策点输出格式。

**速查：**
- **S4 Positioning 重新评估** 触发条件：使用者提到「定位飘移」／「市场变了」／产出对象包含 Sales／行销
- **S6 Pre-mortem** 触发条件：改版范围 ≥30% 既有功能／涉及金流-权限-数据迁移

## Phase 决策点要求

进入 Phase 1 与 Phase 2 之前，渲染 Phase 决策点区块（格式定义于 `rules-optional-trigger.md`）。Phase 0 与 Phase 3 仅含 Core 步骤，不需要决策点。

## Reference 载入指示

| 步骤 | Reference 文件 |
|------|---------------|
| S1–S2 | （无需外部 reference；直接收集使用者数据） |
| S3 | `references/03-define.md` |
| S4（若触发） | `references/03-define.md` |
| S5 | `references/04a-prfaq.md` |
| S6（若触发） | `references/04b-solutions.md` |
| S7 | `references/04c-mvp.md` |
| S8 + 最终产出 | `references/05a-northstar-aha.md` + `references/05c-validation-spec.md` |

## 步骤数总览

| 情境 | 步骤数 |
|----------|-------|
| 预设（仅 Core） | **6** |
| 全部 Optional 触发 | 8 |
|（旧版 12 步流程） | 12 |

## 最终产出格式

**改版产品规格摘要**：改版前后对照 + 改什么／不改什么 + 成功指标。

摘要**必须**揭露本次跳过的 Optional 步骤，并提供单一指令补回的路径（依 `rules-optional-trigger.md` 第 6 节）。

完成后，依 `references/rules-end-of-flow.md` 执行流程结束规则。
