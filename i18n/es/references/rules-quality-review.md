# Reglas de Revisión de Calidad

> Se carga al completar cada paso.

## Protocolo

Después del output de cada paso:
1. Marcar cada ítem de la checklist ✅ o ❌. Cada ❌ declara: brecha, impacto downstream, dirección de mejora.
2. **≥1 ❌ requerido** (Hard Gate). ⚠️ NO sustituye. Sin bypass por apéndice "aspecto más débil". ❌ debe ser una brecha sustantiva de contenido, no formato/redacción. Si todo se siente ✅ → baja la vara, re-revisa. Todo artefacto tiene una dimensión más débil.
3. Formato: `📝 Autoevaluación de Calidad:` luego `- ✅/❌ ítem → Brecha / Impacto / Mejora`.

Autoverificación sobre la autoverificación: sin ❌ → rehaz el paso 2.

---

## Checklists por framework

**Persona**: 1) por propósito/motivación no demografía, 2) MECE, 3) TA principal vs secundario claro, 4) puntos de dolor de observación/inferencia real, 5) "enfoque actual + razón" lo suficientemente específico para identificar workarounds.

**JTBD**: 1) contexto específico (no "en cualquier momento"), 2) un solo job central, 3) funcional + emocional + social presentes, 4) usable para evaluar soluciones, 5) "enfoque actual + brecha" indicado, 6) Q5 de las cinco preguntas toca emoción/identidad/miedo.

**Positioning (April Dunford)**: 1) alternativa competitiva desde la perspectiva del usuario, 2) atributo único que los competidores no pueden igualar, 3) valor en lenguaje del usuario no del producto, 4) mercado objetivo lo suficientemente específico para encontrarlos, 5) los 5 elementos lógicamente consistentes.

**HMW**: 1) restricciones claras, 2) espacio de soluciones amplio, 3) mapea a JTBD/dolor, 4) el equipo puede empezar a idear.

**PR-FAQ**: 1) titular perspectiva del usuario ("Los usuarios ahora pueden X"), 2) primer párrafo entrega "por qué importa" en 10s, 3) dolor desde escenario real, 4) la solución abre con sentimiento del usuario, 5) cita suena humana, 6) FAQ tiene preguntas agudas vs herramientas existentes.

**North Star**: 1) refleja valor para el usuario (no ingresos/DAU), 2) puede crecer continuamente, 3) el equipo sabe qué hacer al verla, 4) guardarrails si es manipulable, 5) B2B: valor a nivel de la organización.

**Aha Moment**: 1) comportamiento específico rastreable, 2) atado al job funcional del JTBD, 3) tiempo objetivo razonable (B2C: primer uso; B2B: período de prueba), 4) onboarding diseñable para acelerar.

**Seguridad** (completo: `08-security-checklist.md`): 1) autenticación explícitamente elegida, 2) ≥3 headers de seguridad planificados, 3) rate limit adaptado no plantilla, 4) `.gitignore` cubre todos los archivos sensibles.

**Exportación de Documentos** (completo: `rules-export-document.md`): 1) sin sintaxis Markdown residual en HTML, 2) filas/columnas de tablas coinciden con el original.

---

## Consistencia Entre Pasos (solo al final del flujo)

Detallado: `rules-end-of-flow.md`.

| # | Dimensión | Pregunta |
|---|-----------|----------|
| 1 | Usuario objetivo | ¿JTBD, Posicionamiento, PR-FAQ apuntan a las mismas personas? |
| 2 | Problema central | ¿PR-FAQ aborda el problema del JTBD? ¿MVP lo resuelve? |
| 3 | Solución ↔ Alcance | ¿La solución seleccionada es consistente con el alcance del MVP? |
| 4 | Métrica ↔ Valor | ¿North Star mide los resultados del JTBD? |
| 5 | Vigencia de riesgos | ¿Los riesgos del Pre-mortem siguen siendo relevantes para la solución final? |
