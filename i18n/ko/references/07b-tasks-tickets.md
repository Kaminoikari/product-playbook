# 개발 핸드오프 — TASKS.md + TICKETS.md

## 📄 TASKS.md 템플릿

기능 분해 핵심 원칙:
- MVP 필수 기능(P0 기능)에서 시작
- 각 Task는 User Story에 매핑
- Phase 간 명확한 의존성: Phase N+1은 Phase N 산출물에 의존
- 각 Task에 Claude Code가 자체 검증 가능한 인수 기준 포함

```markdown
# [제품명] — 개발 Task 목록

## Phase 0: 프로젝트 초기화
> 목표: 실행 가능한 빈 프로젝트 스켈레톤 구축

- [ ] **T0.1** 프로젝트 초기화 (`scripts/setup.sh` 또는 수동)
  - 인수:
    - [ ] `npm run dev` / `python manage.py runserver` 또는 동등 명령이 성공적으로 시작됨
    - [ ] `.gitignore` 생성됨, `.env`, `.env.local`, `node_modules/`, `.product-playbook-progress.md`, `.product-dev-active` 등 민감 파일 포함
    - [ ] `.env.example` 생성됨 (키 이름만, 실제 값 없음)
- [ ] **T0.2** 린터 + 포매터 설정
  - 인수: lint가 에러 없이 통과
- [ ] **T0.3** 데이터베이스 설정 + 초기 마이그레이션 실행
  - 인수: 데이터베이스 연결 가능, 기본 테이블 생성됨
- [ ] **T0.4** 기본 라우팅 구조 설정
  - 인수: 모든 주요 페이지 라우트 접근 가능 (빈 페이지 반환도 괜찮음)

## Phase 1: 핵심 플로우 (Aha Moment 경로)
> 목표: 사용자가 진입부터 Aha Moment까지 최단 경로를 완료하도록
> 대응 User Stories: [US-001, US-002, ...]

- [ ] **T1.1** [기능명]
  - User Story: [Persona]로서 나는 [행동]을 하고 싶어서 [가치]를 얻고 싶다
  - 인수 기준:
    - [ ] [구체적 테스트 가능 조건 1]
    - [ ] [구체적 테스트 가능 조건 2]
  - 기술 참고: [필요한 API / 서드파티 서비스 / 특수 로직]

- [ ] **T1.2** [기능명]
  - User Story: ...
  - 인수 기준: ...

> **Phase 1 완료 체크포인트**: 사용자가 [Aha Moment 행동]을 완료할 수 있음. 그렇지 않으면 Phase 2로 넘어가지 마세요.

## Phase 2: MVP 완성
> 목표: Phase 1에서 다루지 않은 나머지 P0 기능 채우기
> 대응 User Stories: [US-003, US-004, ...]

- [ ] **T2.1** [기능명]
  - ...

> **Phase 2 완료 체크포인트**: 모든 P0 User Story 인수 기준 통과.

## Phase 3: 품질 & 경험
> 목표: 에러 처리, 엣지 케이스, 로딩 상태, 기본 보안

- [ ] **T3.1** 글로벌 에러 처리
- [ ] **T3.2** 폼 유효성 검증 + 엣지 케이스
- [ ] **T3.3** 로딩 상태 + 빈 상태
- [ ] **T3.4** 보안 점검 (`references/08-security-checklist.md`에 따라 각 항목 검증)
  - 인수:
    - [ ] OWASP Top 10 관련 항목 대응 (입력 유효성 검증, 인증, XSS 방어, CSRF 방어)
    - [ ] 보안 헤더 설정 (CSP, X-Frame-Options, HSTS 등)
    - [ ] CORS 정책 설정 (와일드카드 * 사용 금지)
    - [ ] 민감한 API 엔드포인트에 rate limiting 적용
    - [ ] API 에러 응답에 내부 정보 노출 없음
- [ ] **T3.5** 반응형 디자인 (웹인 경우)

## Phase 4: 배포
> 목표: 외부 사용자가 접근 가능하도록

- [ ] **T4.1** 환경 변수 관리
- [ ] **T4.2** 배포 설정
- [ ] **T4.3** 기본 모니터링 + 로깅
```

---

## 📄 TICKETS.md 템플릿

TICKETS.md는 TASKS.md의 기능 분해를 가져와, 프로젝트 관리 도구에서 직접 티켓을 생성할 수 있는 구조화된 내용을 작성합니다. 각 티켓에는 PM이 필요한 모든 정보가 포함됩니다.

> **디자인 목표**: PM이 각 티켓의 내용을 Jira / Asana / Linear 등 도구에 직접 복사하여 티켓을 생성할 수 있습니다. 향후 버전은 API를 통한 자동 티켓 생성을 지원할 예정입니다.

