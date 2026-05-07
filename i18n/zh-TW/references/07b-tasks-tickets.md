# 開發銜接 — TASKS.md + TICKETS.md

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
  - 驗收：
    - [ ] `npm run dev` / `python manage.py runserver` 等指令可啟動
    - [ ] `.gitignore` 已建立，包含 `.env`、`.env.local`、`node_modules/`、`.product-playbook-progress.md`、`.product-dev-active` 等敏感檔案
    - [ ] `.env.example` 已建立（只有 key 名稱，沒有實際值）
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
- [ ] **T3.4** 安全性檢查（依 `references/08-security-checklist.md` 逐項確認）
  - 驗收：
    - [ ] OWASP Top 10 相關項目已處理（輸入驗證、認證、XSS 防護、CSRF 防護）
    - [ ] 安全性 Headers 已設定（CSP、X-Frame-Options、HSTS 等）
    - [ ] CORS 政策已配置（不使用 wildcard *）
    - [ ] 敏感 API 端點有 Rate Limiting
    - [ ] API 錯誤回應不洩漏內部資訊
- [ ] **T3.5** 響應式設計（如果是 Web）

## Phase 4：部署
> 目標：可以讓外部用戶訪問

- [ ] **T4.1** 環境變數管理
- [ ] **T4.2** 部署配置
- [ ] **T4.3** 基礎監控 + 日誌
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
