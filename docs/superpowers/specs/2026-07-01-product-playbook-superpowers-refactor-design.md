# Product Playbook 重構：大道至簡 · Outcome-first 設計

**日期**：2026-07-01
**狀態**：Design（待實作 plan）
**決策範圍**：可大膽重構（現有 6-mode 與 5 語言 i18n 皆非硬約束）
**產出深度**：評估報告 + 完整遷移藍圖

---

## 0. 核心哲學（本次重構的北極星）

這套 framework 的成功指標只有一個：**完美達成使用者要的 outcome**。流程完整度、走完幾個相位、守住幾個 hard gate，都不是評分項。

三句話定調：

- **大道至簡**：整套系統概念上只有三層。一個 meta-skill（情境判讀 + framework 選擇/融合），一組 framework lens skill，幾顆選配 recipe。沒有 mode、沒有進度條、沒有逐步 gate。
- **Framework 作為 lens**：框架是用來看清問題的鏡片，套上去產出更好的 outcome。使用者要的是 outcome，框架是達成手段（框架本身不當作必經的 checkpoint）。
- **流程極致輕量**：預設只做「讀 outcome → 選 lens → 產出 → 標 provenance」四件事。使用者沒特別要求，就不做額外 ceremony、不加贅字。

借 superpowers 的**可組合性與按需觸發**。superpowers 的紀律機制（hard gate、Red Flags、相位 gate）保留知識、改變形態：從 always-on 的阻擋器，變成**相對性 guardrails**——預設沉默，偵測到 outcome 有風險時才按比例現身，一行輕量 nudge，永遠可被使用者 override（見 §4.5）。

---

## 1. 背景與問題

`product-playbook` 是已發布的 Claude Code plugin（marketplace + npm + curl 三管道），整合 22 個 PM 框架，用 6 個 mode 引導完成產品規劃。使用後暴露的問題：整體**過於線性且沈重**，每次被固定步驟序列牽著走，缺少「依當次情境判斷該用哪些框架」的彈性，也沒留給使用者自由選擇的空間。

### 1.1 診斷：重量壓在哪（實測數字）

拆解 repo 後確認，重量集中在編排層與鏡像層，框架知識本身反而已是理想形態。

| 重量來源 | 量體 | 性質 |
|---|---|---|
| i18n 6 倍鏡像 | 225 檔 / 24,410 行（另 5 份 README） | 純維護債；SKILL + references + commands 各複製 5 份 |
| 5 個 mode 脊椎檔 | rules-quick/full/revision/custom/build | 純編排膠水，本身零框架知識 |
| 橫切狀態機 | optional-trigger / change-propagation / progress / end-of-flow（約 400 行） | Phase Decision Point、進度條、pause/resume、跨步一致性檢查 |
| Hard Gate 控制層 | SKILL.md 7 條 gate + 逐步等確認 + 禁跳步 | 強制線性、加重流程的來源 |
| 綁死 mode 的 eval | 24 個 behavioral case（12 × 2 語言） | 9/12 測的是編排行為（選單有沒有列全 6 mode、S1 完成有沒有停），非框架品質 |
| dispatch hook | `user-prompt-detect-specialist-dispatch.py`（141 行） | 把 dispatch protocol 在 harness 層又硬編一次 |

**關鍵發現**：22 個 PM 框架幾乎全住在 `references/00~05c`，早已是扁平、一檔一框架的形態。沈重感來自外層的 mode 編排 + i18n 鏡像 + 為守線性而堆的 gate/hook/eval。要拆的是殼，核心可直接平移。

### 1.2 內容 vs 膠水的分界

- **A 類（真框架知識，直接平移成 lens skill）**：所有 `NN-*.md`。JTBD（167 行）、PR-FAQ、Pre-mortem/GEM/RICE/PRD 模板（04b，269 行）等本身就厚，天生一顆。
- **B 類（純編排膠水，拆殼後丟棄）**：5 個 `rules-<mode>.md` 脊椎、optional-trigger 的 Phase Decision Point、change-propagation 的進度條、progress 整檔、end-of-flow 的收尾編排。
- **C 類（藏在膠水裡的高價值知識，先救出再丟殼）**：Persona-Journey 綁定的 rationale、change-propagation 的 artifact 依賴矩陣、Revision 的假設紀律、end-of-flow 的 Decision Consistency Check。無腦拆 mode 會誤刪這層。

---

## 2. 目標與非目標

### 2.1 目標

