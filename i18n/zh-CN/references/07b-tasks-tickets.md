# 开发衔接 — TASKS.md + TICKETS.md

## 📄 TASKS.md 模板

功能拆解的核心原则：
- 从 MVP 必须有（P0）的功能出发
- 每个 Task 对应一个 User Story
- Phase 之间有明确的依赖关系：Phase N+1 依赖 Phase N 的产出
- 每个 Task 包含验收标准，Claude Code 可以自我检查

```markdown
# [产品名称] — 开发任务清单

## Phase 0：专案初始化
> 目标：建立可运行的空白专案骨架

- [ ] **T0.1** 初始化专案（`scripts/setup.sh` 或手动）
  - 验收：
    - [ ] `npm run dev` / `python manage.py runserver` 等指令可启动
    - [ ] `.gitignore` 已建立，包含 `.env`、`.env.local`、`node_modules/`、`.product-playbook-progress.md`、`.product-dev-active` 等敏感文件
    - [ ] `.env.example` 已建立（只有 key 名称，没有实际值）
- [ ] **T0.2** 设定 linter + formatter
  - 验收：lint 通过无错误
- [ ] **T0.3** 建立数据库 + 执行初始 migration
  - 验收：数据库可连接，基础 table 已建立
- [ ] **T0.4** 建立基础路由结构
  - 验收：所有主要页面路由可访问（返回空白页面即可）

## Phase 1：核心流程（Aha Moment 路径）
> 目标：让用户可以走完从进入到 Aha Moment 的最短路径
> 对应 User Story：[US-001, US-002, ...]

- [ ] **T1.1** [功能名称]
  - User Story：身为 [Persona]，我想要 [行为]，以便 [价值]
  - 验收标准：
    - [ ] [可测试的具体条件 1]
    - [ ] [可测试的具体条件 2]
  - 技术备注：[需要的 API / 第三方服务 / 特殊逻辑]

- [ ] **T1.2** [功能名称]
  - User Story：...
  - 验收标准：...

> **Phase 1 完成检查点**：用户可以完成 [Aha Moment 行为]。如果不行，不要进入 Phase 2。

## Phase 2：完整 MVP
> 目标：补全 MVP 范围中所有 P0 功能
> 对应 User Story：[US-003, US-004, ...]

- [ ] **T2.1** [功能名称]
  - ...

> **Phase 2 完成检查点**：所有 P0 User Story 的验收标准都通过。

## Phase 3：品质与体验
> 目标：错误处理、边界情境、载入状态、基础安全性

- [ ] **T3.1** 全域错误处理
- [ ] **T3.2** 表单验证 + 边界情境
- [ ] **T3.3** 载入状态 + 空状态
- [ ] **T3.4** 安全性检查（依 `references/08-security-checklist.md` 逐项确认）
  - 验收：
    - [ ] OWASP Top 10 相关项目已处理（输入验证、认证、XSS 防护、CSRF 防护）
    - [ ] 安全性 Headers 已设定（CSP、X-Frame-Options、HSTS 等）
    - [ ] CORS 政策已配置（不使用 wildcard *）
    - [ ] 敏感 API 端点有 Rate Limiting
    - [ ] API 错误回应不泄漏内部资讯
- [ ] **T3.5** 响应式设计（如果是 Web）

## Phase 4：部署
> 目标：可以让外部用户访问

- [ ] **T4.1** 环境变数管理
- [ ] **T4.2** 部署配置
- [ ] **T4.3** 基础监控 + 日志
```

---

## 📄 TICKETS.md 模板

TICKETS.md 是根据 TASKS.md 中的功能拆解，产出可直接在专案管理工具中开票的结构化内容。每张票包含 PM 开票所需的完整资讯。

> **设计目标**：PM 可以直接将每张票的内容复制到 Jira / Asana / Linear 等工具中开票，后续版本将支持通过 API 自动开票。

