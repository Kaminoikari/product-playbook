# フェーズ3：Develop — PR-FAQ（Working Backwards）

## 3.1 AmazonのWorking Backwards手法（PR-FAQ）

プロダクトのプレスリリースを書くことから始めます — 顧客のアウトカムから逆算して考えることを強制します：

```
## [Product Name] Press Release

**Headline**: [What can the user achieve? One sentence.]
**Subheadline**: [What problem does it solve, and for whom?]

**Opening Paragraph (Aha Moment)**:
[Describe the moment the user experiences the product's core value — the "Wow!" moment]

**Pain Point Description**:
[What problem are users facing today? Why aren't current solutions good enough?]

**Solution Description**:
[How does our product solve this problem? (Describe the experience — don't list features)]

**Customer Quote**:
"[A quote from a target user that represents a genuine emotional reaction]"

**FAQ (The Hardest Questions)**:
Q: [The hardest question to answer]
A: [An honest answer]
```

> 人々をワクワクさせるプレスリリースが書けないなら、プロダクトの方向性に欠陥があるかもしれません — 問題定義に戻ってください。

### 📝 PR-FAQ品質チェックリスト

ClaudeはPR-FAQ出力後、各項目に✅または❌を付ける必要があります；❌の項目には改善方法を記載：
- [ ] 見出しはユーザーの視点で書かれているか？（「ユーザーがXをできるようになった」vs「機能Yをリリースしました」）
- [ ] 読者が最初の段落を10秒で読んで「なぜこれが重要か」を理解できるか？
- [ ] ペインポイントの説明は実際のユーザーシナリオから来ているか？
- [ ] ソリューションセクションの最初の文はユーザーの体験/シナリオで始まっているか？（機能の動詞ではなく）
- [ ] 顧客の声は実際の人が言いそうな言葉か？
- [ ] FAQには既存ツールとの鋭い比較が含まれているか？

**実行ルール（Hard Gate）：**
- 少なくとも1つの「内部的な緊張感」または「改善余地のある領域」を特定する必要がある — すべて✅にして完了とすることはできない
- すべての項目が合格した場合、追加で「このPR-FAQの最も脆弱な仮定は何か」を記述
- AmazonのPR-FAQの品質基準は、問題を見つけることから来る、問題がないことを確認することからではない
- ❌ よくある問題：見出しがニュースではなくプロダクト発表に読める、ソリューションセクションが機能リストになる、FAQがすべてソフトボール質問

---

### ✍️ ソリューションセクション（本文）のライティングルール

**ソリューションセクションの最初の文は、機能の説明から始めてはいけません。**

❌ 禁止例：
- 「MealPrepはワンクリックでメニューを入力し、食材を自動計算します」
- 「システムがメニューに基づいて調達リストを自動生成します」
- 「『リスト生成』ボタンをクリックすると、準備計画が完了します」

✅ 正しい例：
- 「今では、陳シェフは金曜の午後に10分だけあれば、週末の仕込みの詳細をすべて確認できます」
- 「張マネージャーはもう3つのExcelシートをめくって在庫が足りるかどうか確認する必要はありません」

**公式**：ユーザーの体験 / 具体的なシナリオから始める → 次に「これが可能なのは[プロダクトの仕組み]のおかげ」で機能を紹介。

**自己検証（送信前に必須）**：自分のソリューション段落の最初の文を声に出して読んでください。主語がプロダクト名や「システム」/「アプリ」/「ユーザーは〜できる」であれば、**書き直してください**。主語は、何かをしている、またはある瞬間を体験している具体的なアクター（名前のある人物、役割、またはユーザーを指す代名詞）でなければなりません。

---

### 📍 リード / 冒頭段落の要件

冒頭段落（Aha Moment）には、以下の3つすべてが含まれていなければなりません：

1. **名前または役割が特定されたアクター**（「アレックス」「陳シェフ」「30席のビストロのキッチンマネージャー」）— 決して漠然とした「ユーザー」ではなく。
2. **具体的な時間 / 場所 / きっかけ**（「金曜の午後」「ランチのピークが終わった後」「週末の前」）。
3. **少なくとも2つの具体的な数字** — 数量、所要時間、金額、パーセンテージ。「30秒以内」「3つの融資シナリオにわたって」「月額2,400ドル」「20分の仕込み時間」。曖昧な数字（「数分」「いくつかの選択肢」）はこの要件をFAILします。

