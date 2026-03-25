# 一個開源 Claude Skill 如何取代你的整個 PM 工具鏈 — 22 個框架、6 種執行模式、獨家 Change Propagation Engine

*每個人都有 AI 副駕駛，卻沒人有 AI 產品經理*

⭐ **GitHub**: [github.com/kaminoikari/product-playbook](https://github.com/kaminoikari/product-playbook)

📦 **立即安裝**: `npx product-playbook`

---

# Part I: 背景

## AI 自動化了簡單的部分，困難的留給直覺

GitHub Copilot 突破 1.8M 付費訂閱、Cursor 拿了 $900M 融資、Windsurf、Devin、Replit Agent 接連拿到天價估值。整個產業瘋狂投入一個命題：**讓 AI 把規格變成程式碼**。但「寫程式之前」的階段呢？決定要做什麼、搞清楚為誰做、理解為什麼值得做 — 這些產品最上游的決策，仍然靠直覺和散裝的 ChatGPT 對話。

**最貴的那行程式碼，不是 bug 最多的那行 — 是解決錯誤問題的那行。** CB Insights 經典研究：35% 的新創失敗因為「沒有市場需求」。AI 讓我們能更快地做出沒人要的東西。

一個典型 PM 的工作日：Notion 寫規格、ChatGPT 做腦力激盪、Figma 對原型、Jira 開票、Google Docs 寫 PRD。五個工具、五個斷裂的脈絡、零個一致性引擎。改了 JTBD，PR-FAQ 立刻過時，North Star 需要調整，MVP 範圍要重畫 — 但誰會去更新？每份文件活在自己的宇宙裡，沒有依賴圖、沒有傳播機制。

**如果一個 AI Skill 能取代整個拼裝車工具鏈，一路橋接到開發交接？**

---

# Part II: 產品介紹

## 是什麼

[The Product Playbook](https://github.com/kaminoikari/product-playbook) 是一個 **Claude AI Skill** — 安裝在本地的結構化指令集，賦予 Claude 系統化產品規劃能力。MIT 開源、支援 6 語言、零訂閱費。

## 六大執行模式

| 模式 | 步驟數 | 時間 | 適合場景 |
|------|--------|------|----------|
| 🚀 **快速模式（Quick）** | 3 | ~30 分鐘 | 快速驗證、pitch 準備 |
| 📦 **完整模式（Full）** | 20 | 數小時 | 完整產品企劃 |
| 🔄 **改版模式（Revision）** | 12 | 1-2 小時 | 現有產品優化 |
| ✏️ **自訂模式（Custom）** | 4-16 | 彈性 | 補特定框架缺口 |
| ⚡ **直接實作模式（Build）** | 7 | ~1 小時 | 問題已知，需要執行 |
| 🔧 **功能擴充模式（Feature Extension）** | 4 | ~30 分鐘 | 為現有產品加功能 |

## 22 個框架：Lenny's Podcast 去蕪存菁

我打造這個工具的起點是一個簡單的觀察：**PM 不缺框架，缺的是框架之間的連結。**

我花了大量時間研究 Lenny's Podcast — 那些集數邀請了全球最頂尖的 PM：Teresa Torres、Shreyas Doshi、Gibson Biddle、April Dunford、Marty Cagan、Richard Rumelt。我看了數百小時最頂尖 PM 的分享，發現很多框架有重疊和冗餘。於是我去蕪存菁，只留下真正驅動產品決策的 22 個，然後按產品規劃的邏輯順序系統化連結 — 每個框架的產出餵養下一個框架的輸入：

- **理解使用者**：JTBD、Persona、User Journey Map、Continuous Discovery Habits、Opportunity Solution Tree
- **定義問題**：April Dunford Positioning、HMW
- **解法設計**：Working Backwards / PR-FAQ、Pre-mortem、GEM Model、RICE Scoring、MVP Definition
- **策略**：Strategy Blocks、Good Strategy Kernel、DHM Model、Empowered Teams
- **度量與交付**：North Star Metric、Three-Layer Signal Metrics、Aha Moment、Four-level PMF、Sean Ellis Score、GTM Strategy

**這些不是隨機拼湊的清單。它們是被實戰驗證過的方法論，由系統化的依賴關係串起來。**

## 給誰用

Solo PM、indie hacker、startup founder、product-oriented 工程師、一個人扛產品規劃、沒有資深 PM 可以請教的人。The Product Playbook 就是你的 AI 資深 PM 教練。

---

# Part III: 核心差異化 — TOP 5

這些不是 nice to have，是讓 The Product Playbook 和所有其他工具有根本差異的能力。

## 1. Change Propagation Engine（變更傳播引擎）

你改了 JTBD，然後呢？在 Notion 和 Google Docs 的世界裡，沒人記得所有依賴關係。The Product Playbook 知道。當你修改任何上游步驟，系統根據完整的依賴圖自動標記所有受影響的下游產出：

```
修改 Persona / JTBD → 標記：HMW、Positioning、PR-FAQ、North Star、產品規格摘要
修改 PR-FAQ / 解法 → 標記：Pre-mortem、GEM/RICE、MVP、Aha Moment、產品規格摘要
修改 MVP           → 標記：User Story、DB Schema、產品規格摘要
```

不是全部自動改寫，而是告訴你「這些地方因為上游變更可能需要調整」，讓你做決定。**這一個功能就值得整個 Skill 的存在。沒有其他 PM 工具有依賴圖。**

## 2. Dev Handoff Package（開發交接包）

PM 和工程之間的交接不再是「把文件丟過牆」。一個指令生成工程師可以直接開工的結構化開發包：CLAUDE.md（Claude Code 專案上下文）、TASKS.md（分階段交付）、TICKETS.md（Jira/Linear 格式票單）、ARCHITECTURE.md（DB Schema + API + 目錄結構）、PRD.md。安全性內建：OWASP Top 10 清單、`.gitignore` 範本、認證/CORS/CSP 架構。

## 3. Quality Hard Gates（品質硬閘門）

每個步驟完成後，AI 執行品質自我審查。硬規則：**至少一項必須標記為失敗。** 如果全部通過，系統必須主動指出最薄弱的環節。為什麼？因為沒有這條規則，AI 每次都說「看起來不錯！」 — 就像不敢說實話的 junior PM。Benchmark 中，沒有 Skill 的 Claude **從不批評自己的產出**，通過率 0%。

## 4. Codebase-Aware Planning（程式碼感知規劃）

在現有專案中啟動，系統自動掃描 `package.json`、`schema.sql`、`api/routes/` 等檔案，偵測技術棧。Pre-mortem 風險不是假設性的「可能有效能問題」，而是「你的 PostgreSQL schema 缺少這個索引」。MVP 範圍引用你的實際模組。開發交接是增量式的，不是 greenfield。**產品規劃和技術現實在同一個流程中結合。**

## 5. Decision Consistency Check（決策一致性檢查）

產出最終文件前，系統執行跨步驟驗證。你的 JTBD 說目標是 freelancer，但 PR-FAQ 在講 agency ，系統抓到矛盾。PR-FAQ 承諾了「自動生成報告」，但 MVP 把它放在「不做清單」，系統浮出問題。多數 PM 不是故意讓文件不一致，是在長時間規劃中沒有系統在做交叉檢查。

---

# Part IV: Benchmark 實證

說了這麼多，有效嗎？讓數據來說話。

測試套件（開源在 `evals/` 目錄）：9 個測試情境、49 項期望值、同一個 Claude 模型、唯一變數是 Skill 是否安裝。

| 測試項目 | 有 Skill | 無 Skill | 差距 |
|----------|:--------:|:--------:|:----:|
| 模式選擇（漸進式確認） | 100% | 0% | **+100%** |
| 快速模式 JTBD 分析 | 100% | 43% | +57% |
| JTBD 深度（B2B + Five Whys） | 100% | 57% | +43% |
| PR-FAQ 撰寫品質 | 100% | 33% | **+67%** |
| 改版模式識別 | 100% | 67% | +33% |
| 品質自我檢查硬閘門 | 100% | 0% | **+100%** |
| 功能擴充模式 | 100% | 17% | **+83%** |
| 安全整合 | 100% | 25% | **+75%** |
| 上下文引導 | 100% | 0% | **+100%** |

**整體：100% vs. ~27% — 三項 +100% 差距代表沒有 Skill 時根本不存在的能力。** 不是做得不好，是完全沒有。Skill 不是拐杖 — 它是 GPS 和「我覺得應該左轉」的差別。

---

# Part V: 競品比較

| 維度 | Product Playbook | ChatPRD | PM-Skills (Dean) | Lenny's Skills | pm-skills | Notion AI |
|------|:---:|:---:|:---:|:---:|:---:|:---:|
| PM 框架數 | 22 | ~5 | 46 | 86 | 27 | 0 |
| 連貫工作流引擎 | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Change Propagation | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 執行模式數 | 6 | 1 | N/A | N/A | 1 | N/A |
| Dev Handoff 整合 | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 程式碼感知規劃 | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Quality Hard Gates | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 團隊協作 | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |
| 定價 | Free (MIT) | $15-24/月 | Free | Free | Free | $10/月+ |

市場上的工具分三類：

1. **廣而淺**（Lenny's 86 個 skill、Dean 46 個，但彼此獨立，沒有連貫工作流）
2. **深而窄**（ChatPRD 做 PRD 很好，但不做 JTBD、Pre-mortem、開發交接）
3. **通用型**（Notion AI 不知道什麼是 PR-FAQ 格式）

The Product Playbook 佔據獨特位置：深度 + 連貫 + 整合。公正地說，ChatPRD 贏在團隊協作，Lenny's Skills 贏在主題廣度。**沒有工具在每個面向都最好，選擇取決於你最需要什麼。**

---

# Part VI: 開始使用

**步驟 1：安裝**

```bash
npx product-playbook
```

**步驟 2：打開 Claude Code，輸入：**

```
我想做一個產品
```

**步驟 3：跟隨引導流程。** 選擇模式、描述產品、讓系統逐步引導你。

快速模式 30 分鐘有方向，完整模式一個下午有完整企劃。

**給 indie hacker**：30 分鐘驗證你的想法值不值得投入一個週末。**給 PM**：22 個框架系統化連結，Change Propagation Engine 確保整個企劃保持一致。**給工程主管**：直接在你的程式碼上做產品規劃，產出工程團隊可以立刻開工的交接包。

---

⭐ **GitHub**: [github.com/kaminoikari/product-playbook](https://github.com/kaminoikari/product-playbook)

📦 **立即安裝**: `npx product-playbook`

*The Product Playbook 以 MIT 授權開源。由 Charles Chen 打造。*

---

如果喜歡這篇文章，請幫我拍手1–10下。
如果喜歡閱讀關於新創公司/產品經理相關主題的話，請幫我拍手10–30下。
如果希望看到更多的話，請幫我大力拍手30–50下。
也請記得 Follow 我 Charles Chen，讓我與你分享更多好知識😊
非常歡迎你在文章底下留言，我很樂意也很期待跟你討論或聊天！
