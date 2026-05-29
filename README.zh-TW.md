[English](README.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [Español](README.es.md) | [한국어](README.ko.md)

# 🎯 The Product Playbook

**世界級產品規劃 AI Skill — 從 Idea 到開發，一套框架全搞定**

[![npm version](https://img.shields.io/npm/v/product-playbook.svg)](https://www.npmjs.com/package/product-playbook)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://code.claude.com)
[![Claude.ai](https://img.shields.io/badge/Claude.ai-Custom%20Skill-blue)](https://claude.ai)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![i18n](https://img.shields.io/badge/i18n-6%20languages-green)](README.md)

> 整合 Lenny's Podcast 歷來最重要的 PM 框架（Teresa Torres、Shreyas Doshi、Gibson Biddle、April Dunford、Todd Jackson、Marty Cagan、Richard Rumelt 等），讓 AI 成為你的資深產品經理教練。

---

## ✨ 這是什麼？

The Product Playbook 是一個 **Claude AI Skill**，能夠系統性地引導你完成從 0 到 1 的產品規劃。它不只是一個提示詞（prompt），而是一套完整的互動式框架引導系統，包含：

- 🧭 **6 種執行模式** — 從 30 分鐘快速驗證到完整企劃（含功能擴充快速路徑）
- 📐 **22 個產品框架** — 涵蓋 Discovery → Define → Develop → Deliver 全流程
- 🤝 **3 個專家 sub-agent** — Discovery、策略批判、Pre-mortem 在獨立 context window 中運作，各自攜帶專屬框架專業
- 🔄 **變更傳播引擎** — 修改任何步驟，自動更新所有下游產出
- 📎 **檔案智慧整合** — 上傳數據、截圖、文件，AI 自動整合到對應步驟
- 🔗 **開發銜接** — 產出 CLAUDE.md + TASKS.md + TICKETS.md，無縫銜接 Claude Code 開發
- 📊 **多格式產出** — PDF（含書籤）、HTML 報告、Word 文件、PowerPoint、開發交接包
- 📄 **智慧文件匯入** — 三層 PDF 解析（文字擷取 → Claude Vision → OCR 備援）、DOCX/PPTX 支援

**用一句話觸發整個流程：**

```
我想做一個產品
```

---

## 🎬 Demo

<p align="center">
  <img src="assets/demo-build-zh-TW.gif" alt="The Product Playbook Demo — Build Mode" width="800">
</p>

> 上圖展示**直接實作模式**：輸入需求 → 掃描 codebase → 偵測技術棧 → 引用框架進行問題釐清，直接進入解法設計。

---

## 🚀 快速開始

### 方法一：Claude.ai 自訂 Skill

> ⚠️ 不要用 GitHub 的「Download ZIP」— 整個 repo 約 70MB（demo GIF 佔大宗），Claude.ai 自訂 Skill 上傳上限是 30MB。

1. 從 [latest release](https://github.com/kaminoikari/product-playbook/releases/latest) 下載 `product-playbook-claude-ai-v<最新版>.zip`（約 900KB）
2. 本機解壓縮
3. 前往 [Claude.ai](https://claude.ai) → 設定 → 自訂 Skill
4. 上傳解壓後的 `product-playbook/` 資料夾
5. 在對話中說「我想做一個產品」即可觸發

### 方法二：Claude Code Plugin

在 Claude Code 中執行：

```
/plugin marketplace add kaminoikari/product-playbook
/plugin install product-playbook@kaminoikari-product-playbook
```

> 第一行指令新增 marketplace（只需執行一次），第二行安裝 plugin。

### 方法三：Claude Code Skill（推薦）

> 💡 更新方式：重新執行安裝指令即可覆蓋更新。

| 方式 | 適合誰 | 需要什麼 |
|------|--------|----------|
| ① 複製貼上 | 新手 | 只要開 Claude Code |
| ② 一鍵安裝 | 開發者 | 終端機 |
| ③ 手動安裝 | 想自訂路徑 | 終端機 + git |

#### ① 複製貼上安裝（最簡單）

啟動 Claude Code 後，直接貼上以下內容，Claude 會自動幫你完成安裝：

```
請幫我執行以下指令來安裝（或更新）product-playbook skill，
執行完畢後告訴我結果：

git clone https://github.com/kaminoikari/product-playbook.git /tmp/product-playbook
mkdir -p ~/.claude/skills ~/.claude/commands
cp -r /tmp/product-playbook ~/.claude/skills/product-playbook
cp /tmp/product-playbook/commands/* ~/.claude/commands/
rm -rf /tmp/product-playbook
```

#### ② 一鍵安裝（終端機）

```bash
# curl
curl -fsSL https://raw.githubusercontent.com/kaminoikari/product-playbook/main/install.sh | bash

# npx（需要 Node.js）
npx product-playbook
```

解除安裝：

```bash
curl -fsSL https://raw.githubusercontent.com/kaminoikari/product-playbook/main/install.sh | bash -s -- --uninstall
# 或
npx product-playbook --uninstall
```

#### ③ 手動安裝

```bash
git clone https://github.com/kaminoikari/product-playbook.git
mkdir -p ~/.claude/skills ~/.claude/commands
cp -r product-playbook ~/.claude/skills/product-playbook
cp product-playbook/commands/* ~/.claude/commands/
```

安裝完成後，在 Claude Code 中觸發：

```bash
# Skill 主指令
> /product-playbook

# Slash Commands（安裝後可用）
> /product-quick 我想做一個記帳 App
> /product-full 寵物社群平台
> /product-revision 改版我們的電商結帳流程

# 或自然語言
> 我想做一個產品企劃
> 用 JTBD 分析一下我的產品
> 幫我做個 MVP 規劃
```

---

## 📦 檔案結構

```
product-playbook/
├── SKILL.md                          # 主控核心：模式定義、步驟序列、指令系統
├── LICENSE                           # MIT License
├── README.md                         # English README
├── README.zh-TW.md                   # 繁體中文 README（本文件）
├── assets/
│   └── demo-build-zh-TW.gif          # README 動態展示圖
├── commands/                         # Claude Code CLI Slash Commands（可選安裝）
│   ├── product-quick.md              # /product-quick — 快速模式
│   ├── product-full.md               # /product-full — 完整模式
│   ├── product-revision.md           # /product-revision — 改版模式
│   ├── product-build.md              # /product-build — 直接實作模式
│   ├── product-feature.md            # /product-feature — 功能擴充模式
│   ├── product-prd.md                # /product-prd — 產出 PRD
│   ├── product-report.md             # /product-report — 產出 HTML 報告
│   └── product-dev.md                # /product-dev — 產出開發交接包
├── agents/                           # 專家 sub-agent（Claude Code plugin 自動載入）
│   ├── discovery-specialist.md       # Persona / JTBD / OST / Journey Map 專家
│   ├── strategy-critic.md            # Rumelt 視角的策略批判者
│   └── pre-mortem-runner.md          # 15+ failure scenarios + leading indicators
└── references/
    ├── 00-opportunity-check.md       # 機會評估 + DHM Model
    ├── 01-strategy.md                # Strategy Blocks + Rumelt + OKR
    ├── 02-discovery.md               # Persona + JTBD + OST + Journey Map
    ├── 03-define.md                  # 痛點 + Positioning + HMW + 機會評估
    ├── 04-develop.md                 # PR-FAQ + Pre-mortem + RICE + MVP + PRD
    ├── 05-deliver.md                 # North Star + PMF + GTM + 商業模式 + 產品規格
    ├── 06-html-report.md             # HTML 企劃報告產出規格
    ├── 07-dev-handoff.md             # 開發銜接：CLAUDE.md + TASKS.md + 架構
    ├── 08-security-checklist.md      # OWASP Top 10 + CORS + CSP + 安全架構
    ├── rules-context.md              # 跨 Session 產品上下文累積規則
    ├── rules-document-tools.md       # 文件轉換工具依賴管理
    ├── rules-import-document.md      # 三層 PDF 解析 + DOCX/PPTX 匯入
    ├── rules-export-document.md      # 多格式匯出（PDF/DOCX/PPTX）
    ├── rules-*.md                    # 各模式步驟規則 + 進度/變更/檔案整合規則
    └── templates/
        ├── prd-style.css             # 專業印刷級 CSS（PDF 匯出用）
        └── report-style.css          # 列印最佳化 CSS（HTML 報告 → PDF）
```

---

## 🧭 六種執行模式

| 模式 | 步驟數 | 耗時 | 適合情境 |
|------|--------|------|---------|
| 🚀 **快速模式** | 3 步 | ~30 分鐘 | 快速驗證想法、準備簡報 |
| 📦 **完整模式** | 9–11 步(8 Core + 1 預設啟用 Journey Map + 2 預設停用 Optional) | 1-2 小時 | 新產品規劃、重大改版 |
| 🔄 **改版模式** | 6–8 步(6 Core + 2 Optional) | <1 小時 | 既有產品改版優化 |
| ✏️ **自訂模式** | 4-16 步 | 依選擇 | 補足特定環節 |
| ⚡ **直接實作** | 7 步 | ~1 小時 | 問題已知，直接進解法 |
| 🔧 **功能擴充** | 4 步 | ~30 分鐘 | 既有產品加單一功能 |

---

## 📐 涵蓋的框架

### 理解用戶
| 框架 | 提出者 | 用途 |
|------|--------|------|
| JTBD（Jobs to Be Done） | Clayton Christensen | 找出用戶真正想完成的工作 |
| Persona | — | 用途/任務/動機導向的用戶角色 |
| User Journey Map | — | 用戶完整體驗旅程 |
| Continuous Discovery | Teresa Torres | 每週接觸用戶的持續習慣 |
| OST（機會解法樹） | Teresa Torres | 系統化連結機會與解法 |

### 定義問題
| 框架 | 提出者 | 用途 |
|------|--------|------|
| Positioning | April Dunford | 競爭場域和差異化定位 |
| HMW（How Might We） | — | 將痛點轉化為設計問題 |

### 解法設計
| 框架 | 提出者 | 用途 |
|------|--------|------|
| Working Backwards / PR-FAQ | Amazon | 從用戶結果出發倒推解法 |
| Pre-mortem | Shreyas Doshi | 在失敗前預測並預防失敗 |
| GEM Model | Gibson Biddle | Growth / Engagement / Monetization 排序 |
| RICE Scoring | Intercom | 量化功能優先排序 |
| MVP 定義 | — | 最小可行產品範圍 |

### 策略層
| 框架 | 提出者 | 用途 |
|------|--------|------|
| Strategy Blocks | Chandra Janakiraman | Mission → Vision → Strategy 層級結構 |
| Good Strategy Kernel | Richard Rumelt | 診斷 → 指導方針 → 連貫行動 |
| DHM Model | Gibson Biddle | Delight / Hard to copy / Margin-enhancing |
| Empowered Teams | Marty Cagan | 賦能型團隊 vs 功能型團隊 |

### 衡量與交付
| 框架 | 提出者 | 用途 |
|------|--------|------|
| North Star Metric | Sean Ellis / Amplitude | 代表核心用戶價值的單一指標 |
| 四級 PMF 框架 | Todd Jackson | 判斷產品市場契合度 |
| Sean Ellis Score | Sean Ellis | 量化 PMF 熱情程度 |
| GTM 策略 | — | Go-to-Market 上市與獲客 |
| 商業模式與定價 | — | 收費模式選擇與價值定價 |

---

## 🔑 核心特色

### 📎 智慧檔案整合

在任何步驟中上傳補充檔案，AI 自動判斷並整合：

| 上傳內容 | 自動整合到 |
|---------|-----------|
| 競品截圖 | Positioning 分析 |
| 訪談逐字稿 | Persona + JTBD |
| 用戶數據 CSV | 機會評估 + PMF 判斷 |
| 市場報告 PDF | 機會評估 + Strategy |
| 既有 PRD | 改版模式 + MVP |

### 🔄 變更傳播引擎

修改任何上游步驟，下游自動更新：

```
修改 JTBD → 自動更新 HMW、Positioning、PR-FAQ、North Star、產品規格摘要
修改 MVP  → 自動更新 User Story、DB Schema、產品規格摘要
```

### 🔗 開發銜接

產出完整開發交接包，一句話啟動 Claude Code 開發：

```
📦 開發交接包
├── CLAUDE.md          → Claude Code 專案記憶
├── TASKS.md           → 功能拆解 + Phase 分期
├── TICKETS.md         → 開票清單（可直接在 Jira/Asana/Linear 開票）
├── docs/
│   ├── PRD.md         → 完整 PRD
│   ├── ARCHITECTURE.md → DB Schema + API + 目錄結構
│   └── PRODUCT-SPEC.md → 產品規格摘要
└── scripts/
    └── setup.sh       → 一鍵初始化腳本
```

```bash
# 在 Claude Code 中一句話開始開發
> 請讀取 CLAUDE.md 和 TASKS.md，開始執行 Phase 0
```

### 🪝 生命週期 Hooks

三個 plugin hook 將 playbook 的核心規則從「靠 Claude 自己記得」轉為「由 harness 強制執行」。所有 hook 只注入 `systemMessage` 軟提醒，**不阻擋使用者**。

| 事件 | 觸發時機 | 作用 |
|------|---------|------|
| `SessionStart` | 每次新 session 或 resume | 自動將 `.product-playbook-progress.md` 與 `.product-context.md` 注入模型 context，讓中斷的規劃從原步驟無縫接續 |
| `UserPromptSubmit` | 規劃進行中每次送出 prompt | 偵測（a）離題訊息（debug / 錯誤 / "幫我改 code"）→ 提醒 Claude 執行 SKILL.md 的存檔規則；（b）變更意圖關鍵字（`改 step 2`、`update persona`、`重做 JTBD`）→ 提醒套用 Change Propagation 規則 |
| `PreToolUse` (Write/Edit/MultiEdit) | 每次寫檔前 | 若專案仍在規劃階段（無 `.product-dev-active` 標記）且目標是原始碼副檔名（`.ts/.tsx/.py/.go/...`），提醒 Claude「規劃只產文件、不產 code」。`/product-dev` 執行時會自動建立該標記 |

Hooks 由 `hooks/hooks.json` 在 plugin 安裝時自動載入。在非 product-playbook 專案中完全 no-op，安裝 plugin 不會影響其他 codebase。

### 📄 文件匯入與匯出

**匯入**任何現有文件到規劃流程中 — 無需手動複製貼上：

```
PDF（數位）      → pymupdf 文字擷取（即時、免費）
PDF（向量/掃描） → Claude Vision 語意解析（最佳品質）
PDF（備援）      → Tesseract OCR（可離線使用）
DOCX / PPTX     → Pandoc 轉換
```

**匯出**規劃成果為專業格式：

```
/export pdf   → Playwright 渲染 + pikepdf 書籤（CJK 完美支援）
/export docx  → Pandoc + 參考模板
/export pptx  → Pandoc 投影片生成
/export html  → 互動式 HTML 報告（既有功能）
```

> **為什麼用 Playwright 輸出 PDF？** WeasyPrint 會產生 CJK 亂碼。Playwright（Chromium）渲染完美 — 已在正式環境以繁體中文文件驗證。

### 🔥 既有系統直接規劃（Build 模式殺手級用法）

在既有專案目錄中啟動 **直接實作模式**，Claude Code 會一邊讀取你的 codebase 一邊做產品規劃 — 等於把**產品規劃**和**技術可行性評估**合在同一個流程裡完成：

```
你的既有專案                          Product Playbook
┌─────────────────┐                ┌─────────────────────┐
│ src/             │  ← 自動讀取 →  │ Pre-mortem 風險評估   │
│ db/schema.sql    │  ← 自動讀取 →  │ MVP 範圍定義         │
│ api/routes/      │  ← 自動讀取 →  │ RICE 功能排序        │
│ package.json     │  ← 自動讀取 →  │ User Story 拆解     │
│ CLAUDE.md        │  ← 自動讀取 →  │ 開發交接包（增量）    │
└─────────────────┘                └─────────────────────┘
```

**操作範例：**

```bash
# 1. 進入你的既有專案
cd /path/to/your-existing-project

# 2. 啟動 Claude Code
claude

# 3. 使用直接實作模式，描述你要加的功能
> /product-feature 我想在現有系統加上即時通知功能
```

Claude Code 會自動：
- 掃描你的目錄結構、技術棧、DB Schema
- 基於**真實架構**做 Pre-mortem（而不是憑空想像的風險）
- 產出的 MVP 和 User Story 直接對接現有模組
- 開發交接包是**增量規劃**，不是從零開始

> 💡 **為什麼這很強？** 傳統產品規劃和技術評估是分開的 — PM 寫完企劃丟給工程師，工程師才說「這個做不了」。Build 模式讓規劃過程就建立在真實系統約束之上，省去來回。

### 🔒 安全性內建

開發交接包自動包含安全架構，不再是事後補強：

- **OWASP Top 10 檢查清單** — 輸入驗證、認證授權、XSS/CSRF 防護
- **安全架構段落** — CORS 政策、CSP Headers、Rate Limiting、API 安全中間件
- **.gitignore 模板** — 自動排除 `.env`、credentials、進度檔案
- **Pre-mortem 安全情境** — 資料洩漏、帳號盜用、API 濫用等必考項目

### 📦 跨 Session 產品上下文累積

每次規劃的成果自動保存到 `.product-context.md`，下次開啟時自動載入：

```
第一次規劃（完整模式）→ 儲存 Identity + Core Strategy + Architecture
第二次規劃（功能擴充）→ 自動帶入技術棧和模組，省去重複收集
第三次規劃（改版模式）→ 帶入歷史決策和已知痛點，聚焦差異
```

### 🏢 B2B / B2C 自動調整

確認產品類型後，框架自動適配：

| 面向 | B2C | B2B |
|------|-----|-----|
| Persona | 個人動機分群 | 購買者 + 使用者雙 Persona |
| PMF | DAU/留存/Sean Ellis | 付費客戶數/NRR/NPS |
| North Star | 核心動作完成次數 | ARR / Net Revenue Retention |
| Aha Moment | 首次使用內 | Onboarding / Time-to-Value |

---

## 📊 品質評測結果

透過對比「有 Skill 引導」與「無 Skill 引導」的回應品質，以 AI 評審自動評分，量化 Skill 的實際效益。

### 四次 Iteration 對比

| 評測輪次 | 評測項目數 | 有 Skill 通過率 | 無 Skill 通過率 | 差距（Delta） |
|---------|:--------:|:--------------:|:--------------:|:-----------:|
| Iteration 1（基準） | 6 項 | 100% | 57.4% | +42.6% |
| Iteration 2 | 6 項 | 100% | 63.3% | +36.7% |
| Iteration 3 | 6 項 | 94.1% | 38.2% | +55.9% |
| **Iteration 4（最新）** | **9 項** | **100%** | **31%** | **+69% ✅** |

### Iteration 4 詳細結果（9 項評測 × 49 個期望值）

| 評測項目 | 有 Skill | 無 Skill | Delta |
|---------|:-------:|:-------:|:-----:|
| 模式選擇（三步漸進） | 100% | 0% | +100% |
| 快速模式 JTBD 分析 | 100% | 43% | +57% |
| JTBD 深度（B2B 組織層級） | 100% | 57% | +43% |
| PR-FAQ 撰寫 | 100% | 33% | +67% |
| 改版模式 | 100% | 67% | +33% |
| 品質自檢 Hard Gate | 100% | 0% | +100% |
| **功能擴充模式（新）** | **100%** | **17%** | **+83%** |
| **安全性整合（新）** | **100%** | **25%** | **+75%** |
| **Context Bootstrap（新）** | **100%** | **0%** | **+100%** |

### 關鍵發現

- **品質自檢 Hard Gate**（+100%）：AI 在完成產出後，是否會主動以嚴格標準批判自己的輸出、標記不足並要求改進——無 Skill 時通過率為 0%
- **Context Bootstrap**（+100%）：首次使用時是否會先收集產品基礎資訊再開始規劃，而非直接跳入技術實作——無 Skill 時完全跳過此步驟
- **功能擴充模式**(+83%):是否能識別「在既有產品上加功能」的場景,啟用 4 步精簡流程而非完整 6-11 步——無 Skill 時直接輸出技術方案
- **安全性整合**（+75%）：開發交接包是否包含安全架構、.gitignore 模板、平台特定安全措施——無 Skill 時安全性僅佔一個簡表

> 詳細評測方法與數據見 [`evals/`](./evals/) 目錄。

### Iteration 5：Sub-agent A/B 對照（3 個專家相關評測 × 22 個期望值）

針對 v1.2.0+ 推出的 3 個專家 sub-agent（`discovery-specialist`、`strategy-critic`、`pre-mortem-runner`）所做的聚焦 A/B 測試，量化它們在品質上的邊際貢獻。相同 skill 版本（v1.2.3）、相同 prompt、兩個 arm：

- **有 Sub-agent**：executor 可讀取對應的 `agents/*.md`，並遵循該專家宣告的輸出 schema 與自檢；回應中標記 dispatch。
- **無 Sub-agent**：executor 不得讀取任何 `agents/*.md`，不得提及 delegation；只能用 `SKILL.md` + `commands/` + `references/` 由 orchestrator 自行 inline 處理。

| 評測項目 | 有 Sub-agent | 無 Sub-agent | 差異 |
|-----------|:--------:|:------------:|:-----:|
| Discovery（Persona + JTBD） | 100%（7/7） | 85.7%（6/7） | +14.3% |
| Strategy Critic | 100%（6/6） | 83.3%（5/6） | +16.7% |
| **Pre-mortem（Build Mode 風險評估）** | **100%（9/9）** | **22.2%（2/9）** | **+77.8% ✅** |
| **總計** | **100%（22/22）** | **59.1%（13/22）** | **+40.9%** |

兩個 arm 的 token 消耗幾乎相同（151K vs 154K）——保留專家不會比 inline 處理更貴。

**關鍵發現**

- **Pre-mortem-runner 是 load-bearing**（+77.8%）：少了它，orchestrator 只能產出單薄、未來式的風險清單，缺失 scenario 數量（≥15）、五類別覆蓋、leading-indicator 紀律、低成本上線前實驗、以及過去式「已上線且失敗」敘事框架。結構化的專家 schema 在做真正的工作，光看 `references/` 無法重建。
- **Discovery-specialist 與 strategy-critic 屬於中度貢獻**（+14–17%）：orchestrator 自己處理 Persona+JTBD 與策略批判已可達合理水準。兩個 arm 唯一分歧的 assertion 是 dispatch 契約本身，而非結構性品質。
- **意涵**：3 個專家中，pre-mortem-runner 對品質提升的貢獻最大、最值得保留；另外兩個原則上可以靠加強 reference 文件 fold 回 orchestrator，但因為 token 成本相同，沒有減量誘因。

**Harness 警語**：此評測環境的 `general-purpose` executor 並未暴露 nested `Task`，因此「有 Sub-agent」arm 是以「讀取專家 `agents/*.md` + 標記 dispatch + 遵循 schema inline」近似真實 dispatch。結構性對比是真的，但要完全驗證端到端 Task 工具 dispatch 還需要 top-session 測試。

> 原始 artifacts 與每項 assertion 分歧詳見 [`~/product-playbook-workspace/iteration-3/benchmark.md`](./evals/)。

### Iteration 6：Token 優化（v1.2.5）

一輪 token 縮減迭代。Skill 語意內容不變,但每個 session 的 footprint 更小。目標:在維持 100% 品質的前提下,token 用量減少 ≥25%。

**本輪變更**

- **SKILL.md 瘦身**——將 Sub-Agent Delegation Rules 抽出為 lazy 載入的 `rules-subagent-dispatch.md`;精簡 Hard Gate 描述;整併 Mode Overview 重複內容。eager 進入點 **6,188 → 2,877 tokens(-54%)**。
- **rules-context.md 拆分**——決策邏輯保持 eager(1,594 tokens);冗長的 YAML 模板、Bootstrap 流程與 Conflict UX 腳本移到 lazy `rules-context-template.md`(1,849 tokens,僅在觸發時載入)。
- **rules-quality-review.md 瘦身**——從 1,040 → 817 tokens,改用緊湊的 3 步驟協定與每個框架 1 行的檢查表。
- **專家 agents 瘦身**——移除與 `references/*.md` 重複的內嵌框架知識,改為依需要指向參考檔。每次 dispatch:**discovery-specialist −25%、strategy-critic −18%、pre-mortem-runner −20%**。

**單一 9 步 Full Mode session 的預估節省:**

| 來源 | 之前 | 之後 | 節省 |
|--------|:------:|:-----:|:-----:|
| Eager(SKILL + context + progress) | ~8,800 | ~5,500 | **−3,300** |
| Quality review(×9 step loads) | ~9,360 | ~7,353 | **−2,007** |
| Sub-agent dispatches(3 個專家) | ~9,005 | ~7,106 | **−1,899** |
| **每次 session 合計** | **~27,200** | **~18,900** | **−8,300(−30%)** |

**品質驗證**:依 Iteration 5 結果中品質最敏感的 pre-mortem-runner,在 v1.2.5 瘦身內容上重跑 eval-12。結果為 **9/9 assertions PASS**——涵蓋全部 5 個類別共 16 個 scenario、5 個引用真實 stack 元件的架構落地 scenario、5 個帶有二元判準的低成本上線前實驗,並維持過去式敘事框架。靜態交叉檢查確認 eval-10/11 的 assertions(共 13 項)在瘦身後的 agent prompt 中皆有明確支撐。

**Token 成本取捨**:拆分新增 2 個 lazy 檔案(`rules-subagent-dispatch.md` 978 tokens、`rules-context-template.md` 1,849 tokens),僅在觸發時載入。在最常見的 session 路徑中,這兩個檔案根本不會載入;即使在 Bootstrap 或 Conflict 路徑下,eager 端的節省仍淨為正。

**5 個 i18n 語系同步**(zh-TW、zh-CN、ja、es、ko),保留既有翻譯——結構性瘦身在各語系等比例套用。

### Iteration 7:Eval Harness 韌性強化(Sprint 1 + 2A,v1.2.9)

Harness 層的迭代,不是 skill 層。Skill 語意沒變,變的是**被測量的表面**。目標:解除 4 個一直在悄悄產出 0/0 verdict 的 eval,讓真實品質基線浮出水面。

**Sprint 1 — 解鎖無法測量的群集(`d2023fb`、`cee67cb`):**

4 個 eval(`eval-jtbd-depth`、`eval-prfaq-output`、`eval-subagent-discovery`、`eval-subagent-premortem`)每次都產出 0 pass / 0 fail,在彙總分數中與「沒問題」無法區分。三個原因:

1. **CI headless 模式缺少 sub-agent** — CI 把 skill 裝到 `~/.claude/skills/`,卻沒把 `agents/*.md` 複製到 `~/.claude/agents/`。`claude -p` 因此無法透過 `Task` 派發,orchestrator 只能默默 inline 執行。
2. **Specialist-dispatch hook 在 `claude -p` 不會載入** — plugin 層的 `hooks/` 在 headless 模式不會載入,只有 user 層 `~/.claude/settings.json` 的 UserPromptSubmit hook 會。CI 現在會在每次 behavioral run 之前以程式碼方式把 dispatch hook 註冊到 user 層。
3. **Response + judge timeout 太緊** — 180s response / 120s judge 會把長篇 Discovery、Pre-mortem 輸出中途切斷,judge 看到截斷字串就吐出 0/0。提升到 600s / 240s,且非 JSON 輸出時重試一次。

同時也從 evals 10/11/12 刪掉「orchestrator 必須透過 Task 派發」這類程序性 expectation——在 `claude -p` 沒有 nested Task 介面,無法驗證,也不是我們最終在意的性質。留下的 expectation 都針對 specialist 應產出的**輸出品質**。

**Sprint 2A — judge 韌性 + CI 上限(`f973939`):**

PR #9 review 之後的兩個跟進修正:

1. **Judge 修復重試保留原始 context** — `claude -p` 是無狀態的,所以修復 prompt 現在會重新帶入完整原始 `judge_prompt`(response + expectations)加上前一次的 malformed output。新的 `_judge_output_complete()` 檢查會拒絕「沒有完整 N 個 indexed expectation」的回應,避免 model 在第一次輸出無法救援時憑空捏造一份看起來合理的 verdict。
2. **CI `behavioral-eval` job timeout 90 → 120 分鐘** — 最壞情況 = 12 evals / 2 workers × (600s response + 240s judge + 240s repair) ≈ 108 分鐘,先前 90 分鐘上限可能默默 cancel 整輪 run。120 分鐘給 setup + artifact upload 留 ~10 分鐘餘裕。

**新可見的基線**(本機 run,2026-05-28):**0 / 100** `at-risk`、**13 / 33** expectation 通過、**6 critical + 14 warning** 失敗。彙總分數並沒有退步,退的是**可見**分數——四個原本貢獻 0/0 的 eval 現在開始產出真實 signal。這 6 個 critical 失敗就是 Stage 2 明確的待修清單:三層 JTBD(functional / emotional / social)、B2B 組織層 Jobs、B2B buyer vs user persona 分離、Discovery scope 守備、pre-mortem leading-indicator 紀律。逐項細節見 [`docs/sprint1-local-eval-2026-05-28.md`](./docs/sprint1-local-eval-2026-05-28.md)。

**Harness 改進住在 `evals/` 與 `.github/workflows/`,不會發到 npm。** 版本不需要再往 v1.2.9 之上 bump(v1.2.9 已經包含 user-level hook 與 evals 10/11/12 的 scope 調整)。

**5 個 i18n 語系同步**(zh-TW、zh-CN、ja、es、ko)。

### Iteration 8:Closed-Loop 自我修正 pipeline(v1.2.14)

Stage 1(Sprint 1)讓失敗**可見**。Stage 2(手動)驗證了模式:critical / warning 失敗可以靠在對應 reference 加上 **Hard Gate 區塊**(規則 + FAIL 範例 + ✅ 範例)然後鏡像到 5 i18n 來翻過去。Iteration 8 把這個迴圈端到端自動化並 ship 結果。

**現在存在的 pipeline**(每一步都是 `scripts/` 下的 script,以 `npm run` 形式暴露):

```
[手動 eval run]
       ↓
eval-results.behavioral.json
       ↓
scripts/eval-debt-report.py        ← 失敗 → 檔案歸屬(無 LLM)
       ↓ 每個檔案的修補 backlog
scripts/patch-proposer.py          ← LLM 提案 Hard Gate diff(預設 dry-run)
       ↓ EN diff 等人工 review
references/*.md 由人類審查後套用 diff
       ↓
scripts/i18n-mirror-apply.py       ← LLM 把 EN 變動傳到 5 語(預設 dry-run)
       ↓ 5 語 diff
i18n/*/references/*.md 由 --apply 寫回
       ↓
scripts/i18n-drift-report.py       ← 確定性 detector(無 LLM)驗證同步
       ↓ exit 0 = 乾淨
[手動 eval 重跑]
       ↓
scripts/eval-lift-report.py        ← per-expectation delta + 分數 vs 真實 lift 歸因
```

兩個用 LLM 的工具(`patch-proposer`、`i18n-mirror-apply`)預設都是 dry-run,搭配 `--max N` 爆炸半徑上限與 `--apply` 寫檔閘門,確保每次寫入都有人在迴圈內。

**CI 政策**同步調整:`eval-gate.yml` 改成 `workflow_dispatch` only(2026-05-28 的事件 — auto-run on PR + push 在 Stage 2.3 smoke 測試時悄悄燒光維護者的 5 小時滾動 subscription 配額 — 是觸發點)。一個新的輕量 workflow `i18n-drift-check.yml` *依然*在 PR / push 動到 `references/` 或 `i18n/` 時 auto-fire,因為 detector 是確定性 Python 沒有 API 呼叫 — 通知模式,永不阻塞 merge。

**Closed-loop 跑出來的數字**(本機 run,2026-05-29,`--runs 1`,完整 12 eval,分數 artifact [`docs/post-closed-loop-eval-2026-05-29.md`](./docs/post-closed-loop-eval-2026-05-29.md),lift 歸因 [`docs/eval-lift-closed-loop.md`](./docs/eval-lift-closed-loop.md)):

| Run | 覆蓋 | Expectation 通過 | Critical | Warning | 彙總分數 |
|---|---|---|---|---|---|
| Sprint 1 baseline(2026-05-28) | 4 eval(局部) | 13 / 33(39 %) | 6 | 14 | 0 / `at-risk` |
| **Closed-loop 之後(2026-05-29)** | **12 eval(完整)** | **69 / 82(84 %)** | **5** | **6** | **0 / `at-risk`** |

兩輪的彙總分數都壓在 0(累積嚴重度扣分都超過 100 點預算),但底層的移動很劇烈。在跟 Sprint 1 baseline **共享的 4 個 eval**(apples-to-apples,31 paired expectation):

- **17 improved**(fail → pass),含 4 個 Stage 2 critical backlog:三層 JTBD、B2B buyer-vs-user 分離、Discovery scope 守備、B2B 組織層 Jobs
- **2 regressed** — 都在 `eval-subagent-premortem` 的 category coverage;`--runs 1` 的 LLM variance,`--runs 3` majority vote 預期會洗掉
- **Net hard lift: +95 點**(gain +125、loss −30)

新加入覆蓋的 8 個 eval(51 個 expectation)補上可見度缺口;只剩 `eval-mode-selection`、`eval-security-awareness`、`eval-context-bootstrap`、`eval-subagent-premortem` 還掛著 5 個 critical。那些就是下一輪 `patch-proposer` 的目標。

**5 個 i18n 語系同步。**

---

## 🧪 開發與評測

`evals/` 目錄包含兩套互補的測試集和一個確定性計分模組。

**本地（免費，推薦）**：用 `claude` CLI 搭配你的 Claude Pro/Max 訂閱（先 `claude login` 一次）跑這些 script。不需要 API key、沒有額外成本。整套 eval 系統就是設計來在每次發版前本地跑一遍。

**CI（選用，不額外計費）**：`.github/workflows/eval-gate.yml` 會在每個 PR 與每次 push 到 `main`（含 `package.json` 變動）時跑這兩套，把分數寫進 workflow 的 Job Summary。**不擋 merge、不擋 publish** — 看到結果後由維護者決定要不要調整。CI 同樣走你的 Claude Pro/Max 訂閱（不需 API key、沒有按 token 計費的成本）：一次性設定為本機 `claude setup-token` 產生長期 token，把它加進 repo secret `CLAUDE_CODE_OAUTH_TOKEN`。沒設 secret 時 eval job **會乾淨地 skip**（灰色 ⏭️），不會出現誤導的紅叉。

### 本地執行

```bash
# 推薦：一個命令跑完兩套
npm run eval

# 或分開跑
npm run eval:trigger      # ~5–15 分鐘 — skill 是否自動觸發
npm run eval:behavioral   # ~10–40 分鐘 — claude 同時當 assistant 和 judge
npm run eval:zh-TW        # 用 zh-TW 評測集跑 behavioral eval
npm run eval:quick        # 只跑 1 次，不取多數決（快速 iterate 用）
npm run eval:test         # 計分模組單元測試

# 需要更細的 flag 控制時，直接呼叫底層 Python 腳本：
python3 evals/run_behavioral_eval.py --only 11        # debug 單一 eval id
python3 evals/run_behavioral_eval.py --fail-on none   # 只報告，不 exit 1
python3 evals/run_trigger_test.py --eval-file evals/trigger-eval-fuzzy.json
```

本地預設 `--runs 3`（多數決可吸收 LLM 變異性）；`claude` CLI 走你的 Claude Pro/Max OAuth session（`claude login`），沒有按 token 計費的成本。CI 用 `--runs 1`，靠同一個訂閱透過 `CLAUDE_CODE_OAUTH_TOKEN` secret 認證（用 `claude setup-token` 一次性產生）。

### Severity 與計分

`evals.json` 裡每個 expectation 都標一個 severity：

| Severity | 失敗扣分 | 適用情境 |
|---|---|---|
| `critical` | −15 | Hard Gate 違反、Mode dispatch 錯誤、B2B buyer/user 分開、Security default-on、框架完整性（JTBD 三層、Rumelt diagnosis、pre-mortem 15+ scenarios）|
| `warning`  | −5  | 品質深度與結構（多數 expectations）|
| `info`     | −1  | 語言偵測、Progress indicator 格式 |

起點 100 分，按失敗 deduct，clamp 在 0–100。

| Band | 範圍 | 含意 |
|---|---|---|
| 🟢 `healthy` | ≥ 90 | 最多一個 critical 失敗 |
| 🟡 `needs-attention` | ≥ 70 | 兩個 critical 以下或數個 warning |
| 🔴 `at-risk` | < 70 | 三個以上 critical；gate 應失敗 |

### `--fail-on` 語意

| Flag 值 | Runner 在以下情況 exit non-zero |
|---|---|
| `critical` | 任一 critical expectation 失敗（CI 預設）|
| `any` | 任一 expectation 失敗（不分 severity）|
| `none` | 永不失敗；本地探索 informational mode |

所有計分邏輯集中在 `evals/compute_eval_score.py` 這個單一來源，避免兩個 runner 各自實作造成 drift。

### 發版 checklist

bump `package.json` version 之前（push 到 `main` 且 `package.json` 變動會觸發 `npm publish`）：

1. `npm run eval` — 取得當前 trigger + behavioral 分數
2. 任一 **critical** expectation 失敗 → 發版前先查清楚並修掉
3. 只是 warning 或 info 退步 → 自行判斷；若接受退步，在 commit message 寫清楚理由
4. 修完 commit，bump version，然後 `git push`

---

## 💬 可用指令一覽

### ⌨️ Claude Code CLI Slash Commands

安裝 Skill 後自動可用的主指令：

| 指令 | 說明 |
|------|------|
| `/product-playbook` | 啟動完整產品規劃引導流程 |

如需更細粒度的快捷指令，可安裝 `commands/` 資料夾中的預建 slash commands：

```bash
# 安裝所有 slash commands
cp -r product-playbook/commands/* ~/.claude/commands/
```

| 指令 | 說明 |
|------|------|
| `/product-quick <描述>` | 快速模式 — 30 分鐘內跑完 JTBD → PR-FAQ → North Star |
| `/product-full <描述>` | 完整模式 — 完整產品企劃(9–11 步;Journey Map 預設啟用) |
| `/product-revision <描述>` | 改版模式 — 既有產品改版優化 |
| `/product-build <描述>` | 直接實作模式 — 跳過 Discovery，直接進解法 |
| `/product-feature <描述>` | 功能擴充模式 — 在既有產品新增單一功能（4 步） |
| `/product-prd` | 產出 PRD 工程師交付包 |
| `/product-report` | 產出 HTML 企劃報告 |
| `/product-dev` | 產出開發交接包（CLAUDE.md + TASKS.md + TICKETS.md） |

### 💬 對話中的自然語言指令

#### 流程控制
- `切換到 [框架]` — 立即切換框架
- `跳過這個步驟` — 跳過當前步驟
- `回到 [步驟名]` — 回到任意步驟修改
- `幫我簡化` / `幫我展開` — 調整深度

#### 產出指令
- `產出報告` — HTML 企劃報告
- `產出 PRD` — 工程師交付包（含流程圖 + DB Schema + Wireframe）
- `產出簡報` — PowerPoint 簡報
- `進入開發` — 開發交接包（CLAUDE.md + TASKS.md）
- `/export pdf` — 匯出為 PDF，含專業排版、封面、目錄及書籤
- `/export docx` — 匯出為 Word 文件
- `/export pptx` — 匯出為 PowerPoint 簡報
- `/parse [file]` — 解析 PDF/DOCX/PPTX 為 Markdown 以供規劃使用

#### 分析指令
- `幫我做完整性評估` — 評估規劃完整度
- `幫我找出假設` — 列出未驗證假設
- `做一次 Pre-mortem` — 事前驗屍
- `這個產品在 PMF 哪個等級？` — PMF 判斷
- `幫我找出瓶頸` — Aha Moment 障礙分析

---

## 🤝 Contributing

歡迎貢獻！以下是幾個特別歡迎的方向：

- 🌍 **多語言支援** — 將框架翻譯為其他語言
- 📐 **新增框架** — 加入更多產品管理框架
- 📝 **範例補充** — 在各框架中加入更多填寫範例
- 🐛 **Bug 回報** — 使用過程中發現的邏輯問題或遺漏
- 💡 **體驗改善** — 互動流程、指令設計的改善建議

### 如何貢獻

1. Fork 本 repo
2. 建立你的 feature branch (`git checkout -b feature/amazing-framework`)
3. Commit (`git commit -m 'feat: add amazing framework'`)
4. Push (`git push origin feature/amazing-framework`)
5. 開啟 Pull Request

### 貢獻指南

- reference 檔案中的框架內容必須註明出處
- 新增框架需同步更新 SKILL.md 的框架索引和步驟序列
- 品質自檢清單使用 ✅ / ❌ 格式
- 支援多語言：繁體中文與英文並行維護

---

## 📚 框架來源與延伸學習

本專案的框架整理自以下思想家的公開內容：

| 思想家 | 核心貢獻 | 推薦閱讀 |
|--------|---------|---------|
| Teresa Torres | Continuous Discovery、OST | 《Continuous Discovery Habits》 |
| Shreyas Doshi | LNO、Pre-mortem、三層次產品工作 | Lenny's Podcast Ep.3 |
| Gibson Biddle | DHM Model、GEM | Lenny's Podcast |
| April Dunford | Positioning Framework | 《Obviously Awesome》 |
| Todd Jackson | 四級 PMF、Four P's | Lenny's Podcast |
| Richard Rumelt | Good Strategy / Bad Strategy | 《Good Strategy Bad Strategy》 |
| Marty Cagan | Empowered Teams | 《Inspired》《Empowered》 |
| Clayton Christensen | Jobs to Be Done | 《Competing Against Luck》 |
| Amazon | Working Backwards / PR-FAQ | 《Working Backwards》 |
| Sean Ellis | Sean Ellis Score、Growth | 《Hacking Growth》 |
| Lenny Rachitsky | Shape / Ship / Synchronize | Lenny's Newsletter + Podcast |

---

## 📄 License

本專案採用 [MIT License](LICENSE) 授權 — 免費使用、修改、分發，不設限。

---

## ⭐ Star History

如果這個專案對你有幫助，請給個 ⭐ 讓更多人看到！

---

<p align="center">
  <strong>Built with ❤️ for Product Managers who want to build things that matter.</strong>
</p>

---

Copyright (c) 2026 Charles Chen.
