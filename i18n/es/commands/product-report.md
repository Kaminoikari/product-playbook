---
description: Generar Reporte HTML de Planificación — Compila todo el contenido de planificación de producto en un único reporte HTML legible sin conexión
---

Por favor lee ~/.claude/skills/product-playbook/SKILL.md y su references/06-html-report.md.

Basándote en el contenido de planificación de producto completado en la conversación actual, genera un reporte completo de planificación HTML siguiendo las especificaciones de diseño en 06-html-report.md:
- Archivo HTML único (CSS + JS inline, carga de fuentes Google Fonts CDN con Inter)
- Renderiza dinámicamente las etapas completadas; omite las etapas no completadas
- Incluye navegación con tabla de contenidos sticky, diseño basado en tarjetas y efectos interactivos

Si no existe contenido de planificación de producto en la conversación, solicita al usuario que ejecute un flujo de planificación de producto primero.
