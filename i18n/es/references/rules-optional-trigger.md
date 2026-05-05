# 🔵 Reglas de Disparo de Pasos Optional

> Fuente autoritativa para los disparadores de pasos Optional y el formato del Punto de Decisión de Fase. Cargado por los archivos de reglas de los modos Full / Revision / Custom.

Este archivo centraliza las condiciones de disparo de los pasos Optional para que cada archivo de reglas de modo no las duplique.

---

## 1. Definiciones de Core vs Optional

- **Core (Núcleo)**: Siempre se ejecuta. No puede omitirse sin una anulación explícita del usuario.
- **Optional (Opcional)**: Se ejecuta solo cuando se cumple al menos una condición de disparo. El usuario siempre puede forzar su inclusión o su omisión.

---

## 2. Regla de Emparejamiento Persona-Journey (Global)

**El Journey Map es la extensión natural de la Persona: la Persona define Quién y el Journey Map describe el viaje que ese Quién experimenta. Tras completar el paso de Persona, el Journey Map se incluye por DEFECTO (Default ON) y solo se salta cuando la situación es genuinamente demasiado simple para mapearla.**

> ⚠️ Esta regla corrige una suposición errónea anterior según la cual "0-a-1 no necesita Journey Map". Lo cierto es lo contrario — Teresa Torres (Continuous Discovery), Indi Young (Mental Models) y el proceso Working Backwards de Amazon tratan el Journey Map como esencial durante el 0-a-1, porque modela cómo se diseña la nueva experiencia. La variable relevante es **si el Job del usuario abarca múltiples etapas**, no si el producto ya existe.

### Condiciones de salto (por defecto ON; saltar solo si se cumple alguna)

1. **Punto de interacción único** — el Job se resuelve con una sola llamada a una API, un único botón, un servicio puramente backend o una herramienta de configuración pura (no existe un flujo multi-etapa)
2. **El flujo tiene solo 1–2 pasos** — el flujo completo del usuario es tan corto que un Journey Map degenera en una lista sin transiciones de etapa significativas
3. **El usuario solicita explícitamente saltarlo** — p. ej. "saltar Journey Map", "skip Journey Map", "我不需要 Journey Map"

### Comportamiento al saltar

Comunica la decisión al usuario, no la saltes en silencio:

> "Persona está completa. Según el contexto actual ([punto de interacción único / el flujo solo tiene N pasos]), se omite el Journey Map. Puedes añadirlo en cualquier momento respondiendo 'add journey'."

### Comportamiento al disparar (por defecto)

Antes de entrar en el paso de Journey Map, muestra una breve nota de evaluación citando **por qué** es necesario:

> "Persona está completa. El Job abarca [N] etapas ([etapa A → etapa B → ...]) — procediendo con el User Journey Map. Responde '-S3' para saltarlo si no lo necesitas."

---

## 3. Disparadores Optional — Full Mode

| Paso | Framework | Por defecto | Lógica |
|------|-----------|-------------|--------|
| S3 | User Journey Map | **ON** | Ver la regla Persona-Journey arriba (Sección 2). Saltar solo cuando hay un punto de interacción único / el flujo tiene ≤2 pasos / el usuario solicita explícitamente saltarlo |
| S6 | Posicionamiento April Dunford | OFF | Disparar cuando: (a) Lanzamiento de nuevo producto O (b) Reposicionamiento O (c) La audiencia incluye Sales/BD/Marketing |
| S11 | PMF + GTM + Modelo de Negocio + Plan de Validación de Hipótesis | OFF | Disparar cuando: (a) El producto se está lanzando al mercado O (b) La audiencia es Ejecutivos/Científicos de Datos O (c) El usuario solicitó explícitamente un plan de validación |

---

## 4. Disparadores Optional — Revision Mode

| Paso | Framework | Disparador (basta con uno) |
|------|-----------|------------------------------|
| S4 | Re-evaluación de Posicionamiento | El usuario menciona "deriva de posicionamiento" / "el mercado cambió" O la audiencia incluye Sales/Marketing |
| S6 | Pre-mortem | (a) Alcance del cambio ≥30% de la funcionalidad existente O (b) Toca pagos/permisos/migración de datos |

