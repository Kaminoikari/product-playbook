[English](README.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [Español](README.es.md) | [한국어](README.ko.md)

# 🎯 The Product Playbook

**世界级产品规划 AI Skill — 从 Idea 到开发，一套框架全搞定**

[![npm version](https://img.shields.io/npm/v/the-product-playbook.svg)](https://www.npmjs.com/package/the-product-playbook)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://code.claude.com)
[![Claude.ai](https://img.shields.io/badge/Claude.ai-Custom%20Skill-blue)](https://claude.ai)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![i18n](https://img.shields.io/badge/i18n-6%20languages-green)](README.md)

> 整合 Lenny's Podcast 历来最重要的 PM 框架（Teresa Torres、Shreyas Doshi、Gibson Biddle、April Dunford、Todd Jackson、Marty Cagan、Richard Rumelt 等），让 AI 成为你的资深产品经理教练。

---

## ✨ 这是什么？

The Product Playbook 是一个 **Claude AI Skill**，能够系统性地引导你完成从 0 到 1 的产品规划。它不只是一个提示词（prompt），而是一套完整的互动式框架引导系统，包含：

- 🧭 **6 种执行模式** — 从 30 分钟快速验证到完整企划（含功能扩充快速路径）
- 📐 **22 个产品框架** — 涵盖 Discovery → Define → Develop → Deliver 全流程
- 🔄 **变更传播引擎** — 修改任何步骤，自动更新所有下游产出
- 📎 **文件智慧整合** — 上传数据、截图、文件，AI 自动整合到对应步骤
- 🔗 **开发衔接** — 产出 CLAUDE.md + TASKS.md + TICKETS.md，无缝衔接 Claude Code 开发
- 📊 **多格式产出** — HTML 报告、PRD、PowerPoint、开发交接包

**用一句话触发整个流程：**

```
我想做一个产品
```

---

## 🎬 Demo

<p align="center">
  <img src="assets/demo-build-zh-CN.gif" alt="The Product Playbook Demo — Build Mode" width="800">
</p>

> 上图展示**直接实作模式**：输入需求 → 扫描 codebase → 侦测技术栈 → 引用框架进行问题厘清，直接进入解法设计。

---

## 🚀 快速开始

### 方法一：Claude.ai 自订 Skill

1. 下载本 repo 的 zip 档
2. 前往 [Claude.ai](https://claude.ai) → 设定 → 自订 Skill
3. 上传整个 `the-product-playbook/` 数据夹
4. 在对话中说「我想做一个产品」即可触发

### 方法二：Claude Code Skill（推荐）

> 💡 更新方式：重新执行安装指令即可覆盖更新。

| 方式 | 适合谁 | 需要什么 |
|------|--------|----------|
| ① 复制贴上 | 新手 | 只要开 Claude Code |
| ② 一键安装 | 开发者 | 终端机 |
| ③ 手动安装 | 想自订路径 | 终端机 + git |

#### ① 复制贴上安装（最简单）

启动 Claude Code 后，直接贴上以下内容，Claude 会自动帮你完成安装：

```
请帮我执行以下指令来安装（或更新）the-product-playbook skill，
执行完毕后告诉我结果：

git clone https://github.com/kaminoikari/the-product-playbook.git /tmp/the-product-playbook
mkdir -p ~/.claude/skills ~/.claude/commands
cp -r /tmp/the-product-playbook ~/.claude/skills/the-product-playbook
cp /tmp/the-product-playbook/commands/* ~/.claude/commands/
rm -rf /tmp/the-product-playbook
```

#### ② 一键安装（终端机）

```bash
# curl
curl -fsSL https://raw.githubusercontent.com/kaminoikari/the-product-playbook/main/install.sh | bash -s -- --lang zh-CN

# npx（需要 Node.js）
npx the-product-playbook --lang zh-CN
```

解除安装：

```bash
curl -fsSL https://raw.githubusercontent.com/kaminoikari/the-product-playbook/main/install.sh | bash -s -- --uninstall
# 或
npx the-product-playbook --uninstall
```

#### ③ 手动安装

```bash
git clone https://github.com/kaminoikari/the-product-playbook.git
mkdir -p ~/.claude/skills ~/.claude/commands
cp -r the-product-playbook ~/.claude/skills/the-product-playbook
cp the-product-playbook/commands/* ~/.claude/commands/
```

安装完成后，在 Claude Code 中触发：

```bash
# Skill 主指令
> /the-product-playbook

# Slash Commands（安装后可用）
> /product-quick 我想做一个记帐 App
> /product-full 宠物社群平台
> /product-revision 改版我们的电商结帐流程

# 或自然语言
> 我想做一个产品企划
> 用 JTBD 分析一下我的产品
> 帮我做个 MVP 规划
```

---

## 📦 文件结构

```
the-product-playbook/
├── SKILL.md                          # 主控核心：模式定义、步骤序列、指令系统
├── LICENSE                           # MIT License
├── README.md                         # English README
├── README.zh-CN.md                   # 简体中文 README（本文件）
├── assets/
│   └── demo.gif                      # README 动态展示图
├── commands/                         # Claude Code CLI Slash Commands（可选安装）
│   ├── product-quick.md              # /product-quick — 快速模式
│   ├── product-full.md               # /product-full — 完整模式
│   ├── product-revision.md           # /product-revision — 改版模式
│   ├── product-build.md              # /product-build — 直接实作模式
│   ├── product-prd.md                # /product-prd — 产出 PRD
│   ├── product-report.md             # /product-report — 产出 HTML 报告
│   └── product-dev.md                # /product-dev — 产出开发交接包
└── references/
    ├── 00-opportunity-check.md       # 机会评估 + DHM Model
    ├── 01-strategy.md                # Strategy Blocks + Rumelt + OKR
    ├── 02-discovery.md               # Persona + JTBD + OST + Journey Map
    ├── 03-define.md                  # 痛点 + Positioning + HMW + 机会评估
    ├── 04-develop.md                 # PR-FAQ + Pre-mortem + RICE + MVP + PRD
    ├── 05-deliver.md                 # North Star + PMF + GTM + 商业模式 + 产品规格
    ├── 06-html-report.md             # HTML 企划报告产出规格
    ├── 07-dev-handoff.md             # 开发衔接：CLAUDE.md + TASKS.md + 架构
    ├── 08-security-checklist.md      # OWASP Top 10 + CORS + CSP + 安全架构
    ├── rules-context.md              # 跨 Session 产品上下文累积规则
    └── rules-*.md                    # 各模式步骤规则 + 进度/变更/文件整合规则
```

---

## 🧭 六种执行模式

| 模式 | 步骤数 | 耗时 | 适合情境 |
|------|--------|------|---------|
| 🚀 **快速模式** | 3 步 | ~30 分钟 | 快速验证想法、准备简报 |
| 📦 **完整模式** | 20 步 | 数小时 | 新产品规划、重大改版 |
| 🔄 **改版模式** | 12 步 | 1-2 小时 | 既有产品改版优化 |
| ✏️ **自订模式** | 4-16 步 | 依选择 | 补足特定环节 |
| ⚡ **直接实作** | 7 步 | ~1 小时 | 问题已知，直接进解法 |
| 🔧 **功能扩充** | 4 步 | ~30 分钟 | 既有产品加单一功能 |

---

## 📐 涵盖的框架

### 理解用户
| 框架 | 提出者 | 用途 |
|------|--------|------|
| JTBD（Jobs to Be Done） | Clayton Christensen | 找出用户真正想完成的工作 |
| Persona | — | 用途/任务/动机导向的用户角色 |
| User Journey Map | — | 用户完整体验旅程 |
| Continuous Discovery | Teresa Torres | 每周接触用户的持续习惯 |
| OST（机会解法树） | Teresa Torres | 系统化链接机会与解法 |

### 定义问题
| 框架 | 提出者 | 用途 |
|------|--------|------|
| Positioning | April Dunford | 竞争场域和差异化定位 |
| HMW（How Might We） | — | 将痛点转化为设计问题 |

### 解法设计
| 框架 | 提出者 | 用途 |
|------|--------|------|
| Working Backwards / PR-FAQ | Amazon | 从用户结果出发倒推解法 |
| Pre-mortem | Shreyas Doshi | 在失败前预测并预防失败 |
| GEM Model | Gibson Biddle | Growth / Engagement / Monetization 排序 |
| RICE Scoring | Intercom | 量化功能优先排序 |
| MVP 定义 | — | 最小可行产品范围 |

### 策略层
| 框架 | 提出者 | 用途 |
|------|--------|------|
| Strategy Blocks | Chandra Janakiraman | Mission → Vision → Strategy 层级结构 |
| Good Strategy Kernel | Richard Rumelt | 诊断 → 指导方针 → 连贯移动 |
| DHM Model | Gibson Biddle | Delight / Hard to copy / Margin-enhancing |
| Empowered Teams | Marty Cagan | 赋能型团队 vs 功能型团队 |

### 衡量与交付
| 框架 | 提出者 | 用途 |
|------|--------|------|
| North Star Metric | Sean Ellis / Amplitude | 代表核心用户价值的单一指标 |
| 四级 PMF 框架 | Todd Jackson | 判断产品市场契合度 |
| Sean Ellis Score | Sean Ellis | 量化 PMF 热情程度 |
| GTM 策略 | — | Go-to-Market 上市与获客 |
| 商业模式与定价 | — | 收费模式选择与价值定价 |

---

## 🔑 核心特色

### 📎 智慧文件整合

在任何步骤中上传补充文件，AI 自动判断并整合：

| 上传内容 | 自动整合到 |
|---------|-----------|
| 竞品截图 | Positioning 分析 |
| 访谈逐字稿 | Persona + JTBD |
| 用户数据 CSV | 机会评估 + PMF 判断 |
| 市场报告 PDF | 机会评估 + Strategy |
| 既有 PRD | 改版模式 + MVP |

### 🔄 变更传播引擎

修改任何上游步骤，下游自动更新：

```
修改 JTBD → 自动更新 HMW、Positioning、PR-FAQ、North Star、产品规格摘要
修改 MVP  → 自动更新 User Story、DB Schema、产品规格摘要
```

### 🔗 开发衔接

产出完整开发交接包，一句话启动 Claude Code 开发：

```
📦 开发交接包
├── CLAUDE.md          → Claude Code 专案记忆
├── TASKS.md           → 功能拆解 + Phase 分期
├── TICKETS.md         → 开票清单（可直接在 Jira/Asana/Linear 开票）
├── docs/
│   ├── PRD.md         → 完整 PRD
│   ├── ARCHITECTURE.md → DB Schema + API + 目录结构
│   └── PRODUCT-SPEC.md → 产品规格摘要
└── scripts/
    └── setup.sh       → 一键初始化脚本
```

```bash
# 在 Claude Code 中一句话开始开发
> 请读取 CLAUDE.md 和 TASKS.md，开始执行 Phase 0
```

### 🔥 既有系统直接规划（Build 模式杀手级用法）

在既有专案目录中启动 **直接实作模式**，Claude Code 会一边读取你的 codebase 一边做产品规划 — 等于把**产品规划**和**技术可行性评估**合在同一个流程里完成：

```
你的既有专案                          Product Playbook
┌─────────────────┐                ┌─────────────────────┐
│ src/             │  ← 自动读取 →  │ Pre-mortem 风险评估   │
│ db/schema.sql    │  ← 自动读取 →  │ MVP 范围定义         │
│ api/routes/      │  ← 自动读取 →  │ RICE 功能排序        │
│ package.json     │  ← 自动读取 →  │ User Story 拆解     │
│ CLAUDE.md        │  ← 自动读取 →  │ 开发交接包（增量）    │
└─────────────────┘                └─────────────────────┘
```

**操作范例：**

```bash
# 1. 进入你的既有专案
cd /path/to/your-existing-project

# 2. 启动 Claude Code
claude

# 3. 使用直接实作模式，描述你要加的功能
> /product-build 我想在现有系统加上即时通知功能
```

Claude Code 会自动：
- 扫描你的目录结构、技术栈、DB Schema
- 基于**真实架构**做 Pre-mortem（而不是凭空想像的风险）
- 产出的 MVP 和 User Story 直接对接现有模组
- 开发交接包是**增量规划**，不是从零开始

> 💡 **为什么这很强？** 传统产品规划和技术评估是分开的 — PM 写完企划丢给工程师，工程师才说「这个做不了」。Build 模式让规划过程就建立在真实系统约束之上，省去来回。

### 🔒 安全性内建

开发交接包自动包含安全架构，不再是事后补强：

- **OWASP Top 10 检查清单** — 输入验证、认证授权、XSS/CSRF 防护
- **安全架构段落** — CORS 政策、CSP Headers、Rate Limiting、API 安全中间件
- **.gitignore 模板** — 自动排除 `.env`、credentials、进度文件
- **Pre-mortem 安全情境** — 数据泄漏、帐号盗用、API 滥用等必考项目

### 📦 跨 Session 产品上下文累积

每次规划的成果自动保存到 `.product-context.md`，下次开启时自动载入：

```
第一次规划（完整模式）→ 储存 Identity + Core Strategy + Architecture
第二次规划（功能扩充）→ 自动带入技术栈和模组，省去重复收集
第三次规划（改版模式）→ 带入历史决策和已知痛点，聚焦差异
```

### 🏢 B2B / B2C 自动调整

确认产品类型后，框架自动适配：

| 面向 | B2C | B2B |
|------|-----|-----|
| Persona | 个人动机分群 | 购买者 + 使用者双 Persona |
| PMF | DAU/留存/Sean Ellis | 付费客户数/NRR/NPS |
| North Star | 核心动作完成次数 | ARR / Net Revenue Retention |
| Aha Moment | 首次使用内 | Onboarding / Time-to-Value |

---

## 📊 品质评测结果

通过对比「有 Skill 引导」与「无 Skill 引导」的回应品质，以 AI 评审自动评分，量化 Skill 的实际效益。

### 四次 Iteration 对比

| 评测轮次 | 评测项目数 | 有 Skill 通过率 | 无 Skill 通过率 | 差距（Delta） |
|---------|:--------:|:--------------:|:--------------:|:-----------:|
| Iteration 1（基准） | 6 项 | 100% | 57.4% | +42.6% |
| Iteration 2 | 6 项 | 100% | 63.3% | +36.7% |
| Iteration 3 | 6 项 | 94.1% | 38.2% | +55.9% |
| **Iteration 4（最新）** | **9 项** | **100%** | **31%** | **+69% ✅** |

### Iteration 4 详细结果（9 项评测 × 49 个期望值）

| 评测项目 | 有 Skill | 无 Skill | Delta |
|---------|:-------:|:-------:|:-----:|
| 模式选择（三步渐进） | 100% | 0% | +100% |
| 快速模式 JTBD 分析 | 100% | 43% | +57% |
| JTBD 深度（B2B 组织层级） | 100% | 57% | +43% |
| PR-FAQ 撰写 | 100% | 33% | +67% |
| 改版模式 | 100% | 67% | +33% |
| 品质自检 Hard Gate | 100% | 0% | +100% |
| **功能扩充模式（新）** | **100%** | **17%** | **+83%** |
| **安全性整合（新）** | **100%** | **25%** | **+75%** |
| **Context Bootstrap（新）** | **100%** | **0%** | **+100%** |

### 关键发现

- **品质自检 Hard Gate**（+100%）：AI 在完成产出后，是否会主动以严格标准批判自己的输出、标记不足并要求改进——无 Skill 时通过率为 0%
- **Context Bootstrap**（+100%）：首次使用时是否会先收集产品基础资讯再开始规划，而非直接跳入技术实作——无 Skill 时完全跳过此步骤
- **功能扩充模式**（+83%）：是否能识别「在既有产品上加功能」的场景，启用 4 步精简流程而非完整 7-12 步——无 Skill 时直接输出技术方案
- **安全性整合**（+75%）：开发交接包是否包含安全架构、.gitignore 模板、平台特定安全措施——无 Skill 时安全性仅占一个简表

> 详细评测方法与数据见 [`evals/`](./evals/) 目录。

---

## 💬 可用指令一览

### ⌨️ Claude Code CLI Slash Commands

安装 Skill 后自动可用的主指令：

| 指令 | 说明 |
|------|------|
| `/the-product-playbook` | 启动完整产品规划引导流程 |

如需更细粒度的快捷指令，可安装 `commands/` 数据夹中的预建 slash commands：

```bash
# 安装所有 slash commands
cp -r the-product-playbook/commands/* ~/.claude/commands/
```

| 指令 | 说明 |
|------|------|
| `/product-quick <描述>` | 快速模式 — 30 分钟内跑完 JTBD → PR-FAQ → North Star |
| `/product-full <描述>` | 完整模式 — 完整 20 步产品企划 |
| `/product-revision <描述>` | 改版模式 — 既有产品改版优化 |
| `/product-build <描述>` | 直接实作模式 — 跳过 Discovery，直接进解法 |
| `/product-prd` | 产出 PRD 工程师交付包 |
| `/product-report` | 产出 HTML 企划报告 |
| `/product-dev` | 产出开发交接包（CLAUDE.md + TASKS.md + TICKETS.md） |

### 💬 对话中的自然语言指令

#### 流程控制
- `切换到 [框架]` — 立即切换框架
- `跳过这个步骤` — 跳过当前步骤
- `回到 [步骤名]` — 回到任意步骤修改
- `帮我简化` / `帮我展开` — 调整深度

#### 产出指令
- `产出报告` — HTML 企划报告
- `产出 PRD` — 工程师交付包（含流程图 + DB Schema + Wireframe）
- `产出简报` — PowerPoint 简报
- `进入开发` — 开发交接包（CLAUDE.md + TASKS.md）

#### 分析指令
- `帮我做完整性评估` — 评估规划完整度
- `帮我找出假设` — 列出未验证假设
- `做一次 Pre-mortem` — 事前验尸
- `这个产品在 PMF 哪个等级？` — PMF 判断
- `帮我找出瓶颈` — Aha Moment 障碍分析

---

## 🤝 Contributing

欢迎贡献！以下是几个特别欢迎的方向：

- 🌍 **多语言支持** — 将框架翻译为其他语言
- 📐 **新增框架** — 加入更多产品管理框架
- 📝 **范例补充** — 在各框架中加入更多填写范例
- 🐛 **Bug 回报** — 使用过程中发现的逻辑问题或遗漏
- 💡 **体验改善** — 互动流程、指令设计的改善建议

### 如何贡献

1. Fork 本 repo
2. 建立你的 feature branch (`git checkout -b feature/amazing-framework`)
3. Commit (`git commit -m 'feat: add amazing framework'`)
4. Push (`git push origin feature/amazing-framework`)
5. 开启 Pull Request

### 贡献指南

- reference 文件中的框架内容必须注明出处
- 新增框架需同步更新 SKILL.md 的框架索引和步骤序列
- 品质自检清单使用 ✅ / ❌ 格式
- 支持多语言：简体中文、繁体中文、英文等多语言并行维护

---

## 📚 框架来源与延伸学习

本专案的框架整理自以下思想家的公开内容：

| 思想家 | 核心贡献 | 推荐阅读 |
|--------|---------|---------|
| Teresa Torres | Continuous Discovery、OST | 《Continuous Discovery Habits》 |
| Shreyas Doshi | LNO、Pre-mortem、三层次产品工作 | Lenny's Podcast Ep.3 |
| Gibson Biddle | DHM Model、GEM | Lenny's Podcast |
| April Dunford | Positioning Framework | 《Obviously Awesome》 |
| Todd Jackson | 四级 PMF、Four P's | Lenny's Podcast |
| Richard Rumelt | Good Strategy / Bad Strategy | 《Good Strategy Bad Strategy》 |
| Marty Cagan | Empowered Teams | 《Inspired》《Empowered》 |
| Clayton Christensen | Jobs to Be Done | 《Competing Against Luck》 |
| Amazon | Working Backwards / PR-FAQ | 《Working Backwards》 |
| Sean Ellis | Sean Ellis Score、Growth | 《Hacking Growth》 |
| Lenny Rachitsky | Shape / Ship / Synchronize | Lenny's Newsletter + Podcast |

---

## 📄 License

本专案采用 [MIT License](LICENSE) 授权 — 免费使用、修改、分发，不设限。

---

## ⭐ Star History

如果这个专案对你有帮助，请给个 ⭐ 让更多人看到！

---

<p align="center">
  <strong>Built with ❤️ for Product Managers who want to build things that matter.</strong>
</p>

---

Copyright (c) 2026 Charles Chen.
