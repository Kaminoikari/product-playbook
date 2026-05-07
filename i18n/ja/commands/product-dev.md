---
description: 開発ハンドオフパッケージを生成 — CLAUDE.md + TASKS.md + TICKETS.md + ARCHITECTURE.md + setup.sh を作成し、Claude Codeでの開発をすぐに開始可能
---

product-playbook skill を起動してください。
次に以下のリファレンスファイルを順番に読み込んでください：
1. `references/07a-handoff-core.md`（CLAUDE.mdテンプレート + 技術スタック確認）
2. `references/07b-tasks-tickets.md`（TASKS.md + TICKETS.mdテンプレート）
3. `references/07c-architecture-setup.md`（ARCHITECTURE.md + setup.sh + ユーザーガイダンス）

現在の会話で完成したプロダクト企画内容に基づいて、完全な開発ハンドオフパッケージを生成します：
1. 技術スタックの確認（ユーザーが指定していない場合、プロダクト特性に基づいて推奨）
2. プロジェクトルートに `.product-dev-active` マーカーファイル（空ファイル）を作成します。これによりプラグインの PreToolUse hook へ「プロジェクトが正式に開発ハンドオフフェーズへ移行した」と伝え、以降のソースコード書き込みは hook によるリマインドの対象外となります。
3. CLAUDE.md を生成（Claude Codeプロジェクトメモリ）
4. TASKS.md を生成（機能分解 + フェーズリリース + 受入基準）
5. TICKETS.md を生成（チケットリスト）
6. docs/ARCHITECTURE.md を生成（ディレクトリ構造 + DBスキーマ + APIエンドポイント）
7. docs/PRD.md + docs/PRODUCT-SPEC.md を生成
8. scripts/setup.sh を生成（ワンクリック初期化）
9. Claude Codeトランジションガイドを表示

会話にプロダクト企画内容がない場合は、まずプロダクト企画フローを実行するよう促してください。

注：`.product-dev-active` は session-local なマーカーです（プラグインの .gitignore で除外済み）。プロジェクトが純粋な企画モードへ戻る場合はこのファイルを削除してください。