```markdown
# [제품명] — 티켓 목록

> 생성일: [타임스탬프]
> 대응 TASKS.md 버전: [버전/타임스탬프]
> 총: [N]개 티켓

---

## 티켓 개요

| 티켓 # | 제목 | Phase | 우선순위 | 예상 시간 | 의존성 |
|--------|------|-------|---------|----------|--------|
| TKT-001 | [제목] | Phase 0 | P0 | [X]h | — |
| TKT-002 | [제목] | Phase 1 | P0 | [X]h | TKT-001 |
| ... | | | | | |

---

## TKT-001: [제목]

**Phase**: Phase 0 — 프로젝트 초기화
**대응 Task**: T0.1
**우선순위**: P0
**예상 시간**: [X]시간
**의존성**: 없음
**담당자**: [역할/팀, 예: 백엔드 엔지니어]

### 설명

[이 티켓이 달성하는 것을 1-3 문단으로 설명, 비즈니스 맥락과 기술 목표 포함]

### User Story

[Persona]로서 나는 [행동]을 하고 싶어서 [가치]를 얻고 싶다

### 인수 기준

- [ ] [구체적 테스트 가능 조건 1]
- [ ] [구체적 테스트 가능 조건 2]
- [ ] [구체적 테스트 가능 조건 3]

### 기술 참고

- [구현 고려사항]
- [필요한 API / 서드파티 서비스]
- [관련 파일 경로 또는 모듈]

### 제안 라벨

`[Phase 0]` `[backend]` `[setup]`

---

## TKT-002: [제목]

[동일 형식, 각 티켓에 대해 확장]
```

### 티켓 규칙

1. **티켓-Task 매핑**: TASKS.md의 각 Task는 하나의 티켓에 매핑 (TKT-001 ↔ T0.1); 지나치게 큰 Task는 여러 티켓으로 분할 가능
2. **우선순위 상속**: Phase 0-1은 기본 P0, Phase 2는 기본 P1, Phase 3-4는 기본 P2 — RICE 점수에 따라 조정 가능
3. **의존성**: 티켓 간 의존성을 명시적으로 표시하여 엔지니어가 단계를 건너뛰지 않도록
4. **예상 시간**: Task 세분화 원칙(1-4시간)에 기반하여 합리적인 추정 제공
5. **제안 라벨**: Phase, 기술 도메인(frontend / backend / database / infra), 기능 모듈 포함

### 프로젝트 관리 도구 통합 (예약)

> 다음은 향후 자동 티켓 생성을 위한 예약 인터페이스 설계입니다. 현재 버전은 PM이 수동으로 티켓을 생성하기 위한 TICKETS.md만 작성합니다.

TICKETS.md의 구조화된 형식은 향후 API 임포트를 위해 다음 필드를 예약합니다:

| 필드 | Jira 매핑 | Asana 매핑 | Linear 매핑 |
|------|----------|-----------|------------|
| 티켓 # | Issue Key | Task ID | Issue ID |
| 제목 | Summary | Task Name | Title |
| 설명 | Description | Description | Description |
| 우선순위 | Priority | Custom Field | Priority |
| 예상 시간 | Story Points / Time Estimate | Custom Field | Estimate |
| 의존성 | Linked Issues | Dependencies | Relations |
| 라벨 | Labels + Components | Tags | Labels |
| Phase | Epic | Section | Project |
| 담당자 | Assignee | Assignee | Assignee |
| 인수 기준 | Acceptance Criteria (Description) | Subtasks | Sub-issues |

---

## 기능 분해 로직

MVP 기능을 Tasks로 변환하는 규칙:

### Phase 분할 원칙

```
Phase 0: 프로젝트 스켈레톤 (모든 모드에 필수)
  → 초기화, 린터, DB, 기본 라우팅

Phase 1: Aha Moment까지의 최단 경로 (가장 중요)
  → 사용자 진입부터 Aha Moment까지의 최소 기능
  → 이 경로 상의 P0 기능만 포함

Phase 2: MVP 완성
  → Phase 1에서 다루지 않은 나머지 P0 기능 채우기
  → 부차적 플로우, 지원 페이지

Phase 3: 품질 & 경험
  → 에러 처리, 엣지 케이스, 로딩/빈 상태
  → 기본 보안, 반응형 디자인

Phase 4: 배포
  → 환경 변수, 배포 설정, 모니터링
```

### Task 세분화 원칙

- 각 Task는 **1-4시간** 내에 완료 가능해야 함
- 너무 큰 경우 → 서브 Task로 분할 (T1.1a, T1.1b)
- 너무 작은 경우 → 관련 Task로 병합
- 각 Task는 최소 하나의 테스트 가능한 인수 기준 보유

### User Story → Task 매핑

```
단일 User Story는 1-3개의 Tasks에 매핑될 수 있음:
  US-001: 새 사용자로서 나는 계정을 등록하고 싶어서 제품을 사용할 수 있다
    → T1.1: 등록 페이지 UI
    → T1.2: 등록 API + 데이터 유효성 검증
    → T1.3: 이메일 인증 플로우 (MVP에 필요한 경우)
```
