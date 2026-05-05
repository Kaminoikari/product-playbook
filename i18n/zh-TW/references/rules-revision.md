# 🔄 改版模式步驟序列(6 Core + 2 Optional,共 6–8 步)

> 此檔案為改版模式的權威步驟定義。由 SKILL.md 核心派發載入。

**已從原本的 12 步流程(v1.0.x)精簡而來:合併冗餘框架,並把選用步驟改為條件觸發。** 觸發邏輯與 Phase 決策點格式請見 `references/rules-optional-trigger.md`。

## 步驟序列

```
Phase 0:現況分析
  S1.  現況回顧 + JTBD 重新檢驗  [Core]
       (合併:資料盤點 + 哪些既有 Job 做得好/做得不好)

Phase 1:問題收斂
  S2.  用戶痛點收集  [Core]
       (留存/流失分析 + 用戶反饋彙整 + 行為數據)
  S3.  痛點 + HMW + 機會排序  [Core]
       → references/03-define.md
       (合併:痛點彙整表 + HMW + 機會評估表)
  S4.  Positioning 重新評估  [Optional — 見觸發條件]
       → references/03-define.md

Phase 2:解法設計
  S5.  PR-FAQ(描述改版後的體驗) [Core]
       → references/04a-prfaq.md
  S6.  Pre-mortem  [Optional — 見觸發條件]
       → references/04b-solutions.md
  S7.  MVP + Not Doing List  [Core]
       → references/04c-mvp.md

Phase 3:驗證
  S8.  North Star + Aha(改版前後對比)+ 假設驗證計畫  [Core]
       → references/05a-northstar-aha.md + references/05c-validation-spec.md
       (合併:任何改版都必須驗證假設;兩者高度耦合)

────
最終產出 → 產品規格摘要(改版版)
```

### S1 前置:產品上下文載入

進入 S1 前,讀取 `references/rules-context.md` 並檢查 `.product-context.md`:

- **有完整上下文(情境 1)**:自動帶入 PMF 等級、North Star、已知痛點、安全現況、近 3 筆 Decision History。S1 引導改為**差異式**:「上次評估時,你的 PMF 等級為 [X],北極星指標為 [Y]。目前這些有變化嗎?最新的 DAU/MAU 和留存率是多少?」— 已有的歷史決策和已知痛點不需要重新收集。
- **無上下文(情境 2)**:觸發 Context Bootstrap(`rules-context.md` Section 4,Round 1 + 3),完成後再進入下方標準 S1 數據收集。
- **部分上下文(情境 3)**:從 Decision History 帶入功能變更歷史(知道哪些模組被改過、有哪些風險被識別過),但需詢問整體產品策略和指標(之前只做過功能擴充,缺全局視角)。

### S1 標準引導

> 改版模式的 S1 會主動詢問使用者提供既有產品數據:DAU/MAU、留存率、主要用戶反饋、過去版本的關鍵決策等。若 context 已預填部分答案,改為確認而非重新收集。
> S1 同時收集安全現況:現有認證/授權機制、已知安全漏洞或技術債、近期安全事件。這些資訊會影響改版的風險評估和 Pre-mortem(若觸發)。

### 快速路徑

當使用者在 S1 已提供充分數據(含用戶反饋、指標、痛點),S3 可在單次來回對話中產出,而非多次確認。觸發條件:S2 收集到的痛點清單已有明確的優先級和數據支持。Hard Gate 規則不變 — 每個步驟的產出仍須完整呈現,只是確認節奏加快。

## Optional 觸發規則

讀取 `references/rules-optional-trigger.md` 取得權威的觸發條件與 Phase 決策點輸出格式。

**速查:**
- **S4 Positioning 重新評估** 觸發條件:使用者提到「定位漂移」/「市場改變」/ 對象包含 Sales/行銷
- **S6 Pre-mortem** 觸發條件:改動範圍 ≥30% 既有功能 / 涉及金流-權限-資料遷移

## Phase 決策點要求

進入 Phase 1 與 Phase 2 之前,需呈現 Phase 決策點區塊(格式定義於 `rules-optional-trigger.md`)。Phase 0 與 Phase 3 僅含 Core 步驟,不需決策點。

## Reference 載入指示

| 步驟 | Reference 檔案 |
|------|---------------|
| S1–S2 | (無需外部 reference;直接收集使用者數據) |
| S3 | `references/03-define.md` |
| S4(若觸發) | `references/03-define.md` |
| S5 | `references/04a-prfaq.md` |
| S6(若觸發) | `references/04b-solutions.md` |
| S7 | `references/04c-mvp.md` |
| S8 + 最終產出 | `references/05a-northstar-aha.md` + `references/05c-validation-spec.md` |

## 步驟數量總覽

| 情境 | 步驟數 |
|----------|-------|
| 預設(僅 Core) | **6** |
| 觸發全部 Optional | 8 |
| (舊版 12 步流程) | 12 |

## 最終產出格式

**改版產品規格摘要**:改版前後對照 + 改什麼/不改什麼 + 成功指標。

摘要必須揭露本次被略過的 Optional 步驟,並提供一鍵補上的指令(依 `rules-optional-trigger.md` Section 6)。

完成後,依 `references/rules-end-of-flow.md` 執行流程結束規則。
