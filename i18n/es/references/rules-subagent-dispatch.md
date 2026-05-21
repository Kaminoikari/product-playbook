# 🤝 Reglas de Delegación a Sub-Agentes

> Se carga al entrar en S2 de cualquier modo (primer paso en el que podría aplicar el dispatch a un especialista). Los tres especialistas operan en ventanas de contexto aisladas — delega en el paso adecuado en lugar de manejar todo inline.

## Cuándo delegar en `discovery-specialist`

Triggers:
- **Full Mode**: S2 (Persona) → S3 (JTBD) → S4 (OST) → S5 (Journey Map) → S6 (hipótesis de Continuous Discovery)
- **Revision Mode**: S2 (análisis del usuario actual) → S3 (síntesis de puntos de dolor) → S4 (identificación de oportunidades)
- **Build Mode**: S2 (clarificación del problema con la lente JTBD)
- **Custom Mode**: cualquier paso que seleccione Persona / JTBD / OST / Journey Map / Continuous Discovery

Cómo invocar:

> Usa el subagente `discovery-specialist` para producir [Persona | JTBD | OST | Journey Map] para [descripción del producto]. Público objetivo: [B2C / B2B / B2B2C]. Datos de investigación disponibles: [lista de archivos subidos, o "ninguno — marcar como low confidence"]. Responde en [idioma].

Integra el YAML devuelto en el resultado del paso. Muestra `open_questions` como parte del mensaje de confirmación del paso.

---

## Cuándo delegar en `strategy-critic`

Trigger **inmediatamente después** de que el usuario finalice cualquier artefacto de estrategia:
- Tras Strategy Blocks (Full Mode S7)
- Tras Rumelt Good Strategy Kernel (Full Mode S8)
- Tras DHM Model (Full Mode S9)
- Tras el charter de Empowered Teams (cualquier modo)
- Cada vez que el usuario escriba "esta es nuestra estrategia" en prosa sin nombrar un framework

Cómo invocar:

> Usa el subagente `strategy-critic` para criticar el siguiente artefacto de estrategia: [pegar textualmente]. El artefacto es [nombre del framework o "generic strategy doc"]. Responde en [idioma].

El crítico devuelve críticas, no reescrituras. Presenta al usuario `three_questions_to_ask_the_writer` textualmente — no las suavices. Si el usuario revisa, vuelve a invocar al crítico sobre la versión revisada.

---

## Cuándo delegar en `pre-mortem-runner`

Triggers:
- **Full Mode**: S10 (tras MVP scoping)
- **Build Mode**: S4 (pre-mortem anclado en arquitectura)
- **Revision Mode**: S8
- **Feature Extension Mode**: S3 (evaluación de riesgos)
- Cada vez que el usuario solicite explícitamente pre-mortem / análisis de riesgos / "qué podría salir mal"

Cómo invocar:

> Usa el subagente `pre-mortem-runner` para hacer un pre-mortem del siguiente [producto | feature | estrategia]: [pegar textualmente]. Mode: [build_mode_architecture_grounded | standard | feature_extension]. Si es build mode, contexto de arquitectura disponible: [pegar el contenido o resumen de los archivos relevantes]. Responde en [idioma].

El runner devuelve más de 15 escenarios. En el output de cara al usuario, encabeza con `priority_three` y `pre_launch_experiments`. Muestra la lista completa de escenarios en una sección plegable o archivo adjunto.

---

## Higiene de delegación

1. **Un sub-agente por paso**. No encadenes sub-agentes en un solo turno — deja que el usuario confirme el output intermedio primero.
2. **Pasa el idioma explícitamente**. Los sub-agentes detectan el idioma desde tu prompt; especifica siempre el idioma de trabajo del usuario.
3. **Respeta `status: out_of_scope`**. El rechazo de alcance del sub-agente es una característica, no un fallo — sigue su recomendación de enrutamiento.
4. **Herencia del Hard Gate**. Los sub-agentes heredan la regla de no escribir código. Se negarán a escribir archivos aunque se lo pidas.
5. **La autoverificación de calidad sigue aplicando**. Tras integrar el output del sub-agente, ejecuta la autoverificación de calidad de `rules-quality-review.md` (o usa la checklist de 6 ítems inline en el archivo de reglas de tu modo).
