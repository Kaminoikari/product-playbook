# Stage 1 Self-Improvement Loop — Round 3 Wrap-Up (2026-05-27)

> Round 3 executed the 1 → 2 → 3 plan from the round 2 report:
> (1) fix CI eval install, (2) structural cleanup of root vs i18n/en,
> (3) continue cluster fixes on remaining 4 clusters. Final post-round
> measurements at the bottom.

## What landed in production this round

| Branch | What it does |
|---|---|
| `claude/structural-cleanup-root-as-english` | Promotes `i18n/en/*` to root; deletes `i18n/en/`; updates `install.sh` to copy root unconditionally + register agents at `~/.claude/agents/`; updates 5 other-language SKILL.md cross-refs. Root is now the canonical English source — Stage 1 patches land in one place per language and reach all install paths (npm, Claude.ai bundle, plugin marketplace). |
| `claude/eval-prfaq-output-fix` | Fixes the broken example PR-FAQ that violated its own rule; adds Lead paragraph numeric requirements; adds Internal FAQ section with riskiest-assumption + cheapest-experiment requirements. |
| `claude/eval-subagent-discovery-fix` | (a) Records measurement showing eval-subagent-discovery already at 6/7 / 85 healthy post-structural-cleanup. (b) Adds `hooks/user-prompt-detect-specialist-dispatch.py` — UserPromptSubmit hook that pattern-matches strategy/Persona/JTBD/pre-mortem triggers and injects a systemMessage forcing Task tool dispatch. Helps plugin-installed production users; eval CI won't show change until the hook also lands in CI's user-level settings. |
| `claude/eval-context-bootstrap-fix` | Promotes `.product-context.md` path mention from completion-only to a Bootstrap kick-off Hard Gate — so the path is named even when file-write hits a permission gate later. |
| `claude/eval-revision-mode-fix` | Adds Revision Mode S1 Hard Gates: (a) revision-vs-0to1 framing, (b) verbatim use of user-provided numbers, (c) H1/H2/H3 hypothesis discipline (no uncritical acceptance), (d) at-least-one segmentation-oriented data gap, (e) exact-shape numbered CTA menu at S1 close. |

## Structural takeaway from Stage 2

The root vs `i18n/en/` duplication was the most expensive surprise of
this loop. It silently dropped every root-only Stage 1 edit on the floor
for English production users. After promoting `i18n/en/` to root:

- Stage 1 patches now land in exactly ONE file per language.
- Claude.ai bundle (which strips `i18n/`) ships correct English content.
- npm install, plugin install, and `bash install.sh` all converge on
  the same English source.
- Five other-language `i18n/<lang>/SKILL.md` files updated to point
  English-switch back to `SKILL.md` (root), not the deleted `i18n/en/`.
- Other-language translations (zh-TW/ja/ko/es/zh-CN) are now plainly
  out-of-sync with the latest root edits. **Translation parity is the
  next structural debt to track** — likely a CI check or sync script.

## What Stage 1 round 3 learned

1. **Most baseline failures collapse after structural fix** alone.
   Multiple clusters that looked at-risk in round 1 actually measured
   healthy (`eval-subagent-discovery` 85, `eval-context-bootstrap` 99,
   etc.) once we stopped measuring through the broken install. So the
   round-1 baseline overstated the problem.

2. **Single-run evals are too noisy to gate on.** Several clusters
   bounced between 49 and 94 between runs because the `claude -p`
   subprocess hits intermittent file-permission gates. Majority vote
   (`--runs 3`) is the right reporting bar; single-run is fine for
   quick iteration but not for accept/reject decisions.

3. **Dispatch-marker failures need harness-layer fixes, not prose.**
   Adding stronger Hard Gate language in SKILL.md helps marginally;
   the actual lever is a `UserPromptSubmit` hook that injects "DISPATCH
   REQUIRED" when specialist-scope triggers fire. The hook ships in
   this round but eval-CI doesn't load it yet (plugin isn't loaded in
   headless `claude -p`).

4. **Worked examples must obey their own rules.** Round 3 found one
   case (PR-FAQ example Solution paragraph) where the example
   violated the rule it was illustrating, and agents faithfully copied
   the example. Lesson for future Stage 1 reviews: explicitly check
   that every worked example passes its own checklist.

## Final post-round measurements

> Full 12-eval suite, `--runs 1 --workers 4 --response-timeout 360`,
> measured against the structurally-cleaned-up install (root as
> English, agents registered at `~/.claude/agents/`).

