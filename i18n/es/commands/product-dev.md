---
description: Generar Paquete de Handoff de Desarrollo — Produce CLAUDE.md + TASKS.md + TICKETS.md + ARCHITECTURE.md + setup.sh, listo para iniciar desarrollo en Claude Code
---

Por favor lee ~/.claude/skills/product-playbook/SKILL.md.
Luego lee los siguientes archivos de referencia en orden:
1. `references/07a-handoff-core.md` (plantilla CLAUDE.md + confirmación de stack tecnológico)
2. `references/07b-tasks-tickets.md` (plantillas TASKS.md + TICKETS.md)
3. `references/07c-architecture-setup.md` (ARCHITECTURE.md + setup.sh + guía de usuario)

Basándote en el contenido de planificación de producto completado en la conversación actual, genera el paquete completo de handoff de desarrollo:
1. Confirma el stack tecnológico (si no fue especificado por el usuario, recomienda uno basado en las características del producto)
2. Genera CLAUDE.md (memoria de proyecto de Claude Code)
3. Genera TASKS.md (desglose de funcionalidades + releases por fases + criterios de aceptación)
4. Genera TICKETS.md (lista de tickets)
5. Genera docs/ARCHITECTURE.md (estructura de directorios + DB Schema + API Endpoints)
6. Genera docs/PRD.md + docs/PRODUCT-SPEC.md
7. Genera scripts/setup.sh (script de inicialización en un solo comando)
8. Muestra la guía de transición a Claude Code

Si no existe contenido de planificación de producto en la conversación, solicita al usuario que ejecute un flujo de planificación de producto primero.
