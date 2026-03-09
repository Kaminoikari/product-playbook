# 開發銜接（Dev Handoff）— 從規劃到實作

> 當使用者說「進入開發」「產出開發交接包」「幫我建專案」「接到 Claude Code」時觸發。
> 讀取此檔案，整合整個產品規劃流程的產出，生成可直接在 Claude Code CLI 中使用的開發交接包。

## 環境限制與銜接策略

**關鍵事實：Claude Chat / Cowork 和 Claude Code 是獨立的運行環境，無法從 Chat 內直接啟動 Claude Code。**

因此銜接策略是：**產出結構化的開發交接包（一組檔案）**，使用者下載後放入專案資料夾，在 Claude Code 中一句話即可啟動整個開發流程。

銜接方式視使用者環境而定：

| 使用者環境 | 銜接方式 |
|-----------|---------|
| **Claude Chat（Web/App）** | 產出 zip 檔供下載，使用者解壓到專案目錄後開啟 Claude Code |
| **Claude Cowork（Desktop）** | 同上，但可直接將檔案寫入使用者指定的本地路徑 |
| **已在 Claude Code 中** | 直接在專案目錄中建立所有檔案（此情境下此 skill 多半由 CLAUDE.md 引用） |

---

## 開發交接包組成

產出以下檔案組合，所有檔案放在專案根目錄：

```
[project-name]/
├── CLAUDE.md              # Claude Code 的專案記憶檔：產品上下文 + 開發規範
├── TASKS.md               # 功能拆解 + Phase 分期 + 逐 Task 驗收標準
├── TICKETS.md             # 開票內容：每張票的標題、描述、驗收標準，PM 可直接開票
├── docs/
│   ├── PRD.md             # 完整 PRD（從 04-develop.md 產出格式整合）
│   ├── ARCHITECTURE.md    # 技術架構：目錄結構 + DB schema + API endpoints
│   └── PRODUCT-SPEC.md    # 產品規格摘要（從 05-deliver.md → 4.6 整合）
└── scripts/
    └── setup.sh           # 一鍵初始化腳本（建立目錄 + 安裝 dependencies）
```

---

## 📄 CLAUDE.md 模板

CLAUDE.md 是 Claude Code 的專案記憶檔，Claude Code 每次啟動時會自動讀取。必須包含：

```markdown
# [產品名稱] — 專案指引

## 產品上下文

**一句話描述**：[PR-FAQ 標題]
**目標用戶**：[Persona 一句話描述]
**核心 JTBD**：[Target Customer] 想要在 [Job Context] 完成 [Job]
**Aha Moment**：當用戶完成 [行為]，他們體驗到核心價值
**北極星指標**：[指標名稱 + 定義]

## 技術棧

- **前端**：[框架 + 版本]
- **後端**：[框架 + 版本]
- **資料庫**：[類型 + 版本]
- **部署**：[平台]
- **套件管理**：[工具]

## 開發規範

- 使用 [語言] 開發
- 遵循 [風格指南/lint 規則]
- commit message 格式：`[type]: [description]`（type: feat / fix / refactor / docs / test）
- 分支策略：[main / develop / feature-xxx]
- 每個功能必須有對應的 User Story 編號（見 TASKS.md）

## MVP 邊界

**必須有（P0）**：
- [功能 1]
- [功能 2]
- [功能 3]

**明確不做**：
- [排除項 1] — 原因：[理由]
- [排除項 2] — 原因：[理由]

## 關鍵決策記錄

| 決策 | 選擇 | 理由 | 日期 |
|------|------|------|------|
| [例：資料庫選擇] | [PostgreSQL] | [需要關聯查詢 + JSON 支援] | [日期] |

## 風險警示（來自 Pre-mortem）

- ⚠️ [風險 1]：[預防措施]
- ⚠️ [風險 2]：[預防措施]

## 開發流程

請依照 `TASKS.md` 的 Phase 順序逐步執行。每完成一個 Phase：
1. 確認所有 Task 的驗收標準都通過
2. 詢問使用者是否要進入下一個 Phase
3. 如果遇到架構問題，參考 `docs/ARCHITECTURE.md`
```

---

## 📄 TASKS.md 模板

功能拆解的核心原則：
- 從 MVP 必須有（P0）的功能出發
- 每個 Task 對應一個 User Story
- Phase 之間有明確的依賴關係：Phase N+1 依賴 Phase N 的產出
- 每個 Task 包含驗收標準，Claude Code 可以自我檢查

