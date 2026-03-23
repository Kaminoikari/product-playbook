# ⚡ Secuencia de Pasos del Modo Build (7 Pasos + Output Final)

> Este archivo es la definición autoritativa de pasos para el Modo Build. Cargado por el despachador central de SKILL.md.

> ⚠️ Recordatorio obligatorio: "Omitir la fase de investigación de usuarios significa que tu solución está construida sobre suposiciones. Recomendamos realizar Descubrimiento Continuo lo antes posible después de la ejecución para validar."

## Secuencia de Pasos

```
S1. Confirmar declaración del problema (una oración)
S2. PR-FAQ → Leer references/04a-prfaq.md
S3. Soluciones paralelas → Leer references/04b-solutions.md → 3.2
S4. Pre-mortem → Leer references/04b-solutions.md → 3.3
S5. Priorización GEM + RICE → Leer references/04b-solutions.md → 3.4 + 3.5
S6. MVP + Lista de No Hacer → Leer references/04c-mvp.md
S7. North Star + Aha Moment → Leer references/05a-northstar-aha.md
────
Output Final → Resumen de ejecución orientado a ingenieros
```

## Instrucciones de Carga de Referencias

| Paso | Archivo de Referencia |
|------|----------------------|
| S1 | No se necesita referencia externa (guiar directamente al usuario para declarar el problema) |
| S2 | `references/04a-prfaq.md` |
| S3-S5 | `references/04b-solutions.md` |
| S6 | `references/04c-mvp.md` |
| S7 | `references/05a-northstar-aha.md` |

## Formato del Output Final

**Resumen de ejecución orientado a ingenieros**: Decisiones de solución → Límites del MVP → Métricas de éxito → Riesgos clave

Al completar, sigue `references/rules-end-of-flow.md` para ejecutar las reglas de fin de flujo.

---

## 🔧 Ruta Rápida de Extensión de Feature (4 Pasos)

> Se cambia automáticamente a esta ruta cuando el usuario está **agregando una sola funcionalidad a un producto existente**.
> Condiciones de activación: La descripción del usuario incluye frases como "agregar una funcionalidad," "nueva funcionalidad," "agregar funcionalidad XX," "sobre el sistema existente," "el producto existente necesita," etc.

**Diferencias con el Modo Build completo (7 pasos)**: Un producto existente ya tiene North Star, Aha Moment y posicionamiento de producto — no es necesario redefinirlos. Una sola funcionalidad no requiere un comunicado de prensa PR-FAQ ni una re-priorización completa GEM+RICE. El enfoque está en "qué agregar, cómo agregarlo, y si romperá funcionalidades existentes."

### Secuencia de Pasos de Extensión de Feature

```
S1. Problema + contexto del sistema existente
S2. Tres soluciones paralelas + pros/contras + recomendación AI → Leer references/04b-solutions.md → 3.2
S3. Evaluación de riesgos (regresión + compatibilidad) → Leer references/04b-solutions.md → 3.3
S4. Alcance de ejecución (qué hacer / qué no tocar / criterios de aceptación) → Leer references/04c-mvp.md
────
Output Final → Especificación de desarrollo de feature
```

### Pre-paso S1: Carga de Contexto de Producto

Antes de entrar a S1, lee `references/rules-context.md` y verifica `.product-context.md`:

- **Contexto completo disponible (Escenario 1)**: Trae automáticamente nombre del producto, stack tecnológico, módulos clave, y las 3 entradas más recientes del Historial de Decisiones. Cambia la guía de S1 a **estilo confirmación**: "Tu producto es [nombre], usando [stack tecnológico], con módulos clave incluyendo [lista de módulos]. ¿Qué funcionalidad quieres agregar? ¿Qué módulos serán afectados?" (Preguntas 2 y parte de la pregunta 3 están pre-llenadas — solo necesita confirmación)
- **Sin contexto (Escenario 2)**: Activar Context Bootstrap (`rules-context.md` Sección 4), luego proceder al S1 estándar abajo
- **Contexto parcial (Escenario 3)**: Traer stack tecnológico y módulos conocidos (fusionados del Historial de Decisiones), y recopilar las partes faltantes. Por ejemplo: "Además de [módulos conocidos], ¿hay otros módulos que podrían verse afectados?"

