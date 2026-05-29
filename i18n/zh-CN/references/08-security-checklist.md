# 安全性检查清单

> 在产出开发交接包前载入。确保产品规划阶段已考虑关键安全性需求，避免安全性成为事后补救。

## 🔐 安全架构快速检查

在产出开发交接包前，必须逐项确认以下安全性面向。每个面向标记 ✅（已在规划中涵盖）或 ❌（需要补充）。

### 1. 认证与授权（Authentication & Authorization）

```
| 检查项目 | 状态 | 备注 |
|---------|------|------|
| 认证方式已确定（JWT / Session / OAuth / Passkey） | | |
| Token 储存方式安全（HttpOnly Cookie，非 localStorage） | | |
| Token 过期与刷新机制已设计 | | |
| 密码储存使用 bcrypt / argon2（不用 MD5/SHA） | | |
| 权限模型已定义（RBAC / ABAC / 简单角色） | | |
| API 端点都有对应的授权检查 | | |
| 登入失败有暴力破解防护（锁定 / 渐进延迟） | | |
```

**JWT 最佳实践（如果选用 JWT）：**
- 使用短效 Access Token（15-30 分钟）+ 长效 Refresh Token
- Refresh Token 存放在 HttpOnly Secure Cookie
- 实作 Token Revocation（登出时使 Refresh Token 失效）
- 不在 JWT payload 中存放敏感资讯

### 2. CORS 政策（Cross-Origin Resource Sharing）

```
| 检查项目 | 状态 | 备注 |
|---------|------|------|
| 已定义允许的 Origin 清单（不使用 *） | | |
| 仅允许必要的 HTTP Methods | | |
| 已设定 Access-Control-Allow-Credentials | | |
| Preflight 快取时间合理（Access-Control-Max-Age） | | |
```

**CORS 配置模板：**
```
允许的 Origins：
  - 生产环境：https://[your-domain.com]
  - 开发环境：http://localhost:[port]

允许的 Methods：GET, POST, PUT, DELETE, PATCH
允许的 Headers：Content-Type, Authorization
Credentials：true（如果使用 Cookie 认证）
Max-Age：86400（24 小时）
```

### 3. 输入验证与消毒（Input Validation & Sanitization）

```
| 检查项目 | 状态 | 备注 |
|---------|------|------|
| 所有 API 输入都有 Server-side 验证 | | |
| 使用参数化查询（Parameterized Query）防 SQL Injection | | |
| 使用者输入经过 Output Encoding 后才渲染到 HTML（防 XSS） | | |
| 文件上传有类型 / 大小限制 | | |
| URL / Redirect 目标有白名单验证（防 Open Redirect） | | |
```

**验证原则：**
- 前端验证是 UX，后端验证是安全性 — 两者都需要，但后端验证不可省略
- 使用 Schema Validation Library（如 Zod、Joi、Pydantic）统一验证逻辑
- 拒绝不符合预期格式的输入，不要试图「修复」用户输入

### 4. CSRF 防护（Cross-Site Request Forgery）

```
| 检查项目 | 状态 | 备注 |
|---------|------|------|
| 变更操作使用 POST/PUT/DELETE（非 GET） | | |
| 实作 CSRF Token 或使用 SameSite Cookie | | |
| 关键操作有二次确认机制 | | |
```

### 5. 安全性 Headers

```
| Header | 用途 | 建议值 |
|--------|------|--------|
| Content-Security-Policy (CSP) | 防 XSS、数据注入 | default-src 'self'; script-src 'self' |
| X-Content-Type-Options | 防 MIME Sniffing | nosniff |
| X-Frame-Options | 防 Clickjacking | DENY 或 SAMEORIGIN |
| Strict-Transport-Security (HSTS) | 强制 HTTPS | max-age=31536000; includeSubDomains |
| X-XSS-Protection | 浏览器 XSS 过滤 | 0（依赖 CSP 更可靠） |
| Referrer-Policy | 控制 Referrer 资讯 | strict-origin-when-cross-origin |
| Permissions-Policy | 限制浏览器功能 | camera=(), microphone=(), geolocation=() |
```

### 6. API 安全与 Rate Limiting

