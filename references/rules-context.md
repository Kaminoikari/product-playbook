# 📦 產品上下文累積規則

> 此檔案定義 `.product-context.md` 的格式、讀寫規則、情境處理和衝突解決。
> 由 SKILL.md 啟動流程觸發載入，或由各模式 S1 前置步驟載入。

## 1. 檔案位置與生命週期

- **路徑**：專案根目錄下的 `.product-context.md`（與 `.product-playbook-progress.md` 同層）
- **永久保留**：此檔案在流程結束後**不會被刪除**，跨 session 持續累積
- **首次建立時**提醒使用者：「⚠️ 建議將 `.product-context.md` 加入 `.gitignore`，此檔案可能包含敏感的產品策略資訊。」

---

## 2. 檔案格式

```markdown
# Product Context
<!-- Auto-maintained by the-product-playbook. Do not delete. -->
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

## Accumulated Insights
- **Known pain points**: [痛點清單，附來源]
- **User feedback themes**: [跨 session 的反饋主題]
- **PMF status**: [最近評估等級 + 日期]
- **Security posture**: [認證/授權方式、已知漏洞]
- **Technical debt**: [跨 session 累積的技術債]
```

---

## 3. 三種情境偵測

啟動時（進度檔案檢查之後、模式選擇之前），偵測 `.product-context.md` 狀態：

| 條件 | 情境 | 動作 |
|------|------|------|
| 檔案存在，`Core Strategy` section 有實際內容（非空/非 placeholder） | **情境 1：完整上下文** | 靜默載入。顯示：「📦 偵測到 **[產品名]** 的產品上下文，將作為本次規劃的基線。」 |
| 檔案不存在 | **情境 2：無上下文** | 記錄此狀態。進入功能擴充或改版模式時觸發 Context Bootstrap（見 Section 4） |
| 檔案存在，`Core Strategy` 空白或僅有 placeholder，但 `Decision History` 有至少一筆紀錄 | **情境 3：部分上下文** | 顯示已知資訊摘要，提供補充選項（見 Section 5） |

**偵測邏輯**：
1. 檔案是否存在？
2. `Identity` section 是否有 Product name（非 placeholder）？
3. `Core Strategy` section 是否有 Core JTBD（非 placeholder）？→ 有 = 情境 1
4. `Decision History` section 是否有任何 `###` 條目？→ 有但 3 為否 = 情境 3

---

## 4. Context Bootstrap（情境 2 專用）

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

除了使用者口述，Bootstrap 可**讀取專案檔案**輔助偵測（唯讀，不違反 Hard Gate）：

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

使用者確認後才寫入 `.product-context.md`。

### Bootstrap 完成後

將收集到的資訊寫入 `.product-context.md`，未收集的 section 留空（使用 placeholder），然後進入模式的正式 S1。

---

## 5. 部分上下文處理（情境 3）

當 `.product-context.md` 存在但 Core Strategy 為空、僅有 Decision History 時：

**呈現方式**：
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

## 6. Context Auto-Read 規則

各模式 S1 前置載入 context 時，**只注入相關 sections**，不要向使用者完整顯示檔案內容：

| 模式 + 步驟 | 注入的 Context Sections |
|-------------|------------------------|
| 功能擴充 S1 | Identity, Architecture & Tech Stack, 最近 3 筆 Decision History |
| 改版 S1 | Identity, Core Strategy, Accumulated Insights（痛點、PMF、安全）, 最近 3 筆 Decision History |
| 完整/Quick/Build S1 | Identity only（產品名、類型、一句話描述） |
| 任何模式的 Pre-mortem | Security posture + Technical debt（從 Accumulated Insights） |

**膨脹控制**：Decision History 預設只注入最近 3 筆。使用者可要求載入更多。

---

## 7. 空白 Sections 跳過規則

Context 檔案存在但某些 sections 為空時，依**模式**決定是否可跳過或需收集：

| Section | 功能擴充 | 改版模式 | 完整/Quick/Build |
|---------|---------|---------|-----------------|
| Identity | 必要（無則 Bootstrap） | 必要（無則 Bootstrap） | 流程本身會產出，不需預載 |
| Core Strategy | **可跳過** | 必要（無則在 S1 內快問快答補收集） | 流程本身會產出 |
| Architecture & Tech Stack | 必要（無則 Bootstrap 或自動偵測） | 可跳過 | 流程本身會產出 |
| Decision History | 可跳過 | 有則帶入，無則跳過 | 流程本身會產出 |
| Accumulated Insights | 可跳過 | 有則帶入，無則跳過 | 流程本身會產出 |

**原則**：空白 section **不阻擋流程**。只有對當前模式「必要」且為空的 section 才觸發收集。

---

## 8. Context Auto-Write 規則（流程結束時萃取）

流程結束時（與 `rules-end-of-flow.md` 的結束條件檢查同步），自動萃取 context：

| 流程類型 | 寫入/更新的 Sections |
|---------|---------------------|
| Quick | Identity, Core Strategy（JTBD + North Star）, 追加 Decision History |
| Full | **全部 sections**（覆寫 Identity/Strategy/Insights，追加 History） |
| Revision | 更新 Core Strategy（若有重新定位）, 更新 Insights, 追加 History |
| Feature Extension | 合併 Architecture, 追加 Decision History（功能專用模板） |
| Custom | 更新對應已完成步驟的 sections |
| Build（7 步） | Identity, Core Strategy（部分）, 追加 History |

### 寫入策略

| Section | 策略 | 說明 |
|---------|------|------|
| Identity | **最新覆寫** | 每次都用最新流程的資料覆寫 |
| Core Strategy | **最新覆寫** | 同上。改版後的策略取代改版前的 |
| Architecture & Tech Stack | **合併** | 新增模組不刪除舊的。新技術項目追加 |
| Decision History | **僅追加** | 永遠不刪除先前紀錄。每次完成流程追加一筆 |
| Accumulated Insights | **合併去重** | 痛點、反饋主題去重追加。PMF、Security 覆寫為最新值 |

### Decision History 追加模板

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

### 完成後通知

```
✅ 產品上下文已更新至 `.product-context.md`，下次規劃時將自動載入。
```

---

## 9. 衝突處理

### 使用者修正既有 context

完全允許。使用者提供的修正直接覆寫對應 section（latest wins）。

### 使用者提供的資料與程式碼不一致

當 S1 前置同時讀取了 `.product-context.md` 和專案檔案（如 `package.json`），發現兩者不一致時：

```
⚠️ 偵測到資訊不一致：
- Context 記錄：[context 中的值]
- 專案程式碼：[程式碼中偵測到的值]
請確認哪個是正確的？
  1️⃣ 以程式碼為準（更新 context）
  2️⃣ 以 context 為準（可能正在遷移中）
  3️⃣ 兩者都不完整，我來說明
```

**處理原則**：
- **不自動覆寫**，由使用者裁決
- 使用者選擇後更新 `.product-context.md`
- 若選「正在遷移」，在 Architecture section 標注：`[遷移中] React → Vue 3`
- 衝突紀錄寫入 Decision History

### 流程中的新資料覆蓋 context

若流程中產出的資料與 context 中的舊資料不同（例如改版模式重新定義了 JTBD），**流程資料優先**。流程結束時自動覆寫。
