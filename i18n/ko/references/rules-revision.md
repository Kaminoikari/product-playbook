# 🔄 Revision Mode 단계 시퀀스 (6 Core + 2 Optional, 총 6–8 단계)

> Revision Mode의 권위 있는 단계 정의. SKILL.md에서 디스패치됩니다.

**기존 12단계 플로우(v1.0.x)에서 중복된 프레임워크를 통합하고 옵션 단계는 트리거 조건 뒤로 게이팅하여 슬림화되었습니다.** 트리거 로직과 Phase 결정 포인트 형식은 `references/rules-optional-trigger.md`를 참조하세요.

## 단계 시퀀스

```
Phase 0: Current State Analysis
  S1.  Current State Review + JTBD Re-validation  [Core]
       (Merged: data inventory + which existing Jobs are done well/poorly)

Phase 1: Problem Convergence
  S2.  User Pain Points Collection  [Core]
       (Retention/churn analysis + feedback synthesis + behavior data)
  S3.  Pain Points + HMW + Opportunity Ranking  [Core]
       → references/03-define.md
       (Merged: Pain Points Summary + HMW + Opportunity Assessment Table)
  S4.  Positioning Re-assessment  [Optional — see triggers]
       → references/03-define.md

Phase 2: Solution Design
  S5.  PR-FAQ (post-revision experience)  [Core]
       → references/04a-prfaq.md
  S6.  Pre-mortem  [Optional — see triggers]
       → references/04b-solutions.md
  S7.  MVP + Not Doing List  [Core]
       → references/04c-mvp.md

Phase 3: Validation
  S8.  North Star + Aha (before/after comparison) + Hypothesis Validation Plan  [Core]
       → references/05a-northstar-aha.md + references/05c-validation-spec.md
       (Merged: any revision must validate hypotheses; tightly coupled)

────
Final output → Product Spec Summary (revision edition)
```

### S1 사전 단계: 제품 컨텍스트 로딩

S1에 진입하기 전, `references/rules-context.md`를 읽고 `.product-context.md`를 확인하세요:

- **완전한 컨텍스트 (시나리오 1)**: PMF 수준, North Star, 알려진 페인포인트, 보안 상태, 가장 최근 3개 Decision History 항목을 자동 입력. S1을 **델타 스타일 안내**로 전환: "지난 평가에서 PMF 수준은 [X], North Star는 [Y]였습니다. 이것들이 변경되었나요? 최신 DAU/MAU와 리텐션 수치는?" — 과거 의사결정과 알려진 페인포인트는 재수집할 필요가 없음.
- **컨텍스트 없음 (시나리오 2)**: Context Bootstrap 트리거(`rules-context.md` 섹션 4, 라운드 1 + 3), 그 다음 표준 S1 데이터 수집으로 진입.
- **부분 컨텍스트 (시나리오 3)**: Decision History에서 기능 변경 이력을 가져옴(어떤 모듈이 변경되었는지, 어떤 리스크가 식별되었는지), 그러나 전체적인 제품 전략과 지표는 질문(이전에는 기능 확장만 수행되었으므로 — 글로벌 뷰가 누락됨).

### S1 표준 안내

> Revision Mode의 S1은 사용자에게 기존 제품 데이터를 능동적으로 요청합니다: DAU/MAU, 리텐션, 주요 사용자 피드백, 이전 버전의 핵심 결정 등. 컨텍스트가 이미 일부 답변을 사전 입력한 경우 재수집이 아닌 확인으로 전환합니다.
> S1은 또한 현재 보안 상태도 수집합니다: 기존 인증/권한 메커니즘, 알려진 보안 갭 또는 기술 부채, 최근 보안 인시던트. 이 데이터는 리비전 리스크 평가와 Pre-mortem(트리거된 경우)에 반영됩니다.

### S1 산출물 요건 (Hard Gates)

