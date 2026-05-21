# 🤝 Sub-Agent 위임 규칙

> 모든 모드의 S2(전문 위임이 적용될 수 있는 첫 단계)에 진입할 때 로드됨. 3개의 전문 sub-agent는 격리된 context window에서 작동합니다 — 모든 것을 인라인으로 처리하지 말고 적절한 단계에서 위임하세요.

## `discovery-specialist`에 위임하는 시점

트리거:
- **Full Mode**: S2(Persona) → S3(JTBD) → S4(OST) → S5(Journey Map) → S6(Continuous Discovery 가설)
- **Revision Mode**: S2(현황 사용자 분석) → S3(페인포인트 통합) → S4(기회 식별)
- **Build Mode**: S2(JTBD 관점의 문제 명확화)
- **Custom Mode**: Persona / JTBD / OST / Journey Map / Continuous Discovery를 선택한 모든 단계

호출 방법:

> `discovery-specialist` subagent를 사용하여 [제품 설명]에 대한 [Persona | JTBD | OST | Journey Map]을 생성하세요. 타깃 고객: [B2C / B2B / B2B2C]. 사용 가능한 리서치 데이터: [업로드된 파일 나열, 또는 "없음 — low confidence로 표시"]. [언어]로 답변하세요.

반환된 YAML을 단계의 출력에 통합합니다. specialist의 `open_questions`를 단계 확인 프롬프트의 일부로 표면화하세요.

---

## `strategy-critic`에 위임하는 시점

사용자가 전략 산출물을 확정한 **직후**에 위임:
- Strategy Blocks 완료 후 (Full Mode S7)
- Rumelt Good Strategy Kernel 완료 후 (Full Mode S8)
- DHM Model 완료 후 (Full Mode S9)
- Empowered Teams charter 완료 후 (모든 모드)
- 사용자가 프레임워크 이름 없이 평문으로 "이것이 우리의 전략이다"라고 작성할 때

호출 방법:

> `strategy-critic` subagent를 사용하여 다음 전략 산출물을 비평하세요: [그대로 붙여넣기]. 이 산출물은 [프레임워크 이름, 또는 "generic strategy doc"]입니다. [언어]로 답변하세요.

Critic은 비평을 반환하며, 재작성하지 않습니다. critic의 `three_questions_to_ask_the_writer`를 사용자에게 그대로 제시하고, 완화하지 마세요. 사용자가 수정하면 수정된 버전에 대해 critic을 다시 호출하세요.

---

## `pre-mortem-runner`에 위임하는 시점

트리거:
- **Full Mode**: S10 (MVP scoping 완료 후)
- **Build Mode**: S4 (architecture-grounded pre-mortem)
- **Revision Mode**: S8
- **Feature Extension Mode**: S3 (리스크 평가)
- 사용자가 pre-mortem / 리스크 분석 / "무엇이 잘못될 수 있는가"를 명시적으로 요청할 때

호출 방법:

> `pre-mortem-runner` subagent를 사용하여 다음 [제품 | 기능 | 전략]에 대해 pre-mortem을 실행하세요: [그대로 붙여넣기]. Mode: [build_mode_architecture_grounded | standard | feature_extension]. build mode인 경우, 사용 가능한 architecture context: [관련 파일 내용 또는 요약 붙여넣기]. [언어]로 답변하세요.

Runner는 15개 이상의 scenario를 반환합니다. 사용자 대상 출력에서 `priority_three`와 `pre_launch_experiments`를 먼저 제시하세요. 전체 scenario 목록은 접을 수 있는 섹션이나 첨부 파일로 표면화합니다.

---

## 위임 위생

1. **한 단계당 하나의 sub-agent**. 한 턴에서 sub-agent를 연쇄하지 마세요 — 사용자가 중간 출력을 먼저 확인하게 하세요.
2. **언어를 명시적으로 전달**. Sub-agent는 당신의 prompt에서 언어를 감지합니다; 항상 사용자의 작업 언어를 지정하세요.
3. **`status: out_of_scope`를 존중**. Sub-agent의 scope 거부는 기능이지 실패가 아닙니다 — 라우팅 권장 사항을 따르세요.
4. **Hard Gate 상속**. Sub-agent는 no-code 규칙을 상속합니다. 요청해도 파일 작성을 거부합니다.
5. **품질 자체 점검은 계속 적용**. Sub-agent 출력을 통합한 후, `rules-quality-review.md`의 품질 자체 점검을 실행하세요 (또는 모드 규칙 파일의 인라인 6개 체크리스트 사용).
