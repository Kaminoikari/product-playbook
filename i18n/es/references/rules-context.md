# 📦 Reglas de Acumulación de Contexto de Producto

> Este archivo define el formato, reglas de lectura/escritura, manejo de escenarios y resolución de conflictos para `.product-context.md`.
> Cargado por el flujo de inicio de SKILL.md o por el pre-paso S1 de cada modo.

## 1. Ubicación del Archivo y Ciclo de Vida

- **Ruta**: `.product-context.md` en el directorio raíz del proyecto (mismo nivel que `.product-playbook-progress.md`)
- **Retenido permanentemente**: Este archivo **no se elimina** cuando el flujo termina — persiste y acumula a través de sesiones
- **En la primera creación**, recordar al usuario: "⚠️ Recomendamos agregar `.product-context.md` a `.gitignore` — este archivo puede contener información sensible de estrategia de producto."

---

## 2. Formato del Archivo

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

## 3. Detección de Tres Escenarios

Al inicio (después de verificación de archivo de progreso, antes de selección de modo), detectar el estado de `.product-context.md`:

| Condición | Escenario | Acción |
|-----------|----------|--------|
| El archivo existe, la sección `Estrategia Central` tiene contenido real (no vacío / no placeholder) | **Escenario 1: Contexto completo** | Cargar silenciosamente. Mostrar: "📦 Contexto de producto detectado para **[nombre del producto]** — servirá como línea base para esta sesión de planificación." |
| El archivo no existe | **Escenario 2: Sin contexto** | Registrar este estado. Activar Context Bootstrap al entrar en modo Extensión de Feature o Revisión (ver Sección 4) |
| El archivo existe, `Estrategia Central` está vacío o contiene solo placeholders, pero `Historial de Decisiones` tiene al menos una entrada | **Escenario 3: Contexto parcial** | Mostrar un resumen de información conocida y ofrecer opciones de complemento (ver Sección 5) |

**Lógica de detección**:
1. ¿Existe el archivo?
2. ¿La sección `Identidad` tiene un nombre de producto (no es placeholder)?
3. ¿La sección `Estrategia Central` tiene un JTBD Central (no es placeholder)? → Sí = Escenario 1
4. ¿La sección `Historial de Decisiones` tiene alguna entrada `###`? → Sí pero 3 es No = Escenario 3

---

## 4. Context Bootstrap (Solo Escenario 2)

Cuando el usuario entra en **Extensión de Feature** o **Modo Revisión** pero no hay `.product-context.md`, insertar "Paso 0" antes del S1 del modo.

**Presentación**:
```
📦 Esta es tu primera vez usando la herramienta de planificación de producto en este proyecto. Para hacer el flujo subsiguiente más eficiente,
recopilaré información básica del producto primero (unos 2-3 minutos). Se guardará automáticamente para uso futuro.
```

### Recopilación Progresiva (no hacer todas las preguntas a la vez)

**Ronda 1 (requerida para todos los modos)**:
- ¿Cómo se llama el producto?
- Describe lo que hace en una oración.
- ¿Tipo de producto? (B2C / B2B / B2B2C / Herramienta interna)

**Ronda 2 (requerida para Extensión de Feature, opcional para Revisión)**:
- ¿Qué stack tecnológico usas? (Lenguajes, frameworks, bases de datos, infraestructura)
- ¿Cuáles son los módulos o servicios clave?

**Ronda 3 (requerida para Revisión, opcional para Extensión de Feature)**:
- ¿Tienes datos de DAU/MAU o tasa de retención?
- ¿Cuál es el feedback o queja más común de los usuarios?
- ¿Hay problemas de seguridad o deuda técnica conocidos?

### Auto-Detección de Stack Tecnológico

Además del input verbal del usuario, Bootstrap puede **leer archivos del proyecto** para asistir la detección (solo lectura — no viola el Hard Gate):

| Archivo | Contenido de Detección |
|---------|----------------------|
| `package.json` | Ecosistema Node.js, frameworks, dependencias |
| `Cargo.toml` | Rust |
| `go.mod` | Go |
| `requirements.txt` / `pyproject.toml` | Python |
| `Dockerfile` / `docker-compose.yml` | Arquitectura containerizada |
| Estructura de directorios raíz del proyecto (`src/`, `app/`, `lib/`, etc.) | Inferencia de módulos |