1. **大道至簡**：整套系統只剩 meta-skill + framework lens + 選配 recipe 三層，無 mode / 進度條 / 逐步 gate。
2. **Outcome-first**：成功指標是達成使用者要的 outcome，流程完整度與 hard gate 不列入評分。
3. **情境化 framework 選擇**：meta-skill 依情境判斷用單一 framework 或融合多個。
4. **Framework 可回溯**：每個 output 自帶輕量 provenance，融合多框架時仍看得出骨架。
5. **流程極致輕量**：使用者沒特別要求，就不做額外 ceremony、不加贅字。
6. **砍 i18n 改 runtime 語言偵測**：消除 6 倍鏡像債。

### 2.2 非目標

- 不重寫 22 個框架的知識內容（只改封裝形態）。
- 不追求流程完整度、不設 always-on 的 hard gate（紀律改為 §4.5 的相對性 guardrails）、不預設逐步確認。
- 不預設走完整 recipe；recipe 是選配深度，供使用者明確要求時用。
- 不保留 mode / 進度條 / Red Flags 說教。

---

## 3. 可行性判定

**判定：走。** 而且往「outcome-first、極致輕量」收，比原本照抄 superpowers 更貼近這個領域該有的樣子。

產品規劃天生有階段性（strategy → discovery → define → solution → validation），但強迫線性正是這個領域的反模式（Marty Cagan 的 outcome 導向、Teresa Torres 的持續發現，核心都反對前置一次、線性交付）。現行 6-mode 把方法論精神用線性狀態機焊死了。

從 superpowers 借三個手法，並依「outcome-first」調整：

1. **description 只寫「何時觸發」，不寫「內部流程」**：實測顯示 description 一旦摘要 workflow，agent 會照抄 description、不讀內文。直接沿用。
2. **meta-skill + SessionStart hook 取代中央 dispatcher**：編排邏輯分散進「各 skill 的 description」，改流程只改單一 skill。沿用，但 meta-skill 定位從「紀律 enforcer」改為「outcome 讀取 + lens 選擇/融合」。
3. **flowchart 當地圖用**：superpowers 用帶回頭邊的 flow 表達預設順序 + 合法跳階。這裡進一步弱化：flow 僅供 meta-skill 判讀情境時參考，使用者可任意跳接，過程不設 gate 阻擋。

---

## 4. 目標架構

### 4.1 三層結構（全貌）

```
第一層：SessionStart hook
  └─ 每次 session（含 compact 後）注入 meta-skill 全文（僅一顆，輕量）
第二層：meta-skill「product-playbook」（情境判讀 + framework 選擇/融合）
  ├─ 讀 outcome：判斷使用者真正要的產出是什麼
  ├─ 選 lens：依情境決定用單一或融合多個 framework
  ├─ 極簡執行：直接產出，不開選單、不逐步確認、不貼進度條
  ├─ 標 provenance：output 末尾一行標「套用框架：X · Y」
  └─ 需要時才加深：使用者要求完整走查，或任務橫跨多階段，才引入 recipe
第三層：framework lens skill（~16–22 顆）＋ 選配 recipe（4 顆）
```

### 4.2 meta-skill 的四個動作（取代整個 mode 編排器）

meta-skill 是唯一 SessionStart 就注入的 skill，職責是把使用者需求映射到最小必要的 framework，直接產出 outcome。

1. **讀 outcome**：先辨識使用者要的是什麼產出（一份 PR-FAQ？一個 go/no-go 決策？一套指標？一份完整規劃？）。辨識不了才問一個關鍵澄清問題。
2. **選 lens（單一 or 融合，依情境）**：
   - 窄而明確的產出 → 單一 framework。
   - 需要多視角的決策 → 融合多個 framework 成一個整合答案，不逐個框架分步走。
3. **極簡執行**：預設直接給 outcome。不開 6-mode 選單、不逐步等確認、不貼進度條、不做每步 quality self-review。
4. **標 provenance**：見 §4.4。

**情境判讀對照（單一 vs 融合）**：

| 使用者情境 | 判讀 | lens |
|---|---|---|
| 「幫我寫一份 PR-FAQ」 | 單一、產出明確 | `pr-faq` |
| 「這功能值不值得做？」 | go/no-go 決策，需多視角 | `jtbd`（真需求？）＋ `solution-prioritization`（投報）＋ `pre-mortem`（風險）→ 融合成一個 go/no-go |
| 「我們北極星指標該設什麼」 | 單一 | `success-metrics` |
| 「幫我完整規劃這個新產品」 | 大任務、可能要完整走 | 建議 `full-product-plan` recipe（仍可只挑幾顆） |
| 「這個定位站得住嗎」 | 評審 ≠ 生成 | `strategy-critic` |

