# 🔧 프레임워크 메뉴 + 보조 명령

> 사용자가 "프레임워크 목록", "사용 가능한 프레임워크를 보여주세요"를 요청하거나 보조 명령을 사용할 때 로드됩니다.

## 프레임워크 지정

**두 가지 트리거 방법:**

**방법 A (사용자가 프레임워크를 직접 지정):** 해당 프레임워크의 안내 플로우로 바로 진행 — 다시 질문할 필요 없음.

**방법 B (사용자가 "프레임워크를 고르고 싶어요", "모든 프레임워크를 보여주세요" 등):** 다음 메뉴를 제시:

```
📚 사용 가능한 프레임워크 — 번호 또는 이름을 입력하세요:

【사용자 이해】
 1. JTBD (Jobs to Be Done) — 사용자가 진정으로 완수하고 싶은 과업 식별
 2. Persona — 사용/과업/동기 기반 사용자 프로필 구축
 3. User Journey Map — 완전한 사용자 경험 여정 매핑
 4. Continuous Discovery — 주간 사용자 소통 습관 구축

【문제 정의】
 5. OST / Opportunity Solution Tree — 기회와 솔루션을 체계적으로 연결
 6. 포지셔닝 / April Dunford — 실제 경쟁 영역과 차별화 발견
 7. HMW — 페인포인트를 디자인 질문으로 재구성

【솔루션 설계】
 8. Working Backwards / PR-FAQ — 사용자 성과에서 역으로 솔루션 도출
 9. Pre-mortem — 실패가 발생하기 전에 예측하고 방지
10. GEM — Growth / Engagement / Monetization 3차원 우선순위
11. RICE — 정량적 기능 우선순위 결정
12. MVP — 최소 실행 가능한 제품 범위 정의

【전략 계층】
13. 전략 / Strategy Blocks — Mission → Vision → Strategy 계층
14. DHM Model — Delight / Hard to copy / Margin-enhancing 기회 평가
15. LNO Framework — Leverage / Neutral / Overhead 시간 배분
16. Empowered Teams — 임파워드 팀 vs. 기능 팀

【측정 계층】
17. North Star / North Star Metric — 핵심 사용자 가치를 대표하는 단일 지표 정의
18. PMF — 4단계 Product-Market Fit 평가
19. Sean Ellis Score — PMF 열정 수준 정량화

【비즈니스 계층】
20. 비즈니스 모델 & 프라이싱 — 수익 모델 선택 및 가치 기반 가격 정렬
21. GTM 전략 — Go-to-Market 출시 및 고객 획득 전략

【개발 핸드오프】
22. 개발 핸드오프 — CLAUDE.md + TASKS.md + TICKETS.md를 생성하여 Claude Code에 개발 핸드오프

프레임워크 번호 또는 이름을 입력하세요 (복수 선택 가능, 쉼표로 구분):
```

## 디스커버리 건너뛰기 / 빌드로 바로 진행

사용자가 "사용자 리서치 건너뛰기", "문제는 이미 알고 있어요", "Develop으로 바로 가기"라고 말하면, `references/rules-build.md`를 읽고 빌드 모드 단계 시퀀스를 따르세요.

> 사용자에게 알림: "사용자 리서치 단계를 건너뛰면 솔루션이 가정에 기반하게 됩니다. 실행 후 가능한 빨리 Continuous Discovery를 수행하여 검증하는 것을 권장합니다."

## 기능 확장 모드 트리거

- "기능 추가" / "새 기능을 추가하고 싶어요" / "기존 제품에 새 기능" → 기능 확장 모드를 트리거합니다 (`references/rules-build.md` → 기능 확장 빠른 경로를 읽음)

## 보조 명령

