# 文件导入解析规则

> 使用者上传 PDF / DOCX / PPTX 文件，或触发 `/parse [file]` 时载入。
> 首次使用时先载入 `rules-document-tools.md` 确认工具已安装。
> 本规则与 `rules-file-integration.md` 搭配使用——该文件定义「何时触发」，本文件定义「如何解析」。

---

## 解析目标

将任何格式的输入文件转换为**结构化 Markdown**，供后续流程使用：
- Feature Extension / Revision 模式的 S1 上下文收集
- 增量更新的原始文件基底
- 一般性的文件内容提取

---

## PDF 解析：三层策略 + 逐页检测

### 总览

```
输入 PDF
  │
  ▼
pymupdf 逐页文字提取（零成本）
  │
  ├── 该页文字 > 30 字符 → ✅ 直接转 Markdown（层 1）
  │
  └── 该页文字 ≤ 30 字符（空白 / 向量路径 / 扫描件）
        │
        ├── 预设 → Claude Vision 语意解析（层 2）
        │
        └── Vision 不可用 / Token 预算不足 → Tesseract OCR（层 3）
```

### 步骤 1：逐页类型检测

**关键原则**：以「页」为单位检测，而非整份文件。一份 PDF 可能混合数位文字页和扫描图片页。

```python
import fitz  # pymupdf

doc = fitz.open(pdf_path)
total_pages = len(doc)
page_results = {}

for i in range(total_pages):
    page = doc[i]
    text = page.get_text("text").strip()

    if len(text) > 30:
        # 层 1：数位文字，直接提取
        page_results[i] = {"type": "digital", "text": text}
    else:
        # 需要 Vision 或 OCR
        page_results[i] = {"type": "needs_vision", "text": None}

digital_count = sum(1 for p in page_results.values() if p["type"] == "digital")
vision_count = total_pages - digital_count

print(f"PDF 分析：{total_pages} 页，{digital_count} 页可直接提取，{vision_count} 页需视觉解析")
```

### 步骤 2：大文件处理策略

| 条件 | 策略 |
|------|------|
| 全部页面为 digital（vision_count = 0）| 直接提取所有页面，零成本 |
| vision_count ≤ 20 | 一次用 Claude Vision 读取所有需视觉解析的页面 |
| vision_count > 20 | 分批处理（每批 ≤ 20 页），合并结果 |
| 总页数 > 50 且 vision_count > 20 | 询问使用者是否全文解析或指定页面范围 |

**大文件（>50 页）的使用者确认提示**：

```
📄 此 PDF 共 {total_pages} 页：
  • {digital_count} 页可直接提取文字（免费）
  • {vision_count} 页需要视觉解析（消耗 Vision Token）

请选择：
  1️⃣ 全文解析（完整但消耗较多 Token）
  2️⃣ 只解析特定页面（请输入页码范围，如 1-10,15,20-25）
  3️⃣ 只提取可直接提取的页面（跳过扫描/向量页面）
```

### 步骤 3：层 1 — pymupdf 直接提取

```python
def extract_digital_pages(doc, page_results):
    """提取所有数位文字页面"""
    markdown_parts = []
    for i, result in sorted(page_results.items()):
        if result["type"] == "digital":
            markdown_parts.append(f"<!-- Page {i+1} -->\n{result['text']}")
    return "\n\n".join(markdown_parts)
```

### 步骤 4：层 2 — Claude Vision 语意解析

对于 `needs_vision` 类型的页面，先用 pymupdf 渲染为 PNG 图片，再用 Claude 的 Read 工具读取。

**渲染为图片**：
```python
def render_pages_to_png(doc, page_indices, dpi=300):
    """将指定页面渲染为 PNG"""
    output_files = []
    for i in page_indices:
        page = doc[i]
        pix = page.get_pixmap(dpi=dpi)
        output_path = f"/tmp/pdf-page-{i+1:04d}.png"
        pix.save(output_path)
        output_files.append((i, output_path))
    return output_files
```

**Claude Vision 解析 Prompt**：

对每个需要视觉解析的页面（或批次），使用 Read 工具读取 PNG 后，依以下 prompt 转换：