### 4.3 Framework lens skill（atomic，核心 ~22 顆）

顆粒度原則：以「完成一個決策 outcome」為職責邊界，非以「背一個框架名」。本身厚且自帶獨立品質標準的（JTBD / PR-FAQ / Pre-mortem）天生一顆；拆開只能串用的（Pain → HMW → 排序、North Star → Signals → Aha）合成一顆。輸出模板（PRD / HTML / CSS）與思考框架分離。

每顆 lens skill = 一個框架的知識 + 如何套用 + 好 output 長怎樣 + 自帶 provenance 標籤。可單獨觸發，也可被 meta-skill 拉來融合。**定案 16 顆**（依大道至簡精神合併）：

| 相位 | Skill | 併入來源 | 內含框架 |
|---|---|---|---|
| Strategy | `strategy-kernel` | 00 + 01 + 05a(empowered) | Opportunity Check、DHM、Strategy Blocks、Rumelt Kernel、Shreyas 三層、Empowered Teams |
| Discovery | `persona-journey` | 02a + 02c(journey) | Persona（含 B2B Buyer/User）、User Journey Map（沿用原 Persona-Journey 綁定） |
| Discovery | `jtbd` | 02b | JTBD 三層 + B2B Org-Level Jobs（密度最高，獨立一顆） |
| Discovery | `opportunity-solution-tree` | 02c(OST) | OST（Teresa Torres） |
| Define | `problem-framing` | 03 §2.1/2.3/2.4 | Pain Point Table、HMW Reframing、Opportunity Assessment |
| Define | `positioning` | 03 §2.2 | April Dunford Positioning |
| Develop | `pr-faq` | 04a | Working Backwards PR-FAQ |
| Develop | `pre-mortem` | 04b §3.3 + agent | Shreyas Doshi Pre-mortem（保留 subagent 形式供 context 隔離） |
| Develop | `solution-prioritization` | 04b §3.4/3.5 | RICE、GEM、Impact/Effort |
| Develop | `mvp-scoping` | 04b §3.2/3.6 + 04c | MVP、Not Doing List、Parallel Prototyping、User Story |
| Measure | `success-metrics` | 05a | North Star、Three-Layer Signals、Aha Moment、Sean Ellis Score |
| Measure | `pmf-gtm` | 05b | Four-Level PMF、GTM、Business Model & Pricing |
| Output | `prd-and-handoff` | 04b(PRD) + 07a/07b/07c + 08 | PRD 模板 + Mermaid、交接包（CLAUDE.md/TASKS/TICKETS/ARCHITECTURE）、security section |
| Output | `document-export` | 06 + rules-export-document | 互動 HTML 報告 + PDF 匯出（自帶 report-style.css / prd-style.css 兩支） |
| Cross | `product-spec-summary` | 05c | 最終規格彙整 + Risk Register + Gaps & Blind Spots |
| Review | `strategy-critic` | agent | 對抗式策略評審（職責與生成正交，保留獨立） |

**合併說明（22 → 16）**：strategy 三顆（kernel / DHM-opportunity / empowered）併為一個 strategy lens；persona + journey 沿用原全域綁定併為 `persona-journey`；`prd-generation` + `dev-handoff-package` + `security-checklist` 併為 `prd-and-handoff`（08 的 security Hard Gate 本就被 07b 消費）；`html-report` + `export-to-pdf` 併為 `document-export`。內含框架仍以 body 分節保留，融合不損知識。

**Specialist 三 subagent 處置**：`discovery-specialist` 知識與 02a/b/c 完全重疊 → 收斂進四顆 discovery skill，subagent 刪除；`pre-mortem-runner` 是知識增量 → 保留成 `pre-mortem` skill；`strategy-critic` 職責正交 → 保留獨立。

### 4.4 Framework provenance 機制（本次唯一刻意保留的結構）

大道至簡下仍讓使用者看得出「這結論用了哪些 lens」，可回溯、可質疑、可要求換 lens。

- **格式**：output 末尾一行輕量標記，例：`— 套用框架：JTBD · RICE · Pre-mortem`。
- **融合時**：列出所有貢獻的 framework；單一時就一個。
- **保持輕量**：固定一行，不做成大表格或分段。使用者要求 breakdown 時才展開「各框架各貢獻了什麼」。
- **可關**：使用者說「不用標」就不標。它是回溯工具，不是新 ceremony。
- **實作**：每顆 lens skill body 內含一句「產出時在末尾附上本框架標籤」；meta-skill 融合多顆時彙整成單行。

