---
description: 기능 확장 모드 — 기존 제품에 단일 기능 추가, 4단계 간소화 프로세스
argument-hint: <기능 설명>
---

product-playbook skill을 실행합니다.
그 다음 references/rules-build.md를 읽고 "🔧 Feature Extension Quick Path" 섹션으로 직접 이동하세요.
각 단계를 실행할 때, 해당 섹션에 명시된 대로 레퍼런스 파일을 로드하세요.

실행 모드: 🔧 기능 확장 모드
기능 설명: $ARGUMENTS

Feature Extension 단계 시퀀스(S1 → S4)를 따르세요. 먼저 rules-context.md에 따라 제품 컨텍스트를 로드하세요. 각 단계에서 진행 표시기를 표시하세요.

**S0 → S1 순서 (중요)**: `.product-context.md`가 없어 Context Bootstrap(S0)이 트리거된 경우, **같은 턴 안에서** Bootstrap과 S1을 완료한 뒤 **S1 완료 후** 사용자 확인을 기다려 S2로 진행해야 합니다. S0과 S1 사이에서 멈추지 마세요 — 일부 Bootstrap 필드가 빠져 있더라도 플레이스홀더로 baseline `.product-context.md`를 기록하고 S1으로 진입한 뒤, 빠진 필드는 S1 확인 질문의 일부로 물어보세요. 자세한 내용은 `references/rules-context.md`「Bootstrap → S1 순서」를 참조하세요.
