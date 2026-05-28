# 1단계: 디스커버리 — Persona 구축

### 🚫 디스커버리 출력 범위 (Hard Gate)

orchestrator 가 디스커버리 작업(Persona, JTBD, OST, Journey Map, Continuous Discovery)을 수행하도록 요청받을 때, 출력은 **디스커버리 범위 안에 머물러야 합니다**. 디스커버리는 "사용자가 누구인가", "그들이 충족하려는 미충족 니즈는 무엇인가"에 답합니다 — 그 외에는 다루지 않습니다. 다음 하류 단계의 산출물은 자연스러워 보이더라도 **디스커버리 결과물에 절대 등장해서는 안 됩니다**:

- **Define 단계 산출물**: positioning statement, HMW (How Might We) 질문, 솔루션 프롬프트 역할을 겸하는 페인포인트 매트릭스
- **Develop 단계 산출물**: PR-FAQ 초안, pre-mortem 시나리오, RICE 테이블, MVP scope 정의, PRD 섹션, 기능 목록
- **Deliver 단계 산출물**: North Star 메트릭 정의, PMF 기준, GTM 계획, 비즈니스 모델 블록, 제품 사양 표
- **Strategy 단계 산출물**: Strategy Blocks, Rumelt 의 diagnosis / guiding-policy / coherent-action, DHM Model 분해, OKR 계층

디스커버리 발견이 하류 산출물을 강력히 시사하는 경우(예: JTBD 분석에서 명확한 포지셔닝 각도 부상), 끝에 **한 줄짜리 open question 또는 next-step pointer**로 기록 — 직접 그 산출물을 만들지 마세요. 다음 단계에 전용 스텝이 있습니다.

불합격 예: JTBD 분석 끝에 채워진 RICE 테이블, MVP scope 목록, 또는 "Recommended Positioning" 단락 추가 — 다른 디스커버리 하위 섹션이 모두 올바르더라도 이 출력은 Hard Gate 에 FAIL.

---

## Continuous Discovery Habits (Teresa Torres)

하나의 핵심 습관을 구축하세요: **매주 최소 한 명의 타겟 사용자와 대화하기.** 디스커버리는 일회성 의식이 아니라 지속적인 시스템입니다.

> "제품 디스커버리는 프로젝트 시작 전 일회성 의식이 아닌, 지속적인 습관이어야 합니다." — Teresa Torres

## 1.1 Persona 테이블 구축

Persona는 나이와 성별이 아닌 **목적 / 과업 / 동기**로 구분하여 다양한 유형의 사용자를 식별합니다.

### 🏢 B2B Hard Gate — Buyer Persona ≠ User Persona

모든 B2B (또는 B2B2C) 제품에서, **Buyer** (계약 체결, 예산 관리, 벤더 리스크 보유) 와 **일상 User** (매일 제품 사용) 는 거의 항상 **목표, 페인포인트, 의사결정 기준이 다른** 별개의 역할입니다. 이들을 하나의 Persona 로 합치는 것은 두 개의 다른 Job 을 하나의 모호한 아키타입에 강제로 욱여넣는 것이며, 분석 결과는 제품 의사결정을 이끌어낼 수 없습니다.

Hard Gate 규칙:
- B2B 에서는 두 역할이 명확히 다를 때 (B2B 기본 가정) `Buyer` 와 `User` 라벨이 붙은 **두 개의 별개 Persona 블록**을 생성하는 것이 기본.
- 동일 인물인 경우 (드문 예외 — 보통 창업자 주도 도구 또는 1인 B2B), "왜 이 시나리오에서 Buyer 가 일상 User 이기도 한지" 한 문장으로 명시.
- 두 Persona 간 크로스링크: Buyer 의 평가 기준이 User 의 일상 행동에 어디서 의존하는지 표기 (예: "Buyer 의 감사 준비 기준은 User 가 당일에 양식을 작성하느냐에 달려 있음 — 사후 일괄 작성이 아니라").

불합격 예: 하나의 Persona ("HR 매니저") 만 생성하여 "예산 승인" 과 "매일 휴가 양식 작성" 이라는 두 개의 다른 Job 을 하나의 모호한 아키타입에 욱여넣음 — 이 출력은 Hard Gate 에 FAIL.

```
| 항목 | Persona 1: [별칭] | Persona 2: [별칭] | Persona 3: [별칭] |
|------|---|---|---|
| 목적 / 과업 / 동기 | | | |
| 규모 (SCALE) | | | |
| 문제 / 과제 / 동인 | | | |
| 현재 접근법 및 이유 | | | |
| 빈도 | | | |
| 정보 소스 | | | |
| 채택 / 실행 장벽 | | | |
```

