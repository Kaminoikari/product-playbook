# 🔧 Menú de Frameworks + Comandos Complementarios

> Se carga cuando el usuario solicita "listar frameworks," "muéstrame los frameworks disponibles," o usa un comando complementario.

## Especificar un Framework

**Dos formas de activar:**

**Método A (El usuario nombra directamente un framework):** Ir directo al flujo guiado de ese framework — no es necesario preguntar de nuevo.

**Método B (El usuario dice "quiero elegir un framework," "listar todos los frameworks," etc.):** Presentar el siguiente menú:

```
📚 Frameworks disponibles — ingresa un número o nombre:

【Entendiendo Usuarios】
 1. JTBD (Jobs to Be Done) — Identificar el trabajo que los usuarios realmente quieren lograr
 2. Persona — Construir perfiles de usuario impulsados por uso/tarea/motivación
 3. User Journey Map — Mapear el recorrido completo de experiencia del usuario
 4. Descubrimiento Continuo — Construir un hábito semanal de interactuar con usuarios

【Definiendo el Problema】
 5. OST / Opportunity Solution Tree — Conectar sistemáticamente oportunidades con soluciones
 6. Posicionamiento / April Dunford — Encontrar la arena competitiva real y la diferenciación
 7. HMW — Reformular puntos de dolor como preguntas de diseño

【Diseño de Solución】
 8. Working Backwards / PR-FAQ — Comenzar desde los resultados del usuario y trabajar hacia atrás
 9. Pre-mortem — Predecir y prevenir el fracaso antes de que suceda
10. GEM — Priorización tridimensional Growth / Engagement / Monetization
11. RICE — Priorización cuantitativa de funcionalidades
12. MVP — Definir alcance mínimo viable del producto

【Capa de Estrategia】
13. Estrategia / Strategy Blocks — Jerarquía Misión → Visión → Estrategia
14. Modelo DHM — Evaluación de oportunidad Delight / Hard to copy / Margin-enhancing
15. Framework LNO — Asignación de tiempo Leverage / Neutral / Overhead
16. Empowered Teams — Equipos empoderados vs. feature teams

【Capa de Medición】
17. North Star / North Star Metric — Definir la métrica única que representa el valor central para el usuario
18. PMF — Evaluación de cuatro niveles de Product-Market Fit
19. Sean Ellis Score — Cuantificar nivel de entusiasmo PMF

【Capa de Negocio】
20. Modelo de Negocio y Precios — Selección de modelo de ingresos y alineación de precios basados en valor
21. Estrategia GTM — Estrategia de lanzamiento Go-to-Market y adquisición de clientes

【Handoff de Desarrollo】
22. Handoff de Desarrollo — Generar CLAUDE.md + TASKS.md + TICKETS.md para entregar a Claude Code para desarrollo

Ingresa un número o nombre de framework (selección múltiple permitida, separada por comas):
```

## Omitir Discovery / Ir Directo a Build

Cuando el usuario dice "omitir investigación de usuarios," "el problema ya es conocido," "ir directo a Desarrollo," lee `references/rules-build.md` y sigue la secuencia de pasos del Modo Build.

> Recuerda al usuario: "Omitir la fase de investigación de usuarios significa que tu solución está construida sobre suposiciones. Recomendamos realizar Descubrimiento Continuo lo antes posible después de la ejecución para validar."

## Activación del Modo Extensión de Funcionalidad

- "Agregar una funcionalidad" / "Quiero agregar una nueva funcionalidad" / "nueva funcionalidad para producto existente" → activa el Modo Extensión de Funcionalidad (lee `references/rules-build.md` → Ruta Rápida de Extensión de Funcionalidad)

## Comandos Complementarios

