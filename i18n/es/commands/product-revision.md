---
description: Planificación de Producto Modo Revisión — Optimiza e itera sobre un producto existente, aprovechando datos de usuarios y bases de funcionalidades
argument-hint: <nombre del producto y objetivos de revisión>
---

Activa el skill product-playbook.
Luego lee references/rules-revision.md para la secuencia de pasos.
Al ejecutar cada paso, carga los archivos de referencia correspondientes según se indica en rules-revision.md.

Modo de ejecución: Modo Revisión
Descripción del producto: $ARGUMENTS

Sigue la secuencia de pasos en rules-revision.md (S1 → S8, los pasos Optional están condicionados por los disparadores en rules-optional-trigger.md). S1 preguntará proactivamente sobre métricas del producto existente (DAU/MAU, tasa de retención, feedback clave de usuarios, etc.). Renderiza un bloque Punto de Decisión de Fase antes de cualquier fase que contenga pasos Optional, y muestra un indicador de progreso en cada paso.