---

## 5. Formato de Salida del Punto de Decisión de Fase

**Antes de entrar en cada Fase que contenga un paso Optional, la IA DEBE imprimir un bloque de Punto de Decisión de Fase que liste qué pasos Core/Optional se ejecutarán y por qué.**

### Formato requerido

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔀 Decisión de Pasos de la Fase [N]

✅ Core (siempre se ejecuta): S[a], S[b]
🔵 Evaluación Optional:
  • S[x] [Nombre del framework] (Por defecto ON):  [PROCEDER / SALTAR] — [razón]
  • S[y] [Nombre del framework] (Por defecto OFF): [DISPARAR / SALTAR] — [razón]

→ Esta fase ejecutará [N] paso(s)
(Responde "+S[x]" para forzar inclusión, "-S[y]" para forzar omisión, o simplemente continúa)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Para un paso Por defecto ON (p. ej. S3 Journey Map), usa **PROCEDER** cuando se mantienen las condiciones y **SALTAR** cuando se dispara una condición de salto.
Para un paso Por defecto OFF (p. ej. S6 Posicionamiento, S11 PMF/GTM), usa **DISPARAR** cuando se cumplen las condiciones y **SALTAR** en caso contrario.

### Cuándo renderizarlo

- Renderiza una vez al inicio de cada Fase que contenga al menos un paso Optional
- Las Fases con solo pasos Core NO requieren un punto de decisión (continuar directamente)
- Después de renderizar, espera la respuesta del usuario. Una respuesta sin anulación (p. ej. "ok", "continuar" o contenido sustantivo) significa "aceptar la decisión de la IA"

### Comandos de anulación del usuario

| Entrada del usuario | Comportamiento |
|---------------------|----------------|
| `+S[x]` o "añadir S[x]" | Forzar la inclusión del paso Optional previamente omitido |
| `-S[y]` o "omitir S[y]" | Forzar la omisión del paso Optional previamente disparado |
| Contenido sustantivo / "continuar" / Enter | Aceptar la evaluación de la IA y continuar |

---

## 6. Modo Custom — Inserción Condicional Persona-Journey

Los presets del Modo Custom (Lean / Standard / Comprehensive) tienen secuencias de pasos fijas, pero la regla de emparejamiento Persona-Journey sigue aplicando a cualquier preset que contenga un paso de Persona.

| Preset | Comportamiento por defecto | Comportamiento tras el paso de Persona |
|--------|---------------------------|----------------------------------------|
| **Lean** | Sin paso de Persona | N/A |
| **Standard** | 8 pasos fijos, S1 = Persona | Tras S1, la IA ejecuta la evaluación Persona-Journey según la Sección 2. Si NO se cumplen las condiciones de salto, la IA inserta proactivamente el Journey Map como **S1.5 (se convierte en una ejecución de 9 pasos)** y el usuario puede responder `-journey` para revertir. Si se cumplen las condiciones de salto, se salta en silencio y se divulga en el output final (Sección 7). |
| **Comprehensive** | 11 pasos fijos, S2 = Persona, S3 = Journey Map (ya incluido) | La IA puede mostrar una breve nota de "salto disponible": "El Journey Map se incluye por defecto. Responde `-S3` si tu situación es demasiado simple para mapearla." En caso contrario, continuar con normalidad. |

Esto evita interrumpir a los usuarios de Lean/Standard cuando la situación es genuinamente simple, al tiempo que asegura que los usuarios que *sí* se beneficiarían del Journey Map no se vean privados de él en silencio.

---

## 7. Divulgación en el Output Final

Cuando el modo termina, el Resumen de Spec de Producto final DEBE listar qué pasos Optional fueron omitidos y ofrecer una ruta de un solo comando para añadirlos de vuelta, p. ej.:

> "Pasos Optional omitidos en esta ejecución: S6 (Posicionamiento), S11 (PMF/GTM). Responde 'añadir S6' o 'añadir S11' para completarlos."
