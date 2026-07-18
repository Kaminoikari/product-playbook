---
name: dev-discipline
description: Use when implementation work starts on a feature or bug fix: writing or modifying source code, adding tests, or closing out a branch. Covers TDD-first, scope integrity, secret and security hygiene, dual post-implementation review (code reviewer plus spec reviewer), and finish-branch closure. Triggers on "implement", "start coding", "build the feature", "write the code", "fix the bug", "finish the branch", "wrap up the branch", and the same intent in any language ("開始實作", "開發這個功能", "收尾", "実装して").
---

# Dev Discipline

Detect the user's language and reply in it; the protocol below is authored in English.

**Provenance:** this lens governs process, so code changes carry no framework tag. Skip the `— Frameworks:` line on code output; add `dev-discipline` to the provenance line only when the outcome is a document (a review report, a handoff note).

## Right-sizing: small vs large

Decide the track before the first edit; ceremony scales with ambiguity, not with nervousness.

- **Enter plan mode only** when two or more reasonable architectures exist or picking wrong wastes significant rework (session vs JWT auth, Redis vs in-memory cache, WebSocket vs SSE). Do NOT plan for: obvious bug fixes, convention-following features, renames, formatting, test-only changes, or "update the error handling" requests — start working and ask specific questions inline. Research and exploration go to subagents, never to plan mode.
- **Small change** — a single-purpose diff under ~30 lines with a green focused test: skip the reviewer subagents; review the diff inline yourself and run the entry-point launch check from gate 6. The deterministic backstops still apply.
- **Large change** — architectural ambiguity, multi-file, or high-risk surface: write the plan contract below before implementing, then run every gate in full.

## Plan contract — large tasks only

Write the plan to `docs/plans/<slug>.md` before implementing. The plan is a frozen contract on the OBSERVABLE OUTCOME the task asks for, never on how to build it — freezing file names or function signatures lets a reviewer refute correct work for diverging from them. Sections, in order:

```
# Plan: <one-sentence headline>
## Acceptance criteria    3-5 gating, outcome-based criteria; group related behaviors, never silently drop one
## Verification plan      per criterion: the action + the observation that must hold; tag each step gating|evidence
## Non-goals              required — park plausible-but-unrequested scope here so a reviewer sees it was deferred, not forgotten
## Assumed scope          files / modules / deps this touches
## Task checklist         3-8 checkboxes, flipped as you work; guidance, never part of the judged contract
## Deviations             single section, one terse bullet per deviation; never edit the criteria themselves
```

Keep the criteria set small and satisficing — inflating the contract is what makes a task unfinishable. The spec reviewer receives the git diff of the plan file alongside the code diff: a weakened or deleted acceptance criterion is itself a finding.

## The six gates

Apply these while implementation is active. Proportional like every lens: no ceremony, no per-step confirmation, no progress theater. Each gate is one judgment applied at the moment it matters.

### 1. TDD first

Write the failing test before the production code. The cycle is red, green, refactor:

1. **Red** — write the smallest test that captures the behavior, run it, and watch it fail for the expected reason. A test that passes immediately proves nothing.
2. **Green** — write the minimal production code that makes the test pass. Run it and confirm green.
3. **Refactor** — clean up with the suite green, keeping behavior fixed.

Every bug fix starts from a failing reproduction test, so the fix has proof and the regression stays covered.

**No test theater.** A passing test must prove the SHIPPED code works on the real path. Four named cheats, all forbidden: hard-code the expected value, start past the thing under test, re-implement the code under test inside the test, or report success without driving the real entry point. A test that passes while the program is broken is worse than none. The honest line: injecting a fake at an environment boundary — a clock, RNG, network, file, or output sink — to make the unit's real logic observable is honest and standard; faking the unit's OWN logic or its expected output is theater.

While developing, run the narrowest test touching the change first and widen only on green; the full suite has its mandatory run at branch close (gate 6).

Waivers are explicit, never silent. Valid waivers: the user waived TDD for this task, or the change has no testable runtime surface (docs, comments, pure renames, generated files). State the waiver in one line when you use it.

### 2. Scope integrity

Build exactly what was agreed. When you discover an out-of-scope problem, flag it in one line and keep going; never silently fix it, never silently expand the task. When the agreed scope itself turns out to be wrong, say so and let the user decide before widening.

### 3. Security hygiene

- Never hardcode API keys, tokens, or passwords; load them from env vars or a secret manager.
- Never read, print, or commit `.env` files.
- Validate input at every system boundary (API, DB, file system, user input).
- Treat payments, auth, permissions, and data migration as high-risk surfaces: before finishing, check authorization on every new endpoint, injection on every new query, and rollback on every migration.
- No empty catch blocks; handle the error or re-throw it at the boundary.

### 4. Subagent economy

