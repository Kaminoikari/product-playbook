---
description: Generar Paquete de Handoff de Desarrollo — Produce CLAUDE.md + TASKS.md + TICKETS.md + ARCHITECTURE.md + setup.sh, listo para iniciar desarrollo en Claude Code
---

Activa el skill product-playbook.
Luego lee los siguientes archivos de referencia en orden:
1. `references/07a-handoff-core.md` (plantilla CLAUDE.md + confirmación de stack tecnológico)
2. `references/07b-tasks-tickets.md` (plantillas TASKS.md + TICKETS.md)
3. `references/07c-architecture-setup.md` (ARCHITECTURE.md + setup.sh + guía de usuario)

Basándote en el contenido de planificación de producto completado en la conversación actual, genera el paquete completo de handoff de desarrollo:
1. Confirma el stack tecnológico (si no fue especificado por el usuario, recomienda uno basado en las características del producto)
2. Crea el archivo marcador `.product-dev-active` en la raíz del proyecto (archivo vacío) y añade `.product-dev-active` al `.gitignore` del proyecto (crea el archivo si no existe, o añade la entrada si falta — sin duplicar). Esto le indica al hook PreToolUse del plugin que el proyecto ha entrado oficialmente en la fase de handoff de desarrollo, por lo que las siguientes escrituras de código fuente ya no serán filtradas por el hook.
3. Genera CLAUDE.md (memoria de proyecto de Claude Code)
4. Genera TASKS.md (desglose de funcionalidades + releases por fases + criterios de aceptación)
5. Genera TICKETS.md (lista de tickets)
6. Genera docs/ARCHITECTURE.md (estructura de directorios + DB Schema + API Endpoints)
7. Genera docs/PRD.md + docs/PRODUCT-SPEC.md
8. Genera scripts/setup.sh (script de inicialización en un solo comando)
9. Muestra la guía de transición a Claude Code

Si no existe contenido de planificación de producto en la conversación, solicita al usuario que ejecute un flujo de planificación de producto primero.

Nota: `.product-dev-active` es un marcador session-local y no debe ser commiteado — el paso 2 asegura que esté listado en el `.gitignore` del propio proyecto. Elimina el marcador si el proyecto vuelve al modo de solo planificación.
