---
name: document-export
description: Use when the user wants the plan rendered as an interactive HTML report or exported to PDF/DOCX/PPTX. Triggers on 'HTML report', 'export to PDF', 'export document', 'downloadable report', 'PDF/DOCX/PPTX', and the same intent in any language.
---

# Document Export

Detect the user's language and reply in it; the framework below is authored in English.

**Provenance:** when you produce an HTML report or a PDF/DOCX/PPTX export, contribute the framework tags `HTML Report` and `PDF Export` to the meta-skill's provenance line (`— Frameworks: … · HTML Report · PDF Export · …`).

## Framework

<!-- migrated from references/06-html-report.md (whole file, lines 1-128) + references/rules-export-document.md (whole file, lines 1-346); the CSS read-paths are updated to the bundled assets/ paths so the skill reads its own bundled assets -->

# HTML Product Planning Report Output

Triggered when the user says "produce a report" or confirms the last stage content is correct.

## Design Specifications

Use a **modern design style** — a single HTML file (CSS and JS fully inlined), ensuring it's readable offline.

**Overall Style:**
- Gradient background Hero section (with mode, audience, date labels)
- Card-based layout (rounded corners + shadows), each section like an independent information card
- Clear typography hierarchy and comfortable reading spacing
- Responsive design, smooth reading on mobile

**Color Scheme:**
- Primary: Deep blue `#1a1a2e` → `#16213e` → `#0f3460`
- Accent: `#e94560` or `#533483`
- Content area background: `#f8f9fa`, cards: white with `box-shadow`

**Font:** Load Inter from Google Fonts CDN first, fall back to system fonts:
```css
/* In <head> */
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">

/* In CSS */
font-family: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
```
> This is the only permitted external CDN dependency. If Google Fonts is unavailable, the page will still render correctly.

## Page Structure (Dynamically rendered based on completed stages)

```
┌──────────────────────────────────────────────────────────────┐
│  Hero Section (Product name, one-liner, mode, audience, date)│
├──────────────────────────────────────────────────────────────┤
│  Table of Contents Navigation (Sticky, only shows completed) │
├──────────────────────────────────────────────────────────────┤
│  🧭 Strategy Section (if completed)                          │
│     ├─ Strategy Blocks hierarchy diagram                     │
│     ├─ Rumelt's Kernel of Good Strategy (Diagnosis/Policy/   │
│     │  Actions)                                              │
│     └─ Shreyas' Three Levels of Product Work                 │
│  ✅ Opportunity Check Section (if completed)                  │
│  🔍 Discovery Section (if completed)                          │
│     ├─ Persona Table (card-style table)                      │
│     ├─ Persona Cards (one per persona)                       │
│     ├─ JTBD Analysis Table (four types)                      │
│     ├─ Opportunity Solution Tree (visual tree)               │
│     └─ User Journey Map (overview + accordion detail)        │
│  🎯 Define Section (if completed)                            │
│     ├─ Pain Point Summary Table                              │
│     ├─ April Dunford Positioning Framework Card              │
│     ├─ HMW Question Cards (with JTBD type tags)             │
│     └─ Opportunity Assessment Table (opportunity cost view)  │
│  💡 Develop Section (if completed)                           │
│     ├─ PR-FAQ Card (simulated press release format)          │
│     ├─ Solution Ideation (three-column parallel cards)       │
│     ├─ Pre-mortem Risk Table (color-coded High/Med risk)     │
│     ├─ GEM Matrix + Impact/Effort Quadrant Chart             │
│     ├─ RICE Prioritization Table (if completed)              │
│     ├─ User Story Table (if completed)                       │
│     └─ MVP Scope (three-column cards + Not Doing List)       │
│  🚀 Deliver Section (if completed)                           │
│     ├─ Aha Moment Definition Card (prominently displayed)    │
│     ├─ North Star Metric Card                                │
│     ├─ Three-Layer Signal Metrics Table                      │
│     ├─ PMF Level Assessment (four-level visual + current     │
│     │  position marker)                                      │
│     ├─ GTM Strategy (channel selection + first 100 users     │
│     │  plan, if completed)                                   │
│     ├─ Business Model & Pricing (revenue model + pricing     │
│     │  strategy, if completed)                               │
│     ├─ Hypothesis Validation Plan Table (if completed)       │
│     └─ Product Spec Summary (three-section structure:        │
│        Decision Summary / Execution Boundaries / Deep Ref)   │
│  ⭐ Best Entry Point Analysis (full logic chain visual)       │
├──────────────────────────────────────────────────────────────┤
│  Footer: Output date + mode + framework attribution          │
└──────────────────────────────────────────────────────────────┘
```