Después de la detección, presentar en **estilo confirmación**:
```
Detecté que tu proyecto usa:
- Stack tecnológico: Next.js 14 + TypeScript + PostgreSQL + Redis
- Módulos clave: auth/, billing/, dashboard/, api/
¿Es correcto? ¿Algo que agregar o corregir?
```

Solo escribir a `.product-context.md` después de que el usuario confirme.

### Después de Completar Bootstrap

Escribir la información recopilada a `.product-context.md`, dejar secciones no recopiladas vacías (usando placeholders), luego proceder al S1 formal del modo.

---

## 5. Manejo de Contexto Parcial (Escenario 3)

Cuando `.product-context.md` existe pero la Estrategia Central está vacía, con solo entradas en el Historial de Decisiones:

**Presentación**:
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

**Intento de auto-reconstrucción**: Escanear todas las entradas del Historial de Decisiones, extraer nombres de productos recurrentes, stacks tecnológicos y nombres de módulos de `Módulos afectados`, `Alcance` y `Decisiones clave`, y auto-llenar en `Arquitectura y Stack Tecnológico`. Marcar con `<!-- inferido del historial de decisiones -->` para indicar la fuente inferida.

---

## 6. Reglas de Auto-Lectura de Contexto

Al cargar contexto en el pre-paso S1 de cada modo, **solo inyectar secciones relevantes** — no mostrar el contenido completo del archivo al usuario:

| Modo + Paso | Secciones de Contexto Inyectadas |
|-------------|--------------------------------|
| Extensión de Feature S1 | Identidad, Arquitectura y Stack Tecnológico, 3 entradas más recientes del Historial de Decisiones |
| Revisión S1 | Identidad, Estrategia Central, Insights Acumulados (puntos de dolor, PMF, seguridad), 3 entradas más recientes del Historial de Decisiones |
| Full/Quick/Build S1 | Solo Identidad (nombre del producto, tipo, descripción en una línea) |
| Pre-mortem en cualquier modo | Postura de seguridad + Deuda técnica (de Insights Acumulados) |

**Control de volumen**: El Historial de Decisiones por defecto solo inyecta las 3 entradas más recientes. El usuario puede solicitar más.

---

## 7. Reglas de Omisión de Secciones Vacías

Cuando el archivo de contexto existe pero algunas secciones están vacías, determinar si omitir o recopilar basándose en el **modo**:

| Sección | Extensión de Feature | Modo Revisión | Full/Quick/Build |
|---------|---------------------|--------------|-----------------|
| Identidad | Requerida (Bootstrap si falta) | Requerida (Bootstrap si falta) | El flujo mismo producirá esto — no se necesita pre-carga |
| Estrategia Central | **Puede omitirse** | Requerida (recopilación rápida Q&A dentro de S1 si falta) | El flujo mismo producirá esto |
| Arquitectura y Stack Tecnológico | Requerida (Bootstrap o auto-detección si falta) | Puede omitirse | El flujo mismo producirá esto |
| Historial de Decisiones | Puede omitirse | Incluir si disponible, omitir si no | El flujo mismo producirá esto |
| Insights Acumulados | Puede omitirse | Incluir si disponible, omitir si no | El flujo mismo producirá esto |

| Extensión de Funcionalidad | Identity (solo confirmar), Architecture & Tech Stack (requerido), Core Strategy (se permite omitir) |

**Principio**: Las secciones vacías **no bloquean el flujo**. Solo las secciones que son "requeridas" para el modo actual y están vacías activarán la recopilación.

---

## 8. Reglas de Auto-Escritura de Contexto (Extracción al Final del Flujo)

Al final de un flujo (en sincronía con la verificación de condición final en `rules-end-of-flow.md`), extraer contexto automáticamente:

| Tipo de Flujo | Secciones Escritas/Actualizadas |
|---------------|-------------------------------|
| Quick | Identidad, Estrategia Central (JTBD + North Star), agregar al Historial de Decisiones |
| Full | **Todas las secciones** (sobrescribir Identidad/Estrategia/Insights, agregar al Historial) |
| Revision | Actualizar Estrategia Central (si se reposicionó), actualizar Insights, agregar al Historial |
| Feature Extension | Fusionar Arquitectura, agregar al Historial de Decisiones (plantilla específica de feature) |
| Custom | Actualizar secciones correspondientes a pasos completados |
| Build (7 pasos) | Identidad, Estrategia Central (parcial), agregar al Historial |

