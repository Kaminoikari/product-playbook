[English](README.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [Español](README.es.md) | [한국어](README.ko.md)

# 🎯 The Product Playbook

**世界トップクラスのプロダクト企画AIスキル — アイデアから開発まで、すべてを網羅するフレームワーク**

[![npm version](https://img.shields.io/npm/v/product-playbook.svg)](https://www.npmjs.com/package/product-playbook)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://code.claude.com)
[![Claude.ai](https://img.shields.io/badge/Claude.ai-Custom%20Skill-blue)](https://claude.ai)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![i18n](https://img.shields.io/badge/i18n-6%20languages-green)](README.md)

> Lenny's Podcastの最もインパクトのあるPMフレームワーク（Teresa Torres、Shreyas Doshi、Gibson Biddle、April Dunford、Todd Jackson、Marty Cagan、Richard Rumeltなど）を統合 — AIをあなたのシニアプロダクトマネージャーコーチに変えます。

---

## ✨ これは何？

The Product Playbookは、ゼロから一まで体系的にプロダクト企画をガイドする**Claude AIスキル**です。単なるプロンプトではなく、以下を含む完全なインタラクティブフレームワークガイダンスシステムです：

- 🧭 **6つの実行モード** — 30分の迅速な検証からフルスケールのプロダクト企画まで（機能拡張ファストトラックを含む）
- 📐 **22のプロダクトフレームワーク** — Discovery → Define → Develop → Deliverの全パイプラインをカバー
- 🤝 **3つの専門サブエージェント** — Discovery、戦略批評、Pre-mortem が独立した context window で動作し、フレームワーク固有の専門性を持つ
- 🔄 **変更伝播エンジン** — 任意のステップを修正すると下流の全出力が自動更新
- 📎 **スマートファイル統合** — データ、スクリーンショット、ドキュメントをアップロードするとAIが関連ステップに自動統合
- 🔗 **開発ハンドオフ** — CLAUDE.md + TASKS.md + TICKETS.mdを生成してClaude Code開発にシームレスに接続
- 📊 **マルチフォーマット出力** — PDF（ブックマーク付き）、HTMLレポート、Wordドキュメント、PowerPointデッキ、開発ハンドオフパッケージ
- 📄 **スマートドキュメントインポート** — 三層PDFパース（テキスト抽出 → Claude Vision → OCRフォールバック）、DOCX/PPTXサポート

**一文でフロー全体をトリガー：**

```
プロダクトを作りたい
```

---

## 🎬 デモ

<p align="center">
  <img src="assets/demo-build-ja.gif" alt="The Product Playbook デモ — ビルドモード" width="800">
</p>

> 上のデモは**ビルドモード**を示しています：要件を説明 → コードベースをスキャン → 技術スタックを検出 → フレームワークを適用して問題を明確化し、ソリューション設計にジャンプします。

---

## 🚀 クイックスタート

### オプション1：Claude.ai カスタムスキル

1. このリポジトリをzipファイルとしてダウンロード
2. [Claude.ai](https://claude.ai) → 設定 → カスタムスキルに移動
3. `product-playbook/`フォルダ全体をアップロード
4. 会話で「プロダクトを作りたい」と言ってスキルをトリガー

### 方法2：Claude Code Plugin

Claude Code で以下を実行：

```
/plugin marketplace add kaminoikari/product-playbook
/plugin install product-playbook@kaminoikari-product-playbook
```

> 最初のコマンドで marketplace を追加（初回のみ）、2番目で plugin をインストールします。

### オプション3：Claude Codeスキル（推奨）

> 💡 更新するには：インストールコマンドを再実行するだけで最新バージョンに上書きされます。

| 方法 | 最適な用途 | 要件 |
|--------|----------|-------------|
| ① コピー＆ペースト | 初心者 | Claude Codeを開くだけ |
| ② ワンラインインストール | 開発者 | ターミナル |
| ③ 手動インストール | カスタムパス | ターミナル + git |

#### ① コピー＆ペーストインストール（最も簡単）

Claude Codeを起動後、以下を貼り付けるとClaudeが自動的にインストールを処理します：

```
以下のコマンドを実行してproduct-playbookスキルをインストール（または更新）してください。
完了したら結果を教えてください：

git clone https://github.com/kaminoikari/product-playbook.git /tmp/product-playbook
mkdir -p ~/.claude/skills ~/.claude/commands
cp -r /tmp/product-playbook ~/.claude/skills/product-playbook
cp /tmp/product-playbook/commands/* ~/.claude/commands/
rm -rf /tmp/product-playbook
```

#### ② ワンラインインストール（ターミナル）

```bash
# curl
curl -fsSL https://raw.githubusercontent.com/kaminoikari/product-playbook/main/install.sh | bash

# npx（Node.jsが必要）
npx product-playbook
```

アンインストール：

```bash
curl -fsSL https://raw.githubusercontent.com/kaminoikari/product-playbook/main/install.sh | bash -s -- --uninstall
# または
npx product-playbook --uninstall
```

#### ③ 手動インストール

```bash
git clone https://github.com/kaminoikari/product-playbook.git
mkdir -p ~/.claude/skills ~/.claude/commands
cp -r product-playbook ~/.claude/skills/product-playbook
cp product-playbook/commands/* ~/.claude/commands/
```

インストール後、Claude Codeでトリガー：

```bash
# メインスキルコマンド
> /product-playbook

# スラッシュコマンド（インストール後に利用可能）
> /product-quick 家計簿アプリを作りたい
> /product-full ペットSNSプラットフォーム
> /product-revision ECサイトの決済フローをリデザイン

# または自然言語
> プロダクト企画をしたい
> JTBDで私のプロダクトを分析して
> MVPの企画を手伝って
```

---

## 📦 ファイル構造

```
product-playbook/
├── SKILL.md                          # コアエンジン：モード定義、ステップ順序、コマンドシステム
├── LICENSE                           # MIT License
├── README.md                         # 英語README
├── README.zh-TW.md                   # 繁體中文README
├── README.ja.md                      # 日本語README（このファイル）
├── assets/
│   └── demo.gif                      # READMEデモアニメーション
├── commands/                         # Claude Code CLIスラッシュコマンド（オプションインストール）
│   ├── product-quick.md              # /product-quick — クイックモード
│   ├── product-full.md               # /product-full — フルモード
│   ├── product-revision.md           # /product-revision — リビジョンモード
│   ├── product-build.md              # /product-build — ビルドモード
│   ├── product-feature.md            # /product-feature — 機能拡張モード
│   ├── product-prd.md                # /product-prd — PRD生成
│   ├── product-report.md             # /product-report — HTMLレポート生成
│   └── product-dev.md                # /product-dev — 開発ハンドオフパッケージ生成
├── agents/                           # 専門サブエージェント（Claude Code プラグインが自動読み込み）
│   ├── discovery-specialist.md       # Persona / JTBD / OST / Journey Map スペシャリスト
│   ├── strategy-critic.md            # Rumelt 視点の戦略批評者
│   └── pre-mortem-runner.md          # 15+ の失敗シナリオ + リーディングインジケーター
└── references/
    ├── 00-opportunity-check.md       # 機会評価 + DHMモデル
    ├── 01-strategy.md                # Strategy Blocks + Rumelt + OKR
    ├── 02-discovery.md               # ペルソナ + JTBD + OST + ジャーニーマップ
    ├── 03-define.md                  # ペインポイント + ポジショニング + HMW + 機会評価
    ├── 04-develop.md                 # PR-FAQ + Pre-mortem + RICE + MVP + PRD
    ├── 05-deliver.md                 # North Star + PMF + GTM + ビジネスモデル + プロダクトスペック
    ├── 06-html-report.md             # HTML企画レポート出力仕様
    ├── 07-dev-handoff.md             # 開発ハンドオフ：CLAUDE.md + TASKS.md + アーキテクチャ
    ├── 08-security-checklist.md      # OWASP Top 10 + CORS + CSP + セキュリティアーキテクチャ
    ├── rules-context.md              # クロスセッションプロダクトコンテキスト蓄積ルール
    ├── rules-document-tools.md       # ドキュメント変換ツール依存管理
    ├── rules-import-document.md      # 三層PDFパース + DOCX/PPTXインポート
    ├── rules-export-document.md      # マルチフォーマットエクスポート（PDF/DOCX/PPTX）
    ├── rules-*.md                    # モードステップルール + 進捗/変更/ファイル統合ルール
    └── templates/
        ├── prd-style.css             # プロフェッショナル印刷グレードCSS（PDFエクスポート用）
        └── report-style.css          # 印刷最適化CSS（HTMLレポート → PDF）
```

---

## 🧭 6つの実行モード

| モード | ステップ | 所要時間 | 最適な用途 |
|------|-------|----------|----------|
| 🚀 **クイックモード** | 3ステップ | 約30分 | 迅速なアイデア検証、ピッチ準備 |
| 📦 **フルモード** | 9–11ステップ（8 Core + 1 デフォルト ON Journey Map + 2 デフォルト OFF Optional） | 1-2時間 | 新プロダクト企画、大規模リニューアル |
| 🔄 **リビジョンモード** | 6–8ステップ（6 Core + 2 Optional） | <1時間 | 既存プロダクトの改善 |
| ✏️ **カスタムモード** | 4-16ステップ | 場合による | 特定のギャップを埋める |
| ⚡ **ビルドモード** | 7ステップ | 約1時間 | 問題は既知、ソリューションに直行 |
| 🔧 **機能拡張** | 4ステップ | 約30分 | 既存プロダクトに単一機能を追加 |

---

## 📐 含まれるフレームワーク

### ユーザー理解
| フレームワーク | 提唱者 | 目的 |
|-----------|---------|---------|
| JTBD（Jobs to Be Done） | Clayton Christensen | ユーザーが本当に達成しようとしているジョブを発見 |
| ペルソナ | — | タスク/モチベーション駆動のユーザーアーキタイプ |
| ユーザージャーニーマップ | — | エンドツーエンドのユーザー体験マッピング |
| Continuous Discovery | Teresa Torres | ユーザーとの週次対話の習慣 |
| OST（Opportunity Solution Tree） | Teresa Torres | 機会とソリューションを体系的に接続 |

### 問題定義
| フレームワーク | 提唱者 | 目的 |
|-----------|---------|---------|
| ポジショニング | April Dunford | 競争コンテキストと差別化 |
| HMW（How Might We） | — | ペインポイントをデザインチャレンジに変換 |

### ソリューション設計
| フレームワーク | 提唱者 | 目的 |
|-----------|---------|---------|
| Working Backwards / PR-FAQ | Amazon | 顧客のアウトカムから逆算 |
| Pre-mortem | Shreyas Doshi | 失敗が起きる前に予測し防止 |
| GEMモデル | Gibson Biddle | Growth / Engagement / Monetization優先順位付け |
| RICEスコアリング | Intercom | 定量的な機能優先順位付け |
| MVP定義 | — | 最小実行可能プロダクトのスコープ設定 |

### 戦略
| フレームワーク | 提唱者 | 目的 |
|-----------|---------|---------|
| Strategy Blocks | Chandra Janakiraman | Mission → Vision → Strategy の階層 |
| Good Strategy Kernel | Richard Rumelt | 診断 → 基本方針 → 一貫した行動 |
| DHMモデル | Gibson Biddle | Delight / Hard to copy / Margin-enhancing |
| Empowered Teams | Marty Cagan | エンパワードチーム vs フィーチャーチーム |

### 測定＆デリバリー
| フレームワーク | 提唱者 | 目的 |
|-----------|---------|---------|
| North Star Metric | Sean Ellis / Amplitude | コアユーザー価値を表す単一メトリクス |
| 4段階PMFフレームワーク | Todd Jackson | プロダクトマーケットフィットの評価 |
| Sean Ellis Score | Sean Ellis | PMF熱狂度の定量化 |
| GTM戦略 | — | Go-to-Marketローンチと顧客獲得 |
| ビジネスモデル＆プライシング | — | 収益モデル選択と価値ベースプライシング |

---

## 🔑 主要機能

### 📎 スマートファイル統合

任意のステップで補足ファイルをアップロード — AIが自動的に識別し統合：

| アップロード | 自動統合先 |
|--------|---------------------|
| 競合スクリーンショット | ポジショニング分析 |
| インタビュー記録 | ペルソナ + JTBD |
| ユーザーデータCSV | 機会評価 + PMF評価 |
| 市場レポートPDF | 機会評価 + 戦略 |
| 既存PRD | リビジョンモード + MVP |

### 🔄 変更伝播エンジン

上流の任意のステップを修正すると下流の出力が自動更新：

```
JTBDを修正 → HMW、ポジショニング、PR-FAQ、North Star、プロダクトスペックサマリーを自動更新
MVPを修正 → User Stories、DBスキーマ、プロダクトスペックサマリーを自動更新
```

### 🔗 開発ハンドオフ

完全な開発ハンドオフパッケージを生成し、単一コマンドでClaude Code開発を開始：

```
📦 開発ハンドオフパッケージ
├── CLAUDE.md          → Claude Codeプロジェクトメモリ
├── TASKS.md           → 機能分解 + フェーズデリバリー
├── TICKETS.md         → チケットリスト（Jira/Asana/Linear対応）
├── docs/
│   ├── PRD.md         → 完全なPRD
│   ├── ARCHITECTURE.md → DBスキーマ + API + ディレクトリ構造
│   └── PRODUCT-SPEC.md → プロダクトスペックサマリー
└── scripts/
    └── setup.sh       → ワンクリック初期化スクリプト
```

```bash
# 単一コマンドでClaude Code開発を開始
> CLAUDE.mdとTASKS.mdを読んで、Phase 0の実行を開始してください
```

### 🪝 ライフサイクルフック

3つのプラグインフックで、Playbook の中核ルールを「Claude の記憶頼み」から「ハーネスによる強制実行」へ昇格させます。すべてのフックは `systemMessage` によるソフトリマインダーを注入するのみで、**ユーザーを止めることはありません**。

| イベント | トリガー | 役割 |
|---------|---------|------|
| `SessionStart` | 新規 / 再開セッションごと | `.product-playbook-progress.md` と `.product-context.md` を自動でモデルの context に注入し、中断した企画を直前のステップから途切れなく再開 |
| `UserPromptSubmit` | 企画進行中のプロンプト送信ごと | (a) 脱線メッセージ（debug / エラー / "このコード直して"）を検出して SKILL.md の進捗保存ルールを実行するよう Claude に指示。(b) 変更意図キーワード（`改 step 2`、`update persona`、`JTBD やり直し`）を検出して Change Propagation ルールの適用を促す |
| `PreToolUse` (Write/Edit/MultiEdit) | ファイル書き込み前 | プロジェクトが企画フェーズ（`.product-dev-active` マーカー無し）で、対象がソースコード拡張子（`.ts/.tsx/.py/.go/...`）の場合、「企画はドキュメントのみ、コードは生成しない」と Claude にリマインド。マーカーは `/product-dev` 実行時に自動生成 |

フックはプラグインインストール時に `hooks/hooks.json` から自動ロードされます。product-playbook プロジェクト外では完全に no-op で動作するため、他のコードベースへの影響はありません。

### 📄 ドキュメントインポート＆エクスポート

**インポート** — 既存のドキュメントを企画フローに直接取り込み、手動コピペ不要：

```
PDF（デジタル）    → pymupdfテキスト抽出（即座、無料）
PDF（ベクター/スキャン） → Claude Visionセマンティックパース（最高品質）
PDF（フォールバック） → Tesseract OCR（オフライン対応）
DOCX / PPTX       → Pandoc変換
```

**エクスポート** — 企画アウトプットをプロフェッショナルなフォーマットに：

```
/export pdf   → Playwrightレンダリング + pikepdfブックマーク（CJK完全対応）
/export docx  → Pandoc + リファレンステンプレート
/export pptx  → Pandocスライド生成
/export html  → インタラクティブHTMLレポート（既存）
```

> **なぜPlaywrightでPDF？** WeasyPrintはCJKテキストが文字化けします。Playwright（Chromium）は完璧にレンダリング — 繁體中文ドキュメントで本番環境検証済み。

### 🔥 既存システム上で直接企画（ビルドモードのキラー機能）

既存プロジェクトディレクトリ内で**ビルドモード**を起動 — Claude Codeがコードベースを読みながらプロダクト企画を行い、**プロダクト企画**と**技術的実現可能性評価**を単一フローに統合：

```
既存プロジェクト                      Product Playbook
┌─────────────────┐                ┌─────────────────────┐
│ src/             │  ← 自動スキャン → │ Pre-mortemリスク      │
│ db/schema.sql    │  ← 自動スキャン → │ MVPスコーピング       │
│ api/routes/      │  ← 自動スキャン → │ RICE優先順位付け      │
│ package.json     │  ← 自動スキャン → │ User Story分解       │
│ CLAUDE.md        │  ← 自動スキャン → │ 開発ハンドオフ（差分） │
└─────────────────┘                └─────────────────────┘
```

**使用例：**

```bash
# 1. 既存プロジェクトに移動
cd /path/to/your-existing-project

# 2. Claude Codeを起動
claude

# 3. ビルドモードを使用して追加したい機能を説明
> /product-feature 既存システムにリアルタイム通知を追加したい
```

Claude Codeは自動的に：
- ディレクトリ構造、技術スタック、DBスキーマをスキャン
- **実際のアーキテクチャ**に基づいてPre-mortemを実行（仮説的リスクではなく）
- 既存モジュールに直接プラグインするMVPとUser Storiesを生成
- グリーンフィールドビルドではなく**差分プラン**として開発ハンドオフパッケージを作成

> 💡 **なぜこれが強力か？** 従来のプロダクト企画と技術評価は別プロセス — PMが仕様を書き、エンジニアに投げて、エンジニアが「これはできない」と言う。ビルドモードは企画プロセスを実際のシステム制約に基づかせ、やり取りを排除します。

### 🔒 セキュリティ内蔵

開発ハンドオフパッケージにはセキュリティアーキテクチャが自動的に含まれます — 後付けパッチは不要：

- **OWASP Top 10チェックリスト** — 入力バリデーション、認証/認可、XSS/CSRF保護
- **セキュリティアーキテクチャセクション** — CORSポリシー、CSPヘッダー、Rate Limiting、APIセキュリティミドルウェア
- **.gitignoreテンプレート** — `.env`、クレデンシャル、進捗ファイルを自動除外
- **Pre-mortemセキュリティシナリオ** — データ漏洩、アカウント乗っ取り、API悪用を必須検討項目として

### 📦 クロスセッションプロダクトコンテキスト蓄積

企画出力は自動的に`.product-context.md`に保存され、次のセッションで読み込み：

```
1回目（フルモード） → Identity + Core Strategy + Architectureを保存
2回目（機能拡張） → 技術スタックとモジュールを自動読み込み、冗長な収集をスキップ
3回目（リビジョンモード） → 過去の決定と既知のペインポイントを引き継ぎ、差分にフォーカス
```

### 🏢 B2B / B2C自動適応

プロダクトタイプが確認されると、フレームワークが自動適応：

| 観点 | B2C | B2B |
|--------|-----|-----|
| ペルソナ | 個人のモチベーションセグメンテーション | 購入者 + ユーザーの二重ペルソナ |
| PMF | DAU / リテンション / Sean Ellis | 有料顧客 / NRR / NPS |
| North Star | コアアクション完了数 | ARR / Net Revenue Retention |
| Aha Moment | 初回使用内 | オンボーディング / Time-to-Value |

---

## 📊 品質ベンチマーク結果

「スキルガイドあり」と「スキルガイドなし」のレスポンス品質を自動AI採点で比較し、スキルの実際のインパクトを定量化しました。

### 4回のイテレーション比較

| イテレーション | テスト項目 | スキルあり合格率 | スキルなし合格率 | 差分 |
|-----------|:--------:|:-------------------:|:----------------------:|:-----:|
| イテレーション1（ベースライン） | 6 | 100% | 57.4% | +42.6% |
| イテレーション2 | 6 | 100% | 63.3% | +36.7% |
| イテレーション3 | 6 | 94.1% | 38.2% | +55.9% |
| **イテレーション4（最新）** | **9** | **100%** | **31%** | **+69% ✅** |

### イテレーション4 詳細結果（9テスト × 49期待値）

| テスト項目 | スキルあり | スキルなし | 差分 |
|-----------|:--------:|:------------:|:-----:|
| モード選択（3段階プログレッシブ） | 100% | 0% | +100% |
| クイックモード JTBD分析 | 100% | 43% | +57% |
| JTBD深掘り（B2B組織レベル） | 100% | 57% | +43% |
| PR-FAQライティング | 100% | 33% | +67% |
| リビジョンモード | 100% | 67% | +33% |
| 品質セルフチェック ハードゲート | 100% | 0% | +100% |
| **機能拡張モード（新規）** | **100%** | **17%** | **+83%** |
| **セキュリティ統合（新規）** | **100%** | **25%** | **+75%** |
| **Context Bootstrap（新規）** | **100%** | **0%** | **+100%** |

### 主要な発見

- **品質セルフチェック ハードゲート**（+100%）：AIが成果物完成後に厳格な基準で自発的に自身の出力を批評し、ギャップを指摘し、改善を求めるかどうか — スキルなしでは合格率0%
- **Context Bootstrap**（+100%）：AIが企画を始める前に基礎的なプロダクト情報を収集するか、それとも技術的実装にすぐ飛び込むか — スキルなしでは完全にスキップ
- **機能拡張モード**（+83%）：AIが「既存プロダクトへの機能追加」シナリオを認識し、フルの6-11ステップではなく効率化された4ステップフローを起動するか — スキルなしでは技術ソリューションに直行
- **セキュリティ統合**（+75%）：開発ハンドオフにセキュリティアーキテクチャ、.gitignoreテンプレート、プラットフォーム固有のセキュリティ対策が含まれるか — スキルなしではセキュリティは単一のサマリー表に縮小

> 詳細な方法論とデータは[`evals/`](./evals/)を参照。

### イテレーション5：Sub-agent A/B 比較（ディスパッチ関連3評価 × 22期待値）

v1.2.0+ で導入された3つの専門 sub-agent（`discovery-specialist`、`strategy-critic`、`pre-mortem-runner`）の品質への限界貢献を測定する集中 A/B 評価。同じスキル版（v1.2.3）、同じプロンプト、2つの arm：

- **Sub-agent あり**：executor は該当する `agents/*.md` を読み、専門エージェントが宣言する出力スキーマと自己チェックに従う。レスポンス内に dispatch マーカーを記録。
- **Sub-agent なし**：executor は `agents/*.md` を一切読まず、delegation に言及しない。`SKILL.md` + `commands/` + `references/` のみを使い、orchestrator が inline で処理する。

| 評価項目 | Sub-agent あり | Sub-agent なし | 差分 |
|-----------|:--------:|:------------:|:-----:|
| Discovery（Persona + JTBD） | 100%（7/7） | 85.7%（6/7） | +14.3% |
| Strategy Critic | 100%（6/6） | 83.3%（5/6） | +16.7% |
| **Pre-mortem（Build Mode リスク評価）** | **100%（9/9）** | **22.2%（2/9）** | **+77.8% ✅** |
| **合計** | **100%（22/22）** | **59.1%（13/22）** | **+40.9%** |

両 arm の token 消費はほぼ同じ（151K vs 154K）— 専門エージェントを保持することは inline 処理より高くはならない。

**主要な発見**

- **Pre-mortem-runner は load-bearing**（+77.8%）：これがないと、orchestrator は薄く未来形のリスクリストしか生成できず、シナリオ数（≥15）、5カテゴリーのカバレッジ、leading indicator の規律、低コスト pre-launch 実験、過去形「出荷して失敗した」のナラティブ枠組みを失う。構造化された専門エージェントのスキーマが本当の仕事をしており、`references/` だけでは再構築できない。
- **Discovery-specialist と strategy-critic は中程度の貢献**（+14–17%）：orchestrator 単独でも Persona+JTBD と戦略批評を妥当なレベルで処理できる。両 arm で分岐する assertion は dispatch コントラクト自体であり、構造的品質ではない。
- **含意**：3つの専門のうち、pre-mortem-runner が単独での品質向上が最大で、最も保持を正当化される。他の2つは原理的には強化された reference ページで orchestrator に折り返せるが、token コストが同じなので削減誘因はない。

**ハーネスの注意**：この評価環境の `general-purpose` executor は nested `Task` を公開しないため、「Sub-agent あり」 arm は「専門エージェントの `agents/*.md` を読む + dispatch マーカー + スキーマを inline で遵守」で実際の dispatch を近似する。構造的対比は実物だが、エンドツーエンドの Task ツール dispatch を完全に検証するには top-session 実行が必要。

> 生の成果物と assertion ごとの分岐は [`~/product-playbook-workspace/iteration-3/benchmark.md`](./evals/) を参照。

---

### イテレーション6：Token 最適化パス（v1.2.5）

token 削減イテレーション。スキル内容のセマンティクスは同じで、セッションあたりのフットプリントを縮小。目標は品質を 100% に維持しながら 25% 以上の token 削減。

**出荷した変更：**
- **SKILL.md スリム化** — Sub-Agent Delegation Rules を lazy な `rules-subagent-dispatch.md` に抽出、Hard Gate の記述を簡潔化、Mode Overview の重複を統合。eager エントリポイントで **6,188 → 2,877 tokens（-54%）**。
- **rules-context.md 分割** — 決定ロジックは eager のまま維持（1,594 tokens）、冗長な YAML テンプレート + Bootstrap 手順 + Conflict UX スクリプトを lazy な `rules-context-template.md`（1,849 tokens、トリガー時のみ読込）に移動。
- **rules-quality-review.md スリム化** — 1,040 → 817 tokens に蒸留、コンパクトな 3 ステップのプロトコル + 各 framework 1 行のチェックリスト。
- **Specialist agents スリム化** — `references/*.md` と重複していた framework 知識を削除し、on-demand のポインタに置換。dispatch あたり **discovery-specialist −25%、strategy-critic −18%、pre-mortem-runner −20%**。

**9 ステップ Full Mode セッションあたりの推定削減：**

| ソース | Before | After | 削減 |
|--------|:------:|:-----:|:-----:|
| Eager（SKILL + context + progress） | ~8,800 | ~5,500 | **−3,300** |
| Quality review（×9 ステップロード） | ~9,360 | ~7,353 | **−2,007** |
| Sub-agent dispatches（3 specialists） | ~9,005 | ~7,106 | **−1,899** |
| **セッション合計** | **~27,200** | **~18,900** | **−8,300（−30%）** |

**品質検証：** pre-mortem-runner（イテレーション 5 で最も品質感受性が高い specialist）が v1.2.5 のスリム化された内容で eval-12 を再実行。結果は **9/9 assertion PASS** — 全 5 カテゴリーにまたがる 16 シナリオ、実際のスタック構成要素を引用するアーキテクチャ根拠付きシナリオ 5 件、二項決定ルールを持つ低コスト pre-launch 実験 5 件、過去形の枠組みを維持。静的クロスチェックにより、スリム化された agent プロンプトにおいて eval-10/11 の assertion（合計 13 件）すべてに明示的な裏付けがあることを確認。

**Token コストのトレードオフ：** 分割により、トリガー時のみ読み込まれる 2 つの新規 lazy ファイル（`rules-subagent-dispatch.md` 978 tokens、`rules-context-template.md` 1,849 tokens）が追加される。最も一般的なセッション経路ではこれらは読み込まれない。Bootstrap または Conflict 経路でも、eager の削減が依然としてネットでプラス。

**5 つの i18n ロケール（zh-TW、zh-CN、ja、es、ko）にミラー** — 既存の翻訳を保持しつつ、構造的なスリム化を言語ごとに同一に適用。

---

## 🧪 開発と評価

`evals/` ディレクトリには 2 つの補完的なテストセットと決定論的なスコアラーが含まれます。

**ローカル（無料、推奨）**：`claude` CLI を Claude Pro/Max サブスクリプションで認証して（一度だけ `claude login`）同じスクリプトを実行できます。API key 不要、追加コストなし。eval システムは各リリース前にローカルで実行する設計です。

**CI（オプション、有料）**：`.github/workflows/eval-gate.yml` はすべての PR と `package.json` を変更する `main` への push で両方を実行し、スコアを workflow の Job Summary に書き込みます。**merge も publish もブロックしません** — リグレッションに対応するかどうかはメンテナが判断します。CI には `ANTHROPIC_API_KEY` secret が必要です（GitHub Actions は headless コンテナで OAuth が使えません）。secret 未設定時は eval job が**クリーンに skip**（グレー ⏭️）され、誤解を招く赤バツは出ません。

### ローカル実行

```bash
# Trigger eval — 自然言語の prompt で skill が自動トリガーされるか?
python3 evals/run_trigger_test.py --runs 3 --workers 4 --fail-on critical \
  --json evals/eval-results.trigger.json

# Behavioral eval — 各シナリオで skill が正しい出力を生成するか?
# claude を assistant 兼 judge として使用（--runs 3 で多数決）
python3 evals/run_behavioral_eval.py --runs 3 --workers 2 --fail-on critical \
  --json evals/eval-results.behavioral.json

# ローカライズ版
python3 evals/run_behavioral_eval.py --eval-file evals/evals-zh-TW.json --runs 3

# スコアラーのユニットテスト
python3 -m unittest evals/test_compute_eval_score.py
```

両方の runner は `claude` CLI が `PATH` 上にあり、`ANTHROPIC_API_KEY` 環境変数が設定されている必要があります。ローカルは `--runs 3` がデフォルト（多数決で LLM のばらつきを吸収）、CI ではコスト削減のため `--runs 1` を使用します。

### Severity とスコアリング

`evals.json` の各 expectation には severity がタグ付けされています：

| Severity | 失敗時の減点 | 適用範囲 |
|---|---|---|
| `critical` | −15 | Hard Gate 違反、Mode dispatch エラー、B2B buyer/user 分離、Security default-on、フレームワークの完全性（JTBD 3 層、Rumelt diagnosis、pre-mortem 15+ シナリオ）|
| `warning`  | −5  | 品質の深さと構造（多くの expectations）|
| `info`     | −1  | 言語検出、Progress indicator フォーマット |

100 点からスタート、失敗ごとに減点、0–100 にクランプ。

| Band | 範囲 | 意味 |
|---|---|---|
| 🟢 `healthy` | ≥ 90 | critical 失敗は最大 1 つ |
| 🟡 `needs-attention` | ≥ 70 | critical 2 つまで、または数個の warning |
| 🔴 `at-risk` | < 70 | critical が 3 つ以上；gate 失敗の対象 |

### `--fail-on` のセマンティクス

| Flag 値 | Runner が exit non-zero になる条件 |
|---|---|
| `critical` | critical な expectation が 1 つでも失敗（CI デフォルト）|
| `any` | severity 問わず任意の expectation が失敗 |
| `none` | 失敗しない；ローカル探索用 informational mode |

すべてのスコアリングロジックは `evals/compute_eval_score.py` という単一のソースに集約され、2 つの runner が独自実装で drift することを防ぎます。

---

## 💬 利用可能なコマンド

### ⌨️ Claude Code CLIスラッシュコマンド

スキルインストール後に利用可能なメインコマンド：

| コマンド | 説明 |
|---------|-------------|
| `/product-playbook` | 完全なプロダクト企画ガイドフローを起動 |

より細かいショートカットとして、`commands/`フォルダのプリビルトスラッシュコマンドをインストール：

```bash
# すべてのスラッシュコマンドをインストール
cp -r product-playbook/commands/* ~/.claude/commands/
```

| コマンド | 説明 |
|---------|-------------|
| `/product-quick <説明>` | クイックモード — JTBD → PR-FAQ → North Starを30分以内で実行 |
| `/product-full <説明>` | フルモード — 完全なプロダクト企画（9–11ステップ；Journey Map デフォルト ON） |
| `/product-revision <説明>` | リビジョンモード — 既存プロダクトの改善と最適化 |
| `/product-build <説明>` | ビルドモード — ディスカバリーをスキップ、ソリューションに直行 |
| `/product-feature <説明>` | 機能拡張モード — 既存プロダクトに単一機能を追加（4ステップ） |
| `/product-prd` | PRDエンジニアリングハンドオフパッケージを生成 |
| `/product-report` | HTML企画レポートを生成 |
| `/product-dev` | 開発ハンドオフパッケージを生成（CLAUDE.md + TASKS.md + TICKETS.md） |

### 💬 会話内の自然言語コマンド

#### フロー制御
- `[フレームワーク]に切り替え` — 即座にフレームワークを切り替え
- `このステップをスキップ` — 現在のステップをスキップ
- `[ステップ名]に戻る` — 任意のステップに戻って修正
- `簡潔にして` / `詳しくして` — 深さを調整

#### 出力コマンド
- `レポートを生成` — HTML企画レポート
- `PRDを生成` — エンジニアリングハンドオフ（フローチャート + DBスキーマ + ワイヤーフレーム付き）
- `プレゼンを生成` — PowerPointプレゼンテーション
- `開発を始めて` — 開発ハンドオフパッケージ（CLAUDE.md + TASKS.md）
- `/export pdf` — プロフェッショナルなタイポグラフィ、表紙、目次、ブックマーク付きPDFとしてエクスポート
- `/export docx` — Wordドキュメントとしてエクスポート
- `/export pptx` — PowerPointスライドとしてエクスポート
- `/parse [file]` — PDF/DOCX/PPTXをMarkdownにパースして企画に利用

#### 分析コマンド
- `完成度チェックを実行` — 企画カバレッジの評価
- `仮定を特定して` — 未検証の仮定をリスト
- `Pre-mortemを実行` — Pre-mortem分析
- `このプロダクトのPMFレベルは？` — PMF評価
- `ボトルネックを見つけて` — Aha Moment障害分析

---

## 🤝 コントリビューション

コントリビューションを歓迎します！特に以下の領域でのご協力をお待ちしています：

- 🌍 **多言語サポート** — フレームワークの他言語への翻訳
- 📐 **新フレームワーク** — プロダクトマネジメントフレームワークの追加
- 📝 **例** — 各フレームワークへの実例の追加
- 🐛 **バグレポート** — 使用中に発見されたロジックの問題やギャップ
- 💡 **UX改善** — インタラクションフローとコマンド設計への提案

### コントリビューション方法

1. このリポジトリをFork
2. フィーチャーブランチを作成（`git checkout -b feature/amazing-framework`）
3. 変更をコミット（`git commit -m 'feat: add amazing framework'`）
4. ブランチにPush（`git push origin feature/amazing-framework`）
5. Pull Requestを作成

### コントリビューションガイドライン

- リファレンスファイルのフレームワーク内容は出典を引用すること
- 新フレームワークはSKILL.mdのフレームワークインデックスとステップ順序の更新を含むこと
- 品質セルフチェックリストは✅ / ❌フォーマットを使用
- 多言語サポート：英語版と日本語版の両方をメンテナンス

---

## 📚 フレームワーク出典＆参考文献

このプロジェクトのフレームワークは以下のソートリーダーの公開著作から統合されています：

| ソートリーダー | コア貢献 | 推奨リーディング |
|----------------|-------------------|---------------------|
| Teresa Torres | Continuous Discovery、OST | *Continuous Discovery Habits* |
| Shreyas Doshi | LNO、Pre-mortem、プロダクトワーク3レベル | Lenny's Podcast Ep.3 |
| Gibson Biddle | DHMモデル、GEM | Lenny's Podcast |
| April Dunford | ポジショニングフレームワーク | *Obviously Awesome* |
| Todd Jackson | 4段階PMF、Four P's | Lenny's Podcast |
| Richard Rumelt | 良い戦略 / 悪い戦略 | *Good Strategy Bad Strategy* |
| Marty Cagan | Empowered Teams | *Inspired*、*Empowered* |
| Clayton Christensen | Jobs to Be Done | *Competing Against Luck* |
| Amazon | Working Backwards / PR-FAQ | *Working Backwards* |
| Sean Ellis | Sean Ellis Score、Growth | *Hacking Growth* |
| Lenny Rachitsky | Shape / Ship / Synchronize | Lenny's Newsletter + Podcast |

---

## 📄 ライセンス

このプロジェクトは[MITライセンス](LICENSE)の下で公開されています — 自由に使用、変更、配布できます。

---

## ⭐ Star履歴

このプロジェクトがお役に立ちましたら、⭐を付けてより多くの人に見つけてもらえるようにしてください！

---

<p align="center">
  <strong>本当に重要なものを作りたいプロダクトマネージャーのために、❤️を込めて構築されました。</strong>
</p>

---

Copyright (c) 2026 Charles Chen.
