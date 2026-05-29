# 🔄 Secuencia de Pasos del Modo Revisión (6 Core + 2 Optional, total 6–8 pasos)

> Definición autoritativa de pasos para el Modo Revisión. Despachado desde SKILL.md.

**Reducido desde el flujo original de 12 pasos (v1.0.x) fusionando frameworks redundantes y condicionando los opcionales a disparadores.** Consulta `references/rules-optional-trigger.md` para la lógica de disparo y el formato del Punto de Decisión de Fase.

## Secuencia de Pasos

```
Fase 0: Análisis del Estado Actual
  S1.  Revisión del Estado Actual + Re-validación de JTBD  [Core]
       (Fusionado: inventario de datos + qué Jobs existentes están bien/mal cubiertos)

Fase 1: Convergencia del Problema
  S2.  Recopilación de Puntos de Dolor de Usuarios  [Core]
       (Análisis de retención/churn + síntesis de feedback + datos de comportamiento)
  S3.  Puntos de Dolor + HMW + Ranking de Oportunidades  [Core]
       → references/03-define.md
       (Fusionado: Resumen de Puntos de Dolor + HMW + Tabla de Evaluación de Oportunidades)
  S4.  Re-evaluación de Posicionamiento  [Optional — ver disparadores]
       → references/03-define.md

Fase 2: Diseño de Solución
  S5.  PR-FAQ (experiencia post-revisión)  [Core]
       → references/04a-prfaq.md
  S6.  Pre-mortem  [Optional — ver disparadores]
       → references/04b-solutions.md
  S7.  MVP + Lista de No Hacer  [Core]
       → references/04c-mvp.md

Fase 3: Validación
  S8.  North Star + Aha (comparación antes/después) + Plan de Validación de Hipótesis  [Core]
       → references/05a-northstar-aha.md + references/05c-validation-spec.md
       (Fusionado: cualquier revisión debe validar hipótesis; fuertemente acoplados)

────
Output Final → Resumen de Spec de Producto (edición de revisión)
```

### Pre-paso S1: Carga de Contexto de Producto

Antes de entrar en S1, lee `references/rules-context.md` y verifica `.product-context.md`:

- **Contexto completo (Escenario 1)**: Auto-rellenar nivel de PMF, North Star, puntos de dolor conocidos, estado de seguridad, y las 3 entradas más recientes del Historial de Decisiones. Cambia S1 a **modo delta**: "La última evaluación dejó tu nivel de PMF en [X] y tu North Star en [Y]. ¿Han cambiado? ¿Cuáles son los últimos números de DAU/MAU y retención?" — el historial de decisiones y los puntos de dolor conocidos no necesitan re-recopilarse.
- **Sin contexto (Escenario 2)**: Activar Context Bootstrap (`rules-context.md` Sección 4, Ronda 1 + 3), luego entrar en la recopilación estándar de datos de S1.
- **Contexto parcial (Escenario 3)**: Traer historial de cambios de features del Historial de Decisiones (qué módulos se han tocado, qué riesgos se han identificado), pero preguntar sobre estrategia general del producto y métricas (anteriormente solo se hizo extensión de features — falta la visión global).

### Guía Estándar de S1

> El S1 del Modo Revisión pide proactivamente al usuario datos del producto existente: DAU/MAU, retención, feedback principal de usuarios, decisiones clave de versiones anteriores, etc. Si el contexto ya pre-rellena algunas respuestas, cambia a confirmación en lugar de re-recopilación.
> S1 también recopila el estado de seguridad actual: mecanismos de auth/authz existentes, brechas de seguridad conocidas o deuda técnica, incidentes de seguridad recientes. Estos datos alimentan la evaluación de riesgos de la revisión y el Pre-mortem (si se dispara).

### Requisitos de Salida de S1 (Hard Gates)

Cada respuesta de S1 del Modo Revisión DEBE contener LOS CUATRO de:

1. **Enmarca esto como revisión, no como 0-a-1** — abre con una o dos frases que señalen que este es un análisis de un *producto existente*: estamos re-validando los JTBD existentes contra los datos actuales, comparando métricas de referencia (baseline) y leyendo `.product-context.md` para decisiones previas. Esto difiere del Discovery 0-a-1 (que parte de un modelo de usuario en blanco). Sin este encuadre, el usuario no puede saber por qué las preguntas son diferentes.

2. **Usa los números reales del usuario textualmente** — cita el MAU, el % de caída de retención, los tamaños de cohorte y las fechas del prompt del usuario de vuelta en tu análisis (p. ej. "la caída del 85% al 72% el último trimestre, sobre la base de 2.800 MAU, significa aproximadamente N usuarios afectados…"). La discusión genérica que ignora los números FAILS este gate.

