[English](README.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [Español](README.es.md) | [한국어](README.ko.md)

# 🎯 The Product Playbook

**世界トップクラスのプロダクト企画AIスキル — アイデアから開発まで、すべてを網羅するフレームワーク**

[![npm version](https://img.shields.io/npm/v/the-product-playbook.svg)](https://www.npmjs.com/package/the-product-playbook)
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
- 🔄 **変更伝播エンジン** — 任意のステップを修正すると下流の全出力が自動更新
- 📎 **スマートファイル統合** — データ、スクリーンショット、ドキュメントをアップロードするとAIが関連ステップに自動統合
- 🔗 **開発ハンドオフ** — CLAUDE.md + TASKS.md + TICKETS.mdを生成してClaude Code開発にシームレスに接続
- 📊 **マルチフォーマット出力** — HTMLレポート、PRD、PowerPointデッキ、開発ハンドオフパッケージ

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
3. `the-product-playbook/`フォルダ全体をアップロード
4. 会話で「プロダクトを作りたい」と言ってスキルをトリガー

### オプション2：Claude Codeスキル（推奨）

> 💡 更新するには：インストールコマンドを再実行するだけで最新バージョンに上書きされます。

| 方法 | 最適な用途 | 要件 |
|--------|----------|-------------|
| ① コピー＆ペースト | 初心者 | Claude Codeを開くだけ |
| ② ワンラインインストール | 開発者 | ターミナル |
| ③ 手動インストール | カスタムパス | ターミナル + git |

#### ① コピー＆ペーストインストール（最も簡単）

Claude Codeを起動後、以下を貼り付けるとClaudeが自動的にインストールを処理します：

```
以下のコマンドを実行してthe-product-playbookスキルをインストール（または更新）してください。
完了したら結果を教えてください：

git clone https://github.com/kaminoikari/the-product-playbook.git /tmp/the-product-playbook
mkdir -p ~/.claude/skills ~/.claude/commands
cp -r /tmp/the-product-playbook ~/.claude/skills/the-product-playbook
cp /tmp/the-product-playbook/commands/* ~/.claude/commands/
rm -rf /tmp/the-product-playbook
```

#### ② ワンラインインストール（ターミナル）

```bash
# curl
curl -fsSL https://raw.githubusercontent.com/kaminoikari/the-product-playbook/main/install.sh | bash -s -- --lang ja

# npx（Node.jsが必要）
npx the-product-playbook --lang ja
```

アンインストール：

```bash
curl -fsSL https://raw.githubusercontent.com/kaminoikari/the-product-playbook/main/install.sh | bash -s -- --uninstall
# または
npx the-product-playbook --uninstall
```

#### ③ 手動インストール

```bash
git clone https://github.com/kaminoikari/the-product-playbook.git
mkdir -p ~/.claude/skills ~/.claude/commands
cp -r the-product-playbook ~/.claude/skills/the-product-playbook
cp the-product-playbook/commands/* ~/.claude/commands/
```

インストール後、Claude Codeでトリガー：

```bash
# メインスキルコマンド
> /the-product-playbook

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
the-product-playbook/
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
│   ├── product-prd.md                # /product-prd — PRD生成
│   ├── product-report.md             # /product-report — HTMLレポート生成
│   └── product-dev.md                # /product-dev — 開発ハンドオフパッケージ生成
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
    └── rules-*.md                    # モードステップルール + 進捗/変更/ファイル統合ルール
```

---

## 🧭 6つの実行モード

| モード | ステップ | 所要時間 | 最適な用途 |
|------|-------|----------|----------|
| 🚀 **クイックモード** | 3ステップ | 約30分 | 迅速なアイデア検証、ピッチ準備 |
| 📦 **フルモード** | 20ステップ | 数時間 | 新プロダクト企画、大規模リニューアル |
| 🔄 **リビジョンモード** | 12ステップ | 1-2時間 | 既存プロダクトの改善 |
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
> /product-build 既存システムにリアルタイム通知を追加したい
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
- **機能拡張モード**（+83%）：AIが「既存プロダクトへの機能追加」シナリオを認識し、フルの7-12ステップではなく効率化された4ステップフローを起動するか — スキルなしでは技術ソリューションに直行
- **セキュリティ統合**（+75%）：開発ハンドオフにセキュリティアーキテクチャ、.gitignoreテンプレート、プラットフォーム固有のセキュリティ対策が含まれるか — スキルなしではセキュリティは単一のサマリー表に縮小

> 詳細な方法論とデータは[`evals/`](./evals/)を参照。

---

## 💬 利用可能なコマンド

### ⌨️ Claude Code CLIスラッシュコマンド

スキルインストール後に利用可能なメインコマンド：

| コマンド | 説明 |
|---------|-------------|
| `/the-product-playbook` | 完全なプロダクト企画ガイドフローを起動 |

より細かいショートカットとして、`commands/`フォルダのプリビルトスラッシュコマンドをインストール：

```bash
# すべてのスラッシュコマンドをインストール
cp -r the-product-playbook/commands/* ~/.claude/commands/
```

| コマンド | 説明 |
|---------|-------------|
| `/product-quick <説明>` | クイックモード — JTBD → PR-FAQ → North Starを30分以内で実行 |
| `/product-full <説明>` | フルモード — 20ステップの完全なプロダクト企画 |
| `/product-revision <説明>` | リビジョンモード — 既存プロダクトの改善と最適化 |
| `/product-build <説明>` | ビルドモード — ディスカバリーをスキップ、ソリューションに直行 |
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
