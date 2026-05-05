# 🔄 Revision Mode 단계 시퀀스 (6 Core + 2 Optional, 총 6–8 단계)

> Revision Mode의 권위 있는 단계 정의. SKILL.md에서 디스패치됩니다.

**기존 12단계 플로우(v1.0.x)에서 중복된 프레임워크를 통합하고 옵션 단계는 트리거 조건 뒤로 게이팅하여 슬림화되었습니다.** 트리거 로직과 Phase 결정 포인트 형식은 `references/rules-optional-trigger.md`를 참조하세요.

## 단계 시퀀스

```
Phase 0: 현상 분석
  S1.  현상 리뷰 + JTBD 재검증  [Core]
       (통합: 데이터 인벤토리 + 어떤 기존 Job이 잘/못 수행되고 있는가)

Phase 1: 문제 수렴
  S2.  사용자 페인포인트 수집  [Core]
       (리텐션/이탈 분석 + 피드백 종합 + 행동 데이터)
  S3.  페인포인트 + HMW + 기회 우선순위 평가  [Core]
       → references/03-define.md
       (통합: 페인포인트 요약 + HMW + 기회 평가 테이블)
  S4.  Positioning 재평가  [Optional — 트리거 참조]
       → references/03-define.md

Phase 2: 솔루션 설계
  S5.  PR-FAQ (리비전 후 경험)  [Core]
       → references/04a-prfaq.md
  S6.  Pre-mortem  [Optional — 트리거 참조]
       → references/04b-solutions.md
  S7.  MVP + Not Doing List  [Core]
       → references/04c-mvp.md

Phase 3: 검증
  S8.  North Star + Aha (전후 비교) + 가설 검증 계획  [Core]
       → references/05a-northstar-aha.md + references/05c-validation-spec.md
       (통합: 모든 리비전은 가설을 검증해야 하며 긴밀히 결합되어 있음)

────
최종 산출물 → Product Spec Summary (리비전 에디션)
```

### S1 사전 단계: 제품 컨텍스트 로딩

S1에 진입하기 전, `references/rules-context.md`를 읽고 `.product-context.md`를 확인하세요:

- **완전한 컨텍스트 (시나리오 1)**: PMF 수준, North Star, 알려진 페인포인트, 보안 상태, 가장 최근 3개 Decision History 항목을 자동 입력. S1을 **델타 스타일 안내**로 전환: "지난 평가에서 PMF 수준은 [X], North Star는 [Y]였습니다. 이것들이 변경되었나요? 최신 DAU/MAU와 리텐션 수치는?" — 과거 의사결정과 알려진 페인포인트는 재수집할 필요가 없음.
- **컨텍스트 없음 (시나리오 2)**: Context Bootstrap 트리거(`rules-context.md` 섹션 4, 라운드 1 + 3), 그 다음 표준 S1 데이터 수집으로 진입.
- **부분 컨텍스트 (시나리오 3)**: Decision History에서 기능 변경 이력을 가져옴(어떤 모듈이 변경되었는지, 어떤 리스크가 식별되었는지), 그러나 전체적인 제품 전략과 지표는 질문(이전에는 기능 확장만 수행되었으므로 — 글로벌 뷰가 누락됨).

### S1 표준 안내

> Revision Mode의 S1은 사용자에게 기존 제품 데이터를 능동적으로 요청합니다: DAU/MAU, 리텐션, 주요 사용자 피드백, 이전 버전의 핵심 결정 등. 컨텍스트가 이미 일부 답변을 사전 입력한 경우 재수집이 아닌 확인으로 전환합니다.
> S1은 또한 현재 보안 상태도 수집합니다: 기존 인증/권한 메커니즘, 알려진 보안 갭 또는 기술 부채, 최근 보안 인시던트. 이 데이터는 리비전 리스크 평가와 Pre-mortem(트리거된 경우)에 반영됩니다.

### Fast Path

사용자가 S1에서 충분한 데이터(피드백, 지표, 우선순위 포함)를 제공하면, S3은 여러 번 확인하는 대신 한 번의 왕복으로 산출될 수 있습니다. 트리거 조건: S2에서 수집된 페인포인트 목록에 이미 명시적인 우선순위와 데이터 뒷받침이 있는 경우. 하드 게이트 규칙은 유지됨 — 각 단계의 산출물은 여전히 완전히 제시되어야 하며, 확인 리듬만 가속됩니다.

## Optional 트리거 규칙

권위 있는 트리거 조건과 Phase 결정 포인트 출력 형식은 `references/rules-optional-trigger.md`를 읽으세요.

**빠른 참조:**
- **S4 Positioning 재평가**는 다음과 같을 때 트리거됨: 사용자가 "포지셔닝 표류" / "시장 변화"를 언급 / 대상 독자에 Sales/Marketing 포함
- **S6 Pre-mortem**은 다음과 같을 때 트리거됨: 변경 범위가 기존 기능의 30% 이상 / 결제-권한-데이터 마이그레이션과 관련

## Phase 결정 포인트 요건

Phase 1과 Phase 2에 진입하기 전, Phase 결정 포인트 블록을 표시하세요(형식은 `rules-optional-trigger.md`에 정의됨). Phase 0과 Phase 3은 Core 단계만 포함하므로 결정 포인트를 건너뜁니다.

## 레퍼런스 로딩 지침

| 단계 | 레퍼런스 파일 |
|------|---------------|
| S1–S2 | (외부 레퍼런스 없음; 사용자에게 직접 데이터 수집) |
| S3 | `references/03-define.md` |
| S4 (트리거 시) | `references/03-define.md` |
| S5 | `references/04a-prfaq.md` |
| S6 (트리거 시) | `references/04b-solutions.md` |
| S7 | `references/04c-mvp.md` |
| S8 + 최종 산출물 | `references/05a-northstar-aha.md` + `references/05c-validation-spec.md` |

## 단계 수 요약

| 시나리오 | 단계 수 |
|----------|-------|
| 기본값 (Core만) | **6** |
| 모든 Optional 트리거 | 8 |
| (레거시 12단계 플로우) | 12 |

## 최종 산출물 형식

**리비전 Product Spec Summary**: 전후 비교 + 변경할 것 / 변경하지 않을 것 + 성공 지표.

요약은 반드시 건너뛴 Optional 단계를 공개하고 한 번의 명령으로 다시 추가할 수 있는 경로를 제공해야 합니다(`rules-optional-trigger.md` 섹션 6 참조).

완료 후, `references/rules-end-of-flow.md`에 따라 플로우 종료 규칙을 실행하세요.
