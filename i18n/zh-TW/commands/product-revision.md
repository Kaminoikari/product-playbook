---
description: 改版模式產品規劃 — 針對既有產品改版優化，有用戶數據和功能基礎
argument-hint: <產品名稱與改版目標>
---

觸發 product-playbook skill。
然後讀取 references/rules-revision.md 取得步驟序列。
執行各步驟時，依 rules-revision.md 中的 Reference 載入指示讀取對應的 reference 檔。

執行模式：🔄 改版模式
產品描述：$ARGUMENTS

依照 rules-revision.md 的步驟序列(S1 → S8,Optional 步驟由 rules-optional-trigger.md 中的觸發條件決定是否執行)執行。S1 會主動詢問既有產品數據(DAU/MAU、留存率、主要用戶反饋等)。在含 Optional 步驟的 phase 開始前輸出 Phase 決策點,每步驟顯示進度指示器。
