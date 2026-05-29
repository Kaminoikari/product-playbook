# Fase 1: Descubrimiento — Análisis JTBD

## 1.3 Análisis JTBD (Jobs to Be Done)

> "La unidad de análisis no es el consumidor, sino el trabajo que el consumidor está tratando de realizar." — Clayton Christensen

**Cobertura JTBD de Tres Capas (Hard Gate — las tres capas requeridas):**

Cada análisis JTBD DEBE hacer aflorar **las tres capas explícitamente**: **Funcional** (la tarea que se está completando), **Emocional** (cómo el usuario quiere sentirse durante/después), y **Social** (cómo el usuario quiere ser percibido). Producir solo la capa Funcional es el fallo más común en JTBD — los Jobs Emocionales y Sociales suelen ser los verdaderos disparadores de switching, especialmente en B2B. Si una Persona dada genuinamente no tiene un Job Emocional o Social significativo para el producto, decilo explícitamente con una oración de reasoning en lugar de omitir silenciosamente la fila.

**Forma Canónica JTBD (Hard Gate — se requiere estructura de tres cláusulas):**

Cada declaración JTBD (Primary, Funcional, Emocional, Social — cada capa) DEBE escribirse como una oración completa de tres cláusulas en la forma canónica. Las tres cláusulas son obligatorias:

```
Cuando [situación], quiero [motivación], para que [resultado].
```

Al producir output en inglés, usar la forma canónica equivalente:
```
When [situation], I want to [motivation], so [outcome].
```

**Ejemplos no válidos** (fragmentos en celda de tabla, faltan cláusulas):
- ❌ "Capturar ideas clave rápidamente" (falta Cuando; falta para que)
- ❌ "Anotar pensamientos en el viaje al trabajo" (falta quiero; falta resultado)

**Ejemplo válido** (las tres cláusulas presentes):
- ✅ "**Cuando** acabo de terminar de leer un artículo y la idea clave todavía está fresca, **quiero** capturar una conclusión en 5 segundos, **para que** semanas después aún pueda encontrarla y conectarla con una nueva idea."

Ejemplo: **Cuando** está comparando opciones de hipoteca a altas horas de la noche y no puede contactar a un banco, un comprador primerizo **quiere** estimar rápidamente los pagos mensuales, **para que** pueda explicarle a su pareja su plan financiero.

**Tabla de Análisis de Cuatro Tipos JTBD:**

Cada celda (Persona 1 / Persona 2) DEBE contener una oración JTBD completa de tres cláusulas. **Frases cortas como "Sentir que sigo cumpliendo conmigo mismo", "registrar entrenamientos a diario", "seguir el progreso fácilmente" todas FAIL el Hard Gate.** Usá el ejemplo desarrollado de abajo como la forma literal — cada celda debe leerse como una oración con `When …, I want to …, so …`.

Ejemplo desarrollado (rastreador de hábitos de fitness B2C, una sola Persona — replicá esta forma para cada celda):

| Tipo JTBD | Definición | Persona: Profesional Ocupado |
|-----------|------------|-----------|
| Job Funcional | Completar una tarea específica o lograr un objetivo funcional | **Cuando** llego a casa después de un largo día de trabajo y tengo 20 minutos antes de mi próximo compromiso, **quiero** registrar el entrenamiento que acabo de hacer y ver qué se recomienda a continuación, **para que** pueda mantener la racha sin gastar energía mental planificando. |
| Job Emocional | Cómo se sienten o quieren sentirse | **Cuando** me pierdo un entrenamiento planificado dos días seguidos, **quiero** sentir que sigo en el camino en lugar de empezar de cero, **para que** no caiga en la espiral de todo-o-nada que mata mi consistencia. |
| Job Social | Cómo quieren ser percibidos por otros | **Cuando** un amigo me pregunta cómo va mi entrenamiento, **quiero** mostrar un registro limpio de actividad reciente, **para que** se me vea como alguien que cumple los compromisos consigo mismo. |
| Contexto del Job | Bajo qué circunstancias necesitan realizar este trabajo | **Cuando** mi agenda es volátil a lo largo de la semana (reuniones tempranas, llamadas nocturnas), **quiero** encajar entrenamientos en ventanas de 15–45 minutos donde sea que caigan, **para que** el entrenamiento se adapte a mi vida en lugar de competir con ella. |

Tabla vacía (llená cada celda con oraciones completas `When …, I want to …, so …` — NO la acortes a frases):

