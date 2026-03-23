# 🏁 Reglas de Fin de Flujo

> Se carga cuando todos los pasos están completados.

## ⛔ Verificación de Condición Final

Antes de producir el output final integrado, lo siguiente debe verificarse:

1. Confirmar que todos los pasos en el indicador de progreso están marcados ✅
2. Si algún paso fue omitido (a solicitud explícita del usuario), marcarlo como "⚠️ Omitido" en el output final
3. Si algún paso está marcado ⬜ (no ejecutado), no proceder al output final
4. **Verificación rápida de seguridad**: Si el usuario entrará a la fase de desarrollo (generando un paquete de handoff de desarrollo), incluir un recordatorio de seguridad en el output final, y al generar el paquete de handoff de desarrollo, leer automáticamente `references/08-security-checklist.md` para producir la sección correspondiente de arquitectura de seguridad

Violaciones a esta regla incluyen: Decidir independientemente que "los pasos restantes no son importantes" y omitirlos, marcar pasos incompletos como completados, o combinar múltiples pasos en un solo output.

## 📦 Auto-Extracción de Contexto de Producto

Después de que todos los pasos estén completos y mientras se produce el output final integrado, lee `references/rules-context.md` Sección 8 para realizar la extracción de contexto:

1. **Verificar si `.product-context.md` existe**
   - No existe → Crear un archivo nuevo
   - Existe → Actualizar según las reglas (Identidad/Estrategia Central sobrescribir, Historial de Decisiones agregar, Arquitectura fusionar, Insights fusionar y deduplicar)

2. **Extraer contenido** (según el mapeo de tipo de flujo en la tabla de la Sección 8 de `rules-context.md`)

3. **Informar al usuario**: Después del output final, mostrar:
   "✅ El contexto de producto ha sido actualizado en `.product-context.md` — se cargará automáticamente en tu próxima sesión de planificación."

4. **Recordatorio de control de versiones** (solo primera creación):
   "⚠️ Recomendamos agregar `.product-context.md` a `.gitignore` — este archivo puede contener información sensible de estrategia de producto."

## Análisis del Mejor Punto de Entrada (solo Modo Completo)

```
[Puntos de Dolor de Persona] → [Declaración JTBD] → [Oportunidad OST] → [Pregunta HMW]
    → [Posicionamiento (April Dunford)] → [Validación PR-FAQ] → [Solución Seleccionada]
        → [Aha Moment] → [North Star Metric] → [Evaluación de Nivel PMF]
```

Puntos de análisis: Problema más valioso a resolver / JTBD Central / Posicionamiento del producto / Nivel de PMF y próximo hito / Primer paso de acción / Alertas de riesgo del Pre-mortem

## Output Final por Modo

| Modo | Output Final Integrado |
|------|----------------------|
| ⚡ Extensión de Feature (variante Modo Build) | Especificación de desarrollo de feature: Problema → Solución seleccionada → Alcance de impacto → Alcance de ejecución → Riesgos |
| 🚀 Modo Rápido | Resumen de dirección de una página: Problema → Solución → Definición de Éxito |
| 📦 Modo Completo | Análisis del Mejor Punto de Entrada + Resumen de Spec de Producto |
| 🔄 Modo Revisión | Resumen de spec de producto de revisión: Comparación antes/después + Qué cambiar/Qué no cambiar + Métricas de éxito |
| ✏️ Modo Personalizado | Resumen de Spec de Producto (campos no ejecutados marcados "No Ejecutado") |
| ⚡ Modo Build | Resumen de ejecución orientado a ingenieros |

### Anulación de Idioma de Output

Los usuarios pueden solicitar outputs en un idioma diferente al de la sesión de planificación:
- "Genera el PR-FAQ en japonés"
- "Genera el reporte en español"
- "Escribe el PRD en chino"

Cuando se solicita una anulación de idioma:
1. Generar el contenido del output en el idioma solicitado
2. Mantener los nombres de frameworks en inglés (JTBD, PR-FAQ, North Star, etc.)
3. Volver al idioma original de la sesión de planificación después de la generación del output
4. Nota: Esto solo afecta el idioma del documento de output, no los archivos de referencia ni el flujo de planificación

## Prompt de Output Extendido

Después de completar el output final integrado, preguntar proactivamente:

```
"¡El contenido de planificación ha sido completamente integrado! ¿Te gustaría que genere alguno de los siguientes documentos?

□ [Tipo de documento] actualizado (actualización incremental basada en el documento fuente subido) ← solo mostrar cuando se subió un documento fuente
□ Documento PDF (diseño profesional con navegación por marcadores, adecuado para compartir formalmente)
□ Reporte de planificación HTML (interactivo, adecuado para compartir en línea)
□ Documento Word (adecuado para edición colaborativa)
□ Paquete de entrega de ingeniería PRD (incluye diagramas de flujo, DB Schema, wireframes UI)
□ Presentación PPTX (adecuada para reportes en reuniones, se recomienda pulir con Keynote / PowerPoint después de exportar)
□ Paquete de handoff de desarrollo (CLAUDE.md + TASKS.md + TICKETS.md + arquitectura técnica — listo para iniciar desarrollo en Claude Code)
□ Todo lo anterior

También puedes decir 'No, gracias' para terminar, o especificar un documento en particular.
También puedes usar /export [pdf|docx|pptx|html|md] para exportar en cualquier momento."
```

**Reglas de visualización de opciones**:
- Documento fuente subido → "[Tipo de documento] actualizado" listado primero con etiqueta "(recomendado)"
- Audiencia objetivo son ingenieros → PRD y paquete de handoff de desarrollo listados primero
- Audiencia objetivo son ejecutivos/liderazgo → PDF y presentación listados primero
- Audiencia objetivo es cross-funcional → PDF, reporte HTML y presentación todos listados
- Modo Rápido → Solo preguntar si se necesita PDF o presentación
- Audiencia objetivo eres tú mismo → Paquete de handoff de desarrollo listado primero

**Reglas de activación de exportación**:
- El usuario selecciona PDF / Word / Presentación PPTX → Cargar `rules-export-document.md`
- Primera vez que se activa exportación de documentos → Cargar `rules-document-tools.md` primero para verificar e instalar herramientas necesarias
- El usuario selecciona reporte de planificación HTML → Cargar `06-html-report.md` (reglas existentes)
- El usuario selecciona "Todo lo anterior" → Ejecutar cada exportación de formato en secuencia
