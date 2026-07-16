---
name: dev-discipline
description: Use when implementation work starts on a feature or bug fix: writing or modifying source code, adding tests, or closing out a branch. Covers TDD-first, scope integrity, secret and security hygiene, dual post-implementation review (code reviewer plus spec reviewer), and finish-branch closure. Triggers on "implement", "start coding", "build the feature", "write the code", "fix the bug", "finish the branch", "wrap up the branch", and the same intent in any language ("開始實作", "開發這個功能", "收尾", "実装して").
---

# Dev Discipline

Detect the user's language and reply in it; the protocol below is authored in English.

**Provenance:** this lens governs process, so code changes carry no framework tag. Skip the `— Frameworks:` line on code output; add `dev-discipline` to the provenance line only when the outcome is a document (a review report, a handoff note).

## The six gates

Apply these while implementation is active. Proportional like every lens: no ceremony, no per-step confirmation, no progress theater. Each gate is one judgment applied at the moment it matters.

### 1. TDD first

Write the failing test before the production code. The cycle is red, green, refactor:

1. **Red** — write the smallest test that captures the behavior, run it, and watch it fail for the expected reason. A test that passes immediately proves nothing.
2. **Green** — write the minimal production code that makes the test pass. Run it and confirm green.
3. **Refactor** — clean up with the suite green, keeping behavior fixed.

Every bug fix starts from a failing reproduction test, so the fix has proof and the regression stays covered.

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

After an implementation milestone is complete and tests are green, dispatch two independent reviewers with fresh context, in parallel:

- **Code reviewer** — gets the diff only. Judges the code on its own merits: correctness, bugs, security, error handling, maintainability. A code-review agent or the built-in `/code-review` both qualify.
- **Spec reviewer** — gets the agreed requirements (the task statement, plan, or PRD) plus the diff. Checks that the implementation delivers exactly what was agreed: nothing missing, nothing extra. This is the scope-integrity gate re-applied at review time, by a reader with no stake in the code.

Fresh context matters: the author's context defends the code, a reviewer's context reads it. The two lenses catch different failures: code review finds bugs in what was built, spec review finds gaps between what was built and what was asked. Address confirmed findings from both; report the findings you decided against acting on. Skip the reviews only when the user waives them or the change is trivial (typo, comment, config value).

### 6. Finish the branch

Closing checklist, in order:

1. Full test suite green, run after the last code change, with real output reported. A green run recorded before a later edit proves nothing about the code after it.
2. Review findings resolved, or explicitly deferred with the user's knowledge.
3. Offer the user the close-out choice: **merge** to the base branch, **open a PR**, or **keep the branch**. Never merge or push without the user picking one.

## Deterministic backstops

Two plugin hooks enforce the highest-value gates outside the model's discretion:

- `pre-write-tdd-gate.py` raises a one-line advisory when production code is written and no test referencing it exists anywhere in the repo. Silence it project-wide with a `.product-tdd-waived` marker file.
- `pre-write-secret-guard.py` pauses the write for user confirmation when file content matches a high-confidence credential pattern, or when the target is a `.env` file.

Both follow the plugin's relative-guardrail style: one line, user overrides in one word, never a hard stop.