```
| Tipo JTBD | Definición | Persona 1 (debe usar la forma completa "Cuando … quiero … para que …") | Persona 2 (igual) |
|-----------|------------|-----------|-----------|
| Job Funcional | Completar una tarea específica o lograr un objetivo funcional | | |
| Job Emocional | Cómo se sienten o quieren sentirse | | |
| Job Social | Cómo quieren ser percibidos por otros | | |
| Contexto del Job | Bajo qué circunstancias necesitan realizar este trabajo | | |
```

**Cinco Preguntas de Profundización JTBD:**
1. **Problema Raíz**: Detrás de lo que los usuarios expresan como su necesidad, ¿qué están realmente tratando de resolver?
2. **Restricciones Actuales**: ¿Qué soluciones han sido descartadas debido a ciertas limitaciones?
3. **Soluciones Alternativas Actuales**: ¿Cómo están lidiando los usuarios hoy? ¿Qué soluciones improvisadas han construido?
4. **Brecha**: ¿Dónde se quedan cortas las soluciones alternativas actuales? (Esta brecha es tu oportunidad)
5. **Solución Ideal**: Si se eliminaran las restricciones, ¿cómo sería su solución ideal?

**Mejores Prácticas de Entrevista a Usuarios de Teresa Torres:**
- Enfócate en el **comportamiento pasado real** de los usuarios, no en comportamiento futuro hipotético
- Pregunta "La última vez que tuviste este problema, ¿qué hiciste?" en lugar de "¿Qué funcionalidades te gustarían?"
- Errores más comunes: hacer preguntas hipotéticas, introducir sesgo de solución, no profundizar en detalles

### 📝 Lista de Verificación de Calidad JTBD

Claude debe autoevaluar después de producir el output JTBD (cada ítem debe marcarse ✅ o ❌; ítems ❌ deben incluir cómo mejorar):
- [ ] ¿**Las tres capas** (Funcional / Emocional / Social) están escritas en la forma canónica completa "Cuando … quiero … para que …" (en inglés "When … I want to … so …")? (Si a cualquier capa le falta una cláusula → marcar ❌)
- [ ] ¿Incluye un contexto específico? (No "en cualquier momento y lugar" — sino "a altas horas de la noche cuando no puede contactar al banco")
- [ ] ¿Se enfoca en un solo trabajo central? (No tres trabajos metidos en una sola oración)
- [ ] ¿Puede usarse para evaluar "¿Esta solución realmente aborda este trabajo?"
- [ ] ¿Incluye "soluciones alternativas actuales" y "brecha"? (Brecha = oportunidad)
- [ ] ¿La P5 de la Profundización **usa explícitamente al menos una palabra del vocabulario canónico** (`fear`, `anxiety`, `shame`, `worry`, `dread`, `self-doubt`, `sense of loss`, `threat to identity`, `embarrassment`, `guilt`)? Paráfrasis consecuenciales como "credibilidad en riesgo" o "reputación dañada" FAIL este ítem — son consecuencias, no la emoción sentida.

**Reglas de Ejecución (Hard Gate):**
- Debe marcar cada ítem ✅ o ❌ — listas [ ] en blanco o ✅ sin explicación no están permitidas
- **La checklist DEBE contener al menos un ❌** (ver regla "Crítica Obligatoria" en `references/rules-quality-review.md`). Un marcador de advertencia ⚠️ no puede reemplazar ❌; una nota de "aspecto más débil" añadida fuera de la checklist tampoco puede reemplazar un ❌ dentro de ella. Si después de una revisión honesta todos los ítems parecen aprobados, baja la vara y encuentra el ítem que más merece ser marcado ❌, especificando cómo fortalecerlo.
- ❌ Problemas comunes: estructura de tres cláusulas incompleta (falta Cuando / quiero / para que), demasiado abstracto, demasiados jobs mezclados, falta contexto, sustituir funcionalidades del producto por descripciones de jobs, P5 quedándose a nivel funcional

---

### 🏢 Requisitos de Profundización para Productos B2B (Hard Gate)

**Hard Gate — para cualquier producto B2B (o B2B2C), los siguientes tres sub-análisis son TODOS obligatorios. Saltarse cualquiera es una contract failure, sin importar si el usuario lo pidió explícitamente.** Si el tipo de producto es ambiguo, hacé una pregunta de clarificación; no asumas silenciosamente B2C.