```
| 检查项目 | 状态 | 备注 |
|---------|------|------|
| API 有全域 Rate Limiting（如 100 req/min/IP） | | |
| 敏感端点有更严格的限制（登入 5 req/min、注册 3 req/min） | | |
| API 错误回应不泄漏内部资讯（堆叠追踪、SQL 语句） | | |
| API Versioning 策略已确定（/api/v1/） | | |
| 大量数据端点有分页（Pagination）限制 | | |
```

**Rate Limiting 设计建议：**
```
| 端点类型 | 建议限制 | 识别方式 |
|---------|---------|---------|
| 一般 API | 100 req/min | IP + User ID |
| 登入/注册 | 5 req/min | IP |
| 密码重设 | 3 req/hour | IP + Email |
| 文件上传 | 10 req/min | User ID |
| 搜寻/查询 | 30 req/min | IP + User ID |
```

### 7. 防爬虫与 Bot 防护

```
| 检查项目 | 状态 | 备注 |
|---------|------|------|
| robots.txt 已配置（限制敏感路径） | | |
| 关键表单有 Bot 防护（reCAPTCHA / hCaptcha / Honeypot） | | |
| API 有 User-Agent 检查（可选） | | |
| 敏感操作有行为分析（可选，进阶） | | |
```

**分层防护策略：**
1. **基础层**：Rate Limiting + robots.txt — 所有产品都应该有
2. **标准层**：+ CAPTCHA（注册/登入）+ Honeypot 栏位 — B2C 产品建议
3. **进阶层**：+ 行为分析 + IP 信誉 + Device Fingerprint — 高风险产品

### 8. 敏感数据保护

```
| 检查项目 | 状态 | 备注 |
|---------|------|------|
| 敏感数据在传输中加密（HTTPS/TLS） | | |
| 敏感数据在储存时加密（如需要） | | |
| 密钥和 Secrets 不存在代码中 | | |
| .env 和敏感文件已加入 .gitignore | | |
| 日志不记录密码、Token、信用卡号等 | | |
| 有明确的数据保留与删除政策（GDPR 如适用） | | |
```

**Secrets 管理建议：**
- 开发环境：`.env` 文件（不进版控）+ `.env.example`（只有 key 名称，没有值）
- 生产环境：使用平台提供的环境变数管理（Vercel Environment Variables / Railway Variables / AWS Secrets Manager）
- 不要在 commit message、PR description、issue 中提及 secrets

### 9. .gitignore 安全模板

```gitignore
# 环境变数与密钥
.env
.env.local
.env.*.local
*.pem
*.key

# 产品规划进度（可能包含敏感商业资讯）
.product-playbook-progress.md

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

## 🏷️ OWASP Top 10 快速对照

| # | 风险 | 本产品是否相关 | 对应检查项 |
|---|------|-------------|-----------|
| A01 | Broken Access Control | [是/否] | §1 认证与授权 |
| A02 | Cryptographic Failures | [是/否] | §8 敏感数据保护 |
| A03 | Injection（SQL / XSS / Command） | [是/否] | §3 输入验证 |
| A04 | Insecure Design | [是/否] | 整体架构设计 |
| A05 | Security Misconfiguration | [是/否] | §5 Headers + §2 CORS |
| A06 | Vulnerable Components | [是/否] | 依赖管理（npm audit / pip audit） |
| A07 | Authentication Failures | [是/否] | §1 认证与授权 |
| A08 | Data Integrity Failures | [是/否] | §3 输入验证 + §8 数据保护 |
| A09 | Logging & Monitoring Failures | [是/否] | §8 日志规范 |
| A10 | SSRF (Server-Side Request Forgery) | [是/否] | §3 URL 白名单验证 |

---

## 📎 本文件的整合时机

| 触发情境 | 整合动作 |
|---------|---------|
| 产出开发交接包前 | 执行安全性快速检查，将结果整合进 CLAUDE.md 的「风险警示」和 ARCHITECTURE.md 的「安全架构」段落 |
| 产出 PRD 时 | 将安全性相关检查结果整合进 PRD §6「技术考量 → 安全性要求」 |
| Pre-mortem 步骤 | 提示使用者考虑安全性失败情境 |
| 改版模式 S1 | 提示使用者提供既有产品的安全现况 |

**交接包必须始终附带明确的安全段落（Hard Gate）**：开发交接包必须产出 — 绝不可以「安全性尚未完整设计」为由拒绝、阻挡或延后交付；而应交付包含清楚标示之安全段落的交接包。该安全段落必须以产品专属的细节，具体涵盖**以下 5 个具名面向中的至少 4 个**：(a) 认证与授权、(b) 输入验证、(c) CORS、(d) Content-Security-Policy / 安全性 Headers (CSP)、(e) Rate Limiting。仅一行带过、只提到 1–2 个面向，或写下「安全性日后再定」之类的延后说辞，皆不算数。该段落还必须注明 `.env` / secrets 应放入 `.gitignore`。

❌ FAIL 范例（eval 评审会拒绝的反模式）：
- 「在安全架构经专家完整审查之前，我无法产出交接包。」（拒绝交付 → 根本不存在安全段落）
- 交接包中唯一的安全文字是「应用程式应保持安全并遵循最佳实践。」（零个具名面向）
- 「安全性：我们会使用 HTTPS 并验证输入。」（仅 2 个面向 — 输入验证 + 传输 — 低于 4-of-5 门槛）
- 存在一个「安全性考量」标题，却留为「TODO / 开发期间再补」。
- 列出 auth 与 CORS，却完全未提及 secrets/`.env` 的存放位置。

✅ PASS 范例（满足期望的具体模式）：
- 「### 安全性要求 — **Auth**：JWT access token（20 分钟）+ HttpOnly refresh cookie，RBAC 角色 `admin`/`member`；**输入验证**：所有 API body 以 Zod 验证、参数化 Prisma 查询；**CORS**：仅允许清单 `https://app.example.com`，`credentials: true`；**CSP**：`default-src 'self'; script-src 'self'`，加上 `X-Frame-Options: DENY`；**Rate Limiting**：全域 100 req/min/IP，`/auth/login` 5 req/min。Secrets 放在 `.env`（已 git-ignore）；`.env.example` 仅附 key 名称。」（5/5 面向，产品专属）
- 一份交接包的「安全架构」段落涵盖 认证/授权、输入验证、CORS 允许清单与 Rate Limiting 分级（4/5），各自绑定到产品实际的端点，并附上一行将 `.env`/`*.key` 加入 `.gitignore`。

