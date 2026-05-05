# 📦 Full Mode ステップ順序（8 Core + 1 デフォルト ON + 2 Optional、合計 9〜11 ステップ）

> このファイルは Full Mode の正式なステップ定義です。SKILL.md からディスパッチされます。

**従来の 20 ステップフロー（v1.0.x）から、重複するフレームワークを統合し、Optional をトリガー条件付きにすることでスリム化しました。** トリガーロジックと Phase 判定ポイントのフォーマットは `references/rules-optional-trigger.md` を参照してください。

**Journey Map（S3）に関する注記**：デフォルト ON。Persona-Journey は、プロダクトが 0-to-1 か既存プロダクトかに関わらずバンドルされたペアです — 関連する変数はユーザーの Job が複数ステージにまたがるかどうかです。状況が本当に単純な場合（単一の API/ボタン、フローが ≤2 ステップ、またはユーザーが明示的にスキップを要求）にのみスキップしてください。

## ステップ順序

```
Phase 0：Strategy
  S1.  Strategy Diagnosis  [Core]
       → references/00-opportunity-check.md + references/01-strategy.md
       （統合：Opportunity + DHM + Strategy Blocks + Rumelt Kernel）

Phase 1：Discovery
  S2.  Persona（表 + カード）  [Core]
       → references/02a-persona.md
  S3.  User Journey Map  [デフォルト ON — 状況が単純すぎる場合のみスキップ]
       → references/02c-ost-journey.md
  S4.  JTBD 分析  [Core]
       → references/02b-jtbd.md

Phase 2：Define
  S5.  ペインポイント + HMW + 機会ランキング  [Core]
       → references/03-define.md
       （統合：ペインポイントサマリー + HMW + 機会評価；
        OST ツリーの可視化はこのステップ内のオプションのサブフォーマット）
  S6.  April Dunford Positioning  [Optional — トリガーを参照]
       → references/03-define.md

Phase 3：Develop
  S7.  PR-FAQ（Working Backwards）  [Core]
       → references/04a-prfaq.md
  S8.  ソリューション評価  [Core]
       → references/04b-solutions.md
       （統合：並行プロトタイプ + Pre-mortem + GEM + RICE）
  S9.  MVP + Not Doing List  [Core]
       → references/04c-mvp.md

Phase 4：Deliver
  S10. North Star + 3 層シグナル + Aha Moment  [Core]
       → references/05a-northstar-aha.md
  S11. PMF + GTM + ビジネスモデル + 仮説検証プラン  [Optional — トリガーを参照]
       → references/05b-pmf-gtm.md + references/05c-validation-spec.md

────
最終出力 → プロダクトスペックサマリー（references/05c-validation-spec.md → 4.6） + 最適エントリーポイント分析
```

> オーディエンスが経営層またはクロスファンクショナル連携の場合、S10 の前に Empowered Teams フレームワークを追加してください。

## Optional トリガールール

正式なトリガー条件と Phase 判定ポイントの出力フォーマットは `references/rules-optional-trigger.md` を参照してください。

**クイックリファレンス：**
- **S3 Journey Map**（デフォルト ON）：単一インタラクションポイント / フロー ≤2 ステップ / ユーザーがスキップ要求の場合を除き実行
- **S6 Positioning**（デフォルト OFF）：新プロダクトのローンチ / リポジショニング / オーディエンスに Sales-BD-Marketing が含まれる場合にトリガー
- **S11 PMF/GTM/BM/Validation**（デフォルト OFF）：プロダクトの市場投入 / オーディエンスが経営層またはデータサイエンティスト / ユーザーが検証プランを要求した場合にトリガー

## Phase 判定ポイントの要件

Phase 1、Phase 2、Phase 4 に入る前に、Phase 判定ポイントブロックを表示してください（フォーマットは `rules-optional-trigger.md` で定義）。Phase 0 と Phase 3 は Core ステップのみのため、判定ポイントは省略します。

## リファレンス読み込み指示

各リファレンスファイルは、対応するステップに入った時にのみ読み込んでください（すべてのリファレンスを事前読み込みしない）：

| ステップ | リファレンスファイル |
|------|---------------|
| S1 | `references/00-opportunity-check.md` + `references/01-strategy.md` |
| S2 | `references/02a-persona.md` |
| S3（トリガー時） | `references/02c-ost-journey.md` |
| S4 | `references/02b-jtbd.md` |
| S5 | `references/03-define.md` |
| S6（トリガー時） | `references/03-define.md` |
| S7 | `references/04a-prfaq.md` |
| S8 | `references/04b-solutions.md` |
| S9 | `references/04c-mvp.md` |
| S10 | `references/05a-northstar-aha.md` |
| S11（トリガー時） | `references/05b-pmf-gtm.md` + `references/05c-validation-spec.md` |
| 最終出力 | `references/05c-validation-spec.md` |

## ステップ数サマリー

| シナリオ | ステップ数 |
|----------|-------|
| デフォルト（8 Core + S3 Journey ON） | **9** |
| シンプルなフロー（S3 スキップ） | 8 |
| デフォルト OFF Optional の 1 つトリガー（S6 または S11） | 10 |
| すべての Optional がトリガー | 11 |
| （旧来の 20 ステップフロー） | 20 |

## 最終出力フォーマット

**最適エントリーポイント分析**（完全な推論チェーン）+ **プロダクトスペックサマリー**

プロダクトスペックサマリーでは、スキップされた Optional ステップを必ず開示し、それらをワンコマンドで補完できるパスを提示してください（`rules-optional-trigger.md` セクション 6 に従う）。

完了後は `references/rules-end-of-flow.md` のエンドオブフロールールに従ってください。
