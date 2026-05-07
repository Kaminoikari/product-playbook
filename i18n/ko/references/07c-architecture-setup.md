# 개발 핸드오프 — ARCHITECTURE.md + setup.sh

## 📄 ARCHITECTURE.md 템플릿

```markdown
# [제품명] — 기술 아키텍처

## 디렉토리 구조

[기술 스택에 맞는 디렉토리 구조 생성]

## 데이터베이스 설계

[PRD의 DB Schema에서 통합 — CREATE TABLE SQL 또는 ORM 모델 정의로 변환]

### ER 다이어그램

[Mermaid erDiagram]

### 주요 테이블 설명

| 테이블 | 설명 | 핵심 필드 | 인덱스 권장사항 |
|--------|------|----------|--------------|
| | | | |

## API 설계

[User Stories와 기능 상세를 기반으로 RESTful API 엔드포인트 또는 GraphQL 스키마 정의]

### 엔드포인트 목록

| 메서드 | 경로 | 설명 | 대응 Task |
|--------|------|------|----------|
| GET | /api/v1/[resource] | [설명] | T1.1 |
| POST | /api/v1/[resource] | [설명] | T1.2 |

### 인증

[JWT / Session / OAuth 등]

## 서드파티 서비스

| 서비스 | 용도 | 대응 기능 |
|--------|------|----------|
| | | |

## 보안 아키텍처

### CORS 설정

| 설정 | 값 | 비고 |
|------|---|------|
| 허용 오리진 | [프로덕션 도메인, localhost:port] | 와일드카드 * 사용 금지 |
| 허용 메서드 | GET, POST, PUT, DELETE | 실제 API 니즈 기반 |
| 허용 헤더 | Content-Type, Authorization | |
| Credentials | true/false | 인증 방식에 따라 |

### 보안 헤더

[제품 요구사항에 맞게 references/08-security-checklist.md §5에서 해당 헤더 선택]

### Rate Limiting 전략

| 엔드포인트 유형 | 제한 | 식별 방법 |
|---------------|------|----------|
| 일반 API | [X] req/min | IP + User ID |
| 로그인/등록 | [X] req/min | IP |
| 파일 업로드 | [X] req/min | User ID |

### 민감한 데이터 처리

- 시크릿 관리: [.env + 플랫폼 환경 변수 / Secrets Manager]
- 로깅 규칙: 비밀번호, 토큰, 개인 데이터는 절대 로그하지 않음
- 데이터 암호화: [전송 중 TLS / 저장 시 암호화 요구사항]

> 전체 보안 체크리스트는 `references/08-security-checklist.md` 참조
```

---

## 📄 .gitignore 템플릿

```gitignore
# 환경 변수 및 시크릿
.env
.env.local
.env.*.local
*.pem
*.key

# 제품 기획 진행 상황 (민감한 비즈니스 정보 포함 가능)
.product-playbook-progress.md
# Product-playbook 개발 핸드오프 마커 (session-local; commit 금지)
.product-dev-active

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

## 📄 setup.sh 템플릿

```bash
#!/bin/bash
# [제품명] — 프로젝트 초기화 스크립트
# 사용법: chmod +x scripts/setup.sh && ./scripts/setup.sh

set -e

echo "🚀 [제품명] 초기화 중..."

# ===== 사전 요구사항 확인 =====
command -v [node/python/etc] >/dev/null 2>&1 || { echo "❌ [런타임]이 필요합니다"; exit 1; }

# ===== 의존성 설치 =====
echo "📦 의존성 설치 중..."
[npm install / pip install -r requirements.txt / etc]

# ===== 환경 설정 =====
if [ ! -f .env ]; then
  echo "📝 .env 파일 생성 중..."
  cp .env.example .env
  echo "⚠️  .env를 편집하여 필요한 환경 변수를 입력해 주세요"
fi

# ===== 데이터베이스 초기화 =====
echo "🗄️  데이터베이스 초기화 중..."
[migration commands]

echo ""
echo "✅ 초기화 완료!"
echo ""
echo "다음 단계:"
echo "  1. .env를 편집하여 환경 변수 입력"
echo "  2. 개발 서버 시작: [시작 명령]"
echo "  3. 개발 시작: claude \"CLAUDE.md와 TASKS.md를 읽고, Phase 1 실행 시작\""
```

---

## 사용자 가이드 텍스트

### Claude Chat / Cowork에서

핸드오프 패키지 작성 후 다음 가이드를 표시하세요:

```
📦 개발 핸드오프 패키지가 준비되었습니다! 다음 파일들이 포함됩니다:

  CLAUDE.md        → Claude Code의 프로젝트 메모리 (제품 컨텍스트 + 기술 사양)
  TASKS.md         → 개발 Task 목록 (4 Phase, 총 [N]개 Task)
  TICKETS.md       → 티켓 목록 ([N]개 티켓, Jira/Asana/Linear에서 바로 생성 가능)
  docs/PRD.md      → 전체 PRD
  docs/ARCHITECTURE.md → 기술 아키텍처 (DB schema + API + 디렉토리 구조)
  docs/PRODUCT-SPEC.md → 제품 스펙 요약
  scripts/setup.sh → 원클릭 초기화 스크립트

🔗 개발 시작 방법:

  1. 다운로드하여 프로젝트 폴더에 압축 해제
  2. 터미널을 열고 프로젝트 폴더로 이동
  3. Claude Code 실행:
     $ claude
  4. Claude Code에게 시작 명령:
     > CLAUDE.md와 TASKS.md를 읽고, Phase 0 실행 시작

💡 팁:
  - Claude Code는 자동으로 CLAUDE.md를 읽으므로, 이미 전체 제품 컨텍스트를 알고 있습니다
  - 각 Phase 완료 후, 다음 Phase로 진행할지 물어봅니다
  - 기능 범위를 조정하려면 TASKS.md를 직접 편집하세요
  - CLAUDE.md의 "명시적 제외" 목록이 Claude Code가 범위 밖으로 개발하는 것을 방지합니다
```

### 출력 전 최종 확인

```
개발 핸드오프 패키지를 작성하기 전에 몇 가지 확인이 필요합니다:

1. 기술 스택: [확인됨 / 확인 필요]
2. 제품명 (프로젝트 폴더 이름용): [확인됨 / 확인 필요]
3. 다른 기술 제약이나 선호사항이 있나요?
   - 예: 특정 ORM 사용 필수, 특정 브라우저 지원, 기존 CI/CD 등
```