```
你正在阅读一份 PDF 文件的第 {page_num}/{total_pages} 页。
请将此页面的内容精确转换为 Markdown 格式。

严格规则：
1. 表格 → Markdown table（保留所有栏位、行数、对齐方式）
2. 标题 → # / ## / ### 对应原始层级
3. 编号清单 → 1. 2. 3.（保留原始编号）
4. 项目符号 → - 或 •
5. 粗体/斜体 → **粗体** / *斜体*
6. 图表/图片 → > [图表：简述内容]
7. 页首、页尾、页码 → 忽略
8. 数字、日期、人名、帐号 → 必须 100% 精确，不得猜测
9. 不要添加原文没有的内容
10. 不要翻译——保留原文语言
```

> **为什么这比 OCR 强**：Claude 理解表格的「语意结构」（第一行是表头、哪些栏位对齐），而 Tesseract 只能逐字符辨识后用规则重建表格，经常失败。

### 步骤 5：层 3 — Tesseract OCR Fallback

仅在以下情况使用：
- 使用者明确要求节省 Token
- Claude Vision 不可用（API 限制等）
- 离线环境

```python
import subprocess
from PIL import Image

def ocr_page(png_path, lang="chi_tra+eng"):
    """Tesseract OCR 单页"""
    # macOS 的 tesseract 可能无法直接读取 PNG，需先转 TIFF 或用 stdin
    tiff_path = png_path.replace('.png', '.tiff')
    Image.open(png_path).save(tiff_path)

    result = subprocess.run(
        ['tesseract', 'stdin', 'stdout', '-l', lang],
        stdin=open(tiff_path, 'rb'),
        capture_output=True, text=True, timeout=120
    )
    return result.stdout
```

**Tesseract 注意事项（实战经验）**：
- macOS 上 tesseract 可能无法直接读取 PNG 文件，需用 `stdin` 管道或先转 TIFF
- 建议解析度 300dpi
- `chi_tra+eng` 语言包同时辨识繁体中文和英文
- OCR 结果需后处理：合并断行、修复表格结构

### 步骤 6：合并所有页面

```python
def merge_all_pages(digital_md, vision_md_list):
    """按页序合并所有页面的 Markdown"""
    all_pages = {}
    # digital pages
    for page_num, md in digital_md.items():
        all_pages[page_num] = md
    # vision/ocr pages
    for page_num, md in vision_md_list.items():
        all_pages[page_num] = md

    # 按页码排序，合并
    final_md = []
    for i in sorted(all_pages.keys()):
        final_md.append(all_pages[i])

    return "\n\n---\n\n".join(final_md)
```

### 步骤 7：输出并告知使用者

```
📄 PDF 解析完成：
  • 总页数：{total_pages}
  • 直接提取：{digital_count} 页（pymupdf）
  • 视觉解析：{vision_count} 页（Claude Vision）
  • 输出：{output_path}（Markdown，{字数} 字）
```

---

## DOCX 解析

```bash
pandoc "{input_path}" -t markdown -o "/tmp/parsed-{timestamp}.md" --wrap=none
```

**后处理**：
- 移除 Pandoc 产生的多余空行
- 确认表格格式正确

---

## PPTX 解析

```bash
pandoc "{input_path}" -t markdown -o "/tmp/parsed-{timestamp}.md" --wrap=none
```

> Pandoc 会将每张投影片转为一个 `##` 标题区段。

---

## HTML 解析

```bash
pandoc "{input_path}" -f html -t markdown -o "/tmp/parsed-{timestamp}.md" --wrap=none
```

---

## 图片解析

直接使用 Claude Read 工具读取图片，然后依照 Vision 解析 Prompt 转换为 Markdown。

---

## 与 rules-file-integration.md 的协作

当 `rules-file-integration.md` 检测到以下场景时，载入本规则：

| 场景 | 动作 |
|------|------|
| 使用者在 Feature Extension S1 上传 PDF | 载入本规则 → 解析 PDF → 提取既有系统背景 |
| 使用者在 Revision S1 上传旧版 PRD | 载入本规则 → 解析 PDF → 作为改版基底 |
| 使用者用 `/parse` 指令 | 载入本规则 → 解析指定文件 → 输出 Markdown |
| 使用者上传市场报告 PDF | 载入本规则 → 提取关键资讯 → 整合到对应步骤 |

### 原始文件识别

解析完成后，若判断该文件是「原始文件」（PRD、规格书等），自动标记：

```
📎 检测到原始文件——最终产出将基于此文件进行增量更新。
  文件结构：{章节数} 个章节，{表格数} 个表格
  格式惯例：[识别到的格式特征]
```

并将文件结构记录，供 `rules-export-document.md` 在最终产出时使用。
