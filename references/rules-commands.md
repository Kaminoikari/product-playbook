# 🔧 框架選單 + 補充指令

> 當使用者要求「列出框架」「給我看有哪些框架」或使用補充指令時載入。

## 指定框架

**觸發方式有兩種：**

**方式 A（使用者直接說框架名稱）：** 直接進入該框架引導流程，不需要再問。

**方式 B（使用者說「我想指定框架」「列出所有框架」等）：** 呈現以下選單：

```
📚 可指定的框架清單，請填寫編號或名稱：

【理解用戶】
 1. JTBD（Jobs to Be Done）— 找出用戶真正想完成的工作
 2. Persona — 建立用途/任務/動機導向的用戶角色
 3. User Journey Map — 繪製用戶完整體驗旅程
 4. Continuous Discovery — 建立每週接觸用戶的持續習慣

【定義問題】
 5. OST / 機會解法樹 — 系統化連結機會與解法
 6. Positioning / April Dunford — 找出真正的競爭場域和差異化
 7. HMW — 將痛點轉化為設計問題

【解法設計】
 8. Working Backwards / PR-FAQ — 從用戶結果出發倒推解法
 9. Pre-mortem / 事前驗屍 — 在失敗前預測並預防失敗
10. GEM — Growth / Engagement / Monetization 三維優先排序
11. RICE — 量化功能優先排序
12. MVP — 定義最小可行產品範圍

【策略層】
13. Strategy / Strategy Blocks — Mission → Vision → Strategy 層級結構
14. DHM Model — Delight / Hard to copy / Margin-enhancing 機會檢驗
15. LNO Framework — Leverage / Neutral / Overhead 時間分配
16. Empowered Teams — 賦能型團隊 vs 功能型團隊

【衡量層】
17. North Star / 北極星指標 — 定義代表核心用戶價值的單一指標
18. PMF — 判斷產品市場契合度的四個等級
19. Sean Ellis Score — 量化 PMF 熱情程度

【商業層】
20. 商業模式與定價 — 收費模式選擇與價值定價對齊
21. GTM 策略 — Go-to-Market 上市與獲客策略

【開發銜接】
22. Dev Handoff / 開發交接包 — 產出 CLAUDE.md + TASKS.md + TICKETS.md，銜接 Claude Code 開發

請輸入框架編號或名稱（可多選，用逗號分隔）：
```

## 跳過 Discovery / 直接進實作

當使用者說「跳過用戶研究」「問題已知」「直接進到 Develop」時，讀取 `references/rules-build.md` 並依照直接實作模式步驟序列執行。

> 提醒使用者：「跳過用戶研究階段，代表解法建立在假設上。建議執行後盡快進行 Continuous Discovery 驗證。」

## 功能擴充模式觸發

- 「新增功能」/「我要在現有產品加一個功能」/「加新功能」→ 觸發功能擴充模式（讀取 `references/rules-build.md` → 功能擴充快速路徑）

## 補充指令

| 指令 | 行為 |
|------|------|
| `「切換到 [框架]」` | 立即切換，保留已完成內容 |
| `「我想改變目標對象」` | 重新調整框架優先序和呈現方式 |
| `「跳過這個步驟」` | 提醒必要性後尊重決定，進入下一步 |
| `「回到 [步驟/框架名稱]」` | 回到指定的任意步驟重新引導（見 `references/rules-change-propagation.md`） |
| `「幫我簡化」` / `「幫我展開」` | 濃縮核心要點 / 深入補充分析 |
| `「產出報告」` | 讀取 `references/06-html-report.md`，產出 HTML 企劃報告 |
| `「產出 PRD」` / `「產出給工程師的文件」` | 讀取 `references/04b-solutions.md`，整合 PR-FAQ + MVP + User Story + Pre-mortem，**自動一併產出：流程圖（Mermaid）+ DB schema（Mermaid ERD）+ UI wireframe（HTML）** |
| `「產出流程圖」` / `「幫我畫流程圖」` | 以 Mermaid 語法產出流程圖（單獨觸發） |
| `「產出 DB schema」` / `「幫我設計資料庫」` | 產出 DB schema（Mermaid ERD 語法）（單獨觸發） |
| `「產出 UI wireframe」` / `「幫我畫線框圖」` | 以 HTML/SVG 產出低保真 UI 線框圖（單獨觸發） |
| `「產出簡報」` / `「幫我做成 PPT」` | 呼叫系統 pptx skill |
| `「把文件調整成給 [對象] 看的版本」` | 重新編排框架重點和呈現語言 |
| `「我只有 15 分鐘」` | 給出最關鍵的三個決策問題或行動 |
| `「幫我做完整性評估」` | 評估哪些環節完整、哪些有風險 |
| `「幫我找出假設」` | 識別所有尚未驗證的核心假設清單 |
| `「做一次 Pre-mortem」` | 對任何解法立即進行事前驗屍 |
| `「產出給不同對象的版本」` | 自動產出多個對象版本的摘要 |
| `「這個產品在 PMF 哪個等級？」` | 判斷 PMF 等級並說明下一步里程碑 |
| `「幫我找出瓶頸」` | 分析最影響 Aha Moment 到達率的障礙 |
| `「我要改版，不是新產品」` | 切換改版模式（讀取 `references/rules-revision.md`） |
| `「我要說服老闆批准」` | 切換老闆模式，突出商業價值和資源邏輯 |
| `「進入開發」` / `「產出開發交接包」` | 讀取 `references/07a-handoff-core.md`，確認技術棧後產出完整開發交接包 |
| `「幫我建專案」` / `「接到 Claude Code」` | 同上 |
| `「暫停」` / `「存檔」` / `「先做別的」` | 依 `references/rules-progress.md` 存檔 |
| `「繼續」` / `「回到企劃」` | 依 `references/rules-progress.md` 恢復 |
| `「清除進度」` / `「重新開始」` | 刪除進度檔案，從頭開始 |
| `/export [format]` | 匯出為指定格式。format = `pdf` / `docx` / `pptx` / `html` / `md`。讀取 `references/rules-export-document.md`，首次使用時先載入 `references/rules-document-tools.md` 檢查工具。 |
| `/parse [file]` | 解析上傳的文件為 Markdown。支援 PDF / DOCX / PPTX / 圖片。讀取 `references/rules-import-document.md`，首次使用時先載入 `references/rules-document-tools.md` 檢查工具。 |

**上下文相關指令提示**：每個步驟完成時，根據當前進度主動提示 2-3 個最相關的可用指令。