アクターとシナリオはあるが具体的な数字がないリードは、マーケティングコピーのように読めます — プレスリリースは具体的なアウトカムを可視化するものであり、願望を語るものではありません。

---

### ❓ FAQ鋭い質問の基準

**少なくとも1つのFAQは：「なぜ[既存ツール]を使い続けないのか？」であること**

回答フォーマットの要件：
1. **まず既存ツールの強みを認める**（否定しない）
2. **次にギャップを説明**（機能のギャップではなく、根本的なシナリオのギャップ）

❌ 禁止回答パターン：「既存ツールは機能が不足 — 当社はより強力」
✅ 正しい回答パターン：
> 「Excelは確かに数値管理ができますし、シェフたちも使い方を知っています。問題は、毎週末に計算をやり直す必要があることです — 再入力、再変換 — その1時間は誰かがスプレッドシートが苦手だからではなく、問題が本当に複雑だからです。MealPrepはExcelのスキルを節約するのではなく、毎回ゼロからやり直す精神的負担を節約するのです。」

---

### 🧪 内部FAQの要件

外部FAQ（顧客向け）とは別に、少なくとも以下を含む**内部FAQ**セクションを作成します：

**Q: このPR-FAQの最もリスクの高い仮定は何か？それが偽なら、何がプロダクトを殺すか？**
A: 1つの具体的な仮定を挙げる（リストではなく）。よく練られた回答の例：
- 「キッチンマネージャーが自動生成された発注書を手動検証なしで信頼すると仮定している。もし信頼しないなら（過去の在庫エラーで損をした経験から）、彼らは全項目をダブルチェックし、当社の『1時間節約』という価値提案は『5分節約』に崩壊する。」
- 「物件写真には面積を確実に抽出できる十分な解像度があると仮定している。画像ベースのOCRが20%以上の物件で失敗するなら、コアとなる『撮るだけ』の体験は破綻する。」

**Q: この仮定を無効化できる最小の実験は何か？**
A: 具体的なローンチ前のテスト — N人のユーザーにインタビューする、コンバージョン目標Xでランディングページをスモークテストする、2週間の社内パイロットを実施する、など。**漠然とした「エンゲージメントを追跡する」や「リテンションを観察する」はこの要件をFAILします** — それらはローンチ後の成功を測るものであり、コミットメント前の無効化を測るものではありません。

内部FAQは顧客のためのものではありません。チームが構築する前に、何がプロダクトを殺しうるかを自ら名指しすることを強制するために存在します。

---

**例（架空のプロダクト — 住宅ローン計算アプリ）：**

```
## MortgageSnap Helps First-Time Buyers Understand What They Can Afford in 3 Minutes

**Subheadline**: No bank visits, no waiting for rate quotes — figure out your monthly payments with your partner, even at midnight

**Opening Paragraph (Aha Moment)**:
After scrolling through Zillow late at night, Alex spots a house he loves but has no idea if he can
actually afford it. He opens MortgageSnap, screenshots the listing page, and the app automatically
extracts the price and square footage. Within 30 seconds, it shows monthly payments across three
loan scenarios. He shares the results with his wife, and for the first time, they're looking at the
same numbers together.

**Pain Point Description**:
First-time homebuyers comparing mortgage options have to manually enter terms across multiple bank
websites and wait for responses. When you want to run the numbers late at night, there's no
convenient tool — so people end up hacking together an Excel sheet or just giving up.

**Solution Description**:
Now, Alex spends 3 minutes instead of 3 evenings to know what's actually affordable. He snaps a
listing on his phone, sees monthly payments across three lender scenarios appear within 30 seconds,
and shares a single screen with his wife — so the conversation moves from "I think we can afford it"
to "here are the three numbers we should talk about." This works because MortgageSnap automatically
extracts price and square footage from the listing image, then pulls live rate offers from partnered
lenders.

**Customer Quote**:
"I finally don't have to wait for the bank to call back at midnight. Three minutes and I can tell
my wife exactly how much we'd pay each month."

**FAQ**:
Q: There are already tons of mortgage calculators out there — what's different?
A: Existing calculators require you to input interest rates, loan terms, and other parameters, but
most first-time buyers don't even know those numbers. MortgageSnap's difference is that it
automatically pulls in real offers from various lenders — all you need to provide is the price and
your down payment.
```