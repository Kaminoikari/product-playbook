# 🔄 Change Propagation Rules

> Loaded when the user modifies a previously completed step.

## 📍 Progress Indicator (must be displayed at every step)

When executing any step, Claude must display a progress bar at the very beginning of the response, in this format:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 [Execution Mode] ｜ Progress S[current step number] / S[total steps]
✅ S1: [Step name] (completed)
✅ S2: [Step name] (completed)
▶️ S3: [Step name] (in progress)
⬜ S4: [Step name] (pending)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

This progress indicator must appear in the following situations:
- When entering a new step
- When the user goes back to a step to make modifications
- When completing a step and prompting the user for confirmation before moving to the next step

## Trigger Methods
- "Go back to Persona," "Go back to JTBD," "Go back to HMW," "Go back to PR-FAQ," or any other step name
- "I want to modify [step name]," "[step name] — I want to change something"
- Directly referencing an already-produced table or content with "change this to..."

## Required Actions After Modification

When any step is modified, Claude **must proactively perform the following checks**:

```
Modified Layer               Affected Downstream (must re-confirm or update)
─────────────────────────────────────────────────────
Persona / JTBD            → HMW, Opportunity Assessment Table, Positioning, PR-FAQ, North Star, Product Spec Summary
HMW / Opportunity Assessment → PR-FAQ, Parallel Solutions, MVP, North Star, Product Spec Summary
Positioning               → PR-FAQ, Product Spec Summary
PR-FAQ / Solutions        → Pre-mortem, GEM/RICE, MVP, Aha Moment, Product Spec Summary
MVP / Not Doing List      → User Story, DB schema (if already generated), Product Spec Summary
North Star / Metrics      → Hypothesis Validation Plan, Product Spec Summary
Product Spec Summary      → HTML Report, PRD (if already generated)
```

### Feature Extension dependency:
```
Feature Extension dependency:
─────────────────────────────────────────────────────
S1 (Problem + Context)  → S2 (Solutions), S3 (Risks), S4 (Execution Scope)
S2 (Selected Solution)  → S3 (Risks), S4 (Execution Scope)
S3 (Risk Assessment)    → S4 (Execution Scope)
```

## Execution Process

1. **Inform the user of the impact scope**: "You modified [step]. This affects [list of downstream steps]. I will update each one."
2. **Confirm or auto-update downstream items**:
   - If the downstream change is minor (wording adjustments) → Update directly and explain what changed
   - If the downstream change is significant (directional shift) → Prompt the user to confirm the new direction before updating
3. **Re-integrate the Product Spec Summary**
4. **If an HTML report or PRD has already been generated**: Re-generate it directly and output a version snapshot:

```
📋 Version Snapshot v[old version] → v[new version]
Modified step: [Step name]
Key content before modification: [1-3 sentences]
Key content after modification: [1-3 sentences]
Downstream updates triggered: [Which steps were also adjusted]
```

## Principles
- No modification happens silently — the impact scope must always be explicitly communicated
- The user has the right to choose "only modify this step, leave downstream as-is for now." Claude must mark which parts are outdated (add a ⚠️ Needs Update label)
- Modification history remains traceable within the conversation
