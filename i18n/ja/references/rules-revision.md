# 🔄 Revision Mode ステップ順序（6 Core + 2 Optional、合計 6〜8 ステップ）

> このファイルは Revision Mode の正式なステップ定義です。SKILL.md からディスパッチされます。

**従来の 12 ステップフロー（v1.0.x）から、重複するフレームワークを統合し、Optional をトリガー条件付きにすることでスリム化しました。** トリガーロジックと Phase 判定ポイントのフォーマットは `references/rules-optional-trigger.md` を参照してください。

## ステップ順序

```
Phase 0：現状分析
  S1.  現状レビュー + JTBD 再検証  [Core]
       （統合：データインベントリ + 既存 Job がうまくいっているか/いないか）

Phase 1：問題の収束
  S2.  ユーザーペインポイント収集  [Core]
       （リテンション/チャーン分析 + フィードバック統合 + 行動データ）
  S3.  ペインポイント + HMW + 機会ランキング  [Core]
       → references/03-define.md
       （統合：ペインポイントサマリー + HMW + 機会評価表）
  S4.  ポジショニング再評価  [Optional — トリガーを参照]
       → references/03-define.md

Phase 2：ソリューション設計
  S5.  PR-FAQ（リビジョン後の体験）  [Core]
       → references/04a-prfaq.md
  S6.  Pre-mortem  [Optional — トリガーを参照]
       → references/04b-solutions.md
  S7.  MVP + Not Doing List  [Core]
       → references/04c-mvp.md

Phase 3：バリデーション
  S8.  North Star + Aha（Before/After 比較） + 仮説検証プラン  [Core]
       → references/05a-northstar-aha.md + references/05c-validation-spec.md
       （統合：いかなるリビジョンも仮説の検証が必須；密結合）

────
最終出力 → プロダクトスペックサマリー（リビジョン版）
```

### S1 プレステップ：プロダクトコンテキスト読み込み

S1 に入る前に、`references/rules-context.md` を読み込み、`.product-context.md` を確認します：

- **完全なコンテキスト（シナリオ 1）**：PMF レベル、North Star、既知のペインポイント、セキュリティステータス、最新 3 件の Decision History を自動反映。S1 を**差分モードのプロンプト**に切り替え：「前回の評価では、PMF レベルが [X]、North Star が [Y] でした。変化はありますか？最新の DAU/MAU とリテンションは？」— 過去の決定事項と既知のペインポイントは再収集不要。
- **コンテキストなし（シナリオ 2）**：Context Bootstrap（`rules-context.md` セクション 4、ラウンド 1 + 3）をトリガーし、その後標準の S1 データ収集に進む。
- **部分的コンテキスト（シナリオ 3）**：Decision History から機能変更履歴を取得（どのモジュールが触られたか、どのリスクが特定されたか）するが、全体的なプロダクト戦略とメトリクスについては質問する（過去は機能拡張のみで、全体像が欠落している）。

### S1 標準プロンプト

> Revision Mode の S1 では、ユーザーに既存プロダクトデータを積極的に求めます：DAU/MAU、リテンション、主要ユーザーフィードバック、過去のバージョンの主要な決定など。コンテキストが一部の回答を事前入力済みの場合は、再収集ではなく確認に切り替えます。
> S1 では現在のセキュリティステータスも収集します：既存の認証/認可メカニズム、既知のセキュリティ脆弱性や技術的負債、最近のセキュリティインシデント。これらのデータはリビジョンのリスク評価と Pre-mortem（トリガー時）に反映されます。

### ファストパス

S1 でユーザーが十分なデータ（フィードバック、メトリクス、優先順位を含む）を提供した場合、S3 を複数回の確認ではなく 1 回の往復で生成可能です。トリガー条件：S2 で収集したペインポイントリストに既に明確な優先順位とデータの裏付けがある。ハードゲートルールは変更なし — 各ステップの出力は完全に提示する必要があり、確認のリズムのみが加速します。

## Optional トリガールール

正式なトリガー条件と Phase 判定ポイントの出力フォーマットは `references/rules-optional-trigger.md` を参照してください。

**クイックリファレンス：**
- **S4 ポジショニング再評価** のトリガー：ユーザーが「ポジショニングのズレ」/「市場の変化」に言及 / オーディエンスに Sales/Marketing が含まれる
- **S6 Pre-mortem** のトリガー：変更スコープが既存機能の 30% 以上 / 決済・権限・データ移行に関わる

## Phase 判定ポイントの要件

Phase 1 と Phase 2 に入る前に、Phase 判定ポイントブロックを表示してください（フォーマットは `rules-optional-trigger.md` で定義）。Phase 0 と Phase 3 は Core ステップのみのため、判定ポイントは省略します。

## リファレンス読み込み指示

| ステップ | リファレンスファイル |
|------|---------------|
| S1〜S2 | （外部リファレンスなし；ユーザーデータの直接収集） |
| S3 | `references/03-define.md` |
| S4（トリガー時） | `references/03-define.md` |
| S5 | `references/04a-prfaq.md` |
| S6（トリガー時） | `references/04b-solutions.md` |
| S7 | `references/04c-mvp.md` |
| S8 + 最終出力 | `references/05a-northstar-aha.md` + `references/05c-validation-spec.md` |

## ステップ数サマリー

| シナリオ | ステップ数 |
|----------|-------|
| デフォルト（Core のみ） | **6** |
| すべての Optional がトリガー | 8 |
| （旧来の 12 ステップフロー） | 12 |

## 最終出力フォーマット

**リビジョンプロダクトスペックサマリー**：Before/After 比較 + 変更すること / 変更しないこと + 成功メトリクス。

サマリーでは、スキップされた Optional ステップを必ず開示し、それらをワンコマンドで補完できるパスを提示してください（`rules-optional-trigger.md` セクション 6 に従う）。

完了後は `references/rules-end-of-flow.md` のエンドオブフロールールに従ってください。