```markdown
# [產品名稱] — 開發任務清單

## Phase 0：專案初始化
> 目標：建立可運行的空白專案骨架

- [ ] **T0.1** 初始化專案（`scripts/setup.sh` 或手動）
  - 驗收：`npm run dev` / `python manage.py runserver` 等指令可啟動
- [ ] **T0.2** 設定 linter + formatter
  - 驗收：lint 通過無錯誤
- [ ] **T0.3** 建立資料庫 + 執行初始 migration
  - 驗收：資料庫可連接，基礎 table 已建立
- [ ] **T0.4** 建立基礎路由結構
  - 驗收：所有主要頁面路由可訪問（回傳空白頁面即可）

## Phase 1：核心流程（Aha Moment 路徑）
> 目標：讓用戶可以走完從進入到 Aha Moment 的最短路徑
> 對應 User Story：[US-001, US-002, ...]

- [ ] **T1.1** [功能名稱]
  - User Story：身為 [Persona]，我想要 [行為]，以便 [價值]
  - 驗收標準：
    - [ ] [可測試的具體條件 1]
    - [ ] [可測試的具體條件 2]
  - 技術備註：[需要的 API / 第三方服務 / 特殊邏輯]

- [ ] **T1.2** [功能名稱]
  - User Story：...
  - 驗收標準：...

> **Phase 1 完成檢查點**：用戶可以完成 [Aha Moment 行為]。如果不行，不要進入 Phase 2。

## Phase 2：完整 MVP
> 目標：補全 MVP 範圍中所有 P0 功能
> 對應 User Story：[US-003, US-004, ...]

- [ ] **T2.1** [功能名稱]
  - ...

> **Phase 2 完成檢查點**：所有 P0 User Story 的驗收標準都通過。

## Phase 3：品質與體驗
> 目標：錯誤處理、邊界情境、載入狀態、基礎安全性

- [ ] **T3.1** 全域錯誤處理
- [ ] **T3.2** 表單驗證 + 邊界情境
- [ ] **T3.3** 載入狀態 + 空狀態
- [ ] **T3.4** 基礎安全性（輸入消毒、認證檢查）
- [ ] **T3.5** 響應式設計（如果是 Web）

## Phase 4：部署
> 目標：可以讓外部用戶訪問

- [ ] **T4.1** 環境變數管理
- [ ] **T4.2** 部署配置
- [ ] **T4.3** 基礎監控 + 日誌
```

---

## 📄 ARCHITECTURE.md 模板

```markdown
# [產品名稱] — 技術架構

## 目錄結構

[根據技術棧產出對應的目錄結構]

## 資料庫設計

[從 PRD 的 DB Schema 整合，轉為建表 SQL 或 ORM Model 定義]

### ER 關係圖

[Mermaid erDiagram]

### 關鍵 Table 說明

| Table | 說明 | 關鍵欄位 | 索引建議 |
|-------|------|---------|---------|
| | | | |

## API 設計

[根據 User Story 和功能規格，定義 RESTful API endpoints 或 GraphQL schema]

### Endpoints 清單

| 方法 | 路徑 | 說明 | 對應 Task |
|------|------|------|----------|
| GET | /api/v1/[resource] | [說明] | T1.1 |
| POST | /api/v1/[resource] | [說明] | T1.2 |

### 認證方式

[JWT / Session / OAuth 等]

## 第三方服務

| 服務 | 用途 | 對應功能 |
|------|------|---------|
| | | |
```

---

## 📄 setup.sh 模板

```bash
#!/bin/bash
# [產品名稱] — 專案初始化腳本
# 使用方式：chmod +x scripts/setup.sh && ./scripts/setup.sh

set -e

echo "🚀 正在初始化 [產品名稱]..."

# ===== 檢查前置條件 =====
command -v [node/python/etc] >/dev/null 2>&1 || { echo "❌ 需要安裝 [runtime]"; exit 1; }

# ===== 安裝依賴 =====
echo "📦 安裝依賴..."
[npm install / pip install -r requirements.txt / etc]

# ===== 環境設定 =====
if [ ! -f .env ]; then
  echo "📝 建立 .env 檔案..."
  cp .env.example .env
  echo "⚠️  請編輯 .env 填入必要的環境變數"
fi

# ===== 資料庫初始化 =====
echo "🗄️  初始化資料庫..."
[migration commands]

echo ""
echo "✅ 初始化完成！"
echo ""
echo "下一步："
echo "  1. 編輯 .env 填入環境變數"
echo "  2. 啟動開發伺服器：[start command]"
echo "  3. 開始開發：claude \"請讀取 CLAUDE.md 和 TASKS.md，開始執行 Phase 1\""
```