## Section Design Details

**Table Styling:** Zebra stripes, dark header, rounded corners, hover highlight

**Persona Cards:** One card per Persona, pain points with red left border, JTBD emphasized with blue/purple color blocks

**Opportunity Solution Tree:** Use CSS or lightweight SVG to draw the tree structure, clearly showing the Goal → Opportunity → Solution hierarchy

**PMF Level Chart:** Use a progress bar or step diagram showing four levels, marking the user's current position

**PR-FAQ Card:** Simulated press release format with headline, subtitle, lead paragraph — visually resembling a real document

**Pre-mortem Risk Table:** High-risk items in red alert, medium-risk in yellow

**Best Entry Point Logic Chain:** Visualize the full reasoning chain, each node as a small card, connected by arrows

## Interactive Effects

- `scroll-behavior: smooth` — Smooth scrolling on TOC click
- Intersection Observer — Highlight current section in TOC while scrolling
- Card hover micro-lift (`transform: translateY(-2px)` + `transition`)
- Accordion expand/collapse (User Journey Map stages, `<details>/<summary>`)
- `@media print` — Hide interactive elements when printing, ensure tables aren't truncated

## Important Notes

- All CSS and JS inlined in HTML — no external dependencies except Google Fonts CDN for Inter
- If a stage was not completed, don't render an empty section — just skip it
- The Hero section displays the "Mode" and "Audience" so readers immediately understand the document's context
- The page can be very long — TOC navigation is critical for quick jumping

## Framework Attribution & Further Reading (in footer)

| Thinker | Key Contribution | Source |
|---------|-----------------|--------|
| Teresa Torres | Continuous Discovery, Opportunity Solution Tree | Lenny's Podcast + *Continuous Discovery Habits* |
| Shreyas Doshi | LNO Framework, Pre-mortem, Three Levels of Product Work, Opportunity Cost Thinking | Lenny's Podcast Ep.3 |
| Gibson Biddle | DHM Model, GEM Prioritization | Lenny's Podcast |
| April Dunford | Positioning Framework | Lenny's Podcast + *Obviously Awesome* |
| Todd Jackson | Four-Level PMF Framework, Four P's | Lenny's Podcast (First Round Capital) |
| Richard Rumelt | Good Strategy / Bad Strategy, Kernel of Good Strategy | Lenny's Podcast + *Good Strategy Bad Strategy* |
| Marty Cagan | Empowered Teams, Product Discovery | Lenny's Podcast + *Inspired*, *Empowered* |
| Chandra Janakiraman | Strategy Blocks | Lenny's Newsletter (Headspace / Meta) |
| Clayton Christensen | Jobs to Be Done | *Competing Against Luck* |
| Amazon | Working Backwards / PR-FAQ | *Working Backwards* |
| Sean Ellis | Sean Ellis Score, ICE Scoring | *Hacking Growth* |
| Lenny Rachitsky | Shape / Ship / Synchronize, North Star Thinking | Lenny's Newsletter + Podcast |

# Multi-Format Document Export Rules

> Loaded when the user triggers `/export [format]` or selects an export format after the flow ends.
> On first use, load `rules-document-tools.md` first to confirm tools are installed.

## Supported Export Formats

| Format | Command | Conversion Path | Tools |
|--------|---------|----------------|-------|
| PDF | `/export pdf` | HTML+CSS → Playwright → pikepdf bookmarks | Playwright MCP + pikepdf |
| DOCX | `/export docx` | MD → Pandoc | pandoc + reference.docx |
| PPTX | `/export pptx` | MD → Pandoc | pandoc |
| HTML | `/export html` | Existing `06-html-report.md` rules | Built-in |
| Markdown | `/export md` | Direct output | Built-in |

