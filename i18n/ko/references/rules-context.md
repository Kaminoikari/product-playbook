# 📦 제품 컨텍스트 축적 규칙

> SKILL.md 시작 시 로드. 모든 결정 로직(언제/어느 것/어떻게)을 포함. 상세 YAML 형식과 전체 UX 스크립트는 `rules-context-template.md`에 있음 (실제로 파일을 쓰거나 Bootstrap을 실행할 때만 지연 로드).

## 1. 파일 생명주기

- **경로**: 프로젝트 루트의 `.product-context.md` (`.product-playbook-progress.md`와 같은 레벨)
- **영구 보존**: 세션 간 지속
- **최초 생성 시**: 사용자에게 `.gitignore`에 추가하도록 알림 (민감한 전략 정보 포함 가능)

---

## 2. 세 가지 시나리오 감지 (시작 시)

진행 파일 점검 후, 모드 선택 전:

| 조건 | 시나리오 | 행동 |
|------|---------|------|
| 파일 존재, `Core Strategy`에 실제 내용 있음 | **1. 완전** | 조용히 로드. 표시: "📦 **[제품명]**의 제품 컨텍스트가 감지되었습니다 — 이번 세션의 기준선으로 사용됩니다." |
| 파일이 존재하지 않음 | **2. 없음** | 상태 기록. 기능 확장 / 리비전 진입 시 Bootstrap 트리거. → 템플릿 §Bootstrap 로드 |
| 파일 존재, Core Strategy 비어있거나 플레이스홀더, Decision History에 1개 이상 항목 | **3. 부분** | 알려진 정보 요약 + 보완 옵션 표시. → 템플릿 §Partial 로드 |

**감지 로직:**
1. 파일이 존재하는가?
2. `Identity`에 제품명이 있는가 (플레이스홀더 아님)?
3. `Core Strategy`에 핵심 JTBD가 있는가 (플레이스홀더 아님)? → 예 = 시나리오 1
4. `Decision History`에 `###` 항목이 있는가? → 예이지만 3이 아니오 = 시나리오 3

---

## 3. 자동 읽기 규칙 (각 모드의 S1 사전 단계)

**관련 섹션만 주입** — 사용자에게 전체 파일을 표시하지 마세요:

| 모드 + 단계 | 주입되는 섹션 |
|------------|-------------|
| 기능 확장 S1 | Identity, Architecture & Tech Stack, 가장 최근 3개 Decision History |
| 리비전 S1 | Identity, Core Strategy, Accumulated Insights (페인포인트, PMF, 보안), 가장 최근 3개 Decision History |
| Full/Quick/Build S1 | Identity만 (제품명, 유형, 원라이너) |
| 모든 모드의 Pre-mortem | 보안 상태 + 기술 부채 (Accumulated Insights에서) |

**비대화 제어**: Decision History는 기본적으로 가장 최근 3개 항목. 사용자가 더 많이 요청 가능.

---

## 4. 빈 섹션 건너뛰기 규칙

| 섹션 | 기능 확장 | 리비전 | Full/Quick/Build |
|------|----------|--------|-----------------|
| Identity | 필수 (누락 시 Bootstrap) | 필수 (누락 시 Bootstrap) | 플로우가 생성 |
| Core Strategy | 건너뛸 수 있음 | 필수 (누락 시 S1에서 빠른 Q&A) | 플로우가 생성 |
| Architecture & Tech Stack | 필수 (Bootstrap 또는 자동 감지) | 건너뛸 수 있음 | 플로우가 생성 |
| Decision History | 건너뛸 수 있음 | 있으면 포함, 없으면 건너뛰기 | 플로우가 생성 |
| Accumulated Insights | 건너뛸 수 있음 | 있으면 포함, 없으면 건너뛰기 | 플로우가 생성 |

**원칙**: 빈 섹션은 플로우를 차단하지 않음. "필수" + 비어있는 섹션만 수집을 트리거.

---

## 5. 자동 쓰기 규칙 (플로우 종료 시)

`rules-end-of-flow.md` 종료 조건과 동기화. 컨텍스트 자동 추출:

| 플로우 유형 | 작성/업데이트되는 섹션 |
|-----------|---------------------|
| Quick | Identity, Core Strategy (JTBD + North Star), History에 추가 |
| Full | 모든 섹션 (Identity/Strategy/Insights 덮어쓰기, History에 추가) |
| Revision | Core Strategy 업데이트 (재포지셔닝 시), Insights 업데이트, History에 추가 |
| Feature Extension | Architecture 병합, History에 추가 (기능 템플릿) |
| Custom | 완료된 단계에 해당하는 섹션 업데이트 |
| Build | Identity, Core Strategy (부분), History에 추가 |

### 섹션별 쓰기 전략

| 섹션 | 전략 |
|------|------|
| Identity | 최신으로 덮어쓰기 |
| Core Strategy | 최신으로 덮어쓰기 (리비전 후가 리비전 전을 대체) |
| Architecture & Tech Stack | 병합 (새 모듈 추가, 기존 모듈 유지) |
| Decision History | 추가 전용 (이전 항목 절대 삭제 금지) |
| Accumulated Insights | 병합 및 중복 제거 (페인포인트/피드백 중복 제거; PMF/보안 덮어쓰기) |

처음 쓸 때 (파일 생성) 또는 Decision History 추가 시 → **`rules-context-template.md` §File Format / §Append Templates 로드**.

완료 표시: `✅ 제품 컨텍스트가 '.product-context.md'에 업데이트되었습니다 — 다음 세션에서 자동 로드됩니다.`

---

## 6. 충돌 처리 (요약)

| 충돌 유형 | 해결 |
|----------|------|
| 사용자가 기존 컨텍스트 수정 | 최신 우선 — 직접 덮어쓰기 |
| 컨텍스트가 코드베이스와 충돌 (예: package.json 차이) | 자동 덮어쓰기 금지 — 사용자에게 질문. → 템플릿 §Conflict UX 로드 |
| 플로우 데이터가 기존 컨텍스트와 다름 | 플로우 데이터 우선 — 플로우 종료 시 자동 덮어쓰기 |

---

## 7. 언어 설정 (요약)

컨텍스트 생성/업데이트 시 `Language Preference` 섹션에 기록:
- **설치 언어**: `.lang` 파일 또는 사용자 로케일에서
- **사용자 선호 언어**: 사용자가 소통에 사용하는 언어

로드 시: 기록되어 있으면 해당 언어로 세션 계속.
쓰기 시: Bootstrap 중 또는 파일을 처음 생성하는 플로우 종료 시 기록. 사용자가 세션 중 언어 전환 시 업데이트.

---

## 8. `rules-context-template.md` 로드 시점

다음 트리거 중 하나가 발동될 때만:

| 트리거 | 템플릿 섹션 |
|--------|-----------|
| 시나리오 2 + 기능 확장 / 리비전 진입 | §Bootstrap, §File Format |
| 시나리오 3 (부분 컨텍스트) | §Partial Context, §File Format |
| 컨텍스트를 처음 쓰기 | §File Format |
| 플로우 종료 시 Decision History 추가 | §Append Templates |
| 코드베이스 충돌 감지 | §Conflict UX |
| Bootstrap 완료 → baseline 쓰기 | §File Format |

시작 시 템플릿을 사전 로드하지 마세요.
