# 文件匯入解析規則

> 使用者上傳 PDF / DOCX / PPTX 檔案，或觸發 `/parse [file]` 時載入。
> 首次使用時先載入 `rules-document-tools.md` 確認工具已安裝。
> 本規則與 `rules-file-integration.md` 搭配使用——該檔定義「何時觸發」，本檔定義「如何解析」。

---

## 解析目標

將任何格式的輸入文件轉換為**結構化 Markdown**，供後續流程使用：
- Feature Extension / Revision 模式的 S1 情境蒐集
- 增量更新的原始文件基底
- 一般性的文件內容提取

---

## PDF 解析：三層策略 + 逐頁檢測

### 總覽

```
輸入 PDF
  │
  ▼
pymupdf 逐頁文字提取（零成本）
  │
  ├── 該頁文字 > 30 字元 → ✅ 直接轉 Markdown（層 1）
  │
  └── 該頁文字 ≤ 30 字元（空白 / 向量路徑 / 掃描件）
        │
        ├── 預設 → Claude Vision 語意解析（層 2）
        │
        └── Vision 不可用 / Token 預算不足 → Tesseract OCR（層 3）
```

### 步驟 1：逐頁類型檢測

**關鍵原則**：以「頁」為單位檢測，而非整份文件。一份 PDF 可能混合數位文字頁和掃描圖片頁。

```python
import fitz  # pymupdf

doc = fitz.open(pdf_path)
total_pages = len(doc)
page_results = {}

for i in range(total_pages):
    page = doc[i]
    text = page.get_text("text").strip()

    if len(text) > 30:
        # 層 1：數位文字，直接提取
        page_results[i] = {"type": "digital", "text": text}
    else:
        # 需要 Vision 或 OCR
        page_results[i] = {"type": "needs_vision", "text": None}

digital_count = sum(1 for p in page_results.values() if p["type"] == "digital")
vision_count = total_pages - digital_count

print(f"PDF 分析：{total_pages} 頁，{digital_count} 頁可直接提取，{vision_count} 頁需視覺解析")
```

### 步驟 2：大文件處理策略

| 條件 | 策略 |
|------|------|
| 全部頁面為 digital（vision_count = 0）| 直接提取所有頁面，零成本 |
| vision_count ≤ 20 | 一次用 Claude Vision 讀取所有需視覺解析的頁面 |
| vision_count > 20 | 分批處理（每批 ≤ 20 頁），合併結果 |
| 總頁數 > 50 且 vision_count > 20 | 詢問使用者是否全文解析或指定頁面範圍 |

**大文件（>50 頁）的使用者確認提示**：

```
📄 此 PDF 共 {total_pages} 頁：
  • {digital_count} 頁可直接提取文字（免費）
  • {vision_count} 頁需要視覺解析（消耗 Vision Token）

請選擇：
  1️⃣ 全文解析（完整但消耗較多 Token）
  2️⃣ 只解析特定頁面（請輸入頁碼範圍，如 1-10,15,20-25）
  3️⃣ 只提取可直接提取的頁面（跳過掃描/向量頁面）
```

### 步驟 3：層 1 — pymupdf 直接提取

```python
def extract_digital_pages(doc, page_results):
    """提取所有數位文字頁面"""
    markdown_parts = []
    for i, result in sorted(page_results.items()):
        if result["type"] == "digital":
            markdown_parts.append(f"<!-- Page {i+1} -->\n{result['text']}")
    return "\n\n".join(markdown_parts)
```

### 步驟 4：層 2 — Claude Vision 語意解析

對於 `needs_vision` 類型的頁面，先用 pymupdf 渲染為 PNG 圖片，再用 Claude 的 Read 工具讀取。

**渲染為圖片**：
```python
def render_pages_to_png(doc, page_indices, dpi=300):
    """將指定頁面渲染為 PNG"""
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

對每個需要視覺解析的頁面（或批次），使用 Read 工具讀取 PNG 後，依以下 prompt 轉換：

```
你正在閱讀一份 PDF 文件的第 {page_num}/{total_pages} 頁。
請將此頁面的內容精確轉換為 Markdown 格式。