---

## PDF Export (Core Flow)

### Path Selection

PDF export has two paths, automatically selected based on source content:

| Source | Path | Reason |
|--------|------|--------|
| Planning output direct export (PRD / incremental update / spec) | **Path A: setContent** | No external JS dependencies, all resources can be inlined |
| HTML planning report to PDF (with Mermaid diagrams / CDN fonts) | **Path B: HTTP Server** | Needs to load external JS (mermaid.js) and CDN fonts |

### Path A: Standalone Document → PDF (setContent)

Applicable to: PRD, feature extension incremental updates, specs, any content without external JS.

**Step 1: Generate HTML Content**

Claude reads `assets/prd-style.css` and generates a complete HTML document:

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<style>
/* Read the full contents of assets/prd-style.css and inline here */
</style>
</head>
<body>

<!-- Cover page -->
<div class="cover-page">
  <h1>[Document Title]</h1>
  <div class="subtitle">[Subtitle or one-line description]</div>
  <div class="version-badge">[Version Number]</div>
  <div class="meta-info">
    <strong>PM</strong> [PM Name]<br>
    <strong>Date</strong> [ISO Date]<br>
    <strong>Status</strong> [Status]
  </div>
</div>

<!-- Legend (only for incremental update documents) -->
<div class="diff-legend">
  <div class="diff-legend-item"><div class="diff-legend-swatch swatch-new"></div> New in this version</div>
  <div class="diff-legend-item"><div class="diff-legend-swatch swatch-upd"></div> Modified in this version</div>
  <div class="diff-legend-item"><div class="diff-legend-swatch swatch-unchanged"></div> Unchanged</div>
</div>

<!-- Table of Contents page -->
<div class="toc-page">
  <h2>Table of Contents</h2>
  <ul class="toc">
    <!-- Claude auto-generates TOC items based on h2 headings -->
    <li>
      <span class="toc-title">[Section Name]</span>
      <span class="toc-dots"></span>
      <span class="toc-page-num">[Page Number]</span>
    </li>
  </ul>
</div>

<!-- Body content -->
[Body HTML]

<!-- Footer -->
<div class="doc-footer">
  [Document Code] [Version] ｜ [Date] ｜ Generated by Product Playbook
</div>

</body>
</html>
```

**Important**:
- CSS must be fully inlined (no external links)
- Fonts use system fonts: `"PingFang TC", "Noto Sans TC", system-ui` (Playwright will automatically embed in PDF)
- No `<script>` tags or external resource references
- TOC page numbers are estimates (may need fine-tuning after PDF generation)

**Step 2: Playwright Renders PDF**

Save the HTML content to `/tmp/export-{timestamp}.html`, then call Playwright MCP:

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

> Note: If the HTML content is too large (>500KB), setContent may time out. In that case, switch to Path B (HTTP Server).

**Step 3: pikepdf Bookmark Injection**

```python
import pikepdf, re

pdf = pikepdf.open('{output_path}')

# Extract h2 headings from HTML as bookmarks
# Claude should record the estimated page number for each h2 when generating HTML
bookmarks = [
    # (title, page index 0-based)
    ("Revision History", 2),
    ("User Story", 4),
    ("Development Architecture", 6),
    # ... generated based on actual content
]

with pdf.open_outline() as outline:
    for title, page_idx in bookmarks:
        page_idx = min(page_idx, len(pdf.pages) - 1)
        outline.root.append(
            pikepdf.OutlineItem(title, page_idx)
        )

# Set PDF metadata
with pdf.open_metadata() as meta:
    meta['dc:title'] = '[Document Title]'
    meta['dc:creator'] = ['[PM Name]']
    meta['pdf:Producer'] = 'Product Playbook + Playwright'

pdf.save('{output_path}')
```

**Step 4: Notify User**

```
✅ PDF exported to: {output_path}
  📄 {page_count} pages ｜ {file_size}
  📑 Includes bookmark navigation ({bookmark_count} sections)
