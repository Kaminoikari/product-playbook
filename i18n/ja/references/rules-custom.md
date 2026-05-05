# ✏️ Custom Mode ステップ順序

> このファイルは Custom Mode の正式なステップ定義です。SKILL.md からディスパッチされます。

完成度レベルを選択（または個別にステップを選択）：

## 🔴 Lean — 4 ステップ

```
S1. JTBD ステートメント → references/02b-jtbd.md
S2. 一つの HMW → references/03-define.md
S3. PR-FAQ → references/04a-prfaq.md
S4. North Star → references/05a-northstar-aha.md
（各ステップはユーザーの希望で別のフレームワークに入れ替え可能）
────
最終出力 → プロダクトスペックサマリー（未実行フィールドは「未実行」と記載）
```

## 🟡 Standard — 8 ステップ（Journey Map が必要な場合は自動的に 9 ステップに拡張）

> Full Mode の 8 ステップサブセット：Full の Core から Strategy Diagnosis を除き、Positioning を追加。Standard ユーザーは通常、深い戦略診断よりも先に市場ポジショニングを必要とするため、この入れ替えになっています。
>
> **Persona-Journey 条件付き挿入**：S1（Persona）完了後、AI は `rules-optional-trigger.md` セクション 2 に従って Persona-Journey 評価を実行します。スキップ条件が成立**しない**場合（Job が複数ステージにまたがる場合）、AI は **能動的に Journey Map を S1.5 として挿入** し、9 ステップ実行となります。ユーザーは `-journey` と返信して 8 ステップに戻すことができます。スキップ条件が成立した場合（単一インタラクションポイント / フロー ≤2 ステップ）、サイレントにスキップして最終出力で開示します。

```
S1.   Persona（表 + カード） → references/02a-persona.md
S1.5  User Journey Map [デフォルトで挿入；状況が単純すぎる場合のみスキップ]
      → references/02c-ost-journey.md
S2.   JTBD 分析 → references/02b-jtbd.md
S3.   ペインポイント + HMW + 機会ランキング → references/03-define.md
S4.   April Dunford Positioning → references/03-define.md
S5.   PR-FAQ → references/04a-prfaq.md
S6.   ソリューション評価（並行 + Pre-mortem + GEM + RICE） → references/04b-solutions.md
S7.   MVP + Not Doing List → references/04c-mvp.md
S8.   North Star + 3 層シグナル + Aha Moment → references/05a-northstar-aha.md
```

## 🟢 Comprehensive — 11 ステップ

> Full Mode の Core + すべてのデフォルト OFF Optional がトリガーされた状態（Positioning + PMF/GTM/BM/Validation）。**S2 Persona の直後に S3 User Journey Map** が続きます（Persona-Journey バンドルルールに従う）。状況が本当に単純な場合は S3 をスキップ可能 — Persona の後に `-S3` と返信すれば 10 ステップに戻せます。

```
S1.  Strategy Diagnosis → references/00-opportunity-check.md + references/01-strategy.md
S2.  Persona（表 + カード） → references/02a-persona.md
S3.  User Journey Map → references/02c-ost-journey.md   ← S2 とバンドル（デフォルト ON）
S4.  JTBD 分析 → references/02b-jtbd.md
S5.  ペインポイント + HMW + 機会ランキング → references/03-define.md
S6.  April Dunford Positioning → references/03-define.md
S7.  PR-FAQ → references/04a-prfaq.md
S8.  ソリューション評価（並行 + Pre-mortem + GEM + RICE） → references/04b-solutions.md
S9.  MVP + Not Doing List → references/04c-mvp.md
S10. North Star + 3 層シグナル + Aha Moment → references/05a-northstar-aha.md
S11. PMF + GTM + BM + 仮説検証プラン → references/05b-pmf-gtm.md + references/05c-validation-spec.md
```

## リファレンス読み込みルール

各リファレンスファイルは、対応するステップに入った時にのみ読み込んでください（すべてのリファレンスを事前読み込みしない）。上記の各ステップにリファレンスパスが注記されています。

## Persona-Journey バンドル

`references/rules-optional-trigger.md` のセクション 2 および 6 に従い、Custom プリセットが Persona ステップを含む場合、Journey Map は **デフォルト ON** です：

- **Comprehensive**：Journey Map は S3 として固定で含まれます（上記の順序に既に含まれている）。Persona の後にユーザーは `-S3` と返信してスキップできます。
- **Standard**：スキップ条件が成立しない場合（複数ステージの Job）、Journey Map は **S1.5** として自動挿入されます。状況が単純すぎる場合（単一インタラクションポイント、フロー ≤2 ステップ、ユーザーがスキップ要求）、Journey Map はサイレントにスキップされ、最終出力で開示されます。
- **Lean**：Persona ステップが存在しないため、このルールは適用されません。

スキップ条件（いずれか 1 つを満たした場合 → Journey をスキップ）：
1. 単一インタラクションポイント（API、単一ボタン、バックエンドサービス、設定ツール）
2. フローが 1〜2 ステップしかない
3. ユーザーが明示的にスキップを要求

## 最終出力フォーマット

**プロダクトスペックサマリー**（完了したステップのみ統合；未実行フィールドは「未実行」と記載）。

完了後は `references/rules-end-of-flow.md` のエンドオブフロールールに従ってください。
