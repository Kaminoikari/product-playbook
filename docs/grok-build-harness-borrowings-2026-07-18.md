# grok-build Harness 借鏡報告（2026-07-18）

來源：https://github.com/xai-org/grok-build（xAI 開源的 Grok Build CLI/agent runtime，Rust，2,761 檔案）。
研究方法：12 個平行 reader 深讀各子系統（prompt templates、goal-mode 編排、內建 skills、24 篇 user-guide、compaction、subagent resolution、hooks 引擎、circuit breaker、changelog 全掃、本地現況盤點），其中 7 個領域經 adversarial verifier 逐條覆核。共萃取 180 個機制（per-domain：core-prompts 19、goal-mode 12、builtin-skills 8、docs-config 22、docs-hooks-memory 14、docs-modes-safety 22、token-economy 16、subagents-lifecycle 10、context-state 8、reliability-hooks 17、changelog-sweep 17、local-inventory 15）。goal-mode 與 core-prompts 的 8 份模板與 3 份 skill 由本 session 親讀原檔；引用的關鍵數字（85% compaction、retry 15、classifier cap 10、stall threshold 2 等）已用 grep 對原始碼逐一覆核。

**驗證狀態聲明**：builtin-skills、docs 三領域、subagents-lifecycle 經獨立 verifier 確認；token-economy、context-state、reliability-hooks-engine、changelog-sweep 的 verifier 撞到 session limit 未跑，本報告只引用其中已由本 session grep 覆核或有雙讀者交叉印證的細節，未覆核的個別數字在文中標註。

---

## 一、grok-build harness 架構總覽

四層設計，每層都值得對照：

1. **Prompt 紀律層**：主 system prompt 僅 45 行；所有動態內容（git status、AGENTS.md、日期、背景任務狀態）以 `<system-reminder>` user message 注入，永不重寫 system prompt（保 prompt cache）。subagent prompt 有尺寸回歸測試（general <3700 字元、read-only <2800）。
2. **Goal-mode 編排層**（長任務品質引擎）：Planner（一次性、產出凍結的 outcome 合約）→ Implementer（留存證據）→ 3 個 adversarial Skeptic（多數決、audit-don't-author）→ Strategist（連續卡關才出場，只改 HOW 不改 WHAT）→ Summarizer（≤80 字收尾）。每個角色有 fail-open/fail-closed 的明確語義與數字預算。
3. **機制層**：compaction（85% 觸發、user 訊息與 AGENTS.md verbatim 不經 summarizer）、doom-loop 偵測（identical-args 才算）、circuit breaker、retry 分類（deterministic 永不重試）、hunk tracker、記憶體 dream consolidation。
4. **Hooks/Config 層**：14 個事件、只有 PreToolUse 可 block、一律 fail-open、無效 matcher fail-closed（裝 never，不放寬成 match-all）、每個自我修正迴圈都有 fire cap。

**貫穿的設計哲學**（最值得整體吸收）：
- 每個 retry/nudge/verify 迴圈都有明確數字預算與預算耗盡後的升級路徑
- 「gate 說 no」與「gate 自己壞了」永遠分開處理
- 證據由 implementer 生產、reviewer 稽核，不重建
- 收斂保護是雙向的：既防 rubber-stamp（default to refuted），也防無限挑剔（anti-ratchet + anti-invention）

---

## 二、借鏡清單

### A. 全域 CLAUDE.md / fable-soul（純文字改動，P0）

**A1. Reviewer 收斂三原則**（來源：`goal_verifier_prompt.md`）
- 「Default to refuted if uncertain」：不確定 required criterion 是否成立時判 refuted；但這永遠只作用於合約內的條款，不是加新需求的許可。
- Anti-ratchet：「The bar does NOT rise between rounds」。重驗回合的主要工作是確認 prior gaps 真的修好；每輪換新挑剔是讓任務永遠收不了尾的失敗模式。
- Anti-invention：「Inventing requirements beyond the contract is the most common FALSE refute」。禁止以 Non-goals 裡的項目、edge case、額外 robustness、test-construction 偏好為由 refute。
- 本地缺口：dev-discipline gate 5 的 dual reviewers 目前沒有這三條，正是 review 迴圈 token 黑洞的成因。soul rule 20（confirm before flagging）已有一半，補上另一半（anti-ratchet）。

