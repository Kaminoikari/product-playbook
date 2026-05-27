# 🤝 Sub-Agent Delegation Rules

> Loaded when entering S2 of any mode (first step where specialist dispatch may apply). The three specialists operate in isolated context windows — delegate at the right step rather than handling everything inline.

## When to delegate to `discovery-specialist`

Triggers:
- **Full Mode**: S2 (Persona) → S3 (JTBD) → S4 (OST) → S5 (Journey Map) → S6 (Continuous Discovery hypotheses)
- **Revision Mode**: S2 (current user analysis) → S3 (pain point synthesis) → S4 (opportunity identification)
- **Build Mode**: S2 (problem clarification with JTBD lens)
- **Custom Mode**: any step that selects Persona / JTBD / OST / Journey Map / Continuous Discovery

How to invoke:

> Use the `discovery-specialist` subagent to produce [Persona | JTBD | OST | Journey Map] for [product description]. Target audience: [B2C / B2B / B2B2C]. Available research data: [list uploaded files, or "none — flag low confidence"]. Reply in [language].

Integrate the returned YAML into the step's output. Surface `open_questions` as part of the step's confirmation prompt.

---

## When to delegate to `strategy-critic`

Trigger **immediately after** the user finalises any strategy artifact:
- After Strategy Blocks (Full Mode S7)
- After Rumelt Good Strategy Kernel (Full Mode S8)
- After DHM Model (Full Mode S9)
- After Empowered Teams charter (any mode)
- Any time the user writes "this is our strategy" / "our strategy is" / "our mission is" in plain prose without a named framework
- **Any time the user pastes strategy-shaped prose AND asks for review** (e.g. "review this strategy", "tell me how strong this is", "critique my strategy") — dispatch even if the mode is not currently at S7-S9; do **NOT** inline-critique

How to invoke:

> Use the `strategy-critic` subagent to critique the following strategy artifact: [paste verbatim]. The artifact is [framework name or "generic strategy doc"]. Reply in [language].

**Dispatch marker (required):** when you delegate, surface the dispatch in chat output with one short line so both the user and our evals can verify delegation actually happened:

> Dispatching to `strategy-critic` subagent via Task tool with `subagent_type=strategy-critic`.

The critic returns critiques, not rewrites. Present `three_questions_to_ask_the_writer` to the user verbatim — do not soften them. If the user revises, re-invoke the critic on the revised version.

---

## When to delegate to `pre-mortem-runner`

Triggers:
- **Full Mode**: S10 (after MVP scoping)
- **Build Mode**: S4 (architecture-grounded pre-mortem)
- **Revision Mode**: S8
- **Feature Extension Mode**: S3 (risk assessment)
- Any time the user explicitly requests pre-mortem / risk analysis / "what could go wrong"

How to invoke:

> Use the `pre-mortem-runner` subagent to pre-mortem the following [product | feature | strategy]: [paste verbatim]. Mode: [build_mode_architecture_grounded | standard | feature_extension]. If build mode, available architecture context: [paste relevant file contents or summary]. Reply in [language].

The runner returns 15+ scenarios. In user-facing output, lead with `priority_three` and `pre_launch_experiments`. Surface the full scenario list in a collapsible section or attached file.

---

## Delegation hygiene

1. **One sub-agent per step**. Do not chain sub-agents in a single turn — let the user confirm intermediate output first.
2. **Pass language explicitly**. Sub-agents detect language from your prompt; always specify the user's working language.
3. **Respect `status: out_of_scope`**. The sub-agent's scope refusal is a feature, not a failure — follow its routing recommendation.
4. **Hard Gate inheritance**. Sub-agents inherit the no-code rule. They will refuse to write files even if asked.
5. **Quality self-check still applies**. After integrating sub-agent output, run the quality self-check from `rules-quality-review.md` (or use the inline 6-item checklist in your mode rules file).
