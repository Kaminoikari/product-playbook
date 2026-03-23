# 📎 File Integration Guide

> Loaded when the user uploads supplementary materials.

## Directly Supported File Types

| File Type | Common Scenarios | Integration Method |
|-----------|-----------------|-------------------|
| **Images** | Competitor screenshots, whiteboard photos, hand-drawn journey maps, app interface screenshots, data report screenshots | Recognize content and integrate into the corresponding step |
| **PDF** | Market reports, internal documents, user research reports, legacy PRDs | Load `rules-import-document.md` for three-layer parsing (pymupdf direct extraction → Claude Vision semantic parsing → Tesseract fallback). On first use, load `rules-document-tools.md` to check tools. |
| **CSV / Excel** | User behavior data, retention data, NPS survey results, sales data | Analyze data and use for quantitative assessment |
| **Text files** | Interview transcripts, existing requirements documents, meeting notes | Extract Persona clues, pain points, JTBD evidence |
| **DOCX** | Existing PRDs, product spec documents, user research reports | Load `rules-import-document.md`, use Pandoc to convert to Markdown then integrate. On first use, load `rules-document-tools.md` to check tools. |
| **PPTX** | Existing presentations, product intro slides | Load `rules-import-document.md`, use Pandoc to convert to Markdown then integrate. |

## Not Directly Supported but Guidance Available

| File Type | Guidance |
|-----------|----------|
| **Video** | Ask the user to describe key scenes, or provide a transcript/subtitle file |
| **Figma / Sketch** | Ask the user to take screenshots and upload them |
| **Protobuf / Swagger** | Ask the user to export as JSON or text format |

## File → Step Auto-Mapping Table

| Uploaded Content | Auto-Mapped Step | Integration Action |
|-----------------|-----------------|-------------------|
| Competitor app / website screenshots | Positioning | Identify as "competitive alternatives," analyze differentiation |
| Whiteboard hand-drawn flowchart | Journey Map / OST | Recognize the flow and convert into a structured table |
| User interview transcript | Persona + JTBD | Extract pain points, current workarounds, emotional reactions, Job statements |
| User behavior data (CSV) | Opportunity Assessment + North Star + PMF | Replace assumption-based scores with real data |
| NPS / satisfaction survey | PMF + Sean Ellis Score | Directly calculate the Score; determine PMF level |
| Existing PRD / requirements document | Revision Mode S1 + MVP | Extract existing feature list and decision history |
| Market report PDF | Opportunity Assessment + Strategy | Extract market size, trends, competitive landscape |
| Sales data | Business Model + GTM | Analyze revenue structure, customer distribution, channel effectiveness |
| App interface screenshots | Aha Moment + Journey | Analyze the current experience path |

## Integration Rules

1. **Proactive identification**: First explain "I see you uploaded [file type]. I will integrate the [key information] from it into [step name]."
2. **Do not overwrite existing output**: Mark the uploaded content as "supplementary material," update the output, and trigger the change propagation rules
3. **Mark the source**: Annotate in the output which content came from the uploaded file (e.g., "✦ From the uploaded user research report")
4. **Data takes priority**: When real data conflicts with previous assumptions, defer to the real data
5. **Cross-step impact**: A single file may affect multiple steps — list all affected steps at once

## 📎 Source Document Identification & Incremental Update

When a user uploads a file during **Feature Extension** or **Revision Mode**, determine if it is a "source document" (a document that should be incrementally updated with the new planning output):

### Identification Criteria
- File type: PRD, product spec, architecture doc, requirements doc, design doc
- User explicitly says: "this is our current PRD", "update this document", "build on this spec", etc.
- Uploaded during S1 (context collection) of Feature Extension or Revision Mode

### When a Source Document Is Identified
1. Mark it: "📎 Source document detected — final output will be an incremental update based on this file"
2. Parse the document structure (section headings, formatting conventions, naming patterns)
3. Record the document's format and style for consistent output
4. During S1, use the document to pre-fill existing system context (tech stack, modules, features)

### Incremental Output Rules (applied at Final Output stage)
- New content inserted into the appropriate sections, marked with `[NEW]`
- Modified content marked with `[UPDATED]`, original content preserved as comment
- Sections unrelated to the new feature remain untouched
- The output document maintains the original file's format, style, and naming conventions
