# 📦 Secuencia de Pasos del Modo Completo (8 Core + 1 Por defecto ON + 2 Optional, total 9–11 pasos)

> Definición autoritativa de pasos para el Modo Completo. Despachado desde SKILL.md.

**Reducido desde el flujo original de 20 pasos (v1.0.x) fusionando frameworks redundantes y condicionando los opcionales a disparadores.** Consulta `references/rules-optional-trigger.md` para la lógica de disparo y el formato del Punto de Decisión de Fase.

**Nota sobre el Journey Map (S3)**: Por defecto ON. Persona-Journey es un par emparejado independientemente de si el producto es 0-a-1 o un producto existente — la variable relevante es si el Job del usuario abarca múltiples etapas. Saltar solo cuando la situación es genuinamente demasiado simple (API/botón único, flujo ≤2 pasos, o el usuario solicita explícitamente saltarlo).

## Secuencia de Pasos

```
Fase 0: Estrategia
  S1.  Diagnóstico Estratégico  [Core]
       → references/00-opportunity-check.md + references/01-strategy.md
       (Fusionado: Oportunidad + DHM + Strategy Blocks + Kernel de Rumelt)

Fase 1: Descubrimiento
  S2.  Persona (Tabla + Tarjetas)  [Core]
       → references/02a-persona.md
  S3.  User Journey Map  [Por defecto ON — saltar solo si la situación es demasiado simple]
       → references/02c-ost-journey.md
  S4.  Análisis JTBD  [Core]
       → references/02b-jtbd.md

Fase 2: Definición
  S5.  Puntos de Dolor + HMW + Ranking de Oportunidades  [Core]
       → references/03-define.md
       (Fusionado: Resumen de Puntos de Dolor + HMW + Tabla de Evaluación de Oportunidades;
        la visualización de árbol OST es un sub-formato opcional dentro de este paso)
  S6.  Posicionamiento April Dunford  [Optional — ver disparadores]
       → references/03-define.md

Fase 3: Desarrollo
  S7.  PR-FAQ (Working Backwards)  [Core]
       → references/04a-prfaq.md
  S8.  Evaluación de Soluciones  [Core]
       → references/04b-solutions.md
       (Fusionado: Prototipos Paralelos + Pre-mortem + GEM + RICE)
  S9.  MVP + Lista de No Hacer  [Core]
       → references/04c-mvp.md

Fase 4: Entrega
  S10. North Star + Señales de Tres Capas + Aha Moment  [Core]
       → references/05a-northstar-aha.md
  S11. PMF + GTM + Modelo de Negocio + Plan de Validación de Hipótesis  [Optional — ver disparadores]
       → references/05b-pmf-gtm.md + references/05c-validation-spec.md

────
Output Final → Resumen de Spec de Producto (references/05c-validation-spec.md → 4.6) + Análisis del Mejor Punto de Entrada
```

> Cuando la audiencia es Ejecutivos o Alineación Cross-funcional, antepón el framework Empowered Teams antes de S10.

## Reglas de Disparo Optional

Lee `references/rules-optional-trigger.md` para las condiciones de disparo autoritativas y el formato de salida del Punto de Decisión de Fase.

**Referencia rápida:**
- **S3 Journey Map** (Por defecto ON): proceder a menos que haya un punto de interacción único / el flujo tenga ≤2 pasos / el usuario solicite saltarlo
- **S6 Posicionamiento** (Por defecto OFF): disparar al lanzar nuevo producto / reposicionamiento / audiencia con Sales-BD-Marketing
- **S11 PMF/GTM/BM/Validación** (Por defecto OFF): disparar al lanzar al mercado / audiencia es Ejecutivos o Científicos de Datos / el usuario solicita un plan de validación

## Requisito del Punto de Decisión de Fase

Antes de entrar en la Fase 1, Fase 2 y Fase 4, renderiza el bloque de Punto de Decisión de Fase (formato definido en `rules-optional-trigger.md`). La Fase 0 y la Fase 3 contienen solo pasos Core y omiten el punto de decisión.

## Instrucciones de Carga de Referencias

Carga cada archivo de referencia SOLO al entrar en su paso correspondiente (no pre-cargar todas las referencias):

| Paso | Archivo de Referencia |
|------|----------------------|
| S1 | `references/00-opportunity-check.md` + `references/01-strategy.md` |
| S2 | `references/02a-persona.md` |
| S3 (si se dispara) | `references/02c-ost-journey.md` |
| S4 | `references/02b-jtbd.md` |
| S5 | `references/03-define.md` |
| S6 (si se dispara) | `references/03-define.md` |
| S7 | `references/04a-prfaq.md` |
| S8 | `references/04b-solutions.md` |
| S9 | `references/04c-mvp.md` |
| S10 | `references/05a-northstar-aha.md` |
| S11 (si se dispara) | `references/05b-pmf-gtm.md` + `references/05c-validation-spec.md` |
| Output Final | `references/05c-validation-spec.md` |

## Resumen de Conteo de Pasos

| Escenario | Pasos |
|-----------|-------|
| Por defecto (8 Core + S3 Journey ON) | **9** |
| Flujo simple (S3 omitido) | 8 |
| 1 Optional Por defecto OFF disparado (S6 o S11) | 10 |
| Todos los Optional disparados | 11 |
| (Flujo legacy de 20 pasos) | 20 |

## Formato del Output Final

**Análisis del Mejor Punto de Entrada** (cadena de razonamiento completa) + **Resumen de Spec de Producto**.

El Resumen de Spec de Producto DEBE divulgar cualquier paso Optional omitido y ofrecer una ruta de un solo comando para añadirlos de vuelta (según `rules-optional-trigger.md` Sección 6).

Al completar, sigue `references/rules-end-of-flow.md` para ejecutar las reglas de fin de flujo.
