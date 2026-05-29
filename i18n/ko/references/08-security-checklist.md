# 보안 체크리스트

> 개발 핸드오프 패키지 작성 전에 로드됩니다. 제품 기획 단계에서 핵심 보안 요구사항이 고려되도록 하여, 보안이 사후 고려가 되지 않도록 합니다.

## 🔐 보안 아키텍처 빠른 점검

개발 핸드오프 패키지 작성 전에, 다음 보안 측면을 각각 검증하세요. 각각 ✅ (기획에 반영됨) 또는 ❌ (추가 필요)로 표시하세요.

### 1. 인증 & 인가

```
| 점검 항목 | 상태 | 비고 |
|----------|------|------|
| 인증 방식 결정됨 (JWT / Session / OAuth / Passkey) | | |
| 토큰 저장이 안전함 (HttpOnly Cookie, localStorage 아님) | | |
| 토큰 만료 및 갱신 메커니즘 설계됨 | | |
| 비밀번호 저장에 bcrypt / argon2 사용 (MD5/SHA 아님) | | |
| 권한 모델 정의됨 (RBAC / ABAC / 단순 역할) | | |
| 모든 API 엔드포인트에 해당 인가 체크 있음 | | |
| 로그인 실패에 무차별 대입 방어 (잠금 / 점진적 지연) | | |
```

**JWT 모범 사례 (JWT 사용 시):**
- 짧은 수명의 Access Token (15-30분) + 긴 수명의 Refresh Token 사용
- Refresh Token을 HttpOnly Secure Cookie에 저장
- Token Revocation 구현 (로그아웃 시 Refresh Token 무효화)
- JWT 페이로드에 민감한 정보 저장하지 않기

### 2. CORS 정책 (Cross-Origin Resource Sharing)

```
| 점검 항목 | 상태 | 비고 |
|----------|------|------|
| 허용 Origin 목록 정의됨 (와일드카드 * 사용 금지) | | |
| 필요한 HTTP 메서드만 허용됨 | | |
| Access-Control-Allow-Credentials 설정됨 | | |
| Preflight 캐시 기간이 합리적 (Access-Control-Max-Age) | | |
```

**CORS 설정 템플릿:**
```
허용 Origins:
  - 프로덕션: https://[your-domain.com]
  - 개발: http://localhost:[port]

허용 Methods: GET, POST, PUT, DELETE, PATCH
허용 Headers: Content-Type, Authorization
Credentials: true (쿠키 기반 인증 사용 시)
Max-Age: 86400 (24시간)
```

### 3. 입력 유효성 검증 & 새니타이징

```
| 점검 항목 | 상태 | 비고 |
|----------|------|------|
| 모든 API 입력에 서버사이드 유효성 검증 있음 | | |
| SQL Injection 방지를 위해 파라미터화 쿼리 사용 | | |
| 사용자 입력이 HTML 렌더링 전 출력 인코딩됨 (XSS 방지) | | |
| 파일 업로드에 타입 / 크기 제한 있음 | | |
| URL / 리디렉트 대상에 화이트리스트 검증 (Open Redirect 방지) | | |
```

**유효성 검증 원칙:**
- 프론트엔드 유효성 검증은 UX; 백엔드 유효성 검증은 보안 — 둘 다 필요하지만, 백엔드 유효성 검증은 타협 불가
- Schema Validation Library 사용 (예: Zod, Joi, Pydantic)으로 통합 유효성 검증 로직
- 예상 형식과 맞지 않는 입력은 거부 — 사용자 입력을 "수정"하려 하지 마세요

### 4. CSRF 방어 (Cross-Site Request Forgery)

```
| 점검 항목 | 상태 | 비고 |
|----------|------|------|
| 상태 변경 작업에 POST/PUT/DELETE 사용 (GET 아님) | | |
| CSRF Token 구현 또는 SameSite Cookie 사용 | | |
| 중요 작업에 2차 확인 있음 | | |
```

### 5. 보안 헤더