---

## 📄 TICKETS.md 模板

TICKETS.md 是根據 TASKS.md 中的功能拆解，產出可直接在專案管理工具中開票的結構化內容。每張票包含 PM 開票所需的完整資訊。

> **設計目標**：PM 可以直接將每張票的內容複製到 Jira / Asana / Linear 等工具中開票，後續版本將支援透過 API 自動開票。

```markdown
# [產品名稱] — 開票清單

> 產出時間：[時間戳]
> 對應 TASKS.md 版本：[版本/時間]
> 共 [N] 張票

---

## 票務總覽

| 票號 | 標題 | Phase | 優先級 | 預估工時 | 依賴 |
|------|------|-------|--------|---------|------|
| TKT-001 | [標題] | Phase 0 | P0 | [X]h | — |
| TKT-002 | [標題] | Phase 1 | P0 | [X]h | TKT-001 |
| ... | | | | | |

---

## TKT-001：[標題]

**Phase**：Phase 0 — 專案初始化
**對應 Task**：T0.1
**優先級**：P0
**預估工時**：[X] 小時
**依賴**：無
**指派對象**：[角色/團隊，例如：後端工程師]

### 描述

[用 1-3 段文字描述這張票要完成什麼，包含業務背景和技術目標]

### User Story

身為 [Persona]，我想要 [行為]，以便 [價值]

### 驗收標準

- [ ] [可測試的具體條件 1]
- [ ] [可測試的具體條件 2]
- [ ] [可測試的具體條件 3]

### 技術備註

- [實作注意事項]
- [需要的 API / 第三方服務]
- [相關檔案路徑或模組]

### 標籤建議

`[Phase 0]` `[backend]` `[setup]`

---

## TKT-002：[標題]

[同上格式，逐張展開]
```

### 開票規則

1. **票號對應 Task**：每個 TASKS.md 中的 Task 對應一張票（TKT-001 ↔ T0.1），粒度過大的 Task 可拆為多張票
2. **優先級繼承**：Phase 0-1 預設 P0，Phase 2 預設 P1，Phase 3-4 預設 P2，可根據 RICE 分數調整
3. **依賴關係**：明確標記票與票之間的前後依賴，避免工程師跳步開發
4. **預估工時**：根據 Task 粒度原則（1-4 小時），提供合理預估
5. **標籤建議**：包含 Phase、技術領域（frontend / backend / database / infra）、功能模組

### 專案管理工具串接（預留）

> 以下為未來自動開票功能的預留接口設計，目前版本僅產出 TICKETS.md 供 PM 手動開票。

TICKETS.md 的結構化格式已預留以下欄位，便於後續透過 API 自動匯入：

| 欄位 | Jira 對應 | Asana 對應 | Linear 對應 |
|------|----------|-----------|------------|
| 票號 | Issue Key | Task ID | Issue ID |
| 標題 | Summary | Task Name | Title |
| 描述 | Description | Description | Description |
| 優先級 | Priority | Custom Field | Priority |
| 預估工時 | Story Points / Time Estimate | Custom Field | Estimate |
| 依賴 | Linked Issues | Dependencies | Relations |
| 標籤 | Labels + Components | Tags | Labels |
| Phase | Epic | Section | Project |
| 指派對象 | Assignee | Assignee | Assignee |
| 驗收標準 | Acceptance Criteria (Description) | Subtasks | Sub-issues |

---

## 技術棧確認流程

產出開發交接包前，必須確認技術棧。如果使用者沒有指定，依以下順序詢問：

### 必問（影響所有產出）

```
1. 這是什麼類型的應用？
   □ Web App（瀏覽器）
   □ Mobile App（iOS / Android / 跨平台）
   □ Desktop App
   □ API / Backend Service
   □ CLI 工具
   □ 其他

2. 你有偏好的技術棧嗎？
   （如果沒有，我會根據產品特性推薦）
```