#### Análisis de Jobs a Nivel Organizacional (Hard Gate — cubrir al menos 2 niveles)

Un análisis JTBD B2B que se queda puramente al nivel de usuario individual FAILS este gate. Los Jobs a nivel organizacional (auditoría de cumplimiento, flujos de aprobación cross-departamentales, control de costos, alineación de políticas de headcount, integridad de pista de auditoría) son necesidades que existen más allá de la tarea diaria de cualquier usuario individual y rutinariamente dominan las decisiones de switching B2B. La tabla de abajo DEBE producirse y al menos 2 de los 3 niveles DEBEN contener Jobs específicos de B2B (no enunciados genéricos de productividad).

| Nivel | Descripción | Ejemplos |
|-------|-------------|----------|
| **Job Estratégico** | Necesidades cross-departamentales a nivel organización/gestión | Auditorías de cumplimiento, control de costos, optimización de fuerza laboral |
| **Job Operacional** | Necesidades de coordinación a nivel proceso/gerente de departamento | Gestión de flujo de aprobaciones, sincronización de información entre equipos |
| **Job de Tarea** | Necesidades operativas diarias de usuarios individuales | Llenar formularios, verificar estados, exportar reportes |

#### Análisis Comprador (Buyer) vs. Usuario (User) (Hard Gate)

El comprador de un producto B2B (firma el contrato, controla el presupuesto) y el usuario diario (toca el producto todos los días) son casi siempre dos roles, **correspondientes a Jobs diferentes**. Tratarlos como una sola Persona es el fallo más común en Descubrimiento B2B. Regla del Hard Gate:

- Si buyer ≠ user (suposición por defecto en B2B), producir **dos bloques separados de Persona+JTBD**: uno para el Buyer (justificación de ROI, reducción de riesgo, compliance, consolidación de vendors, audit-readiness), y uno para el User (eficiencia, reducción de errores, contexto de uso diario). Y cross-link: notá dónde el Job del Buyer depende del Job del User (ej. "el Job de compliance del Buyer depende de que el User realmente complete el reporte cada ciclo, no de que lo haga en batch al final del mes").
- Si buyer = user (raro — usualmente herramientas fundador-led), explicá en una oración por qué en este escenario específico el tomador de decisiones también es el usuario diario — no lo asumas silenciosamente.
- Ejemplo no aceptable: producir una sola Persona ("HR Manager") que fusiona la autoridad de aprobar presupuesto Y el llenado diario de formularios. Eso colapsa dos Jobs distintos en un rol borroso y el análisis no puede impulsar decisiones de producto.

#### Cinco Preguntas de Profundización — Versión Mejorada B2B (Hard Gate)

**Hard Gate — la P5 DEBE usar explícitamente al menos una palabra del siguiente vocabulario canónico**: `fear` (miedo), `anxiety` (ansiedad), `shame` (vergüenza), `worry` (preocupación), `dread` (pavor), `self-doubt` (auto-duda), `sense of loss` (sensación de pérdida), `threat to identity` (amenaza a la identidad), `embarrassment` (bochorno), `guilt` (culpa). Paráfrasis funcionales/consecuenciales como "credibilidad en riesgo", "reputación dañada", "métrica cae", "usuarios churnean", "pierde confianza", "impacto en la carrera" FAIL este gate aunque describan stakes B2B reales — son *consecuencias*, no la *emoción sentida* de la cual el persona quiere *alejarse*.

Una P5 que describe la motivación más profunda del persona solo en lenguaje funcional FALLA el contrato de Descubrimiento: el propósito entero de la P5 es hacer aflorar el *miedo/ansiedad sentido* que impulsa el switching — los resultados puramente funcionales pueden resolverse con herramientas incrementalmente mejores, pero es el fear/anxiety sentido lo que hace que un buyer B2B supere la inercia organizacional y firme un nuevo contrato.

**Ejemplos válidos** (cada uno contiene una palabra del vocabulario canónico):
- ✅ Identidad profesional: "Ella **teme (fears)** verse incompetente frente al liderazgo cuando este reporte representa la credibilidad de su departamento"
- ✅ Motivación emocional: "Él carga una **ansiedad (anxiety)** silenciosa de que sus reportes directos descubran que en realidad no tiene un control firme de los números"
- ✅ Miedo psicológico: "Su mayor **pavor (dread)** es que el auditor encuentre una brecha en el proceso — ya le llamaron la atención una vez, y la **vergüenza (shame)** de un segundo incidente marcaría su expediente para siempre"
- ✅ Amenaza a la identidad: "Él siente una **amenaza a la identidad (threat to identity)** cuando consultores externos explican mejor que él las métricas de su propio equipo frente a la junta"

