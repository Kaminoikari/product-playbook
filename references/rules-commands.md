# 🔧 Framework Menu + Supplementary Commands

> Loaded when the user requests "list frameworks," "show me the available frameworks," or uses a supplementary command.

## Specify a Framework

**Two ways to trigger:**

**Method A (User directly names a framework):** Go straight into that framework's guided flow — no need to ask again.

**Method B (User says "I want to pick a framework," "list all frameworks," etc.):** Present the following menu:

```
📚 Available frameworks — enter a number or name:

【Understanding Users】
 1. JTBD (Jobs to Be Done) — Identify the job users truly want to accomplish
 2. Persona — Build usage/task/motivation-driven user profiles
 3. User Journey Map — Map the complete user experience journey
 4. Continuous Discovery — Build a weekly habit of engaging with users

【Defining the Problem】
 5. OST / Opportunity Solution Tree — Systematically link opportunities to solutions
 6. Positioning / April Dunford — Find the real competitive arena and differentiation
 7. HMW — Reframe pain points as design questions

【Solution Design】
 8. Working Backwards / PR-FAQ — Start from user outcomes and work backwards to the solution
 9. Pre-mortem — Predict and prevent failure before it happens
10. GEM — Growth / Engagement / Monetization three-dimensional prioritization
11. RICE — Quantitative feature prioritization
12. MVP — Define minimum viable product scope

【Strategy Layer】
13. Strategy / Strategy Blocks — Mission → Vision → Strategy hierarchy
14. DHM Model — Delight / Hard to copy / Margin-enhancing opportunity assessment
15. LNO Framework — Leverage / Neutral / Overhead time allocation
16. Empowered Teams — Empowered teams vs. feature teams

【Measurement Layer】
17. North Star / North Star Metric — Define the single metric representing core user value
18. PMF — Four levels of Product-Market Fit assessment
19. Sean Ellis Score — Quantify PMF enthusiasm level

【Business Layer】
20. Business Model & Pricing — Revenue model selection and value-based pricing alignment
21. GTM Strategy — Go-to-Market launch and customer acquisition strategy

【Dev Handoff】
22. Dev Handoff — Generate CLAUDE.md + TASKS.md + TICKETS.md to hand off to Claude Code for development

Enter a framework number or name (multiple selections allowed, separated by commas):
```

## Skip Discovery / Go Straight to Build

When the user says "skip user research," "problem is already known," "go straight to Develop," read `references/rules-build.md` and follow the Build Mode step sequence.

> Remind the user: "Skipping the user research phase means your solution is built on assumptions. We recommend conducting Continuous Discovery as soon as possible after execution to validate."

## Feature Extension Mode Trigger

- "Add a feature" / "I want to add a new feature" / "new feature for existing product" → triggers Feature Extension Mode (reads `references/rules-build.md` → Feature Extension Quick Path)

## Supplementary Commands

| Command | Behavior |
|---------|----------|
| `"Switch to [framework]"` | Switch immediately, preserving completed content |
| `"I want to change the target audience"` | Re-adjust framework priority and presentation style |
| `"Skip this step"` | Remind of necessity, then respect the decision and move to the next step |
| `"Go back to [step/framework name]"` | Return to the specified step for re-guidance (see `references/rules-change-propagation.md`) |
| `"Simplify"` / `"Expand"` | Condense to key points / Add in-depth analysis |
| `"Generate report"` | Read `references/06-html-report.md`, produce an HTML planning report |
| `"Generate PRD"` / `"Generate engineer docs"` | Read `references/04b-solutions.md`, integrate PR-FAQ + MVP + User Story + Pre-mortem, **automatically also generate: flowchart (Mermaid) + DB schema (Mermaid ERD) + UI wireframe (HTML)** |
| `"Generate flowchart"` / `"Draw me a flowchart"` | Output a flowchart in Mermaid syntax (standalone trigger) |
| `"Generate DB schema"` / `"Design the database"` | Output a DB schema in Mermaid ERD syntax (standalone trigger) |
| `"Generate UI wireframe"` / `"Draw me a wireframe"` | Output a low-fidelity UI wireframe in HTML/SVG (standalone trigger) |
| `"Generate presentation"` / `"Make a PPT"` | Invoke the system pptx skill |
| `"Adapt this document for [audience]"` | Re-organize framework highlights and language for the specified audience |
| `"I only have 15 minutes"` | Provide the three most critical decision questions or actions |
| `"Run a completeness assessment"` | Assess which areas are solid and which carry risk |
| `"Help me find the assumptions"` | Identify all unvalidated core assumptions |
| `"Run a Pre-mortem"` | Immediately run a pre-mortem on any solution |
| `"Generate versions for different audiences"` | Automatically produce summaries tailored to multiple audiences |
| `"What PMF level is this product at?"` | Determine the PMF level and explain the next milestone |
| `"Help me find the bottleneck"` | Analyze the biggest obstacle to achieving the Aha Moment |
| `"This is a revision, not a new product"` | Switch to Revision Mode (read `references/rules-revision.md`) |
| `"I need to convince my boss to approve"` | Switch to Boss Mode — emphasize business value and resource logic |
| `"Start development"` / `"Generate dev handoff package"` | Read `references/07a-handoff-core.md`, confirm tech stack, then generate the full dev handoff package |
| `"Set up the project"` / `"Connect to Claude Code"` | Same as above |
| `"Pause"` / `"Save"` / `"Do something else first"` | Save progress per `references/rules-progress.md` |
| `"Continue"` / `"Back to planning"` | Resume per `references/rules-progress.md` |
| `"Clear progress"` / `"Start over"` | Delete progress file and start from scratch |
| `/export [format]` | Export to specified format. format = `pdf` / `docx` / `pptx` / `html` / `md`. Read `references/rules-export-document.md`. On first use, load `references/rules-document-tools.md` first to check tools. |
| `/parse [file]` | Parse an uploaded document to Markdown. Supports PDF / DOCX / PPTX / images. Read `references/rules-import-document.md`. On first use, load `references/rules-document-tools.md` first to check tools. |

**Context-aware command hints**: After each step is completed, proactively suggest 2-3 of the most relevant available commands based on the current progress.
