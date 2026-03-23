# Reglas de Importación y Análisis de Documentos

> Se carga cuando el usuario sube un archivo PDF / DOCX / PPTX, o activa `/parse [archivo]`.
> En el primer uso, cargar `rules-document-tools.md` primero para confirmar que las herramientas están instaladas.
> Esta regla funciona en conjunto con `rules-file-integration.md` — ese archivo define "cuándo activar," este archivo define "cómo analizar."

---

## Objetivo del Análisis

Convertir cualquier formato de documento de entrada en **Markdown estructurado** para uso en flujos posteriores:
- Recopilación de contexto S1 del modo Extensión de Funcionalidades / Revisión
- Baseline del documento fuente para actualización incremental
- Extracción general de contenido de documentos

---

## Análisis de PDF: Estrategia de Tres Capas + Detección Por Página

### Resumen General

```
PDF de entrada
  │
  ▼
Extracción de texto por página con pymupdf (costo cero)
  │
  ├── Texto de página > 30 caracteres → ✅ Convertir directamente a Markdown (Capa 1)
  │
  └── Texto de página ≤ 30 caracteres (en blanco / trazos vectoriales / escaneado)
        │
        ├── Por defecto → Análisis semántico con Claude Vision (Capa 2)
        │
        └── Vision no disponible / Presupuesto de tokens insuficiente → Tesseract OCR (Capa 3)
```

### Paso 1: Detección de Tipo Por Página

**Principio clave**: Detectar a nivel de "página", no del documento completo. Un solo PDF puede mezclar páginas de texto digital y páginas de imágenes escaneadas.

```python
import fitz  # pymupdf

doc = fitz.open(pdf_path)
total_pages = len(doc)
page_results = {}

for i in range(total_pages):
    page = doc[i]
    text = page.get_text("text").strip()

    if len(text) > 30:
        # Capa 1: Texto digital, extraer directamente
        page_results[i] = {"type": "digital", "text": text}
    else:
        # Necesita Vision u OCR
        page_results[i] = {"type": "needs_vision", "text": None}

digital_count = sum(1 for p in page_results.values() if p["type"] == "digital")
vision_count = total_pages - digital_count

print(f"Análisis PDF: {total_pages} páginas, {digital_count} extraíbles directamente, {vision_count} requieren análisis visual")
```

### Paso 2: Estrategia para Archivos Grandes

| Condición | Estrategia |
|-----------|-----------|
| Todas las páginas son digitales (vision_count = 0) | Extraer todas las páginas directamente, costo cero |
| vision_count ≤ 20 | Leer todas las páginas que necesitan análisis visual de una vez con Claude Vision |
| vision_count > 20 | Procesar en lotes (≤ 20 páginas cada uno), fusionar resultados |
| Total de páginas > 50 y vision_count > 20 | Preguntar al usuario si desea analizar el documento completo o especificar un rango de páginas |

**Prompt de confirmación para archivos grandes (>50 páginas)**:

```
📄 Este PDF tiene {total_pages} páginas:
  • {digital_count} páginas se pueden extraer directamente (gratis)
  • {vision_count} páginas requieren análisis visual (consume tokens de Vision)

Por favor elige:
  1️⃣ Análisis completo del documento (completo pero consume más tokens)
  2️⃣ Analizar solo páginas específicas (ingresa rangos de páginas, p.ej. 1-10,15,20-25)
  3️⃣ Extraer solo páginas directamente extraíbles (omitir páginas escaneadas/vectoriales)
```

### Paso 3: Capa 1 — Extracción Directa con pymupdf

```python
def extract_digital_pages(doc, page_results):
    """Extraer todas las páginas de texto digital"""
    markdown_parts = []
    for i, result in sorted(page_results.items()):
        if result["type"] == "digital":
            markdown_parts.append(f"<!-- Page {i+1} -->\n{result['text']}")
    return "\n\n".join(markdown_parts)
```

### Paso 4: Capa 2 — Análisis Semántico con Claude Vision

Para páginas de tipo `needs_vision`, primero renderizar a PNG con pymupdf, luego leer con la herramienta Read de Claude.

**Renderizar a imagen**:
```python
def render_pages_to_png(doc, page_indices, dpi=300):
    """Renderizar páginas especificadas a PNG"""
    output_files = []
    for i in page_indices:
        page = doc[i]
        pix = page.get_pixmap(dpi=dpi)
        output_path = f"/tmp/pdf-page-{i+1:04d}.png"
        pix.save(output_path)
        output_files.append((i, output_path))
    return output_files
```

**Prompt de análisis con Claude Vision**:

Para cada página que requiere análisis visual (o lote), después de leer el PNG con la herramienta Read, convertir usando el siguiente prompt:

