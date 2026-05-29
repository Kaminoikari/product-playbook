# 阶段三：Develop — PR-FAQ（Working Backwards）

## 3.1 Amazon 的逆向工作法（Working Backwards / PR-FAQ）

先写产品新闻稿，强迫你从用户结果出发：

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

> 如果你无法把新闻稿写得让人兴奋，代表这个产品方向可能有问题，需要回头重新定义问题。

### 📝 PR-FAQ 品质自检清单

Claude 产出 PR-FAQ 后必须逐项标记 ✅ 或 ❌，❌ 项目必须说明如何改善：
- [ ] 标题是否从用户角度出发？（「用户能做到 X」vs「我们推出了 Y 功能」）
- [ ] 第一段是否能让读者在 10 秒内理解「这为什么重要」？
- [ ] 痛点描述是否来自真实用户场景？
- [ ] 解法段第一句是否以用户感受/场景开头（非功能动词）？
- [ ] 用户引言是否像真人会说的话？
- [ ] FAQ 是否包含了对比现有工具的尖锐质疑？

**执行规则（Hard Gate）**：
- 必须至少找出 1 个「内部张力」或「值得迭代的地方」，不得全部 ✅ 宣告完成
- 若所有项目都通过，额外说明「这份 PR-FAQ 最脆弱的假设是什么」
- Amazon PR-FAQ 的品质是靠找到问题，不是确认没问题
- ❌ 常见问题：标题像产品公告不像新闻、解法段变成功能列表、FAQ 都是容易回答的问题

---

### ✍️ 解法段落（Body）写作规则

**解法段第一句禁止以功能描述起头。**

❌ 禁止范例：
- 「备料通让你一键输入菜单自动计算食材」
- 「系统会自动根据菜单生成采购清单」
- 「点击『生成清单』按钮即可完成备料规划」

✅ 正确范例：
- 「现在，陈师傅周五下午只需 10 分钟，就能确认周末备料的每一个细节」
- 「张主任不再需要在周五下午翻三份 Excel 才能确定食材够不够」

**公式**：先写用户感受/具体情境 → 然后才说「这是因为 [产品机制]」带出功能。

**自我验证（送出前必做）**：把你自己写的解法段第一句念出声来。如果主语是产品名称、或是「系统」/「这个 App」/「用户可以」，就**重写它**。主语必须是一个具体的行动者（具名的人、角色，或指称某位用户的代词）正在做某件事，或正在经历某个时刻。

---

### 📍 开场段落（Lead）要求

开场段（Aha Moment）必须同时具备以下三项：

1. 一个**具名或具体角色的行动者**（「Alex」、「陈师傅」、「一家 30 座位小餐馆的厨房主管」）——绝不能是泛称的「用户」。
2. 一个**具体的时间／地点／触发点**（「周五下午」、「午餐尖峰过后」、「周末前」）。
3. **至少 2 个具体数字**——数量、时长、金额、百分比。「30 秒内」、「跨 3 种贷款方案」、「每月 $2,400」、「20 分钟的备料窗口」。模糊的数字（「几分钟」、「好几个选项」）不符合此要求，FAIL this requirement。

一个有行动者＋场景但没有具体数字的开场，读起来像行销文案——新闻稿应该让一个具体的结果变得可见，而不是停留在愿景层次。

---

### ❓ FAQ 尖锐质疑标准

**至少 1 个 FAQ 必须是：「为什么不继续用 [现有工具]？」**

回答格式要求：
1. **先正面承认现有工具的优点**（不能否定它）
2. **然后说明 gap**（不是功能不足，而是根本的场景缺口）

❌ 禁止回答模式：「现有工具功能不足，我们更强大」
✅ 正确回答模式：
> 「Excel 确实能记录数字，厨师也早就会用。问题是每次周末前的计算需要重新填表、重新换算，花 1 小时不是因为笨，是因为这个问题就是这么复杂。备料通省的不是 Excel 技能，是每次都要重头算的心理负担。」

---

### 🧪 内部 FAQ 要求

除了对外 FAQ（面向客户）之外，另外产出一个**内部 FAQ** 段落，至少包含：

**Q：这份 PR-FAQ 中风险最高的假设是什么？如果它不成立，什么会让产品死掉？**
A：指出**一个**具体假设（不是列一串）。写得好的答案范例：
- 「我们假设厨房主管会信任自动生成的采购单，不需人工核对。如果他们不信（因为过去库存出错让他们赔过钱），他们会逐行复查，我们『省下 1 小时』的价值主张就崩塌成『省下 5 分钟』。」
- 「我们假设房屋照片的解析度足以可靠地提取坪数。如果基于影像的 OCR 在超过 20% 的房源上失败，核心的『拍一下就走』体验就会崩溃。」

**Q：能推翻这个假设的最小实验是什么？**
A：具体的上线前测试——访谈 N 位用户、用转化目标 X 对落地页做 smoke-test、跑一个为期 2 周的内部试点等等。**笼统的「我们会追踪互动数据」或「我们会观察留存」不符合此要求，FAILS this requirement**——那些是在上线后衡量成功，而不是在投入承诺前推翻假设。

内部 FAQ 不是给客户看的。它的存在是为了逼团队在动手做之前，先讲清楚什么可能让产品死掉。

---

**范例（虚构产品 — 房贷计算 App）：**

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