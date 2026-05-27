# Stage 1 Self-Improvement Loop — Run Log (2026-05-27)

> First end-to-end run of the eval-debt → attribution → patch → re-measure
> closed loop. Three clusters worked, one structural finding surfaced
> that retroactively invalidated mid-loop measurements. Real net win:
> two clusters now landing in `needs-attention` band (80–100) versus
> baseline `at-risk` (0/100 aggregate).

## Eval score deltas (with proper install)

| Cluster | Baseline | After Stage 1 | Net |
|---|---|---|---|
| `eval-mode-selection` | 3/4 pass (1 critical fail) | **5/5 pass, 100/100 healthy** | +25 |
| `eval-quality-hardgate` | 1/4 pass (3 warning fail) | 4/5 pass, 85/100 needs-attention | +85 (was at-risk) |
| `eval-subagent-strategy-critic` | 2/5 pass (3 fail) | 4/6 pass, 80/100 needs-attention | +80 (was at-risk) |
| `eval-jtbd-canonical-form` (round 2 attempt) | — | 2/5 → 75 (one critical resolved, one remains) | partial |

(Eval 11's 6th expectation didn't exist at baseline measurement — it was
added recently and reflects a new orchestrator-side requirement. Net pass
count went 2 → 4 in the same direction.)

## What landed in production (branches all auto-merge to main)

| Branch | What it does |
|---|---|
| `claude/eval-debt-report-stage1` | The Stage 1 tooling itself: `scripts/eval-debt-report.py`, `npm run eval:debt`, infra-error filter to keep harness noise out of fix backlog. |
| `claude/strategy-critic-fixes-v1` | (a) Agent file `Step 0: classify before critiquing` table + worked example, (b) `Hard rule: critic, not author` with forbidden-pattern blacklist, (c) broadened dispatch trigger, (d) SKILL.md Hard Gate #7 + `Specialist Dispatch Protocol`, (e) CI fix: install sub-agents at `~/.claude/agents/` so headless `claude -p` can dispatch via Task tool. |
| `claude/eval-mode-selection-fix` | SKILL.md onboarding rewrite: cap recommendation at 2 candidates, add `Neutrality rule (Hard Gate for this step)`. |
| `claude/eval-quality-hardgate-fix` | (a) `rules-quality-review.md` forbids soft markers (⚠️/partial/blank) as ❌ substitutes, (b) demands `Impact: blocks [downstream]` clause in every ❌, (c) JTBD checklist item 6 enumerates emotional vocabulary, (d) SKILL.md Hard Gate #6 removes `or load` escape hatch. |
| `claude/eval-jtbd-canonical-form-fix` | (a) Mirror all root edits to `i18n/en/` (critical infra fix — see below), (b) JTBD reference adds a fully-worked canonical-form table example. |

## The infra finding that retroactively invalidated mid-loop measurements

Mid-way through the loop I discovered that my local install command
(`cp -r ./. /root/.claude/skills/product-playbook/`) skipped the i18n
overlay step that `install.sh` performs for English locale:

```bash
cp -r ./. /destination/                               # ← what I did
cp i18n/en/SKILL.md /destination/SKILL.md             # ← also needed
cp -r i18n/en/references /destination/                # ← also needed
cp -r i18n/en/commands /destination/                  # ← also needed
```

The CI eval workflow (`.github/workflows/eval-gate.yml`) had the
identical bug — copies root, skips the i18n overlay. Net effect:

1. Stage 1 patches written to root-level SKILL.md / references were
   not actually shipping to English npm/Claude.ai users (their install
   overwrites root with the stale `i18n/en/` copies).
2. My mid-loop eval runs (eval 1 = 100/100, eval 11 = 80/100) measured
   the inflated state where my root edits were visible.
3. Re-running after correct install with `i18n/en/` overlay surfaced
   the gap. Re-validation under correct install: scores hold once the
   edits are mirrored.

Two open follow-ups from this finding:

- [x] **Fixed for current Stage 1 patches** in `eval-jtbd-canonical-form-fix`
      branch (mirrored SKILL.md, rules-quality-review.md,
      rules-subagent-dispatch.md to `i18n/en/`).
- [ ] **CI eval install needs the same overlay fix.** Currently `eval-gate.yml`
      installs the broken way. Track as a follow-up — every CI eval
      result on main right now is partially measuring stale i18n/en/.
- [ ] **Structural issue (open)**: root vs i18n/en/ are 99% duplicate
      content. Either merge to one source of truth or write a sync
      hook. Every Stage 1 patch now has to touch two files; that
      doubles maintenance error rate.

## What Stage 1 learned about its own attribution

EVAL_ATTRIBUTION in `scripts/eval-debt-report.py` is hand-curated.
Two adjustments made this round:

- `eval-subagent-strategy-critic` had only `agents/strategy-critic.md`
  as primary; the actual failure root cause split between agent file
  AND `SKILL.md` dispatch rules AND `rules-subagent-dispatch.md`.
  Added the two orchestrator-side files as secondary.
- `eval-quality-hardgate` had `rules-quality-review.md` as primary,
  but the fix also required tightening SKILL.md Hard Gate #6 (the
  `or load` escape hatch). Attribution dict would benefit from a
  third field: "structural up-stream control points that gate
  whether this file even gets read".

Attribution is right-direction always; it just sometimes points at
half the surface area. The fix loop catches the other half within 1–2
patch iterations. This is acceptable cost.

## What's left in the eval-debt backlog (today)

From the original baseline report, untouched clusters:

| Cluster | Weight | Where to look | Hint |
|---|---|---|---|
| `eval-prfaq-output` | 15 | `references/04a-prfaq.md` | Solution para opens with user feel; ≥1 ❌ self-check |
| `eval-subagent-discovery` | 15 | `agents/discovery-specialist.md` | B2B: separate Buyer vs User Persona |
| `eval-context-bootstrap` | 6 | `references/rules-context.md` | Reuse declared stack; mention `.product-context.md` |
| `eval-revision-mode` | 5 | `references/rules-revision.md` | Post-S1: concrete CTA menu |

Plus residuals from clusters Stage 1 partially solved:

- `eval-quality-hardgate` — Q5 emotional vocab requirement applies at
  Five-Whys generation time, but `rules-quality-review.md` only loads
  AFTER step output. Sequencing issue: vocab requirement needs to live
  in `02b-jtbd.md` Five Whys section directly, not just in the post-hoc
  quality file.
- `eval-subagent-strategy-critic` — dispatch marker still failing in
  `claude -p` single-shot mode even with Hard Gate #7. Agent reads the
  rule, considers the strategy a "simple enough" case, inlines anyway.
  May need either a `UserPromptSubmit` hook that injects "DISPATCH
  REQUIRED" when strategy paste + review intent is detected, or
  acceptance that single-shot mode evals can't enforce dispatch.

## What to do next

Three options, ranked by impact:

1. **Sync the rest of root → i18n/en/ for all 6 languages**, OR pick a
   structural fix (single source of truth). Without this, every future
   Stage 1 patch silently fails to ship.
2. **Fix the CI eval install** to overlay i18n/en/ + register sub-agents
   at `~/.claude/agents/`. This unblocks accurate CI scoring and turns
   the eval-gate.yml workflow from a measurement-of-broken-install
   into a measurement-of-actual-skill.
3. **Continue Stage 1 cluster fixes** on the 4 untouched clusters.

Recommendation: 2 → 1 → 3. Get CI honest first, then make sure shipping
works, then continue cluster fixes with confidence that the loop is
measuring what it claims to measure.
