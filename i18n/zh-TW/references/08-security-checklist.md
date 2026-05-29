# 安全性檢查清單

> 在產出開發交接包前載入。確保產品規劃階段已考慮關鍵安全性需求，避免安全性成為事後補救。

## 🔐 安全架構快速檢查

在產出開發交接包前，必須逐項確認以下安全性面向。每個面向標記 ✅（已在規劃中涵蓋）或 ❌（需要補充）。

### 1. 認證與授權（Authentication & Authorization）

```
| 檢查項目 | 狀態 | 備註 |
|---------|------|------|
| 認證方式已確定（JWT / Session / OAuth / Passkey） | | |
| Token 儲存方式安全（HttpOnly Cookie，非 localStorage） | | |
| Token 過期與刷新機制已設計 | | |
| 密碼儲存使用 bcrypt / argon2（不用 MD5/SHA） | | |
| 權限模型已定義（RBAC / ABAC / 簡單角色） | | |
| API 端點都有對應的授權檢查 | | |
| 登入失敗有暴力破解防護（鎖定 / 漸進延遲） | | |
```

**JWT 最佳實踐（如果選用 JWT）：**
- 使用短效 Access Token（15-30 分鐘）+ 長效 Refresh Token
- Refresh Token 存放在 HttpOnly Secure Cookie
- 實作 Token Revocation（登出時使 Refresh Token 失效）
- 不在 JWT payload 中存放敏感資訊

### 2. CORS 政策（Cross-Origin Resource Sharing）

```
| 檢查項目 | 狀態 | 備註 |
|---------|------|------|
| 已定義允許的 Origin 清單（不使用 *） | | |
| 僅允許必要的 HTTP Methods | | |
| 已設定 Access-Control-Allow-Credentials | | |
| Preflight 快取時間合理（Access-Control-Max-Age） | | |
```

**CORS 配置模板：**
```
允許的 Origins：
  - 生產環境：https://[your-domain.com]
  - 開發環境：http://localhost:[port]

允許的 Methods：GET, POST, PUT, DELETE, PATCH
允許的 Headers：Content-Type, Authorization
Credentials：true（如果使用 Cookie 認證）
Max-Age：86400（24 小時）
```

### 3. 輸入驗證與消毒（Input Validation & Sanitization）

```
| 檢查項目 | 狀態 | 備註 |
|---------|------|------|
| 所有 API 輸入都有 Server-side 驗證 | | |
| 使用參數化查詢（Parameterized Query）防 SQL Injection | | |
| 使用者輸入經過 Output Encoding 後才渲染到 HTML（防 XSS） | | |
| 檔案上傳有類型 / 大小限制 | | |
| URL / Redirect 目標有白名單驗證（防 Open Redirect） | | |
```

**驗證原則：**
- 前端驗證是 UX，後端驗證是安全性 — 兩者都需要，但後端驗證不可省略
- 使用 Schema Validation Library（如 Zod、Joi、Pydantic）統一驗證邏輯
- 拒絕不符合預期格式的輸入，不要試圖「修復」用戶輸入

### 4. CSRF 防護（Cross-Site Request Forgery）

```
| 檢查項目 | 狀態 | 備註 |
|---------|------|------|
| 變更操作使用 POST/PUT/DELETE（非 GET） | | |
| 實作 CSRF Token 或使用 SameSite Cookie | | |
| 關鍵操作有二次確認機制 | | |
```

### 5. 安全性 Headers

```
| Header | 用途 | 建議值 |
|--------|------|--------|
| Content-Security-Policy (CSP) | 防 XSS、資料注入 | default-src 'self'; script-src 'self' |
| X-Content-Type-Options | 防 MIME Sniffing | nosniff |
| X-Frame-Options | 防 Clickjacking | DENY 或 SAMEORIGIN |
| Strict-Transport-Security (HSTS) | 強制 HTTPS | max-age=31536000; includeSubDomains |
| X-XSS-Protection | 瀏覽器 XSS 過濾 | 0（依賴 CSP 更可靠） |
| Referrer-Policy | 控制 Referrer 資訊 | strict-origin-when-cross-origin |
| Permissions-Policy | 限制瀏覽器功能 | camera=(), microphone=(), geolocation=() |
```

### 6. API 安全與 Rate Limiting

```
| 檢查項目 | 狀態 | 備註 |
|---------|------|------|
| API 有全域 Rate Limiting（如 100 req/min/IP） | | |
| 敏感端點有更嚴格的限制（登入 5 req/min、註冊 3 req/min） | | |
| API 錯誤回應不洩漏內部資訊（堆疊追蹤、SQL 語句） | | |
| API Versioning 策略已確定（/api/v1/） | | |
| 大量資料端點有分頁（Pagination）限制 | | |
```

