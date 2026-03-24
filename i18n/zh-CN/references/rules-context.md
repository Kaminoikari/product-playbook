# 📦 产品上下文累积规则

> 此文件定义 `.product-context.md` 的格式、读写规则、情境处理和冲突解决。
> 由 SKILL.md 启动流程触发载入，或由各模式 S1 前置步骤载入。

## 1. 文件位置与生命周期

- **路径**：专案根目录下的 `.product-context.md`（与 `.product-playbook-progress.md` 同层）
- **永久保留**：此文件在流程结束后**不会被删除**，跨 session 持续累积
- **首次建立时**提醒使用者：「⚠️ 建议将 `.product-context.md` 加入 `.gitignore`，此文件可能包含敏感的产品策略资讯。」

---

## 2. 文件格式

```markdown
# Product Context
<!-- Auto-maintained by the-product-playbook. Do not delete. -->
<!-- last-updated: [ISO timestamp] -->

## Identity
- **Product name**: [name]
- **Product type**: [B2C / B2B / B2B2C / Internal tool]
- **One-liner**: [一句话描述]
- **Target audience**: [主要 Persona 摘要]

## Core Strategy
- **Core JTBD**: [Target Customer] + wants to [Job] + in [Context]
  - Functional: [...]
  - Emotional: [...]
  - Social: [...]
- **Positioning (April Dunford)**:
  - Real competitive alternatives: [...]
  - Unique attributes: [...]
  - Core value: [...]
  - Target market: [...]
  - Market category: [...]
- **North Star Metric**: [指标名 + 定义]
- **Aha Moment**: [描述]

## Architecture & Tech Stack
- **Tech stack**: [语言、框架、基础设施]
- **Key modules**: [主要模组清单]
- **Data model highlights**: [核心数据实体，若已知]

## Decision History
<!-- Append-only. 每次完成流程追加一笔。 -->

### [ISO date] - [流程类型: Full/Quick/Revision/Feature Extension/Custom/Build]
- **Scope**: [规划/变更范围]
- **Key decisions**: [重大决策]
- **Risks identified**: [风险]
- **MVP boundary**: [做什么 / 不做什么]
- **Success metrics**: [成功指标 + 目标值]

## Language Preference
- **Installed language**: [从 .lang 文件自动侦测或使用者的语系]
- **User's preferred language**: [使用者沟通时使用的语言]

## Accumulated Insights
- **Known pain points**: [痛点清单，附来源]
- **User feedback themes**: [跨 session 的反馈主题]
- **PMF status**: [最近评估等级 + 日期]
- **Security posture**: [认证/授权方式、已知漏洞]
- **Technical debt**: [跨 session 累积的技术债]
```

---

## 3. 三种情境侦测

启动时（进度文件检查之后、模式选择之前），侦测 `.product-context.md` 状态：

| 条件 | 情境 | 动作 |
|------|------|------|
| 文件存在，`Core Strategy` section 有实际内容（非空/非 placeholder） | **情境 1：完整上下文** | 静默载入。显示：「📦 侦测到 **[产品名]** 的产品上下文，将作为本次规划的基线。」 |
| 文件不存在 | **情境 2：无上下文** | 记录此状态。进入功能扩充或改版模式时触发 Context Bootstrap（见 Section 4） |
| 文件存在，`Core Strategy` 空白或仅有 placeholder，但 `Decision History` 有至少一笔纪录 | **情境 3：部分上下文** | 显示已知资讯摘要，提供补充选项（见 Section 5） |

**侦测逻辑**：
1. 文件是否存在？
2. `Identity` section 是否有 Product name（非 placeholder）？
3. `Core Strategy` section 是否有 Core JTBD（非 placeholder）？→ 有 = 情境 1
4. `Decision History` section 是否有任何 `###` 条目？→ 有但 3 为否 = 情境 3

---

## 4. Context Bootstrap（情境 2 专用）

当使用者进入**功能扩充**或**改版模式**但没有 `.product-context.md` 时，在模式 S1 之前插入「Step 0」。

**呈现方式**：
```
📦 这是你第一次在此专案使用产品规划工具。为了让后续流程更有效率，
我先收集一些基本产品资讯（约 2-3 分钟），之后会自动保存供未来使用。
```

