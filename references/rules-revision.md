# 🔄 改版模式步驟序列（共 12 步 + 最終產出）

> 此檔案為改版模式的權威步驟定義。由 SKILL.md 核心派發載入。

## 步驟序列

```
Phase 0：現況分析
  S1.  既有產品現況回顧（用戶數據概覽 + 核心指標 + 已知問題 + 安全現況）
  S2.  現有用戶 JTBD 重新檢驗（哪些 Job 做得好？哪些做不好？）

Phase 1：問題收斂
  S3.  用戶痛點收集（留存/流失分析 + 用戶反饋彙整 + 行為數據）
  S4.  痛點彙整表 → 讀取 references/03-define.md → 2.1
  S5.  Positioning 重新評估 → 讀取 references/03-define.md → 2.2（焦點：定位是否需要調整？）
  S6.  HMW 問題轉化 → 讀取 references/03-define.md → 2.3
  S7.  機會評估表 → 讀取 references/03-define.md → 2.4

Phase 2：解法設計
  S8.  PR-FAQ → 讀取 references/04a-prfaq.md（描述改版後的體驗）
  S9.  Pre-mortem → 讀取 references/04b-solutions.md → 3.3
  S10. MVP 範圍 + Not Doing List → 讀取 references/04c-mvp.md（焦點：改什麼 / 不改什麼）

Phase 3：驗證
  S11. North Star + Aha Moment → 讀取 references/05a-northstar-aha.md（比較改版前後指標）
  S12. 假設驗證計畫 → 讀取 references/05c-validation-spec.md
────
最終產出 → 產品規格摘要（改版版）
```

### S1 前置：產品上下文載入

進入 S1 前，讀取 `references/rules-context.md` 並檢查 `.product-context.md`：

- **有完整上下文（情境 1）**：自動帶入 PMF 等級、North Star、已知痛點、安全現況、近 3 筆 Decision History。S1 引導改為**差異式**：「上次評估時，你的 PMF 等級為 [X]，北極星指標為 [Y]。目前這些有變化嗎？最新的 DAU/MAU 和留存率是多少？」— 已有的歷史決策和已知痛點不需要重新收集
- **無上下文（情境 2）**：觸發 Context Bootstrap（`rules-context.md` Section 4，Round 1 + 3），完成後再進入下方標準 S1 數據收集
- **部分上下文（情境 3）**：從 Decision History 帶入功能變更歷史（知道哪些模組被改過、有哪些風險被識別過），但需詢問整體產品策略和指標（之前只做過功能擴充，缺全局視角）

### S1 標準引導

> 改版模式的 S1 會主動詢問使用者提供既有產品數據：DAU/MAU、留存率、主要用戶反饋、過去版本的關鍵決策等。若 context 已預填部分答案，改為確認而非重新收集。
> S1 同時收集安全現況：現有認證/授權機制、已知安全漏洞或技術債、近期安全事件。這些資訊會影響改版的風險評估和 Pre-mortem。

### 快速路徑

當使用者在 S1 已提供充分數據（含用戶反饋、指標、痛點），S4-S7（痛點→定位→HMW→機會評估）可在單次對話中連續產出，中間只需一次確認而非四次。觸發條件：S3 收集到的痛點清單已有明確的優先級和數據支持。Hard Gate 規則不變 — 每個步驟的產出仍須完整呈現，只是確認節奏加快。

## Reference 載入指示

| 步驟 | Reference 檔案 |
|------|---------------|
| S1-S3 | 無需外部 reference（直接引導使用者提供數據） |
| S4-S7 | `references/03-define.md` |
| S8 | `references/04a-prfaq.md` |
| S9 | `references/04b-solutions.md` |
| S10 | `references/04c-mvp.md` |
| S11 | `references/05a-northstar-aha.md` |
| S12 + 最終產出 | `references/05c-validation-spec.md` |

## 最終產出格式

**改版產品規格摘要**：改版前後對照 + 改什麼/不改什麼 + 成功指標

完成後，依 `references/rules-end-of-flow.md` 執行流程結束規則。
