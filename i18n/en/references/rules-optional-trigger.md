# 🔵 Optional Step Trigger Rules

> Authoritative source for Optional step triggers and the Phase Decision Point format. Loaded by Full / Revision / Custom mode rule files.

This file centralizes the trigger conditions for Optional steps so each mode rule file does not duplicate them.

---

## 1. Core vs Optional Definitions

- **Core**: Always executed. Cannot be skipped without explicit user override.
- **Optional**: Executed only when at least one trigger condition is satisfied. The user may always force-include or force-skip.

---

## 2. Persona-Journey Bundling Rule (Global)

**Journey Map is the natural extension of Persona: Persona defines Who, Journey Map describes the journey Who experiences. After completing the Persona step, Journey Map is included by DEFAULT, and only skipped when the situation is genuinely too simple to map.**

> ⚠️ This rule corrects an earlier mistaken assumption that "0-to-1 doesn't need Journey Map." The opposite is true — Teresa Torres (Continuous Discovery), Indi Young (Mental Models), and the Amazon Working Backwards process all treat Journey Map as essential during 0-to-1 because it shapes how the new experience is designed. The relevant variable is **whether the user's Job spans multiple stages**, not whether the product already exists.

### Skip conditions (default ON; skip only if any one of these holds)

1. **Single interaction point** — the Job is solved by a single API call, single button, pure backend service, or pure config tool (no multi-stage flow exists)
2. **Flow is only 1–2 steps** — the entire user flow is so short that a Journey Map degenerates into a list with no meaningful stage transitions
3. **User explicitly requests skip** — e.g., "skip Journey Map", "我不需要 Journey Map"

### Behavior when skipping

Surface the decision to the user, do not silently skip:

> "Persona is complete. Based on the current context ([single interaction point / flow has only N steps]), Journey Map is being skipped. You can add it back any time by replying 'add journey'."

### Behavior when triggering (default)

Render a brief evaluation note before entering the Journey Map step, citing **why** it is needed:

> "Persona is complete. The Job spans [N] stages ([stage A → stage B → ...]) — proceeding to User Journey Map. Reply '-S3' to skip if you don't need it."

---

## 3. Optional Triggers — Full Mode

| Step | Framework | Default | Logic |
|------|-----------|---------|-------|
| S3 | User Journey Map | **ON** | See Persona-Journey rule above (Section 2). Skip only when single interaction point / flow ≤2 steps / user explicitly requests skip |
| S6 | April Dunford Positioning | OFF | Trigger when: (a) New product launch OR (b) Repositioning OR (c) Audience includes Sales/BD/Marketing |
| S11 | PMF + GTM + Business Model + Hypothesis Validation Plan | OFF | Trigger when: (a) Product is launching to market OR (b) Audience is Executives/Data Scientists OR (c) User explicitly asked for a validation plan |

---

## 4. Optional Triggers — Revision Mode

| Step | Framework | Trigger (any one satisfies) |
|------|-----------|------------------------------|
| S4 | Positioning Re-assessment | User mentions "positioning drift" / "market changed" OR audience includes Sales/Marketing |
| S6 | Pre-mortem | (a) Change scope ≥30% of existing functionality OR (b) Touches payments/permissions/data migration |

---

## 5. Phase Decision Point Output Format

**Before entering each Phase that contains an Optional step, the AI MUST output a Phase Decision Point block that lists which Core/Optional steps will run and why.**

### Required format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔀 Phase [N] Step Decision

✅ Core (always run): S[a], S[b]
🔵 Optional evaluation:
  • S[x] [Framework name] (Default ON):  [PROCEED / SKIP] — [reason]
  • S[y] [Framework name] (Default OFF): [TRIGGER / SKIP] — [reason]

→ This phase will execute [N] step(s)
(Reply "+S[x]" to force-include, "-S[y]" to force-skip, or just continue)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

For a Default-ON step (e.g., S3 Journey Map), use **PROCEED** when conditions hold and **SKIP** when a skip condition fires.
For a Default-OFF step (e.g., S6 Positioning, S11 PMF/GTM), use **TRIGGER** when conditions are met and **SKIP** otherwise.

### When to render

- Render once at the start of each Phase that contains at least one Optional step
- Phases with only Core steps do NOT require a decision point (proceed directly)
- After rendering, wait for user response. A non-override response (e.g., "ok", "continue", or substantive content) means "accept AI's decision"

### User override commands

| User input | Behavior |
|------------|----------|
| `+S[x]` or "add S[x]" | Force-include the previously skipped Optional step |
| `-S[y]` or "skip S[y]" | Force-skip the previously triggered Optional step |
| Substantive content / "continue" / Enter | Accept AI's evaluation, proceed |

---

## 6. Custom Mode — Persona-Journey Conditional Insert

Custom Mode presets (Lean / Standard / Comprehensive) have fixed step sequences, but the Persona-Journey bundling rule still applies to any preset that contains a Persona step.

| Preset | Default behavior | Behavior after Persona step |
|--------|------------------|----------------------------|
| **Lean** | No Persona step | N/A |
| **Standard** | 8 fixed steps, S1 = Persona | After S1, AI runs the Persona-Journey evaluation per Section 2. If skip conditions do NOT hold, AI proactively inserts Journey Map as **S1.5 (becomes a 9-step run)** with the user able to reply `-journey` to revert. If skip conditions hold, silently skip and disclose at final output (Section 7). |
| **Comprehensive** | 11 fixed steps, S2 = Persona, S3 = Journey Map (already included) | AI may surface a brief "skip available" note: "Journey Map is included by default. Reply `-S3` if your situation is too simple to map." Otherwise proceed normally. |

This keeps Lean/Standard users from being interrupted when the situation is genuinely simple, while ensuring users who *would* benefit from Journey Map are not silently denied it.

---

## 7. Final Output Disclosure

When the mode completes, the final Product Spec Summary MUST list which Optional steps were skipped and offer a one-command path to add them back, e.g.:

> "Optional steps skipped this run: S6 (Positioning), S11 (PMF/GTM). Reply 'add S6' or 'add S11' to fill them in."
