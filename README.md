# 🎯 The Product Playbook

**世界級產品規劃 AI Skill — 從 Idea 到開發，一套框架全搞定**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://code.claude.com)
[![Claude.ai](https://img.shields.io/badge/Claude.ai-Custom%20Skill-blue)](https://claude.ai)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

> 整合 Lenny's Podcast 歷來最重要的 PM 框架（Teresa Torres、Shreyas Doshi、Gibson Biddle、April Dunford、Todd Jackson、Marty Cagan、Richard Rumelt 等），讓 AI 成為你的資深產品經理教練。

---

## ✨ 這是什麼？

The Product Playbook 是一個 **Claude AI Skill**，能夠系統性地引導你完成從 0 到 1 的產品規劃。它不只是一個提示詞（prompt），而是一套完整的互動式框架引導系統，包含：

- 🧭 **5 種執行模式** — 從 30 分鐘快速驗證到完整企劃
- 📐 **22 個產品框架** — 涵蓋 Discovery → Define → Develop → Deliver 全流程
- 🔄 **變更傳播引擎** — 修改任何步驟，自動更新所有下游產出
- 📎 **檔案智慧整合** — 上傳數據、截圖、文件，AI 自動整合到對應步驟
- 🔗 **開發銜接** — 產出 CLAUDE.md + TASKS.md + TICKETS.md，無縫銜接 Claude Code 開發
- 📊 **多格式產出** — HTML 報告、PRD、PowerPoint、開發交接包

**用一句話觸發整個流程：**

```
我想做一個產品
```

---

## 🎬 Demo

<p align="center">
  <img src="assets/demo.gif" alt="The Product Playbook Demo — Quick Mode" width="800">
</p>

> 上圖展示**快速模式**：一句指令 → JTBD 陳述 → PR-FAQ → North Star → 一頁式方向摘要，約 30 分鐘內完成。

---

## 🚀 快速開始

### 方法一：Claude.ai 自訂 Skill

1. 下載本 repo 的 zip 檔
2. 前往 [Claude.ai](https://claude.ai) → 設定 → 自訂 Skill
3. 上傳整個 `the-product-playbook/` 資料夾
4. 在對話中說「我想做一個產品」即可觸發

### 方法二：Claude Code Skill（推薦）

| 方式 | 適合誰 | 需要什麼 |
|------|--------|----------|
| ① 複製貼上 | 新手 | 只要開 Claude Code |
| ② 一鍵安裝 | 開發者 | 終端機 |
| ③ 手動安裝 | 想自訂路徑 | 終端機 + git |

#### ① 複製貼上安裝（最簡單）

啟動 Claude Code 後，直接貼上以下內容，Claude 會自動幫你完成安裝：

```
請幫我安裝 the-product-playbook skill：
git clone https://github.com/kaminoikari/the-product-playbook.git /tmp/the-product-playbook
mkdir -p ~/.claude/skills ~/.claude/commands
cp -r /tmp/the-product-playbook ~/.claude/skills/the-product-playbook
cp /tmp/the-product-playbook/commands/* ~/.claude/commands/
rm -rf /tmp/the-product-playbook
```

> 💡 更新也是貼上同一段，重新執行即可。

#### ② 一鍵安裝（終端機）

```bash
# curl
curl -fsSL https://raw.githubusercontent.com/kaminoikari/the-product-playbook/main/install.sh | bash

# npx（需要 Node.js）
npx the-product-playbook
```

更新也是同一行指令，重新執行即可。

解除安裝：

```bash
curl -fsSL https://raw.githubusercontent.com/kaminoikari/the-product-playbook/main/install.sh | bash -s -- --uninstall
# 或
npx the-product-playbook --uninstall
```

#### ③ 手動安裝

```bash
git clone https://github.com/kaminoikari/the-product-playbook.git
mkdir -p ~/.claude/skills ~/.claude/commands
cp -r the-product-playbook ~/.claude/skills/the-product-playbook
cp the-product-playbook/commands/* ~/.claude/commands/
```

安裝完成後，在 Claude Code 中觸發：

```bash
# Skill 主指令
> /the-product-playbook

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
the-product-playbook/
├── SKILL.md                          # 主控核心：模式定義、步驟序列、指令系統
├── LICENSE                           # MIT License
├── README.md                         # 本文件
├── assets/
│   └── demo.gif                      # README 動態展示圖
├── commands/                         # Claude Code CLI Slash Commands（可選安裝）
│   ├── product-quick.md              # /product-quick — 快速模式
│   ├── product-full.md               # /product-full — 完整模式
│   ├── product-revision.md           # /product-revision — 改版模式
│   ├── product-build.md              # /product-build — 直接實作模式
│   ├── product-prd.md                # /product-prd — 產出 PRD
│   ├── product-report.md             # /product-report — 產出 HTML 報告
│   └── product-dev.md                # /product-dev — 產出開發交接包
└── references/
    ├── 00-opportunity-check.md       # 機會評估 + DHM Model
    ├── 01-strategy.md                # Strategy Blocks + Rumelt + OKR
    ├── 02-discovery.md               # Persona + JTBD + OST + Journey Map
    ├── 03-define.md                  # 痛點 + Positioning + HMW + 機會評估
    ├── 04-develop.md                 # PR-FAQ + Pre-mortem + RICE + MVP + PRD
    ├── 05-deliver.md                 # North Star + PMF + GTM + 商業模式 + 產品規格
    ├── 06-html-report.md             # HTML 企劃報告產出規格
    └── 07-dev-handoff.md             # 開發銜接：CLAUDE.md + TASKS.md + 架構
```

---

## 🧭 五種執行模式

| 模式 | 步驟數 | 耗時 | 適合情境 |
|------|--------|------|---------|
| 🚀 **快速模式** | 3 步 | ~30 分鐘 | 快速驗證想法、準備簡報 |
| 📦 **完整模式** | 20 步 | 數小時 | 新產品規劃、重大改版 |
| 🔄 **改版模式** | 12 步 | 1-2 小時 | 既有產品改版優化 |
| ✏️ **自訂模式** | 4-16 步 | 依選擇 | 補足特定環節 |
| ⚡ **直接實作** | 7 步 | ~1 小時 | 問題已知，直接進解法 |

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
> /product-build 我想在現有系統加上即時通知功能
```

Claude Code 會自動：
- 掃描你的目錄結構、技術棧、DB Schema
- 基於**真實架構**做 Pre-mortem（而不是憑空想像的風險）
- 產出的 MVP 和 User Story 直接對接現有模組
- 開發交接包是**增量規劃**，不是從零開始

> 💡 **為什麼這很強？** 傳統產品規劃和技術評估是分開的 — PM 寫完企劃丟給工程師，工程師才說「這個做不了」。Build 模式讓規劃過程就建立在真實系統約束之上，省去來回。

### 🏢 B2B / B2C 自動調整

確認產品類型後，框架自動適配：

| 面向 | B2C | B2B |
|------|-----|-----|
| Persona | 個人動機分群 | 購買者 + 使用者雙 Persona |
| PMF | DAU/留存/Sean Ellis | 付費客戶數/NRR/NPS |
| North Star | 核心動作完成次數 | ARR / Net Revenue Retention |
| Aha Moment | 首次使用內 | Onboarding / Time-to-Value |

---

## 💬 可用指令一覽

### ⌨️ Claude Code CLI Slash Commands

安裝 Skill 後自動可用的主指令：

| 指令 | 說明 |
|------|------|
| `/the-product-playbook` | 啟動完整產品規劃引導流程 |

如需更細粒度的快捷指令，可安裝 `commands/` 資料夾中的預建 slash commands：

```bash
# 安裝所有 slash commands
cp -r the-product-playbook/commands/* ~/.claude/commands/
```

| 指令 | 說明 |
|------|------|
| `/product-quick <描述>` | 快速模式 — 30 分鐘內跑完 JTBD → PR-FAQ → North Star |
| `/product-full <描述>` | 完整模式 — 完整 20 步產品企劃 |
| `/product-revision <描述>` | 改版模式 — 既有產品改版優化 |
| `/product-build <描述>` | 直接實作模式 — 跳過 Discovery，直接進解法 |
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
- 保持繁體中文為主要語言

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
