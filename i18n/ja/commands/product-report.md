---
description: HTML企画レポートを生成 — すべてのプロダクト企画内容を1つのオフライン閲覧可能なHTMLレポートにまとめる
---

~/.claude/skills/product-playbook/SKILL.md と references/06-html-report.md を読み込んでください。

現在の会話で完成したプロダクト企画内容に基づいて、06-html-report.md のデザイン仕様に従い、完全なHTML企画レポートを生成します：
- 単一HTMLファイル（CSS + JSインライン、Google Fonts CDNでNoto Sans JPを読み込み）
- 完了済みステージを動的にレンダリング；未完了ステージはスキップ
- スティッキー目次ナビゲーション、カードベースレイアウト、インタラクティブエフェクトを含む

会話にプロダクト企画内容がない場合は、まずプロダクト企画フローを実行するよう促してください。