```markdown
# [产品名称] — 开票清单

> 产出时间：[时间戳]
> 对应 TASKS.md 版本：[版本/时间]
> 共 [N] 张票

---

## 票务总览

| 票号 | 标题 | Phase | 优先级 | 预估工时 | 依赖 |
|------|------|-------|--------|---------|------|
| TKT-001 | [标题] | Phase 0 | P0 | [X]h | — |
| TKT-002 | [标题] | Phase 1 | P0 | [X]h | TKT-001 |
| ... | | | | | |

---

## TKT-001：[标题]

**Phase**：Phase 0 — 专案初始化
**对应 Task**：T0.1
**优先级**：P0
**预估工时**：[X] 小时
**依赖**：无
**指派对象**：[角色/团队，例如：后端工程师]

### 描述

[用 1-3 段文字描述这张票要完成什么，包含业务背景和技术目标]

### User Story

身为 [Persona]，我想要 [行为]，以便 [价值]

### 验收标准

- [ ] [可测试的具体条件 1]
- [ ] [可测试的具体条件 2]
- [ ] [可测试的具体条件 3]

### 技术备注

- [实作注意事项]
- [需要的 API / 第三方服务]
- [相关文件路径或模组]

### 标签建议

`[Phase 0]` `[backend]` `[setup]`

---

## TKT-002：[标题]

[同上格式，逐张展开]
```

### 开票规则

1. **票号对应 Task**：每个 TASKS.md 中的 Task 对应一张票（TKT-001 ↔ T0.1），粒度过大的 Task 可拆为多张票
2. **优先级继承**：Phase 0-1 默认 P0，Phase 2 默认 P1，Phase 3-4 默认 P2，可根据 RICE 分数调整
3. **依赖关系**：明确标记票与票之间的前后依赖，避免工程师跳步开发
4. **预估工时**：根据 Task 粒度原则（1-4 小时），提供合理预估
5. **标签建议**：包含 Phase、技术领域（frontend / backend / database / infra）、功能模组

### 专案管理工具串接（预留）

> 以下为未来自动开票功能的预留接口设计，目前版本仅产出 TICKETS.md 供 PM 手动开票。

TICKETS.md 的结构化格式已预留以下栏位，便于后续通过 API 自动汇入：

| 栏位 | Jira 对应 | Asana 对应 | Linear 对应 |
|------|----------|-----------|------------|
| 票号 | Issue Key | Task ID | Issue ID |
| 标题 | Summary | Task Name | Title |
| 描述 | Description | Description | Description |
| 优先级 | Priority | Custom Field | Priority |
| 预估工时 | Story Points / Time Estimate | Custom Field | Estimate |
| 依赖 | Linked Issues | Dependencies | Relations |
| 标签 | Labels + Components | Tags | Labels |
| Phase | Epic | Section | Project |
| 指派对象 | Assignee | Assignee | Assignee |
| 验收标准 | Acceptance Criteria (Description) | Subtasks | Sub-issues |

---

## 功能拆解逻辑

将 MVP 功能转换为 Task 的规则：

### Phase 划分原则

```
Phase 0：专案骨架（所有模式都必须有）
  → 初始化、linter、DB、基础路由

Phase 1：Aha Moment 最短路径（最重要）
  → 从用户进入到达 Aha Moment 所需的最少功能
  → 只包含这条路径上的 P0 功能

Phase 2：完整 MVP
  → 补全 Phase 1 没有覆盖的其他 P0 功能
  → 支线流程、次要页面

Phase 3：品质与体验
  → 错误处理、边界情境、载入/空状态
  → 安全性基础、响应式设计

Phase 4：部署
  → 环境变数、部署配置、监控
```

### Task 粒度原则

- 每个 Task 应该可以在 **1-4 小时** 内完成
- 太大 → 拆成子 Task（T1.1a, T1.1b）
- 太小 → 合并到相关 Task
- 每个 Task 必须有至少一个可测试的验收标准

### User Story → Task 对应

```
一个 User Story 可能对应 1-3 个 Task：
  US-001: 身为新用户，我想要注册帐号，以便开始使用
    → T1.1: 注册页面 UI
    → T1.2: 注册 API + 数据验证
    → T1.3: Email 验证流程（如果 MVP 需要）
```
