---
description: 機能拡張モード — 既存プロダクトに単一機能を追加、4ステップの効率的フロー
argument-hint: <機能の説明>
---

product-playbook skill を起動してください。
次に references/rules-build.md を読み、「🔧 Feature Extension Quick Path」セクションに直接ジャンプしてください。
各ステップ実行時に、該当セクションで指定されたリファレンスファイルを読み込んでください。

実行モード：🔧 機能拡張モード
機能の説明：$ARGUMENTS

Feature Extension のステップ順序（S1 → S4）に従ってください。まず rules-context.md に従ってプロダクトコンテキストを読み込んでください。各ステップで進捗インジケーターを表示してください。

**S0 → S1 の順序（重要）**：`.product-context.md` が存在しないために Context Bootstrap（S0）がトリガーされた場合、**同じターン内**で Bootstrap と S1 を完了し、**S1 完了後**にユーザーの確認を待って S2 に進んでください。S0 と S1 の間で停止してはいけません — Bootstrap の一部フィールドが欠けていても、プレースホルダーで baseline `.product-context.md` を書き込み、S1 に進み、欠けているフィールドは S1 確認質問の一部として尋ねてください。詳細は `references/rules-context.md`「Bootstrap → S1 の順序」を参照。