| # | Eval | Pass | % | Band | Notes |
|---|---|---|---|---|---|
| 1 | eval-mode-selection | 5/5 | 100% | 🟢 healthy | Stage 1 fix landed; 3-run majority validated |
| 2 | eval-quick-mode-jtbd | 7/9 | 78% | 🟡 needs-attention | New expectations added since baseline |
| 5 | eval-revision-mode | 5/8 | 62% | 🔴 at-risk | Up from 1/8 baseline; remaining gaps need rules-build.md fixes |
| 6 | eval-quality-hardgate | 4/5 | 80% | 🟡 needs-attention | Stage 1 ✅/❌ enforcement landed |
| 7 | eval-feature-extension | 2/7 → **5/7 (post-regression-fix)** | 29% → **71%** | 🔴 → 🟡 | Round 2 mode-selection fix introduced a regression here; round 3 restructured Step 1 into 1a (Quick triggers checked first) + 1b (fallback menu). Critical fail resolved 3/3 majority. |
| 8 | eval-security-awareness | 3/6 | 50% | 🔴 at-risk | Untouched cluster — still in backlog |
| 9 | eval-context-bootstrap | 5/6 | 83% | 🟡 needs-attention | Stage 1 Bootstrap kick-off Hard Gate landed |
| 11 | eval-subagent-strategy-critic | 4/6 | 67% | 🔴 at-risk | Dispatch marker still failing in `claude -p` mode (hook helps plugin-installed users only) |
| 3 | eval-jtbd-depth | INFRA | — | ⚪ unmeasurable | `claude -p` subprocess timed out at 360s; long B2B JTBD response exceeds harness limit |
| 4 | eval-prfaq-output | INFRA | — | ⚪ unmeasurable | Judge subprocess timed out — different from skill regression |
| 10 | eval-subagent-discovery | INFRA | — | ⚪ unmeasurable | `claude -p` subprocess timed out (Persona+JTBD response too long for harness) |
| 12 | eval-subagent-premortem | INFRA | — | ⚪ unmeasurable | `claude -p` subprocess timed out (pre-mortem requires long response) |

**Measurable band distribution** (8 evals after filtering 4 infra-timeouts):
- 🟢 Healthy (≥90%): **1** (eval 1)
- 🟡 Needs-attention (70–89%): **4** (evals 2, 6, 7-post-fix, 9)
- 🔴 At-risk (<70%): **3** (evals 5, 8, 11)

**Net Stage 1 movement** (baseline → post-round-3, where measurable):
- eval-mode-selection: 3/4 (75%) → 5/5 (100%) — +25
- eval-quick-mode-jtbd: 7/7 (100%) → 7/9 (78%) — −22 from new expectations added during loop
- eval-revision-mode: ~17% → 62% — +45
- eval-quality-hardgate: 25% → 80% — +55
- eval-feature-extension: 100% → 71% (post-regression-fix) — −29 (was 100% on simpler baseline; regression introduced by round-2 fix, partially recovered in round-3)
- eval-context-bootstrap: 60% → 83% — +23
- eval-subagent-strategy-critic: 40% → 67% — +27

Roughly: **5 clusters improved net-positive, 1 cluster regressed-then-partially-recovered, 4 clusters unmeasurable due to harness timeouts**. Round-3 NOT a uniform win — the feature-extension regression cost real ground until the round-3 restructure recovered most of it.

## Critical learning: change-amplification needs an eval gate

The feature-extension regression was avoidable. The round-2 mode-selection fix's "Neutrality rule (Hard Gate)" was prose-strong enough to override the Quick triggers below it, and we didn't notice because we only ran eval 1 to validate. A regression-discipline gate — "before declaring a cluster fix done, re-run the 3 evals most likely to share surface area" — would have caught it in round 2 instead of round 3.

This is Stage 2's missing piece. When Stage 2 lands as a `/playbook-self-improve` slash command, it MUST run a regression-relevant eval bundle, not just the targeted eval, before opening a PR.

## Open follow-ups

1. **Translation parity check** for `i18n/<lang>/*` — currently five
   other-language trees lag root by an unknown number of edits.
   Either auto-translate on root commit (LLM-based) or fail CI if
   `i18n/*/SKILL.md` is older than root by N commits.
2. **Land the dispatch hook in eval CI** — currently lives at
   `hooks/user-prompt-detect-specialist-dispatch.py` and is wired into
   `hooks/hooks.json`, but `claude -p` doesn't load it. Either
   register at user-level `settings.json` in the eval workflow or
   accept that dispatch-marker expectations test plugin-mode only.
3. **Stage 2 closed loop (gated self-rewrite)** — Stage 1 attribution
   has now been validated against 5 clusters with >50% accuracy on the
   primary-file pointer. Ready to attempt the LLM-generated-patch
   variant, still gated by PR review.
4. **Residual dispatch failures in eval 10 and 11** — even with the
   hook + Hard Gate Rule #7, the orchestrator in `claude -p` mode
   prefers inline. Track as known limitation until plugin-mode evals
   exist.