### Contenido de Guía S1 (Problema + Contexto del Sistema Existente)

Claude necesita recopilar la siguiente información (guiar paso a paso — no hacer todas las preguntas a la vez. Si el contexto ya ha pre-llenado algunas respuestas, confirmar en lugar de re-recopilar):

```
1. ¿Qué funcionalidad quieres agregar? ¿Qué problema resuelve?
2. Resumen de la arquitectura actual del producto (stack tecnológico, módulos clave) ← el contexto puede pre-llenar
3. ¿Qué módulos existentes afectará esta funcionalidad? ← el contexto puede pre-llenar parcialmente
4. ¿Hay algún feedback de usuarios o datos que respalden este requisito?
```

### Contenido de Guía S2 (Tres Soluciones Paralelas + Recomendación AI)

```
| HMW | Solución A (Conservadora / cambio mínimo) | Solución B (Equilibrada) | Solución C (Audaz / refactorización) |
|-----|------------------------------------------|-------------------------|-------------------------------------|
| [Problema] | | | |

| Solución | Pros | Contras | Alcance de Impacto | Complejidad de Implementación |
|----------|------|---------|-------------------|-------------------------------|
| A | | | | |
| B | | | | |
| C | | | | |

🤖 Recomendación AI: Solución [X]
Justificación: [Juicio integral basado en alcance de impacto, complejidad y riesgo]
```

### Contenido de Guía S3 (Evaluación de Riesgos — Enfocada en Regresión y Compatibilidad)

```
| Tipo de Riesgo | Riesgo Específico | Probabilidad | Mitigación |
|---------------|-------------------|-------------|-----------|
| Riesgo de regresión | [Áreas donde funcionalidades existentes pueden verse afectadas] | | |
| Riesgo de compatibilidad | [Conflictos con arquitectura/datos/APIs existentes] | | |
| Riesgo de rendimiento | [Impacto de la nueva funcionalidad en el rendimiento del sistema] | | |
| Riesgo de seguridad | [Consideraciones de seguridad introducidas por la nueva funcionalidad] | | |
```

### Contenido de Guía S4 (Alcance de Ejecución)

```
**Qué hacer (Alcance)**:
- [Ítems específicos de funcionalidad a agregar]
- [Módulos existentes que necesitan modificación]

**No Tocar**:
- [Módulos y funcionalidades que explícitamente no se deben modificar]
- [Razón para no tocarlos]

**Criterios de Aceptación**:
- [ ] [Condición específica comprobable]
- [ ] [Prueba de regresión: confirmar que funcionalidades existentes no se ven afectadas]
```

### Formato del Output Final de Extensión de Feature

**Especificación de desarrollo de feature**: Declaración del problema → Solución seleccionada + justificación → Alcance de impacto → Alcance de ejecución + criterios de aceptación → Lista de riesgos

### Salida Incremental de Documento (cuando hay documento fuente disponible)

Si el usuario subió un documento fuente (PRD, especificación, etc.) durante el proceso:

1. **Versión incremental** (predeterminada cuando existe documento fuente):
   - Insertar/modificar secciones en la estructura del documento original
   - Mantener el formato, estilo y convenciones de nomenclatura del archivo original
   - Contenido nuevo marcado con `[NEW]`
   - Contenido modificado marcado con `[UPDATED]` con el original preservado como referencia
   - Las secciones no relacionadas con la nueva funcionalidad permanecen completamente intactas

2. **Versión independiente** (cuando no hay documento fuente):
   - Usar el formato estándar de especificación de desarrollo de feature (como se definió arriba)

3. **Preguntar al usuario antes de generar**:
   "Detecté que subiste un [tipo de documento]. ¿Cómo deseas la salida?
    A) Actualización incremental sobre el documento original (recomendado)
    B) Especificación de desarrollo de feature independiente"

### Instrucciones de Carga de Referencias

| Paso | Archivo de Referencia |
|------|----------------------|
| S1 | No se necesita referencia externa |
| S2 | `references/04b-solutions.md` → 3.2 |
| S3 | `references/04b-solutions.md` → 3.3 |
| S4 | `references/04c-mvp.md` |

Al completar, sigue `references/rules-end-of-flow.md` para ejecutar las reglas de fin de flujo.
