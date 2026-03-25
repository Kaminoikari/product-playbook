---
description: 개발 핸드오프 패키지 생성 — CLAUDE.md + TASKS.md + TICKETS.md + ARCHITECTURE.md + setup.sh를 생성하여 Claude Code에서 바로 개발 시작 준비
---

~/.claude/skills/product-playbook/SKILL.md를 읽어 주세요.
그 다음 아래 레퍼런스 파일을 순서대로 읽으세요:
1. `references/07a-handoff-core.md` (CLAUDE.md 템플릿 + 기술 스택 확인)
2. `references/07b-tasks-tickets.md` (TASKS.md + TICKETS.md 템플릿)
3. `references/07c-architecture-setup.md` (ARCHITECTURE.md + setup.sh + 사용자 가이드)

현재 대화에서 완료된 제품 기획 내용을 기반으로 전체 개발 핸드오프 패키지를 생성하세요:
1. 기술 스택 확인 (사용자가 지정하지 않은 경우 제품 특성에 맞는 추천)
2. CLAUDE.md 생성 (Claude Code 프로젝트 메모리)
3. TASKS.md 생성 (기능 분해 + 단계별 릴리스 + 인수 기준)
4. TICKETS.md 생성 (티켓 목록)
5. docs/ARCHITECTURE.md 생성 (디렉토리 구조 + DB Schema + API Endpoints)
6. docs/PRD.md + docs/PRODUCT-SPEC.md 생성
7. scripts/setup.sh 생성 (원클릭 초기화)
8. Claude Code 전환 가이드 표시

대화에 제품 기획 내용이 없는 경우, 제품 기획 플로우를 먼저 실행하도록 안내하세요.
