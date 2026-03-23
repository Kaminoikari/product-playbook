# Document Import & Parsing Rules

> Loaded when the user uploads a PDF / DOCX / PPTX file, or triggers `/parse [file]`.
> On first use, load `rules-document-tools.md` first to confirm tools are installed.
> This rule works in conjunction with `rules-file-integration.md` — that file defines "when to trigger," this file defines "how to parse."

---

## Parsing Goal

Convert any format of input document into **structured Markdown** for use in subsequent flows:
- Feature Extension / Revision mode S1 context collection
- Incremental update source document baseline
- General document content extraction

---

## PDF Parsing: Three-Layer Strategy + Per-Page Detection

### Overview

```
Input PDF
  │
  ▼
pymupdf per-page text extraction (zero cost)
  │
  ├── Page text > 30 characters → ✅ Convert directly to Markdown (Layer 1)
  │
  └── Page text ≤ 30 characters (blank / vector paths / scanned)
        │
        ├── Default → Claude Vision semantic parsing (Layer 2)
        │
        └── Vision unavailable / Token budget insufficient → Tesseract OCR (Layer 3)
```

### Step 1: Per-Page Type Detection

**Key principle**: Detect at the "page" level, not the entire document. A single PDF may mix digital text pages and scanned image pages.

```python
import fitz  # pymupdf

doc = fitz.open(pdf_path)
total_pages = len(doc)
page_results = {}

for i in range(total_pages):
    page = doc[i]
    text = page.get_text("text").strip()

    if len(text) > 30:
        # Layer 1: Digital text, extract directly
        page_results[i] = {"type": "digital", "text": text}
    else:
        # Needs Vision or OCR
        page_results[i] = {"type": "needs_vision", "text": None}

digital_count = sum(1 for p in page_results.values() if p["type"] == "digital")
vision_count = total_pages - digital_count

print(f"PDF analysis: {total_pages} pages, {digital_count} directly extractable, {vision_count} require visual parsing")
```

### Step 2: Large File Handling Strategy

| Condition | Strategy |
|-----------|----------|
| All pages are digital (vision_count = 0) | Extract all pages directly, zero cost |
| vision_count ≤ 20 | Read all pages needing visual parsing at once with Claude Vision |
| vision_count > 20 | Process in batches (≤ 20 pages each), merge results |
| Total pages > 50 and vision_count > 20 | Ask the user whether to parse the full document or specify a page range |

**Large file (>50 pages) user confirmation prompt**:

```
📄 This PDF has {total_pages} pages:
  • {digital_count} pages can be directly extracted (free)
  • {vision_count} pages require visual parsing (consumes Vision tokens)

Please choose:
  1️⃣ Full document parsing (complete but consumes more tokens)
  2️⃣ Parse specific pages only (enter page ranges, e.g. 1-10,15,20-25)
  3️⃣ Extract only directly extractable pages (skip scanned/vector pages)
```

### Step 3: Layer 1 — pymupdf Direct Extraction

```python
def extract_digital_pages(doc, page_results):
    """Extract all digital text pages"""
    markdown_parts = []
    for i, result in sorted(page_results.items()):
        if result["type"] == "digital":
            markdown_parts.append(f"<!-- Page {i+1} -->\n{result['text']}")
    return "\n\n".join(markdown_parts)
```

### Step 4: Layer 2 — Claude Vision Semantic Parsing

For `needs_vision` type pages, first render to PNG with pymupdf, then read with Claude's Read tool.

**Render to image**:
```python
def render_pages_to_png(doc, page_indices, dpi=300):
    """Render specified pages to PNG"""
    output_files = []
    for i in page_indices:
        page = doc[i]
        pix = page.get_pixmap(dpi=dpi)
        output_path = f"/tmp/pdf-page-{i+1:04d}.png"
        pix.save(output_path)
        output_files.append((i, output_path))
    return output_files
```

**Claude Vision parsing prompt**:

For each page requiring visual parsing (or batch), after reading the PNG with the Read tool, convert using the following prompt:

