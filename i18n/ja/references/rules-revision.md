# 🔄 Revision Mode ステップ順序（6 Core + 2 Optional、合計 6〜8 ステップ）

> このファイルは Revision Mode の正式なステップ定義です。SKILL.md からディスパッチされます。

**従来の 12 ステップフロー（v1.0.x）から、重複するフレームワークを統合し、Optional をトリガー条件付きにすることでスリム化しました。** トリガーロジックと Phase 判定ポイントのフォーマットは `references/rules-optional-trigger.md` を参照してください。

## ステップ順序

```
Phase 0: Current State Analysis
  S1.  Current State Review + JTBD Re-validation  [Core]
       (Merged: data inventory + which existing Jobs are done well/poorly)

Phase 1: Problem Convergence
  S2.  User Pain Points Collection  [Core]
       (Retention/churn analysis + feedback synthesis + behavior data)
  S3.  Pain Points + HMW + Opportunity Ranking  [Core]
       → references/03-define.md
       (Merged: Pain Points Summary + HMW + Opportunity Assessment Table)
  S4.  Positioning Re-assessment  [Optional — see triggers]
       → references/03-define.md

Phase 2: Solution Design
  S5.  PR-FAQ (post-revision experience)  [Core]
       → references/04a-prfaq.md
  S6.  Pre-mortem  [Optional — see triggers]
       → references/04b-solutions.md
  S7.  MVP + Not Doing List  [Core]
       → references/04c-mvp.md

Phase 3: Validation
  S8.  North Star + Aha (before/after comparison) + Hypothesis Validation Plan  [Core]
       → references/05a-northstar-aha.md + references/05c-validation-spec.md
       (Merged: any revision must validate hypotheses; tightly coupled)

────
Final output → Product Spec Summary (revision edition)
```

### S1 プレステップ：プロダクトコンテキスト読み込み

S1 に入る前に、`references/rules-context.md` を読み込み、`.product-context.md` を確認します：

- **完全なコンテキスト（シナリオ 1）**：PMF レベル、North Star、既知のペインポイント、セキュリティステータス、最新 3 件の Decision History を自動反映。S1 を**差分モードのプロンプト**に切り替え：「前回の評価では、PMF レベルが [X]、North Star が [Y] でした。変化はありますか？最新の DAU/MAU とリテンションは？」— 過去の決定事項と既知のペインポイントは再収集不要。
- **コンテキストなし（シナリオ 2）**：Context Bootstrap（`rules-context.md` セクション 4、ラウンド 1 + 3）をトリガーし、その後標準の S1 データ収集に進む。
- **部分的コンテキスト（シナリオ 3）**：Decision History から機能変更履歴を取得（どのモジュールが触られたか、どのリスクが特定されたか）するが、全体的なプロダクト戦略とメトリクスについては質問する（過去は機能拡張のみで、全体像が欠落している）。

### S1 標準プロンプト

> Revision Mode の S1 では、ユーザーに既存プロダクトデータを積極的に求めます：DAU/MAU、リテンション、主要ユーザーフィードバック、過去のバージョンの主要な決定など。コンテキストが一部の回答を事前入力済みの場合は、再収集ではなく確認に切り替えます。
> S1 では現在のセキュリティステータスも収集します：既存の認証/認可メカニズム、既知のセキュリティ脆弱性や技術的負債、最近のセキュリティインシデント。これらのデータはリビジョンのリスク評価と Pre-mortem（トリガー時）に反映されます。

### S1 出力要件（Hard Gates）

すべての Revision Mode S1 のレスポンスは、以下の 4 つすべてを必ず含まなければなりません：

1. **0-to-1 ではなく、リビジョンとしてフレーミングする** — 冒頭で 1〜2 文を使い、これが*既存プロダクト*の分析であることを明示する：既存の JTBD を現在のデータに照らして再検証し、ベースラインメトリクスを比較し、過去の決定について `.product-context.md` を読み込んでいる、という点を述べる。これは（ユーザーモデルを白紙から始める）0-to-1 Discovery とは異なる。このフレーミングがないと、ユーザーはなぜ質問が異なるのかを判断できない。

2. **ユーザーの実際の数値をそのまま使う** — ユーザーのプロンプトに含まれる MAU、リテンション低下率（%）、コホートサイズ、日付を、分析の中でそのまま引用して返す（例：「前四半期に 85% から 72% へ低下したこと、2,800 MAU のベースに対して、影響を受けたユーザーはおよそ N 人を意味します…」）。数値を無視した一般論はこのゲートを FAIL する。

3. **ユーザーが述べた原因を事実ではなく H1 として扱う** — ユーザーが有力な原因を挙げた場合（「リテンション低下は機能の複雑さによる」）、それを明示的に H1 とラベル付けし、同じデータから導かれる少なくとも 2 つの対立仮説（H2、H3）を提示する。検討すべき対立仮説の例：コホート構成のシフト、オンボーディングのリグレッション、価格変更、競合のローンチ、サポート品質の低下、機能の廃止、季節要因。**ユーザーが述べた原因を無批判に受け入れることはこのゲートを FAIL する** — Revision Mode の価値は仮説の規律にある。

4. **少なくとも 1 つのセグメンテーション志向のギャップを含むデータギャップリスト** — H1/H2/H3 を識別するために、具体的にどの追加データが必要かを列挙する。**少なくとも 1 項目はセグメンテーションギャップでなければならない**：コホート（登録月）、ティア（無料/有料）、ロール（管理者/ユーザー）、機能利用セグメント。漠然とした「もっとユーザーインタビューを」だけでは FAIL — *どのセグメント*にインタビューするのか、*具体的に何を*聞くのかを名指しする。

### S1 クロージングフォーマット（Hard Gate）

S1 のレスポンスは、オープンエンドの質問ではなく、番号付きの CTA メニューで締めくくる。以下の正確な形を使う：

```
What's next? Pick one:
  1️⃣ Share the requested data so we can move to S2 (pain-point convergence with hypothesis testing)
  2️⃣ Refine the hypothesis list before collecting data (suggest more H_n candidates)
  3️⃣ Skip to S3 if you already have enough data to converge on a top hypothesis
  4️⃣ Pause and resume later (progress will be saved to .product-playbook-progress.md)
```

「Any thoughts?」/「Let me know what you think」/「Share what you have」のように番号付きメニューを欠いた締めくくりは、この契約を FAIL する — ユーザーには次の一手の明確な手がかりが必要。

### ファストパス

S1 でユーザーが十分なデータ（フィードバック、メトリクス、優先順位を含む）を提供した場合、S3 を複数回の確認ではなく 1 回の往復で生成可能です。トリガー条件：S2 で収集したペインポイントリストに既に明確な優先順位とデータの裏付けがある。Hard Gate ルールは変更なし — 各ステップの出力は完全に提示する必要があり、確認のリズムのみが加速します。

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