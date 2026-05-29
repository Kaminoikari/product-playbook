# 📦 プロダクトコンテキスト蓄積ルール

> SKILL.md 起動時に読み込まれます。すべての判断ロジック（いつ／どれを／どう）を含みます。詳細な YAML フォーマットと UX スクリプトは `rules-context-template.md` にあり、ファイルを実際に書き込む時や Bootstrap 実行時のみ遅延読み込みされます。

## 1. ファイルライフサイクル

- **パス**：プロジェクトルートディレクトリの `.product-context.md`（`.product-playbook-progress.md` と同じレベル）
- **永続保持**：セッションを跨いで保持
- **初回作成時**：ユーザーに `.gitignore` への追加をリマインド（機密戦略情報を含む可能性）

**Bootstrap 開始アナウンス（Hard Gate — 情報収集を始める前に必須）：** Bootstrap の最初のユーザー向けメッセージは、(a) 取得した情報が今後のセッションのために保存されること、AND (b) 正確なパス `.product-context.md` の両方を明示しなければなりません。文言例：

> 今後のセッションのためにプロダクトコンテキストをセットアップします — 取得した内容をプロジェクトルートの `.product-context.md` に保存し、以降の実行では基本事項の再質問をスキップできるようにします。

これは交渉の余地がありません：Bootstrap のファイル書き込みが後でパーミッションゲートや中断に遭遇しても、ユーザーには事前にパスが伝えられている必要があります。完了時のみパスに言及する（「✅ .product-context.md に保存しました」）方式は、完了が訪れなかった場合に破綻します。

---

## 2. 3 シナリオ検出（起動時）

進捗ファイルチェック後、モード選択前に実行：

| 条件 | シナリオ | アクション |
|-----------|----------|--------|
| ファイル存在、`Core Strategy` に実内容あり | **1. 完全** | サイレント読み込み。表示：「📦 **[プロダクト名]** のプロダクトコンテキストを検出 — 今回のセッションのベースラインとして使用します。」 |
| ファイル不在 | **2. なし** | 状態を記録。機能拡張／リビジョン突入時に Bootstrap をトリガー。→ template §Bootstrap を読み込み |
| ファイル存在、Core Strategy 空/プレースホルダー、Decision History に ≥1 エントリ | **3. 部分的** | 既知情報サマリー + 補完オプションを表示。→ template §Partial を読み込み |

**検出ロジック**：
1. ファイルは存在するか？
2. `Identity` に Product name があるか（プレースホルダーではなく）？
3. `Core Strategy` に Core JTBD があるか（プレースホルダーではなく）？→ はい = シナリオ 1
4. `Decision History` に `###` エントリがあるか？→ はいだが 3 がいいえ = シナリオ 3

---

## 3. コンテキスト自動読み込みルール（各モードの S1 プレステップ）

**関連セクションのみ注入** — ファイル全体をユーザーに表示しない：

| モード + ステップ | 注入セクション |
|-------------|------------------|
| 機能拡張 S1 | Identity、Architecture & Tech Stack、最新 3 件の Decision History |
| リビジョン S1 | Identity、Core Strategy、Accumulated Insights（ペインポイント、PMF、セキュリティ）、最新 3 件の Decision History |
| Full/Quick/Build S1 | Identity のみ（プロダクト名、タイプ、ワンライナー） |
| 任意モードの Pre-mortem | Security posture + Technical debt（Accumulated Insights から） |

**肥大化制御**：Decision History はデフォルトで最新 3 件のみ注入。ユーザーは追加リクエスト可能。

---

## 4. 空セクションスキップルール

| セクション | 機能拡張 | リビジョン | Full/Quick/Build |
|---------|------------------|----------|-----------------|
| Identity | 必須（欠落時は Bootstrap） | 必須（欠落時は Bootstrap） | フロー自体が生成 |
| Core Strategy | スキップ可能 | 必須（欠落時は S1 内でクイック Q&A 収集） | フロー自体が生成 |
| Architecture & Tech Stack | 必須（欠落時は Bootstrap または自動検出） | スキップ可能 | フロー自体が生成 |
| Decision History | スキップ可能 | あれば含める、なければスキップ | フロー自体が生成 |
| Accumulated Insights | スキップ可能 | あれば含める、なければスキップ | フロー自体が生成 |

**原則**：空セクションはフローをブロックしない。「必須」かつ空の場合のみ収集をトリガー。

---

## 5. コンテキスト自動書き込みルール（フロー終了時）

`rules-end-of-flow.md` の終了条件と同期。コンテキストを自動抽出：

| フロータイプ | 書き込み/更新セクション |
|-----------|-------------------------|
| Quick | Identity、Core Strategy（JTBD + North Star）、History 追加 |
| Full | 全セクション（Identity/Strategy/Insights を上書き、History 追加） |
| Revision | Core Strategy 更新（リポジショニングした場合）、Insights 更新、History 追加 |
| Feature Extension | Architecture をマージ、History 追加（機能テンプレート） |
| Custom | 完了ステップに対応するセクションを更新 |
| Build | Identity、Core Strategy（部分的）、History 追加 |

### セクション別書き込み戦略

| セクション | 戦略 |
|---------|----------|
| Identity | 最新で上書き |
| Core Strategy | 最新で上書き（リビジョン後がリビジョン前を置換） |
| Architecture & Tech Stack | マージ（新モジュール追加、古いものは保持） |
| Decision History | 追加のみ（過去エントリを削除しない） |
| Accumulated Insights | マージ＆重複排除（ペインポイント/フィードバックは重複排除；PMF/Security は上書き） |

初回書き込み時（ファイル作成）または Decision History 追加時 → **`rules-context-template.md` §File Format / §Append Templates を読み込み**。

完了表示：`✅ プロダクトコンテキストが '.product-context.md' に更新されました — 次回セッションで自動読み込み。`

---

## 6. コンフリクト処理（サマリー）

| コンフリクト種別 | 解決 |
|---------------|-----------|
| ユーザーが既存コンテキストを修正 | 最新優先 — 直接上書き |
| コンテキストとコードベースのコンフリクト（例：package.json と異なる） | 自動上書きしない — ユーザーに確認。→ template §Conflict UX を読み込み |
| フローデータが古いコンテキストと異なる | フローデータ優先 — フロー終了時に自動上書き |

---

## 7. 言語設定（サマリー）

コンテキスト作成/更新時に `Language Preference` セクションに記録：
- **インストール言語**：`.lang` ファイルまたはユーザーロケールから
- **ユーザーの希望言語**：ユーザーがコミュニケーションに使用する言語

読み込み時：記録があればその言語でセッション継続。
書き込み時：Bootstrap 時、またはファイルを初めて作成するフロー終了時。ユーザーがセッション途中で言語切り替え時に更新。

---

## 8. `rules-context-template.md` を読み込むタイミング

以下のいずれか 1 つがトリガーされた時のみ：

| トリガー | テンプレートセクション |
|---------|------------------|
| シナリオ 2 + 機能拡張／リビジョン突入 | §Bootstrap、§File Format |
| シナリオ 3（部分的コンテキスト） | §Partial Context、§File Format |
| コンテキスト初回書き込み | §File Format |
| フロー終了時に Decision History 追加 | §Append Templates |
| コードベースのコンフリクト検出 | §Conflict UX |
| Bootstrap 完了 → baseline 書き込み | §File Format |

起動時にテンプレートを事前読み込み**しないこと**。