```
You are reading page {page_num}/{total_pages} of a PDF document.
Please convert the content of this page precisely into Markdown format.

Strict rules:
1. Tables → Markdown table (preserve all columns, rows, and alignment)
2. Headings → # / ## / ### corresponding to original level
3. Numbered lists → 1. 2. 3. (preserve original numbering)
4. Bullet points → - or •
5. Bold/Italic → **bold** / *italic*
6. Charts/Images → > [Chart: brief description]
7. Headers, footers, page numbers → Ignore
8. Numbers, dates, names, account numbers → Must be 100% accurate, do not guess
9. Do not add content not present in the original
10. Do not translate — preserve the original language
```

> **Why this is better than OCR**: Claude understands the "semantic structure" of tables (which row is the header, which columns are aligned), whereas Tesseract can only recognize characters one by one and then attempt to reconstruct tables with rules, which often fails.

### Step 5: Layer 3 — Tesseract OCR Fallback

Use only in the following situations:
- User explicitly requests token conservation
- Claude Vision is unavailable (API limitations, etc.)
- Offline environment

```python
import subprocess
from PIL import Image

def ocr_page(png_path, lang="chi_tra+eng"):
    """Tesseract OCR single page"""
    # macOS tesseract may not read PNG directly, convert to TIFF or use stdin
    tiff_path = png_path.replace('.png', '.tiff')
    Image.open(png_path).save(tiff_path)

    result = subprocess.run(
        ['tesseract', 'stdin', 'stdout', '-l', lang],
        stdin=open(tiff_path, 'rb'),
        capture_output=True, text=True, timeout=120
    )
    return result.stdout
```

**Tesseract notes (from practical experience)**:
- On macOS, tesseract may not read PNG files directly — use `stdin` pipe or convert to TIFF first
- Recommended resolution: 300dpi
- `chi_tra+eng` language pack recognizes both Traditional Chinese and English simultaneously
- OCR results need post-processing: merge broken lines, repair table structure

### Step 6: Merge All Pages

```python
def merge_all_pages(digital_md, vision_md_list):
    """Merge all pages' Markdown in page order"""
    all_pages = {}
    # digital pages
    for page_num, md in digital_md.items():
        all_pages[page_num] = md
    # vision/ocr pages
    for page_num, md in vision_md_list.items():
        all_pages[page_num] = md

    # Sort by page number and merge
    final_md = []
    for i in sorted(all_pages.keys()):
        final_md.append(all_pages[i])

    return "\n\n---\n\n".join(final_md)
```

### Step 7: Output and Notify User

```
📄 PDF parsing complete:
  • Total pages: {total_pages}
  • Direct extraction: {digital_count} pages (pymupdf)
  • Visual parsing: {vision_count} pages (Claude Vision)
  • Output: {output_path} (Markdown, {word_count} words)
```

---

## DOCX Parsing

```bash
pandoc "{input_path}" -t markdown -o "/tmp/parsed-{timestamp}.md" --wrap=none
```

**Post-processing**:
- Remove excess blank lines generated by Pandoc
- Verify table formatting is correct

---

## PPTX Parsing

```bash
pandoc "{input_path}" -t markdown -o "/tmp/parsed-{timestamp}.md" --wrap=none
```

> Pandoc converts each slide into a `##` heading section.

---

## HTML Parsing

```bash
pandoc "{input_path}" -f html -t markdown -o "/tmp/parsed-{timestamp}.md" --wrap=none
```

---

## Image Parsing

Use the Claude Read tool directly to read the image, then convert to Markdown using the Vision parsing prompt.

---

## Coordination with rules-file-integration.md

When `rules-file-integration.md` detects the following scenarios, this rule is loaded:

| Scenario | Action |
|----------|--------|
| User uploads PDF during Feature Extension S1 | Load this rule → Parse PDF → Extract existing system context |
| User uploads old PRD during Revision S1 | Load this rule → Parse PDF → Use as revision baseline |
| User uses `/parse` command | Load this rule → Parse specified file → Output Markdown |
| User uploads market report PDF | Load this rule → Extract key information → Integrate into corresponding step |

### Source Document Identification

After parsing is complete, if the file is identified as a "source document" (PRD, spec, etc.), automatically mark it:

```
📎 Source document detected — final output will be an incremental update based on this file.
  Document structure: {section_count} sections, {table_count} tables
  Format conventions: [identified formatting characteristics]
```

The document structure is recorded for use by `rules-export-document.md` during final output.