```
| 헤더 | 용도 | 권장 값 |
|------|------|--------|
| Content-Security-Policy (CSP) | XSS, 데이터 주입 방지 | default-src 'self'; script-src 'self' |
| X-Content-Type-Options | MIME 스니핑 방지 | nosniff |
| X-Frame-Options | 클릭재킹 방지 | DENY 또는 SAMEORIGIN |
| Strict-Transport-Security (HSTS) | HTTPS 강제 | max-age=31536000; includeSubDomains |
| X-XSS-Protection | 브라우저 XSS 필터 | 0 (CSP에 의존하는 것이 더 신뢰성 있음) |
| Referrer-Policy | 리퍼러 정보 제어 | strict-origin-when-cross-origin |
| Permissions-Policy | 브라우저 기능 제한 | camera=(), microphone=(), geolocation=() |
```

### 6. API 보안 & Rate Limiting

```
| 점검 항목 | 상태 | 비고 |
|----------|------|------|
| API에 글로벌 rate limiting 있음 (예: 100 req/min/IP) | | |
| 민감한 엔드포인트에 더 엄격한 제한 (로그인 5 req/min, 등록 3 req/min) | | |
| API 에러 응답에 내부 상세 노출 없음 (스택 트레이스, SQL문) | | |
| API 버전 관리 전략 결정됨 (/api/v1/) | | |
| 대량 데이터 엔드포인트에 페이지네이션 제한 있음 | | |
```

**Rate Limiting 설계 권장사항:**
```
| 엔드포인트 유형 | 권장 제한 | 식별 방법 |
|---------------|----------|----------|
| 일반 API | 100 req/min | IP + User ID |
| 로그인/등록 | 5 req/min | IP |
| 비밀번호 재설정 | 3 req/hour | IP + Email |
| 파일 업로드 | 10 req/min | User ID |
| 검색/쿼리 | 30 req/min | IP + User ID |
```

### 7. 스크래핑 방지 & 봇 보호

```
| 점검 항목 | 상태 | 비고 |
|----------|------|------|
| robots.txt 설정됨 (민감한 경로 제한) | | |
| 중요 폼에 봇 보호 있음 (reCAPTCHA / hCaptcha / Honeypot) | | |
| API에 User-Agent 체크 있음 (선택) | | |
| 민감한 작업에 행동 분석 있음 (선택, 고급) | | |
```

**계층적 보호 전략:**
1. **기본 계층**: Rate Limiting + robots.txt — 모든 제품에 필수
2. **표준 계층**: + CAPTCHA (등록/로그인) + Honeypot 필드 — B2C 제품에 권장
3. **고급 계층**: + 행동 분석 + IP 평판 + Device Fingerprint — 고위험 제품

### 8. 민감한 데이터 보호

```
| 점검 항목 | 상태 | 비고 |
|----------|------|------|
| 민감한 데이터 전송 중 암호화 (HTTPS/TLS) | | |
| 민감한 데이터 저장 시 암호화 (필요한 경우) | | |
| 시크릿과 키가 코드에 저장되지 않음 | | |
| .env 및 민감 파일이 .gitignore에 추가됨 | | |
| 로그에 비밀번호, 토큰, 신용카드 번호 등 기록하지 않음 | | |
| 명확한 데이터 보존 및 삭제 정책 (해당되는 경우 GDPR) | | |
```

**시크릿 관리 권장사항:**
- 개발: `.env` 파일 (버전 관리에 포함하지 않음) + `.env.example` (키 이름만, 값 없음)
- 프로덕션: 플랫폼 제공 환경 변수 관리 사용 (Vercel Environment Variables / Railway Variables / AWS Secrets Manager)
- 커밋 메시지, PR 설명, 이슈에 시크릿 언급하지 않기

### 9. .gitignore 보안 템플릿

```gitignore
# 환경 변수 및 시크릿
.env
.env.local
.env.*.local
*.pem
*.key

# 제품 기획 진행 상황 (민감한 비즈니스 정보 포함 가능)
.product-playbook-progress.md

# IDE 및 OS
.idea/
.vscode/
*.swp
.DS_Store
Thumbs.db

# 의존성
node_modules/
__pycache__/
*.pyc
venv/

# 빌드 출력
dist/
build/
.next/
```

