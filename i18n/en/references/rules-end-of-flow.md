# 🏁 End-of-Flow Rules

> Loaded when all steps are completed.

## ⛔ End Condition Check

Before producing the final integrated output, the following must be verified:

1. Confirm that all steps in the progress indicator are marked ✅
2. If any steps were skipped (at the user's explicit request), mark them as "⚠️ Skipped" in the final output
3. If any steps are marked ⬜ (not executed), do not proceed to the final output
4. **Security quick check**: If the user will be entering the development phase (generating a dev handoff package), include a security reminder in the final output, and when generating the dev handoff package, automatically read `references/08-security-checklist.md` to produce the corresponding security architecture section

Violations of this rule include: Independently deciding that "the remaining steps are not important" and skipping them, marking incomplete steps as completed, or combining multiple steps into a single output.

## 🔍 Decision Consistency Check

Before generating the final integrated output, scan ALL completed steps and verify cross-step consistency:

### Checks by Mode

**🚀 Quick Mode** (3 steps — check 2 cross-references):
1. JTBD ↔ PR-FAQ: Does the PR-FAQ address the same problem as the JTBD statement?
2. PR-FAQ ↔ North Star: Does the North Star measure the outcome the PR-FAQ promises?

**📦 Full Mode** (20 steps — check all 7):
1. Target User — same persona referenced across JTBD, Positioning, PR-FAQ, and North Star?
2. Core Problem / JTBD — PR-FAQ addresses the same problem? MVP solves it?
3. Positioning — reflected in PR-FAQ headline and solution direction?
4. Solution Direction — selected solution matches MVP scope?
5. MVP Scope — consistent with PR-FAQ promises? "Not Doing" items respected?
6. North Star Metric — measures JTBD outcome? Achievable with MVP scope?
7. Pre-mortem Risks — still relevant given final solution and MVP?

**🔄 Revision Mode** (12 steps — check 4):
1. Existing JTBD ↔ Pain Points ↔ Positioning: consistent after re-evaluation?
2. PR-FAQ ↔ MVP Scope: revision scope matches what PR-FAQ describes?
3. North Star ↔ Before/After: metric comparison is logical?
4. Pre-mortem Risks: still relevant for the revised product?

**⚡ Build Mode** (7 steps — check 4):
1. Problem Statement ↔ PR-FAQ: same problem addressed?
2. Solution Direction ↔ MVP Scope: selected solution matches MVP?
3. North Star ↔ MVP: metric achievable with MVP scope?
4. Pre-mortem Risks: still relevant for final solution?

**🔧 Feature Extension Mode** (4 steps — check 3):
1. Problem ↔ Selected Solution: solution directly addresses the stated problem?
2. Solution ↔ Execution Scope: scope correctly implements the selected solution?
3. Risk Assessment: identified risks still relevant for the execution scope?

**✏️ Custom Mode** — only check cross-references between steps the user actually executed. Skip checks for steps that were not part of the custom selection.

### Execution
1. List each core decision as a one-liner (e.g., "Target User: Early-stage startup founders")
2. Check for contradictions or outdated references between steps
3. If inconsistencies are found:
   - Display: "⚠️ Consistency check found [N] issue(s) before final output:"
   - List each issue with the affected steps
   - Ask user: "Should I fix these before generating the final output, or proceed as-is?"
4. If all consistent:
   - Display: "✅ Decision consistency check passed — all steps aligned."
   - Proceed to final output

### Why This Matters
During iterative planning, users may modify upstream decisions (e.g., change JTBD) while some downstream steps retain outdated content. This check catches those gaps before the final document is produced, preventing inconsistent deliverables.

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
| 🔧 Feature Extension Mode | Feature development spec: Problem → Selected solution → Impact scope → Execution scope → Risks |
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
□ PDF document (professional layout with bookmark navigation, suitable for formal sharing)
□ HTML planning report (interactive, suitable for online sharing)
□ Word document (suitable for collaborative editing)
□ PRD engineer delivery package (includes flowchart, DB schema, UI wireframe)
□ Presentation PPTX (suitable for meeting reports, recommend polishing with Keynote / PowerPoint after export)
□ Dev handoff package (CLAUDE.md + TASKS.md + TICKETS.md + technical architecture — ready to start development in Claude Code)
□ All of the above

You can also say 'No thanks' to finish, or specify a particular document.
You can also use /export [pdf|docx|pptx|html|md] to export at any time."
```

**Option display rules**:
- Source document uploaded → "Updated [document type]" listed first with "(recommended)" label
- Target audience is engineers → PRD and dev handoff package listed first
- Target audience is executives/leadership → PDF and presentation listed first
- Target audience is cross-functional → PDF, HTML report, and presentation all listed
- Quick Mode → Only ask if PDF or presentation is needed
- Target audience is yourself → Dev handoff package listed first

**Export trigger rules**:
- User selects PDF / Word / Presentation PPTX → Load `rules-export-document.md`
- First time triggering document export → Load `rules-document-tools.md` first to check and install necessary tools
- User selects HTML planning report → Load `06-html-report.md` (existing rules)
- User selects "All of the above" → Execute each format export in sequence