### 4.5 流程極致輕量化 + 相對性 guardrails

界定「預設不做 / 預設做 / 有必要才現身的 guardrails」，避免舊 mode 的 ceremony 回流，同時把紀律保留成風險比例的安全網。

- **預設不做**：mode 選單、進度條、逐步等確認、每步 quality self-review、把「我要開始了嗎」問出口。
- **預設做**：讀 outcome → 選 lens → 產出 outcome → 標 provenance。四步，無贅字。

**相對性 guardrails（dormant by default，偵測風險才按比例現身，永遠可 override，永不硬性阻擋）**：

舊系統的 hard gate / Red Flags / 相位 gate 是 always-on 的阻擋器。這裡保留同一套紀律知識，改成 risk-proportional 的 guardrails。判準只有一句：**這一步照使用者當下的走法，outcome 會不會被實質危害？** 不會就沉默，會才現身，且只用一行輕量 nudge，使用者一句話即可略過。

| 觸發情境 | guardrail | 現身方式（範例） |
|---|---|---|
| 要直接產 solution/PRD，但沒有任何 problem statement | 相位 guardrail | 一行提醒：「還沒有明確的 problem statement，要我先花一分鐘釐清，還是你已有、直接給我？」 |
| 偵測到會實質傷害 outcome 的合理化（如 0-to-1 卻「我知道用戶要什麼、跳過 discovery」） | Red Flag（輕量版） | 一句點名風險 + 交使用者決定，不說教、不成段 |
| 功能觸及 payments / permissions / data migration | security guardrail | 一句提示補 security 視角（引 `prd-and-handoff` 的 security section） |
| 規劃階段意外要寫 source code | codebase 安全網 | 預設產文件；使用者明確轉入 build 才寫 |
| 方向性大改會連動已產出的下游 artifact | 一致性 guardrail | 一行標出 impact scope，讓使用者選只改本步或連動更新 |

三個共同性質：**proportional**（按風險決定要不要出、出多重）、**non-blocking**（永遠可略過）、**one-line**（不說教、不成段）。它們是保護 outcome 的護欄，不是流程的關卡。guardrail 觸發門檻由 P3 的 eval 校準，避免頻繁現身而退化成 ceremony。

### 4.6 Recipe（選配深度，非預設）

4 顆薄 recipe 保留，但定位從「主介面」降為「使用者明確要完整走一遍時的選配」。預設路徑是 §4.2 的輕量融合。**不露出成 slash command**；由 meta-skill 依情境判讀後口頭建議觸發（例：偵測到大型完整規劃任務時，一句「要不要用 full-product-plan 完整走一遍？」，由使用者決定）。

| Recipe | 對應舊 mode | 內容（推薦順序，可增減跳回） |
|---|---|---|
| `full-product-plan` | Full | strategy-kernel → persona → journey-map → jtbd → problem-framing →（positioning 選配）→ pr-faq → solution-prioritization → mvp-scoping → success-metrics →（pmf-gtm 選配） |
| `quick-validation` | Quick | jtbd → pr-faq → success-metrics（一頁方向） |
| `product-revision` | Revision | 現況盤點（含假設紀律）→ problem-framing → pr-faq →（pre-mortem 選配）→ mvp-scoping → success-metrics（before/after） |
| `feature-extension` | Feature / Build | problem-framing（含既有系統脈絡）→ solution-prioritization → pre-mortem（regression/compatibility）→ mvp-scoping |

舊 Custom mode 直接由「自由組合 lens skill」取代，不需獨立 recipe。

### 4.7 i18n：全砍改 runtime 偵測

- 刪 `i18n/` 5 份鏡像（225 檔 / 24,410 行）與 5 份 README 翻譯。
- 單一英文正本；每顆 skill 與 meta-skill body 內含指令：偵測使用者語言，framework 內容以英文撰寫，所有 user-facing 輸出比照使用者語言。此為 superpowers 既有做法。
- 連帶解掉 `evals-zh-TW.json`、`i18n-mirror-apply.py`、`i18n-drift-report.py`、install.sh 的 `--lang` 六語邏輯。

---

## 5. 遷移藍圖