**A2. NO TEST THEATER 四型態**（來源：`goal_rules.md`，四個具名作弊）
> a passing test must prove the SHIPPED code works on the real path. Never hard-code the expected value, start past the thing under test, re-implement the code under test inside the test, or report success without driving the real entry point.

搭配 honest-vs-hacky 判準（來源：verifier prompt）：mock 環境邊界（clock/RNG/network/sink）= honest；假造 unit 自身邏輯或期望輸出 = theater。放進 CLAUDE.md 測試段與 dev-discipline gate 1。

**A3. task_completion_discipline 四條**（來源：`goal_task_discipline.md`）
1. Tool-call first, narration second：敘述動作的句子必須與 tool call 同一則回應；「If you end a turn with such a sentence but no tool call, the action did not happen.」
2. 不為 in-flight 工作要許可（cadence negotiation、確認顯而易見的下一步都不算真 ambiguity）。
3. Todo 是自己的 scratchpad，非交付物；不過度拆解、不花 turn 做簿記。
4. 別留著無阻塞的 easy work 就停手；合法停點只有三種：等背景任務、真 ambiguity、硬外部 blocker（明說）。
與 soul rule 4/15 重疊但表述更鋒利，建議以此措辭替換，並把「narration 無 call = 動作沒發生」加進 rationalization table。

**A4. 失敗分類 taxonomy**（來源：`retry_policy.rs` + `sampler/retry.rs`，已 grep 覆核）
重跑任何失敗指令前先分類：
- deterministic（語法錯、斷言失敗、400/403/404、parse error）：永不原樣重跑，改 code 或改假設
- transient（timeout、網路、5xx）：退避重試至多 2 次然後停手回報
- auth/config（401、缺 env、路徑錯）：修一次原因，再試一次
- rate limit（429）：至多等 2 次就上報（grok 常數 `RATE_LIMIT_RETRY_THRESHOLD=2`：「no point burning a long backoff just to be rate-limited again」）
這是 soul rule 13 的具體預算版。另加 circuit-breaker 習慣：同一外部目標（API、flaky test runner、MCP server）失敗 ≥3 次且失敗率 ≥50% 即宣告 OPEN，停止呼叫並告知使用者，恢復時只發一次 probe。

**A5. Plan-mode 分流準則**（來源：`19-plan-mode.md`，正反清單近乎照抄）
- 要 plan：真架構歧義（session vs JWT、Redis vs in-memory、WS vs SSE）、改錯方向重工代價大
- 不 plan：明顯 bug fix、循慣例的功能、rename/格式/測試、「update error handling」（直接動手邊做邊問）、「can we work on X」（使用者要開工）；研究探索走 subagent 不走 plan
這條直接落實「小功能不燒 token 在規劃」的目標。

**A6. 其他單行規則**
- 「One approval is not a blank check」：shared-state 動作（push/PR/comment）的核准是單次的；發現不明檔案/branch 先調查再刪。
- 測試範圍階梯：先跑最貼近改動的測試，綠了再擴大；「whole repo suite only when the change is repo-wide」。
- 機械修復迴圈（format/lint）上限 3 次，然後回報。
- 收尾訊息 ≤80 字：交付了什麼 + 怎麼跑（exact command），壞消息先講；其餘進 PR body。
- 大輸出導檔再 grep（`cmd > scratch/out.txt`），不讓巨量輸出進 context 觸發提早 compaction。
- bytes/4 ≈ token 估算：讀大檔前 `wc -c` 除 4 判斷要不要整讀。
- Monitor 衛生：pipe 一律 `grep --line-buffered`、never pipe raw logs、遠端輪詢 ≥30s。

### B. Hooks（決定性強制，P1）

