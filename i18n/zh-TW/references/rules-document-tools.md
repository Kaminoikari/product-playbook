# 文件轉換工具依賴管理

> 首次觸發 `/export` 或 `/parse` 指令時載入。

## 依賴層級

| 層級 | 工具 | 用途 | 安裝方式 | 大小 |
|------|------|------|---------|------|
| **核心（零安裝）** | Claude Read tool (Vision) | PDF 語意解析 | 內建 | 0 |
| **核心（零安裝）** | Playwright MCP | PDF 渲染 | 內建 | 0 |
| **基礎** | pymupdf (fitz) | PDF 文字提取 + 圖片渲染 | `pip3 install --break-system-packages pymupdf` | ~23MB |
| **基礎** | pikepdf | PDF 書籤注入 + 元資料 | `pip3 install --break-system-packages pikepdf` | ~5MB |
| **擴充** | pandoc | DOCX / PPTX 轉換 | `brew install pandoc` | ~50MB |
| **Fallback** | tesseract + chi_tra | 離線 OCR（Vision 不可用時） | `brew install tesseract tesseract-lang` | ~150MB |
| **進階** | python-docx | 高品質 DOCX 產出 | `pip3 install --break-system-packages python-docx` | ~5MB |

## 啟動檢測流程

當使用者首次觸發文件轉換功能時，依以下順序檢測並按需安裝：

### 步驟 1：判斷需要哪些工具

| 使用者操作 | 需要的工具 |
|-----------|-----------|
| `/export pdf` | pymupdf + pikepdf + Playwright MCP |
| `/export docx` 或 `/export pptx` | pandoc |
| `/parse [PDF 檔案]` | pymupdf（+ Claude Vision 或 tesseract） |
| `/parse [DOCX/PPTX 檔案]` | pandoc |

### 步驟 2：檢測已安裝的工具

執行以下 Bash 指令（靜默檢測，不顯示輸出）：

```bash
# pymupdf
python3 -c "import fitz; print(fitz.version)" 2>/dev/null && echo "pymupdf: OK" || echo "pymupdf: MISSING"

# pikepdf
python3 -c "import pikepdf; print(pikepdf.__version__)" 2>/dev/null && echo "pikepdf: OK" || echo "pikepdf: MISSING"

# pandoc
which pandoc >/dev/null 2>&1 && echo "pandoc: OK" || echo "pandoc: MISSING"

# tesseract（僅在明確需要時檢測）
which tesseract >/dev/null 2>&1 && tesseract --list-langs 2>&1 | grep -q chi_tra && echo "tesseract: OK" || echo "tesseract: MISSING"
```

### 步驟 3：自動安裝缺少的工具

若檢測到缺少的工具，顯示以下訊息並自動安裝：

```
📦 文件轉換需要安裝以下工具：
  ☐ [工具名稱]（[用途]，[大小]）
  ...
正在安裝，請稍候...
```

安裝指令依序執行：

```bash
# pymupdf + pikepdf（一次安裝）
pip3 install --break-system-packages pymupdf pikepdf

# pandoc
brew install pandoc

# tesseract（僅在需要離線 OCR 時）
brew install tesseract tesseract-lang
```

安裝完成後顯示：
```
✅ 工具安裝完成，繼續執行...
```

### 步驟 4：檢測 Playwright MCP

Playwright MCP 是 PDF 渲染的核心依賴。檢測方式：

1. 嘗試呼叫 `mcp__plugin_playwright_playwright__browser_run_code`
2. 若 MCP 可用 → 正常使用
3. 若 MCP 不可用（未連線）→ 顯示：

```
⚠️ Playwright MCP 未連線。PDF 渲染需要 Playwright 瀏覽器。
請執行以下操作之一：
  1. 啟動 Playwright MCP（推薦）
  2. 或輸入 ! npx playwright install chromium 安裝本地 Chromium
```

**Playwright Fallback**（MCP 不可用時）：

若使用者安裝了本地 Chromium，改用 Bash 執行 Node.js 腳本進行 PDF 渲染：
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

## 工具狀態快取

首次檢測結果記錄在記憶中（避免每次重複檢測）：
- 在同一個對話 session 中，已確認安裝的工具不再重複檢測
- 若安裝失敗，記錄錯誤訊息，下次觸發時重試

## 平台相容性

| 平台 | pymupdf | pikepdf | pandoc | tesseract | Playwright |
|------|---------|---------|--------|-----------|------------|
| macOS (Homebrew) | ✅ pip3 | ✅ pip3 | ✅ brew | ✅ brew | ✅ MCP/npx |
| Linux (apt) | ✅ pip3 | ✅ pip3 | ✅ apt | ✅ apt | ✅ MCP/npx |
| Windows (WSL) | ✅ pip3 | ✅ pip3 | ✅ choco | ✅ choco | ✅ MCP/npx |

根據使用者的作業系統自動選擇對應的套件管理器。偵測方式：
```bash
[[ "$(uname)" == "Darwin" ]] && echo "macOS" || echo "Linux"
```
