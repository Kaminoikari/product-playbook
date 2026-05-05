# 📦 Full Mode 단계 시퀀스 (8 Core + 1 기본 ON + 2 Optional, 총 9–11 단계)

> Full Mode의 권위 있는 단계 정의. SKILL.md에서 디스패치됩니다.

**기존 20단계 플로우(v1.0.x)에서 중복된 프레임워크를 통합하고 옵션 단계는 트리거 조건 뒤로 게이팅하여 슬림화되었습니다.** 트리거 로직과 Phase 결정 포인트 형식은 `references/rules-optional-trigger.md`를 참조하세요.

**Journey Map (S3) 관련 안내**: 기본 ON. Persona-Journey는 제품이 0-to-1이든 기존 제품이든 관계없이 번들 페어입니다 — 관련 변수는 사용자의 Job이 여러 단계에 걸쳐 있는지 여부입니다. 상황이 진정으로 너무 단순할 때(단일 API/버튼, 플로우 ≤2 단계, 또는 사용자가 명시적으로 스킵 요청)에만 스킵하세요.

## 단계 시퀀스

```
Phase 0: 전략
  S1.  Strategy Diagnosis  [Core]
       → references/00-opportunity-check.md + references/01-strategy.md
       (통합: Opportunity + DHM + Strategy Blocks + Rumelt Kernel)

Phase 1: 디스커버리
  S2.  Persona (테이블 + 카드)  [Core]
       → references/02a-persona.md
  S3.  User Journey Map  [기본 ON — 상황이 너무 단순한 경우에만 스킵]
       → references/02c-ost-journey.md
  S4.  JTBD 분석  [Core]
       → references/02b-jtbd.md

Phase 2: Define
  S5.  페인포인트 + HMW + 기회 우선순위 평가  [Core]
       → references/03-define.md
       (통합: 페인포인트 요약 + HMW + 기회 평가;
        OST 트리 시각화는 이 단계 내의 옵션 하위 형식)
  S6.  April Dunford Positioning  [Optional — 트리거 참조]
       → references/03-define.md

Phase 3: Develop
  S7.  PR-FAQ (Working Backwards)  [Core]
       → references/04a-prfaq.md
  S8.  솔루션 평가  [Core]
       → references/04b-solutions.md
       (통합: 병렬 프로토타입 + Pre-mortem + GEM + RICE)
  S9.  MVP + Not Doing List  [Core]
       → references/04c-mvp.md

Phase 4: Deliver
  S10. North Star + 3계층 시그널 + Aha Moment  [Core]
       → references/05a-northstar-aha.md
  S11. PMF + GTM + Business Model + 가설 검증 계획  [Optional — 트리거 참조]
       → references/05b-pmf-gtm.md + references/05c-validation-spec.md

────
최종 산출물 → Product Spec Summary (references/05c-validation-spec.md → 4.6) + 최적 진입점 분석
```

> 대상 독자가 경영진 또는 크로스펑셔널 정렬일 경우, S10 앞에 Empowered Teams 프레임워크를 추가하세요.

## Optional 트리거 규칙

권위 있는 트리거 조건과 Phase 결정 포인트 출력 형식은 `references/rules-optional-trigger.md`를 읽으세요.

**빠른 참조:**
- **S3 Journey Map** (기본 ON): 단일 상호작용 지점 / 플로우 ≤2 단계 / 사용자 스킵 요청이 아니면 진행
- **S6 Positioning** (기본 OFF): 신제품 출시 / 재포지셔닝 / 대상 독자에 Sales-BD-Marketing 포함 시 트리거
- **S11 PMF/GTM/BM/Validation** (기본 OFF): 제품 출시 중 / 대상 독자가 경영진 또는 Data Scientist / 사용자가 검증 계획 요청 시 트리거

## Phase 결정 포인트 요건

Phase 1, Phase 2, Phase 4에 진입하기 전, Phase 결정 포인트 블록을 표시하세요(형식은 `rules-optional-trigger.md`에 정의됨). Phase 0과 Phase 3은 Core 단계만 포함하므로 결정 포인트를 건너뜁니다.

## 레퍼런스 로딩 지침

각 단계에 진입할 때만 해당 레퍼런스 파일을 로드하세요(모든 레퍼런스를 사전 로드하지 마세요):

| 단계 | 레퍼런스 파일 |
|------|---------------|
| S1 | `references/00-opportunity-check.md` + `references/01-strategy.md` |
| S2 | `references/02a-persona.md` |
| S3 (트리거 시) | `references/02c-ost-journey.md` |
| S4 | `references/02b-jtbd.md` |
| S5 | `references/03-define.md` |
| S6 (트리거 시) | `references/03-define.md` |
| S7 | `references/04a-prfaq.md` |
| S8 | `references/04b-solutions.md` |
| S9 | `references/04c-mvp.md` |
| S10 | `references/05a-northstar-aha.md` |
| S11 (트리거 시) | `references/05b-pmf-gtm.md` + `references/05c-validation-spec.md` |
| 최종 산출물 | `references/05c-validation-spec.md` |

## 단계 수 요약

| 시나리오 | 단계 수 |
|----------|-------|
| 기본값 (8 Core + S3 Journey ON) | **9** |
| 단순한 플로우 (S3 스킵) | 8 |
| 기본 OFF Optional 1개 트리거 (S6 또는 S11) | 10 |
| 모든 Optional 트리거 | 11 |
| (레거시 20단계 플로우) | 20 |

## 최종 산출물 형식

**최적 진입점 분석** (전체 추론 체인) + **Product Spec Summary**.

Product Spec Summary는 반드시 스킵된 Optional 단계를 공개하고 한 번의 명령으로 다시 추가할 수 있는 경로를 제공해야 합니다(`rules-optional-trigger.md` 섹션 6 참조).

완료 후, `references/rules-end-of-flow.md`에 따라 플로우 종료 규칙을 실행하세요.
