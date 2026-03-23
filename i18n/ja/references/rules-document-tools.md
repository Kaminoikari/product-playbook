# ドキュメント変換ツール依存管理

> `/export` または `/parse` コマンドが初めてトリガーされた時に読み込みます。

## 依存レイヤー

| レイヤー | ツール | 用途 | インストール方法 | サイズ |
|------|------|------|---------|------|
| **コア（インストール不要）** | Claude Read tool (Vision) | PDF セマンティック解析 | 内蔵 | 0 |
| **コア（インストール不要）** | Playwright MCP | PDF レンダリング | 内蔵 | 0 |
| **基本** | pymupdf (fitz) | PDF テキスト抽出 + 画像レンダリング | `pip3 install --break-system-packages pymupdf` | ~23MB |
| **基本** | pikepdf | PDF ブックマーク注入 + メタデータ | `pip3 install --break-system-packages pikepdf` | ~5MB |
| **拡張** | pandoc | DOCX / PPTX 変換 | `brew install pandoc` | ~50MB |
| **Fallback** | tesseract + chi_tra | オフライン OCR（Vision が利用不可の場合） | `brew install tesseract tesseract-lang` | ~150MB |
| **高度** | python-docx | 高品質 DOCX 出力 | `pip3 install --break-system-packages python-docx` | ~5MB |

## 起動検出フロー

ユーザーが初めてドキュメント変換機能をトリガーした際、以下の順序で検出し、必要に応じてインストールします：

### ステップ 1：必要なツールを判断

| ユーザー操作 | 必要なツール |
|-----------|-----------|
| `/export pdf` | pymupdf + pikepdf + Playwright MCP |
| `/export docx` または `/export pptx` | pandoc |
| `/parse [PDF ファイル]` | pymupdf（+ Claude Vision または tesseract） |
| `/parse [DOCX/PPTX ファイル]` | pandoc |

### ステップ 2：インストール済みツールを検出

以下の Bash コマンドを実行（サイレント検出、出力非表示）：

```bash
# pymupdf
python3 -c "import fitz; print(fitz.version)" 2>/dev/null && echo "pymupdf: OK" || echo "pymupdf: MISSING"

# pikepdf
python3 -c "import pikepdf; print(pikepdf.__version__)" 2>/dev/null && echo "pikepdf: OK" || echo "pikepdf: MISSING"

# pandoc
which pandoc >/dev/null 2>&1 && echo "pandoc: OK" || echo "pandoc: MISSING"

# tesseract（明示的に必要な場合のみ検出）
which tesseract >/dev/null 2>&1 && tesseract --list-langs 2>&1 | grep -q chi_tra && echo "tesseract: OK" || echo "tesseract: MISSING"
```

### ステップ 3：不足ツールを自動インストール

不足ツールが検出された場合、以下のメッセージを表示し自動インストール：

```
📦 ドキュメント変換に以下のツールのインストールが必要です：
  ☐ [ツール名]（[用途]、[サイズ]）
  ...
インストール中、お待ちください...
```

インストールコマンドを順次実行：

```bash
# pymupdf + pikepdf（一括インストール）
pip3 install --break-system-packages pymupdf pikepdf

# pandoc
brew install pandoc

# tesseract（オフライン OCR が必要な場合のみ）
brew install tesseract tesseract-lang
```

インストール完了後に表示：
```
✅ ツールのインストールが完了しました。処理を続行します...
```

### ステップ 4：Playwright MCP の検出

Playwright MCP は PDF レンダリングのコア依存です。検出方法：

1. `mcp__plugin_playwright_playwright__browser_run_code` の呼び出しを試行
2. MCP が利用可能 → 通常使用
3. MCP が利用不可（未接続）→ 以下を表示：

```
⚠️ Playwright MCP が接続されていません。PDF レンダリングには Playwright ブラウザが必要です。
以下のいずれかを実行してください：
  1. Playwright MCP を起動（推奨）
  2. または ! npx playwright install chromium を実行してローカル Chromium をインストール
```

**Playwright Fallback**（MCP が利用不可の場合）：

ユーザーがローカル Chromium をインストールした場合、Bash で Node.js スクリプトを実行して PDF レンダリング：
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

## ツール状態キャッシュ

初回検出結果をメモリに記録（毎回の重複検出を回避）：
- 同一会話セッション内で、インストール確認済みのツールは再検出しない
- インストール失敗の場合、エラーメッセージを記録し、次回トリガー時にリトライ

## プラットフォーム互換性

| プラットフォーム | pymupdf | pikepdf | pandoc | tesseract | Playwright |
|------|---------|---------|--------|-----------|------------|
| macOS (Homebrew) | ✅ pip3 | ✅ pip3 | ✅ brew | ✅ brew | ✅ MCP/npx |
| Linux (apt) | ✅ pip3 | ✅ pip3 | ✅ apt | ✅ apt | ✅ MCP/npx |
| Windows (WSL) | ✅ pip3 | ✅ pip3 | ✅ choco | ✅ choco | ✅ MCP/npx |

ユーザーの OS に応じて対応するパッケージマネージャーを自動選択。検出方法：
```bash
[[ "$(uname)" == "Darwin" ]] && echo "macOS" || echo "Linux"
```
