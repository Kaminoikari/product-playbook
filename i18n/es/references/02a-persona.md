# Etapa 1: Descubrimiento — Construyendo Personas

### 🚫 Alcance de Salida de Descubrimiento (Hard Gate)

Cuando el orchestrator recibe el pedido de ejecutar trabajo de Descubrimiento (Persona, JTBD, OST, Journey Map, Descubrimiento Continuo), la salida debe **mantenerse dentro del alcance de Descubrimiento**. Descubrimiento responde "quién es el usuario" y "qué necesidad insatisfecha intenta cubrir" — nada más. Los siguientes artefactos de etapas downstream **NO deben aparecer** en un entregable de Descubrimiento, incluso si se siente natural mencionarlos:

- **Artefactos de etapa Define**: declaración de positioning, preguntas HMW (How Might We), matrices de pain points que doblan como prompts de solución
- **Artefactos de etapa Develop**: borradores de PR-FAQ, escenarios de pre-mortem, tablas RICE, definición de scope de MVP, secciones de PRD, listas de features
- **Artefactos de etapa Deliver**: definición de métrica North Star, criterios de PMF, plan GTM, bloques de business-model canvas, tablas de product spec
- **Artefactos de etapa Strategy**: Strategy Blocks, diagnosis / guiding-policy / coherent-action de Rumelt, descomposición de DHM Model, escalas OKR

Si los hallazgos de Descubrimiento sugieren fuertemente un artefacto downstream (ej. el análisis JTBD revela un ángulo de positioning claro), regístralo como una **open question o next-step pointer de una línea** al final — pero **NO produzcas el artefacto en sí**. La siguiente etapa tiene su propio step dedicado.

Ejemplo no aceptable: terminar un análisis JTBD con una tabla RICE poblada, una lista de scope de MVP, o un párrafo "Recommended Positioning" — incluso si todas las otras sub-secciones de Descubrimiento están correctas, esta salida FAIL este Hard Gate.

---

## Hábitos de Descubrimiento Continuo (Teresa Torres)

Construye un hábito clave: **Habla con al menos un usuario objetivo cada semana.** El descubrimiento no es un ritual único — es un sistema continuo.

> "El descubrimiento de producto debería ser un hábito continuo, no una ceremonia única antes de que un proyecto comience." — Teresa Torres

## 1.1 Construir la Tabla de Personas

Las Personas no se segmentan por edad y género, sino por **propósito / tarea / motivación** para distinguir diferentes tipos de usuarios.

### 🏢 Hard Gate B2B — Persona Buyer ≠ Persona User

Para cualquier producto B2B (o B2B2C), el **Buyer** (firma el contrato, controla el presupuesto, asume riesgo de vendor) y el **User diario** (toca el producto todos los días) son casi siempre roles distintos con **objetivos, pain points y criterios de decisión diferentes**. Tratarlos como una sola Persona colapsa dos Jobs distintos en un arquetipo borroso y el análisis resultante no puede impulsar decisiones de producto.

Regla del Hard Gate:
- Producir **dos bloques de Persona separados** etiquetados `Buyer` y `User` cuando el producto es B2B y los dos roles son distintos (suposición por defecto en B2B).
- Si son la misma persona (raro — usualmente herramientas fundador-led o B2B de un solo dueño), explicá en una oración por qué el buyer también es el user diario en este escenario específico.
- Cross-link entre las dos Personas: notá dónde el criterio de evaluación del Buyer depende de lo que el User realmente hace a diario (ej. "el criterio de audit-readiness del Buyer depende de que el User complete el formulario el mismo día y no en lote").

Ejemplo no aceptable: producir una sola Persona ("HR Manager") que fusiona aprobar presupuesto Y completar formularios diarios — dos Jobs distintos forzados en un arquetipo borroso. Esa salida FAIL este Hard Gate.

```
| Campo | Persona 1: [Apodo] | Persona 2: [Apodo] | Persona 3: [Apodo] |
|---|---|---|---|
| Propósito / Tarea / Motivación | | | |
| Tamaño (ESCALA) | | | |
| Problemas / Desafíos / Motivadores | | | |
| Enfoque Actual y Razón | | | |
| Frecuencia | | | |
| Fuentes de Información | | | |
| Barreras de Adopción / Ejecución | | | |
```