嚴格規則：
1. 表格 → Markdown table（保留所有欄位、行數、對齊方式）
2. 標題 → # / ## / ### 對應原始層級
3. 編號清單 → 1. 2. 3.（保留原始編號）
4. 項目符號 → - 或 •
5. 粗體/斜體 → **粗體** / *斜體*
6. 圖表/圖片 → > [圖表：簡述內容]
7. 頁首、頁尾、頁碼 → 忽略
8. 數字、日期、人名、帳號 → 必須 100% 精確，不得猜測
9. 不要添加原文沒有的內容
10. 不要翻譯——保留原文語言
```

> **為什麼這比 OCR 強**：Claude 理解表格的「語意結構」（第一行是表頭、哪些欄位對齊），而 Tesseract 只能逐字元辨識後用規則重建表格，經常失敗。

### 步驟 5：層 3 — Tesseract OCR Fallback

僅在以下情況使用：
- 使用者明確要求節省 Token
- Claude Vision 不可用（API 限制等）
- 離線環境

```python
import subprocess
from PIL import Image

def ocr_page(png_path, lang="chi_tra+eng"):
    """Tesseract OCR 單頁"""
    # macOS 的 tesseract 可能無法直接讀取 PNG，需先轉 TIFF 或用 stdin
    tiff_path = png_path.replace('.png', '.tiff')
    Image.open(png_path).save(tiff_path)

    result = subprocess.run(
        ['tesseract', 'stdin', 'stdout', '-l', lang],
        stdin=open(tiff_path, 'rb'),
        capture_output=True, text=True, timeout=120
    )
    return result.stdout
```

**Tesseract 注意事項（實戰經驗）**：
- macOS 上 tesseract 可能無法直接讀取 PNG 檔案，需用 `stdin` 管道或先轉 TIFF
- 建議解析度 300dpi
- `chi_tra+eng` 語言包同時辨識繁體中文和英文
- OCR 結果需後處理：合併斷行、修復表格結構

### 步驟 6：合併所有頁面

```python
def merge_all_pages(digital_md, vision_md_list):
    """按頁序合併所有頁面的 Markdown"""
    all_pages = {}
    # digital pages
    for page_num, md in digital_md.items():
        all_pages[page_num] = md
    # vision/ocr pages
    for page_num, md in vision_md_list.items():
        all_pages[page_num] = md

    # 按頁碼排序，合併
    final_md = []
    for i in sorted(all_pages.keys()):
        final_md.append(all_pages[i])

    return "\n\n---\n\n".join(final_md)
```

### 步驟 7：輸出並告知使用者

```
📄 PDF 解析完成：
  • 總頁數：{total_pages}
  • 直接提取：{digital_count} 頁（pymupdf）
  • 視覺解析：{vision_count} 頁（Claude Vision）
  • 輸出：{output_path}（Markdown，{字數} 字）
```

---

## DOCX 解析

```bash
pandoc "{input_path}" -t markdown -o "/tmp/parsed-{timestamp}.md" --wrap=none
```

**後處理**：
- 移除 Pandoc 產生的多餘空行
- 確認表格格式正確

---

## PPTX 解析

```bash
pandoc "{input_path}" -t markdown -o "/tmp/parsed-{timestamp}.md" --wrap=none
```

> Pandoc 會將每張投影片轉為一個 `##` 標題區段。

---

## HTML 解析

```bash
pandoc "{input_path}" -f html -t markdown -o "/tmp/parsed-{timestamp}.md" --wrap=none
```

---

## 圖片解析

直接使用 Claude Read 工具讀取圖片，然後依照 Vision 解析 Prompt 轉換為 Markdown。

---

## 與 rules-file-integration.md 的協作

當 `rules-file-integration.md` 偵測到以下場景時，載入本規則：

| 場景 | 動作 |
|------|------|
| 使用者在 Feature Extension S1 上傳 PDF | 載入本規則 → 解析 PDF → 提取既有系統背景 |
| 使用者在 Revision S1 上傳舊版 PRD | 載入本規則 → 解析 PDF → 作為改版基底 |
| 使用者用 `/parse` 指令 | 載入本規則 → 解析指定檔案 → 輸出 Markdown |
| 使用者上傳市場報告 PDF | 載入本規則 → 提取關鍵資訊 → 整合到對應步驟 |

### 原始文件識別

解析完成後，若判斷該檔案是「原始文件」（PRD、規格書等），自動標記：

```
📎 偵測到原始文件——最終產出將基於此檔案進行增量更新。
  文件結構：{章節數} 個章節，{表格數} 個表格
  格式慣例：[識別到的格式特徵]
```

並將文件結構記錄，供 `rules-export-document.md` 在最終產出時使用。