### 渐进式收集（不要一次丢出所有问题）

**Round 1（所有模式必问）**：
- 产品叫什么名字？
- 一句话描述它做什么？
- 产品类型？（B2C / B2B / B2B2C / 内部工具）

**Round 2（功能扩充必问，改版选问）**：
- 使用什么技术栈？（语言、框架、数据库、基础设施）
- 主要模组或服务有哪些？

**Round 3（改版必问，功能扩充选问）**：
- 目前有 DAU/MAU 或留存率数据吗？
- 最常收到的用户反馈或投诉是什么？
- 有已知的安全问题或技术债吗？

### Tech Stack 自动侦测

除了使用者口述，Bootstrap 可**读取专案文件**辅助侦测（唯读，不违反 Hard Gate）：

| 文件 | 侦测内容 |
|------|---------|
| `package.json` | Node.js 生态系、框架、依赖 |
| `Cargo.toml` | Rust |
| `go.mod` | Go |
| `requirements.txt` / `pyproject.toml` | Python |
| `Dockerfile` / `docker-compose.yml` | 容器化架构 |
| 专案根目录结构（`src/`、`app/`、`lib/` 等） | 模组推断 |

侦测后以**确认式**呈现：
```
我侦测到你的专案使用：
- 技术栈：Next.js 14 + TypeScript + PostgreSQL + Redis
- 主要模组：auth/、billing/、dashboard/、api/
这些正确吗？有需要补充或修正的吗？
```

使用者确认后才写入 `.product-context.md`。

### Bootstrap 完成后

将收集到的资讯写入 `.product-context.md`，未收集的 section 留空（使用 placeholder），然后进入模式的正式 S1。

---

## 5. 部分上下文处理（情境 3）

当 `.product-context.md` 存在但 Core Strategy 为空、仅有 Decision History 时：

**呈现方式**：
```
📦 我有你之前 [N] 次规划的纪录：
- 技术栈：[从 Decision History 合并的已知 stack]
- 曾修改的模组：[从 Decision History 合并的 affected modules]
- 核心产品策略尚未记录。

你想要：
  1️⃣ 直接开始（使用已知资讯，策略部分跳过）
  2️⃣ 先补充策略资讯（JTBD、定位、北极星指标）
  3️⃣ 这些资讯有误，我来修正
```

**自动重建尝试**：扫描所有 Decision History 条目，从 `Affected modules`、`Scope`、`Key decisions` 中提取重复出现的产品名称、技术栈、模组名称，自动填入 `Architecture & Tech Stack`。以 `<!-- inferred from decision history -->` 标注推断来源。

---

## 6. Context Auto-Read 规则

各模式 S1 前置载入 context 时，**只注入相关 sections**，不要向使用者完整显示文件内容：

| 模式 + 步骤 | 注入的 Context Sections |
|-------------|------------------------|
| 功能扩充 S1 | Identity, Architecture & Tech Stack, 最近 3 笔 Decision History |
| 改版 S1 | Identity, Core Strategy, Accumulated Insights（痛点、PMF、安全）, 最近 3 笔 Decision History |
| 完整/Quick/Build S1 | Identity only（产品名、类型、一句话描述） |
| 任何模式的 Pre-mortem | Security posture + Technical debt（从 Accumulated Insights） |

**膨胀控制**：Decision History 默认只注入最近 3 笔。使用者可要求载入更多。

---

## 7. 空白 Sections 跳过规则

Context 文件存在但某些 sections 为空时，依**模式**决定是否可跳过或需收集：

| Section | 功能扩充 | 改版模式 | 完整/Quick/Build |
|---------|---------|---------|-----------------|
| Identity | 必要（无则 Bootstrap） | 必要（无则 Bootstrap） | 流程本身会产出，不需预载 |
| Core Strategy | **可跳过** | 必要（无则在 S1 内快问快答补收集） | 流程本身会产出 |
| Architecture & Tech Stack | 必要（无则 Bootstrap 或自动侦测） | 可跳过 | 流程本身会产出 |
| Decision History | 可跳过 | 有则带入，无则跳过 | 流程本身会产出 |
| Accumulated Insights | 可跳过 | 有则带入，无则跳过 | 流程本身会产出 |

