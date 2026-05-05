# 🔵 Optional 步驟觸發規則

> Optional 步驟觸發條件與 Phase 決策點格式的權威來源。由 Full / Revision / Custom 模式規則檔載入。

此檔案集中定義 Optional 步驟的觸發條件，使各模式規則檔不需重複描述。

---

## 1. Core 與 Optional 的定義

- **Core（核心）**：必定執行。除非使用者明確要求覆寫，否則不可省略。
- **Optional（選用）**：僅在至少一個觸發條件成立時執行。使用者可隨時強制加入或強制略過。

---

## 2. Persona-Journey 捆綁規則（全域）

**Journey Map 是 Persona 的自然延伸：Persona 定義「Who」，Journey Map 描繪「Who 所經歷的旅程」。完成 Persona 步驟後，Journey Map 預設納入流程，僅在情境真的太過簡單而無法構成旅程時才略過。**

> ⚠️ 此規則修正了過去「0-to-1 不需要 Journey Map」的錯誤假設。事實正好相反——Teresa Torres（Continuous Discovery）、Indi Young（Mental Models）以及 Amazon Working Backwards 流程都把 Journey Map 視為 0-to-1 階段不可或缺的工具，因為它形塑了新體驗的設計方式。真正的關鍵變數是**使用者的 Job 是否跨越多個階段**，而不是產品是否已存在。

### 跳過條件（預設 ON；只有以下任一成立時才略過）

1. **單一互動點** — 該 Job 由單一 API 呼叫、單一按鈕、純後端服務，或純設定工具完成（不存在多階段流程）
2. **流程僅 1–2 步** — 整個使用者流程過於簡短，Journey Map 退化為一張清單，沒有有意義的階段轉換
3. **使用者明確要求跳過** — 例如「skip Journey Map」「我不需要 Journey Map」

### 跳過時的行為

向使用者揭露此決策，不得無聲略過：

> 「Persona 已完成。基於目前的上下文（[單一互動點 / 流程僅有 N 步]），Journey Map 將被略過。隨時可以回覆『add journey』補上。」

### 觸發時的行為（預設）

進入 Journey Map 步驟前，輸出簡短的評估說明，引用**為什麼**需要：

> 「Persona 已完成。該 Job 跨越 [N] 個階段（[階段 A → 階段 B → ...]）——將進入 User Journey Map。若不需要請回覆『-S3』跳過。」

---

## 3. Optional 觸發條件 — Full Mode

| 步驟 | 框架 | 預設 | 邏輯 |
|------|-----------|---------|-------|
| S3 | User Journey Map | **ON** | 見上方 Persona-Journey 規則（第 2 節）。僅在單一互動點 / 流程 ≤2 步 / 使用者明確要求跳過時略過 |
| S6 | April Dunford 定位 | OFF | 觸發條件：(a) 新產品上市 或 (b) 重新定位 或 (c) 產出對象包含 Sales/BD/行銷 |
| S11 | PMF + GTM + 商業模式 + 假設驗證計畫 | OFF | 觸發條件：(a) 產品即將上市 或 (b) 產出對象為老闆/資料科學家 或 (c) 使用者明確要求驗證計畫 |

---

## 4. Optional 觸發條件 — Revision Mode

| 步驟 | 框架 | 觸發條件（任一成立） |
|------|-----------|------------------------------|
| S4 | Positioning 重新評估 | 使用者提到「定位漂移」/「市場改變」 或 產出對象包含 Sales/行銷 |
| S6 | Pre-mortem | (a) 改動範圍 ≥30% 既有功能 或 (b) 涉及金流/權限/資料遷移 |

---

## 5. Phase 決策點輸出格式

**進入每個包含 Optional 步驟的 Phase 之前，AI 必須輸出 Phase 決策點區塊，列出本 Phase 將執行哪些 Core/Optional 步驟與原因。**

### 必要格式

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔀 Phase [N] 步驟決策

✅ Core（必定執行）：S[a], S[b]
🔵 Optional 評估：
  • S[x] [框架名稱]（預設 ON）： [執行 / 跳過] — [原因]
  • S[y] [框架名稱]（預設 OFF）：[觸發 / 跳過] — [原因]

→ 本 Phase 將執行 [N] 個步驟
（回覆「+S[x]」強制加入、「-S[y]」強制跳過，或直接繼續）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

對於預設 ON 的步驟（例如 S3 Journey Map），條件成立時使用 **執行（PROCEED）**，跳過條件命中時使用 **跳過（SKIP）**。
對於預設 OFF 的步驟（例如 S6 Positioning、S11 PMF/GTM），條件成立時使用 **觸發（TRIGGER）**，否則使用 **跳過（SKIP）**。

### 何時呈現

- 在每個包含至少一個 Optional 步驟的 Phase 開始時呈現一次
- 僅含 Core 步驟的 Phase **不需要**決策點（直接進入）
- 呈現後，等待使用者回覆。非覆寫式的回覆（例如「ok」「繼續」或具體內容）即視為「接受 AI 的決策」

### 使用者覆寫指令

| 使用者輸入 | 行為 |
|------------|----------|
| `+S[x]` 或「加入 S[x]」 | 強制加入先前被跳過的 Optional 步驟 |
| `-S[y]` 或「跳過 S[y]」 | 強制跳過先前被觸發的 Optional 步驟 |
| 具體內容 / 「繼續」 / Enter | 接受 AI 的評估，繼續執行 |

---

## 6. Custom Mode — Persona-Journey 條件式插入

Custom Mode 預設組合（Lean / Standard / Comprehensive）有固定的步驟序列，但只要該預設包含 Persona 步驟，Persona-Journey 捆綁規則仍然適用。

| 預設 | 預設行為 | 完成 Persona 後的行為 |
|--------|------------------|----------------------------|
| **Lean** | 不含 Persona 步驟 | 不適用 |
| **Standard** | 8 步固定，S1 = Persona | 完成 S1 後，AI 依第 2 節執行 Persona-Journey 評估。若跳過條件**不**成立，AI 主動將 Journey Map 條件式插入為 **S1.5（變成 9 步流程）**，使用者可回覆 `-journey` 還原。若跳過條件成立，靜默跳過並於最終產出揭露（第 7 節）。 |
| **Comprehensive** | 11 步固定，S2 = Persona、S3 = Journey Map（已內建） | AI 可顯示一段簡短的「可跳過」提示：「Journey Map 已預設納入。若你的情境太過簡單而無法構成旅程，請回覆 `-S3` 跳過。」否則正常進行。 |

如此安排，可避免在情境真的單純時打斷 Lean/Standard 使用者，也確保**真正會受益**於 Journey Map 的使用者不被無聲拒絕。

---

## 7. 最終產出揭露

模式結束時，最終的產品規格摘要必須列出本次被跳過的 Optional 步驟，並提供一鍵補上的指令，例如：

> 「本次跳過的 Optional 步驟：S6（Positioning）、S11（PMF/GTM）。回覆『加入 S6』或『加入 S11』即可補上。」
