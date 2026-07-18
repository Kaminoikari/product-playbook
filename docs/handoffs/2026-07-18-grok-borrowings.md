# Session Handoff — grok-build 借鏡研究與 P0/P1/P2 落地（2026-07-18）

## 1. Primary Request and Intent

使用者要求：「請詳讀 grok build 的所有 harness 機制，並且完整列出所有本 plugin、全域 claude MD 或其他跟 harness 相關的 hook、文件、skills 還可以借鏡的地方」。目標原話：「我的目標是最大化功能品質，但同時要能夠最大化利用 token（token 成本越少越好）和最大化縮短時間成本」；品質定義原話：「在確定程式碼可上線前，要把所有問題都排除，沒有任何 but 出現，包括前後端」。研究後使用者依序下令「go」（P0）、「P1請繼續」、「繼續 P2」。

## 2. Key Technical Concepts

- 借鏡總表：`docs/grok-build-harness-borrowings-2026-07-18.md`（180 機制、P0/P1/P2、「六、落地狀態」）
- Reviewer 收斂三原則：default-to-refuted（限 required criteria）、anti-ratchet（bar 不升高＋prior gaps）、anti-invention
- NO TEST THEATER 四型態＋環境邊界 mock 合法性判準
- Plan 合約：outcome-based criteria 3–5 條、Non-goals 必填、plan diff 交 spec reviewer
- Entry-point launch check：按 deliverable 類型斷言主要可觀察值、跑兩次、誠實降級
- Hook 十二條合約：`~/.claude/hooks/HOOK-STANDARDS.md`（fail-open/fail-closed 分流、observe-first、fire cap、kill-switch、--self-test）
- PreCompact stdout 被 harness 忽略（官方文件查證）；post-compaction 再錨定走 SessionStart matcher `compact`

## 3. Files and Code Sections

- Plugin repo（`/Users/charles/product-playbook`，本地 main）：`skills/dev-discipline/SKILL.md`（Right-sizing／Plan contract／六閘門全升級＋gate 4 Dispatch protocol 七條）、`hooks/session-start-inject-dev-discipline.py`（digest 同步、~620 tokens、3000 字元上限測試）、`tests/test_lens_dev_discipline.py`（+18 斷言）、`tests/test_inject_dev_discipline.py`（+4）、`docs/INDEX.md`（新）、`docs/grok-build-harness-borrowings-2026-07-18.md`
- User-global hooks（`~/.claude/hooks/`）：`bash-policy-guard.py`（33 self-test cases）、`post-tool-observer.py`（8）、`stop-verification-gate.py`（18，**observe mode**）、`subagent-git-ledger.py`（4）、`HOOK-STANDARDS.md`、`memory-lint.sh`（新增 live-directive-tags 檢查，反引號提及豁免）
- User-global skills（`~/.claude/skills/`）：`check-work/`、`best-of-n/`、`session-handoff/`（三者 validate_skill OK、harness 已熱載入）
- `~/.claude/settings.json`：permissions.deny 四條（`Read(**/.env)`、`.env.local`、`.env.production`、`*.pem`）；hooks 註冊 PreToolUse(Bash)、PostToolUse(*)、PostToolUseFailure(*)、Stop、SubagentStart/Stop
- `~/.claude/CLAUDE.md`：測試 +3 條、工作流程 +10 條（失敗分類、斷路、plan 分流、敘述附 call、大輸出導檔、單次核准、派遣三行、compaction 前寫狀態）

## 4. Errors and Fixes

- Write tool 寫入原始 NUL bytes（`bash-policy-guard.py` 4 處）→ Python 拒載；byte 級替換為 `\x00` 逸出序列後修復。
- P1 round 1 雙審皆 FAIL：（a）前端證據檢查被 transcript 的 deferred-tool 清單污染成恆真 → 改為只認 `"tool_use"` 行內未跳脫 `"name":"…browser_…"`，以本 session 2.8MB 真實 transcript 驗證回 False；（b）zh-continue-later pattern 誤中「之後再繼續調整參數即可」等完工收尾 → 刪除該 pattern，reviewer 的四個誤報句收進 self-test；（c）違反 HOOK-STANDARDS 第 9 條 → stop gate 改 observe mode 預設。
- `grep -rnothing` 測試案例預期寫錯（bundled flags 含 -r，deny 是對的）→ 改測試不改偵測。
- plugin.json 被 json rewrite 展開 keywords 陣列 → git checkout 還原後改用 sed 單行替換。
- memory-lint 新檢查誤報 `project_lens_refactor_p0.md`（反引號內歷史提及）→ grep 加 `(^|[^\`])` 豁免。

## 5. Problem Solving

已解：P0（A1–A6、C1–C3、C5＋提前的 C4/C6）、P1（B1–B3、B5、B6 logger、E-1..10）、P2（D1–D4、F 指令標籤檢查）全部落地並經雙審收斂（P1 走了 FAIL→修→PASS 兩輪）。開放假設：stop-verification-gate 的誤報率需一週 fire log 實據才能決定升級 block mode；`stopping-here` 英文 pattern 對罕見開頭（"Stopping here would be premature"）會記 telemetry 但不阻擋。

## 6. All User Messages

1. 「請詳讀 grok build 的所有 harness 機制，並且完整列出所有本 plugin、全域 claude MD 或其他跟 harness 相關的 hook、文件、skills 還可以借鏡的地方…（含目標與範例段）」
2. 「請繼續」（workflow 完成通知後）
3. 「go」
4. 「P1請繼續」
5. 「繼續 P2」

## 7. Pending Tasks

- 使用者尚未決定是否 push（兩個 commits 未推送；push main = 觸發 npm publish + GitHub release）。
- stop-gate 一週後審 `~/.claude/logs/stop-gate-fires.jsonl`，決定是否寫 "block" 進 `~/.claude/hooks/stop-gate-mode`。

## 8. Current Work

P2 收尾中：三個 skills 已驗證並熱載入；memory-lint 擴充已雙向驗證；`docs/INDEX.md` 已建。兩個 P2 reviewer subagents 正在背景審查（prompt reviewer 審三份 SKILL.md＋memory-lint diff＋INDEX 正確性；spec reviewer 對照借鏡 doc 二.D／二.F 查缺漏）。已知 spec reviewer 可能會抓到「六、落地狀態」尚未涵蓋 P2（該段目前只寫到 P1），屬預期 finding，審後補。P2 的 repo 變更（docs/INDEX.md、handoffs/、借鏡 doc 六的 P2 更新）尚未 commit。已 commit：`2de8d8d`（P0，2.2.0）、`34c3ba1`（P1，2.3.0），皆在本地 main，未 push。已安裝 plugin 副本 = 2.3.0。

## 9. Optional Next Step

等兩個 P2 reviewer 的 VERDICT 回來，處理 findings（至少補借鏡 doc 六的 P2 狀態），commit docs 變更，然後回報並讓使用者選擇 push 與否。接續點原話：使用者最後指令為「繼續 P2」，前次回報結尾為「要 **push 發布**、**先留在本地**，還是接著做 **P2**」。

— Frameworks: session-handoff
