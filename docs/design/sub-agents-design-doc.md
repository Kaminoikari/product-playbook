# Sub-Agents 設計文件

> 狀態：已實作（第一波三個 sub-agent）
> 範圍：The Product Playbook plugin 的 L3（multi-agent）層
> 此文件記錄設計理由，整理自一次 Claude.ai 的設計討論。

---

## 1. 背景與動機

### 1.1 Plugin 成熟度盤點

The Product Playbook 對照 Claude Code Plugin 的成熟度階梯：

| 層級 | 說明 | 現況 |
|---|---|---|
| L1 | Knowledge plugin（框架知識）| ✅ |
| L2 | Command plugin（slash command + natural language trigger）| ✅ |
| L3 | Multi-agent plugin（sub-agent 專業分工）| ❌ → **本次補上** |
| L4 | Integration plugin（MCP server）| ❌（後續）|
| L5 | Ecosystem plugin（npm publish、marketplace、i18n）| ✅ |
| L6 | Cross-framework abstraction（Claude.ai Skill / Plugin / Code Skill 三路安裝）| ✅ |

這個分布不尋常：plugin 跳過 L3、L4，直接完成 L5、L6。代表既有優勢在「包裝與分發」，而非「架構複雜度」。補上 L3 之後，plugin 在每一層都站得住，整體深度才完整。

### 1.2 核心問題

目前 22 個 PM framework 全部跑在同一個 main agent 的 context window，靠 `SKILL.md` 與 `references/*.md` 動態載入框架知識。這個設計優雅，但有一個本質限制：

> Main agent 在執行單一 framework（例如 Quick Mode 的 JTBD 分析）時，context 裡同時塞著其餘 21 個 framework 的記憶（GEM Model、Strategy Blocks、Pre-mortem…）。這會稀釋它在當下這個 framework 上的專注度與深度。

Sub-agent 就是為了解決這個問題：把單一 framework cluster 拆進一個獨立的 context window，讓專家 agent 只攜帶它需要的知識。

---

## 2. 設計決策

### 2.1 第一波：三個最有 leverage 的 sub-agent

選擇標準是「專業化收益最大、且彼此 scope 不重疊」的三個 framework cluster：

| Sub-agent | 負責範圍 | 角色定位 |
|---|---|---|
| `discovery-specialist` | Persona / JTBD / OST / Journey Map / Continuous Discovery | 資深 product researcher（Teresa Torres、Christensen 傳統）|
| `strategy-critic` | Strategy Blocks / Rumelt Kernel / DHM / Empowered Teams | 無情但具體的策略批判者（Rumelt + Cagan 雙視角）|
| `pre-mortem-runner` | Pre-mortem 風險分析 | Pre-mortem facilitator（Gary Klein + Shreyas Doshi）|

**為什麼是這三個：**

- **discovery-specialist** — Discovery 階段框架最多、彼此關聯最緊（Persona 定義 Who、Journey Map 描述 Who 的歷程），抽成獨立 context 收益最大。
- **strategy-critic** — 策略錯誤會往下游傳播一整季。批判者必須「預設批判、禁止軟化」；main agent 因為要 balance 各種框架、要對使用者友善，天然無法扮演這個角色。獨立 sub-agent 才能維持 hostile-but-fair 姿態。
- **pre-mortem-runner** — Pre-mortem 在 main agent 裡跑會偏 generic，因為 main agent 必須兼顧所有框架。Sub-agent 可以全力投入「假設產品失敗了，列 15+ 種原因，每種附 leading indicator」。

### 2.2 第二波（暫緩，待第一波驗證有效後再做）

`jtbd-interviewer`、`positioning-sharpener`、`rice-prioritizer`、`dev-handoff-architect`。

### 2.3 L4（MCP server）暫緩

下一個大里程碑是寫一個 Asana handoff MCP server，讓 `/product-dev` 跑完後直接在 Asana 開 project、建 epic + tasks。工程量約 1–2 個週末，重點在 schema 設計。本次不做。

