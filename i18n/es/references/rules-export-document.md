# Reglas de Exportación de Documentos Multi-Formato

> Se carga cuando el usuario activa `/export [formato]` o selecciona un formato de exportación después de que el flujo termina.
> En el primer uso, cargar `rules-document-tools.md` primero para confirmar que las herramientas están instaladas.

## Formatos de Exportación Soportados

| Formato | Comando | Ruta de Conversión | Herramientas |
|---------|---------|-------------------|-------------|
| PDF | `/export pdf` | HTML+CSS → Playwright → pikepdf marcadores | Playwright MCP + pikepdf |
| DOCX | `/export docx` | MD → Pandoc | pandoc + reference.docx |
| PPTX | `/export pptx` | MD → Pandoc | pandoc |
| HTML | `/export html` | Reglas existentes de `06-html-report.md` | Integrado |
| Markdown | `/export md` | Salida directa | Integrado |

---

## Exportación PDF (Flujo Principal)

### Selección de Ruta

La exportación PDF tiene dos rutas, seleccionadas automáticamente según el contenido fuente:

| Fuente | Ruta | Razón |
|--------|------|-------|
| Exportación directa del output de planificación (PRD / actualización incremental / especificación) | **Ruta A: setContent** | Sin dependencias JS externas, todos los recursos pueden estar en línea |
| Reporte de planificación HTML a PDF (con diagramas Mermaid / fuentes CDN) | **Ruta B: Servidor HTTP** | Necesita cargar JS externo (mermaid.js) y fuentes CDN |

### Ruta A: Documento Independiente → PDF (setContent)

Aplicable a: PRD, actualizaciones incrementales de extensión de funcionalidades, especificaciones, cualquier contenido sin JS externo.

**Paso 1: Generar Contenido HTML**

Claude lee `references/templates/prd-style.css` y genera un documento HTML completo:

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<style>
/* Leer el contenido completo de prd-style.css e insertar aquí en línea */
</style>
</head>
<body>

<!-- Página de portada -->
<div class="cover-page">
  <h1>[Título del Documento]</h1>
  <div class="subtitle">[Subtítulo o descripción en una línea]</div>
  <div class="version-badge">[Número de Versión]</div>
  <div class="meta-info">
    <strong>PM</strong> [Nombre del PM]<br>
    <strong>Fecha</strong> [Fecha ISO]<br>
    <strong>Estado</strong> [Estado]
  </div>
</div>

<!-- Leyenda (solo para documentos de actualización incremental) -->
<div class="diff-legend">
  <div class="diff-legend-item"><div class="diff-legend-swatch swatch-new"></div> Nuevo en esta versión</div>
  <div class="diff-legend-item"><div class="diff-legend-swatch swatch-upd"></div> Modificado en esta versión</div>
  <div class="diff-legend-item"><div class="diff-legend-swatch swatch-unchanged"></div> Sin cambios</div>
</div>

<!-- Página de tabla de contenidos -->
<div class="toc-page">
  <h2>Tabla de Contenidos</h2>
  <ul class="toc">
    <!-- Claude auto-genera elementos del TOC basándose en encabezados h2 -->
    <li>
      <span class="toc-title">[Nombre de Sección]</span>
      <span class="toc-dots"></span>
      <span class="toc-page-num">[Número de Página]</span>
    </li>
  </ul>
</div>

<!-- Contenido del cuerpo -->
[HTML del Cuerpo]

<!-- Pie de página -->
<div class="doc-footer">
  [Código del Documento] [Versión] ｜ [Fecha] ｜ Generado por Product Playbook
</div>

