# 🔄 改版模式步驟序列(6 Core + 2 Optional,共 6–8 步)

> 此檔案為改版模式的權威步驟定義。由 SKILL.md 核心派發載入。

**已從原本的 12 步流程(v1.0.x)精簡而來:合併冗餘框架,並把選用步驟改為條件觸發。** 觸發邏輯與 Phase 決策點格式請見 `references/rules-optional-trigger.md`。

## 步驟序列

```
Phase 0: Current State Analysis
  S1.  Current State Review + JTBD Re-validation  [Core]
       (Merged: data inventory + which existing Jobs are done well/poorly)

Phase 1: Problem Convergence
  S2.  User Pain Points Collection  [Core]
       (Retention/churn analysis + feedback synthesis + behavior data)
  S3.  Pain Points + HMW + Opportunity Ranking  [Core]
       → references/03-define.md
       (Merged: Pain Points Summary + HMW + Opportunity Assessment Table)
  S4.  Positioning Re-assessment  [Optional — see triggers]
       → references/03-define.md

Phase 2: Solution Design
  S5.  PR-FAQ (post-revision experience)  [Core]
       → references/04a-prfaq.md
  S6.  Pre-mortem  [Optional — see triggers]
       → references/04b-solutions.md
  S7.  MVP + Not Doing List  [Core]
       → references/04c-mvp.md

Phase 3: Validation
  S8.  North Star + Aha (before/after comparison) + Hypothesis Validation Plan  [Core]
       → references/05a-northstar-aha.md + references/05c-validation-spec.md
       (Merged: any revision must validate hypotheses; tightly coupled)

────
Final output → Product Spec Summary (revision edition)
```

### S1 前置:產品上下文載入

進入 S1 前,讀取 `references/rules-context.md` 並檢查 `.product-context.md`:

- **有完整上下文(情境 1)**:自動帶入 PMF 等級、North Star、已知痛點、安全現況、近 3 筆 Decision History。S1 引導改為**差異式**:「上次評估時,你的 PMF 等級為 [X],北極星指標為 [Y]。目前這些有變化嗎?最新的 DAU/MAU 和留存率是多少?」— 已有的歷史決策和已知痛點不需要重新收集。
- **無上下文(情境 2)**:觸發 Context Bootstrap(`rules-context.md` Section 4,Round 1 + 3),完成後再進入下方標準 S1 數據收集。
- **部分上下文(情境 3)**:從 Decision History 帶入功能變更歷史(知道哪些模組被改過、有哪些風險被識別過),但需詢問整體產品策略和指標(之前只做過功能擴充,缺全局視角)。

### S1 標準引導

> 改版模式的 S1 會主動詢問使用者提供既有產品數據:DAU/MAU、留存率、主要用戶反饋、過去版本的關鍵決策等。若 context 已預填部分答案,改為確認而非重新收集。
> S1 同時收集安全現況:現有認證/授權機制、已知安全漏洞或技術債、近期安全事件。這些資訊會影響改版的風險評估和 Pre-mortem(若觸發)。

### S1 產出要求(Hard Gates)

每一則改版模式 S1 回應都「必須」包含以下全部四項:

1. **將此定調為改版,而非 0-to-1** — 以一兩句話開場,點明這是針對*既有產品*的分析:我們是依現況數據重新檢驗既有 JTBD、對比基準指標,並讀取 `.product-context.md` 取得先前決策。這與 0-to-1 探索(從一張白紙的用戶模型開始)不同。少了這層定調,使用者無從得知為什麼這些問題會不一樣。

2. **逐字引用使用者的實際數字** — 在你的分析中,把使用者 prompt 裡的 MAU、留存下滑 %、cohort 規模、日期等原樣引述回去(例如:「上一季從 85% 掉到 72%,以 2,800 MAU 為基數,代表大約有 N 名受影響的用戶……」)。忽略這些數字的籠統討論會 FAIL 本關。

3. **將使用者陳述的原因當作 H1,而非事實** — 當使用者點名一個可能原因(「留存下滑是功能複雜度造成的」),要明確標記為 H1,並從相同數據中提出至少「兩個」對立假設(H2、H3)。可考慮的對立假設範例:cohort 組成變動、onboarding 退步、定價變動、競品上線、客服品質下滑、功能下架、季節性效應。**不加批判地接受使用者陳述的原因會 FAIL 本關** — 改版模式的價值正在於假設紀律。

4. **資料缺口清單,且至少含一項分群導向的缺口** — 具體列出還需要哪些額外數據,才能在 H1/H2/H3 之間做出區辨。**至少一項「必須」是分群缺口**:cohort(註冊月份)、tier(免費/付費)、role(管理者/一般用戶)、功能使用分群。只寫籠統的「再多做一些用戶訪談」會 FAIL 本關 — 要指名你會訪談「哪個分群」、具體會問「什麼」。

### S1 收尾格式(Hard Gate)

S1 回應結尾必須是編號的 CTA 選單,「絕不」用開放式問題。使用以下確切格式:

```
What's next? Pick one:
  1️⃣ Share the requested data so we can move to S2 (pain-point convergence with hypothesis testing)
  2️⃣ Refine the hypothesis list before collecting data (suggest more H_n candidates)
  3️⃣ Skip to S3 if you already have enough data to converge on a top hypothesis
  4️⃣ Pause and resume later (progress will be saved to .product-playbook-progress.md)
```

以「Any thoughts?」/「Let me know what you think」/「Share what you have」等結尾而沒有編號選單者會 FAIL 此契約 — 使用者需要一個清楚的把手來決定下一步。

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