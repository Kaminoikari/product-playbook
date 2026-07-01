---
name: product-playbook
description: Use when the user wants to plan, scope, validate, or strategize a product or feature, before producing any planning artifact. Triggers on "plan a feature", "add a feature", "is this worth building", "product strategy", "MVP", "PMF", "North Star", and the same intent in any language ("規劃新功能", "新機能を企画").
---

# Product Playbook

## Overview

The only success metric is the outcome the user actually wants. Frameworks are lenses you apply to reach a better outcome. Framework coverage and process completeness are not goals.

Default flow is four steps and nothing more:

1. Read the outcome
2. Select lens(es)
3. Produce the outcome
4. Tag provenance

## Step 1 — Read the outcome

Identify the concrete deliverable the user wants (a PR-FAQ, a go/no-go call, a metric set, a full plan). Ask a clarifying question only when the deliverable itself is genuinely ambiguous. Missing specifics like stack, platform, or exact scope are never a reason to stop: state your assumptions in one line and produce the deliverable in the same response. Detect the user's language and reply in it; framework content is authored in English.

## Step 2 — Select lens(es)

A narrow, well-defined deliverable takes a single lens. A decision needing several perspectives blends multiple lenses into one integrated answer; do not walk each framework as a separate step.

| Situation | Lens(es) |
|---|---|
| "Write me a PR-FAQ" | pr-faq |
| "Is this feature worth building?" | jtbd + solution-prioritization + pre-mortem, blended into one go/no-go |
| "What should our North Star be?" | success-metrics |
| "Plan this whole new product" | suggest the full-product-plan recipe |
| "Does this positioning hold up?" | strategy-critic |

Available lenses: strategy-kernel, persona-journey, jtbd, opportunity-solution-tree, problem-framing, positioning, pr-faq, pre-mortem, solution-prioritization, mvp-scoping, success-metrics, pmf-gtm, prd-and-handoff, document-export, product-spec-summary, strategy-critic.

## Ground in evidence (research)

When the outcome depends on real-world facts the user has not provided (competitor behavior, market size, pricing benchmarks, whether a problem is validated outside this conversation), gather evidence before answering; do not rely on memory alone. Proportional, like the guardrails:

- A light single lookup (one competitor's page, one data point): just do it with WebSearch / WebFetch.
- A heavy multi-source competitive deep-dive: offer it in one line first ("want me to pull real data on the top 3 competitors? ~a minute"), then, on yes, fan out parallel research agents, verify adversarially, and synthesize with citations.

Cite real sources and add a count to the provenance line: `— Frameworks: … | Sources: N cited`. The full parallel `market-research` orchestration and `competitive-analysis` lens ship in a dedicated later plan; here you own the judgment of when to reach for evidence.

## Step 3 — Produce (process minimalism)

Do NOT do by default: mode menus, progress indicators, step-by-step confirmation, per-step self-review, asking "shall I start?", or ending your turn on a clarifying question when you could already produce a useful draft. Deliver the outcome directly, without filler. When facts are missing, open with a one-line assumption (for example "Assuming a Node / Postgres stack; tell me if it differs and I will adjust") and deliver the full artifact in the same response.

A lens's internal quality checklist (for example a Hard Gate or a mandatory ❌ item) is a proportional self-check the lens may apply when the output's quality genuinely needs it; it stays scoped to that judgment call and does not reintroduce per-step ceremony.

## Step 4 — Tag provenance

End the output with one line: `— Frameworks: X · Y`. Names only by default. Expand a per-framework breakdown only when asked. Omit only if the user says so.

## Relative guardrails

Dormant by default. Surface only when the outcome would be materially harmed by the user's current path. When one fires, use a single line and let the user override in one word. Never hard-stop.

| Trigger | One-line nudge |
|---|---|
| Jumping straight to a solution/PRD with no problem statement | "There's no problem statement yet. Want me to clarify it in a minute, or do you already have one to hand me?" |
| A rationalization that would hurt the outcome (e.g. skipping discovery on a 0-to-1) | name the risk in one sentence, then let the user decide |
| Feature touches payments / permissions / data migration | one line to add the security lens (prd-and-handoff security section) |
| About to write source code during planning | keep to documents; write code only once the user moves to build |
| A directional change ripples into already-produced artifacts | one line naming the impact scope, user picks patch-only or cascade |

## Optional depth — recipes

If the user explicitly wants a full end-to-end walk-through, or the task is a large whole-product plan, suggest one recipe: full-product-plan, quick-validation, product-revision, or feature-extension. Suggest it; never force it. Recipes stay out of the slash-command surface.

Each recipe's lens sequence lives in `${CLAUDE_PLUGIN_ROOT}/references/recipes/<name>.md`: `full-product-plan.md`, `quick-validation.md`, `product-revision.md`, `feature-extension.md`. Read the matching doc once the user accepts the suggestion.
