# ✏️ 自訂模式步驟序列

> 此檔案為自訂模式的權威步驟定義。由 SKILL.md 核心派發載入。

選擇一個完整性等級（或自行挑選步驟）：

## 🔴 低（Lean）— 共 4 步

```
S1. JTBD 陳述 → references/02b-jtbd.md
S2. HMW 一個 → references/03-define.md
S3. PR-FAQ → references/04a-prfaq.md
S4. North Star → references/05a-northstar-aha.md
（任一步驟可由使用者替換為其他框架）
────
最終產出 → 產品規格摘要（未執行欄位標記為「未執行」）
```

## 🟡 中（Standard）— 共 8 步（需要 Journey Map 時自動擴充為 9 步）

> Full Mode 的 8 步子集：Full Core 去掉策略診斷、加入 Positioning。Standard 的使用者通常比深度策略診斷更早需要市場定位，因此做此調換。
>
> **Persona-Journey 條件式插入**：完成 S1（Persona）後，AI 依 `rules-optional-trigger.md` 第 2 節執行 Persona-Journey 評估。若跳過條件**不**成立（即 Job 跨越多個階段），AI **主動把 Journey Map 條件式插入為 S1.5**，使整體變成 9 步流程。使用者可回覆 `-journey` 還原為 8 步。若跳過條件成立（單一互動點 / 流程 ≤2 步），靜默跳過並於最終產出揭露。

```
S1.   Persona（Table + 卡片） → references/02a-persona.md
S1.5  User Journey Map [預設條件式插入；僅在情境太簡單時才跳過]
      → references/02c-ost-journey.md
S2.   JTBD 分析 → references/02b-jtbd.md
S3.   痛點 + HMW + 機會排序 → references/03-define.md
S4.   April Dunford 定位 → references/03-define.md
S5.   PR-FAQ → references/04a-prfaq.md
S6.   解法評估（平行原型 + Pre-mortem + GEM + RICE） → references/04b-solutions.md
S7.   MVP + Not Doing List → references/04c-mvp.md
S8.   North Star + 三層訊號 + Aha Moment → references/05a-northstar-aha.md
```

## 🟢 高（Comprehensive）— 共 11 步

> Full Mode Core 加上全部預設 OFF 的 Optional 觸發（Positioning + PMF/GTM/BM/驗證）。**S2 Persona 之後立即接續 S3 User Journey Map**，依 Persona-Journey 捆綁規則。如果情境真的太過簡單，可以在 Persona 之後回覆 `-S3` 還原為 10 步。

```
S1.  策略診斷 → references/00-opportunity-check.md + references/01-strategy.md
S2.  Persona（Table + 卡片） → references/02a-persona.md
S3.  User Journey Map → references/02c-ost-journey.md   ← 與 S2 捆綁（預設 ON）
S4.  JTBD 分析 → references/02b-jtbd.md
S5.  痛點 + HMW + 機會排序 → references/03-define.md
S6.  April Dunford 定位 → references/03-define.md
S7.  PR-FAQ → references/04a-prfaq.md
S8.  解法評估（平行原型 + Pre-mortem + GEM + RICE） → references/04b-solutions.md
S9.  MVP + Not Doing List → references/04c-mvp.md
S10. North Star + 三層訊號 + Aha Moment → references/05a-northstar-aha.md
S11. PMF + GTM + 商業模式 + 假設驗證計畫 → references/05b-pmf-gtm.md + references/05c-validation-spec.md
```

## Reference 載入規則

進入各步驟時，僅讀取對應的 reference 檔案（不要預先全部載入）。各步驟旁已標注對應的 reference 路徑。

## Persona-Journey 捆綁

依 `references/rules-optional-trigger.md` 第 2、6 節，只要 Custom 預設包含 Persona 步驟，Journey Map 就**預設 ON**：

- **Comprehensive**：Journey Map 已硬編碼為 S3（如上序列）。使用者可在 Persona 之後回覆 `-S3` 跳過。
- **Standard**：當跳過條件不成立時（多階段 Job），Journey Map 自動條件式插入為 **S1.5**。當情境太過簡單（單一互動點、流程 ≤2 步、使用者要求跳過）時，靜默跳過並於最終產出揭露。
- **Lean**：不含 Persona 步驟，故此規則不適用。

跳過條件（任一成立 → 跳過 Journey）：
1. 單一互動點（API、單一按鈕、後端服務、設定工具）
2. 流程僅 1–2 步
3. 使用者明確要求跳過

## 最終產出格式

**產品規格摘要**（僅整合已完成的步驟，未執行的欄位標記為「未執行」）。

完成後，依 `references/rules-end-of-flow.md` 執行流程結束規則。
