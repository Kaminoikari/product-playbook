# 📦 Reglas de Acumulación de Contexto de Producto

> Cargado por el arranque de SKILL.md. Contiene toda la lógica de decisión (cuándo / cuál / cómo). Los formatos YAML verbosos y scripts UX completos viven en `rules-context-template.md` (lazy-loaded solo al escribir el archivo o ejecutar Bootstrap).

## 1. Ciclo de Vida del Archivo

- **Ruta**: `.product-context.md` en la raíz del proyecto (mismo nivel que `.product-playbook-progress.md`)
- **Retenido permanentemente**: persiste a través de sesiones
- **En la primera creación**: recordar al usuario agregar a `.gitignore` (puede contener información sensible de estrategia)

---

## 2. Detección de Tres Escenarios (al inicio)

Después de la verificación del archivo de progreso, antes de la selección de modo:

| Condición | Escenario | Acción |
|-----------|----------|--------|
| El archivo existe, `Estrategia Central` tiene contenido real | **1. Completo** | Cargar silenciosamente. Mostrar: "📦 Contexto de producto detectado para **[nombre del producto]** — línea base para esta sesión." |
| El archivo no existe | **2. Sin contexto** | Registrar estado. Activar Bootstrap al entrar en Feature/Revisión. → Cargar template §Bootstrap |
| El archivo existe, Estrategia Central vacía/placeholder, Historial de Decisiones tiene ≥1 entrada | **3. Parcial** | Mostrar resumen de info conocida + opciones de complemento. → Cargar template §Partial |

**Lógica de detección:**
1. ¿Existe el archivo?
2. ¿`Identidad` tiene nombre del producto (no placeholder)?
3. ¿`Estrategia Central` tiene JTBD Central (no placeholder)? → Sí = Escenario 1
4. ¿`Historial de Decisiones` tiene alguna entrada `###`? → Sí pero 3 es No = Escenario 3

---

## 3. Reglas de Auto-Lectura (en el pre-paso S1 de cada modo)

**Solo inyectar secciones relevantes** — no mostrar el archivo completo al usuario:

| Modo + Paso | Secciones Inyectadas |
|-------------|---------------------|
| Extensión de Feature S1 | Identidad, Arquitectura y Stack Tecnológico, 3 entradas más recientes del Historial de Decisiones |
| Revisión S1 | Identidad, Estrategia Central, Insights Acumulados (puntos de dolor, PMF, seguridad), 3 entradas más recientes del Historial de Decisiones |
| Full/Quick/Build S1 | Solo Identidad (nombre del producto, tipo, descripción en una línea) |
| Pre-mortem en cualquier modo | Postura de seguridad + Deuda técnica (de Insights Acumulados) |

**Control de volumen**: Historial de Decisiones por defecto las 3 entradas más recientes. El usuario puede solicitar más.

---

## 4. Reglas de Omisión de Secciones Vacías

| Sección | Extensión de Feature | Revisión | Full/Quick/Build |
|---------|---------------------|----------|-----------------|
| Identidad | Requerida (Bootstrap si falta) | Requerida (Bootstrap si falta) | El flujo la produce |
| Estrategia Central | Puede omitirse | Requerida (Q&A rápida en S1 si falta) | El flujo la produce |
| Arquitectura y Stack Tecnológico | Requerida (Bootstrap o auto-detección) | Puede omitirse | El flujo la produce |
| Historial de Decisiones | Puede omitirse | Incluir si disponible, omitir si no | El flujo lo produce |
| Insights Acumulados | Puede omitirse | Incluir si disponible, omitir si no | El flujo los produce |

**Principio**: Las secciones vacías no bloquean el flujo. Solo "requerida" + vacía activa recopilación.

---

## 5. Reglas de Auto-Escritura (al final del flujo)

Sincronizar con la condición final de `rules-end-of-flow.md`. Auto-extraer contexto:

| Tipo de Flujo | Secciones Escritas/Actualizadas |
|---------------|-------------------------------|
| Quick | Identidad, Estrategia Central (JTBD + North Star), agregar al Historial |
| Full | Todas las secciones (sobrescribir Identidad/Estrategia/Insights, agregar al Historial) |
| Revision | Actualizar Estrategia Central (si se reposicionó), actualizar Insights, agregar al Historial |
| Feature Extension | Fusionar Arquitectura, agregar al Historial (plantilla de feature) |
| Custom | Actualizar secciones correspondientes a pasos completados |
| Build | Identidad, Estrategia Central (parcial), agregar al Historial |

### Estrategia de escritura por sección

| Sección | Estrategia |
|---------|-----------|
| Identidad | Sobrescribir con lo más reciente |
| Estrategia Central | Sobrescribir con lo más reciente (post-revisión reemplaza pre-revisión) |
| Arquitectura y Stack Tecnológico | Fusionar (nuevos módulos añadidos, antiguos preservados) |
| Historial de Decisiones | Solo agregar (nunca eliminar entradas anteriores) |
| Insights Acumulados | Fusionar y deduplicar (puntos de dolor/feedback se deduplicán; PMF/Seguridad se sobrescriben) |

Al escribir por primera vez (creando el archivo) o al añadir al Historial de Decisiones → **cargar `rules-context-template.md` §File Format / §Append Templates**.

Notificación al completar: `✅ El contexto de producto ha sido actualizado en '.product-context.md' — se cargará automáticamente en tu próxima sesión.`

---

## 6. Resolución de Conflictos (resumen)

| Tipo de conflicto | Resolución |
|------------------|-----------|
| El usuario corrige contexto existente | Lo más reciente gana — sobrescribir directo |
| Contexto vs codebase (p.ej., package.json difiere) | No auto-sobrescribir — preguntar al usuario. → Cargar template §Conflict UX |
| Datos del flujo vs contexto antiguo | Datos del flujo ganan — auto-sobrescribir al final del flujo |

---

## 7. Preferencia de Idioma (resumen)

Registrar en la sección `Preferencia de Idioma` cuando el contexto se crea/actualiza:
- **Idioma instalado**: desde archivo `.lang` o configuración regional del usuario
- **Idioma preferido del usuario**: idioma en que el usuario se comunica

Al cargar: si está registrado, continuar la sesión en ese idioma.
Al escribir: durante Bootstrap o al final del primer flujo que crea el archivo. Se actualiza cuando el usuario cambia de idioma a mitad de sesión.

---

## 8. Cuándo cargar `rules-context-template.md`

Solo cuando UNO de estos triggers se active:

| Trigger | Sección del template |
|---------|---------------------|
| Escenario 2 + entrando en Feature Extension / Revision | §Bootstrap, §File Format |
| Escenario 3 (Contexto parcial) | §Partial Context, §File Format |
| Escribiendo contexto por primera vez | §File Format |
| Añadiendo al Historial de Decisiones al final del flujo | §Append Templates |
| Conflicto con codebase detectado | §Conflict UX |
| Bootstrap finalizado → escribiendo línea base | §File Format |

NO pre-cargar el template al inicio.
