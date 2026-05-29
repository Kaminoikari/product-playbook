# 📦 产品上下文累积规则

> 由 SKILL.md 启动流程载入。包含所有决策逻辑（何时/哪些/如何）。冗长的 YAML 格式与完整 UX 脚本位于 `rules-context-template.md`（仅在实际写入文件或执行 Bootstrap 时才 lazy-load）。

## 1. 文件生命周期

- **路径**：专案根目录下的 `.product-context.md`（与 `.product-playbook-progress.md` 同层）
- **永久保留**：跨 session 持续累积
- **首次建立时**：提醒使用者加入 `.gitignore`（可能包含敏感策略资讯）

**Bootstrap 启动公告（Hard Gate —— 在收集任何资讯之前必须执行）：** Bootstrap 面向使用者的第一则讯息「必须」同时说明 (a) 所撷取的资讯将被保存以供未来 session 使用，以及 (b) 确切路径 `.product-context.md`。范例措辞：

> 正在为未来的 session 设置产品上下文 —— 我会把我们撷取到的内容保存到专案根目录的 `.product-context.md`，让后续执行能跳过重新询问基本资讯。

此为不可妥协的要求：若 Bootstrap 的文件写入稍后撞上权限闸门或被中断，使用者仍必须在事前就已被告知路径。只在完成时才提及路径（「✅ 已保存至 .product-context.md」）会在「完成」永远不发生时失败。

---

## 2. 三种情境侦测（启动时）

进度文件检查之后、模式选择之前：

| 条件 | 情境 | 动作 |
|------|------|------|
| 文件存在，`Core Strategy` 有实际内容 | **1. 完整** | 静默载入。显示：「📦 侦测到 **[产品名]** 的产品上下文，将作为本次规划的基线。」 |
| 文件不存在 | **2. 无** | 记录状态。进入功能扩充/改版时触发 Bootstrap。→ 载入 template §Bootstrap |
| 文件存在，Core Strategy 空白/placeholder，Decision History 有 ≥1 笔 | **3. 部分** | 显示已知资讯摘要 + 补充选项。→ 载入 template §Partial |

**侦测逻辑：**
1. 文件存在？
2. `Identity` 有 Product name（非 placeholder）？
3. `Core Strategy` 有 Core JTBD（非 placeholder）？→ 是 = 情境 1
4. `Decision History` 有任何 `###` 条目？→ 是但 3 否 = 情境 3

---

## 3. Auto-Read 规则（各模式 S1 前置）

**只注入相关 sections** —— 不向使用者显示完整文件：

| 模式 + 步骤 | 注入 Sections |
|-------------|--------------|
| 功能扩充 S1 | Identity、Architecture & Tech Stack、最近 3 笔 Decision History |
| 改版 S1 | Identity、Core Strategy、Accumulated Insights（痛点、PMF、安全）、最近 3 笔 Decision History |
| 完整/Quick/Build S1 | Identity only（产品名、类型、一句话） |
| 任何模式的 Pre-mortem | Security posture + Technical debt（来自 Accumulated Insights） |

**膨胀控制**：Decision History 默认只注入最近 3 笔。使用者可要求更多。

---

## 4. 空白 Sections 跳过规则

| Section | 功能扩充 | 改版 | 完整/Quick/Build |
|---------|---------|------|-----------------|
| Identity | 必要（无则 Bootstrap） | 必要（无则 Bootstrap） | 流程会产出 |
| Core Strategy | 可跳过 | 必要（无则 S1 内快问快答补） | 流程会产出 |
| Architecture & Tech Stack | 必要（无则 Bootstrap 或自动侦测） | 可跳过 | 流程会产出 |
| Decision History | 可跳过 | 有则带入，无则跳过 | 流程会产出 |
| Accumulated Insights | 可跳过 | 有则带入，无则跳过 | 流程会产出 |

**原则**：空白 section 不阻挡流程。只有「必要」+ 空白才触发收集。

---

## 5. Auto-Write 规则（流程结束时）

与 `rules-end-of-flow.md` 的结束条件同步。自动萃取 context：

| 流程类型 | 写入/更新 Sections |
|---------|-------------------|
| Quick | Identity、Core Strategy（JTBD + North Star），追加 History |
| Full | 全部 sections（覆写 Identity/Strategy/Insights，追加 History） |
| Revision | 更新 Core Strategy（若有重新定位），更新 Insights，追加 History |
| Feature Extension | 合并 Architecture，追加 History（feature 模板） |
| Custom | 更新对应已完成步骤的 sections |
| Build | Identity、Core Strategy（部分），追加 History |

### 各 Section 写入策略

| Section | 策略 |
|---------|------|
| Identity | 最新覆写 |
| Core Strategy | 最新覆写（改版后取代改版前） |
| Architecture & Tech Stack | 合并（新模组追加，旧模组保留） |
| Decision History | 仅追加（永不删除先前纪录） |
| Accumulated Insights | 合并去重（痛点/反馈去重；PMF/Security 覆写） |

首次写入（建立文件）或追加 Decision History → **载入 `rules-context-template.md` §File Format / §Append Templates**。

完成时显示：`✅ 产品上下文已更新至 '.product-context.md'，下次规划时将自动载入。`

---

## 6. 冲突处理（摘要）

| 冲突类型 | 解决方式 |
|---------|---------|
| 使用者修正既有 context | 最新胜出——直接覆写 |
| Context 与代码不一致（例如 package.json） | 不自动覆写——询问使用者。→ 载入 template §Conflict UX |
| 流程数据与旧 context 不同 | 流程数据胜出——流程结束时自动覆写 |

---

## 7. 语言偏好（摘要）

Context 建立/更新时记录到 `Language Preference` section：
- **Installed language**：从 `.lang` 文件或使用者语系
- **User's preferred language**：使用者沟通使用的语言

载入时：若已记录，以该语言继续 session。
写入时机：Bootstrap 或首次创建 context 文件的流程结束时。使用者中途切换语言时同步更新。

---

## 8. 何时载入 `rules-context-template.md`

仅当以下任一触发条件成立时：

| 触发条件 | Template section |
|---------|------------------|
| 情境 2 + 进入功能扩充/改版 | §Bootstrap、§File Format |
| 情境 3（部分上下文） | §Partial Context、§File Format |
| 首次写入 context | §File Format |
| 流程结束时追加 Decision History | §Append Templates |
| 侦测到代码冲突 | §Conflict UX |
| Bootstrap 完成 → 写入 baseline | §File Format |

启动时**不要**预载 template。