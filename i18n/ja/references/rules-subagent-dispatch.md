# 🤝 Sub-Agent 委譲ルール

> いずれかのモードの S2 に入る際に読み込まれます（specialist 委譲が適用される可能性のある最初のステップ）。3 つの specialist は独立した context window で動作するため、すべてをインラインで処理するのではなく、適切なステップで委譲してください。

## `discovery-specialist` に委譲するタイミング

トリガー：
- **Full Mode**：S2（Persona）→ S3（JTBD）→ S4（OST）→ S5（Journey Map）→ S6（Continuous Discovery 仮説）
- **Revision Mode**：S2（現状ユーザー分析）→ S3（ペインポイント統合）→ S4（機会の特定）
- **Build Mode**：S2（JTBD レンズによる問題の明確化）
- **Custom Mode**：Persona / JTBD / OST / Journey Map / Continuous Discovery を選択したすべてのステップ

呼び出し方：

> `discovery-specialist` subagent を使用して、[製品説明] の [Persona | JTBD | OST | Journey Map] を作成してください。ターゲット層：[B2C / B2B / B2B2C]。利用可能なリサーチデータ：[アップロードされたファイルを列挙、または「なし — low confidence としてフラグ」]。[言語] で返信してください。

返された YAML を現在のステップの出力に統合します。ステップの確認プロンプトの一部として、specialist の `open_questions` をユーザーに提示してください。

---

## `strategy-critic` に委譲するタイミング

ユーザーが戦略成果物を確定した**直後**に委譲：
- Strategy Blocks 完了後（Full Mode S7）
- Rumelt Good Strategy Kernel 完了後（Full Mode S8）
- DHM Model 完了後（Full Mode S9）
- Empowered Teams charter 完了後（それを含むすべてのモード）
- ユーザーがフレームワーク名を挙げずに「これが我々の戦略だ」と平文で書いたとき

呼び出し方：

> `strategy-critic` subagent を使用して、以下の戦略成果物を批評してください：[そのまま貼り付け]。この成果物は [フレームワーク名、または「generic strategy doc」] です。[言語] で返信してください。

Critic が返すのは批評であり、書き直しではありません。critic の `three_questions_to_ask_the_writer` をそのままユーザーに提示し、和らげないでください。ユーザーが修正した場合、修正版に対して critic を再度呼び出してください。

---

## `pre-mortem-runner` に委譲するタイミング

トリガー：
- **Full Mode**：S10（MVP scoping 完了後）
- **Build Mode**：S4（architecture-grounded pre-mortem）
- **Revision Mode**：S8
- **Feature Extension Mode**：S3（リスク評価）
- ユーザーが pre-mortem / リスク分析 /「何がうまくいかない可能性があるか」を明示的に要求したとき

呼び出し方：

> `pre-mortem-runner` subagent を使用して、以下の [製品 | 機能 | 戦略] に対して pre-mortem を実施してください：[そのまま貼り付け]。Mode：[build_mode_architecture_grounded | standard | feature_extension]。build mode の場合、利用可能な architecture context：[関連ファイルの内容または要約を貼り付け]。[言語] で返信してください。

Runner は 15 個以上の scenario を返します。ユーザー向けの出力では、まず `priority_three` と `pre_launch_experiments` を提示してください。scenario の完全なリストは折りたたみ可能なセクションまたは添付ファイルとして提示します。

---

## 委譲の衛生ルール

1. **1 ステップにつき 1 つの sub-agent**。1 ターンで複数の sub-agent を連鎖させない — ユーザーが中間出力を確認してから次に進む。
2. **言語を明示的に渡す**。Sub-agent はあなたの prompt から言語を検出します。必ずユーザーの作業言語を指定してください。
3. **`status: out_of_scope` を尊重する**。Sub-agent の scope refusal は機能であり、失敗ではありません — そのルーティング推奨に従ってください。
4. **Hard Gate の継承**。Sub-agent は「企画中はコードを書かない」ルールを継承します。あなたが頼んでも、ファイルの書き込みを拒否します。
5. **品質セルフチェックは引き続き適用**。Sub-agent の出力をステップに統合した後も、`rules-quality-review.md` の品質セルフチェックを実行してください（またはモードルールファイル内のインライン 6 項目チェックリストを使用）。