| 명령 | 동작 |
|------|------|
| `"[프레임워크]로 전환"` | 즉시 전환, 완료된 내용 유지 |
| `"대상 독자를 바꾸고 싶어요"` | 프레임워크 우선순위와 표현 스타일 재조정 |
| `"이 단계를 건너뛰기"` | 필요성을 알리고, 결정을 존중하여 다음 단계로 이동 |
| `"[단계/프레임워크명]으로 돌아가기"` | 지정된 단계로 복귀하여 재안내 (`references/rules-change-propagation.md` 참조) |
| `"간소화"` / `"확장"` | 핵심만 요약 / 심층 분석 추가 |
| `"보고서 생성"` | `references/06-html-report.md`를 읽고 HTML 기획 보고서 작성 |
| `"PRD 생성"` / `"엔지니어 문서 생성"` | `references/04b-solutions.md`를 읽고 PR-FAQ + MVP + User Story + Pre-mortem 통합, **자동으로 추가 생성: 플로우차트(Mermaid) + DB schema(Mermaid ERD) + UI 와이어프레임(HTML)** |
| `"플로우차트 생성"` / `"플로우차트 그려주세요"` | Mermaid 구문으로 플로우차트 출력 (독립 트리거) |
| `"DB schema 생성"` / `"데이터베이스 설계"` | Mermaid ERD 구문으로 DB schema 출력 (독립 트리거) |
| `"UI 와이어프레임 생성"` / `"와이어프레임 그려주세요"` | HTML/SVG로 저충실도 UI 와이어프레임 출력 (독립 트리거) |
| `"프레젠테이션 생성"` / `"PPT 만들어 주세요"` | 시스템 pptx 스킬 호출 |
| `"이 문서를 [독자]에 맞게 조정"` | 지정된 독자에 맞게 프레임워크 하이라이트와 언어 재구성 |
| `"15분밖에 없어요"` | 가장 중요한 3가지 의사결정 질문 또는 행동 제공 |
| `"완성도 평가를 해 주세요"` | 어떤 영역이 견고하고 어떤 영역에 리스크가 있는지 평가 |
| `"가정을 찾아주세요"` | 모든 미검증 핵심 가정 식별 |
| `"Pre-mortem 실행"` | 모든 솔루션에 대해 즉시 Pre-mortem 실행 |
| `"다른 독자용 버전 생성"` | 여러 독자에 맞춘 요약을 자동 생성 |
| `"이 제품의 PMF 수준은?"` | PMF 수준 판단 및 다음 마일스톤 설명 |
| `"병목을 찾아주세요"` | Aha Moment 달성의 가장 큰 장애물 분석 |
| `"이것은 신규가 아니라 리비전이에요"` | 리비전 모드로 전환 (`references/rules-revision.md` 읽기) |
| `"상사를 설득해야 해요"` | 보스 모드로 전환 — 비즈니스 가치와 리소스 논리 강조 |
| `"개발 시작"` / `"개발 핸드오프 패키지 생성"` | `references/07a-handoff-core.md`를 읽고 기술 스택 확인 후 전체 개발 핸드오프 패키지 생성 |
| `"프로젝트 설정"` / `"Claude Code 연결"` | 위와 동일 |
| `"일시 정지"` / `"저장"` / `"다른 것 먼저"` | `references/rules-progress.md`에 따라 진행 저장 |
| `"계속"` / `"기획으로 돌아가기"` | `references/rules-progress.md`에 따라 재개 |
| `"진행 초기화"` / `"처음부터 다시"` | 진행 파일 삭제 후 처음부터 시작 |
| `/export [format]` | 지정된 형식으로 내보내기. format = `pdf` / `docx` / `pptx` / `html` / `md`. `references/rules-export-document.md`를 읽음. 최초 사용 시 먼저 `references/rules-document-tools.md`를 로드하여 도구 확인. |
| `/parse [file]` | 업로드된 문서를 Markdown으로 파싱. PDF / DOCX / PPTX / 이미지 지원. `references/rules-import-document.md`를 읽음. 최초 사용 시 먼저 `references/rules-document-tools.md`를 로드하여 도구 확인. |

**컨텍스트 인식 명령 힌트**: 각 단계 완료 후, 현재 진행 상황에 맞게 가장 관련 있는 사용 가능한 명령 2-3개를 능동적으로 제안하세요.
