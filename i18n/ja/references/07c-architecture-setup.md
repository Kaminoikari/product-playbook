# 開発ハンドオフ — ARCHITECTURE.md + setup.sh

## 📄 ARCHITECTURE.mdテンプレート

```markdown
# [プロダクト名] — 技術アーキテクチャ

## ディレクトリ構造

[技術スタックに基づいて対応するディレクトリ構造を生成]

## データベース設計

[PRDのDBスキーマから統合 — CREATE TABLE SQLまたはORMモデル定義に変換]

### ERダイアグラム

[Mermaid erDiagram]

### 主要テーブル説明

| テーブル | 説明 | 主要フィールド | インデックス推奨 |
|-------|------------|------------|----------------------|
| | | | |

## API設計

[User Storiesと機能仕様に基づいてRESTful APIエンドポイントまたはGraphQLスキーマを定義]

### エンドポイントリスト

| メソッド | パス | 説明 | 対応タスク |
|--------|------|------------|-------------------|
| GET | /api/v1/[resource] | [説明] | T1.1 |
| POST | /api/v1/[resource] | [説明] | T1.2 |

### 認証

[JWT / Session / OAuthなど]

## サードパーティサービス

| サービス | 目的 | 対応機能 |
|---------|---------|----------------------|
| | | |

## セキュリティアーキテクチャ

### CORS設定

| 設定 | 値 | 備考 |
|---------|-------|-------|
| Allowed Origins | [本番ドメイン、localhost:port] | ワイルドカード*は使用しない |
| Allowed Methods | GET、POST、PUT、DELETE | 実際のAPIニーズに基づく |
| Allowed Headers | Content-Type、Authorization | |
| Credentials | true/false | 認証方法による |

### セキュリティヘッダー

[references/08-security-checklist.md §5からプロダクト要件に基づいて適用するヘッダーを選択]

### Rate Limiting戦略

| エンドポイントタイプ | 制限 | 識別方法 |
|--------------|-------|----------------------|
| 一般API | [X] req/min | IP + User ID |
| ログイン/登録 | [X] req/min | IP |
| ファイルアップロード | [X] req/min | User ID |

### 機密データ取り扱い

- シークレット管理：[.env + プラットフォーム環境変数 / Secrets Manager]
- ロギングルール：パスワード、トークン、個人データを決してログに記録しない
- データ暗号化：[転送中のTLS / 保存時の暗号化要件]

> 完全なセキュリティチェックリストは`references/08-security-checklist.md`にあります
```

---

## 📄 .gitignoreテンプレート

```gitignore
# 環境変数とシークレット
.env
.env.local
.env.*.local
*.pem
*.key

# プロダクト企画進捗（機密ビジネス情報を含む可能性あり）
.product-playbook-progress.md
# Product-playbook 開発ハンドオフマーカー（session-local；commit 禁止）
.product-dev-active

# IDEとOS
.idea/
.vscode/
*.swp
.DS_Store
Thumbs.db

# 依存関係
node_modules/
__pycache__/
*.pyc
venv/

# ビルド出力
dist/
build/
.next/
```

---

## 📄 setup.shテンプレート

```bash
#!/bin/bash
# [プロダクト名] — プロジェクト初期化スクリプト
# 使用方法：chmod +x scripts/setup.sh && ./scripts/setup.sh

set -e

echo "🚀 [プロダクト名]を初期化中..."

# ===== 前提条件の確認 =====
command -v [node/python/etc] >/dev/null 2>&1 || { echo "❌ [ランタイム]が必要です"; exit 1; }

# ===== 依存関係のインストール =====
echo "📦 依存関係をインストール中..."
[npm install / pip install -r requirements.txt / etc]

# ===== 環境設定 =====
if [ ! -f .env ]; then
  echo "📝 .envファイルを作成中..."
  cp .env.example .env
  echo "⚠️  .envを編集し、必要な環境変数を入力してください"
fi

# ===== データベース初期化 =====
echo "🗄️  データベースを初期化中..."
[migration commands]

echo ""
echo "✅ 初期化完了！"
echo ""
echo "次のステップ："
echo "  1. .envを編集して環境変数を入力"
echo "  2. 開発サーバーを起動：[起動コマンド]"
echo "  3. 開発を開始：claude \"CLAUDE.mdとTASKS.mdを読んで、Phase 1の実行を開始してください\""
```

---

## ユーザーガイダンステキスト

### Claude Chat / Cowork内

ハンドオフパッケージの作成後、以下のガイダンスを表示：

```
📦 開発ハンドオフパッケージの準備ができました！以下のファイルが含まれています：

  CLAUDE.md        → Claude Codeのプロジェクトメモリ（プロダクトコンテキスト + 技術仕様）
  TASKS.md         → 開発タスクリスト（4フェーズ、合計[N]タスク）
  TICKETS.md       → チケットリスト（[N]チケット、Jira/Asana/Linearで直接作成可能）
  docs/PRD.md      → 完全なPRD
  docs/ARCHITECTURE.md → 技術アーキテクチャ（DBスキーマ + API + ディレクトリ構造）
  docs/PRODUCT-SPEC.md → プロダクトスペックサマリー
  scripts/setup.sh → ワンクリック初期化スクリプト

🔗 開発の始め方：

  1. ダウンロードしてプロジェクトフォルダに展開
  2. ターミナルを開いてプロジェクトフォルダに移動
  3. Claude Codeを起動：
     $ claude
  4. Claude Codeに指示：
     > CLAUDE.mdとTASKS.mdを読んで、Phase 0の実行を開始してください

💡 ヒント：
  - Claude CodeはCLAUDE.mdを自動的に読み込むので、プロダクトコンテキスト全体を既に把握しています
  - 各フェーズ完了後、次のフェーズに進むか確認します
  - 機能スコープを調整したい場合は、TASKS.mdを直接編集してください
  - CLAUDE.mdの「明示的にやらないこと」リストがClaude Codeのスコープ外の開発を防ぎます
```

### 出力前の最終確認

```
開発ハンドオフパッケージを作成する前に、いくつか確認させてください：

1. 技術スタック：[確認済み / 確認が必要]
2. プロダクト名（プロジェクトフォルダ名用）：[確認済み / 確認が必要]
3. その他の技術的制約や好みはありますか？
   - 例：特定のORMの使用が必須、特定ブラウザのサポートが必要、既存のCI/CDなど
```
