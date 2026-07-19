# 🎯 The Product Playbook

**Outcome-first product-thinking lenses for Claude Code.**

[![npm version](https://img.shields.io/npm/v/product-playbook.svg)](https://www.npmjs.com/package/product-playbook)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-blueviolet)](https://code.claude.com)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

> Integrates the most impactful PM thinking from Lenny's Podcast (Teresa Torres, Shreyas Doshi, Gibson Biddle, April Dunford, Todd Jackson, Marty Cagan, Richard Rumelt, and more), turning Claude into a senior product-thinking partner.

---

## ✨ What Is This?

The Product Playbook is a **Claude Code plugin** built from composable product-thinking lens skills: JTBD, PR-FAQ, positioning, pre-mortem, RICE-style solution prioritization, North Star / success metrics, MVP scoping, PMF / GTM, strategy kernel, and the rest.

A meta-skill (`product-playbook`) reads the outcome you actually want, picks the lens or lenses that get you there, and lets them blend when the situation needs more than one perspective, without walking every framework as a separate step. Every output ends with a one-line provenance tag naming the lens(es) applied, for example `— Frameworks: JTBD · Pre-mortem`.

A small set of relative guardrails stay dormant by default and surface only as a single non-blocking nudge when the outcome would genuinely be harmed by the current path; you can always proceed past them. Claude detects the language you're writing in and replies in it; the lens content itself is authored in English.

---

## 🚀 Install

### Option 1: Marketplace (recommended)

```
/plugin marketplace add kaminoikari/product-playbook
/plugin install product-playbook@product-playbook
```

### Option 2: `install.sh`

```bash
curl -fsSL https://raw.githubusercontent.com/kaminoikari/product-playbook/main/install.sh | bash
```

This installs the plugin as a personal skills-directory plugin at `~/.claude/skills/product-playbook/`, where Claude Code loads it in place, the same way it loads a marketplace install.

After either install method, run `/reload-plugins` in Claude Code (or restart it) to pick it up.

Update: re-run the same command, or `bash install.sh --update`.
Uninstall: `bash install.sh --uninstall`.

---

## 🧭 Usage

Just describe the outcome you want. The meta-skill routes to the right lens (or blend of lenses) on its own:

```
Help me figure out what job users hire my app for
→ jtbd

Is this feature worth building?
→ jtbd + solution-prioritization + pre-mortem, blended into one go/no-go call

Write me a PR-FAQ for this idea
→ pr-faq

What should our North Star metric be?
→ success-metrics

Does this positioning hold up against the alternatives?
→ positioning, then strategy-critic to stress-test it
```

### Available lenses

| Lens | Use it to |
|---|---|
| `persona-journey` | Understand who the users are and how they move through the experience |
| `jtbd` | Understand the job a user hires the product to do |
| `opportunity-solution-tree` | Connect a desired outcome to opportunities and candidate solutions |
| `problem-framing` | Sharpen a vague problem into pain points and ranked opportunities |
| `strategy-kernel` | Set or pressure-test product strategy and direction |
| `strategy-critic` | Stress-test a strategy artifact before it propagates downstream |
| `positioning` | Position a product against the alternatives customers actually consider |
| `pr-faq` | Define a product by writing its launch press release and FAQ first |
| `solution-prioritization` | Decide what to build first (RICE, GEM, impact vs. effort) |
| `pre-mortem` | Surface how a plan could fail before committing to it |
| `mvp-scoping` | Decide what makes the first version and what stays off the list |
| `success-metrics` | Define a North Star, supporting signals, and the activation moment |
| `pmf-gtm` | Assess product-market fit and plan go-to-market and pricing |
| `prd-and-handoff` | Produce an engineer-ready PRD and a dev handoff package |
| `product-spec-summary` | Consolidate planning into a final spec with a risk register |
| `document-export` | Render the plan as an HTML report or export to PDF / DOCX / PPTX |

### Optional depth — recipes

For a larger, end-to-end ask, the meta-skill can suggest one of four recipes, a pre-set lens sequence covering a whole workflow. Recipes are suggested, never forced:

| Recipe | For |
|---|---|
| `full-product-plan` | An end-to-end plan for a new product or a large new capability, strategy through handoff |
| `quick-validation` | A fast, one-page direction check before committing real effort |
| `product-revision` | Revising an already-shipped or already-planned product |
| `feature-extension` | Adding a feature to an existing system, weighed against what's already built |

---

## 🔑 Supporting capabilities

### 🪝 Session continuity

Lifecycle hooks (`hooks/hooks.json`) keep planning state without Claude needing to remember it across turns: injecting the meta-skill and any saved progress at session start, watching for off-topic detours mid-session, and reminding Claude to keep planning output to documents until the user explicitly moves to build. The session-start injection asserts product-playbook firmly for product and feature planning intent (so it holds its ground when other ideation plugins are installed) and stays dormant for everything else. No hook ever blocks you.

### 📄 Document export

The `document-export` lens renders planning output as an interactive HTML report, or exports it to PDF (with bookmarks, via Playwright), DOCX, or PPTX (via Pandoc).

### 🔒 Security awareness

`prd-and-handoff` includes an OWASP-aligned security section (auth/authorization, CORS/CSP, input validation) and a `.gitignore` template in every dev handoff package, plus a dedicated security scenario category in `pre-mortem`.

### 🛠 Engineering discipline (`dev-discipline`)

When the session moves from planning into implementation, a lightweight discipline layer takes over: right-sizing first (plan mode only for real architectural ambiguity; small single-purpose diffs skip reviewer subagents; large tasks freeze an outcome-based plan contract), TDD first with a named ban on test theater (failing test before production code; no hard-coded expectations, no faking the unit under test), scope integrity (out-of-scope finds get flagged, never silently fixed), secret and security hygiene, subagent economy (implement inline by default, with a dispatch protocol when one is justified: task instruction last, file paths instead of pasted content, declared I/O contracts, cheap models for mechanical roles), dual fresh-context review after each implementation milestone (a code reviewer for correctness plus a spec reviewer checking the diff — and the plan-file diff — against the agreed requirements, both auditing saved evidence, holding the bar constant across rounds, and closing with a fail-closed `VERDICT:` sentinel, capped at three rounds), and a finish-branch checklist with an entry-point launch check (run the real deliverable twice, assert the primary observable, screenshot frontend) that ends with the user choosing merge, PR, or keep.

It is deliberately light: a ~600-token session-start digest (size-capped by a regression test), one on-demand skill (`skills/dev-discipline/SKILL.md`), and two deterministic hooks. The TDD gate raises a one-line advisory when production code lands with no test referencing it anywhere in the repo (silence it with a `.product-tdd-waived` marker). The secret guard pauses any write whose content matches a high-confidence credential pattern (AWS / GitHub / Anthropic / OpenAI / Slack / Google / Stripe / npm key shapes, private-key blocks) or whose target is a `.env` file, and asks you to approve in one word. No hook ever hard-stops.

---

## 🧪 Development & Evals

The `evals/` directory ships two complementary test suites and a deterministic scorer.

**Local (free, recommended):** run the same scripts with the `claude` CLI authenticated via your Claude Pro/Max subscription (`claude login` once). No API key, no marginal cost.

**CI (manual trigger only, no extra billing):** `.github/workflows/eval-gate.yml` runs both suites on `workflow_dispatch` only, Actions UI → "Eval Report" → "Run workflow", or `gh workflow run eval-gate.yml --ref <branch>`. It never blocks merge or publish; the maintainer decides whether to act on regressions.

```bash
# Recommended: one command runs both suites
npm run eval

# Or run pieces individually
npm run eval:trigger      # checks if the skill auto-triggers
npm run eval:behavioral   # uses claude as assistant AND judge
npm run eval:quick        # 1 run only, no majority vote (fast iteration)
npm run eval:test         # unit tests for the scoring module

# Unit tests (test runner: unittest)
python3 -m unittest discover tests
```

Every expectation is tagged `critical` / `warning` / `info`, scored 0–100, and banded `healthy` / `needs-attention` / `at-risk`. See `evals/compute_eval_score.py` for the single source of truth on scoring.

**Plugin isolation (default on):** every eval call runs `claude -p` with known-interfering plugins disabled (currently `superpowers`, whose session-start "brainstorm first" directive would otherwise pre-empt product-playbook on ambiguous prompts and skew the score) **and the plugin under test force-enabled** (`product-playbook@skills-dir: true`). The self-enable matters when product-playbook is scoped per-project (user-level `false` plus a repo-local `true`): evals run from `$HOME`, where only the user-level `false` applies, so without it the plugin never loads headless and every `should_trigger` case is a structural zero regardless of model or content. Disabling a plugin that is not installed is a no-op, so clean CI environments are unaffected. Set `PRODUCT_PLAYBOOK_EVAL_ISOLATE=0` to turn isolation off, `PRODUCT_PLAYBOOK_EVAL_ENSURE_SELF=0` to skip the self-enable, or override the disable list via `PRODUCT_PLAYBOOK_EVAL_DISABLE_PLUGINS=<name@marketplace,...>`.

> **Headless trigger-rate caveat.** The trigger eval scores a query as "fired" only when `claude -p` emits a formal `Skill` tool-use or the `— Frameworks:` provenance line. Two cases read as false negatives headless even though behavior is correct: (1) `dev-discipline` — its SessionStart digest hook does not fire headless and it carries no provenance on code output, so only a formal `Skill(dev-discipline)` call registers; (2) exploratory meta-skill prompts ("help me think through this idea") — the model asks a clarifying question first and, with no follow-up user turn, produces no deliverable and thus no provenance within the turn budget. Interactive sessions are unaffected. Treat headless trigger numbers as a lower bound for these two categories.

**Long unattended runs:** a full `npm run eval` makes ~230 `claude` calls against your subscription quota. To run it detached (survives the terminal, keeps the Mac awake):

```bash
nohup caffeinate -is bash -c 'cd <repo> && npm run eval' > /tmp/full-eval.log 2>&1 & disown
```

---

## 🤝 Contributing

Contributions are welcome, especially:

- 🔎 **New lenses**: add another product-thinking framework as a composable skill
- 📝 **Examples**: worked examples that sharpen a lens's trigger and output quality
- 🐛 **Bug reports**: logic issues or gaps found during use
- 💡 **UX improvements**: suggestions for how lenses select, blend, and hand off to each other

### How to contribute

1. Fork this repo
2. Create your feature branch (`git checkout -b feature/new-lens`)
3. Commit your changes (`git commit -m 'feat: add new lens'`)
4. Push to the branch (`git push origin feature/new-lens`)
5. Open a Pull Request

---

## 📚 Framework Sources & Further Reading

The lenses in this project are synthesized from the public work of these thought leaders:

| Thought Leader | Core Contribution | Recommended Reading |
|----------------|-------------------|---------------------|
| Teresa Torres | Continuous Discovery, Opportunity Solution Tree | *Continuous Discovery Habits* |
| Shreyas Doshi | LNO, Pre-mortem, Three Levels of Product Work | Lenny's Podcast Ep.3 |
| Gibson Biddle | DHM Model, GEM | Lenny's Podcast |
| April Dunford | Positioning Framework | *Obviously Awesome* |
| Todd Jackson | Four-level PMF, Four P's | Lenny's Podcast |
| Richard Rumelt | Good Strategy / Bad Strategy | *Good Strategy Bad Strategy* |
| Marty Cagan | Empowered Teams | *Inspired*, *Empowered* |
| Clayton Christensen | Jobs to Be Done | *Competing Against Luck* |
| Amazon | Working Backwards / PR-FAQ | *Working Backwards* |
| Sean Ellis | Sean Ellis Score, Growth | *Hacking Growth* |
| Lenny Rachitsky | Shape / Ship / Synchronize | Lenny's Newsletter + Podcast |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE), free to use, modify, and distribute without restriction.

---

## ⭐ Star History

If this project helps you, give it a ⭐ so more people can find it!

[![Star History Chart](https://api.star-history.com/svg?repos=kaminoikari/product-playbook&type=Date)](https://star-history.com/#kaminoikari/product-playbook&Date)

---

<p align="center">
  <strong>Built with ❤️ for Product Managers who want to build things that matter.</strong>
</p>

---

Copyright (c) 2026 Charles Chen.