---

## 3. Sub-agent 設計三個關鍵心法

### 3.1 最小知識載入

Sub-agent 只攜帶它負責的 framework 知識，不塞整本 Playbook。這是 sub-agent 比 main agent 強的根本原因——專注度不被其他 21 個框架稀釋。

**實作選擇：知識內嵌，而非 file reference。**
原始討論提到「sub-agent 的 system prompt 只 reference 它負責的 framework 檔」。實作時改為把框架知識**直接內嵌**在 sub-agent 的 system prompt（見 `discovery-specialist.md` 的 "Framework reference (embedded knowledge)" 段落）。原因：sub-agent 在獨立 context 啟動，內嵌知識比執行期再去 `Read` 一個 reference 檔更可靠、不受路徑或載入時機影響。「最小知識」的精神不變——內嵌的只有該 agent 負責的框架。

### 3.2 禁止越權，明確 refuse 並 return

Sub-agent 收到不屬於職責範圍的請求時，必須明確拒絕並把控制權交還 main agent，而不是勉強作答。

這是 first-class feature，不是錯誤處理：每個 sub-agent 的 YAML output schema 都內建 `status: out_of_scope` 的 return path，附 `recommended_handler` 指出正確的承接者。例如 `discovery-specialist` 被要求做 RICE，會回 `out_of_scope` 並建議 route 回 `main_agent`。

這個機制就是 Marty Cagan 講的「empowered specialist」與 generic worker 的差別——專家知道自己的邊界。

### 3.3 Structured YAML output

Sub-agent 的 output 是給 main agent 解析的**中介格式**，不是給人看的最終文件。Main agent 拿到 YAML 後負責整合進 step output 呈現給使用者。這個分層是 multi-agent system 與「多個 prompt 串接」的本質差別。

---

## 4. 共通設計約定

### 4.1 觸發機制：`description` 用 PROACTIVELY

每個 sub-agent 的 frontmatter `description` 以 `PROACTIVELY` + action verb 開頭，並明列觸發步驟（如 Full Mode S2-S6）。Claude Code 依此自動 delegate（auto-delegate），不需要使用者手動呼叫。

### 4.2 `model: inherit`

三個 sub-agent 都不硬寫 `sonnet` 或 `opus`，一律 `inherit`。

理由：plugin 使用者橫跨 Claude Pro / Max / API。硬寫 `opus` 會讓 Pro 方案使用者跑不動；硬寫 `sonnet` 又限制了 Max/API 使用者的品質。`inherit` 讓 sub-agent 跟著 main agent 當下的 model 跑，相容所有方案。

### 4.3 工具集：唯讀

三個 sub-agent 的 `tools` 都是 `Read, Grep, Glob, WebSearch`——全部唯讀。

理由：sub-agent 繼承 main agent 的 Hard Gate（規劃過程不寫 code、不建檔）。不給 `Write` / `Edit` / `Bash`，從工具層強制這條規則，即使使用者要求「把 persona 存成檔案」也無法越權。檔案與決策的所有權永遠在 main agent。

> 註：原始討論說「只給 read 跟 web_search」。實作多納入 `Grep` 與 `Glob`，兩者同為唯讀，讓 sub-agent 能在既有 codebase 裡定位檔案（Build Mode 的 architecture-grounded pre-mortem 需要），不違反「不寫入」的精神。

### 4.4 多語言

Sub-agent 檔案本身**不做** i18n 翻譯。每個 sub-agent 在 system prompt 內 instruct 自己「reply in the orchestrator's language」，YAML 欄位名固定英文、敘述內容用 orchestrator 的語言。一份英文 sub-agent 即可服務六種語言。Main agent delegate 時必須在 prompt 裡明示使用者的工作語言。

---

## 5. Output schema 的演進

