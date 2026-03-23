# Gestión de Dependencias de Herramientas de Conversión de Documentos

> Se carga en el primer activación del comando `/export` o `/parse`.

## Niveles de Dependencias

| Nivel | Herramienta | Propósito | Instalación | Tamaño |
|-------|-------------|-----------|-------------|--------|
| **Core (Sin Instalación)** | Claude Read tool (Vision) | Análisis semántico de PDF | Integrado | 0 |
| **Core (Sin Instalación)** | Playwright MCP | Renderizado de PDF | Integrado | 0 |
| **Básico** | pymupdf (fitz) | Extracción de texto PDF + renderizado de imágenes | `pip3 install --break-system-packages pymupdf` | ~23MB |
| **Básico** | pikepdf | Inyección de marcadores PDF + metadatos | `pip3 install --break-system-packages pikepdf` | ~5MB |
| **Extendido** | pandoc | Conversión DOCX / PPTX | `brew install pandoc` | ~50MB |
| **Fallback** | tesseract + chi_tra | OCR offline (cuando Vision no está disponible) | `brew install tesseract tesseract-lang` | ~150MB |
| **Avanzado** | python-docx | Salida DOCX de alta calidad | `pip3 install --break-system-packages python-docx` | ~5MB |

## Flujo de Detección al Inicio

Cuando el usuario activa por primera vez una función de conversión de documentos, detectar e instalar según sea necesario en el siguiente orden:

### Paso 1: Determinar Qué Herramientas Se Necesitan

| Acción del Usuario | Herramientas Requeridas |
|---------------------|------------------------|
| `/export pdf` | pymupdf + pikepdf + Playwright MCP |
| `/export docx` o `/export pptx` | pandoc |
| `/parse [archivo PDF]` | pymupdf (+ Claude Vision o tesseract) |
| `/parse [archivo DOCX/PPTX]` | pandoc |

### Paso 2: Detectar Herramientas Instaladas

Ejecutar los siguientes comandos Bash (detección silenciosa, sin output visible):

```bash
# pymupdf
python3 -c "import fitz; print(fitz.version)" 2>/dev/null && echo "pymupdf: OK" || echo "pymupdf: MISSING"

# pikepdf
python3 -c "import pikepdf; print(pikepdf.__version__)" 2>/dev/null && echo "pikepdf: OK" || echo "pikepdf: MISSING"

# pandoc
which pandoc >/dev/null 2>&1 && echo "pandoc: OK" || echo "pandoc: MISSING"

# tesseract (solo detectar cuando se necesita explícitamente)
which tesseract >/dev/null 2>&1 && tesseract --list-langs 2>&1 | grep -q chi_tra && echo "tesseract: OK" || echo "tesseract: MISSING"
```

### Paso 3: Auto-Instalar Herramientas Faltantes

Si se detectan herramientas faltantes, mostrar el siguiente mensaje e instalar automáticamente:

```
📦 La conversión de documentos requiere las siguientes herramientas:
  ☐ [Nombre de herramienta] ([propósito], [tamaño])
  ...
Instalando, por favor espere...
```

Ejecutar comandos de instalación en secuencia:

```bash
# pymupdf + pikepdf (instalar juntos)
pip3 install --break-system-packages pymupdf pikepdf

# pandoc
brew install pandoc

# tesseract (solo cuando se necesita OCR offline)
brew install tesseract tesseract-lang
```

Después de completar la instalación, mostrar:
```
✅ Instalación de herramientas completada, continuando...
```

### Paso 4: Detectar Playwright MCP

Playwright MCP es una dependencia core para el renderizado de PDF. Método de detección:

1. Intentar llamar a `mcp__plugin_playwright_playwright__browser_run_code`
2. Si MCP está disponible → usar normalmente
3. Si MCP no está disponible (no conectado) → mostrar:

```
⚠️ Playwright MCP no está conectado. El renderizado de PDF requiere el navegador Playwright.
Por favor haga una de las siguientes opciones:
  1. Iniciar Playwright MCP (recomendado)
  2. O ejecutar ! npx playwright install chromium para instalar Chromium local
```

**Fallback de Playwright** (cuando MCP no está disponible):

Si el usuario ha instalado Chromium local, usar Bash para ejecutar un script Node.js para renderizado de PDF:
```bash
node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setContent(require('fs').readFileSync('/tmp/export.html', 'utf8'));
  await page.pdf({ path: '${OUTPUT_PATH}', format: 'A4', printBackground: true,
    margin: { top: '1.8cm', bottom: '1.8cm', left: '2cm', right: '2cm' } });
  await browser.close();
})();
"
```

## Caché de Estado de Herramientas

Los resultados de la primera detección se registran en memoria (para evitar detección repetida):
- Dentro de la misma sesión de conversación, las herramientas confirmadas como instaladas no se vuelven a detectar
- Si la instalación falla, registrar el mensaje de error y reintentar en la próxima activación

## Compatibilidad de Plataformas

| Plataforma | pymupdf | pikepdf | pandoc | tesseract | Playwright |
|------------|---------|---------|--------|-----------|------------|
| macOS (Homebrew) | ✅ pip3 | ✅ pip3 | ✅ brew | ✅ brew | ✅ MCP/npx |
| Linux (apt) | ✅ pip3 | ✅ pip3 | ✅ apt | ✅ apt | ✅ MCP/npx |
| Windows (WSL) | ✅ pip3 | ✅ pip3 | ✅ choco | ✅ choco | ✅ MCP/npx |

Seleccionar automáticamente el gestor de paquetes correspondiente según el sistema operativo del usuario. Método de detección:
```bash
[[ "$(uname)" == "Darwin" ]] && echo "macOS" || echo "Linux"
```