**Ejemplos no válidos** (funcional/consecuencial, sin vocabulario canónico):
- ❌ "Necesita una mejor herramienta para mejorar la eficiencia" (funcional)
- ❌ "Su credibilidad con el liderazgo está en riesgo" (consecuencia, no emoción sentida)
- ❌ "Podría perder su trabajo si este reporte está mal" (resultado, no emoción — ¿qué *siente* sobre esa posibilidad?)
- ❌ "Su reputación en la organización se vería afectada" (consecuencia — reemplazar con `embarrassment`, `shame`, o `dread`)

Si la motivación más profunda del persona genuinamente no mapea a ninguna palabra del vocabulario canónico después de un análisis honesto, marcá el ítem P5 de la Checklist de Calidad JTBD como `❌` con la explicación "La P5 actualmente vive a nivel de consecuencia; se necesita una pregunta más de entrevista que sondee la emoción sentida" — no parafrasees la lista de vocabulario para hacer aparecer una marca de verificación.

#### Análisis de Alternativas Competitivas (Obligatorio)

Lista las alternativas que los usuarios realmente están usando hoy:
- Al menos 2 herramientas existentes nombradas (p.ej., Slack / Excel / formularios en papel / email / comunicación verbal)
- Para cada herramienta, explica su "falla fundamental": no que las funcionalidades sean débiles, sino "por qué esta falla ha sido aceptada y dejada sin resolver" (¿inercia organizacional? ¿costos de cambio? ¿al liderazgo no le importa?)

### 📋 Plantilla de Plan de Entrevista a Usuarios

```
## Plan de Entrevista a Usuarios

**Objetivo de Investigación**: Entender cómo [Persona objetivo] lidia con [problema específico] en [Contexto del Job]
**Criterios de Selección**:
  - Debe haber experimentado [comportamiento específico] en los últimos [X días/semanas]
  - Excluir: [quién no es adecuado — p.ej., empleados internos, power users conocidos]

**Preguntas Centrales (5–7)**:
1. La última vez que tuviste [problema], ¿puedes contarme cómo lo manejaste? (Recuerdo conductual)
2. Durante ese proceso, ¿cuál fue la parte más frustrante o que más tiempo tomó? (Identificación de punto de dolor)
3. ¿Has probado otros enfoques? ¿Por qué sí o por qué no? (Alternativas actuales)
4. Si esa parte pudiera ser mejor, ¿cómo se vería "mejor" para ti? (Estado ideal)
5. ¿Con qué frecuencia sucede esto? ¿Cuándo fue la última vez? (Frecuencia y urgencia)
6. Además de ti, ¿quién más se ve afectado por este problema? (Mapeo de stakeholders)
7. En una escala de 1–10, ¿qué tan severo es este problema para ti? ¿Por qué? (Cuantificación del dolor)

**Estrategias de Seguimiento**:
  - Cuando el entrevistado dice "Normalmente yo..." → Pregunta "¿Qué pasó específicamente la última vez?"
  - Cuando el entrevistado menciona una emoción → Pregunta "¿Puedes describir ese sentimiento más específicamente?"
  - Cuando el entrevistado menciona una herramienta/método → Pregunta "¿Qué te hizo elegir ese enfoque?"

**Formato de Documentación**:
  - Transcripción textual o grabación
  - Dentro de las 24 horas post-entrevista, etiquetar: citas clave / puntos de dolor / hallazgos sorprendentes / contradicciones con suposiciones
```

---

## 📎 Notas de Integración de Archivos para esta Fase

Si el usuario sube archivos durante esta fase, Claude los integra de la siguiente manera:

| Contenido Subido | Integrar En | Acción de Integración |
|-----------------|-------------|----------------------|
| Transcripciones de entrevistas / texto de grabaciones | 1.1 Persona + 1.3 JTBD | Extraer: contexto del usuario → campos de Persona; puntos de dolor + soluciones alternativas actuales → Cinco Preguntas de Profundización JTBD; reacciones emocionales → Jobs Emocionales / Sociales |
| Capturas de pantalla de apps competidoras | 1.3 JTBD (soluciones alternativas actuales) | Identificar como "alternativa actual" del usuario, analizar soluciones improvisadas y brechas |