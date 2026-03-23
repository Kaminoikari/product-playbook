# ドキュメントインポート解析ルール

> ユーザーが PDF / DOCX / PPTX ファイルをアップロード、または `/parse [file]` をトリガーした時に読み込みます。
> 初回使用時は先に `rules-document-tools.md` を読み込んでツールがインストール済みか確認してください。
> 本ルールは `rules-file-integration.md` と連携して使用します — そちらが「いつトリガーするか」を定義し、本ファイルが「どう解析するか」を定義します。

---

## 解析目標

あらゆる形式の入力ドキュメントを**構造化 Markdown** に変換し、後続フローで使用：
- Feature Extension / Revision モードの S1 コンテキスト収集
- インクリメンタル更新の元ドキュメントベース
- 一般的なドキュメントコンテンツ抽出

---

## PDF 解析：三層戦略 + ページ単位検出

### 概要

```
入力 PDF
  │
  ▼
pymupdf ページ単位テキスト抽出（ゼロコスト）
  │
  ├── そのページのテキスト > 30 文字 → ✅ 直接 Markdown に変換（層 1）
  │
  └── そのページのテキスト ≤ 30 文字（空白 / ベクターパス / スキャン文書）
        │
        ├── デフォルト → Claude Vision セマンティック解析（層 2）
        │
        └── Vision 利用不可 / Token 予算不足 → Tesseract OCR（層 3）
```

### ステップ 1：ページ単位タイプ検出

**重要な原則**：「ページ」単位で検出し、ドキュメント全体ではない。1つの PDF にデジタルテキストページとスキャン画像ページが混在する場合がある。

```python
import fitz  # pymupdf

doc = fitz.open(pdf_path)
total_pages = len(doc)
page_results = {}

for i in range(total_pages):
    page = doc[i]
    text = page.get_text("text").strip()

    if len(text) > 30:
        # 層 1：デジタルテキスト、直接抽出
        page_results[i] = {"type": "digital", "text": text}
    else:
        # Vision または OCR が必要
        page_results[i] = {"type": "needs_vision", "text": None}

digital_count = sum(1 for p in page_results.values() if p["type"] == "digital")
vision_count = total_pages - digital_count

print(f"PDF 分析：{total_pages} ページ、{digital_count} ページ直接抽出可能、{vision_count} ページ視覚解析が必要")
```

### ステップ 2：大容量ファイル処理戦略

| 条件 | 戦略 |
|------|------|
| 全ページが digital（vision_count = 0）| 全ページを直接抽出、ゼロコスト |
| vision_count ≤ 20 | Claude Vision で視覚解析が必要な全ページを一括読み取り |
| vision_count > 20 | バッチ処理（各バッチ ≤ 20 ページ）、結果をマージ |
| 総ページ数 > 50 かつ vision_count > 20 | 全文解析かページ範囲指定かユーザーに確認 |

**大容量ファイル（>50 ページ）のユーザー確認プロンプト**：

```
📄 この PDF は全 {total_pages} ページです：
  • {digital_count} ページはテキスト直接抽出可能（無料）
  • {vision_count} ページは視覚解析が必要（Vision Token を消費）

選択してください：
  1️⃣ 全文解析（完全だが Token 消費が多い）
  2️⃣ 特定ページのみ解析（ページ範囲を入力、例：1-10,15,20-25）
  3️⃣ 直接抽出可能なページのみ抽出（スキャン/ベクターページをスキップ）
```

### ステップ 3：層 1 — pymupdf 直接抽出

```python
def extract_digital_pages(doc, page_results):
    """全デジタルテキストページを抽出"""
    markdown_parts = []
    for i, result in sorted(page_results.items()):
        if result["type"] == "digital":
            markdown_parts.append(f"<!-- Page {i+1} -->\n{result['text']}")
    return "\n\n".join(markdown_parts)
```

### ステップ 4：層 2 — Claude Vision セマンティック解析

`needs_vision` タイプのページについて、まず pymupdf で PNG 画像にレンダリングし、Claude の Read ツールで読み取り。

**画像にレンダリング**：
```python
def render_pages_to_png(doc, page_indices, dpi=300):
    """指定ページを PNG にレンダリング"""
    output_files = []
    for i in page_indices:
        page = doc[i]
        pix = page.get_pixmap(dpi=dpi)
        output_path = f"/tmp/pdf-page-{i+1:04d}.png"
        pix.save(output_path)
        output_files.append((i, output_path))
    return output_files
```

**Claude Vision 解析プロンプト**：

視覚解析が必要な各ページ（またはバッチ）について、Read ツールで PNG を読み込んだ後、以下のプロンプトで変換：

