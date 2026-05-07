---
description: 개발 핸드오프 패키지 생성 — CLAUDE.md + TASKS.md + TICKETS.md + ARCHITECTURE.md + setup.sh를 생성하여 Claude Code에서 바로 개발 시작 준비
---

product-playbook skill을 실행합니다.
그 다음 아래 레퍼런스 파일을 순서대로 읽으세요:
1. `references/07a-handoff-core.md` (CLAUDE.md 템플릿 + 기술 스택 확인)
2. `references/07b-tasks-tickets.md` (TASKS.md + TICKETS.md 템플릿)
3. `references/07c-architecture-setup.md` (ARCHITECTURE.md + setup.sh + 사용자 가이드)

현재 대화에서 완료된 제품 기획 내용을 기반으로 전체 개발 핸드오프 패키지를 생성하세요:
1. 기술 스택 확인 (사용자가 지정하지 않은 경우 제품 특성에 맞는 추천)
2. 프로젝트 루트에 `.product-dev-active` 마커 파일(빈 파일)을 생성하고, `.product-dev-active`를 프로젝트의 `.gitignore`에 추가합니다 (`.gitignore`가 없으면 새로 생성, 있으면 항목을 append; 중복 추가 금지). 이 파일은 플러그인의 PreToolUse hook에 "프로젝트가 정식으로 개발 핸드오프 단계에 진입했음"을 알리며, 이후 소스 코드 쓰기에 대한 hook 리마인더가 비활성화됩니다.
3. CLAUDE.md 생성 (Claude Code 프로젝트 메모리)
4. TASKS.md 생성 (기능 분해 + 단계별 릴리스 + 인수 기준)
5. TICKETS.md 생성 (티켓 목록)
6. docs/ARCHITECTURE.md 생성 (디렉토리 구조 + DB Schema + API Endpoints)
7. docs/PRD.md + docs/PRODUCT-SPEC.md 생성
8. scripts/setup.sh 생성 (원클릭 초기화)
9. Claude Code 전환 가이드 표시

대화에 제품 기획 내용이 없는 경우, 제품 기획 플로우를 먼저 실행하도록 안내하세요.

참고: `.product-dev-active`는 session-local 마커이며 commit해서는 안 됩니다 — 단계 2에서 프로젝트 자체의 `.gitignore`에 등록되었습니다. 프로젝트가 다시 순수 기획 모드로 돌아갈 경우 이 마커 파일을 삭제하면 됩니다.