```
Estás leyendo la página {page_num}/{total_pages} de un documento PDF.
Por favor convierte el contenido de esta página precisamente a formato Markdown.

Reglas estrictas:
1. Tablas → Tabla Markdown (preservar todas las columnas, filas y alineación)
2. Encabezados → # / ## / ### correspondiente al nivel original
3. Listas numeradas → 1. 2. 3. (preservar numeración original)
4. Viñetas → - o •
5. Negrita/Cursiva → **negrita** / *cursiva*
6. Gráficos/Imágenes → > [Gráfico: descripción breve]
7. Encabezados de página, pies de página, números de página → Ignorar
8. Números, fechas, nombres, números de cuenta → Deben ser 100% precisos, no adivinar
9. No agregar contenido que no esté presente en el original
10. No traducir — preservar el idioma original
```

> **Por qué esto es mejor que OCR**: Claude entiende la "estructura semántica" de las tablas (qué fila es el encabezado, qué columnas están alineadas), mientras que Tesseract solo puede reconocer caracteres uno por uno e intentar reconstruir tablas con reglas, lo cual frecuentemente falla.

### Paso 5: Capa 3 — Fallback con Tesseract OCR

Usar solo en las siguientes situaciones:
- El usuario solicita explícitamente conservar tokens
- Claude Vision no está disponible (limitaciones de API, etc.)
- Entorno offline

```python
import subprocess
from PIL import Image

def ocr_page(png_path, lang="chi_tra+eng"):
    """Tesseract OCR página individual"""
    # macOS tesseract puede no leer PNG directamente, convertir a TIFF o usar stdin
    tiff_path = png_path.replace('.png', '.tiff')
    Image.open(png_path).save(tiff_path)

    result = subprocess.run(
        ['tesseract', 'stdin', 'stdout', '-l', lang],
        stdin=open(tiff_path, 'rb'),
        capture_output=True, text=True, timeout=120
    )
    return result.stdout
```

**Notas sobre Tesseract (de experiencia práctica)**:
- En macOS, tesseract puede no leer archivos PNG directamente — usar pipe `stdin` o convertir a TIFF primero
- Resolución recomendada: 300dpi
- El paquete de idiomas `chi_tra+eng` reconoce tanto chino tradicional como inglés simultáneamente
- Los resultados de OCR necesitan post-procesamiento: fusionar líneas rotas, reparar estructura de tablas

### Paso 6: Fusionar Todas las Páginas

```python
def merge_all_pages(digital_md, vision_md_list):
    """Fusionar el Markdown de todas las páginas en orden de página"""
    all_pages = {}
    # páginas digitales
    for page_num, md in digital_md.items():
        all_pages[page_num] = md
    # páginas vision/ocr
    for page_num, md in vision_md_list.items():
        all_pages[page_num] = md

    # Ordenar por número de página y fusionar
    final_md = []
    for i in sorted(all_pages.keys()):
        final_md.append(all_pages[i])

    return "\n\n---\n\n".join(final_md)
```

### Paso 7: Output y Notificación al Usuario

```
📄 Análisis de PDF completado:
  • Total de páginas: {total_pages}
  • Extracción directa: {digital_count} páginas (pymupdf)
  • Análisis visual: {vision_count} páginas (Claude Vision)
  • Output: {output_path} (Markdown, {word_count} palabras)
```

---

## Análisis de DOCX

```bash
pandoc "{input_path}" -t markdown -o "/tmp/parsed-{timestamp}.md" --wrap=none
```

**Post-procesamiento**:
- Eliminar líneas en blanco excesivas generadas por Pandoc
- Verificar que el formato de tablas sea correcto

---

## Análisis de PPTX

```bash
pandoc "{input_path}" -t markdown -o "/tmp/parsed-{timestamp}.md" --wrap=none
```

> Pandoc convierte cada diapositiva en una sección con encabezado `##`.

---

## Análisis de HTML

```bash
pandoc "{input_path}" -f html -t markdown -o "/tmp/parsed-{timestamp}.md" --wrap=none
```

---

## Análisis de Imágenes

Usar directamente la herramienta Read de Claude para leer la imagen, luego convertir a Markdown usando el prompt de análisis de Vision.

---

## Coordinación con rules-file-integration.md

Cuando `rules-file-integration.md` detecta los siguientes escenarios, se carga esta regla:

| Escenario | Acción |
|-----------|--------|
| El usuario sube un PDF durante Extensión de Funcionalidades S1 | Cargar esta regla → Analizar PDF → Extraer contexto del sistema existente |
| El usuario sube un PRD antiguo durante Revisión S1 | Cargar esta regla → Analizar PDF → Usar como baseline de revisión |
| El usuario usa el comando `/parse` | Cargar esta regla → Analizar archivo especificado → Output en Markdown |
| El usuario sube un reporte de mercado en PDF | Cargar esta regla → Extraer información clave → Integrar en el paso correspondiente |

### Identificación de Documento Fuente

Después de completar el análisis, si el archivo se identifica como un "documento fuente" (PRD, especificación, etc.), marcarlo automáticamente:

```
📎 Documento fuente detectado — la salida final será una actualización incremental basada en este archivo.
  Estructura del documento: {section_count} secciones, {table_count} tablas
  Convenciones de formato: [características de formato identificadas]
```

La estructura del documento se registra para uso de `rules-export-document.md` durante la salida final.
