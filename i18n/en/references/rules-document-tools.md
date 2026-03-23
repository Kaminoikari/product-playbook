# Document Conversion Tool Dependency Management

> Loaded on first trigger of `/export` or `/parse` command.

## Dependency Tiers

| Tier | Tool | Purpose | Installation | Size |
|------|------|---------|-------------|------|
| **Core (Zero Install)** | Claude Read tool (Vision) | PDF semantic parsing | Built-in | 0 |
| **Core (Zero Install)** | Playwright MCP | PDF rendering | Built-in | 0 |
| **Basic** | pymupdf (fitz) | PDF text extraction + image rendering | `pip3 install --break-system-packages pymupdf` | ~23MB |
| **Basic** | pikepdf | PDF bookmark injection + metadata | `pip3 install --break-system-packages pikepdf` | ~5MB |
| **Extended** | pandoc | DOCX / PPTX conversion | `brew install pandoc` | ~50MB |
| **Fallback** | tesseract + chi_tra | Offline OCR (when Vision is unavailable) | `brew install tesseract tesseract-lang` | ~150MB |
| **Advanced** | python-docx | High-quality DOCX output | `pip3 install --break-system-packages python-docx` | ~5MB |

## Startup Detection Flow

When the user first triggers a document conversion feature, detect and install as needed in the following order:

### Step 1: Determine Which Tools Are Needed

| User Action | Required Tools |
|-------------|---------------|
| `/export pdf` | pymupdf + pikepdf + Playwright MCP |
| `/export docx` or `/export pptx` | pandoc |
| `/parse [PDF file]` | pymupdf (+ Claude Vision or tesseract) |
| `/parse [DOCX/PPTX file]` | pandoc |

### Step 2: Detect Installed Tools

Run the following Bash commands (silent detection, no output displayed):

```bash
# pymupdf
python3 -c "import fitz; print(fitz.version)" 2>/dev/null && echo "pymupdf: OK" || echo "pymupdf: MISSING"

# pikepdf
python3 -c "import pikepdf; print(pikepdf.__version__)" 2>/dev/null && echo "pikepdf: OK" || echo "pikepdf: MISSING"

# pandoc
which pandoc >/dev/null 2>&1 && echo "pandoc: OK" || echo "pandoc: MISSING"

# tesseract (only detect when explicitly needed)
which tesseract >/dev/null 2>&1 && tesseract --list-langs 2>&1 | grep -q chi_tra && echo "tesseract: OK" || echo "tesseract: MISSING"
```

### Step 3: Auto-Install Missing Tools

If missing tools are detected, display the following message and install automatically:

```
📦 Document conversion requires the following tools:
  ☐ [Tool name] ([purpose], [size])
  ...
Installing, please wait...
```

Run installation commands in sequence:

```bash
# pymupdf + pikepdf (install together)
pip3 install --break-system-packages pymupdf pikepdf

# pandoc
brew install pandoc

# tesseract (only when offline OCR is needed)
brew install tesseract tesseract-lang
```

After installation completes, display:
```
✅ Tool installation complete, continuing...
```

### Step 4: Detect Playwright MCP

Playwright MCP is a core dependency for PDF rendering. Detection method:

1. Attempt to call `mcp__plugin_playwright_playwright__browser_run_code`
2. If MCP is available → use normally
3. If MCP is unavailable (not connected) → display:

```
⚠️ Playwright MCP is not connected. PDF rendering requires the Playwright browser.
Please do one of the following:
  1. Start Playwright MCP (recommended)
  2. Or run ! npx playwright install chromium to install local Chromium
```

**Playwright Fallback** (when MCP is unavailable):

If the user has installed local Chromium, use Bash to run a Node.js script for PDF rendering:
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

## Tool State Cache

First detection results are recorded in memory (to avoid repeated detection):
- Within the same conversation session, confirmed installed tools are not re-detected
- If installation fails, record the error message and retry on the next trigger

## Platform Compatibility

| Platform | pymupdf | pikepdf | pandoc | tesseract | Playwright |
|----------|---------|---------|--------|-----------|------------|
| macOS (Homebrew) | ✅ pip3 | ✅ pip3 | ✅ brew | ✅ brew | ✅ MCP/npx |
| Linux (apt) | ✅ pip3 | ✅ pip3 | ✅ apt | ✅ apt | ✅ MCP/npx |
| Windows (WSL) | ✅ pip3 | ✅ pip3 | ✅ choco | ✅ choco | ✅ MCP/npx |

Automatically select the corresponding package manager based on the user's operating system. Detection method:
```bash
[[ "$(uname)" == "Darwin" ]] && echo "macOS" || echo "Linux"
```
