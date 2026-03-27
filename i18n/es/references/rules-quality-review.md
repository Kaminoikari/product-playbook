# 🔍 Reglas de Revisión de Calidad

> Se carga al completar cada paso. Este archivo separa el "proceso de revisión" de los "criterios de revisión", asegurando que el mecanismo de autoevaluación de calidad funcione realmente.

## ⚙️ Proceso de Revisión (Común a Todos los Modos)

Después de producir el output de cada paso, Claude debe ejecutar el siguiente proceso de revisión:

### Paso 1: Autoevaluación Ítem por Ítem

1. Buscar la lista de verificación de calidad correspondiente al paso actual (ver la sección "Criterios de Revisión" abajo)
2. Marcar cada ítem como ✅ o ❌
3. Los ítems marcados con ❌ deben incluir una explicación específica de "cómo mejorar"

### Paso 2: Crítica Obligatoria

- **No todos los ítems pueden ser ✅**: Si todos los ítems pasan, se debe identificar proactivamente "el aspecto más débil de este output" y explicar cómo fortalecerlo
- Esto no es ser quisquilloso — asegura que la autoevaluación no se convierta en un sello de goma
- Siguiendo el espíritu de Amazon PR-FAQ: la calidad viene de encontrar problemas, no de confirmar que no hay ninguno

### Paso 3: Formato de Presentación

```
📝 Autoevaluación de Calidad:
- ✅ [Ítem de verificación]
- ✅ [Ítem de verificación]
- ❌ [Ítem de verificación] → Dirección de mejora: [explicación específica]
⚠️ Aspecto más débil: [descripción] → Sugerencia de fortalecimiento: [acción específica]
```

---

## 📋 Criterios de Revisión (Por Paso)

> A continuación se presentan las listas de verificación independientes para cada framework. El proceso de revisión no cambia — solo se sustituye la lista de verificación correspondiente.

### Persona

| # | Ítem de Verificación |
|---|---------------------|
| 1 | ¿La segmentación se basa en "propósito/tarea/motivación" en lugar de demografía? |
| 2 | ¿Las Personas son MECE (mutuamente excluyentes y colectivamente exhaustivas del mercado objetivo)? |
| 3 | ¿Se identifica claramente el TA principal vs. el TA secundario? |
| 4 | ¿Los "problemas/desafíos" de cada Persona provienen de observaciones reales o inferencias razonables? |
| 5 | ¿El "enfoque actual y su razón" es lo suficientemente específico para identificar workarounds? |

Problemas comunes: Segmentar por edad/género, Personas demasiado similares entre sí, puntos de dolor demasiado vagos

### JTBD (Jobs to Be Done)

| # | Ítem de Verificación |
|---|---------------------|
| 1 | ¿Incluye un contexto específico? (No "en cualquier momento y lugar" sino "a altas horas de la noche cuando no puedo contactar al banco") |
| 2 | ¿Se enfoca en un solo trabajo central? (No tres trabajos fusionados en una oración) |
| 3 | ¿Se identifican los trabajos funcionales, emocionales y sociales? |
| 4 | ¿Se puede usar para evaluar "¿esta solución resuelve este trabajo"? |
| 5 | ¿Incluye el "enfoque actual" y la "brecha"? (brecha = oportunidad) |
| 6 | ¿La Q5 de las cinco preguntas de profundización toca la motivación emocional/identidad profesional/miedo psicológico? (No una descripción funcional) |

### Positioning (Posicionamiento)

| # | Ítem de Verificación |
|---|---------------------|
| 1 | ¿La "alternativa competitiva" es desde la perspectiva del usuario? (Lo que los usuarios realmente usan como sustituto, no lo que tú crees que es la competencia) |
| 2 | ¿El "atributo único" es algo que las alternativas competitivas no pueden hacer o hacen mal? |
| 3 | ¿El "valor para el usuario" está expresado en lenguaje del usuario o del producto? ("Ahorra 2 horas" vs. "Automatización impulsada por IA") |
| 4 | ¿El "mercado objetivo" es lo suficientemente específico para encontrar a estas personas? |
| 5 | ¿Los cinco elementos de posicionamiento son lógicamente consistentes entre sí? |

Problemas comunes: Desconexión entre atributo único y valor, categoría de mercado incorrecta que lleva a ser juzgado por estándares equivocados

### HMW (How Might We)

| # | Ítem de Verificación |
|---|---------------------|
| 1 | ¿Tiene restricciones claras? (No completamente abierto) |
| 2 | ¿Deja suficiente espacio para soluciones? (No apunta a una única solución) |
| 3 | ¿Se mapea directamente a un JTBD o punto de dolor? |
| 4 | ¿El equipo puede empezar a idear soluciones al ver este HMW? |

Problemas comunes: Demasiado amplio (equivale a reafirmar la visión), demasiado estrecho (equivale a especificar la solución), múltiples problemas mezclados

### PR-FAQ (Comunicado de Prensa + FAQ)

