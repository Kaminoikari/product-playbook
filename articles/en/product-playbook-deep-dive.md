# One Open-Source Claude Skill Replaces Your Entire PM Toolkit — 22 Curated Frameworks, 6 Execution Modes, and a Change Propagation Engine No Other Tool Has

*Everyone has an AI copilot. Nobody has an AI product manager.*

**Star on GitHub: [github.com/kaminoikari/product-playbook](https://github.com/kaminoikari/product-playbook)**

```bash
npx product-playbook
```

---

# Part I: The Problem

GitHub Copilot has 1.8 million paid subscribers. Cursor raised $900M at a $9B valuation. The AI coding arms race is real. But nobody is asking the harder question: **what code should these tools be writing?**

We automated the easy part — turning specs into software — and left the genuinely hard part to gut instinct and duct tape. The result: 35% of startups fail because they build something nobody wants (CB Insights). The most expensive line of code solves the wrong problem, and AI coding tools are happy to help you write it faster than ever.

The typical PM's day is a mess. Notion for the PRD, ChatGPT for brainstorming, Google Docs for positioning, Figma for design context, Jira for tickets — six tools, four formats, zero connections between them. Framework knowledge stays shallow. Documents drift apart after every change. The handoff to engineering always reveals that the spec doesn't match the real system.

I built The Product Playbook because I lived this problem. I watched PMs (including myself) waste weeks producing plans that sounded good but fell apart the moment they hit engineering reality. I wanted a single tool that could enforce the rigor of a senior PM coach while staying grounded in the actual codebase. Not another document generator — a complete operating system for product thinking.

---

# Part II: What It Is

The Product Playbook is a Claude AI Skill — a system-level instruction set that gives Claude persistent capabilities, file system access, and multi-session context. It's open source (MIT), supports six languages (English, Traditional Chinese, Japanese, Simplified Chinese, Spanish, Korean), and works in both Claude Code and Claude.ai.

Install with one command. Type "I want to build a product." The system guides you through structured frameworks with quality gates, progress tracking, and change propagation. Every step produces a concrete output. Every output is reviewed. Every change ripples to all downstream dependencies.

## The 6 Execution Modes

| Mode | Steps | Duration | Best For |
|------|-------|----------|----------|
| Quick Mode | 3 | ~30 min | Rapid validation, pitch prep |
| Full Mode | 20 | Several hours | Comprehensive product plans |
| Revision Mode | 12 | 1-2 hours | Optimizing existing products |
| Custom Mode | 4-16 | Varies | Specific framework gaps |
| Build Mode | 7 | ~1 hour | Problem known, need execution |
| Feature Extension | 4 | ~30 min | Adding to existing product |

## The 22 Frameworks — Curated from Lenny's Podcast

The frameworks aren't random. I spent years studying Lenny's Podcast — hundreds of hours of episodes featuring the world's best product minds: Teresa Torres, Shreyas Doshi, Gibson Biddle, April Dunford, Marty Cagan, Richard Rumelt, Todd Jackson, Sean Ellis, Clayton Christensen. I noticed that many popular frameworks overlap. Some are variations of the same idea. Others are genuinely distinct but never get connected in practice.

I removed the redundancy and kept the 22 that actually drive product decisions, organized by phase:

- **Understanding Users (5):** JTBD, Persona, User Journey Map, Continuous Discovery Habits, Opportunity Solution Trees
- **Defining the Problem (2):** April Dunford Positioning, HMW Reframing
- **Solution Design (5):** PR-FAQ (Working Backwards), Pre-mortem, GEM Model, RICE Scoring, MVP Definition
- **Strategy (4):** Strategy Blocks, Good Strategy Kernel, DHM Model, Empowered Teams
- **Measurement & Delivery (6):** North Star Metric, Three-Layer Signals, Aha Moment, Four-Level PMF, Sean Ellis Score, GTM Strategy

The critical point: these frameworks are **connected**. JTBD feeds into Positioning, which feeds the PR-FAQ headline. Pre-mortem risks shape MVP scope. North Star must measure the JTBD outcome. The change propagation engine enforces these connections automatically.

## Who It's For

**Solo PMs, indie hackers, startup founders, and product-oriented engineers** — people who need rigorous product planning without a team of senior PMs to coach them. The solo PM doesn't have time to read twelve books. The indie hacker needs 30 minutes of validation before committing weekends. The engineer-turned-founder knows how to build but has never written a JTBD statement.

---

# Part III: Key Differentiators

## 1. Change Propagation Engine

Product planning isn't linear. You discover new insights in Step 7 that invalidate Step 3. In every other tool, this creates silent inconsistency — documents drift apart and nobody knows what's outdated.

The Product Playbook tracks explicit dependencies. Modify your JTBD, and the system flags every downstream output that needs updating: HMW, Positioning, PR-FAQ, North Star, Product Spec. Minor changes propagate automatically. Major shifts prompt you for confirmation. This alone is worth the install — it's the difference between a living plan and a collection of stale documents.

## 2. Dev Handoff Package

One command generates a complete development starter kit:

```
├── CLAUDE.md         → Project context for Claude Code
├── TASKS.md          → Feature breakdown + phased delivery
├── TICKETS.md        → Jira/Linear-ready tickets
├── docs/PRD.md       → Full product requirements
├── docs/ARCHITECTURE.md → DB schema + API + directory structure
└── scripts/setup.sh  → One-click project initialization
```

Engineers open Claude Code, read `CLAUDE.md`, and start building. Security is baked in — OWASP Top 10 checklist, auth/CORS/CSP architecture, `.gitignore` with sensitive file exclusions. The handoff gap disappears because planning and development happen in the same tool, same context, same project directory.

## 3. Quality Hard Gates

Every step includes a quality checklist. The hard gate rule: **at least one item must be marked as failed.** The AI cannot rubber-stamp its own work — it must identify the weakest aspect and explain how to strengthen it.

Without this, AI self-review is theater. The benchmark shows a +100% delta: without the Skill, Claude never critiques its own output (0% pass rate). With it, every step gets genuine self-critique. This is the difference between a first draft and a senior PM's systematic review.

## 4. Codebase-Aware Planning

Launch the Skill in a project directory and it auto-scans your `package.json`, database schema, API routes, Dockerfiles, and module structure. It then uses this real knowledge throughout planning:

- **Pre-mortem risks** reference your actual architecture
- **MVP scope** references your actual modules
- **Dev handoff** produces incremental deltas, not greenfield diagrams

This collapses the traditional two-step process — PM imagines the system, then engineers correct the imagination — into one step grounded in reality from the start.

## 5. Decision Consistency Check

Before any final output, the system runs a structured cross-step audit. For Full Mode, it checks seven dimensions: target user consistency, JTBD reflection in PR-FAQ, positioning alignment, solution direction, MVP-PR-FAQ match, North Star measurability, and pre-mortem relevance. Inconsistencies surface before you finalize — not after engineering starts building.

---

# Part IV: Benchmark Results

The Skill includes an open-source eval suite: 9 test scenarios, 49 expectations, same model (Claude Sonnet), same prompts, only variable is whether the Skill is installed.

| Test | With Skill | Without Skill | Delta |
|------|:----------:|:-------------:|:-----:|
| Mode Selection | 100% | 0% | **+100%** |
| Quick Mode JTBD Analysis | 100% | 43% | +57% |
| JTBD Depth (B2B + Five Whys) | 100% | 57% | +43% |
| PR-FAQ Writing Quality | 100% | 33% | **+67%** |
| Revision Mode Recognition | 100% | 67% | +33% |
| Quality Self-check Hard Gate | 100% | 0% | **+100%** |
| Feature Extension Mode | 100% | 17% | **+83%** |
| Security Integration | 100% | 25% | **+75%** |
| Context Bootstrap | 100% | 0% | **+100%** |

**Overall: 100% vs. ~27% — a +73% improvement.**

Three tests show +100% deltas: Mode Selection, Quality Self-check, and Context Bootstrap. These capabilities simply don't exist without the Skill. Claude doesn't spontaneously offer structured mode selection, doesn't critique its own output, and doesn't collect product context before planning. These behaviors only emerge with the Skill installed.

The remaining tests show +33% to +83% deltas — areas where Claude can partially perform the task but with significantly less depth and structure.

---

# Part V: Competitive Landscape

| Dimension | Product Playbook | ChatPRD | PM-Skills (Dean) | Lenny's Skills | pm-skills | Notion AI |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|
| PM Frameworks | 22 | ~5 | 46 | 86 | 27 | 0 |
| Connected Workflow | Yes | No | No | No | No | No |
| Change Propagation | Yes | No | No | No | No | No |
| Execution Modes | 6 | 1 | N/A | N/A | 1 | N/A |
| Dev Handoff | Yes | No | No | No | No | No |
| Codebase-Aware | Yes | No | No | No | No | No |
| Quality Hard Gates | Yes | No | No | No | No | No |
| Cross-Session Context | Yes | No | No | No | No | No |
| Team Collaboration | No | Yes | No | No | No | Yes |
| Pricing | Free (MIT) | $15-24/mo | Free | Free | Free | $10/mo+ |

The market splits into three categories:

1. **Broad but shallow** (Lenny's 86 standalone skills, Dean's 46 — independent, no connected workflow)
2. **Deep but narrow** (ChatPRD does PRD well, but no JTBD, Pre-mortem, or dev handoff)
3. **General purpose** (Notion AI doesn't know what a PR-FAQ format is)

The Product Playbook occupies a unique position: depth + connectivity + integration. Fair acknowledgment: ChatPRD wins on team collaboration, Lenny's Skills wins on topic breadth. No tool is best in every dimension — choose based on your biggest pain point.

---

# Part VI: Get Started

**Step 1: Install.**

```bash
npx product-playbook
```

**Step 2: Open Claude Code and type:**

```
I want to build a product
```

Or use a slash command: `/product-quick`, `/product-full`, `/product-build`, `/product-revision`, `/product-feature`.

**Step 3: Follow the guided flow.** Choose a mode, describe your product, and let the system walk you through each framework. Quick Mode gives you a validated direction in 30 minutes. Full Mode gives you a comprehensive plan in an afternoon.

---

**Star on GitHub: [github.com/kaminoikari/product-playbook](https://github.com/kaminoikari/product-playbook)**

```bash
npx product-playbook
```

*The Product Playbook is open source under the MIT License. Created by Charles Chen.*
