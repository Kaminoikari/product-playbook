# 📦 Contexto de Producto — Plantillas y Scripts UX Detallados

> Referencia lazy-loaded. Activada según la tabla de triggers en `rules-context.md` §8. Contiene solo los formatos verbosos YAML/markdown y scripts UX que no se necesitan para el arranque rutinario de sesión.

## File Format

```markdown
# Contexto de Producto
<!-- Mantenido automáticamente por product-playbook. No eliminar. -->
<!-- last-updated: [timestamp ISO] -->

## Identidad
- **Nombre del producto**: [nombre]
- **Tipo de producto**: [B2C / B2B / B2B2C / Herramienta interna]
- **Descripción en una línea**: [Descripción de una oración]
- **Audiencia objetivo**: [Resumen del Persona principal]

## Estrategia Central
- **JTBD Central**: [Cliente Objetivo] + quiere [Job] + en [Contexto]
  - Funcional: [...]
  - Emocional: [...]
  - Social: [...]
- **Posicionamiento (April Dunford)**:
  - Alternativas competitivas reales: [...]
  - Atributos únicos: [...]
  - Valor central: [...]
  - Mercado objetivo: [...]
  - Categoría de mercado: [...]
- **North Star Metric**: [Nombre de la métrica + definición]
- **Aha Moment**: [Descripción]

## Arquitectura y Stack Tecnológico
- **Stack tecnológico**: [Lenguajes, frameworks, infraestructura]
- **Módulos clave**: [Lista de módulos clave]
- **Puntos destacados del modelo de datos**: [Entidades de datos centrales, si se conocen]

## Historial de Decisiones
<!-- Solo agregar. Agregar una entrada cada vez que se completa un flujo. -->

### [fecha ISO] - [Tipo de flujo: Full/Quick/Revision/Feature Extension/Custom/Build]
- **Alcance**: [Alcance de planificación/cambio]
- **Decisiones clave**: [Decisiones principales]
- **Riesgos identificados**: [Riesgos]
- **Límites del MVP**: [Qué hacer / Qué no hacer]
- **Métricas de éxito**: [Métricas de éxito + valores objetivo]

## Preferencia de Idioma
- **Idioma instalado**: [auto-detectado desde archivo .lang o idioma del usuario]
- **Idioma preferido del usuario**: [el idioma en que el usuario se comunica]

## Insights Acumulados
- **Puntos de dolor conocidos**: [Lista de puntos de dolor, con fuentes]
- **Temas de feedback de usuarios**: [Temas de feedback a través de sesiones]
- **Estado de PMF**: [Nivel de evaluación más reciente + fecha]
- **Postura de seguridad**: [Métodos de autenticación/autorización, vulnerabilidades conocidas]
- **Deuda técnica**: [Deuda técnica acumulada a través de sesiones]
```

---

## Bootstrap (Solo Escenario 2)

Cuando el usuario entra en **Extensión de Feature** o **Modo Revisión** sin `.product-context.md`, insertar "Paso 0" antes del S1.

**Presentación:**
```
📦 Esta es tu primera vez usando la herramienta de planificación de producto en este proyecto. Para hacer el flujo subsiguiente más eficiente,
recopilaré información básica del producto primero (unos 2-3 minutos). Se guardará automáticamente para uso futuro.
```

### Recopilación Progresiva (no hacer todas las preguntas a la vez)

**Ronda 1 (requerida para todos los modos):**
- ¿Cómo se llama el producto?
- Describe lo que hace en una oración.
- ¿Tipo de producto? (B2C / B2B / B2B2C / Herramienta interna)

**Ronda 2 (requerida para Extensión de Feature, opcional para Revisión):**
- ¿Qué stack tecnológico usas? (Lenguajes, frameworks, bases de datos, infraestructura)
- ¿Cuáles son los módulos o servicios clave?

**Ronda 3 (requerida para Revisión, opcional para Extensión de Feature):**
- ¿Tienes datos de DAU/MAU o tasa de retención?
- ¿Cuál es el feedback o queja más común de los usuarios?
- ¿Hay problemas de seguridad o deuda técnica conocidos?

### Auto-Detección de Stack Tecnológico

