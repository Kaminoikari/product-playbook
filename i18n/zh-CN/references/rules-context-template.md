# 📦 产品上下文 —— 模板与详细 UX 脚本

> Lazy-loaded reference。依 `rules-context.md` §8 的触发表载入。仅包含日常 session 启动用不到的冗长 YAML/Markdown 格式与 UX 脚本。

## 文件格式

```markdown
# Product Context
<!-- Auto-maintained by product-playbook. Do not delete. -->
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

## Bootstrap（仅情境 2）

当使用者进入**功能扩充**或**改版模式**但没有 `.product-context.md` 时，在 S1 之前插入「Step 0」。

**呈现方式：**
```
📦 这是你第一次在此专案使用产品规划工具。为了让后续流程更有效率，
我先收集一些基本产品资讯（约 2-3 分钟），之后会自动保存供未来使用。
```

### 渐进式收集（不要一次丢出所有问题）

**Round 1（所有模式必问）：**
- 产品叫什么名字？
- 一句话描述它做什么？
- 产品类型？（B2C / B2B / B2B2C / 内部工具）

**Round 2（功能扩充必问，改版选问）：**
- 使用什么技术栈？（语言、框架、数据库、基础设施）
- 主要模组或服务有哪些？

**Round 3（改版必问，功能扩充选问）：**
- 目前有 DAU/MAU 或留存率数据吗？
- 最常收到的用户反馈或投诉是什么？
- 有已知的安全问题或技术债吗？

### Tech Stack 自动侦测

Bootstrap 可读取专案文件（唯读，不违反 Hard Gate）：

| 文件 | 侦测内容 |
|------|---------|
| `package.json` | Node.js 生态系、框架、依赖 |
| `Cargo.toml` | Rust |
| `go.mod` | Go |
| `requirements.txt` / `pyproject.toml` | Python |
| `Dockerfile` / `docker-compose.yml` | 容器化架构 |
| 专案根目录结构（`src/`、`app/`、`lib/` 等） | 模组推断 |

确认方式：
```
我侦测到你的专案使用：
- 技术栈：Next.js 14 + TypeScript + PostgreSQL + Redis
- 主要模组：auth/、billing/、dashboard/、api/
这些正确吗？有需要补充或修正的吗？
```

使用者确认后才写入。

### Bootstrap → S1 顺序（Hard Gate —— Bootstrap 不阻塞流程）

- **预设**：Bootstrap 与 S1 必须在**同一回合**内依序执行（S0 → S1），暂停点固定发生在 **S1 完成后**，不在 S0/S1 之间。
- **若使用者讯息已提供必要栏位** → 以表格确认，直接进入 S1。
- **若栏位缺失** → 在同一回合内以表格列出已知/待补栏位，进入 S1 使用 placeholder，把待补栏位折入 S1 确认问题。
- **禁止**：在 S0 与 S1 之间暂停等待 Round 1 答案。若 S1 仍是 `⬜ pending` 而流程已停下等待使用者输入，视同未通过本规则。

Bootstrap 完成后：写入 `.product-context.md`（即使有 placeholder），然后在同一回合内进入 S1。

---

## 部分上下文 UX（情境 3）

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

**自动重建尝试**：扫描 Decision History，从 `Affected modules`、`Scope`、`Key decisions` 中提取重复出现的产品名称、技术栈、模组名称，自动填入 `Architecture & Tech Stack`。以 `<!-- inferred from decision history -->` 标注。

---

## 追加模板

**通用模板：**
```markdown
### [ISO date] - [流程类型]
- **Scope**: [...]
- **Key decisions**: [...]
- **Risks identified**: [...]
- **MVP boundary**: [...]
- **Success metrics**: [...]
```

**功能扩充专用模板：**
```markdown
### [ISO date] - Feature Extension: [功能名称]
- **Problem**: [一句话问题陈述]
- **Chosen solution**: [选定方案 + 理由]
- **Affected modules**: [影响的模组]
- **Scope**: [做什么 / 不动什么]
- **Acceptance criteria**: [验收标准]
```

---

## 冲突 UX（代码 vs context）

```
⚠️ 侦测到资讯不一致：
- Context 记录：[context 中的值]
- 专案代码：[代码中侦测到的值]
请确认哪个是正确的？
  1️⃣ 以代码为准（更新 context）
  2️⃣ 以 context 为准（可能正在迁移中）
  3️⃣ 两者都不完整，我来说明
```

- 不自动覆写——由使用者裁决
- 若选「正在迁移」：在 Architecture 标注 `[迁移中] React → Vue 3`
- 冲突纪录写入 Decision History
