# 階段一：Discovery — Persona 建立

### 🚫 Discovery 輸出範疇（Hard Gate）

當 orchestrator 被要求執行 Discovery 工作（Persona、JTBD、OST、Journey Map、Continuous Discovery）時,輸出必須**停留在 Discovery 範疇內**。Discovery 回答「用戶是誰」「他們想滿足的未被滿足需求」——僅此而已。下列下游階段的產出絕對**不可**出現在 Discovery 交付物中,即使順手感覺合理:

- **Define 階段產出**:positioning statement、HMW(How Might We)問題、可被解讀為解法提示的痛點矩陣
- **Develop 階段產出**:PR-FAQ 草稿、pre-mortem 情境、RICE 表格、MVP scope 定義、PRD 段落、功能列表
- **Deliver 階段產出**:North Star 指標定義、PMF 判準、GTM 計畫、商業模式區塊、產品規格表
- **Strategy 階段產出**:Strategy Blocks、Rumelt 的 diagnosis / guiding-policy / coherent-action、DHM Model 拆解、OKR 階層

若 Discovery 發現明顯指向某個下游產出(例如 JTBD 浮出清晰的 positioning 角度),可在文末以**一行 open question 或 next-step pointer** 紀錄——但**不要**自己產出該產出。下個階段在規劃流程中有專屬步驟負責它。

不合格範例:JTBD 分析結尾附上填好的 RICE 表、MVP scope 列表、或一段「Recommended Positioning」——即使前面 Discovery 子段都正確,這個輸出仍 FAIL 此 Hard Gate。

---

## Continuous Discovery 習慣（Teresa Torres）

建立一個關鍵習慣：**每週至少接觸一位目標用戶**。Discovery 不是一次性儀式，而是持續系統。

> 「Product discovery 應該是持續的習慣，而不是專案開始前的一次性儀式。」— Teresa Torres

## 1.1 建立 Persona Table

Persona 不是用年齡性別來分群，而是用「用途 / 任務 / 動機」來區分不同類型的用戶。

### 🏢 B2B Hard Gate — 買方 Persona ≠ 使用者 Persona

對於任何 B2B（或 B2B2C）產品,**買方(Buyer)**(簽合約、掌預算、扛供應商風險)與**日常使用者(User)**(每天接觸產品)幾乎都是**目標、痛點、決策準則完全不同**的兩個角色。把他們合併成同一個 Persona 等於把兩個不同的 Job 強塞進一個模糊原型,分析結果無法驅動產品決策。

Hard Gate 規則:
- B2B 預設要產出**兩個獨立的 Persona 區塊**,標示為 `Buyer` 和 `User`,當兩個角色明顯不同(B2B 的預設假設)。
- 若為同一個人(少數例外——通常是創辦人主導的工具或獨資 B2B),請用一句話明確說明「為何此場景中買方就是日常使用者」。
- 兩個 Persona 之間要交叉連結:標出買方的評估準則何處依賴使用者的日常行為(例如「買方的稽核就緒準則取決於使用者是否當天填假單,而不是事後補登」)。

不合格範例:只產出一個 Persona(「HR 經理」),把「核定預算」和「每天填假單」這兩個不同的 Job 硬塞進同一個模糊原型——這個輸出 FAIL 此 Hard Gate。

```
| 欄位 | Persona 1: [暱稱] | Persona 2: [暱稱] | Persona 3: [暱稱] |
|---|---|---|---|
| 用途 / 任務 / 動機 | | | |
| 規模（SIZE） | | | |
| 問題 / 挑戰 / 驅動力 | | | |
| 現在做法與理由 | | | |
| 頻率 | | | |
| 相關資訊來源 | | | |
| 採用/執行過程的問題 | | | |
```

說明切分邏輯；檢查是否 MECE（互斥且完整覆蓋）；指出核心 TA 和次要 TA。

### 🎯 Persona 優先排序 reasoning（Hard Gate）

只說「指出核心 TA」而沒有具體 reasoning 不符合此 Hard Gate。優先排序的陳述必須指出**一個** Persona 為核心,並用**該產品 go-to-market 動態的具體語言**解釋為什麼——而不是泛泛的「使用頻率高」這類理由。

**B2B 產品**若有多個 user persona,reasoning 必須**至少引用一個**下列 B2B 專屬動態(用這些詞彙或顯然等價的概念):

- **Champion vs Buyer** — 誰在組織內倡導採用 vs 誰簽合約;champion-led adoption 通常在 B2B 優先序中勝出,即使 buyer 是「更資深」的 persona
- **Adoption multiplier** — 誰的採用會解鎖整個組織的擴散(例如 HR Specialist 每日使用會種下其他 persona 後續依賴的 system-of-record)
- **Switching-trigger ownership** — 哪個 persona 感受到讓組織從既有工具切換的痛;擁有 switching trigger 的 persona 即使不是最重使用者,也是優先序候選
- **Budget authority** — 誰掌控預算項目;當 buyer ≠ user 時相關,買方的評估準則主導初始成交決策
- **Audit / compliance pressure ownership** — 稽核發現出事時誰的角色受影響;在 regulated B2B segment 中,承受合規壓力的 persona 通常主導優先序

純粹「Persona X 使用頻率更高」或「Persona Y 用戶數更多」的 reasoning 對 B2B 產品 FAIL 此 Hard Gate。頻率是必要條件、非充分條件——B2B 切換由組織壓力驅動,不是個別使用率。

**B2C 產品**的 reasoning 至少引用一個:switching-trigger ownership、JTBD severity differential、network-effect seeding、willingness-to-pay differential。純頻率 reasoning 對 B2C 也 FAIL。

### 📝 Persona 品質自檢清單
- ✅ 切分是否基於「用途/任務/動機」而非人口統計？
- ✅ 各 Persona 之間是否 MECE（互斥且完整覆蓋目標市場）？
- ✅ 是否明確指出核心 TA vs 次要 TA？
- ✅ 每個 Persona 的「問題/挑戰」是否來自真實觀察或合理推論？
- ✅ 「現在做法與理由」是否具體到可以識別 Workaround？
- ❌ 常見問題：按年齡性別分群、Persona 之間差異不明顯、痛點太籠統

## 1.2 建立 Persona 卡片

```
## [Persona 暱稱]：[一句話描述]

**基本資訊**：年齡 / 性別 / 職業 / 所在地 / 個性特質
**背景**：[與產品相關的背景描述]
**目標 / 任務**：[目標1]、[目標2]
**現行做法與理由**：[目前怎麼做、為什麼這樣做]
**資訊來源**：[從哪裡獲取相關資訊]
**阻礙 / 問題 / 挑戰 / 不滿意**：[痛點1]、[痛點2]、[痛點3]
```

---

## 📎 本階段的檔案整合提示

如果使用者在此階段上傳了檔案，Claude 依據以下規則整合：

| 上傳內容 | 整合到 | 整合動作 |
|---------|-------|---------|
| 用戶訪談逐字稿 / 錄音文字 | 1.1 Persona + 1.3 JTBD | 提取：用戶背景 → Persona 欄位；痛點 + 現行做法 → JTBD 深挖五問；情緒反應 → 情感性/社交性 Job |
| 用戶調研報告（PDF） | 1.1 + 1.2 + 1.3 | 提取量化數據（用戶分群比例）填入 Persona 規模；提取質化洞見填入 JTBD |