Implement inline by default; every subagent costs a full context of tokens. Reach for subagents only when the task genuinely benefits from parallel independent work, typically research or exploration across several areas whose results you synthesize afterwards. One subagent per implementation task is the anti-pattern to avoid.

### 5. Independent review, two reviewers

After an implementation milestone is complete and tests are green, first save the evidence: write the actual test-run output (and screenshots for frontend work) to a scratch path. Then dispatch two independent reviewers with fresh context, in parallel:

- **Code reviewer** — gets the diff only. Judges the code on its own merits: correctness, bugs, security, error handling, maintainability. A code-review agent or the built-in `/code-review` both qualify.
- **Spec reviewer** — gets the agreed requirements (the task statement, plan, or PRD) plus the diff, and — when a plan contract exists — the git diff of the plan file, so a weakened acceptance criterion surfaces as a finding. Checks that the implementation delivers exactly what was agreed: nothing missing, nothing extra. This is the scope-integrity gate re-applied at review time, by a reader with no stake in the code.

Fresh context matters: the author's context defends the code, a reviewer's context reads it. The two lenses catch different failures: code review finds bugs in what was built, spec review finds gaps between what was built and what was asked.

**Reviewer dispatch contract.** Every reviewer prompt carries these rules, and reviewers get read-only tools plus an instruction to read the repo's convention files (CLAUDE.md, project rules) before judging:

- *Default to refuted when uncertain* — uncertainty about whether a REQUIRED criterion holds means fail; it is never a license to add requirements.
- *Never invent requirements* — inventing requirements beyond the contract is the most common false refute. Items under Non-goals, extra edge cases, additional robustness, and test-construction preferences are not findings.
- *Audit the saved evidence, don't rebuild it* — reviewers read the implementer's committed tests and captured run output, judge them honest vs hacky per the test-theater taxonomy, and do only cheap spot-checks. Missing or insufficient evidence is a finding that names what to produce, never a gap the reviewer fills itself.
- *Verdict sentinel, fail-closed* — every review ends with exactly `VERDICT: PASS` or `VERDICT: FAIL` plus typed findings (kind, path:line, one-line detail). A missing verdict counts as FAIL.
- *Untestable means refactor* — when a test cannot honestly drive the unit, the finding directs refactoring the shipped code into a directly-callable unit, never patching the test around it.

**Convergence control.** Findings from each round are saved; the next round's reviewers get them as prior gaps with the instruction: your primary job is to check each prior gap is genuinely fixed — the bar does not rise between rounds, and fresh nitpicks while the criteria hold are the failure mode that makes reviews never converge. If a round's finding locations are identical to the previous round's, stop iterating and escalate to the user. After two consecutive failed rounds that ARE making progress, dispatch a fresh-context strategist to diagnose the structural root cause (tangled untestable unit, test theater, or a design fighting the goal) and recommend one restructure — it changes the HOW, never the WHAT. Hard cap: three rounds, then report to the user with the open findings.

Address confirmed findings from both reviewers; report the findings you decided against acting on. Skip the reviews only when the user waives them, the change is trivial (typo, comment, config value), or the small-change valve above applies.

### 6. Finish the branch

Closing checklist, in order:

1. Full test suite green, run after the last code change, with real output reported. A green run recorded before a later edit proves nothing about the code after it.
2. **Entry-point launch check** — green unit tests do not prove the deliverable starts: a crashing `main()`, a missing import, or a bad entry script all pass unit tests and fail the user on first launch. Launch the real entry point and assert its PRIMARY observable is CORRECT — present and non-empty is insufficient:
   - CLI → run the real command on representative input; assert the output content.
   - Server → boot it, hit one endpoint; assert the response body is sane, not just a 200.
   - Library → import from a fresh consumer (not its own tests); assert a real call's return value.
   - Frontend → load the page (Playwright); assert zero page errors, the surface is substantially painted, and one driven input produces the expected visible change; capture a screenshot.
   Run it twice and require consistent success — flaky launch output is a defect to fix, never a run to cherry-pick. If the launcher itself cannot run in this environment, capture that failure and fall back honestly to structural checks plus unit tests of the shipped functions; fabricated launch evidence is worse than the honest fallback.
3. Review findings resolved, or explicitly deferred with the user's knowledge.
4. Offer the user the close-out choice: **merge** to the base branch, **open a PR**, or **keep the branch**. Never merge or push without the user picking one.

## Deterministic backstops

Two plugin hooks enforce the highest-value gates outside the model's discretion:

- `pre-write-tdd-gate.py` raises a one-line advisory when production code is written and no test referencing it exists anywhere in the repo. Silence it project-wide with a `.product-tdd-waived` marker file.
- `pre-write-secret-guard.py` pauses the write for user confirmation when file content matches a high-confidence credential pattern, or when the target is a `.env` file.

Both follow the plugin's relative-guardrail style: one line, user overrides in one word, never a hard stop.