設計討論**早期**的心法曾提出：sub-agent output「永遠以 YAML 開頭，包含 `confidence`、`summary`、`details`、`open_questions` 四個統一欄位」。

**最終實作沒有採用這個統一四欄位 schema**，而是演進為：

- **共用 envelope**：三個 agent 都有 `status`、`language`、`summary_for_main_agent`
- **per-agent framework-specific body**：每個 agent 依其框架特性各自設計 schema
  - `discovery-specialist`：`persona` / `jtbd` / `ost` / `journey_map` / `continuous_discovery` / `open_questions`
  - `strategy-critic`：`rumelt_kernel` / `blind_spots` / `three_questions_to_ask_the_writer`
  - `pre-mortem-runner`：`scenarios` / `priority_three` / `pre_launch_experiments` / `open_questions`
- **`confidence` 改為逐欄位標註**：在 `discovery-specialist` 裡，confidence 不是 top-level 欄位，而是掛在每一個 persona trait / JTBD / opportunity 上（evidence-aware confidence 原則）。

**理由**：強行統一四欄位會讓三個本質差異很大的 framework 被塞進同一個模子。策略批判的產物是「三段式評分 + blind spot」，pre-mortem 的產物是「15+ 帶 leading indicator 的 scenario」，硬套同一 schema 反而降低 main agent 解析的精準度。交付階段重申的設計決策只保留「Output 一律 YAML」這條，放棄了統一欄位。

**已知小不一致**：`discovery-specialist` 與 `pre-mortem-runner` 用 `open_questions`，`strategy-critic` 用語意對應的 `three_questions_to_ask_the_writer`。`INTEGRATION.md` 的 SKILL.md patch 已分別正確指名各自欄位，main agent 整合時依 patch 指示處理即可。若未來要統一 main agent 的解析邏輯，可考慮為 `strategy-critic` 補一個 `open_questions` 別名——目前不視為 bug。

---

## 6. 整合方式

詳細步驟見 repo root 的 `INTEGRATION.md`。摘要：

1. **檔案位置**：`agents/` 目錄置於 plugin root（與 `commands/`、`skills/`、`SKILL.md` 同層），Claude Code 安裝 plugin 時自動載入。
2. **SKILL.md patch**：在 `## 🚦 Mode Dispatcher` section 之後插入 `## 🤝 Sub-Agent Delegation Rules`，告訴 main agent 何時 delegate、如何 invoke、以及 delegation hygiene（一步一個 sub-agent、明示語言、尊重 out_of_scope、Hard Gate 繼承、quality self-check 仍適用）。
3. **i18n**：六份 `i18n/*/SKILL.md` 需同步加入 delegation rules（建議英文版定稿後再翻譯）。
4. **evals**：新增第三組對比「With Skill + Sub-Agents vs With Skill only」，量化 Discovery / Strategy / Pre-mortem 三個步驟的品質提升。
5. **README**：在 "What Is This?" 加一行 sub-agents 說明，File Structure 加 `agents/`。

---

## 7. 預期影響

完成整合後，The Product Playbook 從 L2 升到 L3，成為覆蓋 L1–L6 的完整多層架構：knowledge layer（22 framework）、command interface layer（8 slash command）、sub-agent specialization layer（3 個有 scope refusal 的專家 agent）、evaluation framework（多 iteration 量化比較），並 publish 到 npm 與 Claude Code marketplace、支援 6 種語言。

---

## 8. 後續工作

- [x] 同步六份 i18n SKILL.md 的 delegation rules（en / zh-TW / zh-CN / ja / ko / es）
- [x] 新增 evals sub-agent 對比測項（`evals.json` / `evals-zh-TW.json` 各新增 id 10-12）
- [ ] 實際執行新 evals 取得量化數據（與「With Skill only」對比）
- [x] 更新 README（What Is This? + File Structure，六份 README 皆已同步）
- [ ] 第一波驗證有效後，評估第二波四個 sub-agent
- [ ] L4：Asana handoff MCP server