| 階段 | 動作 | 產出/驗收 |
|---|---|---|
| **P0 基建** | 建 meta-skill「product-playbook」（讀 outcome + 選 lens + provenance，body 保持精簡）；建 SessionStart hook（注入 meta-skill 全文，matcher 含 compact）；畫情境判讀參考地圖（非強制路徑） | meta-skill 可觸發；hook 在 startup/clear/compact 注入 |
| **P1 內容平移** | 22 框架逐一升級成 lens skill（frontmatter description 只寫觸發詞；body 含「好 output 長怎樣 + provenance 標籤」）；把 C 類散落知識救出併入對應 skill | ~22 lens skill 各自可獨立觸發、可被融合 |
| **P2 拆殼** | 刪 5 個 mode 脊椎檔 + optional-trigger/progress/end-of-flow 的編排部分 + dispatch hook；把 6-mode 帶路價值重寫成 4 顆選配 recipe；discovery-specialist subagent 刪除 | 編排層清空；預設走輕量融合 |
| **P3 機器層** | 砍 i18n 5 鏡像 + 2 支 i18n script + 5 份 README；behavioral eval 改測「outcome 品質 + framework 選對沒 + provenance 有沒有標」（不再測 mode 選單）；trigger eval 60+ 沿用；closed-loop 的 `EVAL_ATTRIBUTION` map 改指向新 skill | i18n 債清零；eval 綠燈 |
| **P4 封裝** | 更新 `plugin.json` / `marketplace.json` / `package.json`（三處版本同步 + description 改寫成 outcome-first）；改 install.sh 目錄佈局；bump 版本 | 三管道可發佈 |

### 5.1 成本熱點排序

1. **i18n 6x 鏡像（最貴）**：砍一次同時解掉 evals-zh-TW、i18n-mirror/drift 兩 script、install.sh 六語邏輯、5 份 README。
2. **綁 mode 的 24 個 behavioral eval**：expectation 全數失效需重寫成 outcome 導向。
3. **dispatch hook**：整支重寫（改為無顯式 dispatch）。

### 5.2 可無痛保留

- trigger eval（60+ case）+ Python runner。
- `session-start-load-progress.py`（只依賴進度檔名）。
- closed-loop 自我改進 harness 骨架：只需改 `EVAL_ATTRIBUTION` map。
- templates 兩支 CSS：跟著 `export-to-pdf` / `html-report` skill 走。

---

## 6. 風險與緩解

| 風險 | 緩解 |
|---|---|
| 融合時選錯 lens 或少選 lens，outcome 偏 | provenance 讓使用者一眼看出用了哪些 lens，可要求增補；§4.2 情境判讀表提供對照基準 |
| 輕量化過頭，複雜任務缺結構 | recipe 當選配安全網；任務真大時 meta-skill 主動一句「要不要完整走一遍」，由使用者決定 |
| description 語意觸發不準 | 用現有 60+ trigger eval 回歸；沿用「Use when …, before …」觸發句法 |
| provenance 變成新的 ceremony | 嚴格限一行、可關；預設不展開 breakdown |
| 發布三管道版本 / 佈局不同步 | P4 明列三處版本同步 + install.sh 佈局改動 |
| 平移時誤刪 C 類藏在膠水裡的知識 | P1 明列 C 類知識去向，逐一驗收 |

---

## 7. 已定決策

- **核心哲學**：outcome-first、大道至簡、framework-as-lens、流程極致輕量。
- **編排層**：meta-skill + framework lens + 選配 recipe 三層；mode / 進度條 / 逐步確認移除為預設。
- **紀律機制**：hard gate / Red Flags / 相位 gate 不刪除，降為**相對性 guardrails**——預設沉默，偵測 outcome 風險才按比例現身，一行輕量、永遠可 override、永不硬性阻擋（§4.5）。
- **framework lens**：定案 **16 顆**（§4.3），支援單一或融合，由 meta-skill 依情境判斷。
- **provenance**：output 自帶輕量一行 framework 標記；**預設只標框架名**，breakdown 僅在使用者要求時展開；可關。
- **recipe**：4 顆選配，**純靠 meta-skill 建議觸發，不露出成 slash command**。
- **i18n**：全砍，改 runtime 語言偵測。
- **相容性**：可大膽重構，6-mode 與 i18n 非硬約束。

## 8. 待實作階段釐清（非阻擋設計）

- 相對性 guardrails 的觸發門檻校準：哪些情境值得現身、如何避免頻繁現身而退化成 ceremony（P3 用 eval 迭代）。
- closed-loop harness 是否隨此次重構一併更新，或列為後續獨立工作。