</body>
</html>
```

**Importante**:
- El CSS debe estar completamente en línea (sin enlaces externos)
- Las fuentes usan fuentes del sistema: `"PingFang TC", "Noto Sans TC", system-ui` (Playwright las incrustará automáticamente en el PDF)
- Sin etiquetas `<script>` ni referencias a recursos externos
- Los números de página del TOC son estimaciones (pueden necesitar ajuste fino después de la generación del PDF)

**Paso 2: Playwright Renderiza el PDF**

Guardar el contenido HTML en `/tmp/export-{timestamp}.html`, luego llamar a Playwright MCP:

```javascript
// mcp__plugin_playwright_playwright__browser_run_code
async (page) => {
  const fs = require('fs');
  const html = fs.readFileSync('/tmp/export-{timestamp}.html', 'utf8');
  await page.setContent(html, { waitUntil: 'networkidle' });
  await page.pdf({
    path: '{output_path}',
    format: 'A4',
    margin: { top: '1.8cm', bottom: '1.8cm', left: '2cm', right: '2cm' },
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: '<div style="font-size:8pt;color:#999;text-align:center;width:100%;">p.<span class="pageNumber"></span> / <span class="totalPages"></span></div>'
  });
  return 'PDF generated';
}
```

> Nota: Si el contenido HTML es demasiado grande (>500KB), setContent puede agotar el tiempo de espera. En ese caso, cambiar a la Ruta B (Servidor HTTP).

**Paso 3: Inyección de Marcadores con pikepdf**

```python
import pikepdf, re

pdf = pikepdf.open('{output_path}')

# Extraer encabezados h2 del HTML como marcadores
# Claude debe registrar el número de página estimado para cada h2 al generar el HTML
bookmarks = [
    # (título, índice de página base 0)
    ("Historial de Revisiones", 2),
    ("User Story", 4),
    ("Arquitectura de Desarrollo", 6),
    # ... generado según el contenido real
]

with pdf.open_outline() as outline:
    for title, page_idx in bookmarks:
        page_idx = min(page_idx, len(pdf.pages) - 1)
        outline.root.append(
            pikepdf.OutlineItem(title, page_idx)
        )

# Establecer metadatos del PDF
with pdf.open_metadata() as meta:
    meta['dc:title'] = '[Título del Documento]'
    meta['dc:creator'] = ['[Nombre del PM]']
    meta['pdf:Producer'] = 'Product Playbook + Playwright'

pdf.save('{output_path}')
```

**Paso 4: Notificar al Usuario**

```
✅ PDF exportado a: {output_path}
  📄 {page_count} páginas ｜ {file_size}
  📑 Incluye navegación por marcadores ({bookmark_count} secciones)
```

### Ruta B: Reporte HTML → PDF (Servidor HTTP)

Aplicable a: Reportes HTML con diagramas Mermaid, fuentes CDN, elementos interactivos.

**Paso 1: Reporte HTML Ya Generado**

El reporte HTML es generado por las reglas de `06-html-report.md` y guardado como `/tmp/report-{timestamp}.html`.

**Paso 2: Iniciar Servidor HTTP**

```bash
cd /tmp && python3 -m http.server 18899 &
echo $!  # Registrar PID
```

**Paso 3: Renderizado con Playwright**

```javascript
// mcp__plugin_playwright_playwright__browser_run_code
async (page) => {
  await page.goto('http://localhost:18899/report-{timestamp}.html', {
    waitUntil: 'networkidle',
    timeout: 30000
  });
  // Esperar a que el renderizado de gráficos Mermaid se complete
  await page.waitForTimeout(3000);
  // Expandir todos los elementos accordion (<details>)
  await page.evaluate(() => {
    document.querySelectorAll('details').forEach(d => d.open = true);
  });
  await page.pdf({
    path: '{output_path}',
    format: 'A4',
    margin: { top: '1.8cm', bottom: '1.8cm', left: '2cm', right: '2cm' },
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: '<div style="font-size:8pt;color:#999;text-align:center;width:100%;">p.<span class="pageNumber"></span> / <span class="totalPages"></span></div>'
  });
  return 'PDF generated';
}
```

**Paso 4: Apagar Servidor HTTP + Marcadores pikepdf**

```bash
kill {SERVER_PID}
```

Luego realizar el mismo paso de inyección de marcadores con pikepdf que en la Ruta A.

### Fallback cuando Playwright MCP No Está Disponible

Si Playwright MCP no está conectado, usar Node.js directamente:

```bash
node -e "
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  const html = fs.readFileSync('/tmp/export-{timestamp}.html', 'utf8');
  await page.setContent(html, { waitUntil: 'networkidle' });
  await page.pdf({
    path: '${OUTPUT_PATH}',
    format: 'A4',
    printBackground: true,
    margin: { top: '1.8cm', bottom: '1.8cm', left: '2cm', right: '2cm' }
  });
  await browser.close();
  console.log('PDF generated');
})();
"
```

---

## Exportación DOCX

### Paso 1: Generar Markdown

Claude organiza el output de planificación en formato Markdown limpio y lo guarda como `/tmp/export-{timestamp}.md`.

### Paso 2: Conversión con Pandoc

```bash
pandoc /tmp/export-{timestamp}.md \
  -o "{output_path}" \
  --from markdown \
  --to docx \
  --reference-doc="~/.claude/skills/the-product-playbook/references/templates/reference.docx" \
  --toc \
  --toc-depth=2