| Comando | Comportamiento |
|---------|---------------|
| `"Cambiar a [framework]"` | Cambiar inmediatamente, preservando contenido completado |
| `"Quiero cambiar la audiencia objetivo"` | Re-ajustar prioridad de frameworks y estilo de presentación |
| `"Omitir este paso"` | Recordar necesidad, luego respetar la decisión y pasar al siguiente paso |
| `"Volver a [paso/nombre de framework]"` | Regresar al paso especificado para re-guía (ver `references/rules-change-propagation.md`) |
| `"Simplificar"` / `"Expandir"` | Condensar a puntos clave / Agregar análisis en profundidad |
| `"Generar reporte"` | Leer `references/06-html-report.md`, producir un reporte de planificación HTML |
| `"Generar PRD"` / `"Generar documentos de ingeniería"` | Leer `references/04b-solutions.md`, integrar PR-FAQ + MVP + User Story + Pre-mortem, **también generar automáticamente: diagrama de flujo (Mermaid) + esquema BD (Mermaid ERD) + UI wireframe (HTML)** |
| `"Generar diagrama de flujo"` / `"Dibújame un diagrama de flujo"` | Producir diagrama de flujo en sintaxis Mermaid (activación independiente) |
| `"Generar esquema BD"` / `"Diseñar la base de datos"` | Producir esquema BD en sintaxis Mermaid ERD (activación independiente) |
| `"Generar UI wireframe"` / `"Dibújame un wireframe"` | Producir UI wireframe de baja fidelidad en HTML/SVG (activación independiente) |
| `"Generar presentación"` / `"Hacer un PPT"` | Invocar el skill pptx del sistema |
| `"Adaptar este documento para [audiencia]"` | Re-organizar puntos destacados de frameworks y lenguaje para la audiencia especificada |
| `"Solo tengo 15 minutos"` | Proporcionar las tres preguntas o acciones de decisión más críticas |
| `"Ejecutar evaluación de completitud"` | Evaluar qué áreas son sólidas y cuáles tienen riesgo |
| `"Ayúdame a encontrar las suposiciones"` | Identificar todas las suposiciones centrales no validadas |
| `"Ejecutar un Pre-mortem"` | Ejecutar inmediatamente un pre-mortem sobre cualquier solución |
| `"Generar versiones para diferentes audiencias"` | Producir automáticamente resúmenes adaptados a múltiples audiencias |
| `"¿En qué nivel de PMF está este producto?"` | Determinar el nivel de PMF y explicar el próximo hito |
| `"Ayúdame a encontrar el cuello de botella"` | Analizar el mayor obstáculo para alcanzar el Aha Moment |
| `"Esto es una revisión, no un producto nuevo"` | Cambiar a Modo Revisión (leer `references/rules-revision.md`) |
| `"Necesito convencer a mi jefe de que apruebe"` | Cambiar a Modo Jefe — enfatizar valor de negocio y lógica de recursos |
| `"Iniciar desarrollo"` / `"Generar paquete de handoff de desarrollo"` | Leer `references/07a-handoff-core.md`, confirmar stack tecnológico, luego generar el paquete completo de handoff de desarrollo |
| `"Configurar el proyecto"` / `"Conectar con Claude Code"` | Igual que arriba |
| `"Pausar"` / `"Guardar"` / `"Hacer otra cosa primero"` | Guardar progreso según `references/rules-progress.md` |
| `"Continuar"` / `"Volver a planificación"` | Retomar según `references/rules-progress.md` |
| `"Limpiar progreso"` / `"Empezar de nuevo"` | Eliminar archivo de progreso y comenzar desde cero |
| `/export [formato]` | Exportar al formato especificado. formato = `pdf` / `docx` / `pptx` / `html` / `md`. Leer `references/rules-export-document.md`. En el primer uso, cargar `references/rules-document-tools.md` primero para verificar herramientas. |
| `/parse [archivo]` | Analizar un documento subido a Markdown. Soporta PDF / DOCX / PPTX / imágenes. Leer `references/rules-import-document.md`. En el primer uso, cargar `references/rules-document-tools.md` primero para verificar herramientas. |

**Sugerencias de comandos con contexto**: Después de completar cada paso, sugerir proactivamente 2-3 de los comandos disponibles más relevantes según el progreso actual.