---

## 🏷️ OWASP Top 10 빠른 참조

| # | 리스크 | 이 제품에 해당? | 대응 점검 |
|---|--------|--------------|----------|
| A01 | Broken Access Control | [예/아니오] | §1 인증 & 인가 |
| A02 | Cryptographic Failures | [예/아니오] | §8 민감한 데이터 보호 |
| A03 | Injection (SQL / XSS / Command) | [예/아니오] | §3 입력 유효성 검증 |
| A04 | Insecure Design | [예/아니오] | 전체 아키텍처 설계 |
| A05 | Security Misconfiguration | [예/아니오] | §5 헤더 + §2 CORS |
| A06 | Vulnerable Components | [예/아니오] | 의존성 관리 (npm audit / pip audit) |
| A07 | Authentication Failures | [예/아니오] | §1 인증 & 인가 |
| A08 | Data Integrity Failures | [예/아니오] | §3 입력 유효성 검증 + §8 데이터 보호 |
| A09 | Logging & Monitoring Failures | [예/아니오] | §8 로깅 규칙 |
| A10 | SSRF (Server-Side Request Forgery) | [예/아니오] | §3 URL 화이트리스트 검증 |

---

## 📎 통합 타이밍

| 트리거 | 통합 작업 |
|--------|----------|
| 개발 핸드오프 패키지 작성 전 | 보안 빠른 점검 실행, 결과를 CLAUDE.md "리스크 알림" 및 ARCHITECTURE.md "보안 아키텍처" 섹션에 통합 |
| PRD 작성 시 | 보안 점검 결과를 PRD §6 "기술 고려사항 → 보안 요구사항"에 통합 |
| Pre-mortem 단계 | 사용자에게 보안 실패 시나리오를 고려하도록 프롬프트 |
| 리비전 모드 S1 | 사용자에게 기존 제품의 현재 보안 상태를 제공하도록 프롬프트 |

**핸드오프는 항상 명시적인 보안 섹션과 함께 전달하세요 (Hard Gate)**: 개발 핸드오프 패키지는 반드시 작성되어야 합니다 — 보안이 완전히 설계되지 않았다는 이유로 전달을 거부하거나, 차단하거나, 연기해서는 절대 안 됩니다; 대신 명확히 레이블이 붙은 보안 섹션과 함께 패키지를 전달하세요. 해당 보안 섹션은 다음 5가지 명명된 영역 중 **최소 4가지**를 제품 특화된 세부 내용으로 구체적으로 다루어야 합니다: (a) 인증 & 인가, (b) 입력 유효성 검증, (c) CORS, (d) Content-Security-Policy / 보안 헤더 (CSP), (e) Rate Limiting. 1~2개 영역만 일반적으로 한 줄 언급하거나 "보안은 나중에 결정"과 같이 연기하는 것은 인정되지 않습니다. 해당 섹션은 또한 `.env` / 시크릿이 `.gitignore`에 속한다는 점을 명시해야 합니다.

❌ FAIL 예시 (eval 심사관이 거부할 안티패턴):
- "보안 아키텍처가 전문가에 의해 완전히 검토될 때까지 핸드오프 패키지를 생성할 수 없습니다." (전달 거부 → 보안 섹션이 아예 존재하지 않음)
- 보안 관련 텍스트가 "앱은 안전해야 하고 모범 사례를 따라야 합니다."뿐인 핸드오프. (명명된 영역 0개)
- "보안: HTTPS를 사용하고 입력을 검증하겠습니다." (입력 유효성 검증 + 전송, 2개 영역뿐 — 4-of-5 기준 미달)
- "보안 고려사항" 제목은 있지만 "TODO / 개발 중에 채워질 예정"으로 남겨진 경우.
- 인증과 CORS는 나열하지만 시크릿/`.env`가 어디에 저장되는지에 대한 언급이 누락된 경우.

