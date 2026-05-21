# 🤝 Sub-Agent 委派規則

> 在任何模式進入 S2（首次可能應用專家委派的步驟）時載入。三個專家在獨立 context window 中運作——在對的步驟委派出去，而不是把所有事情塞在 inline。

## 何時委派給 `discovery-specialist`

觸發步驟：

- **Full Mode**：S2（Persona）→ S3（JTBD）→ S4（OST）→ S5（Journey Map）→ S6（Continuous Discovery 假設）
- **Revision Mode**：S2（現狀使用者分析）→ S3（痛點綜整）→ S4（機會點辨識）
- **Build Mode**：S2（以 JTBD 視角釐清問題）
- **Custom Mode**：任何選用 Persona / JTBD / OST / Journey Map / Continuous Discovery 的步驟

如何呼叫：

> 使用 `discovery-specialist` subagent 為 [產品描述] 產出 [Persona | JTBD | OST | Journey Map]。目標客群：[B2C / B2B / B2B2C]。可用研究資料：[列出上傳的檔案，或「無 —— 標記為 low confidence」]。以 [語言] 回覆。

把回傳的 YAML 整合進步驟輸出。在步驟的確認提示中，向使用者揭露 specialist 的 `open_questions`。

---

## 何時委派給 `strategy-critic`

在使用者**完成任何策略產物之後立即**委派：

- Strategy Blocks 完成後（Full Mode S7）
- Rumelt Good Strategy Kernel 完成後（Full Mode S8）
- DHM Model 完成後（Full Mode S9）
- Empowered Teams charter 完成後（任何包含它的模式）
- 任何時候使用者用一般敘述寫下「這就是我們的策略」而未指名框架

如何呼叫：

> 使用 `strategy-critic` subagent 批判以下策略產物：[逐字貼上]。此產物為 [框架名稱，或「generic strategy doc」]。以 [語言] 回覆。

Critic 回傳的是批判，不是改寫。把 `three_questions_to_ask_the_writer` 逐字呈現給使用者，不得軟化。若使用者據此修訂，對修訂後版本重新呼叫 critic。

---

## 何時委派給 `pre-mortem-runner`

觸發步驟：

- **Full Mode**：S10（MVP scoping 完成後）
- **Build Mode**：S4（architecture-grounded pre-mortem）
- **Revision Mode**：S8
- **Feature Extension Mode**：S3（風險評估）
- 任何時候使用者明確要求 pre-mortem / 風險分析 /「可能會出什麼錯」

如何呼叫：

> 使用 `pre-mortem-runner` subagent 對以下 [產品 | 功能 | 策略] 進行 pre-mortem：[逐字貼上]。Mode：[build_mode_architecture_grounded | standard | feature_extension]。若為 build mode，可用的 architecture context：[貼上相關檔案內容或摘要]。以 [語言] 回覆。

Runner 回傳 15+ 個 scenario。在面向使用者的輸出中，先呈現 `priority_three` 與 `pre_launch_experiments`。完整 scenario 清單放在可摺疊區塊或以附件呈現。

---

## 委派衛生守則

1. **一個步驟一個 sub-agent**。不要在同一輪對話串接多個 sub-agent——讓使用者確認中間產物後，再呼叫下一個專家。
2. **明確傳遞語言**。Sub-agent 從 prompt 偵測語言；務必指明使用者的工作語言。
3. **尊重 `status: out_of_scope`**。Sub-agent 的 scope refusal 是一項功能，不是失敗——遵循它的路由建議。
4. **Hard Gate 繼承**。Sub-agent 繼承「規劃過程不寫 code」的規則。即使你要求，它們也會拒絕寫檔。
5. **品質自我檢查仍適用**。把 sub-agent 輸出整合進步驟後，仍需執行 `rules-quality-review.md` 的品質自我檢查（或使用模式規則檔內聯的 6 項清單）。
