[English](README.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [Español](README.es.md) | [한국어](README.ko.md)

# 🎯 The Product Playbook

**세계 수준의 제품 기획 AI 스킬 — 아이디어에서 개발까지, 하나의 프레임워크로 모든 것을**

[![npm version](https://img.shields.io/npm/v/product-playbook.svg)](https://www.npmjs.com/package/product-playbook)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://code.claude.com)
[![Claude.ai](https://img.shields.io/badge/Claude.ai-Custom%20Skill-blue)](https://claude.ai)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![i18n](https://img.shields.io/badge/i18n-6%20languages-green)](README.md)

> Lenny's Podcast에서 소개된 가장 영향력 있는 PM 프레임워크(Teresa Torres, Shreyas Doshi, Gibson Biddle, April Dunford, Todd Jackson, Marty Cagan, Richard Rumelt 등)를 통합하여 — AI를 당신의 시니어 프로덕트 매니저 코치로 변환합니다.

---

## ✨ 이것은 무엇인가요?

The Product Playbook은 제로부터 원까지 제품 기획 전 과정을 체계적으로 안내하는 **Claude AI 스킬**입니다. 단순한 프롬프트가 아니라 다음을 포함하는 완전한 대화형 프레임워크 가이드 시스템입니다:

- 🧭 **6가지 실행 모드** — 30분 빠른 검증부터 전체 제품 기획까지 (기능 확장 빠른 트랙 포함)
- 📐 **22개 제품 프레임워크** — Discovery → Define → Develop → Deliver 전체 파이프라인 커버
- 🤝 **3개 전문 서브에이전트** — Discovery, 전략 비평, Pre-mortem이 격리된 context window에서 작동하며 프레임워크별 전문성을 보유
- 🔄 **변경 전파 엔진** — 어떤 단계든 수정하면 모든 하위 산출물이 자동 업데이트
- 📎 **스마트 파일 통합** — 데이터, 스크린샷, 문서를 업로드하면 AI가 해당 단계에 자동 통합
- 🔗 **개발 핸드오프** — CLAUDE.md + TASKS.md + TICKETS.md를 생성하여 Claude Code 개발로 원활하게 연결
- 📊 **다중 형식 출력** — PDF(북마크 포함), HTML 보고서, Word 문서, PowerPoint 덱, 개발 핸드오프 패키지
- 📄 **스마트 문서 가져오기** — 3단계 PDF 파싱(텍스트 추출 → Claude Vision → OCR 폴백), DOCX/PPTX 지원

**한 문장으로 전체 플로우를 트리거하세요:**

```
제품을 만들고 싶어요
```

---

## 🎬 데모

<p align="center">
  <img src="assets/demo-build-ko.gif" alt="The Product Playbook 데모 — 빌드 모드" width="800">
</p>

> 위 데모는 **빌드 모드**를 보여줍니다: 요구사항 설명 → 코드베이스 스캔 → 기술 스택 감지 → 프레임워크를 적용하여 문제 명확화, 그 후 솔루션 설계로 바로 진행.

---

## 🚀 빠른 시작

### 옵션 1: Claude.ai 커스텀 스킬

1. 이 레포를 zip 파일로 다운로드
2. [Claude.ai](https://claude.ai) → 설정 → 커스텀 스킬로 이동
3. `product-playbook/` 전체 폴더 업로드
4. 대화에서 "제품을 만들고 싶어요"라고 말하면 스킬이 트리거됩니다

### 옵션 2: Claude Code Plugin

Claude Code에서 실행:

```
/plugin marketplace add kaminoikari/product-playbook
/plugin install product-playbook@kaminoikari-product-playbook
```

> 첫 번째 명령어로 marketplace를 추가하고(최초 1회), 두 번째로 plugin을 설치합니다.

### 옵션 3: Claude Code 스킬 (권장)

> 💡 업데이트하려면: 설치 명령을 다시 실행하면 최신 버전으로 덮어쓰기됩니다.

| 방법 | 적합한 사용자 | 필요사항 |
|------|------------|---------|
| ① 복사 & 붙여넣기 | 초보자 | Claude Code만 열면 됨 |
| ② 원라인 설치 | 개발자 | 터미널 |
| ③ 수동 설치 | 맞춤 경로 | 터미널 + git |

#### ① 복사 & 붙여넣기 설치 (가장 쉬움)

Claude Code를 실행한 후 다음을 붙여넣으면 Claude가 자동으로 설치를 처리합니다:

```
다음 명령을 실행하여 product-playbook 스킬을 설치(또는 업데이트)하고,
완료되면 결과를 알려주세요:

git clone https://github.com/kaminoikari/product-playbook.git /tmp/product-playbook
mkdir -p ~/.claude/skills ~/.claude/commands
cp -r /tmp/product-playbook ~/.claude/skills/product-playbook
cp /tmp/product-playbook/commands/* ~/.claude/commands/
rm -rf /tmp/product-playbook
```

#### ② 원라인 설치 (터미널)

```bash
# curl
curl -fsSL https://raw.githubusercontent.com/kaminoikari/product-playbook/main/install.sh | bash

# npx (Node.js 필요)
npx product-playbook
```

제거:

```bash
curl -fsSL https://raw.githubusercontent.com/kaminoikari/product-playbook/main/install.sh | bash -s -- --uninstall
# 또는
npx product-playbook --uninstall
```

#### ③ 수동 설치

```bash
git clone https://github.com/kaminoikari/product-playbook.git
mkdir -p ~/.claude/skills ~/.claude/commands
cp -r product-playbook ~/.claude/skills/product-playbook
cp product-playbook/commands/* ~/.claude/commands/
```

설치 후, Claude Code에서 트리거:

```bash
# 메인 스킬 명령
> /product-playbook

# 슬래시 명령 (설치 후 사용 가능)
> /product-quick 가계부 앱을 만들고 싶어요
> /product-full 반려동물 소셜 플랫폼
> /product-revision 이커머스 결제 플로우 재설계

# 또는 자연어
> 제품을 기획하고 싶어요
> JTBD로 내 제품을 분석해 주세요
> MVP 기획을 도와주세요
```

---

## 📦 파일 구조

```
product-playbook/
├── SKILL.md                          # 코어 엔진: 모드 정의, 단계 시퀀스, 명령 시스템
├── LICENSE                           # MIT 라이선스
├── README.md                         # 영문 README
├── README.zh-TW.md                   # 중국어 번체 README
├── assets/
│   └── demo.gif                      # README 데모 애니메이션
├── commands/                         # Claude Code CLI 슬래시 명령 (선택적 설치)
│   ├── product-quick.md              # /product-quick — 퀵 모드
│   ├── product-full.md               # /product-full — 풀 모드
│   ├── product-revision.md           # /product-revision — 리비전 모드
│   ├── product-build.md              # /product-build — 빌드 모드
│   ├── product-feature.md            # /product-feature — 기능 확장 모드
│   ├── product-prd.md                # /product-prd — PRD 생성
│   ├── product-report.md             # /product-report — HTML 보고서 생성
│   └── product-dev.md                # /product-dev — 개발 핸드오프 패키지 생성
├── agents/                           # 전문 서브에이전트 (Claude Code 플러그인이 자동 로드)
│   ├── discovery-specialist.md       # Persona / JTBD / OST / Journey Map 스페셜리스트
│   ├── strategy-critic.md            # Rumelt 관점의 전략 비평가
│   └── pre-mortem-runner.md          # 15+ 실패 시나리오 + 선행 지표
└── references/
    ├── 00-opportunity-check.md       # 기회 평가 + DHM Model
    ├── 01-strategy.md                # Strategy Blocks + Rumelt + OKR
    ├── 02-discovery.md               # Persona + JTBD + OST + Journey Map
    ├── 03-define.md                  # 페인포인트 + 포지셔닝 + HMW + 기회 평가
    ├── 04-develop.md                 # PR-FAQ + Pre-mortem + RICE + MVP + PRD
    ├── 05-deliver.md                 # North Star + PMF + GTM + 비즈니스 모델 + 제품 스펙
    ├── 06-html-report.md             # HTML 기획 보고서 출력 사양
    ├── 07-dev-handoff.md             # 개발 핸드오프: CLAUDE.md + TASKS.md + Architecture
    ├── 08-security-checklist.md      # OWASP Top 10 + CORS + CSP + 보안 아키텍처
    ├── rules-context.md              # 세션 간 제품 컨텍스트 축적 규칙
    ├── rules-document-tools.md       # 문서 변환 도구 의존성 관리
    ├── rules-import-document.md      # 3단계 PDF 파싱 + DOCX/PPTX 가져오기
    ├── rules-export-document.md      # 다중 형식 내보내기(PDF/DOCX/PPTX)
    ├── rules-*.md                    # 모드 단계 규칙 + 진행/변경/파일 통합 규칙
    └── templates/
        ├── prd-style.css             # 전문 인쇄 등급 CSS(PDF 내보내기용)
        └── report-style.css          # 인쇄 최적화 CSS(HTML 보고서 → PDF)
```

---

## 🧭 6가지 실행 모드

| 모드 | 단계 | 소요 시간 | 적합한 경우 |
|------|------|---------|-----------|
| 🚀 **퀵 모드** | 3단계 | ~30분 | 빠른 아이디어 검증, 피칭 준비 |
| 📦 **풀 모드** | 9–11단계 (8 Core + 1 기본 ON Journey Map + 2 기본 OFF Optional) | 1-2시간 | 신규 제품 기획, 대규모 개편 |
| 🔄 **리비전 모드** | 6–8단계 (6 Core + 2 Optional) | <1시간 | 기존 제품 반복 개선 |
| ✏️ **커스텀 모드** | 4-16단계 | 다양 | 특정 부분 보완 |
| ⚡ **빌드 모드** | 7단계 | ~1시간 | 문제가 명확한 경우, 솔루션으로 바로 |
| 🔧 **기능 확장** | 4단계 | ~30분 | 기존 제품에 단일 기능 추가 |

---

## 📐 포함된 프레임워크

### 사용자 이해
| 프레임워크 | 창시자 | 목적 |
|-----------|--------|------|
| JTBD (Jobs to Be Done) | Clayton Christensen | 사용자가 정말로 완수하려는 과업 발견 |
| Persona | — | 과업/동기 기반 사용자 아키타입 |
| User Journey Map | — | 엔드투엔드 사용자 경험 매핑 |
| Continuous Discovery | Teresa Torres | 매주 사용자와 대화하는 습관 |
| OST (Opportunity Solution Tree) | Teresa Torres | 기회와 솔루션을 체계적으로 연결 |

### 문제 정의
| 프레임워크 | 창시자 | 목적 |
|-----------|--------|------|
| 포지셔닝 | April Dunford | 경쟁 맥락과 차별화 |
| HMW (How Might We) | — | 페인포인트를 디자인 과제로 변환 |

### 솔루션 설계
| 프레임워크 | 창시자 | 목적 |
|-----------|--------|------|
| Working Backwards / PR-FAQ | Amazon | 고객 성과에서 시작하여 역으로 작업 |
| Pre-mortem | Shreyas Doshi | 실패가 발생하기 전에 예측하고 방지 |
| GEM Model | Gibson Biddle | Growth / Engagement / Monetization 우선순위 |
| RICE Scoring | Intercom | 정량적 기능 우선순위 결정 |
| MVP 정의 | — | 최소 실행 가능한 제품 범위 |

### 전략
| 프레임워크 | 창시자 | 목적 |
|-----------|--------|------|
| Strategy Blocks | Chandra Janakiraman | Mission → Vision → Strategy 계층 |
| 좋은 전략의 핵심 | Richard Rumelt | 진단 → 방침 → 일관된 행동 |
| DHM Model | Gibson Biddle | Delight / Hard to copy / Margin-enhancing |
| Empowered Teams | Marty Cagan | 임파워드 팀 vs. 기능 팀 |

### 측정 & 딜리버리
| 프레임워크 | 창시자 | 목적 |
|-----------|--------|------|
| North Star Metric | Sean Ellis / Amplitude | 핵심 사용자 가치를 대표하는 단일 지표 |
| 4단계 PMF 프레임워크 | Todd Jackson | Product-Market Fit 평가 |
| Sean Ellis Score | Sean Ellis | PMF 열정 정량화 |
| GTM 전략 | — | Go-to-Market 출시 및 획득 |
| 비즈니스 모델 & 프라이싱 | — | 수익 모델 선택 및 가치 기반 가격 |

---

## 🔑 핵심 기능

### 📎 스마트 파일 통합

어떤 단계에서든 보충 파일을 업로드하면 — AI가 자동으로 식별하고 통합합니다:

| 업로드 | 자동 통합 대상 |
|--------|-------------|
| 경쟁사 스크린샷 | 포지셔닝 분석 |
| 인터뷰 녹취록 | Persona + JTBD |
| 사용자 데이터 CSV | 기회 평가 + PMF 평가 |
| 시장 보고서 PDF | 기회 평가 + 전략 |
| 기존 PRD | 리비전 모드 + MVP |

### 🔄 변경 전파 엔진

상위 단계를 수정하면 하위 산출물이 자동 업데이트:

```
JTBD 수정 → HMW, 포지셔닝, PR-FAQ, North Star, 제품 스펙 요약 자동 업데이트
MVP 수정  → User Stories, DB Schema, 제품 스펙 요약 자동 업데이트
```

### 🔗 개발 핸드오프

완전한 개발 핸드오프 패키지를 생성하고 단일 명령으로 Claude Code 개발을 시작하세요:

```
📦 개발 핸드오프 패키지
├── CLAUDE.md          → Claude Code 프로젝트 메모리
├── TASKS.md           → 기능 분해 + 단계별 딜리버리
├── TICKETS.md         → 티켓 목록 (Jira/Asana/Linear 바로 사용 가능)
├── docs/
│   ├── PRD.md         → 전체 PRD
│   ├── ARCHITECTURE.md → DB Schema + API + 디렉토리 구조
│   └── PRODUCT-SPEC.md → 제품 스펙 요약
└── scripts/
    └── setup.sh       → 원클릭 초기화 스크립트
```

```bash
# Claude Code에서 단일 명령으로 개발 시작
> CLAUDE.md와 TASKS.md를 읽고, Phase 0 실행 시작
```

### 🪝 라이프사이클 훅

세 개의 플러그인 훅이 Playbook의 핵심 규칙을 "Claude가 알아서 기억"에서 "하네스가 강제 실행"으로 끌어올립니다. 모든 훅은 `systemMessage` 형태의 소프트 리마인더만 주입하며, **사용자를 막지 않습니다**.

| 이벤트 | 트리거 시점 | 역할 |
|--------|------------|------|
| `SessionStart` | 새 세션 또는 재개 시마다 | `.product-playbook-progress.md`와 `.product-context.md`를 자동으로 모델 context에 주입하여, 중단된 기획을 직전 단계에서 매끄럽게 이어가도록 함 |
| `UserPromptSubmit` | 기획 진행 중 프롬프트 제출마다 | (a) 주제 이탈 메시지(debug / 에러 / "이 코드 고쳐주세요")를 감지해 SKILL.md의 진행 상황 저장 규칙을 따르도록 Claude에 지시. (b) 변경 의도 키워드(`改 step 2`, `update persona`, `JTBD 다시 작성`)를 감지해 Change Propagation 규칙 적용을 환기 |
| `PreToolUse` (Write/Edit/MultiEdit) | 파일 쓰기 전마다 | 프로젝트가 기획 단계(`.product-dev-active` 마커 없음)이고 대상이 소스 코드 확장자(`.ts/.tsx/.py/.go/...`)일 경우, "기획은 문서만 생성, 코드는 생성하지 않는다"는 원칙을 Claude에 리마인드. 마커는 `/product-dev` 실행 시 자동 생성됨 |

훅은 플러그인 설치 시 `hooks/hooks.json`에서 자동 로드됩니다. product-playbook 프로젝트가 아닌 곳에서는 완전히 no-op이므로 다른 codebase에 영향을 주지 않습니다.

### 📄 문서 가져오기 및 내보내기

**가져오기** — 기존 문서를 기획 플로우에 직접 투입, 수동 복사 붙여넣기 불필요:

```
PDF (디지털)       → pymupdf 텍스트 추출 (즉시, 무료)
PDF (벡터/스캔)    → Claude Vision 시맨틱 파싱 (최고 품질)
PDF (폴백)         → Tesseract OCR (오프라인 가능)
DOCX / PPTX        → Pandoc 변환
```

**내보내기** — 기획 산출물을 전문적 형식으로:

```
/export pdf   → Playwright 렌더링 + pikepdf 북마크 (CJK 완벽 지원)
/export docx  → Pandoc + 참조 템플릿
/export pptx  → Pandoc 슬라이드 생성
/export html  → 인터랙티브 HTML 보고서 (기존)
```

> **왜 Playwright로 PDF를?** WeasyPrint은 CJK 텍스트가 깨집니다. Playwright(Chromium)는 완벽하게 렌더링됩니다 — 번체 중국어 문서로 프로덕션 환경에서 검증 완료.

### 🔥 기존 시스템 위에서 바로 기획 (빌드 모드 킬러 피처)

기존 프로젝트 디렉토리에서 **빌드 모드**를 실행하면 — Claude Code가 코드베이스를 읽으면서 제품 기획을 수행하여, **제품 기획**과 **기술 실현 가능성 평가**를 단일 플로우로 병합합니다:

```
기존 프로젝트                         Product Playbook
┌─────────────────┐                ┌─────────────────────┐
│ src/             │  ← 자동 스캔 → │ Pre-mortem 리스크     │
│ db/schema.sql    │  ← 자동 스캔 → │ MVP 범위 결정         │
│ api/routes/      │  ← 자동 스캔 → │ RICE 우선순위         │
│ package.json     │  ← 자동 스캔 → │ User Story 분해       │
│ CLAUDE.md        │  ← 자동 스캔 → │ 개발 핸드오프 (델타)    │
└─────────────────┘                └─────────────────────┘
```

**사용 예시:**

```bash
# 1. 기존 프로젝트로 이동
cd /path/to/your-existing-project

# 2. Claude Code 실행
claude

# 3. 빌드 모드를 사용하여 추가할 기능 설명
> /product-feature 기존 시스템에 실시간 알림 기능을 추가하고 싶어요
```

Claude Code가 자동으로:
- 디렉토리 구조, 기술 스택, DB 스키마를 스캔
- **실제 아키텍처**를 기반으로 Pre-mortem 실행 (가상의 리스크가 아닌)
- 기존 모듈에 직접 연결되는 MVP와 User Stories 생성
- **증분 계획**으로 개발 핸드오프 패키지 생성, 그린필드 빌드가 아닌

> 💡 **왜 이것이 강력한가요?** 전통적으로 제품 기획과 기술 평가는 별도의 프로세스입니다 — PM이 스펙을 작성하고 엔지니어에게 넘기면 엔지니어가 "이건 안 됩니다"라고 말합니다. 빌드 모드는 기획 프로세스를 실제 시스템 제약에 기반하게 하여 이런 왕복을 제거합니다.

### 🔒 보안 기본 탑재

개발 핸드오프 패키지에 보안 아키텍처가 자동으로 포함됩니다 — 사후 패치가 아닙니다:

- **OWASP Top 10 체크리스트** — 입력 유효성 검증, 인증/인가, XSS/CSRF 방어
- **보안 아키텍처 섹션** — CORS 정책, CSP 헤더, rate limiting, API 보안 미들웨어
- **.gitignore 템플릿** — `.env`, 크리덴셜, 진행 파일 자동 제외
- **Pre-mortem 보안 시나리오** — 데이터 유출, 계정 탈취, API 남용을 필수 고려사항으로

### 📦 세션 간 제품 컨텍스트 축적

기획 산출물이 `.product-context.md`에 자동 저장되고 다음 세션에서 로드됩니다:

```
1차 세션 (풀 모드) → Identity + Core Strategy + Architecture 저장
2차 세션 (기능 확장) → 기술 스택과 모듈 자동 로드, 중복 수집 건너뛰기
3차 세션 (리비전 모드) → 과거 결정과 알려진 페인포인트 이어서, 델타에 집중
```

### 🏢 자동 B2B / B2C 적응

제품 유형이 확인되면 프레임워크가 자동 적응합니다:

| 측면 | B2C | B2B |
|------|-----|-----|
| Persona | 개인 동기 세분화 | 구매자 + 사용자 이중 Persona |
| PMF | DAU / 리텐션 / Sean Ellis | 유료 고객 / NRR / NPS |
| North Star | 핵심 행동 완료 수 | ARR / Net Revenue Retention |
| Aha Moment | 첫 사용 내 | 온보딩 / Time-to-Value |

---

## 📊 품질 벤치마크 결과

"스킬 가이드 있음"과 "스킬 가이드 없음" 간의 응답 품질을 자동화된 AI 채점으로 비교하여, 스킬의 실제 효과를 정량화했습니다.

### 4차 반복 비교

| 반복 | 테스트 항목 | 스킬 있음 통과율 | 스킬 없음 통과율 | 차이 |
|------|:--------:|:-----------:|:-----------:|:---:|
| 반복 1 (베이스라인) | 6 | 100% | 57.4% | +42.6% |
| 반복 2 | 6 | 100% | 63.3% | +36.7% |
| 반복 3 | 6 | 94.1% | 38.2% | +55.9% |
| **반복 4 (최신)** | **9** | **100%** | **31%** | **+69% ✅** |

### 반복 4 상세 결과 (9 테스트 x 49 기대값)

| 테스트 항목 | 스킬 있음 | 스킬 없음 | 차이 |
|-----------|:-------:|:-------:|:---:|
| 모드 선택 (3단계 점진적) | 100% | 0% | +100% |
| 퀵 모드 JTBD 분석 | 100% | 43% | +57% |
| JTBD 깊이 (B2B 조직 수준) | 100% | 57% | +43% |
| PR-FAQ 작성 | 100% | 33% | +67% |
| 리비전 모드 | 100% | 67% | +33% |
| 품질 자체 점검 하드 게이트 | 100% | 0% | +100% |
| **기능 확장 모드 (신규)** | **100%** | **17%** | **+83%** |
| **보안 통합 (신규)** | **100%** | **25%** | **+75%** |
| **Context Bootstrap (신규)** | **100%** | **0%** | **+100%** |

### 핵심 발견

- **품질 자체 점검 하드 게이트** (+100%): AI가 납품물 완성 후 엄격한 기준으로 자체 산출물을 비판하고, 갭을 지적하며, 개선을 요구하는지 여부 — 스킬 없이는 0% 통과율
- **Context Bootstrap** (+100%): AI가 기획을 시작하기 전에 기초 제품 정보를 수집하는지, 기술 구현으로 바로 뛰어들지 않는지 — 스킬 없이는 완전히 건너뜀
- **기능 확장 모드** (+83%): AI가 "기존 제품에 기능 추가" 시나리오를 인식하고 전체 6-11단계 대신 간소화된 4단계 플로우를 활성화하는지 — 스킬 없이는 기술 솔루션으로 바로 점프
- **보안 통합** (+75%): 개발 핸드오프에 보안 아키텍처, .gitignore 템플릿, 플랫폼별 보안 조치가 포함되는지 — 스킬 없이는 보안이 단일 요약 테이블로 축소

> 상세한 방법론과 데이터는 [`evals/`](./evals/)를 참조하세요.

### 반복 5: Sub-agent A/B 비교 (디스패치 관련 3개 평가 × 22개 기대값)

v1.2.0+ 에서 도입된 3개의 전문 sub-agent (`discovery-specialist`, `strategy-critic`, `pre-mortem-runner`) 의 품질에 대한 한계 기여를 측정하는 집중 A/B 평가. 동일 스킬 버전(v1.2.3), 동일 프롬프트, 2개 arm:

- **Sub-agent 있음**: executor 가 해당 `agents/*.md` 파일을 읽고, 전문가가 선언한 출력 스키마와 자체 점검을 따름. 응답에 dispatch 마커 기록.
- **Sub-agent 없음**: executor 는 어떤 `agents/*.md` 도 읽지 못하며, delegation 을 언급하지 못함. `SKILL.md` + `commands/` + `references/` 만 사용하여 orchestrator 가 inline 으로 처리.

| 평가 항목 | Sub-agent 있음 | Sub-agent 없음 | 차이 |
|-----------|:--------:|:------------:|:-----:|
| Discovery (Persona + JTBD) | 100% (7/7) | 85.7% (6/7) | +14.3% |
| Strategy Critic | 100% (6/6) | 83.3% (5/6) | +16.7% |
| **Pre-mortem (Build Mode 위험 평가)** | **100% (9/9)** | **22.2% (2/9)** | **+77.8% ✅** |
| **합계** | **100% (22/22)** | **59.1% (13/22)** | **+40.9%** |

두 arm 의 token 소비는 거의 동일함 (151K vs 154K) — 전문가를 유지하는 것이 inline 처리보다 더 비싸지 않음.

**핵심 발견**

- **Pre-mortem-runner 가 load-bearing** (+77.8%): 이것이 없으면 orchestrator 는 얇고 미래형인 위험 리스트만 생성하며, 시나리오 수 (≥15), 5개 카테고리 커버리지, leading indicator 규율, 저비용 pre-launch 실험, 과거형 "출시 후 실패" 내러티브 프레임을 놓침. 구조화된 전문가 스키마가 실제로 일을 하고 있으며, `references/` 만으로는 재구성할 수 없음.
- **Discovery-specialist 와 strategy-critic 은 중간 기여자** (+14–17%): orchestrator 자체만으로도 Persona+JTBD 와 전략 비평을 합리적 수준에서 처리할 수 있음. 두 arm 에서 분기하는 유일한 assertion 은 dispatch 계약 자체이며, 구조적 품질이 아님.
- **함의**: 3개 전문가 중 pre-mortem-runner 가 단독 품질 향상이 가장 크고 보존이 가장 정당화됨. 다른 2개는 원칙적으로 강화된 reference 페이지로 orchestrator 에 통합할 수 있지만, token 비용이 동일하므로 축소 동기는 없음.

**Harness 주의사항**: 이 평가 환경의 `general-purpose` executor 는 nested `Task` 를 노출하지 않으므로, "Sub-agent 있음" arm 은 "전문가 `agents/*.md` 읽기 + dispatch 마커 + 스키마를 inline 으로 준수" 로 실제 dispatch 를 근사함. 구조적 대조는 실제이지만, 엔드투엔드 Task 도구 dispatch 를 완전히 검증하려면 top-session 실행이 필요함.

> 원시 artifacts 와 assertion 별 분기는 [`~/product-playbook-workspace/iteration-3/benchmark.md`](./evals/) 참조.

---

### 반복 6: 토큰 최적화 패스 (v1.2.5)

토큰 절감 반복. 스킬 콘텐츠의 시맨틱은 동일하게 유지하되, 세션당 footprint 를 축소. 목표: 품질 100% 를 유지하면서 토큰 ≥25% 감소.

**적용된 변경 사항:**
- **SKILL.md 슬림화** — Sub-Agent Delegation Rules 를 lazy `rules-subagent-dispatch.md` 로 추출, Hard Gate 설명을 축약, Mode Overview 의 중복을 통합. eager 진입점 기준 **6,188 → 2,877 tokens (-54%)**.
- **rules-context.md 분할** — 의사결정 로직은 eager (1,594 tokens) 로 유지, 장문 YAML 템플릿 + Bootstrap 절차 + Conflict UX 스크립트는 lazy `rules-context-template.md` (1,849 tokens, 트리거 시에만 로드) 로 이동.
- **rules-quality-review.md 슬림화** — 1,040 → 817 tokens 로 정제, 컴팩트한 3단계 프로토콜과 프레임워크당 1줄 체크리스트로 구성.
- **전문가 에이전트 슬림화** — `references/*.md` 와 중복되던 임베디드 프레임워크 지식을 제거하고 온디맨드 포인터로 대체. dispatch 당 **discovery-specialist −25%, strategy-critic −18%, pre-mortem-runner −20%**.

**9-step Full Mode 세션당 예상 절감:**

| 출처 | Before | After | 절감 |
|------|:------:|:-----:|:-----:|
| Eager (SKILL + context + progress) | ~8,800 | ~5,500 | **−3,300** |
| Quality review (×9 step loads) | ~9,360 | ~7,353 | **−2,007** |
| Sub-agent dispatch (3개 전문가) | ~9,005 | ~7,106 | **−1,899** |
| **세션당 합계** | **~27,200** | **~18,900** | **−8,300 (−30%)** |

**품질 검증:** pre-mortem-runner (반복 5 기준 품질에 가장 민감한 전문가) 가 v1.2.5 슬림화된 콘텐츠로 eval-12 를 재실행. 결과: **9/9 assertions PASS** — 5개 카테고리 전체에 걸친 16개 시나리오, 실제 stack 컴포넌트를 인용하는 5개의 아키텍처 기반 시나리오, 이진 의사결정 규칙을 가진 5개의 저비용 pre-launch 실험, 과거형 프레이밍 유지. 정적 cross-check 로 eval-10/11 의 assertion (총 13개) 이 슬림화된 에이전트 프롬프트 안에서 모두 명시적으로 뒷받침됨을 확인.

**토큰 비용 트레이드오프:** 분할로 인해 2개의 새 lazy 파일 (`rules-subagent-dispatch.md` 978 tokens, `rules-context-template.md` 1,849 tokens) 이 추가되며, 트리거 시에만 로드됨. 가장 흔한 세션 경로에서는 전혀 로드되지 않음. Bootstrap-or-Conflict 경로에서도 eager 절감분이 여전히 net positive.

**5개 i18n 로케일 (zh-TW, zh-CN, ja, es, ko) 에 미러링** — 기존 번역을 보존하며, 구조적 슬림화는 언어별로 동일하게 적용.

---

## 🧪 개발 및 평가

`evals/` 디렉터리는 두 가지 보완적 테스트 세트와 결정론적 스코어러를 포함합니다.

**로컬 (무료, 권장)**: `claude` CLI를 Claude Pro/Max 구독으로 인증해서 (한 번만 `claude login`) 같은 스크립트를 실행합니다. API key 불필요, 추가 비용 없음. eval 시스템은 각 릴리스 전에 로컬에서 실행하도록 설계되었습니다.

**CI (선택, 유료)**: `.github/workflows/eval-gate.yml`은 모든 PR과 `package.json`을 변경하는 `main`으로의 push에서 두 가지 모두 실행하고, 점수를 workflow Job Summary에 기록합니다. **merge도 publish도 차단하지 않습니다** — 회귀에 대응할지는 유지보수자가 판단합니다. CI는 `ANTHROPIC_API_KEY` secret이 필요합니다 (GitHub Actions는 headless 컨테이너에서 OAuth를 사용할 수 없습니다). secret 미설정 시 eval job은 **깨끗하게 skip**(회색 ⏭️)되며 오해를 일으키는 빨간색 X는 표시되지 않습니다.

### 로컬 실행

```bash
# Trigger eval — 자연어 prompt에서 skill이 자동 트리거되는가?
python3 evals/run_trigger_test.py --runs 3 --workers 4 --fail-on critical \
  --json evals/eval-results.trigger.json

# Behavioral eval — 각 시나리오에서 skill이 올바른 출력을 생성하는가?
# claude를 assistant 겸 judge로 사용 (--runs 3으로 다수결)
python3 evals/run_behavioral_eval.py --runs 3 --workers 2 --fail-on critical \
  --json evals/eval-results.behavioral.json

# 현지화 버전
python3 evals/run_behavioral_eval.py --eval-file evals/evals-zh-TW.json --runs 3

# 스코어러 단위 테스트
python3 -m unittest evals/test_compute_eval_score.py
```

두 runner 모두 `claude` CLI가 `PATH`에 있어야 하며 `ANTHROPIC_API_KEY` 환경 변수가 설정되어 있어야 합니다. 로컬은 `--runs 3`이 기본값(다수결로 LLM 변동성 흡수), CI는 비용 절감을 위해 `--runs 1`을 사용합니다.

### Severity 및 스코어링

`evals.json`의 각 expectation에는 severity가 태그됩니다:

| Severity | 실패 시 감점 | 적용 범위 |
|---|---|---|
| `critical` | −15 | Hard Gate 위반, Mode dispatch 오류, B2B buyer/user 분리, Security default-on, 프레임워크 완전성(JTBD 3계층, Rumelt diagnosis, pre-mortem 15+ 시나리오) |
| `warning`  | −5  | 품질 깊이와 구조(대부분의 expectations) |
| `info`     | −1  | 언어 감지, Progress indicator 형식 |

100점에서 시작하여 실패당 차감, 0–100으로 클램프.

| Band | 범위 | 의미 |
|---|---|---|
| 🟢 `healthy` | ≥ 90 | critical 실패 최대 1개 |
| 🟡 `needs-attention` | ≥ 70 | critical 2개 이하 또는 다수의 warning |
| 🔴 `at-risk` | < 70 | critical 3개 이상; gate 실패 대상 |

### `--fail-on` 의미론

| Flag 값 | Runner가 exit non-zero가 되는 조건 |
|---|---|
| `critical` | critical expectation이 하나라도 실패 (CI 기본값) |
| `any` | severity와 관계없이 임의 expectation 실패 |
| `none` | 절대 실패하지 않음; 로컬 탐색용 informational mode |

모든 스코어링 로직은 `evals/compute_eval_score.py`라는 단일 소스에 집중되어 있어 두 runner가 독립적으로 구현하여 drift하는 것을 방지합니다.

---

## 💬 사용 가능한 명령

### ⌨️ Claude Code CLI 슬래시 명령

스킬 설치 후 사용 가능한 메인 명령:

| 명령 | 설명 |
|------|------|
| `/product-playbook` | 전체 제품 기획 가이드 플로우 시작 |

더 세밀한 단축키는 `commands/` 폴더의 사전 빌드된 슬래시 명령을 설치하세요:

```bash
# 모든 슬래시 명령 설치
cp -r product-playbook/commands/* ~/.claude/commands/
```

| 명령 | 설명 |
|------|------|
| `/product-quick <설명>` | 퀵 모드 — JTBD → PR-FAQ → North Star를 30분 이내 실행 |
| `/product-full <설명>` | 풀 모드 — 완전한 제품 기획 (9–11단계; Journey Map 기본 ON) |
| `/product-revision <설명>` | 리비전 모드 — 기존 제품 반복 최적화 |
| `/product-build <설명>` | 빌드 모드 — 디스커버리 건너뛰고 솔루션으로 바로 |
| `/product-feature <설명>` | 기능 확장 모드 — 기존 제품에 단일 기능 추가 (4단계) |
| `/product-prd` | PRD 엔지니어링 핸드오프 패키지 생성 |
| `/product-report` | HTML 기획 보고서 생성 |
| `/product-dev` | 개발 핸드오프 패키지 생성 (CLAUDE.md + TASKS.md + TICKETS.md) |

### 💬 대화 중 자연어 명령

#### 플로우 제어
- `[프레임워크]로 전환` — 즉시 프레임워크 전환
- `이 단계 건너뛰기` — 현재 단계 건너뛰기
- `[단계명]으로 돌아가기` — 어떤 단계로든 돌아가서 수정
- `간소화` / `확장` — 깊이 조정

#### 산출물 명령
- `보고서 생성` — HTML 기획 보고서
- `PRD 생성` — 엔지니어링 핸드오프 (플로우차트 + DB Schema + 와이어프레임 포함)
- `덱 생성` — PowerPoint 프레젠테이션
- `개발 시작` — 개발 핸드오프 패키지 (CLAUDE.md + TASKS.md)
- `/export pdf` — 전문 타이포그래피, 표지, 목차 및 북마크가 포함된 PDF로 내보내기
- `/export docx` — Word 문서로 내보내기
- `/export pptx` — PowerPoint 슬라이드로 내보내기
- `/parse [file]` — PDF/DOCX/PPTX를 Markdown으로 파싱하여 기획에 활용

#### 분석 명령
- `완성도 점검 해 주세요` — 기획 커버리지 평가
- `가정을 찾아주세요` — 미검증 가정 나열
- `Pre-mortem 실행` — Pre-mortem 분석
- `이 제품의 PMF 수준은?` — PMF 평가
- `병목을 찾아주세요` — Aha Moment 장애물 분석

---

## 🤝 기여하기

기여를 환영합니다! 특히 도움이 필요한 영역:

- 🌍 **다국어 지원** — 다른 언어로 프레임워크 번역
- 📐 **새로운 프레임워크** — 더 많은 제품 관리 프레임워크 추가
- 📝 **예시** — 각 프레임워크에 더 많은 실제 예시 추가
- 🐛 **버그 리포트** — 사용 중 발견된 로직 이슈나 갭
- 💡 **UX 개선** — 상호작용 플로우 및 명령 설계 제안

### 기여 방법

1. 이 레포를 포크
2. 피처 브랜치 생성 (`git checkout -b feature/amazing-framework`)
3. 변경사항 커밋 (`git commit -m 'feat: add amazing framework'`)
4. 브랜치에 푸시 (`git push origin feature/amazing-framework`)
5. Pull Request 열기

### 기여 가이드라인

- 레퍼런스 파일의 프레임워크 내용은 출처를 인용해야 합니다
- 새 프레임워크는 SKILL.md의 프레임워크 인덱스와 단계 시퀀스 업데이트를 포함해야 합니다
- 품질 자체 점검 목록은 ✅ / ❌ 형식 사용
- 다국어 지원: 영어와 해당 언어 버전을 모두 유지

---

## 📚 프레임워크 출처 및 추가 참고자료

이 프로젝트의 프레임워크는 다음 사상가들의 공개된 저작물에서 종합했습니다:

| 사상가 | 핵심 기여 | 추천 도서 |
|--------|---------|----------|
| Teresa Torres | Continuous Discovery, OST | *Continuous Discovery Habits* |
| Shreyas Doshi | LNO, Pre-mortem, 제품 업무 3단계 | Lenny's Podcast Ep.3 |
| Gibson Biddle | DHM Model, GEM | Lenny's Podcast |
| April Dunford | 포지셔닝 프레임워크 | *Obviously Awesome* |
| Todd Jackson | 4단계 PMF, Four P's | Lenny's Podcast |
| Richard Rumelt | 좋은 전략 / 나쁜 전략 | *Good Strategy Bad Strategy* |
| Marty Cagan | Empowered Teams | *Inspired*, *Empowered* |
| Clayton Christensen | Jobs to Be Done | *Competing Against Luck* |
| Amazon | Working Backwards / PR-FAQ | *Working Backwards* |
| Sean Ellis | Sean Ellis Score, Growth | *Hacking Growth* |
| Lenny Rachitsky | Shape / Ship / Synchronize | Lenny's Newsletter + Podcast |

---

## 📄 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE)에 따라 라이선스되었습니다 — 제한 없이 자유롭게 사용, 수정, 배포할 수 있습니다.

---

## ⭐ Star History

이 프로젝트가 도움이 되었다면, ⭐를 눌러 더 많은 사람들이 찾을 수 있게 해주세요!

---

<p align="center">
  <strong>중요한 것을 만들고자 하는 프로덕트 매니저를 위해 ❤️로 제작되었습니다.</strong>
</p>

---

Copyright (c) 2026 Charles Chen.
