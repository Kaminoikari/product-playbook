# Sub-Agents 整合指南

這份文件說明如何把三個新的 sub-agent 整合進 The Product Playbook plugin，讓 main agent 在對的時機自動 delegate。

---

## 交付清單

```
agents/
├── discovery-specialist.md      # Persona / JTBD / OST / Journey Map 專家
├── strategy-critic.md           # Rumelt 視角的策略批判者
└── pre-mortem-runner.md         # 15+ failure scenarios + leading indicators
```

每個 agent 都遵守：

- YAML frontmatter（name, description, tools, model: inherit）
- description 用 PROACTIVELY 觸發 main agent 的 auto-delegate
- 嚴格的 scope refusal（out_of_scope 路由）
- Structured YAML output（main agent 容易 parse）
- 多語言（reply in orchestrator's language）
- 繼承 Hard Gate（不寫 code、不建檔）

---

## 整合步驟

### Step 1：拷貝檔案到 repo

```bash
cd /path/to/product-playbook
cp /path/to/downloaded/agents/*.md ./agents/
```

`agents/` 目錄在 plugin root（跟 `commands/`、`skills/`、`SKILL.md` 同層）。Claude Code 安裝 plugin 時會自動載入這個目錄裡的所有 `.md` 檔。

### Step 2：在 SKILL.md 加入 delegation rules

Main agent 要知道何時 delegate，必須在 SKILL.md 加一個新 section。建議插入位置：在現有的 `## 🚦 Mode Dispatcher` 之後、`## Startup Flow` 之前。具體 patch 看下方 `## SKILL.md Patch` 區塊。

### Step 3：更新 i18n 版本

Main agent 偵測到非英文時會 silently 切換到 `i18n/zh-TW/SKILL.md` 等檔案。這六個 i18n SKILL.md 也需要同步加入 delegation rules。建議做法：先在英文版定稿，跑通整個流程，再翻譯到其他語言。

Sub-agent 檔案本身**不需要** i18n 翻譯 — 它們在 system prompt 裡已經 instruct 自己 reply in orchestrator's language。一份英文 sub-agent 服務六種語言。

### Step 4：更新 evals

你的 `evals/` 已經有「With Skill vs Without Skill」對比。建議新增第三組對比：「With Skill + Sub-Agents vs With Skill only」。預期看到的差距：

- Discovery 步驟的 JTBD 深度（functional / emotional / social 三層完整度）
- Strategy 步驟的 Rumelt kernel 評分嚴格度
- Pre-mortem 的 leading indicator 具體度跟 scenario 多樣性

如果這三項分數明顯提升，這就是 plugin L3 升級的量化證據，可以寫進 README 的 benchmark 章節。

### Step 5：更新 README

在 README 的 `## ✨ What Is This?` 區塊加一行：

> 🤝 **3 specialist sub-agents** — Discovery, Strategy Critique, and Pre-mortem run as isolated context windows with framework-specific expertise

在 File Structure 區塊把 `agents/` 加進去。

---

## SKILL.md Patch

在 `## 🚦 Mode Dispatcher` section 之後插入以下新 section：

```markdown
---

## 🤝 Sub-Agent Delegation Rules

The Product Playbook ships with three specialist subagents that operate in isolated context windows. Delegate to them at the right step rather than handling everything in this main agent's context — specialists produce sharper output because they carry only the framework knowledge they need.

### When to delegate to `discovery-specialist`

Delegate at these steps:

- **Full Mode**: S2 (Persona) → S3 (JTBD) → S4 (OST) → S5 (Journey Map) → S6 (Continuous Discovery hypotheses)
- **Revision Mode**: S2 (current user analysis) → S3 (pain point synthesis) → S4 (opportunity identification)
- **Build Mode**: S2 (problem clarification with JTBD lens)
- **Custom Mode**: any step that selects Persona / JTBD / OST / Journey Map / Continuous Discovery

How to invoke:

> Use the `discovery-specialist` subagent to produce [Persona | JTBD | OST | Journey Map] for [product description]. Target audience: [B2C / B2B / B2B2C]. Available research data: [list uploaded files, or "none — flag low confidence"]. Reply in [language].

Integrate the returned YAML into the current step's output. Surface the specialist's `open_questions` to the user as part of the step's confirmation prompt.

### When to delegate to `strategy-critic`

Delegate **immediately after** the user finalises any strategy artifact:

- After Strategy Blocks completion (Full Mode S7)
- After Rumelt Good Strategy Kernel completion (Full Mode S8)
- After DHM Model completion (Full Mode S9)
- After Empowered Teams charter (any mode that includes it)
- Any time the user writes "this is our strategy" in plain prose without a named framework

How to invoke:

> Use the `strategy-critic` subagent to critique the following strategy artifact: [paste verbatim]. The artifact is [framework name or "generic strategy doc"]. Reply in [language].

The critic returns critiques, not rewrites. Present the critic's `three_questions_to_ask_the_writer` to the user verbatim. Do not soften them. If the user revises in response, re-invoke the critic on the revised version.

### When to delegate to `pre-mortem-runner`

Delegate at these steps:

- **Full Mode**: S10 (after MVP scoping is complete)
- **Build Mode**: S4 (architecture-grounded pre-mortem)
- **Revision Mode**: S8
- **Feature Extension Mode**: S3 (risk assessment)
- Any time the user explicitly requests pre-mortem / risk analysis / "what could go wrong"

How to invoke:

> Use the `pre-mortem-runner` subagent to pre-mortem the following [product | feature | strategy]: [paste verbatim]. Mode: [build_mode_architecture_grounded | standard | feature_extension]. If build mode, available architecture context: [paste relevant file contents or summary]. Reply in [language].

The runner returns 15+ scenarios. In the user-facing output, lead with the `priority_three` and the `pre_launch_experiments`. Surface the full scenario list in a collapsible section or as an attached file.

### Delegation hygiene

1. **One sub-agent per step**. Do not chain sub-agents in a single turn — let the user confirm intermediate output before invoking the next specialist.
2. **Pass language explicitly**. Sub-agents detect language from your prompt; if your prompt is in English but the user is working in 繁體中文, the sub-agent will reply in English. Always specify the user's working language.
3. **Respect `status: out_of_scope`**. If a sub-agent refuses a request, take the routing recommendation seriously — the sub-agent's scope refusal is a feature, not a failure.
4. **Hard Gate inheritance**. Sub-agents inherit the no-code-during-planning rule. They will refuse to write files or run bash even if you ask them to. This is intentional.
5. **Quality self-check still applies**. After integrating sub-agent output into a step, run the existing quality self-check from `references/rules-quality-review.md` — the sub-agent did its own self-check, but the main agent owns the user-facing step output.

---
```

