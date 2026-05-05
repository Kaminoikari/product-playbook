# 🔵 Optional 步骤触发规则

> Optional 步骤触发条件与 Phase 决策点格式的权威来源。由 Full / Revision / Custom 模式规则档载入。

此文件集中管理 Optional 步骤的触发条件，避免各模式规则档重复定义。

---

## 1. Core 与 Optional 的定义

- **Core（核心）**：必定执行。除非使用者明确覆写，否则不可跳过。
- **Optional（可选）**：仅当至少一个触发条件成立时才执行。使用者随时可以强制加入或强制跳过。

---

## 2. Persona-Journey 捆绑规则（全局）

**Journey Map 是 Persona 的自然延伸：Persona 定义「谁」，Journey Map 描述「谁」经历的旅程。完成 Persona 步骤后，Journey Map 预设启用，仅在情境真的过于简单、无法画出旅程时才跳过。**

> ⚠️ 此规则修正了过去「0-to-1 不需要 Journey Map」的错误假设。事实正好相反 —— Teresa Torres（Continuous Discovery）、Indi Young（Mental Models）以及 Amazon Working Backwards 流程，都把 Journey Map 视为 0-to-1 阶段的必要工具，因为它形塑了新体验的设计方式。真正相关的变量是**使用者的 Job 是否横跨多个阶段**，而不是产品是否已经存在。

### 跳过条件（预设 ON；任一成立才跳过）

1. **单一交互点** —— Job 是由单一 API 呼叫、单一按钮、纯后端服务或纯设定工具完成（不存在多阶段流程）
2. **流程仅有 1–2 步** —— 整段使用者流程过短，画 Journey Map 会退化成一份没有阶段转折的清单
3. **使用者明确要求跳过** —— 例如「skip Journey Map」「我不需要 Journey Map」

### 跳过时的行为

向使用者揭露此决策，不要静默跳过：

> 「Persona 已完成。基于目前情境（单一交互点／流程仅有 N 步），将跳过 Journey Map。你随时可以回复『add journey』把它补回。」

### 触发时的行为（预设）

进入 Journey Map 步骤前，先输出一段简短的评估说明，引用**为什么**需要它：

> 「Persona 已完成。Job 横跨 [N] 个阶段（[阶段 A → 阶段 B → ...]）—— 进入 User Journey Map。若不需要请回复『-S3』跳过。」

---

## 3. Optional 触发条件 — Full Mode

| 步骤 | 框架 | 预设 | 逻辑 |
|------|-----------|---------|-------|
| S3 | User Journey Map | **ON** | 见上方第 2 节 Persona-Journey 规则。仅在单一交互点／流程 ≤2 步／使用者明确要求跳过时才跳过 |
| S6 | April Dunford 定位 | OFF | 触发条件：(a) 新产品上市 或 (b) 重新定位 或 (c) 产出对象包含 Sales／BD／行销 |
| S11 | PMF + GTM + 商业模式 + 假设验证计划 | OFF | 触发条件：(a) 产品准备上市 或 (b) 产出对象为高层／数据科学家 或 (c) 使用者明确要求验证计划 |

---

## 4. Optional 触发条件 — Revision Mode

| 步骤 | 框架 | 触发条件（任一成立即触发） |
|------|-----------|------------------------------|
| S4 | Positioning 重新评估 | 使用者提到「定位飘移」／「市场变了」 或 产出对象包含 Sales／行销 |
| S6 | Pre-mortem | (a) 改版范围 ≥30% 既有功能 或 (b) 涉及金流／权限／数据迁移 |

---

## 5. Phase 决策点输出格式

**进入每个含有 Optional 步骤的 Phase 之前，AI 必须输出一个 Phase 决策点区块，列出哪些 Core／Optional 步骤会执行以及原因。**

### 必要格式

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔀 Phase [N] 步骤决策

✅ Core（必定执行）：S[a]、S[b]
🔵 Optional 评估：
  • S[x] [框架名称]（预设 ON）： [执行 / 跳过] — [理由]
  • S[y] [框架名称]（预设 OFF）：[触发 / 跳过] — [理由]

→ 本 Phase 将执行 [N] 个步骤
（回复「+S[x]」可强制加入，「-S[y]」可强制跳过，或直接继续）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

预设 ON 的步骤（例如 S3 Journey Map），条件成立时使用 **执行**，触发任一跳过条件时使用 **跳过**。
预设 OFF 的步骤（例如 S6 Positioning、S11 PMF/GTM），条件成立时使用 **触发**，否则使用 **跳过**。

### 何时呈现

- 进入每一个**至少包含一个 Optional 步骤**的 Phase 时，于开头呈现一次
- 仅有 Core 步骤的 Phase 不需要决策点（直接进入即可）
- 呈现后等待使用者回应。非覆写式回应（例如「ok」「继续」或具体内容）视为「接受 AI 的判定」

### 使用者覆写指令

| 使用者输入 | 行为 |
|------------|----------|
| `+S[x]` 或「加入 S[x]」 | 强制加入原本被跳过的 Optional 步骤 |
| `-S[y]` 或「跳过 S[y]」 | 强制跳过原本被触发的 Optional 步骤 |
| 具体内容／「继续」／Enter | 接受 AI 的评估，继续进行 |

---

## 6. Custom Mode — Persona-Journey 条件式插入

Custom Mode 的预设组（Lean / Standard / Comprehensive）有固定的步骤序列，但只要预设组包含 Persona 步骤，Persona-Journey 捆绑规则一样适用。

| 预设组 | 预设行为 | Persona 步骤之后的行为 |
|--------|------------------|----------------------------|
| **Lean** | 不含 Persona 步骤 | 不适用 |
| **Standard** | 8 步固定序列，S1 = Persona | S1 之后，AI 依第 2 节执行 Persona-Journey 评估。若跳过条件**不**成立，AI 主动将 Journey Map 以 **S1.5（成为 9 步流程）** 插入，使用者可回复 `-journey` 还原。若跳过条件成立，静默跳过并于最终产出揭露（第 7 节）。 |
| **Comprehensive** | 11 步固定序列，S2 = Persona、S3 = Journey Map（已包含） | AI 可输出简短「可跳过」提示：「Journey Map 预设启用。若情境过于简单，请回复 `-S3`。」否则正常进行。 |

这样可避免在情境真的简单时打断 Lean／Standard 使用者，同时确保会因 Journey Map 受益的使用者不会被静默拒绝。

---

## 7. 最终产出揭露

模式结束时，最终的产品规格摘要**必须**列出本次跳过了哪些 Optional 步骤，并提供单一指令补回的路径，例如：

> 「本次跳过的 Optional 步骤：S6（Positioning）、S11（PMF/GTM）。回复『add S6』或『add S11』即可补上。」
