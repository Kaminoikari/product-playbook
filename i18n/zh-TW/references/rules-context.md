# 📦 產品上下文累積規則

> 由 SKILL.md 啟動流程載入。包含所有決策邏輯（何時 / 哪些 / 如何）。Verbose YAML 格式與完整 UX 腳本放在 `rules-context-template.md`（只在實際寫入檔案或執行 Bootstrap 時才 lazy-load）。

## 1. 檔案生命週期

- **路徑**：專案根目錄下的 `.product-context.md`（與 `.product-playbook-progress.md` 同層）
- **永久保留**：跨 session 持續累積
- **首次建立時**：提醒使用者加入 `.gitignore`（可能包含敏感策略資訊）

---

## 2. 三種情境偵測（啟動時）

進度檔案檢查之後、模式選擇之前：

| 條件 | 情境 | 動作 |
|------|------|------|
| 檔案存在，`Core Strategy` 有實際內容 | **1. 完整** | 靜默載入。顯示：「📦 偵測到 **[產品名]** 的產品上下文，將作為本次規劃的基線。」 |
| 檔案不存在 | **2. 無上下文** | 記錄狀態。進入功能擴充 / 改版時觸發 Bootstrap。→ 載入 template §Bootstrap |
| 檔案存在，Core Strategy 空白或僅 placeholder，Decision History 有 ≥1 筆 | **3. 部分** | 顯示已知資訊摘要 + 補充選項。→ 載入 template §Partial |

**偵測邏輯**：
1. 檔案是否存在？
2. `Identity` 是否有 Product name（非 placeholder）？
3. `Core Strategy` 是否有 Core JTBD（非 placeholder）？→ 有 = 情境 1
4. `Decision History` 是否有任何 `###` 條目？→ 有但 3 為否 = 情境 3

---

## 3. Auto-Read 規則（各模式 S1 前置）

**只注入相關 sections** — 不向使用者完整顯示檔案：

| 模式 + 步驟 | 注入的 Sections |
|-------------|----------------|
| 功能擴充 S1 | Identity, Architecture & Tech Stack, 最近 3 筆 Decision History |
| 改版 S1 | Identity, Core Strategy, Accumulated Insights（痛點、PMF、安全）, 最近 3 筆 Decision History |
| 完整/Quick/Build S1 | Identity only（產品名、類型、一句話描述） |
| 任何模式的 Pre-mortem | Security posture + Technical debt（從 Accumulated Insights） |

**膨脹控制**：Decision History 預設只注入最近 3 筆。使用者可要求載入更多。

---

## 4. 空白 Sections 跳過規則

| Section | 功能擴充 | 改版模式 | 完整/Quick/Build |
|---------|---------|---------|-----------------|
| Identity | 必要（無則 Bootstrap） | 必要（無則 Bootstrap） | 流程本身會產出 |
| Core Strategy | 可跳過 | 必要（無則 S1 內快問快答補收集） | 流程本身會產出 |
| Architecture & Tech Stack | 必要（無則 Bootstrap 或自動偵測） | 可跳過 | 流程本身會產出 |
| Decision History | 可跳過 | 有則帶入，無則跳過 | 流程本身會產出 |
| Accumulated Insights | 可跳過 | 有則帶入，無則跳過 | 流程本身會產出 |

**原則**：空白 section **不阻擋流程**。只有對當前模式「必要」且為空的 section 才觸發收集。

---

## 5. Auto-Write 規則（流程結束時）

與 `rules-end-of-flow.md` 結束條件同步。自動萃取 context：

| 流程類型 | 寫入/更新的 Sections |
|---------|---------------------|
| Quick | Identity, Core Strategy（JTBD + North Star）, 追加 History |
| Full | 全部 sections（覆寫 Identity/Strategy/Insights，追加 History） |
| Revision | 更新 Core Strategy（若重新定位）, 更新 Insights, 追加 History |
| Feature Extension | 合併 Architecture, 追加 History（功能專用模板） |
| Custom | 更新對應已完成步驟的 sections |
| Build | Identity, Core Strategy（部分）, 追加 History |

### 各 Section 寫入策略

| Section | 策略 |
|---------|------|
| Identity | 最新覆寫 |
| Core Strategy | 最新覆寫（改版後取代改版前） |
| Architecture & Tech Stack | 合併（新增模組保留舊的） |
| Decision History | 僅追加（永不刪除先前紀錄） |
| Accumulated Insights | 合併去重（痛點/反饋去重；PMF/Security 覆寫） |

首次寫入（建立檔案）或追加 Decision History 時 → **載入 `rules-context-template.md` §File Format / §Append Templates**。

完成後顯示：`✅ 產品上下文已更新至 '.product-context.md'，下次規劃時將自動載入。`

---

## 6. 衝突處理（摘要）

| 衝突類型 | 解決方式 |
|---------|---------|
| 使用者修正既有 context | Latest wins — 直接覆寫 |
| Context 與程式碼不一致（如 package.json） | 不自動覆寫 — 詢問使用者。→ 載入 template §Conflict UX |
| 流程資料與舊 context 不同 | 流程資料優先 — 流程結束時自動覆寫 |

---

## 7. 語系偏好（摘要）

當 context 被建立或更新時，記錄在 `Language Preference` section：
- **Installed language**：從 `.lang` 檔案或使用者語系設定偵測
- **User's preferred language**：使用者在 session 中溝通使用的語言

**載入時**：若已記錄，以該語言繼續 session。
**寫入時**：於 Bootstrap 或首次建立 context 檔案的流程結束時寫入。使用者中途切換語言時同步更新。

---

## 8. 何時載入 `rules-context-template.md`

僅在以下任一 trigger 觸發時：

| 觸發條件 | Template Section |
|---------|------------------|
| 情境 2 + 進入功能擴充 / 改版 | §Bootstrap, §File Format |
| 情境 3（部分上下文） | §Partial Context, §File Format |
| 首次寫入 context | §File Format |
| 流程結束時追加 Decision History | §Append Templates |
| 偵測到程式碼衝突 | §Conflict UX |
| Bootstrap 完成 → 寫入 baseline | §File Format |

啟動時**不要**預先載入 template。
