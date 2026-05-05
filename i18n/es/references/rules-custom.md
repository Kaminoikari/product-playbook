# ✏️ Secuencia de Pasos del Modo Personalizado

> Definición autoritativa de pasos para el Modo Personalizado. Despachado desde SKILL.md.

Elige un nivel de completitud (o selecciona pasos manualmente):

## 🔴 Bajo (Lean) — 4 pasos

```
S1. Declaración JTBD → references/02b-jtbd.md
S2. Un HMW → references/03-define.md
S3. PR-FAQ → references/04a-prfaq.md
S4. North Star → references/05a-northstar-aha.md
(Cualquier paso puede ser intercambiado por el usuario por un framework diferente.)
────
Output Final → Resumen de Spec de Producto (campos no ejecutados marcados "no ejecutado")
```

## 🟡 Medio (Standard) — 8 pasos (se expande a 9 cuando se necesita Journey Map)

> Un subconjunto de 8 pasos del Full Mode: los Core del Full menos Diagnóstico Estratégico, más Posicionamiento. Los usuarios de Standard suelen necesitar el posicionamiento de mercado antes que un diagnóstico estratégico profundo, de ahí el intercambio.
>
> **Inserción Condicional Persona-Journey**: Tras completar S1 (Persona), la IA ejecuta la evaluación Persona-Journey según `rules-optional-trigger.md` Sección 2. Si NO se cumplen las condiciones de salto (es decir, el Job abarca múltiples etapas), la IA **inserta proactivamente el Journey Map como S1.5**, convirtiéndolo en una ejecución de 9 pasos. El usuario puede responder `-journey` para revertir a 8 pasos. Si se cumplen las condiciones de salto (punto de interacción único / flujo ≤2 pasos), se salta en silencio y se divulga en el output final.

```
S1.   Persona (Tabla + Tarjetas) → references/02a-persona.md
S1.5  User Journey Map [Insertado por defecto; saltar solo cuando la situación es demasiado simple]
      → references/02c-ost-journey.md
S2.   Análisis JTBD → references/02b-jtbd.md
S3.   Puntos de Dolor + HMW + Ranking de Oportunidades → references/03-define.md
S4.   Posicionamiento April Dunford → references/03-define.md
S5.   PR-FAQ → references/04a-prfaq.md
S6.   Evaluación de Soluciones (Paralelo + Pre-mortem + GEM + RICE) → references/04b-solutions.md
S7.   MVP + Lista de No Hacer → references/04c-mvp.md
S8.   North Star + Señales de Tres Capas + Aha Moment → references/05a-northstar-aha.md
```

## 🟢 Alto (Comprehensive) — 11 pasos

> Core del Full Mode + todos los Optional Por defecto OFF disparados (Posicionamiento + PMF/GTM/BM/Validación). **S2 Persona va inmediatamente seguido de S3 User Journey Map** según la regla de emparejamiento Persona-Journey. S3 puede saltarse si la situación es genuinamente simple — responde `-S3` después de Persona para revertir a 10 pasos.

```
S1.  Diagnóstico Estratégico → references/00-opportunity-check.md + references/01-strategy.md
S2.  Persona (Tabla + Tarjetas) → references/02a-persona.md
S3.  User Journey Map → references/02c-ost-journey.md   ← emparejado con S2 (por defecto ON)
S4.  Análisis JTBD → references/02b-jtbd.md
S5.  Puntos de Dolor + HMW + Ranking de Oportunidades → references/03-define.md
S6.  Posicionamiento April Dunford → references/03-define.md
S7.  PR-FAQ → references/04a-prfaq.md
S8.  Evaluación de Soluciones (Paralelo + Pre-mortem + GEM + RICE) → references/04b-solutions.md
S9.  MVP + Lista de No Hacer → references/04c-mvp.md
S10. North Star + Señales de Tres Capas + Aha Moment → references/05a-northstar-aha.md
S11. PMF + GTM + BM + Plan de Validación de Hipótesis → references/05b-pmf-gtm.md + references/05c-validation-spec.md
```

## Regla de Carga de Referencias

Carga cada archivo de referencia SOLO al entrar en su paso correspondiente (no pre-cargar todas las referencias). Cada paso arriba tiene su ruta de referencia anotada.

## Emparejamiento Persona-Journey

Según `references/rules-optional-trigger.md` Secciones 2 y 6, siempre que un preset Custom incluya un paso de Persona, el Journey Map está **por defecto ON**:

- **Comprehensive**: el Journey Map está cableado como S3 (ya está en la secuencia de arriba). El usuario puede responder `-S3` después de Persona para saltarlo.
- **Standard**: el Journey Map se inserta automáticamente como **S1.5** cuando no se cumplen las condiciones de salto (Job multi-etapa). Cuando la situación es demasiado simple (punto de interacción único, flujo ≤2 pasos, el usuario solicita saltarlo), el Journey Map se salta en silencio y se divulga en el output final.
- **Lean**: no tiene paso de Persona, por lo que esta regla no aplica.

Condiciones de salto (basta con una → saltar Journey):
1. Punto de interacción único (API, botón único, servicio backend, herramienta de configuración)
2. El flujo tiene solo 1–2 pasos
3. El usuario solicita explícitamente saltarlo

## Formato del Output Final

**Resumen de Spec de Producto** (solo integra los pasos completados; los campos no ejecutados se marcan como "no ejecutado").

Al completar, sigue `references/rules-end-of-flow.md` para ejecutar las reglas de fin de flujo.
