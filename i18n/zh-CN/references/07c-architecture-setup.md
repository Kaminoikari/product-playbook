# 开发衔接 — ARCHITECTURE.md + setup.sh

## 📄 ARCHITECTURE.md 模板

```markdown
# [产品名称] — 技术架构

## 目录结构

[根据技术栈产出对应的目录结构]

## 数据库设计

[从 PRD 的 DB Schema 整合，转为建表 SQL 或 ORM Model 定义]

### ER 关系图

[Mermaid erDiagram]

### 关键 Table 说明

| Table | 说明 | 关键栏位 | 索引建议 |
|-------|------|---------|---------|
| | | | |

## API 设计

[根据 User Story 和功能规格，定义 RESTful API endpoints 或 GraphQL schema]

### Endpoints 清单

| 方法 | 路径 | 说明 | 对应 Task |
|------|------|------|----------|
| GET | /api/v1/[resource] | [说明] | T1.1 |
| POST | /api/v1/[resource] | [说明] | T1.2 |

### 认证方式

[JWT / Session / OAuth 等]

## 第三方服务

| 服务 | 用途 | 对应功能 |
|------|------|---------|
| | | |

## 安全架构

### CORS 配置

| 设定项 | 值 | 说明 |
|--------|---|------|
| 允许的 Origins | [生产域名, localhost:port] | 不使用 wildcard * |
| 允许的 Methods | GET, POST, PUT, DELETE | 依 API 实际需求 |
| 允许的 Headers | Content-Type, Authorization | |
| Credentials | true/false | 依认证方式决定 |

### 安全性 Headers

[根据产品需求，从 references/08-security-checklist.md §5 选择适用的 Headers]

### Rate Limiting 策略

| 端点类型 | 限制 | 识别方式 |
|---------|------|---------|
| 一般 API | [X] req/min | IP + User ID |
| 登入/注册 | [X] req/min | IP |
| 文件上传 | [X] req/min | User ID |

### 敏感数据处理

- 密钥管理：[.env + 平台环境变数 / Secrets Manager]
- 日志规范：不记录密码、Token、个人数据
- 数据加密：[传输中 TLS / 储存时加密需求]

> 完整安全性检查清单见 `references/08-security-checklist.md`
```

---

## 📄 .gitignore 模板

```gitignore
# 环境变数与密钥
.env
.env.local
.env.*.local
*.pem
*.key

# 产品规划进度（可能包含敏感商业资讯）
.product-playbook-progress.md
# Product-playbook 开发交接标记（session-local，请勿 commit）
.product-dev-active

# IDE 与作业系统
.idea/
.vscode/
*.swp
.DS_Store
Thumbs.db

# 依赖
node_modules/
__pycache__/
*.pyc
venv/

# 构建产出
dist/
build/
.next/
```

---

## 📄 setup.sh 模板

```bash
#!/bin/bash
# [产品名称] — 专案初始化脚本
# 使用方式：chmod +x scripts/setup.sh && ./scripts/setup.sh

set -e

echo "🚀 正在初始化 [产品名称]..."

# ===== 检查前置条件 =====
command -v [node/python/etc] >/dev/null 2>&1 || { echo "❌ 需要安装 [runtime]"; exit 1; }

# ===== 安装依赖 =====
echo "📦 安装依赖..."
[npm install / pip install -r requirements.txt / etc]

# ===== 环境设定 =====
if [ ! -f .env ]; then
  echo "📝 建立 .env 文件..."
  cp .env.example .env
  echo "⚠️  请编辑 .env 填入必要的环境变数"
fi

# ===== 数据库初始化 =====
echo "🗄️  初始化数据库..."
[migration commands]

echo ""
echo "✅ 初始化完成！"
echo ""
echo "下一步："
echo "  1. 编辑 .env 填入环境变数"
echo "  2. 启动开发服务器：[start command]"
echo "  3. 开始开发：claude \"请读取 CLAUDE.md 和 TASKS.md，开始执行 Phase 1\""
```

---

## 使用者引导文字

### 在 Claude Chat / Cowork 中

产出开发交接包后，显示以下引导：

```
📦 开发交接包已准备好！包含以下文件：

  CLAUDE.md        → Claude Code 的专案记忆（产品上下文 + 技术规范）
  TASKS.md         → 开发任务清单（4 个 Phase，共 [N] 个 Task）
  TICKETS.md       → 开票清单（共 [N] 张票，可直接在 Jira/Asana/Linear 开票）
  docs/PRD.md      → 完整 PRD
  docs/ARCHITECTURE.md → 技术架构（DB schema + API + 目录结构）
  docs/PRODUCT-SPEC.md → 产品规格摘要
  scripts/setup.sh → 一键初始化脚本

🔗 如何开始开发：

  1. 下载并解压到你的专案数据夹
  2. 开启终端机，进入专案数据夹
  3. 启动 Claude Code：
     $ claude
  4. 告诉 Claude Code 开始：
     > 请读取 CLAUDE.md 和 TASKS.md，开始执行 Phase 0

💡 小提示：
  - Claude Code 会自动读取 CLAUDE.md，所以它已经知道整个产品上下文
  - 每个 Phase 完成后，它会询问你是否要进入下一个 Phase
  - 如果要调整功能范围，直接修改 TASKS.md 即可
  - CLAUDE.md 中的「明确不做」清单会防止 Claude Code 做超出范围的事
```

### 产出前的最终确认

```
在产出开发交接包前，我需要确认几件事：

1. 技术栈：[已确认 / 需要确认]
2. 产品名称（用于专案数据夹名称）：[已确认 / 需要确认]
3. 是否有其他技术限制或偏好？
   - 例如：必须用某个 ORM、需要支持特定浏览器、有既有的 CI/CD 等
```
