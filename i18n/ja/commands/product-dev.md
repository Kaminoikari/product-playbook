---
description: 開発ハンドオフパッケージを生成 — CLAUDE.md + TASKS.md + TICKETS.md + ARCHITECTURE.md + setup.sh を作成し、Claude Codeでの開発をすぐに開始可能
---

~/.claude/skills/product-playbook/SKILL.md を読み込んでください。
次に以下のリファレンスファイルを順番に読み込んでください：
1. `references/07a-handoff-core.md`（CLAUDE.mdテンプレート + 技術スタック確認）
2. `references/07b-tasks-tickets.md`（TASKS.md + TICKETS.mdテンプレート）
3. `references/07c-architecture-setup.md`（ARCHITECTURE.md + setup.sh + ユーザーガイダンス）

現在の会話で完成したプロダクト企画内容に基づいて、完全な開発ハンドオフパッケージを生成します：
1. 技術スタックの確認（ユーザーが指定していない場合、プロダクト特性に基づいて推奨）
2. CLAUDE.md を生成（Claude Codeプロジェクトメモリ）
3. TASKS.md を生成（機能分解 + フェーズリリース + 受入基準）
4. TICKETS.md を生成（チケットリスト）
5. docs/ARCHITECTURE.md を生成（ディレクトリ構造 + DBスキーマ + APIエンドポイント）
6. docs/PRD.md + docs/PRODUCT-SPEC.md を生成
7. scripts/setup.sh を生成（ワンクリック初期化）
8. Claude Codeトランジションガイドを表示

会話にプロダクト企画内容がない場合は、まずプロダクト企画フローを実行するよう促してください。