**B1. Stop hook 升級**（強化現有 `require-tests-before-stop.sh`）
- bail-phrase regex panel（來源：`goal_stop_detector.rs`）：對最後一段行首錨定比對「Stopping here / I'll check back later / unable to proceed / Ready for review」等；命中且 todo 未清 → block 一次。設計紀律照抄：行首錨定防誤傷、每次觸發記 log 以便修剪 false-positive pattern、fire cap（現有 stop_hook_active 機制已滿足）。
- 前端驗證缺口：diff 含前端檔案但 transcript 無 playwright/screenshot 證據 → 提醒一次。這是本地最大盲點（require-tests-before-stop 對 UI 改動完全放行，與「前後端都零問題」目標直接衝突）。
- 現有 hook 只驗「測試指令跑過」，不驗通過；可加解析最後一次 test run 的 exit 狀態。

**B2. PostToolUse doom-loop hook**（來源：changelog 0.2.36–0.2.52 的調參史）
對失敗的 tool call 記 (tool + normalized args) hash；第 2 次 identical 失敗注入「STOP：同一呼叫已失敗 N 次，說出錯誤假設並換層/換工具」。調參教訓照抄：以 identical args 為 key（不是失敗計數），否則平行呼叫批次失敗、同檔多次不同修復都會誤報。

**B3. PreToolUse bash-policy guard**（來源：`no-recursive-grep-guard.py`，該腳本輸出格式已是 Claude Code 的 `hookSpecificOutput.permissionDecision`，可近乎直接複製）
- 核心思想：「The system prompt only asks the model to avoid it; this hook turns that into a hard, deterministic block」。每把一條 CLAUDE.md 的 never-do 規則搬進 hook，就省下一條常駐 context 且不可靠的 prompt 規則。
- 候選規則：grep -r → 導向 Grep tool；cat 巨檔警告；.env 讀取封鎖。
- 配套原則：「guard = hook + deny rule, never hook alone」（hooks fail-open，安全底線必須同時存在於 `permissions.deny`）。現有 pre-write-secret-guard 只擋寫入，Bash 讀取 .env 無防護，建議補 `Read(**/.env)` deny 並實測 shell 路徑是否也被攔。
- 帶 `--self-test`（原腳本 43 個 case），guard 本身可測試。

**B4. PreCompact / session-handoff**
- 9-section compaction prompt（來源：`full_replace_summary_prompt.txt`）做成 handoff 慣例：Primary Request / Key Concepts / Files+Code / Errors and Fixes / Problem Solving / All User Messages 依序 / Pending Tasks（不發明任務）/ Current Work / Next Step 附 verbatim quote「so the task is interpreted without drift」。
- 結構原則：user 的請求與專案規則 verbatim 保留或給路徑重讀，永不讓 summarizer 改寫需求。
- PreCompact hook（先確認安裝版 CLI 支援此事件）：提醒把未決策、未驗證變更、touched paths dump 到檔案；「a handoff note must list open TODOs, unverified changes, and file paths touched; if it cannot, it is too short」（compaction 拒收 <500 字元 summary 的移植版）。

**B5. Hook 作者成文標準**（本地缺口：慣例只散在各腳本中）
- 「gate 說 no」= exit 2 + 具體理由；「gate 自己壞了」= exit 0/1 + log 警告，永不偽裝成 policy denial
- 一律輸出 explicit JSON decision，不靠裸 exit code
- 明確短 timeout（5–10s），任何 gate 都是每次 tool call 的稅
- 輸出必須 deterministic（無 timestamp、無隨機排序），否則打爆 prompt cache（changelog 0.2.41 的教訓：byte-stable prefix 保 KV cache）
- kill-switch：每個 hook 開頭讀 `~/.claude/disabled-hooks`，被點名即 exit 0（免改 settings.json、免版本 bump）
- 跨來源查重：Claude Code 不會 dedup plugin + global 的相同 hook
- 觀察模式先行：新 gate 先 log-only 跑一輪調 false positive，再開 block（grok laziness detector 的 two-step rollout）

