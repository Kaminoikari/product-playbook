---
description: Modo Extensión de Funcionalidad — Añade una funcionalidad a un producto existente en 4 pasos simplificados
argument-hint: <descripción de la funcionalidad>
---

Activa el skill product-playbook.
Luego lee references/rules-build.md y salta directamente a la sección "🔧 Feature Extension Quick Path".
Al ejecutar cada paso, carga los archivos de referencia correspondientes según se indica.

Modo de ejecución: 🔧 Modo Extensión de Funcionalidad
Descripción de la funcionalidad: $ARGUMENTS

Sigue la secuencia de pasos de Feature Extension (S1 → S4). Primero carga el contexto del producto según rules-context.md. Muestra un indicador de progreso en cada paso.

**Secuencia S0 → S1 (importante)**: Si Context Bootstrap (S0) se activa porque falta `.product-context.md`, DEBES completar Bootstrap y S1 en el **mismo turno**, y luego pausar **después de completar S1** esperando la confirmación del usuario antes de S2. NO pauses entre S0 y S1 — incluso si faltan algunos campos del Bootstrap, escribe un baseline `.product-context.md` con placeholders, entra a S1, y pregunta por los campos faltantes como parte de la pregunta de confirmación de S1. Ver `references/rules-context.md` "Secuencia Bootstrap → S1" para detalles.
