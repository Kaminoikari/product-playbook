# 文件转换工具依赖管理

> 首次触发 `/export` 或 `/parse` 指令时载入。

## 依赖层级

| 层级 | 工具 | 用途 | 安装方式 | 大小 |
|------|------|------|---------|------|
| **核心（零安装）** | Claude Read tool (Vision) | PDF 语意解析 | 内建 | 0 |
| **核心（零安装）** | Playwright MCP | PDF 渲染 | 内建 | 0 |
| **基础** | pymupdf (fitz) | PDF 文字提取 + 图片渲染 | `pip3 install --break-system-packages pymupdf` | ~23MB |
| **基础** | pikepdf | PDF 书签注入 + 元数据 | `pip3 install --break-system-packages pikepdf` | ~5MB |
| **扩充** | pandoc | DOCX / PPTX 转换 | `brew install pandoc` | ~50MB |
| **Fallback** | tesseract + chi_tra | 离线 OCR（Vision 不可用时） | `brew install tesseract tesseract-lang` | ~150MB |
| **进阶** | python-docx | 高品质 DOCX 产出 | `pip3 install --break-system-packages python-docx` | ~5MB |

## 启动检测流程

当使用者首次触发文件转换功能时，依以下顺序检测并按需安装：

### 步骤 1：判断需要哪些工具

| 使用者操作 | 需要的工具 |
|-----------|-----------|
| `/export pdf` | pymupdf + pikepdf + Playwright MCP |
| `/export docx` 或 `/export pptx` | pandoc |
| `/parse [PDF 文件]` | pymupdf（+ Claude Vision 或 tesseract） |
| `/parse [DOCX/PPTX 文件]` | pandoc |

### 步骤 2：检测已安装的工具

执行以下 Bash 指令（静默检测，不显示输出）：

```bash
# pymupdf
python3 -c "import fitz; print(fitz.version)" 2>/dev/null && echo "pymupdf: OK" || echo "pymupdf: MISSING"

# pikepdf
python3 -c "import pikepdf; print(pikepdf.__version__)" 2>/dev/null && echo "pikepdf: OK" || echo "pikepdf: MISSING"

# pandoc
which pandoc >/dev/null 2>&1 && echo "pandoc: OK" || echo "pandoc: MISSING"

# tesseract（仅在明确需要时检测）
which tesseract >/dev/null 2>&1 && tesseract --list-langs 2>&1 | grep -q chi_tra && echo "tesseract: OK" || echo "tesseract: MISSING"
```

### 步骤 3：自动安装缺少的工具

若检测到缺少的工具，显示以下讯息并自动安装：

```
📦 文件转换需要安装以下工具：
  ☐ [工具名称]（[用途]，[大小]）
  ...
正在安装，请稍候...
```

安装指令依序执行：

```bash
# pymupdf + pikepdf（一次安装）
pip3 install --break-system-packages pymupdf pikepdf

# pandoc
brew install pandoc

# tesseract（仅在需要离线 OCR 时）
brew install tesseract tesseract-lang
```

安装完成后显示：
```
✅ 工具安装完成，继续执行...
```

### 步骤 4：检测 Playwright MCP

Playwright MCP 是 PDF 渲染的核心依赖。检测方式：

1. 尝试呼叫 `mcp__plugin_playwright_playwright__browser_run_code`
2. 若 MCP 可用 → 正常使用
3. 若 MCP 不可用（未连线）→ 显示：

```
⚠️ Playwright MCP 未连线。PDF 渲染需要 Playwright 浏览器。
请执行以下操作之一：
  1. 启动 Playwright MCP（推荐）
  2. 或输入 ! npx playwright install chromium 安装本地 Chromium
```

**Playwright Fallback**（MCP 不可用时）：

若使用者安装了本地 Chromium，改用 Bash 执行 Node.js 脚本进行 PDF 渲染：
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

## 工具状态缓存

首次检测结果记录在记忆中（避免每次重复检测）：
- 在同一个对话 session 中，已确认安装的工具不再重复检测
- 若安装失败，记录错误讯息，下次触发时重试

## 平台兼容性

| 平台 | pymupdf | pikepdf | pandoc | tesseract | Playwright |
|------|---------|---------|--------|-----------|------------|
| macOS (Homebrew) | ✅ pip3 | ✅ pip3 | ✅ brew | ✅ brew | ✅ MCP/npx |
| Linux (apt) | ✅ pip3 | ✅ pip3 | ✅ apt | ✅ apt | ✅ MCP/npx |
| Windows (WSL) | ✅ pip3 | ✅ pip3 | ✅ choco | ✅ choco | ✅ MCP/npx |

根据使用者的操作系统自动选择对应的包管理器。检测方式：
```bash
[[ "$(uname)" == "Darwin" ]] && echo "macOS" || echo "Linux"
```
