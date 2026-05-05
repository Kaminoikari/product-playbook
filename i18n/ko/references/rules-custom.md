# ✏️ Custom Mode 단계 시퀀스

> Custom Mode의 권위 있는 단계 정의. SKILL.md에서 디스패치됩니다.

완성도 수준을 선택하세요(또는 단계를 직접 선택):

## 🔴 Lean — 4 단계

```
S1. JTBD 진술 → references/02b-jtbd.md
S2. 하나의 HMW → references/03-define.md
S3. PR-FAQ → references/04a-prfaq.md
S4. North Star → references/05a-northstar-aha.md
(사용자가 모든 단계를 다른 프레임워크로 교체할 수 있습니다.)
────
최종 산출물 → Product Spec Summary (미실행 필드는 "미실행"으로 표시)
```

## 🟡 Standard — 8 단계 (Journey Map이 필요할 때 9 단계로 자동 확장)

> Full Mode의 8단계 부분집합: Full Core에서 Strategy Diagnosis를 빼고 Positioning을 추가. Standard 사용자는 일반적으로 깊이 있는 전략 진단보다 시장 포지셔닝이 더 일찍 필요하므로 이렇게 교체했습니다.
>
> **Persona-Journey 조건부 삽입**: S1 (Persona) 완료 후, AI는 `rules-optional-trigger.md` 섹션 2에 따라 Persona-Journey 평가를 실행합니다. 스킵 조건이 충족되지 **않으면**(즉, Job이 여러 단계에 걸쳐 있으면), AI는 **Journey Map을 S1.5로 능동적으로 삽입**하여 9 단계 실행이 됩니다. 사용자는 `-journey`로 답변하여 8 단계로 되돌릴 수 있습니다. 스킵 조건이 충족되면(단일 상호작용 지점 / 플로우 ≤2 단계), 조용히 스킵하고 최종 출력에서 공개합니다.

```
S1.   Persona (테이블 + 카드) → references/02a-persona.md
S1.5  User Journey Map [기본 삽입; 상황이 너무 단순할 때만 스킵]
      → references/02c-ost-journey.md
S2.   JTBD 분석 → references/02b-jtbd.md
S3.   페인포인트 + HMW + 기회 우선순위 평가 → references/03-define.md
S4.   April Dunford Positioning → references/03-define.md
S5.   PR-FAQ → references/04a-prfaq.md
S6.   솔루션 평가 (Parallel + Pre-mortem + GEM + RICE) → references/04b-solutions.md
S7.   MVP + Not Doing List → references/04c-mvp.md
S8.   North Star + 3계층 시그널 + Aha Moment → references/05a-northstar-aha.md
```

## 🟢 Comprehensive — 11 단계

> Full Mode Core + 모든 기본 OFF Optional 트리거됨(Positioning + PMF/GTM/BM/Validation). **S2 Persona 직후 S3 User Journey Map이 이어집니다** — Persona-Journey 번들링 규칙에 따라. 상황이 진정으로 단순한 경우 S3는 스킵될 수 있습니다 — Persona 이후 `-S3`로 답변하면 10 단계로 되돌립니다.

```
S1.  Strategy Diagnosis → references/00-opportunity-check.md + references/01-strategy.md
S2.  Persona (테이블 + 카드) → references/02a-persona.md
S3.  User Journey Map → references/02c-ost-journey.md   ← S2와 번들됨 (기본 ON)
S4.  JTBD 분석 → references/02b-jtbd.md
S5.  페인포인트 + HMW + 기회 우선순위 평가 → references/03-define.md
S6.  April Dunford Positioning → references/03-define.md
S7.  PR-FAQ → references/04a-prfaq.md
S8.  솔루션 평가 (Parallel + Pre-mortem + GEM + RICE) → references/04b-solutions.md
S9.  MVP + Not Doing List → references/04c-mvp.md
S10. North Star + 3계층 시그널 + Aha Moment → references/05a-northstar-aha.md
S11. PMF + GTM + BM + 가설 검증 계획 → references/05b-pmf-gtm.md + references/05c-validation-spec.md
```

## 레퍼런스 로딩 규칙

각 단계에 진입할 때만 해당 레퍼런스 파일을 로드하세요(모든 레퍼런스를 사전 로드하지 마세요). 위의 각 단계에 레퍼런스 경로가 주석으로 표시되어 있습니다.

## Persona-Journey 번들링

`references/rules-optional-trigger.md` 섹션 2와 6에 따라, Custom 프리셋에 Persona 단계가 포함될 때마다 Journey Map은 **기본 ON**입니다:

- **Comprehensive**: Journey Map은 S3로 하드코딩되어 있음(위 시퀀스에 이미 포함됨). 사용자는 Persona 이후 `-S3`로 답변하여 스킵할 수 있습니다.
- **Standard**: 스킵 조건이 충족되지 않을 때(다단계 Job) Journey Map이 **S1.5로 자동 삽입**됩니다. 상황이 너무 단순할 때(단일 상호작용 지점, 플로우 ≤2 단계, 사용자가 스킵 요청) Journey Map은 조용히 스킵되고 최종 출력에서 공개됩니다.
- **Lean**: Persona 단계가 없으므로 이 규칙은 적용되지 않습니다.

스킵 조건 (어느 하나라도 충족되면 → Journey 스킵):
1. 단일 상호작용 지점 (API, 단일 버튼, 백엔드 서비스, 설정 도구)
2. 플로우가 1–2 단계뿐
3. 사용자가 명시적으로 스킵 요청

## 최종 산출물 형식

**Product Spec Summary** (완료된 단계만 통합; 미실행 필드는 "미실행"으로 표시).

완료 후, `references/rules-end-of-flow.md`에 따라 플로우 종료 규칙을 실행하세요.
