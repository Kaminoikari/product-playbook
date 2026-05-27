# Security Checklist

> Loaded before producing the development handoff package. Ensures that critical security requirements are considered during the product planning phase, preventing security from becoming an afterthought.

## 🔐 Security Architecture Quick Check

Before producing the development handoff package, verify each of the following security aspects. Mark each as ✅ (covered in planning) or ❌ (needs to be added).

### 1. Authentication & Authorization

```
| Check Item | Status | Notes |
|-----------|--------|-------|
| Authentication method determined (JWT / Session / OAuth / Passkey) | | |
| Token storage is secure (HttpOnly Cookie, not localStorage) | | |
| Token expiration and refresh mechanism designed | | |
| Password storage uses bcrypt / argon2 (not MD5/SHA) | | |
| Permission model defined (RBAC / ABAC / simple roles) | | |
| All API endpoints have corresponding authorization checks | | |
| Login failures have brute-force protection (lockout / progressive delay) | | |
```

**JWT Best Practices (if using JWT):**
- Use short-lived Access Tokens (15-30 minutes) + long-lived Refresh Tokens
- Store Refresh Tokens in HttpOnly Secure Cookies
- Implement Token Revocation (invalidate Refresh Token on logout)
- Do not store sensitive information in the JWT payload

### 2. CORS Policy (Cross-Origin Resource Sharing)

```
| Check Item | Status | Notes |
|-----------|--------|-------|
| Allowed Origin list defined (no wildcard *) | | |
| Only necessary HTTP methods are allowed | | |
| Access-Control-Allow-Credentials configured | | |
| Preflight cache duration is reasonable (Access-Control-Max-Age) | | |
```

**CORS Configuration Template:**
```
Allowed Origins:
  - Production: https://[your-domain.com]
  - Development: http://localhost:[port]

Allowed Methods: GET, POST, PUT, DELETE, PATCH
Allowed Headers: Content-Type, Authorization
Credentials: true (if using cookie-based auth)
Max-Age: 86400 (24 hours)
```

### 3. Input Validation & Sanitization

```
| Check Item | Status | Notes |
|-----------|--------|-------|
| All API inputs have server-side validation | | |
| Parameterized queries used to prevent SQL Injection | | |
| User input is output-encoded before rendering to HTML (XSS prevention) | | |
| File uploads have type / size restrictions | | |
| URL / redirect targets have whitelist validation (Open Redirect prevention) | | |
```

**Validation Principles:**
- Frontend validation is UX; backend validation is security — both are needed, but backend validation is non-negotiable
- Use a Schema Validation Library (e.g., Zod, Joi, Pydantic) for unified validation logic
- Reject inputs that don't match expected formats — don't try to "fix" user input

### 4. CSRF Protection (Cross-Site Request Forgery)

```
| Check Item | Status | Notes |
|-----------|--------|-------|
| State-changing operations use POST/PUT/DELETE (not GET) | | |
| CSRF Token implemented or SameSite Cookie used | | |
| Critical operations have secondary confirmation | | |
```

### 5. Security Headers

```
| Header | Purpose | Recommended Value |
|--------|---------|-------------------|
| Content-Security-Policy (CSP) | Prevent XSS, data injection | default-src 'self'; script-src 'self' |
| X-Content-Type-Options | Prevent MIME sniffing | nosniff |
| X-Frame-Options | Prevent clickjacking | DENY or SAMEORIGIN |
| Strict-Transport-Security (HSTS) | Enforce HTTPS | max-age=31536000; includeSubDomains |
| X-XSS-Protection | Browser XSS filter | 0 (relying on CSP is more reliable) |
| Referrer-Policy | Control referrer information | strict-origin-when-cross-origin |
| Permissions-Policy | Restrict browser features | camera=(), microphone=(), geolocation=() |
```

### 6. API Security & Rate Limiting

```
| Check Item | Status | Notes |
|-----------|--------|-------|
| API has global rate limiting (e.g., 100 req/min/IP) | | |
| Sensitive endpoints have stricter limits (login 5 req/min, register 3 req/min) | | |
| API error responses don't leak internal details (stack traces, SQL statements) | | |
| API versioning strategy determined (/api/v1/) | | |
| Bulk data endpoints have pagination limits | | |
```

