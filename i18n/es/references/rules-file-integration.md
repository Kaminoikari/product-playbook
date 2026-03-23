# 📎 Guía de Integración de Archivos

> Se carga cuando el usuario sube materiales complementarios.

## Tipos de Archivo Directamente Soportados

| Tipo de Archivo | Escenarios Comunes | Método de Integración |
|----------------|-------------------|----------------------|
| **Imágenes** | Capturas de pantalla de competidores, fotos de pizarrón, journey maps dibujados a mano, capturas de interfaz de app, capturas de reportes de datos | Reconocer contenido e integrar al paso correspondiente |
| **PDF** | Reportes de mercado, documentos internos, reportes de investigación de usuarios, PRDs existentes | Cargar `rules-import-document.md` para análisis de tres capas (extracción directa pymupdf → análisis semántico Claude Vision → fallback Tesseract). En el primer uso, cargar `rules-document-tools.md` para verificar herramientas. |
| **CSV / Excel** | Datos de comportamiento de usuario, datos de retención, resultados de encuestas NPS, datos de ventas | Analizar datos y usar para evaluación cuantitativa |
| **Archivos de texto** | Transcripciones de entrevistas, documentos de requisitos existentes, notas de reuniones | Extraer pistas de Persona, puntos de dolor, evidencia JTBD |
| **DOCX** | PRDs existentes, documentos de especificación de producto, reportes de investigación de usuarios | Cargar `rules-import-document.md`, usar Pandoc para convertir a Markdown luego integrar. En el primer uso, cargar `rules-document-tools.md` para verificar herramientas. |
| **PPTX** | Presentaciones existentes, diapositivas de introducción de producto | Cargar `rules-import-document.md`, usar Pandoc para convertir a Markdown luego integrar. |

## No Directamente Soportados pero con Guía Disponible

| Tipo de Archivo | Guía |
|----------------|------|
| **Video** | Pedir al usuario que describa escenas clave, o proporcionar transcripción/archivo de subtítulos |
| **Figma / Sketch** | Pedir al usuario que tome capturas de pantalla y las suba |
| **Protobuf / Swagger** | Pedir al usuario que exporte como formato JSON o texto |

## Tabla de Auto-Mapeo Archivo → Paso

| Contenido Subido | Paso Auto-Mapeado | Acción de Integración |
|-----------------|-------------------|----------------------|
| Capturas de app / sitio web de competidores | Posicionamiento | Identificar como "alternativas competitivas," analizar diferenciación |
| Diagrama de flujo dibujado a mano en pizarrón | Journey Map / OST | Reconocer el flujo y convertir a tabla estructurada |
| Transcripción de entrevista de usuario | Persona + JTBD | Extraer puntos de dolor, soluciones alternativas actuales, reacciones emocionales, declaraciones de Job |
| Datos de comportamiento de usuario (CSV) | Evaluación de Oportunidades + North Star + PMF | Reemplazar puntuaciones basadas en suposiciones con datos reales |
| Encuesta NPS / satisfacción | PMF + Sean Ellis Score | Calcular directamente el Score; determinar nivel de PMF |
| PRD existente / documento de requisitos | Modo Revisión S1 + MVP | Extraer lista de funcionalidades existentes e historial de decisiones |
| Reporte de mercado PDF | Evaluación de Oportunidades + Estrategia | Extraer tamaño de mercado, tendencias, panorama competitivo |
| Datos de ventas | Modelo de Negocio + GTM | Analizar estructura de ingresos, distribución de clientes, efectividad de canales |
| Capturas de interfaz de app | Aha Moment + Journey | Analizar la ruta de experiencia actual |

## Reglas de Integración

1. **Identificación proactiva**: Primero explica "Veo que subiste [tipo de archivo]. Integraré la [información clave] de este en [nombre del paso]."
2. **No sobrescribir output existente**: Marca el contenido subido como "material complementario," actualiza el output y activa las reglas de propagación de cambios
3. **Marcar la fuente**: Anota en el output qué contenido provino del archivo subido (p.ej., "✦ Del reporte de investigación de usuarios subido")
4. **Datos tienen prioridad**: Cuando datos reales entran en conflicto con suposiciones previas, priorizar los datos reales
5. **Impacto cross-paso**: Un solo archivo puede afectar múltiples pasos — listar todos los pasos afectados a la vez

## 📎 Identificación de Documento Fuente y Actualización Incremental

Cuando un usuario sube un archivo durante la **Extensión de Funcionalidades** o el **Modo Revisión**, determinar si es un "documento fuente" (un documento que debe actualizarse incrementalmente con la nueva planificación):

### Criterios de Identificación
- Tipo de archivo: PRD, especificación de producto, documento de arquitectura, documento de requisitos, documento de diseño
- El usuario dice explícitamente: "este es nuestro PRD actual", "actualiza este documento", "construye sobre esta especificación", etc.
- Subido durante S1 (recopilación de contexto) de Extensión de Funcionalidades o Modo Revisión

### Cuando Se Identifica un Documento Fuente
1. Marcarlo: "📎 Documento fuente detectado — la salida final será una actualización incremental basada en este archivo"
2. Analizar la estructura del documento (encabezados de sección, convenciones de formato, patrones de nomenclatura)
3. Registrar el formato y estilo del documento para una salida consistente
4. Durante S1, usar el documento para prellenar el contexto del sistema existente (stack tecnológico, módulos, funcionalidades)

### Reglas de Salida Incremental (aplicadas en la etapa de Salida Final)
- El contenido nuevo se inserta en las secciones correspondientes, marcado con `[NEW]`
- El contenido modificado se marca con `[UPDATED]`, el contenido original se preserva como comentario
- Las secciones no relacionadas con la nueva funcionalidad permanecen intactas
- El documento de salida mantiene el formato, estilo y convenciones de nomenclatura del archivo original
