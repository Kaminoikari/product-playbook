# 📦 完整模式步驟序列（8 Core + 1 預設 ON + 2 Optional，共 9–11 步）

> 此檔案為完整模式的權威步驟定義。由 SKILL.md 核心派發載入。

**已從原本的 20 步流程（v1.0.x）精簡而來：合併冗餘框架，並把選用步驟改為條件觸發。** 觸發邏輯與 Phase 決策點格式請見 `references/rules-optional-trigger.md`。

**Journey Map（S3）說明**：預設 ON。Persona-Journey 是捆綁的一對，無論產品是 0-to-1 或既有產品都適用——關鍵變數是使用者的 Job 是否跨越多個階段。僅在情境真的太過簡單時才跳過（單一 API/按鈕、流程 ≤2 步、或使用者明確要求跳過）。

## 步驟序列

```
Phase 0：Strategy
  S1.  策略診斷  [Core]
       → references/00-opportunity-check.md + references/01-strategy.md
       （合併：機會評估 + DHM + Strategy Blocks + Rumelt 策略內核）

Phase 1：Discovery
  S2.  Persona（Table + 卡片）  [Core]
       → references/02a-persona.md
  S3.  User Journey Map  [預設 ON — 僅在情境太簡單時才跳過]
       → references/02c-ost-journey.md
  S4.  JTBD 分析  [Core]
       → references/02b-jtbd.md

Phase 2：Define
  S5.  痛點 + HMW + 機會排序  [Core]
       → references/03-define.md
       （合併：痛點彙整表 + HMW + 機會評估表；
        OST 樹狀視覺化為此步驟內的選用子格式）
  S6.  April Dunford 定位  [Optional — 見觸發條件]
       → references/03-define.md

Phase 3：Develop
  S7.  PR-FAQ（Working Backwards）[Core]
       → references/04a-prfaq.md
  S8.  解法評估  [Core]
       → references/04b-solutions.md
       （合併：平行原型 + Pre-mortem + GEM + RICE）
  S9.  MVP + Not Doing List  [Core]
       → references/04c-mvp.md

Phase 4：Deliver
  S10. North Star + 三層訊號 + Aha Moment  [Core]
       → references/05a-northstar-aha.md
  S11. PMF + GTM + 商業模式 + 假設驗證計畫  [Optional — 見觸發條件]
       → references/05b-pmf-gtm.md + references/05c-validation-spec.md

────
最終產出 → 產品規格摘要（references/05c-validation-spec.md → 4.6）+ 最佳切入點分析
```

> 當產出對象為老闆或跨部門對齊時，在 S10 之前加入 Empowered Teams 框架。

## Optional 觸發規則

讀取 `references/rules-optional-trigger.md` 取得權威的觸發條件與 Phase 決策點輸出格式。

**速查：**
- **S3 Journey Map**（預設 ON）：執行，除非單一互動點 / 流程 ≤2 步 / 使用者要求跳過
- **S6 Positioning**（預設 OFF）：觸發條件為新產品上市 / 重新定位 / 對象包含 Sales-BD-行銷
- **S11 PMF/GTM/BM/驗證**（預設 OFF）：觸發條件為產品即將上市 / 對象為老闆或資料科學家 / 使用者要求驗證計畫

## Phase 決策點要求

進入 Phase 1、Phase 2、Phase 4 之前，需呈現 Phase 決策點區塊（格式定義於 `rules-optional-trigger.md`）。Phase 0 與 Phase 3 僅含 Core 步驟，不需決策點。

## Reference 載入指示

進入各步驟時，僅讀取對應的 reference 檔案（不要預先全部載入）：

| 步驟 | Reference 檔案 |
|------|---------------|
| S1 | `references/00-opportunity-check.md` + `references/01-strategy.md` |
| S2 | `references/02a-persona.md` |
| S3（若觸發） | `references/02c-ost-journey.md` |
| S4 | `references/02b-jtbd.md` |
| S5 | `references/03-define.md` |
| S6（若觸發） | `references/03-define.md` |
| S7 | `references/04a-prfaq.md` |
| S8 | `references/04b-solutions.md` |
| S9 | `references/04c-mvp.md` |
| S10 | `references/05a-northstar-aha.md` |
| S11（若觸發） | `references/05b-pmf-gtm.md` + `references/05c-validation-spec.md` |
| 最終產出 | `references/05c-validation-spec.md` |

## 步驟數量總覽

| 情境 | 步驟數 |
|----------|-------|
| 預設（8 Core + S3 Journey ON） | **9** |
| 流程過於簡單（S3 跳過） | 8 |
| 觸發 1 個預設 OFF 的 Optional（S6 或 S11） | 10 |
| 全部 Optional 都觸發 | 11 |
| （舊版 20 步流程） | 20 |

## 最終產出格式

**最佳切入點分析**（完整邏輯鏈）+ **產品規格摘要**。

產品規格摘要必須揭露本次被跳過的 Optional 步驟，並提供一鍵補上的指令（依 `rules-optional-trigger.md` 第 6 節）。

完成後，依 `references/rules-end-of-flow.md` 執行流程結束規則。