Bootstrap puede leer archivos del proyecto (solo lectura, no viola el Hard Gate):

| Archivo | Contenido de Detección |
|---------|----------------------|
| `package.json` | Ecosistema Node.js, frameworks, dependencias |
| `Cargo.toml` | Rust |
| `go.mod` | Go |
| `requirements.txt` / `pyproject.toml` | Python |
| `Dockerfile` / `docker-compose.yml` | Arquitectura containerizada |
| Estructura raíz del proyecto (`src/`, `app/`, `lib/`, etc.) | Inferencia de módulos |

Estilo de confirmación:
```
Detecté que tu proyecto usa:
- Stack tecnológico: Next.js 14 + TypeScript + PostgreSQL + Redis
- Módulos clave: auth/, billing/, dashboard/, api/
¿Es correcto? ¿Algo que agregar o corregir?
```

Solo escribir después de que el usuario confirme.

### Secuencia Bootstrap → S1 (Hard Gate — Bootstrap NO bloquea el flujo)

- **Por defecto**: Bootstrap y S1 DEBEN ejecutarse en el **mismo turno** como S0 → S1. La pausa está fijada **después de completar S1**, no entre S0 y S1.
- **Si el mensaje del usuario ya proporciona los campos requeridos** → confirmar en una tabla, proceder a S1.
- **Si faltan campos** → presentar tabla "conocido / pendiente" en el mismo turno, entrar a S1 con placeholders, agrupar los pendientes en la pregunta de confirmación de S1.
- **Prohibido**: pausar entre S0 y S1 esperando respuestas de Round 1. Si S1 aparece como `⬜ pending` mientras esperas input del usuario, has fallado esta regla.

Tras Bootstrap: escribir a `.product-context.md` (incluso con placeholders), luego entrar a S1 en el mismo turno.

---

## Partial Context UX (Escenario 3)

```
📦 Tengo registros de tus [N] sesiones de planificación anteriores:
- Stack tecnológico: [Stack conocido fusionado del Historial de Decisiones]
- Módulos previamente modificados: [Módulos afectados fusionados del Historial de Decisiones]
- La estrategia central del producto aún no ha sido registrada.

¿Te gustaría:
  1️⃣ Iniciar directamente (usar información conocida, omitir sección de estrategia)
  2️⃣ Llenar información de estrategia primero (JTBD, Posicionamiento, North Star Metric)
  3️⃣ Esta información es incorrecta — déjame corregirla
```

**Intento de auto-reconstrucción**: Escanear el Historial de Decisiones, extraer nombres de productos recurrentes, stacks tecnológicos y nombres de módulos de `Módulos afectados`, `Alcance` y `Decisiones clave`. Auto-llenar en `Arquitectura y Stack Tecnológico`. Marcar con `<!-- inferido del historial de decisiones -->`.

---

## Append Templates

**Plantilla general:**
```markdown
### [fecha ISO] - [Tipo de flujo]
- **Alcance**: [...]
- **Decisiones clave**: [...]
- **Riesgos identificados**: [...]
- **Límites del MVP**: [...]
- **Métricas de éxito**: [...]
```

**Variante de Extensión de Feature:**
```markdown
### [fecha ISO] - Extensión de Feature: [Nombre del feature]
- **Problema**: [Declaración del problema en una oración]
- **Solución elegida**: [Solución seleccionada + justificación]
- **Módulos afectados**: [Módulos afectados]
- **Alcance**: [Qué hacer / Qué no tocar]
- **Criterios de aceptación**: [Criterios de aceptación]
```

---

## Conflict UX (codebase vs contexto)

```
⚠️ Inconsistencia detectada:
- El contexto registra: [valor del contexto]
- Codebase del proyecto: [valor detectado del código]
¿Cuál es correcto?
  1️⃣ Usar codebase como fuente de verdad (actualizar contexto)
  2️⃣ Usar contexto como fuente de verdad (puede estar en medio de una migración)
  3️⃣ Ambos están incompletos — déjame explicar
```

- No auto-sobrescribir — dejar que el usuario decida
- Si migración: anotar la Arquitectura como `[Migrando] React → Vue 3`
- Registrar el conflicto en el Historial de Decisiones
