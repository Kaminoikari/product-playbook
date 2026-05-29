## Behavioral Eval Results

**Score:** 0/100 🔴 `at-risk`

- Passed: **69 / 82** expectations
- Critical failures: **5** (−15 each)
- Warning failures: **6** (−5 each)
- Info failures: **2** (−1 each)

### Bands
- 🟢 `healthy` ≥ 90
- 🟡 `needs-attention` ≥ 70
- 🔴 `at-risk` < 70

### Failed expectations
- 🔵 **[1] eval-mode-selection** — Responds in English
- 🔴 **[1] eval-mode-selection** — Response presents modes as a clear selection menu (numbered options or table) and lists at least the six modes Quick, Full, Revision, Custom, Build, and Feature
- 🟡 **[1] eval-mode-selection** — This turn only asks about mode selection, does not simultaneously ask about product type or completeness level (three-step progressive rule)
- 🔴 **[8] eval-security-awareness** — Developer handoff package includes a security-related section covering at least 4 of: authentication/authorization, input validation, CORS, CSP, Rate Limiting —
- 🔴 **[8] eval-security-awareness** — TASKS.md or the task list includes security-related tasks (not just a vague description buried in the last phase)
- 🟡 **[8] eval-security-awareness** — Handoff includes an actual .gitignore file body (or explicit file content block) with concrete entries for .env, *.pem / *.key, and platform-specific credential
- 🟡 **[8] eval-security-awareness** — Raises security considerations specific to social platforms (at least 1 of: XSS protection, user-uploaded content filtering, real-time message encryption)
- 🟡 **[8] eval-security-awareness** — At least one security task lists concrete numeric or configuration values (e.g., password hashing parameters like argon2id memoryCost ≥ 19456, login rate limit 
- 🔵 **[9] eval-context-bootstrap** — Mentions that product context will be saved for future use AND references the persistence file path (.product-context.md) — a single throwaway mention of either
- 🟡 **[9] eval-context-bootstrap** — Bootstrap is sequenced as Step 0 BEFORE feature extension S1 (not interleaved with S1) — the response clearly shows Bootstrap → S1, not Bootstrap mid-S1
- 🔴 **[12] eval-subagent-premortem** — Produces a substantial set of failure scenarios, targeting 15 or more, with at least 2 scenarios in each of the five categories
- 🔴 **[12] eval-subagent-premortem** — Coverage spans all five failure categories: product/UX, market/demand, team/execution, operational/infrastructure, and external/environment
- 🟡 **[12] eval-subagent-premortem** — Each failure scenario has a leading indicator that would warn the team before the failure is irreversible — a concrete signal with a threshold and a detection t