Explica la lógica de segmentación; verifica MECE (mutuamente excluyente, colectivamente exhaustivo); identifica el TA primario y secundario.

### 🎯 Reasoning de Priorización de Persona (Hard Gate)

Decir solo "identificar TA primario" sin un reasoning explícito falla este Hard Gate. La declaración de priorización debe nombrar una Persona como primaria Y explicar por qué **en términos específicos a la dinámica go-to-market del producto** — no claims genéricos de "frecuencia de uso".

Para **productos B2B con múltiples user personas**, el reasoning DEBE referenciar **al menos una** de estas dinámicas específicas B2B por nombre (usando estos términos o equivalentes claramente análogos):

- **Champion vs Buyer** — quién aboga internamente por la adopción versus quién firma el contrato; la adopción champion-led suele ganar la priorización B2B incluso cuando el buyer es la persona "más senior"
- **Adoption multiplier** — quién, al adoptar, desbloquea la adopción para el resto de la org (ej. el uso diario del HR Specialist siembra el system-of-record del que otras personas dependen después)
- **Switching-trigger ownership** — qué persona siente el dolor que justifica cambiar de la herramienta incumbente; quien posee el switching trigger es el candidato a priorización incluso si no es el usuario más pesado
- **Budget authority** — quién controla la línea de presupuesto; relevante cuando buyer ≠ user y los criterios del buyer dominan la decisión inicial del deal
- **Audit / compliance pressure ownership** — el rol de quién está en juego cuando aparecen hallazgos de auditoría; las personas presionadas por compliance suelen dominar la priorización en segmentos B2B regulados

Un reasoning puro de "Persona X la usa más" o "Persona Y tiene más usuarios" FAIL este Hard Gate para productos B2B. La frecuencia es necesaria pero nunca suficiente — el switching B2B es impulsado por presión organizacional, no por tasas de uso individual.

Para **productos B2C**, el reasoning debe referenciar al menos uno de: switching-trigger ownership, diferencial de severidad JTBD, network-effect seeding, o diferencial de willingness-to-pay. El reasoning puramente por frecuencia también falla para B2C.

### 📝 Lista de Verificación de Calidad de Persona
- ✅ ¿La segmentación está basada en "propósito/tarea/motivación" en lugar de datos demográficos?
- ✅ ¿Las Personas son MECE (mutuamente excluyentes y colectivamente exhaustivas del mercado objetivo)?
- ✅ ¿El TA primario vs. secundario está claramente identificado?
- ✅ ¿Los "problemas/desafíos" de cada Persona están basados en observaciones reales o inferencias razonables?
- ✅ ¿El "enfoque actual y razón" es lo suficientemente específico para identificar soluciones alternativas?
- ❌ Problemas comunes: Segmentar por edad/género, diferencias mínimas entre Personas, puntos de dolor demasiado vagos

## 1.2 Construir Tarjetas de Persona

```
## [Apodo de Persona]: [Descripción de una línea]

**Info Básica**: Edad / Género / Ocupación / Ubicación / Rasgos de personalidad
**Contexto**: [Descripción de contexto relevante al producto]
**Metas / Tareas**: [Meta 1], [Meta 2]
**Enfoque Actual y Razón**: [Qué hacen actualmente y por qué]
**Fuentes de Información**: [Dónde obtienen información relevante]
**Barreras / Problemas / Desafíos / Frustraciones**: [Punto de dolor 1], [Punto de dolor 2], [Punto de dolor 3]
```

---

## 📎 Consejos de Integración de Archivos para esta Etapa

Si el usuario sube archivos durante esta etapa, Claude los integra según estas reglas:

| Contenido Subido | Integrar En | Acción de Integración |
|-----------------|-------------|----------------------|
| Transcripciones de entrevistas de usuario / transcripciones de audio | 1.1 Persona + 1.3 JTBD | Extraer: contexto del usuario → campos de Persona; puntos de dolor + enfoque actual → preguntas de profundización JTBD; reacciones emocionales → Jobs emocionales/sociales |
| Reporte de investigación de usuarios (PDF) | 1.1 + 1.2 + 1.3 | Extraer datos cuantitativos (proporciones de segmentos de usuarios) al tamaño de Persona; extraer insights cualitativos a JTBD |