### 推薦邏輯（使用者沒有指定時）

| 應用類型 | 推薦技術棧 | 推薦理由 |
|---------|-----------|---------|
| Web App（MVP 快速驗證） | Next.js + Tailwind + Supabase | 全端一體、部署簡單、內建 Auth |
| Web App（複雜後端邏輯） | React + Node.js/Express + PostgreSQL | 靈活性高、生態系成熟 |
| Web App（Python 團隊） | React + FastAPI/Django + PostgreSQL | Python 生態系、Django 內建 Admin |
| Mobile App（跨平台） | React Native / Flutter | 單一 Codebase 覆蓋雙平台 |
| API Service | FastAPI / Express / Go | 輕量、高效能 |

> Claude 推薦時應說明理由，並提醒使用者可以覆蓋推薦。

### 選填（根據產品需求追問）

```
3. 需要用戶認證嗎？（影響 Auth 方案選擇）
4. 有即時性需求嗎？（WebSocket / SSE）
5. 需要檔案上傳/處理嗎？（影響 Storage 選擇）
6. 預計部署在哪裡？（Vercel / Railway / AWS / 自建）
```

---

## 功能拆解邏輯

將 MVP 功能轉換為 Task 的規則：

### Phase 劃分原則

```
Phase 0：專案骨架（所有模式都必須有）
  → 初始化、linter、DB、基礎路由

Phase 1：Aha Moment 最短路徑（最重要）
  → 從用戶進入到達 Aha Moment 所需的最少功能
  → 只包含這條路徑上的 P0 功能

Phase 2：完整 MVP
  → 補全 Phase 1 沒有覆蓋的其他 P0 功能
  → 支線流程、次要頁面

Phase 3：品質與體驗
  → 錯誤處理、邊界情境、載入/空狀態
  → 安全性基礎、響應式設計

Phase 4：部署
  → 環境變數、部署配置、監控
```

### Task 粒度原則

- 每個 Task 應該可以在 **1-4 小時** 內完成
- 太大 → 拆成子 Task（T1.1a, T1.1b）
- 太小 → 合併到相關 Task
- 每個 Task 必須有至少一個可測試的驗收標準

### User Story → Task 對應

```
一個 User Story 可能對應 1-3 個 Task：
  US-001: 身為新用戶，我想要註冊帳號，以便開始使用
    → T1.1: 註冊頁面 UI
    → T1.2: 註冊 API + 資料驗證
    → T1.3: Email 驗證流程（如果 MVP 需要）
```

---

## 使用者引導文字

### 在 Claude Chat / Cowork 中

產出開發交接包後，顯示以下引導：

```
📦 開發交接包已準備好！包含以下檔案：

  CLAUDE.md        → Claude Code 的專案記憶（產品上下文 + 技術規範）
  TASKS.md         → 開發任務清單（4 個 Phase，共 [N] 個 Task）
  TICKETS.md       → 開票清單（共 [N] 張票，可直接在 Jira/Asana/Linear 開票）
  docs/PRD.md      → 完整 PRD
  docs/ARCHITECTURE.md → 技術架構（DB schema + API + 目錄結構）
  docs/PRODUCT-SPEC.md → 產品規格摘要
  scripts/setup.sh → 一鍵初始化腳本

🔗 如何開始開發：

  1. 下載並解壓到你的專案資料夾
  2. 開啟終端機，進入專案資料夾
  3. 啟動 Claude Code：
     $ claude
  4. 告訴 Claude Code 開始：
     > 請讀取 CLAUDE.md 和 TASKS.md，開始執行 Phase 0

💡 小提示：
  - Claude Code 會自動讀取 CLAUDE.md，所以它已經知道整個產品上下文
  - 每個 Phase 完成後，它會詢問你是否要進入下一個 Phase
  - 如果要調整功能範圍，直接修改 TASKS.md 即可
  - CLAUDE.md 中的「明確不做」清單會防止 Claude Code 做超出範圍的事
```

### 產出前的最終確認

```
在產出開發交接包前，我需要確認幾件事：

1. 技術棧：[已確認 / 需要確認]
2. 產品名稱（用於專案資料夾名稱）：[已確認 / 需要確認]
3. 是否有其他技術限制或偏好？
   - 例如：必須用某個 ORM、需要支援特定瀏覽器、有既有的 CI/CD 等
```