### Estrategia de Escritura

| Sección | Estrategia | Notas |
|---------|-----------|-------|
| Identidad | **Sobrescribir con lo más reciente** | Siempre sobrescribir con los datos del flujo más reciente |
| Estrategia Central | **Sobrescribir con lo más reciente** | Igual que arriba. La estrategia post-revisión reemplaza la estrategia pre-revisión |
| Arquitectura y Stack Tecnológico | **Fusionar** | Nuevos módulos se agregan sin eliminar los antiguos. Nuevos ítems tecnológicos se agregan al final |
| Historial de Decisiones | **Solo agregar** | Nunca eliminar entradas anteriores. Agregar una entrada cada vez que se completa un flujo |
| Insights Acumulados | **Fusionar y deduplicar** | Puntos de dolor y temas de feedback se deduplicán y agregan. PMF y Seguridad se sobrescriben con los valores más recientes |

### Plantilla de Entrada al Historial de Decisiones

**Plantilla general**:
```markdown
### [fecha ISO] - [Tipo de flujo]
- **Alcance**: [...]
- **Decisiones clave**: [...]
- **Riesgos identificados**: [...]
- **Límites del MVP**: [...]
- **Métricas de éxito**: [...]
```

**Plantilla de Extensión de Feature**:
```markdown
### [fecha ISO] - Extensión de Feature: [Nombre del feature]
- **Problema**: [Declaración del problema en una oración]
- **Solución elegida**: [Solución seleccionada + justificación]
- **Módulos afectados**: [Módulos afectados]
- **Alcance**: [Qué hacer / Qué no tocar]
- **Criterios de aceptación**: [Criterios de aceptación]
```

### Notificación de Finalización

```
✅ El contexto de producto ha sido actualizado en `.product-context.md` — se cargará automáticamente en tu próxima sesión de planificación.
```

---

## 9. Resolución de Conflictos

### El usuario corrige contexto existente

Completamente permitido. Las correcciones proporcionadas por el usuario sobrescriben directamente la sección correspondiente (lo más reciente gana).

### Datos del usuario entran en conflicto con el codebase

Cuando el pre-paso S1 lee tanto `.product-context.md` como archivos del proyecto (p.ej., `package.json`) y encuentra inconsistencias:

```
⚠️ Inconsistencia detectada:
- El contexto registra: [valor del contexto]
- Codebase del proyecto: [valor detectado del código]
¿Cuál es correcto?
  1️⃣ Usar codebase como fuente de verdad (actualizar contexto)
  2️⃣ Usar contexto como fuente de verdad (puede estar en medio de una migración)
  3️⃣ Ambos están incompletos — déjame explicar
```

**Principios de manejo**:
- **No auto-sobrescribir** — dejar que el usuario decida
- Actualizar `.product-context.md` después de que el usuario elija
- Si se selecciona "en medio de una migración," anotar en la sección de Arquitectura: `[Migrando] React → Vue 3`
- Registrar el conflicto en el Historial de Decisiones

### Nuevos datos del flujo sobrescriben contexto

Si los datos producidos durante un flujo difieren de datos antiguos en el contexto (p.ej., Modo Revisión redefine el JTBD), **los datos del flujo tienen prioridad**. Se sobrescribe automáticamente al final del flujo.

---

## 10. Preferencia de Idioma

Cuando `.product-context.md` se crea o actualiza, registrar la preferencia de idioma en la sección `Preferencia de Idioma`:

- **Idioma instalado**: Detectado desde el archivo `.lang` en el directorio de instalación del skill, o desde la configuración regional del usuario.
- **Idioma preferido del usuario**: El idioma en que el usuario se comunica durante la sesión.

**Regla de carga**: Al cargar un `.product-context.md` existente, si hay una preferencia de idioma registrada, continuar la sesión en ese idioma.

**Momento de escritura**: La preferencia de idioma se escribe durante el Context Bootstrap (Sección 4) o al final del primer flujo que crea el archivo de contexto. Se actualiza cuando el usuario cambia explícitamente de idioma durante la sesión.