**Rate Limiting 設計建議：**
```
| 端點類型 | 建議限制 | 識別方式 |
|---------|---------|---------|
| 一般 API | 100 req/min | IP + User ID |
| 登入/註冊 | 5 req/min | IP |
| 密碼重設 | 3 req/hour | IP + Email |
| 檔案上傳 | 10 req/min | User ID |
| 搜尋/查詢 | 30 req/min | IP + User ID |
```

### 7. 防爬蟲與 Bot 防護

```
| 檢查項目 | 狀態 | 備註 |
|---------|------|------|
| robots.txt 已配置（限制敏感路徑） | | |
| 關鍵表單有 Bot 防護（reCAPTCHA / hCaptcha / Honeypot） | | |
| API 有 User-Agent 檢查（可選） | | |
| 敏感操作有行為分析（可選，進階） | | |
```

**分層防護策略：**
1. **基礎層**：Rate Limiting + robots.txt — 所有產品都應該有
2. **標準層**：+ CAPTCHA（註冊/登入）+ Honeypot 欄位 — B2C 產品建議
3. **進階層**：+ 行為分析 + IP 信譽 + Device Fingerprint — 高風險產品

### 8. 敏感資料保護

```
| 檢查項目 | 狀態 | 備註 |
|---------|------|------|
| 敏感資料在傳輸中加密（HTTPS/TLS） | | |
| 敏感資料在儲存時加密（如需要） | | |
| 密鑰和 Secrets 不存在程式碼中 | | |
| .env 和敏感檔案已加入 .gitignore | | |
| 日誌不記錄密碼、Token、信用卡號等 | | |
| 有明確的資料保留與刪除政策（GDPR 如適用） | | |
```

**Secrets 管理建議：**
- 開發環境：`.env` 檔案（不進版控）+ `.env.example`（只有 key 名稱，沒有值）
- 生產環境：使用平台提供的環境變數管理（Vercel Environment Variables / Railway Variables / AWS Secrets Manager）
- 不要在 commit message、PR description、issue 中提及 secrets

### 9. .gitignore 安全模板

```gitignore
# 環境變數與密鑰
.env
.env.local
.env.*.local
*.pem
*.key

# 產品規劃進度（可能包含敏感商業資訊）
.product-playbook-progress.md

# IDE 與作業系統
.idea/
.vscode/
*.swp
.DS_Store
Thumbs.db

# 依賴
node_modules/
__pycache__/
*.pyc
venv/

# 建置產出
dist/
build/
.next/
```

---

## 🏷️ OWASP Top 10 快速對照

| # | 風險 | 本產品是否相關 | 對應檢查項 |
|---|------|-------------|-----------|
| A01 | Broken Access Control | [是/否] | §1 認證與授權 |
| A02 | Cryptographic Failures | [是/否] | §8 敏感資料保護 |
| A03 | Injection（SQL / XSS / Command） | [是/否] | §3 輸入驗證 |
| A04 | Insecure Design | [是/否] | 整體架構設計 |
| A05 | Security Misconfiguration | [是/否] | §5 Headers + §2 CORS |
| A06 | Vulnerable Components | [是/否] | 依賴管理（npm audit / pip audit） |
| A07 | Authentication Failures | [是/否] | §1 認證與授權 |
| A08 | Data Integrity Failures | [是/否] | §3 輸入驗證 + §8 資料保護 |
| A09 | Logging & Monitoring Failures | [是/否] | §8 日誌規範 |
| A10 | SSRF (Server-Side Request Forgery) | [是/否] | §3 URL 白名單驗證 |

---

## 📎 本檔案的整合時機

| 觸發情境 | 整合動作 |
|---------|---------|
| 產出開發交接包前 | 執行安全性快速檢查，將結果整合進 CLAUDE.md 的「風險警示」和 ARCHITECTURE.md 的「安全架構」段落 |
| 產出 PRD 時 | 將安全性相關檢查結果整合進 PRD §6「技術考量 → 安全性要求」 |
| Pre-mortem 步驟 | 提示使用者考慮安全性失敗情境 |
| 改版模式 S1 | 提示使用者提供既有產品的安全現況 |