✅ PASS 예시 (기대를 충족하는 구체적 패턴):
- "### 보안 요구사항 — **Auth**: JWT access token (20분) + HttpOnly refresh cookie, RBAC 역할 `admin`/`member`; **입력 유효성 검증**: 모든 API 바디를 Zod로 검증, 파라미터화된 Prisma 쿼리; **CORS**: `https://app.example.com`만 allow-list, `credentials: true`; **CSP**: `default-src 'self'; script-src 'self'`, 추가로 `X-Frame-Options: DENY`; **Rate Limiting**: 글로벌 100 req/min/IP, `/auth/login`에 5 req/min. 시크릿은 `.env`에 보관 (git-ignored); `.env.example`은 키 이름만 포함." (5/5 영역, 제품 특화)
- Authentication/Authorization, 입력 유효성 검증, CORS allow-list, Rate Limiting 계층 (4/5)을 다루는 핸드오프 "보안 아키텍처" 섹션으로, 각각 제품의 실제 엔드포인트와 연결되며, `.env`/`*.key`에 대한 `.gitignore` 라인을 포함.

**TASKS.md는 개별적이고 최상위 수준의 보안 작업을 포함해야 합니다 (Hard Gate)**: 생성된 TASKS.md / 작업 목록은 보안 작업을 **명명된 독립 작업**으로 포함해야 하며, 관련 없는 기능 작업 안에 묻힌 문장이나 마지막 단계에 방치된 모호한 "전체 강화" 항목이어서는 안 됩니다. 최소 **2개의 별개 보안 작업**이 필요합니다 (예: 인증 + 인가 체크 구현, 서버사이드 입력 유효성 검증 추가, CORS allow-list 설정, 보안 헤더/CSP 추가, rate limiting 추가, `.env`/시크릿을 `.gitignore`에 추가). 각각은 명확한 범위를 가진 체크 가능한 라인 항목이어야 합니다.

❌ FAIL 예시 (eval 심사관이 거부할 안티패턴):
- TASKS.md가 아예 생성되지 않음 (전달 차단).
- 유일한 보안 언급이 기능 작업 안의 절(節)인 경우: "로그인 페이지 구축 (그리고 안전하게 만들기)."
- 마지막 단계의 단일 포괄 항목: "Phase 5: 보안 강화 패스." 세부 분해 없음.
- 보안이 작업 목록 위의 산문에만 나타나고 실제 작업 항목으로는 결코 나타나지 않는 경우.

✅ PASS 예시 (기대를 충족하는 구체적 패턴):
- "- [ ] **[Security] JWT 인증 + 라우트별 인가 (RBAC) 구현**\n- [ ] **[Security] 서버사이드 입력 유효성 검증 추가 (모든 POST/PUT 바디에 Zod 스키마)**\n- [ ] **[Security] CORS allow-list + 보안 헤더 (CSP, HSTS, X-Frame-Options) 설정**\n- [ ] **[Security] rate limiting 추가 (글로벌 100/min, 로그인 5/min)**\n- [ ] **[Security] `.env`, `*.key`, `*.pem`을 `.gitignore`에 추가; `.env.example` 생성**"
- Authentication epic이 "argon2로 비밀번호 해싱", "모든 `/api/*` 라우트에 인가 체크 강제", "5회 로그인 실패 후 잠금"을 별개의 체크 가능한 작업으로 나열하는 TASKS.md.

## 품질 자체 점검

```
| 점검 항목 | ✅/❌ |
|----------|------|
| 인증 방식이 명시적으로 선택됨, "TBD"로 남기지 않음 | |
| 최소 3개 보안 헤더 계획됨 | |
| Rate limiting 전략이 제품 특성에 맞게 조정됨 (템플릿 그대로 복사하지 않음) | |
| .gitignore에 모든 민감 파일 포함 | |
| "해당"으로 표시된 모든 OWASP Top 10 항목에 대응 조치 있음 | |
| 보안 조치 복잡성이 제품 단계에 적합 (MVP에 완벽한 보안은 필요 없지만, 기본은 타협 불가) | |
```