| 功能扩充模式 | Identity（仅确认）、Architecture & Tech Stack（必要）、Core Strategy（可跳过） |

**原则**：空白 section **不阻挡流程**。只有对当前模式「必要」且为空的 section 才触发收集。

---

## 8. Context Auto-Write 规则（流程结束时萃取）

流程结束时（与 `rules-end-of-flow.md` 的结束条件检查同步），自动萃取 context：

| 流程类型 | 写入/更新的 Sections |
|---------|---------------------|
| Quick | Identity, Core Strategy（JTBD + North Star）, 追加 Decision History |
| Full | **全部 sections**（覆写 Identity/Strategy/Insights，追加 History） |
| Revision | 更新 Core Strategy（若有重新定位）, 更新 Insights, 追加 History |
| Feature Extension | 合并 Architecture, 追加 Decision History（功能专用模板） |
| Custom | 更新对应已完成步骤的 sections |
| Build（7 步） | Identity, Core Strategy（部分）, 追加 History |

### 写入策略

| Section | 策略 | 说明 |
|---------|------|------|
| Identity | **最新覆写** | 每次都用最新流程的数据覆写 |
| Core Strategy | **最新覆写** | 同上。改版后的策略取代改版前的 |
| Architecture & Tech Stack | **合并** | 新增模组不删除旧的。新技术项目追加 |
| Decision History | **仅追加** | 永远不删除先前纪录。每次完成流程追加一笔 |
| Accumulated Insights | **合并去重** | 痛点、反馈主题去重追加。PMF、Security 覆写为最新值 |

### Decision History 追加模板

**通用模板**：
```markdown
### [ISO date] - [流程类型]
- **Scope**: [...]
- **Key decisions**: [...]
- **Risks identified**: [...]
- **MVP boundary**: [...]
- **Success metrics**: [...]
```

**功能扩充专用模板**：
```markdown
### [ISO date] - Feature Extension: [功能名称]
- **Problem**: [一句话问题陈述]
- **Chosen solution**: [选定方案 + 理由]
- **Affected modules**: [影响的模组]
- **Scope**: [做什么 / 不动什么]
- **Acceptance criteria**: [验收标准]
```

### 完成后通知

```
✅ 产品上下文已更新至 `.product-context.md`，下次规划时将自动载入。
```

---

## 9. 冲突处理

### 使用者修正既有 context

完全允许。使用者提供的修正直接覆写对应 section（latest wins）。

### 使用者提供的数据与代码不一致

当 S1 前置同时读取了 `.product-context.md` 和专案文件（如 `package.json`），发现两者不一致时：

```
⚠️ 侦测到资讯不一致：
- Context 记录：[context 中的值]
- 专案代码：[代码中侦测到的值]
请确认哪个是正确的？
  1️⃣ 以代码为准（更新 context）
  2️⃣ 以 context 为准（可能正在迁移中）
  3️⃣ 两者都不完整，我来说明
```

**处理原则**：
- **不自动覆写**，由使用者裁决
- 使用者选择后更新 `.product-context.md`
- 若选「正在迁移」，在 Architecture section 标注：`[迁移中] React → Vue 3`
- 冲突纪录写入 Decision History

### 流程中的新数据覆盖 context

若流程中产出的数据与 context 中的旧数据不同（例如改版模式重新定义了 JTBD），**流程数据优先**。流程结束时自动覆写。

---

## 10. 语言偏好

当 `.product-context.md` 被创建或更新时，将语言偏好记录到 `Language Preference` section：

- **Installed language**：从 skill 安装目录的 `.lang` 文件侦测，或从使用者的语系设置获取。
- **User's preferred language**：使用者在 session 中沟通所使用的语言。

**载入规则**：载入已有的 `.product-context.md` 时，若已记录语言偏好，则以该语言继续 session。

**写入时机**：语言偏好在 Context Bootstrap（Section 4）时写入，或在首次创建 context 文件的流程结束时写入。当使用者在 session 中明确切换语言时，会同步更新。