3. **Trata la causa declarada por el usuario como H1, no como hecho** — cuando el usuario nombra una causa probable ("la caída de retención es causada por la complejidad de las features"), etiquétala explícitamente como H1 y expón al menos DOS hipótesis rivales (H2, H3) extraídas de los mismos datos. Ejemplos de hipótesis rivales a considerar: cambio en la mezcla de cohortes, regresión del onboarding, cambio de precios, lanzamiento competitivo, caída de la calidad del soporte, deprecación de features, efecto estacional. **Aceptar acríticamente la causa declarada por el usuario FAILS este gate** — el valor del Modo Revisión es la disciplina de hipótesis.

4. **Lista de brechas de datos con al menos una brecha orientada a la segmentación** — enumera específicamente qué datos adicionales se necesitan para discriminar entre H1/H2/H3. **Al menos un ítem DEBE ser una brecha de segmentación**: cohorte (mes de registro), tier (gratis/pago), rol (admin/usuario), segmento de uso de features. Un genérico "más entrevistas de usuario" por sí solo FAILS — nombra *qué segmento* entrevistarías y *qué específicamente* preguntarías.

### Formato de Cierre de S1 (Hard Gate)

Termina la respuesta de S1 con un menú numerado de CTA, NUNCA con una pregunta abierta. Usa exactamente esta forma:

```
What's next? Pick one:
  1️⃣ Share the requested data so we can move to S2 (pain-point convergence with hypothesis testing)
  2️⃣ Refine the hypothesis list before collecting data (suggest more H_n candidates)
  3️⃣ Skip to S3 if you already have enough data to converge on a top hypothesis
  4️⃣ Pause and resume later (progress will be saved to .product-playbook-progress.md)
```

Las respuestas que terminan con "Any thoughts?" / "Let me know what you think" / "Share what you have" sin un menú numerado FAIL el contrato — el usuario necesita un handle claro para el siguiente movimiento.

### Ruta Rápida

Cuando el usuario proporciona datos suficientes en S1 (con feedback, métricas, prioridades), S3 puede producirse en un único intercambio en lugar de múltiples confirmaciones. Condición de disparo: la lista de puntos de dolor recopilada en S2 ya tiene prioridades explícitas y soporte de datos. Las reglas de Hard Gate permanecen sin cambios — el output de cada paso debe presentarse completo; solo se acelera la cadencia de confirmación.

## Reglas de Disparo Optional

Lee `references/rules-optional-trigger.md` para las condiciones de disparo autoritativas y el formato de salida del Punto de Decisión de Fase.

**Referencia rápida:**
- **S4 Re-evaluación de Posicionamiento** se dispara cuando: el usuario menciona "deriva de posicionamiento" / "el mercado cambió" / la audiencia incluye Sales/Marketing
- **S6 Pre-mortem** se dispara cuando: alcance del cambio ≥30% de la funcionalidad existente / toca pagos-permisos-migración de datos

## Requisito del Punto de Decisión de Fase

Antes de entrar en la Fase 1 y la Fase 2, renderiza el bloque de Punto de Decisión de Fase (formato definido en `rules-optional-trigger.md`). La Fase 0 y la Fase 3 contienen solo pasos Core y omiten el punto de decisión.

## Instrucciones de Carga de Referencias

| Paso | Archivo de Referencia |
|------|----------------------|
| S1–S2 | (sin referencia externa; recopilación directa de datos del usuario) |
| S3 | `references/03-define.md` |
| S4 (si se dispara) | `references/03-define.md` |
| S5 | `references/04a-prfaq.md` |
| S6 (si se dispara) | `references/04b-solutions.md` |
| S7 | `references/04c-mvp.md` |
| S8 + Output Final | `references/05a-northstar-aha.md` + `references/05c-validation-spec.md` |

## Resumen de Conteo de Pasos

| Escenario | Pasos |
|-----------|-------|
| Por defecto (solo Core) | **6** |
| Todos los Optional disparados | 8 |
| (Flujo legacy de 12 pasos) | 12 |

## Formato del Output Final

**Resumen de Spec de Producto de Revisión**: comparación antes/después + qué cambia / qué no cambia + métricas de éxito.

El resumen DEBE divulgar cualquier paso Optional omitido y ofrecer una ruta de un solo comando para añadirlos de vuelta (según `rules-optional-trigger.md` Sección 6).

Al completar, sigue `references/rules-end-of-flow.md` para ejecutar las reglas de fin de flujo.