**B6. 輕量觀測**（來源：`tool-logger.sh` + OTEL 指標集）
- 3 行 PostToolUse hook 把 tool_name+timestamp append 到 `~/.claude/tool-activity.log`，定期分析：哪些 permission prompt 重複出現、哪些工具吃時間。
- eval 腳本標準化 `--output-format json` 並記錄 input/cache_read/output tokens + num_turns，把 cache-hit ratio 當 plugin eval 的成本 KPI（現有 evals/*.json 缺這個維度）。
- 誠實成本語義照抄：任何成本彙總，缺任一分項就整體不出數字並說明原因，「absence means unreported, never free」。

### C. product-playbook dev-discipline 升級（P0–P1）

**C1. Gate 5（dual reviewers）全面升級**：
1. 兩位 reviewer prompt 加入 A1 三原則全文
2. 固定輸出合約：typed findings JSON（kind: bug|gap|todo、location: path:line、detail 一行）+ 結尾 sentinel `VERDICT: PASS|FAIL`；缺 sentinel = FAIL（fail-closed）；orchestrator 機械解析
3. Evidence 合約：implementer 送審前把實際測試輸出（前端加 screenshot）存到 scratch 路徑；reviewer 稽核該證據（honest vs hacky），只做便宜 spot-check，缺證據就 refute 並指名要求，不自己補
4. PRIOR_GAPS threading：每輪 findings 存 findings.json，下輪開頭聲明「主要任務是確認這些已修好；標準不升高」
5. 收斂控制：比對本輪與上輪 findings 的 location 集合，identical → 停止迭代直接升級給使用者（grok stall threshold = 2）；總回合上限 3
6. findings 修法指向：測不了就重構出 directly-callable pure unit，禁止 patch 測試繞過（「that whack-a-mole never converges」）
7. reviewer subagent 定義為唯讀工具集（Read/Grep/Glob，無 Edit/Bash 寫入），並在 prompt 開頭令其先讀 CLAUDE.md/專案慣例（changelog 0.2.12：reviewer 與 implementer 看同一本規則書）
8. spec reviewer 額外收 PLAN.md 的 git diff：弱化驗收條款本身就是 finding

**C2. Plan 合約模板**（大任務進場條件，配 A5 分流）：
```
# Plan: <一句話>
## Goal kind        code-change | analysis | research
## Acceptance criteria   3-5 條、gating、outcome-based（禁止指定檔名/函式名）、分組不砍
## Verification plan     每步標 gating|evidence + 必須觀察到什麼
## Non-goals            必填（未要求但讀者可能以為在範圍內的）
## Assumed scope
## Implementation approach   guidance，非合約
## Task checklist       3-8 個 checkbox，邊做邊勾；guidance，非合約
## Deviations           單一段落、每項一 bullet
```
核心語錄：「The frozen plan is a contract on the OBSERVABLE OUTCOME, NOT on how to build it」「inflating the contract is what makes a goal unfinishable」「Grouping, NOT dropping, is how you fit the cap」。plan 寫到 `docs/plans/<slug>.md`（durable artifact，survive compaction 與跨 session）。

**C3. Entry-point launch check**（finish-branch gate 新增，對「上線前零問題」最關鍵）：
unit test 綠不證明 app 能啟動（「a missing import map, a crashing main(), or a bad entry script all pass unit tests and fail the user on first launch」）。按類型斷言主要可觀察值（present and non-empty is INSUFFICIENT）：
- CLI：真指令跑代表性輸入，斷言輸出內容
- Server：boot + 打一個 endpoint，斷言 response body 合理（不只 HTTP 200）
- Library：從 fresh consumer import，斷言真實呼叫的回傳值
- 前端頁面：Playwright 載入，斷言零 page error、畫面實質填滿（painted fraction，不是 >0 pixels）、驅動一個輸入產生可見變化、存 screenshot
跑兩次要求一致（不一致 = app 缺陷要修，不是挑好的那次）。環境跑不了時誠實降級：capture 那個失敗，回退到 static/structural check + unit tests；「Synthetic stand-ins for launch evidence are worse than the honest fallback」。

**C4. Strategist 升級階段**（soul rule 13 的機械化）：
review→fix 連續 2–3 輪失敗後，強制派一個 fresh-context subagent，prompt 近乎照抄 `goal_strategist_prompt.md`：從 diff + findings 歷史診斷結構性根因（常見三型：tangled unit 無法隔離測試、test theater、子系統設計與目標相沖）、建議一個小步驟化的重構、「Change the HOW, never the WHAT」（禁改 spec 與驗收條款）、「grep for the signal, don't dump them whole」。

**C5. 小任務比例閥**（本地缺口：gate 5 只有 trivial/non-trivial 二分）：
diff < ~30 行且 focused test 綠 → 跳過 reviewer subagent，內聯跑 launch check + diff 自審；更大或跨檔 → 完整 dual review。ceremony 隨 stakes 縮放的具體數字化。

**C6. Plugin CI 加 prompt 尺寸回歸測試**（grok 對每個 prompt 模板都有 <N 字元的 unit test）：
digest、hooks 注入文字、SKILL.md frontmatter description 超過字數預算就 fail。防注入內容隨版本膨脹（metaskill 全文注入已是本地最大固定 token 成本，考慮改 digest+pointer 模式，向 session-start-inject-dev-discipline 看齊）。

### D. 新 Skills（P2）

**D1. check-work port**（最高價值單一 skill）：
- 外圈：派 verifier subagent → 解析 `VERDICT: PASS|FAIL` → FAIL 就修再驗，上限 3 輪；缺 verdict 視為 FAIL
- VERIFIER PROMPT 近乎照抄：Phase A trace review（重建使用者全部要求含 mid-session 修正、逐項核對「說要做但沒做」「可以自己做卻丟回給使用者」、「Do not trust the conversation's claims — verify them」）+ Phase B code review（collect full diff、四準則 CORRECTNESS/ADEQUACY/EXCESS/EDGE CASES、跑 build+tests+linters、鼓勵自寫探測、repo 規則違反 = FAIL 但「If they state no review-relevant rules, do not invent violations」）
- 移植關鍵差異：grok 的 verifier 繼承整個 session transcript 再被指示不信任它；Claude Code subagent 是 fresh context，必須把 session trace 摘要（要求清單、聲稱的動作與結果）注入 prompt，否則 Phase A 跑不了
- verifier 跑在 worktree 或限定 scratchpad，重現「你的探測不會弄髒被審的 diff」保證
- description 加 `[checking my work]` 前綴慣例，讓 SubagentStart/Stop hook 可單獨計量驗證成本

**D2. best-of-n port**（限高風險/明確要求）：
N 個 general-purpose subagent 各進 worktree 平行實作 → 比較表（Correctness > Code Quality > Safety，scope creep 扣分）→ `WINNER: <n>` sentinel → 套用贏家後接 dev-discipline dual review。移植時修掉原版兩個弱點：給每個 candidate 不同取向指令（minimal-diff / restructuring / ...）避免收斂同解；description 明定只在明確要求或高風險歧義任務觸發（原版無 gate，是 token 乘數）。

**D3. session-handoff skill**（B4 的 9 sections 做成可呼叫 skill）。

**D4. 文件索引模式**（來源：help skill）：任何超過常駐 context 的參考文集（docs/、evals/、runbook）建一個 30 行索引 skill：檔名 + 一行摘要 + 「read only the matched file(s)」。progressive disclosure 的標準形。

### E. Subagent 派遣規約（Workflow/Agent 工具的使用紀律，P1）

來源：`xai-grok-subagent-resolution/context.rs`（verified）：
1. **任務指令永遠放 prompt 最後一段**（recency attention；grok 把 task 放在 background 之後的位置 [2]）
2. **不轉發 harness 噪音**：禁貼 system-reminder、git status、目錄樹、skill 全文、整檔內容進 subagent prompt；給路徑與行號讓它自己讀（「These blocks are re-injected by the child session's system prompt builder, so including them is pure duplication」）
3. 背景摘要：最近 2–3 turn 重點 + 已用工具/已讀檔案清單；工具輸出只給 <200 字預覽
4. **I/O 合約**：每個自訂 agent 定義寫明 Expects（required inputs）/ Produces（輸出檔路徑）；派遣前對照補齊，交付物寫到約定路徑，最後一句回報路徑；stage 之間傳檔案路徑，不重新敘述（「chain subagents through files, never re-derive」）
5. **Role→model 對照**：explore/summarize/機械轉換 → haiku 級；review/implement → 強模型；cheap path 不可用時 skip 該 nicety，不升級成貴模型付全價
6. reviewer/explorer 一律唯讀工具集；capability 由 agent 定義層決定，prompt 層不得放寬
7. 反派遣準則：「context-setup cost exceeds the parallelism benefit」就內聯做（與 dev-discipline gate 4 一致，補上這句判準）
8. 第二輪同性質工作（修 findings、重跑失敗實作）優先 resume 原 agent；性質變了才開新的
9. 中途補指示：一則訊息一個指示、verbatim、不合併，讓 agent 自行權衡先完成當前步驟
10. 訂閱式檢查：SubagentStart hook 記 `git rev-parse HEAD`，SubagentStop diff 之，取得 subagent 實際改動的 ground truth（零 token）

### F. 記憶體 hygiene（P2）

- session-derived 記憶一律帶日期；curated 規則不衰減、session 觀察會過期（grok：7 天半衰期、staleness note 遞增）
- consolidation gates：≥3 個新 session note 且 ≥4h 才跑一次 LLM 整併（merge、矛盾以新事實為準、相對日期絕對化、丟棄 greetings/Next steps/工具噪音、NO_REPLY 逃生口、輸出無 header 即拒收）——可做成 /schedule 月度 routine，現有 memory-lint 已覆蓋 deterministic 半邊
- 「Omit entirely rather than point at wrong names」：不確定的工具名/路徑寧可省略，別寫進記憶
- 記憶檔內禁存活性指令標籤（`<system-reminder>`、「IMPORTANT: you must...」），未來 session 會照做——加進 fable-soul Maintain checklist

---

## 三、小任務 vs 大任務雙路徑（目標映射）

**小任務**（明顯 bug fix、循慣例功能、rename）：
1. A5 負面清單 → 不進 plan mode，直接動手
2. 內聯實作 + focused test（測試範圍階梯：最窄先跑）
3. C5 比例閥：diff <30 行 → 免 reviewer subagent，內聯 Phase-B-lite + launch check
4. 收尾 ≤80 字
品質保底由零 token 的機械層扛：NO TEST THEATER 規則、Stop hook（測試+前端證據）、secret guard、doom-loop hook。ceremony ≈ 0。

**大任務**（架構歧義、多模組）：
1. C2 plan 合約（3–5 gating criteria、Non-goals、verification plan）寫入 `docs/plans/`，一次規劃全程受益
2. checklist 驅動實作；邊做邊驗（VERIFY AS YOU GO）；證據隨手存 scratch
3. C1 dual reviewers：audit-don't-author（省 reviewer 重跑全套的 token）、PRIOR_GAPS（每輪只審 delta）、3 輪上限、identical findings 即停
4. 卡關 2 輪 → C4 strategist 換層診斷
5. C3 launch check 雙跑 + 前端 screenshot
6. 收尾 ≤80 字 + PR body
token 控制點：plan 一次凍結（不重談）、reviewer 稽核不重建、findings 收斂機制、機械角色用 haiku、subagent 派遣規約（E）砍掉重複 context。

---

## 四、明確不移植（避免浪費工夫）

| 機制 | 原因 |
|---|---|
| Compaction 引擎、tail-keep/chunked 模式 | Claude Code 有自己的 compaction；只借 prompt 與原則 |
| Rewind/checkpoint/hunk-tracker 引擎 | /rewind、git 已覆蓋；只借「別讓 agent 手工重建舊狀態」規則 |
| Kernel sandbox（Seatbelt/Landlock/bwrap） | 只借 permissions.deny 補強 |
| ACP/WebSocket、TUI、prompt queue、HTTP hooks | 傳輸層/runtime 專屬 |
| SQLite journal、fast-worktree pooling、codebase-graph 索引 | 需常駐 daemon；LSP + EnterWorktree + claude-mem 已覆蓋 |
| SubagentBundle 打包 | plugin marketplace 已覆蓋（version-bump 教訓已在 MEMORY.md） |
| 記憶體 FTS5+vector 引擎 | claude-mem 已覆蓋；只借 hygiene 規則 |

---

## 五、優先順序

**P0（純文字，立即做，影響最大）**：A1–A6、C1（reviewer prompt 部分）、C2、C3、C5
**P1（hook 工程，一次投資長期零 token 回報）**：B1–B6、C4、C6、E 全部
**P2（新 skill 與長期習慣）**：D1–D4、F

## 六、落地狀態（2026-07-18 更新）

- **P0 全數落地**（plugin 2.2.0，commit 2de8d8d）：A1–A6、C1、C2、C3、C5，外加提前拉入的 C4（strategist 一行）與 C6（digest 尺寸回歸測試）。
- **P1 落地**（plugin 2.3.0 ＋ 四個 user-global hooks）：B1（stop-verification-gate.py）、B2（post-tool-observer.py doom-loop）、B3 核心（bash-policy-guard.py ＋ permissions.deny 的 .env 與 *.pem 兩條，.pem 出自本報告 B3 建議）、B5（HOOK-STANDARDS.md）、B6 logger 半邊、E-1..8 進 dev-discipline gate 4、E-9 一行、E-10（subagent-git-ledger.py）。
- **B4 修正**：實查官方文件確認 PreCompact 的 stdout 會被 harness 忽略，注入式 PreCompact hook 不可行；改以 CLAUDE.md compaction 習慣規則 ＋ 既有 SessionStart(compact) digest 再注入承接。限制記錄於 HOOK-STANDARDS.md。
- **明確延後（原因）**：B3 的 cat 巨檔警告（需 stat 目標檔且誤報面大，待設計好 size 判準再上，先由「大輸出導檔」CLAUDE.md 規則承接）；B6 的 eval token ledger（等下一次 eval 迭代時直接改 evals/run_*.py 記 usage JSON，避免無執行路徑的死程式碼）。
- **P2 落地**（user-global skills ＋ 本 repo docs）：
  - D1 `~/.claude/skills/check-work/`（trace 注入、VERDICT fail-closed、3 輪上限、比例閥、Phase B 含 build/tests/linters 與 scratchpad 限定的自寫探測）；D2 `~/.claude/skills/best-of-n/`（diversity 指令、明確請求才觸發、贏家接 dev-discipline review）；D3 `~/.claude/skills/session-handoff/`（9 段結構；已實跑產出 docs/handoffs/2026-07-18-grok-borrowings.md）。三者 validate_skill 通過且 harness 熱載入確認。
  - D4 `docs/INDEX.md` ＋ 進入點 `CLAUDE.md`（repo 級，每 session 載入，指向 index）。
  - F(a) 活性指令標籤禁令：三處落地——session-handoff skill 規則、`~/.claude/hooks/memory-lint.sh` deterministic 檢查（反引號提及豁免；正反向驗證過）、fable-soul `references/maintenance.md` 新增 Memory Hygiene 節（sync_soul.py 已同步 codex mirror）。
  - F(b) 已覆蓋／延後：date 慣例與 >90d age 檢查由既有 memory-lint 承接（already covered）；LLM 合併式 consolidation routine **延後**——現行 weekly reflection 已回報 contradictions/near-duplicates，等其報告出現值得合併的量再上 merge 版，避免為空需求建 routine。

預期效益對照目標：
- 品質：C1（收斂的 adversarial review）+ C3（launch check 補前端盲點）+ A2（測試誠實性）直接對應「零已知問題才上線」
- token：E（subagent 規約）與 B3（規則出 context 進 hook）是最大節流；A1 的 anti-ratchet 砍掉 review 無限迴圈；C5 讓小任務近零開銷
- 時間：A4/B2（不重跑必敗的事）、A5（不 plan 不需要 plan 的事）、平行 review + audit-not-rebuild
