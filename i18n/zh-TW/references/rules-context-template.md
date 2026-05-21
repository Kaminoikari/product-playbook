# 📦 產品上下文 — 模板與詳細 UX 腳本

> Lazy-loaded reference。依 `rules-context.md` §8 的觸發表觸發。僅包含 routine session 啟動不需要的 verbose YAML/markdown 格式與 UX 腳本。

## 檔案格式

```markdown
# Product Context
<!-- Auto-maintained by product-playbook. Do not delete. -->
<!-- last-updated: [ISO timestamp] -->

## Identity
- **Product name**: [name]
- **Product type**: [B2C / B2B / B2B2C / Internal tool]
- **One-liner**: [一句話描述]
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
- **North Star Metric**: [指標名 + 定義]
- **Aha Moment**: [描述]

## Architecture & Tech Stack
- **Tech stack**: [語言、框架、基礎設施]
- **Key modules**: [主要模組清單]
- **Data model highlights**: [核心資料實體，若已知]

## Decision History
<!-- Append-only. 每次完成流程追加一筆。 -->

### [ISO date] - [流程類型: Full/Quick/Revision/Feature Extension/Custom/Build]
- **Scope**: [規劃/變更範圍]
- **Key decisions**: [重大決策]
- **Risks identified**: [風險]
- **MVP boundary**: [做什麼 / 不做什麼]
- **Success metrics**: [成功指標 + 目標值]

## Language Preference
- **Installed language**: [從 .lang 檔案自動偵測或使用者的語系]
- **User's preferred language**: [使用者溝通時使用的語言]

## Accumulated Insights
- **Known pain points**: [痛點清單，附來源]
- **User feedback themes**: [跨 session 的反饋主題]
- **PMF status**: [最近評估等級 + 日期]
- **Security posture**: [認證/授權方式、已知漏洞]
- **Technical debt**: [跨 session 累積的技術債]
```

---

## Bootstrap（情境 2 專用）

當使用者進入**功能擴充**或**改版模式**但沒有 `.product-context.md` 時，在模式 S1 之前插入「Step 0」。

**呈現方式**：
```
📦 這是你第一次在此專案使用產品規劃工具。為了讓後續流程更有效率，
我先收集一些基本產品資訊（約 2-3 分鐘），之後會自動保存供未來使用。
```

### 漸進式收集（不要一次丟出所有問題）

**Round 1（所有模式必問）**：
- 產品叫什麼名字？
- 一句話描述它做什麼？
- 產品類型？（B2C / B2B / B2B2C / 內部工具）

**Round 2（功能擴充必問，改版選問）**：
- 使用什麼技術棧？（語言、框架、資料庫、基礎設施）
- 主要模組或服務有哪些？

**Round 3（改版必問，功能擴充選問）**：
- 目前有 DAU/MAU 或留存率數據嗎？
- 最常收到的用戶反饋或投訴是什麼？
- 有已知的安全問題或技術債嗎？

### Tech Stack 自動偵測

Bootstrap 可**讀取專案檔案**輔助偵測（唯讀，不違反 Hard Gate）：

| 檔案 | 偵測內容 |
|------|---------|
| `package.json` | Node.js 生態系、框架、依賴 |
| `Cargo.toml` | Rust |
| `go.mod` | Go |
| `requirements.txt` / `pyproject.toml` | Python |
| `Dockerfile` / `docker-compose.yml` | 容器化架構 |
| 專案根目錄結構（`src/`、`app/`、`lib/` 等） | 模組推斷 |

偵測後以**確認式**呈現：
```
我偵測到你的專案使用：
- 技術棧：Next.js 14 + TypeScript + PostgreSQL + Redis
- 主要模組：auth/、billing/、dashboard/、api/
這些正確嗎？有需要補充或修正的嗎？
```

使用者確認後才寫入。

### Bootstrap 與 S1 的順序（Hard Gate — Bootstrap 不阻塞流程）

- **預設行為**：Bootstrap 與 S1 必須在**同一個回合**內依序執行（S0 → S1），暫停點固定發生在 **S1 完成後**，不在 S0/S1 之間。
- **若使用者訊息已提供必要欄位** → 直接以表格確認已知欄位，立即進入 S1。
- **若部分欄位缺失** → 在同一回合內以表格列出已知與待補欄位，立即進入 S1，使用 placeholder 標記未確認欄位，並把待補欄位作為 **S1 confirmation question 的一部分**。
- **禁止**：在 S0 與 S1 之間插入「等使用者回答 Round 1 才能進 S1」的 pause。如果你的回應裡 S1 仍是 `⬜ pending` 而流程已停下等使用者輸入，視同未通過 Bootstrap 規則。

Bootstrap 完成後：寫入 `.product-context.md`（即使有 placeholder 也先寫入 baseline），然後在同一回合內進入 S1。

---

## 部分上下文 UX（情境 3）

```
📦 我有你之前 [N] 次規劃的紀錄：
- 技術棧：[從 Decision History 合併的已知 stack]
- 曾修改的模組：[從 Decision History 合併的 affected modules]
- 核心產品策略尚未記錄。

你想要：
  1️⃣ 直接開始（使用已知資訊，策略部分跳過）
  2️⃣ 先補充策略資訊（JTBD、定位、北極星指標）
  3️⃣ 這些資訊有誤，我來修正
```

**自動重建嘗試**：掃描所有 Decision History 條目，從 `Affected modules`、`Scope`、`Key decisions` 中提取重複出現的產品名稱、技術棧、模組名稱，自動填入 `Architecture & Tech Stack`。以 `<!-- inferred from decision history -->` 標註推斷來源。

---

## Append 模板

**通用模板**：
```markdown
### [ISO date] - [流程類型]
- **Scope**: [...]
- **Key decisions**: [...]
- **Risks identified**: [...]
- **MVP boundary**: [...]
- **Success metrics**: [...]
```

**功能擴充專用模板**：
```markdown
### [ISO date] - Feature Extension: [功能名稱]
- **Problem**: [一句話問題陳述]
- **Chosen solution**: [選定方案 + 理由]
- **Affected modules**: [影響的模組]
- **Scope**: [做什麼 / 不動什麼]
- **Acceptance criteria**: [驗收標準]
```

---

## 衝突 UX（程式碼 vs context）

```
⚠️ 偵測到資訊不一致：
- Context 記錄：[context 中的值]
- 專案程式碼：[程式碼中偵測到的值]
請確認哪個是正確的？
  1️⃣ 以程式碼為準（更新 context）
  2️⃣ 以 context 為準（可能正在遷移中）
  3️⃣ 兩者都不完整，我來說明
```

- 不自動覆寫，由使用者裁決
- 若選「正在遷移」，在 Architecture 標注：`[遷移中] React → Vue 3`
- 衝突紀錄寫入 Decision History