---

## 測試計畫

整合完之後跑這個快速驗證，確認三個 sub-agent 都正常工作：

### Test 1：Discovery 觸發

```
> /product-playbook
# 選 Full Mode
# 描述產品："a calendar app for engineering team leads who manage 5-15 people"
# 進到 S2 Persona step
```

**預期行為**：main agent 應該主動 delegate 給 `discovery-specialist`，回傳的 YAML 應該包含 Persona、JTBD 三層、open_questions。Output 語言跟 user input 一致。

**Pass criteria**：

- ✅ Sub-agent 被 invoke（在 Claude Code 介面可以看到 sub-agent indicator）
- ✅ 回傳 YAML 結構正確
- ✅ JTBD 有 functional / emotional / social 三層
- ✅ Persona 不是純 demographic，有 goals / pain_points / triggering_events
- ✅ `summary_for_main_agent` 有實質內容

### Test 2：Strategy Critic 觸發

```
> /product-playbook
# 選 Full Mode
# 走到 Strategy Blocks 步驟
# 故意寫一個爛 strategy："Our mission is to delight customers. Our vision is to be the leader in calendar tools. Our strategy is to add more features faster than competitors."
```

**預期行為**：critic 應該毫不留情地批判每一句。Rumelt kernel 三項都應該被評為 weak 或 missing。

**Pass criteria**：

- ✅ `overall_verdict` 不是 strong（如果是，prompt 設計有問題）
- ✅ Diagnosis 被評為 missing（這個 strategy 沒有真正的 diagnosis）
- ✅ Guiding policy 被評為 missing 或 weak
- ✅ `blind_spots` 至少列出 3 個
- ✅ `three_questions_to_ask_the_writer` 是具體的、可回答的問題

### Test 3：Pre-mortem 觸發

```
> /product-playbook
# 選 Build Mode（在一個既有專案目錄裡）
# 描述新功能："add real-time collaboration to the existing calendar app"
# 走到 S4 risk assessment
```

**預期行為**：runner 應該回傳 15+ scenarios，每類至少 2 個，至少 3 個有 `architecture_grounded: true`。

**Pass criteria**：

- ✅ 至少 15 個 scenarios
- ✅ 五類（product_ux / market_demand / team_execution / operational / external）都有覆蓋
- ✅ 每個 leading_indicator 有具體 threshold 跟 detectable_by 時間
- ✅ Build Mode 下至少 3 個 architecture_grounded scenarios 引用了真實 file 或 fact
- ✅ `priority_three` 真的是高 likelihood × 高 impact 的組合

### Test 4：Refusal 行為

```
# 直接 invoke discovery-specialist 問它做 RICE
> Use discovery-specialist to do RICE prioritization for these features: [...]
```

**預期行為**：sub-agent 應該 return `status: out_of_scope` 並建議 routing 給 main_agent。

**Pass criteria**：

- ✅ 沒有產出 RICE 分數
- ✅ YAML 包含 `status: out_of_scope`
- ✅ `recommended_handler` 正確指向 `main_agent`

---

## 接下來可選的擴充

如果三個 sub-agent 跑得穩，下一波可以加：

- `jtbd-interviewer`：專門模擬 user interview，產出 verbatim quotes
- `positioning-sharpener`：April Dunford 視角的 positioning 批判
- `rice-prioritizer`：純 RICE / GEM scoring 計算
- `dev-handoff-architect`：把 PRD 拆成 phase + tickets

每個新 sub-agent 都重複這份 INTEGRATION 的流程：寫檔案、改 SKILL.md delegation rules、跑 eval、更新 README。

---

## 預期影響

完成這個整合之後，The Product Playbook 從 plugin 成熟度 L2 升到 L3。對應的 portfolio 敘述升級：

**整合前**：
> "我做了一個 Claude Skill，22 個 PM framework，已 publish 到 npm，4 個 iteration 的 eval 證明 quality 提升 +69%。"

**整合後**：
> "我設計了多層 agent 架構：knowledge layer（22 個 PM framework）、command interface layer（8 個 slash command）、sub-agent specialization layer（Discovery / Strategy Critique / Pre-mortem 三個有 scope refusal 機制的專家 agent）、evaluation framework（5 個 iteration 的量化比較）。Plugin publish 到 npm 跟 Claude Code marketplace，支援 6 種語言。"

兩段話的職涯重量差距，就是這次升級的真正價值。