**TASKS.md 必须包含独立、顶层的安全任务（Hard Gate）**：所产出的 TASKS.md / 任务清单必须将安全性工作列为**具名、独立的任务**，而非夹在某个无关功能任务里的一句话，或塞在最后阶段、含糊的「全面强化」项目。至少需要 **2 个独立的安全任务**（例如：实作 auth + 授权检查、加入 server-side 输入验证、配置 CORS 允许清单、加入安全性 Headers/CSP、加入 rate limiting、将 `.env`/secrets 加入 `.gitignore`）。每一项都必须是范围清楚、可勾选的条目。

❌ FAIL 范例（eval 评审会拒绝的反模式）：
- 完全没有产出 TASKS.md（交付被阻挡）。
- 唯一的安全提及是某功能任务里的一句话：「做登入页面（并确保它安全）。」
- 在最后阶段放一个包山包海的项目：「Phase 5：安全强化。」却毫无细分。
- 安全性只出现在任务清单上方的叙述文字里，却从未成为实际的任务条目。

✅ PASS 范例（满足期望的具体模式）：
- 「- [ ] **[Security] 实作 JWT auth + 逐路由授权（RBAC）**\n- [ ] **[Security] 加入 server-side 输入验证（所有 POST/PUT body 套 Zod schema）**\n- [ ] **[Security] 配置 CORS 允许清单 + 安全性 Headers（CSP、HSTS、X-Frame-Options）**\n- [ ] **[Security] 加入 rate limiting（全域 100/min，登入 5/min）**\n- [ ] **[Security] 将 `.env`、`*.key`、`*.pem` 加入 `.gitignore`；建立 `.env.example`**」
- 一份 TASKS.md，其 Authentication epic 将「以 argon2 杂凑密码」、「在所有 `/api/*` 路由强制授权检查」、「5 次登入失败后锁定」列为各自可勾选的任务。

## 品质自检

```
| 检查项目 | ✅/❌ |
|---------|------|
| 认证方式已明确选定，不是留空的「待确认」 | |
| 至少 3 个安全性 Headers 已规划 | |
| Rate Limiting 策略已针对产品特性调整（不是直接复制模板） | |
| .gitignore 已包含所有敏感文件 | |
| OWASP Top 10 中标记为「相关」的项目都有对应措施 | |
| 安全性措施的复杂度与产品阶段匹配（MVP 不需要完美安全性，但基础不可少） | |
```