**Rate Limiting Design Recommendations:**
```
| Endpoint Type | Recommended Limit | Identification Method |
|--------------|-------------------|----------------------|
| General API | 100 req/min | IP + User ID |
| Login/Register | 5 req/min | IP |
| Password Reset | 3 req/hour | IP + Email |
| File Upload | 10 req/min | User ID |
| Search/Query | 30 req/min | IP + User ID |
```

### 7. Anti-Scraping & Bot Protection

```
| Check Item | Status | Notes |
|-----------|--------|-------|
| robots.txt configured (restrict sensitive paths) | | |
| Critical forms have bot protection (reCAPTCHA / hCaptcha / Honeypot) | | |
| API has User-Agent checks (optional) | | |
| Sensitive operations have behavioral analysis (optional, advanced) | | |
```

**Layered Protection Strategy:**
1. **Basic layer**: Rate Limiting + robots.txt — Every product should have this
2. **Standard layer**: + CAPTCHA (registration/login) + Honeypot fields — Recommended for B2C products
3. **Advanced layer**: + Behavioral analysis + IP reputation + Device Fingerprint — High-risk products

### 8. Sensitive Data Protection

```
| Check Item | Status | Notes |
|-----------|--------|-------|
| Sensitive data encrypted in transit (HTTPS/TLS) | | |
| Sensitive data encrypted at rest (if required) | | |
| Secrets and keys not stored in code | | |
| .env and sensitive files added to .gitignore | | |
| Logs don't record passwords, tokens, credit card numbers, etc. | | |
| Clear data retention and deletion policy (GDPR if applicable) | | |
```

**Secrets Management Recommendations:**
- Development: `.env` file (not in version control) + `.env.example` (key names only, no values)
- Production: Use platform-provided env var management (Vercel Environment Variables / Railway Variables / AWS Secrets Manager)
- Never mention secrets in commit messages, PR descriptions, or issues

### 9. .gitignore Security Template

```gitignore
# Environment variables and secrets
.env
.env.local
.env.*.local
*.pem
*.key

# Product planning progress (may contain sensitive business information)
.product-playbook-progress.md

# IDE and OS
.idea/
.vscode/
*.swp
.DS_Store
Thumbs.db

# Dependencies
node_modules/
__pycache__/
*.pyc
venv/

# Build output
dist/
build/
.next/
```

---

## 🏷️ OWASP Top 10 Quick Reference

| # | Risk | Relevant to This Product? | Corresponding Check |
|---|------|--------------------------|-------------------|
| A01 | Broken Access Control | [Yes/No] | §1 Authentication & Authorization |
| A02 | Cryptographic Failures | [Yes/No] | §8 Sensitive Data Protection |
| A03 | Injection (SQL / XSS / Command) | [Yes/No] | §3 Input Validation |
| A04 | Insecure Design | [Yes/No] | Overall architecture design |
| A05 | Security Misconfiguration | [Yes/No] | §5 Headers + §2 CORS |
| A06 | Vulnerable Components | [Yes/No] | Dependency management (npm audit / pip audit) |
| A07 | Authentication Failures | [Yes/No] | §1 Authentication & Authorization |
| A08 | Data Integrity Failures | [Yes/No] | §3 Input Validation + §8 Data Protection |
| A09 | Logging & Monitoring Failures | [Yes/No] | §8 Logging rules |
| A10 | SSRF (Server-Side Request Forgery) | [Yes/No] | §3 URL whitelist validation |

---

## 📎 Integration Timing

| Trigger | Integration Action |
|---------|-------------------|
| Before producing the dev handoff package | Run the security quick check, integrate results into CLAUDE.md "Risk Alerts" and ARCHITECTURE.md "Security Architecture" sections |
| When producing the PRD | Integrate security check results into PRD §6 "Technical Considerations → Security Requirements" |
| Pre-mortem step | Prompt the user to consider security failure scenarios |
| Revision mode S1 | Prompt the user to provide the existing product's current security posture |

## Quality Self-Check

```
| Check Item | ✅/❌ |
|-----------|------|
| Authentication method explicitly chosen, not left as "TBD" | |
| At least 3 security headers planned | |
| Rate limiting strategy tailored to product characteristics (not just copied from template) | |
| .gitignore includes all sensitive files | |
| All OWASP Top 10 items marked "relevant" have corresponding measures | |
| Security measure complexity matches the product stage (MVP doesn't need perfect security, but the basics are non-negotiable) | |
```