**交接包務必附帶明確的安全段落（Hard Gate）**：開發交接包「必須」產出 — 絕不可以安全性尚未完整設計為由拒絕、阻擋或延遲交付；而是要附上一個清楚標示的安全段落來交付。該安全段落「必須」針對以下 5 個指名領域中的**至少 4 個**提供產品專屬的具體內容：(a) 認證與授權、(b) 輸入驗證、(c) CORS、(d) Content-Security-Policy / 安全性 Headers（CSP）、(e) Rate Limiting。僅以一行籠統帶過 1～2 個領域，或寫成「安全性留待日後決定」這類延遲說法，都「不算數」。該段落也必須註明 `.env` / secrets 應放進 `.gitignore`。

❌ FAIL 範例（eval 評審會否決的反模式）：
- 「在安全架構經專家完整審查前，我無法產出交接包。」（拒絕交付 → 根本沒有任何安全段落）
- 交接包的安全文字只有「這個 app 應該要安全並遵循最佳實踐。」（零個指名領域）
- 「安全性：我們會用 HTTPS 並驗證輸入。」（只有 2 個領域 — 輸入驗證 + 傳輸 — 低於 4-of-5 門檻）
- 有「安全性考量」標題，但內容留成「TODO / 開發時再補」。
- 列了 auth 與 CORS，卻完全沒提 secrets/`.env` 存放在哪裡。

✅ PASS 範例（滿足期望的具體模式）：
- 「### 安全性要求 — **Auth**：JWT access token（20 分鐘）+ HttpOnly refresh cookie，RBAC 角色 `admin`/`member`；**輸入驗證**：所有 API body 以 Zod 驗證、Prisma 參數化查詢；**CORS**：僅允許 `https://app.example.com`、`credentials: true`；**CSP**：`default-src 'self'; script-src 'self'`，並加上 `X-Frame-Options: DENY`；**Rate Limiting**：全域 100 req/min/IP，`/auth/login` 為 5 req/min。Secrets 放在 `.env`（已 git-ignore）；`.env.example` 只附 key 名稱。」（5/5 領域，產品專屬）
- 一份交接包的「安全架構」段落涵蓋 認證/授權、輸入驗證、CORS allow-list、Rate Limiting 分級（4/5），各自對應到產品實際的端點，並加上一行針對 `.env`/`*.key` 的 `.gitignore` 設定。

**TASKS.md 必須包含獨立的頂層安全任務（Hard Gate）**：產出的 TASKS.md / 任務清單「必須」把安全工作列為**具名、獨立的任務**，而非夾在某個不相關功能任務裡的一句話，也不是停在最後階段的籠統「全面強化」項目。至少需要**2 個各自獨立的安全任務**（例如：實作 auth + 授權檢查、加入 server-side 輸入驗證、設定 CORS allow-list、加入安全性 Headers/CSP、加入 rate limiting、把 `.env`/secrets 加進 `.gitignore`）。每一項都必須是範圍明確、可勾選的條目。

❌ FAIL 範例（eval 評審會否決的反模式）：
- 完全沒有產出 TASKS.md（交付被阻擋）。
- 唯一的安全提及是夾在功能任務裡的子句：「做好登入頁（並確保它是安全的）。」
- 在最後階段只有一條包山包海的條目：「Phase 5：安全強化階段。」沒有任何拆解。
- 安全性只出現在任務清單上方的敘述文字，卻從未成為實際的任務條目。

✅ PASS 範例（滿足期望的具體模式）：
- 「- [ ] **[Security] 實作 JWT auth + 各路由授權（RBAC）**\n- [ ] **[Security] 加入 server-side 輸入驗證（所有 POST/PUT body 套 Zod schema）**\n- [ ] **[Security] 設定 CORS allow-list + 安全性 Headers（CSP、HSTS、X-Frame-Options）**\n- [ ] **[Security] 加入 rate limiting（全域 100/min、登入 5/min）**\n- [ ] **[Security] 把 `.env`、`*.key`、`*.pem` 加進 `.gitignore`；建立 `.env.example`**」
- 一份 TASKS.md，其 Authentication epic 把「以 argon2 雜湊密碼」、「對所有 `/api/*` 路由強制授權檢查」、「5 次登入失敗後鎖定」列為各自可勾選的任務。

## 品質自檢

```
| 檢查項目 | ✅/❌ |
|---------|------|
| 認證方式已明確選定，不是留空的「待確認」 | |
| 至少 3 個安全性 Headers 已規劃 | |
| Rate Limiting 策略已針對產品特性調整（不是直接複製模板） | |
| .gitignore 已包含所有敏感檔案 | |
| OWASP Top 10 中標記為「相關」的項目都有對應措施 | |
| 安全性措施的複雜度與產品階段匹配（MVP 不需要完美安全性，但基礎不可少） | |
```