모든 Revision Mode S1 응답은 반드시 다음 네 가지를 모두 포함해야 합니다:

1. **0-to-1이 아닌 리비전으로 프레이밍할 것** — 이것이 *기존 제품* 분석임을 명시하는 한두 문장으로 시작하세요: 우리는 현재 데이터에 비추어 기존 JTBD를 재검증하고, 베이스라인 지표를 비교하며, 이전 의사결정을 위해 `.product-context.md`를 읽고 있습니다. 이는 (빈 사용자 모델에서 출발하는) 0-to-1 Discovery와 다릅니다. 이 프레이밍이 없으면 사용자는 왜 질문이 다른지 알 수 없습니다.

2. **사용자의 실제 수치를 그대로 인용할 것** — 사용자의 프롬프트에서 MAU, 리텐션 하락 %, 코호트 규모, 날짜를 분석에 그대로 인용하세요(예: "지난 분기 85%에서 72%로의 하락은 2,800 MAU 기반 대비 약 N명의 영향받은 사용자를 의미합니다…"). 수치를 무시한 일반론적 논의는 이 게이트를 통과하지 못합니다(FAIL).

3. **사용자가 진술한 원인을 사실이 아닌 H1으로 다룰 것** — 사용자가 유력한 원인을 지목할 때("리텐션 하락은 기능 복잡성 때문이다"), 이를 명시적으로 H1로 라벨링하고 동일한 데이터에서 도출한 최소 두 개의 경쟁 가설(H2, H3)을 제시하세요. 고려할 만한 경쟁 가설 예시: 코호트 믹스 변화, 온보딩 회귀, 가격 변경, 경쟁사 출시, 지원 품질 저하, 기능 폐기, 계절적 효과. **사용자가 진술한 원인을 무비판적으로 수용하면 이 게이트를 통과하지 못합니다(FAIL)** — Revision Mode의 가치는 가설 규율에 있습니다.

4. **최소 하나의 세그먼테이션 지향 갭을 포함한 데이터 갭 목록** — H1/H2/H3을 구별하기 위해 추가로 필요한 데이터가 무엇인지 구체적으로 나열하세요. **최소 하나의 항목은 세그먼테이션 갭이어야 합니다**: 코호트(가입 월), 티어(무료/유료), 역할(관리자/사용자), 기능 사용 세그먼트. 일반적인 "더 많은 사용자 인터뷰"만으로는 통과하지 못합니다(FAIL) — *어떤 세그먼트*를 인터뷰할지, *무엇을 구체적으로* 물을지 명시하세요.

### S1 마무리 형식 (Hard Gate)

S1 응답은 개방형 질문이 아닌, 번호가 매겨진 CTA 메뉴로 끝내세요. 다음의 정확한 형태를 사용하세요:

```
What's next? Pick one:
  1️⃣ Share the requested data so we can move to S2 (pain-point convergence with hypothesis testing)
  2️⃣ Refine the hypothesis list before collecting data (suggest more H_n candidates)
  3️⃣ Skip to S3 if you already have enough data to converge on a top hypothesis
  4️⃣ Pause and resume later (progress will be saved to .product-playbook-progress.md)
```

번호 메뉴 없이 "Any thoughts?" / "Let me know what you think" / "Share what you have"로 끝나는 응답은 계약을 위반합니다(FAIL) — 사용자는 다음 행동을 위한 명확한 핸들이 필요합니다.

### Fast Path

사용자가 S1에서 충분한 데이터(피드백, 지표, 우선순위 포함)를 제공하면, S3은 여러 번 확인하는 대신 한 번의 왕복으로 산출될 수 있습니다. 트리거 조건: S2에서 수집된 페인포인트 목록에 이미 명시적인 우선순위와 데이터 뒷받침이 있는 경우. Hard Gate 규칙은 유지됨 — 각 단계의 산출물은 여전히 완전히 제시되어야 하며, 확인 리듬만 가속됩니다.

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