세분화 논리를 설명하고; MECE (상호 배타적이고 전체를 아우르는지) 확인; 1차 TA와 2차 TA를 식별하세요.

### 🎯 Persona 우선순위 reasoning (Hard Gate)

"1차 TA 를 식별한다"고만 말하고 구체적 reasoning 이 없으면 이 Hard Gate 에 불합격입니다. 우선순위 진술은 **한 개의** Persona 를 1차로 지정하고, 왜 그런지 **해당 제품의 go-to-market 다이내믹스에 특화된 언어**로 설명해야 합니다 — 일반적인 "사용 빈도가 높다" 같은 이유가 아니라.

여러 user persona 가 있는 **B2B 제품**에서, reasoning 은 다음 B2B 특유 다이내믹스 중 **최소 하나**를 이름으로 참조해야 합니다 (이 용어 또는 명확히 동등한 개념 사용):

- **Champion vs Buyer** — 조직 내부에서 누가 채택을 옹호하느냐 vs 누가 계약에 서명하느냐; champion-led adoption 은 B2B 우선순위에서 보통 이기며, buyer 가 "더 시니어" 한 persona 라도 그렇다
- **Adoption multiplier** — 누구의 채택이 조직 전체 확산을 잠금 해제하는가 (예: HR Specialist 의 일일 사용은 다른 persona 가 나중에 의존하는 system-of-record 의 씨앗을 뿌림)
- **Switching-trigger ownership** — 어떤 persona 가 기존 도구에서 전환을 정당화하는 고통을 느끼는가; switching trigger 를 소유한 persona 는 최다 사용자가 아니어도 우선순위 후보
- **Budget authority** — 누가 예산 항목을 통제하는가; buyer ≠ user 일 때 관련, buyer 의 평가 기준이 초기 거래 결정을 지배
- **Audit / compliance pressure ownership** — 감사 발견이 발생할 때 누구의 역할이 위험에 처하는가; 규제 B2B segment 에서는 컴플라이언스 압력을 받는 persona 가 우선순위를 지배하는 경우가 많음

순수한 "Persona X 는 사용 빈도가 높다" 또는 "Persona Y 는 사용자 수가 많다" 식 reasoning 은 B2B 제품에 대해 이 Hard Gate 에 FAIL. 빈도는 필요조건이지만 결코 충분조건이 아닙니다 — B2B 전환은 조직 수준의 압력에 의해 구동되지, 개별 사용률에 의해 구동되지 않습니다.

**B2C 제품**의 경우, reasoning 은 다음 중 최소 하나를 참조해야 합니다: switching-trigger ownership, JTBD severity differential, network-effect seeding, willingness-to-pay differential. 순수 빈도 reasoning 은 B2C 에도 FAIL.

### 📝 Persona 품질 체크리스트
- ✅ 세분화가 인구통계가 아닌 "목적/과업/동기" 기반인가?
- ✅ Persona가 MECE인가 (타겟 시장에서 상호 배타적이고 전체를 아우르는가)?
- ✅ 1차 TA vs. 2차 TA가 명확히 식별되었는가?
- ✅ 각 Persona의 "문제/과제"가 실제 관찰이나 합리적 추론에 기반하는가?
- ✅ "현재 접근법 및 이유"가 우회 방법을 식별할 수 있을 만큼 구체적인가?
- ❌ 흔한 문제: 나이/성별로 세분화, Persona 간 차이 미미, 페인포인트가 너무 모호

## 1.2 Persona 카드 구축

```
## [Persona 별칭]: [한 줄 설명]

**기본 정보**: 나이 / 성별 / 직업 / 지역 / 성격 특성
**배경**: [제품 관련 배경 설명]
**목표 / 과업**: [목표 1], [목표 2]
**현재 접근법 및 이유**: [현재 하고 있는 것과 그 이유]
**정보 소스**: [관련 정보를 얻는 곳]
**장벽 / 문제 / 과제 / 불만**: [페인포인트 1], [페인포인트 2], [페인포인트 3]
```

---

## 📎 이 단계의 파일 통합 팁

이 단계에서 사용자가 파일을 업로드하면, Claude는 다음 규칙에 따라 통합합니다:

| 업로드 내용 | 통합 대상 | 통합 작업 |
|------------|----------|----------|
| 사용자 인터뷰 녹취록 / 음성 전사 | 1.1 Persona + 1.3 JTBD | 추출: 사용자 배경 → Persona 항목; 페인포인트 + 현재 접근법 → JTBD 심층 질문; 감정적 반응 → 감정적/사회적 Job |
| 사용자 리서치 보고서 (PDF) | 1.1 + 1.2 + 1.3 | 정량 데이터(사용자 세그먼트 비율)를 Persona 규모에 추출; 정성적 인사이트를 JTBD에 추출 |