```
あなたは PDF ドキュメントの第 {page_num}/{total_pages} ページを読んでいます。
このページの内容を正確に Markdown 形式に変換してください。

厳格ルール：
1. 表 → Markdown table（全カラム、行数、配置を保持）
2. 見出し → # / ## / ### で元のレベルに対応
3. 番号付きリスト → 1. 2. 3.（元の番号を保持）
4. 箇条書き → - または •
5. 太字/斜体 → **太字** / *斜体*
6. 図表/画像 → > [図表：内容の簡潔な説明]
7. ヘッダー、フッター、ページ番号 → 無視
8. 数字、日付、人名、アカウント → 100% 正確でなければならない、推測しない
9. 原文にない内容を追加しない
10. 翻訳しない — 原文の言語を保持
```

> **なぜ OCR より優れているか**：Claude は表の「セマンティック構造」を理解します（最初の行がヘッダー、どのカラムが揃っているか）。Tesseract は文字単位の認識後にルールで表を再構築するだけで、しばしば失敗します。

### ステップ 5：層 3 — Tesseract OCR Fallback

以下の場合のみ使用：
- ユーザーが Token 節約を明示的にリクエスト
- Claude Vision が利用不可（API 制限等）
- オフライン環境

```python
import subprocess
from PIL import Image

def ocr_page(png_path, lang="chi_tra+eng"):
    """Tesseract OCR 単一ページ"""
    # macOS の tesseract は PNG を直接読めない場合がある — TIFF に変換するか stdin を使用
    tiff_path = png_path.replace('.png', '.tiff')
    Image.open(png_path).save(tiff_path)

    result = subprocess.run(
        ['tesseract', 'stdin', 'stdout', '-l', lang],
        stdin=open(tiff_path, 'rb'),
        capture_output=True, text=True, timeout=120
    )
    return result.stdout
```

**Tesseract 注意事項（実戦経験）**：
- macOS 上の tesseract は PNG ファイルを直接読めない場合がある — `stdin` パイプを使用するか先に TIFF に変換
- 推奨解像度 300dpi
- `chi_tra+eng` 言語パックで繁体中国語と英語を同時認識
- OCR 結果は後処理が必要：改行の結合、表構造の修復

### ステップ 6：全ページをマージ

```python
def merge_all_pages(digital_md, vision_md_list):
    """ページ順に全ページの Markdown をマージ"""
    all_pages = {}
    # digital pages
    for page_num, md in digital_md.items():
        all_pages[page_num] = md
    # vision/ocr pages
    for page_num, md in vision_md_list.items():
        all_pages[page_num] = md

    # ページ番号順にソートしてマージ
    final_md = []
    for i in sorted(all_pages.keys()):
        final_md.append(all_pages[i])

    return "\n\n---\n\n".join(final_md)
```

### ステップ 7：出力してユーザーに通知

```
📄 PDF 解析完了：
  • 総ページ数：{total_pages}
  • 直接抽出：{digital_count} ページ（pymupdf）
  • 視覚解析：{vision_count} ページ（Claude Vision）
  • 出力：{output_path}（Markdown、{文字数} 文字）
```

---

## DOCX 解析

```bash
pandoc "{input_path}" -t markdown -o "/tmp/parsed-{timestamp}.md" --wrap=none
```

**後処理**：
- Pandoc が生成する余分な空行を削除
- 表フォーマットが正しいことを確認

---

## PPTX 解析

```bash
pandoc "{input_path}" -t markdown -o "/tmp/parsed-{timestamp}.md" --wrap=none
```

> Pandoc は各スライドを `##` 見出しセクションに変換します。

---

## HTML 解析

```bash
pandoc "{input_path}" -f html -t markdown -o "/tmp/parsed-{timestamp}.md" --wrap=none
```

---

## 画像解析

Claude Read ツールで直接画像を読み取り、Vision 解析プロンプトに従って Markdown に変換。

---

## rules-file-integration.md との連携

`rules-file-integration.md` が以下のシナリオを検出した場合、本ルールを読み込みます：

| シナリオ | アクション |
|------|------|
| ユーザーが Feature Extension S1 で PDF をアップロード | 本ルールを読み込み → PDF を解析 → 既存システム背景を抽出 |
| ユーザーが Revision S1 で旧バージョン PRD をアップロード | 本ルールを読み込み → PDF を解析 → リビジョンベースとして使用 |
| ユーザーが `/parse` コマンドを使用 | 本ルールを読み込み → 指定ファイルを解析 → Markdown を出力 |
| ユーザーが市場レポート PDF をアップロード | 本ルールを読み込み → 主要情報を抽出 → 対応するステップに統合 |

### 元ドキュメント識別

解析完了後、そのファイルが「元ドキュメント」（PRD、仕様書等）であると判断した場合、自動マーク：

```
📎 元ドキュメントを検出しました — 最終出力はこのファイルに基づくインクリメンタル更新になります。
  ドキュメント構造：{セクション数} セクション、{テーブル数} テーブル
  フォーマット規則：[識別されたフォーマット特徴]
```

ドキュメント構造を記録し、`rules-export-document.md` が最終出力時に使用できるようにします。
