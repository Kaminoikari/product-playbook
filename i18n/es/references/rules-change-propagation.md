# 🔄 Reglas de Propagación de Cambios

> Se carga cuando el usuario modifica un paso previamente completado.

## 📍 Indicador de Progreso (debe mostrarse en cada paso)

Al ejecutar cualquier paso, Claude debe mostrar una barra de progreso al inicio de la respuesta, en este formato:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 [Modo de Ejecución] ｜ Progreso S[número de paso actual] / S[total de pasos]
✅ S1: [Nombre del paso] (completado)
✅ S2: [Nombre del paso] (completado)
▶️ S3: [Nombre del paso] (en progreso)
⬜ S4: [Nombre del paso] (pendiente)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Este indicador de progreso debe aparecer en las siguientes situaciones:
- Al entrar a un nuevo paso
- Cuando el usuario regresa a un paso para hacer modificaciones
- Al completar un paso y solicitar confirmación del usuario antes de pasar al siguiente

## Métodos de Activación
- "Volver a Persona," "Volver a JTBD," "Volver a HMW," "Volver a PR-FAQ," o cualquier otro nombre de paso
- "Quiero modificar [nombre del paso]," "[nombre del paso] — quiero cambiar algo"
- Referirse directamente a una tabla o contenido ya producido con "cambia esto a..."

## Acciones Requeridas Después de Modificación

Cuando cualquier paso se modifica, Claude **debe realizar proactivamente las siguientes verificaciones**:

```
Capa Modificada               Downstream Afectado (debe re-confirmar o actualizar)
─────────────────────────────────────────────────────
Persona / JTBD            → HMW, Tabla de Evaluación de Oportunidades, Posicionamiento, PR-FAQ, North Star, Resumen de Spec de Producto
HMW / Evaluación de Oportunidades → PR-FAQ, Soluciones Paralelas, MVP, North Star, Resumen de Spec de Producto
Posicionamiento               → PR-FAQ, Resumen de Spec de Producto
PR-FAQ / Soluciones        → Pre-mortem, GEM/RICE, MVP, Aha Moment, Resumen de Spec de Producto
MVP / Lista de No Hacer      → User Story, esquema BD (si ya se generó), Resumen de Spec de Producto
North Star / Métricas      → Plan de Validación de Hipótesis, Resumen de Spec de Producto
Resumen de Spec de Producto      → Reporte HTML, PRD (si ya se generó)
```

### Dependencia de Extensión de Funcionalidad:
```
Dependencia de Extensión de Funcionalidad:
─────────────────────────────────────────────────────
S1 (Problema + Contexto)      → S2 (Soluciones), S3 (Riesgos), S4 (Alcance de Ejecución)
S2 (Solución Seleccionada)    → S3 (Riesgos), S4 (Alcance de Ejecución)
S3 (Evaluación de Riesgos)    → S4 (Alcance de Ejecución)
```

## Proceso de Ejecución

1. **Informar al usuario del alcance del impacto**: "Modificaste [paso]. Esto afecta [lista de pasos downstream]. Actualizaré cada uno."
2. **Confirmar o auto-actualizar ítems downstream**:
   - Si el cambio downstream es menor (ajustes de redacción) → Actualizar directamente y explicar qué cambió
   - Si el cambio downstream es significativo (cambio de dirección) → Solicitar confirmación del usuario sobre la nueva dirección antes de actualizar
3. **Re-integrar el Resumen de Spec de Producto**
4. **Si ya se generó un reporte HTML o PRD**: Re-generarlo directamente y producir un snapshot de versión:

```
📋 Snapshot de Versión v[versión anterior] → v[nueva versión]
Paso modificado: [Nombre del paso]
Contenido clave antes de modificación: [1-3 oraciones]
Contenido clave después de modificación: [1-3 oraciones]
Actualizaciones downstream activadas: [Qué pasos también se ajustaron]
```

## Principios
- Ninguna modificación ocurre en silencio — el alcance del impacto siempre debe comunicarse explícitamente
- El usuario tiene el derecho de elegir "solo modificar este paso, dejar downstream como está por ahora." Claude debe marcar qué partes están desactualizadas (agregar etiqueta ⚠️ Necesita Actualización)
- El historial de modificaciones permanece rastreable dentro de la conversación
