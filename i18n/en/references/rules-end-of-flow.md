# 🏁 End-of-Flow Rules

> Loaded when all steps are completed.

## ⛔ End Condition Check

Before producing the final integrated output, the following must be verified:

1. Confirm that all steps in the progress indicator are marked ✅
2. If any steps were skipped (at the user's explicit request), mark them as "⚠️ Skipped" in the final output
3. If any steps are marked ⬜ (not executed), do not proceed to the final output
4. **Security quick check**: If the user will be entering the development phase (generating a dev handoff package), include a security reminder in the final output, and when generating the dev handoff package, automatically read `references/08-security-checklist.md` to produce the corresponding security architecture section

Violations of this rule include: Independently deciding that "the remaining steps are not important" and skipping them, marking incomplete steps as completed, or combining multiple steps into a single output.

## 📦 Product Context Auto-Extraction

After all steps are completed and while producing the final integrated output, read `references/rules-context.md` Section 8 to perform context extraction:

1. **Check whether `.product-context.md` exists**
   - Does not exist → Create a new file
   - Exists → Update per the rules (Identity/Core Strategy overwrite, Decision History append, Architecture merge, Insights merge and deduplicate)

2. **Extract content** (according to the flow type mapping in `rules-context.md` Section 8 table)

3. **Inform the user**: After the final output, display:
   "✅ Product context has been updated in `.product-context.md` — it will be automatically loaded in your next planning session."

4. **Version control reminder** (first creation only):
   "⚠️ We recommend adding `.product-context.md` to `.gitignore` — this file may contain sensitive product strategy information."

## Best Entry Point Analysis (Full Mode only)

```
[Persona Pain Points] → [JTBD Statement] → [OST Opportunity] → [HMW Question]
    → [Positioning (April Dunford)] → [PR-FAQ Validation] → [Solution Selected]
        → [Aha Moment] → [North Star Metric] → [PMF Level Assessment]
```

Analysis points: Most worthwhile problem to solve / Core JTBD / Product positioning / PMF level and next milestone / First action step / Pre-mortem risk alerts

## Final Output by Mode

| Mode | Final Integrated Output |
|------|------------------------|
| ⚡ Feature Extension (Build Mode variant) | Feature development spec: Problem → Selected solution → Impact scope → Execution scope → Risks |
| 🚀 Quick Mode | One-page direction summary: Problem → Solution → Success Definition |
| 📦 Full Mode | Best Entry Point Analysis + Product Spec Summary |
| 🔄 Revision Mode | Revision product spec summary: Before/after comparison + What to change/What not to change + Success metrics |
| ✏️ Custom Mode | Product Spec Summary (unexecuted fields marked "Not Executed") |
| ⚡ Build Mode | Engineer-oriented execution summary |

### Output Language Override

Users can request outputs in a different language than the planning session:
- "Generate the PR-FAQ in Japanese"
- "Output the report in Spanish"
- "Write the PRD in Chinese"

When a language override is requested:
1. Generate the output content in the requested language
2. Keep framework names in English (JTBD, PR-FAQ, North Star, etc.)
3. Return to the planning session's original language after output generation
4. Note: This only affects the output document language, not the reference files or planning flow

## Extended Output Prompt

After completing the final integrated output, proactively ask:

```
"The planning content has been fully integrated! Would you like me to generate any of the following documents?

□ Updated [document type] (incremental update based on your uploaded source document) ← only show this option when a source document was uploaded
□ HTML planning report (suitable for sharing with everyone)
□ PRD engineer delivery package (includes flowchart, DB schema, UI wireframe)
□ PowerPoint presentation (suitable for meeting presentations)
□ Dev handoff package (CLAUDE.md + TASKS.md + TICKETS.md + technical architecture — ready to start development in Claude Code)
□ All of the above

You can also say 'No thanks' to finish, or specify a particular document."
```

**Option display rules**:
- Source document uploaded → "Updated [document type]" listed first with "(recommended)" label
- Target audience is engineers → PRD and dev handoff package listed first
- Target audience is executives/leadership → Presentation listed first
- Target audience is cross-functional → Both HTML report and presentation listed
- Quick Mode → Only ask if a presentation is needed
- Target audience is yourself → Dev handoff package listed first