```

### Path B: HTML Report → PDF (HTTP Server)

Applicable to: HTML reports with Mermaid diagrams, CDN fonts, interactive elements.

**Step 1: HTML Report Already Generated**

The HTML report is generated by `06-html-report.md` rules and saved as `/tmp/report-{timestamp}.html`.

**Step 2: Start HTTP Server**

```bash
cd /tmp && python3 -m http.server 18899 &
echo $!  # Record PID
```

**Step 3: Playwright Rendering**

```javascript
// mcp__plugin_playwright_playwright__browser_run_code
async (page) => {
  await page.goto('http://localhost:18899/report-{timestamp}.html', {
    waitUntil: 'networkidle',
    timeout: 30000
  });
  // Wait for Mermaid chart rendering to complete
  await page.waitForTimeout(3000);
  // Expand all accordion (<details>) elements
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

**Step 4: Shut Down HTTP Server + pikepdf Bookmarks**

```bash
kill {SERVER_PID}
```

Then perform the same pikepdf bookmark injection step as Path A.

### Playwright MCP Unavailable Fallback

If Playwright MCP is not connected, use Node.js directly:

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

## DOCX Export

### Step 1: Generate Markdown

Claude organizes the planning output into clean Markdown format and saves it as `/tmp/export-{timestamp}.md`.

### Step 2: Pandoc Conversion

```bash
pandoc /tmp/export-{timestamp}.md \
  -o "{output_path}" \
  --from markdown \
  --to docx \
  --reference-doc="reference.docx" \
  --toc \
  --toc-depth=2
```

If no reference.docx template is available, omit the `--reference-doc` parameter (uses Pandoc default styles).

### Step 3: Notify User

```
✅ Word document exported to: {output_path}
  📄 Includes table of contents ｜ {file_size}
```

---

## PPTX Export

```bash
pandoc /tmp/export-{timestamp}.md \
  -o "{output_path}" \
  --from markdown \
  --to pptx \
  --slide-level=2
```

> Tip: Pandoc PPTX quality is limited. It's recommended to use the PPTX as an outline, then polish it with PowerPoint/Keynote.

---

## Special Handling for Incremental Update Documents

When exporting Feature Extension or Revision mode incremental update documents:

### Diff Visual Marking Rules

1. **Paragraphs marked `[NEW]`**:
   - Use `<span class="new">NEW</span>` marker
   - Table rows get `class="new-row"`
   - Paragraphs get `class="diff-added"`

2. **Paragraphs marked `[UPDATED]`**:
   - Use `<span class="upd">UPDATED</span>` marker
   - Table rows get `class="upd-row"`
   - If original content exists, original content gets `class="diff-removed"`, new content gets `class="diff-added"`

3. **Unchanged paragraphs**: Display normally, no special markers

4. **Legend at document start**:
```html
<div class="diff-legend">
  <div class="diff-legend-item">
    <div class="diff-legend-swatch swatch-new"></div> New in this version
  </div>
  <div class="diff-legend-item">
    <div class="diff-legend-swatch swatch-upd"></div> Modified in this version
  </div>
  <div class="diff-legend-item">
    <div class="diff-legend-swatch swatch-unchanged"></div> No marker = Unchanged
  </div>
</div>
```

---

## Output Path Rules

Default output to `~/Downloads/`, filename format:

```
[Document Code] [Document Title] [Version].{ext}

Examples:
[D-221] Virtual Account v1.0.14 Full Merged Version.pdf
Product Planning Report - UPASS Virtual Account.docx
```

If the user specifies a path, use the user-specified path.

---

## Quality Checklist

Before export, Claude self-checks:

- [ ] No residual Markdown syntax in HTML (`**`, `##`, `|---|`)
- [ ] All table row and column counts match the original content
- [ ] `[NEW]` / `[UPDATED]` markers correctly mapped to corresponding CSS classes
- [ ] Cover page information (title, version, PM, date) is correct
- [ ] TOC items match the body h2 headings
- [ ] CSS is fully inlined (Path A) or CDN is accessible (Path B)
- [ ] Bookmark count matches h2 heading count