| # | Ítem de Verificación |
|---|---------------------|
| 1 | ¿El titular está escrito desde la perspectiva del usuario? ("Los usuarios ahora pueden hacer X" vs. "Lanzamos la funcionalidad Y") |
| 2 | ¿El lector puede entender "por qué esto importa" en los primeros 10 segundos del primer párrafo? |
| 3 | ¿La descripción del punto de dolor proviene de un escenario real de usuario? |
| 4 | ¿La primera oración de la sección de solución comienza con el sentimiento/escenario del usuario (no un verbo funcional)? |
| 5 | ¿La cita del usuario suena como algo que diría una persona real? |
| 6 | ¿El FAQ incluye preguntas agudas comparando con herramientas existentes? |

Problemas comunes: El titular parece un anuncio de producto no una noticia, la sección de solución se convierte en una lista de funcionalidades, las preguntas del FAQ son todas fáciles de responder

### North Star Metric (Métrica Estrella del Norte)

| # | Ítem de Verificación |
|---|---------------------|
| 1 | ¿Refleja el valor que reciben los usuarios? (No ingresos, no DAU) |
| 2 | ¿Puede crecer continuamente? (No alcanzará naturalmente un techo) |
| 3 | ¿Todos en el equipo saben qué hacer cuando ven esta métrica? |
| 4 | ¿Se puede manipular? (Si es así, se necesitan métricas de protección) |
| 5 | Para productos B2B: ¿refleja el valor a nivel de la organización del cliente, no solo de usuarios individuales? |

Problemas comunes: Usar ingresos como North Star (los ingresos son un resultado, no un impulsor), la métrica es demasiado compuesta para ser accionable

### Aha Moment (Momento Aha)

| # | Ítem de Verificación |
|---|---------------------|
| 1 | ¿Es un comportamiento específico y rastreable? (No "siente que el producto es útil") |
| 2 | ¿Está directamente relacionado con el trabajo funcional en JTBD? |
| 3 | ¿El tiempo objetivo para alcanzarlo es razonable? (B2C debería ser en el primer uso; B2B puede ser dentro del período de prueba) |
| 4 | ¿Se puede diseñar el onboarding para guiar a los usuarios a alcanzarlo más rápido? |

### Verificación de Seguridad

> Para criterios detallados, ver `references/08-security-checklist.md`. A continuación un resumen de autoevaluación de calidad:

| # | Ítem de Verificación |
|---|---------------------|
| 1 | El método de autenticación ha sido seleccionado explícitamente, no se dejó como "pendiente" |
| 2 | Al menos 3 headers de seguridad han sido planificados |
| 3 | La estrategia de Rate Limiting ha sido adaptada a las características del producto (no una copia de plantilla) |
| 4 | .gitignore incluye todos los archivos sensibles |

### Exportación de Documentos

> Para criterios detallados, ver `references/rules-export-document.md`.

| # | Ítem de Verificación |
|---|---------------------|
| 1 | No hay sintaxis Markdown residual en el HTML (`**`, `##`, `|---|`) |
| 2 | Todas las filas y columnas de tablas coinciden con el contenido original |

---

## 🔄 Revisión de Consistencia Entre Pasos

> Se carga al final del flujo. Para ítems de verificación detallados por modo, ver `references/rules-end-of-flow.md`.

La revisión de consistencia entre pasos es una segunda capa de revisión independiente de las autoevaluaciones de calidad de un solo paso, ejecutada después de completar todos los pasos. Su propósito es capturar inconsistencias aguas abajo causadas por modificaciones aguas arriba durante la iteración.

### Ítems de Verificación Rápida (Común a Todos los Modos)

| # | Dimensión de Verificación | Pregunta de Validación |
|---|--------------------------|----------------------|
| 1 | Consistencia de usuario objetivo | ¿JTBD, Posicionamiento y PR-FAQ apuntan al mismo grupo de personas? |
| 2 | Consistencia del problema central | ¿El PR-FAQ aborda el problema declarado en JTBD? ¿El MVP lo resuelve? |
| 3 | Solución ↔ Alcance | ¿La solución seleccionada es consistente con el alcance del MVP? |
| 4 | Métrica ↔ Valor | ¿El North Star mide los resultados del JTBD? |
| 5 | Vigencia de riesgos | ¿Los riesgos del Pre-mortem siguen siendo relevantes para la solución final? |

---

## 📐 Principios de Diseño

Este archivo sigue el patrón de diseño Reviewer: **los criterios de revisión y el proceso de revisión se mantienen por separado**.

- **El proceso no cambia**: Paso 1 (autoevaluación ítem por ítem) → Paso 2 (crítica obligatoria) → Paso 3 (formato de presentación)
- **Los criterios son intercambiables**: Al agregar nuevos frameworks, solo se agrega la lista de verificación correspondiente en la sección "Criterios de Revisión"
- **Carga independiente**: Cada archivo de referencia mantiene su lista de verificación embebida como recordatorio en línea; este archivo sirve como punto de entrada de revisión unificado