```

Si no hay plantilla reference.docx disponible, omitir el parámetro `--reference-doc` (usa estilos por defecto de Pandoc).

### Paso 3: Notificar al Usuario

```
✅ Documento Word exportado a: {output_path}
  📄 Incluye tabla de contenidos ｜ {file_size}
```

---

## Exportación PPTX

```bash
pandoc /tmp/export-{timestamp}.md \
  -o "{output_path}" \
  --from markdown \
  --to pptx \
  --slide-level=2
```

> Consejo: La calidad de PPTX de Pandoc es limitada. Se recomienda usar el PPTX como esquema, luego pulir con PowerPoint/Keynote.

---

## Manejo Especial para Documentos de Actualización Incremental

Al exportar documentos de actualización incremental del modo Extensión de Funcionalidades o Revisión:

### Reglas de Marcado Visual de Diferencias

1. **Párrafos marcados `[NEW]`**:
   - Usar marcador `<span class="new">NEW</span>`
   - Las filas de tabla obtienen `class="new-row"`
   - Los párrafos obtienen `class="diff-added"`

2. **Párrafos marcados `[UPDATED]`**:
   - Usar marcador `<span class="upd">UPDATED</span>`
   - Las filas de tabla obtienen `class="upd-row"`
   - Si existe contenido original, el contenido original obtiene `class="diff-removed"`, el nuevo contenido obtiene `class="diff-added"`

3. **Párrafos sin cambios**: Se muestran normalmente, sin marcadores especiales

4. **Leyenda al inicio del documento**:
```html
<div class="diff-legend">
  <div class="diff-legend-item">
    <div class="diff-legend-swatch swatch-new"></div> Nuevo en esta versión
  </div>
  <div class="diff-legend-item">
    <div class="diff-legend-swatch swatch-upd"></div> Modificado en esta versión
  </div>
  <div class="diff-legend-item">
    <div class="diff-legend-swatch swatch-unchanged"></div> Sin marcador = Sin cambios
  </div>
</div>
```

---

## Reglas de Ruta de Salida

Salida por defecto a `~/Downloads/`, formato del nombre de archivo:

```
[Código del Documento] [Título del Documento] [Versión].{ext}

Ejemplos:
[D-221] Cuenta Virtual v1.0.14 Versión Completa Fusionada.pdf
Reporte de Planificación de Producto - Cuenta Virtual UPASS.docx
```

Si el usuario especifica una ruta, usar la ruta especificada por el usuario.

---

## Lista de Verificación de Calidad

Antes de exportar, Claude auto-verifica:

- [ ] No queda sintaxis Markdown residual en el HTML (`**`, `##`, `|---|`)
- [ ] Todos los conteos de filas y columnas de tablas coinciden con el contenido original
- [ ] Los marcadores `[NEW]` / `[UPDATED]` están correctamente mapeados a las clases CSS correspondientes
- [ ] La información de la portada (título, versión, PM, fecha) es correcta
- [ ] Los elementos del TOC coinciden con los encabezados h2 del cuerpo
- [ ] El CSS está completamente en línea (Ruta A) o el CDN es accesible (Ruta B)
- [ ] El conteo de marcadores coincide con el conteo de encabezados h2
