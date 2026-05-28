# 阶段一：Discovery — Persona 建立

### 🚫 Discovery 输出范畴（Hard Gate）

当 orchestrator 被要求执行 Discovery 工作(Persona、JTBD、OST、Journey Map、Continuous Discovery)时,输出必须**停留在 Discovery 范畴内**。Discovery 回答「用户是谁」「他们想满足的未被满足需求」——仅此而已。下列下游阶段的产出绝对**不可**出现在 Discovery 交付物中,即使顺手感觉合理:

- **Define 阶段产出**:positioning statement、HMW(How Might We)问题、可被解读为解法提示的痛点矩阵
- **Develop 阶段产出**:PR-FAQ 草稿、pre-mortem 情境、RICE 表格、MVP scope 定义、PRD 段落、功能列表
- **Deliver 阶段产出**:North Star 指标定义、PMF 判准、GTM 计划、商业模式区块、产品规格表
- **Strategy 阶段产出**:Strategy Blocks、Rumelt 的 diagnosis / guiding-policy / coherent-action、DHM Model 拆解、OKR 阶层

若 Discovery 发现明显指向某个下游产出(例如 JTBD 浮出清晰的 positioning 角度),可在文末以**一行 open question 或 next-step pointer** 记录——但**不要**自己产出该产出。下个阶段在规划流程中有专属步骤负责它。

不合格范例:JTBD 分析结尾附上填好的 RICE 表、MVP scope 列表、或一段「Recommended Positioning」——即使前面 Discovery 子段都正确,这个输出仍 FAIL 此 Hard Gate。

---

## Continuous Discovery 习惯（Teresa Torres）

建立一个关键习惯：**每周至少接触一位目标用户**。Discovery 不是一次性仪式，而是持续系统。

> 「Product discovery 应该是持续的习惯，而不是专案开始前的一次性仪式。」— Teresa Torres

## 1.1 建立 Persona Table

Persona 不是用年龄性别来分群，而是用「用途 / 任务 / 动机」来区分不同类型的用户。

### 🏢 B2B Hard Gate — 买方 Persona ≠ 使用者 Persona

对于任何 B2B(或 B2B2C)产品,**买方(Buyer)**(签合约、掌预算、扛供应商风险)与**日常使用者(User)**(每天接触产品)几乎都是**目标、痛点、决策准则完全不同**的两个角色。把他们合并成同一个 Persona 等于把两个不同的 Job 强塞进一个模糊原型,分析结果无法驱动产品决策。

Hard Gate 规则:
- B2B 预设要产出**两个独立的 Persona 区块**,标示为 `Buyer` 和 `User`,当两个角色明显不同(B2B 的预设假设)。
- 若为同一个人(少数例外——通常是创办人主导的工具或独资 B2B),请用一句话明确说明「为何此场景中买方就是日常使用者」。
- 两个 Persona 之间要交叉连结:标出买方的评估准则何处依赖使用者的日常行为(例如「买方的稽核就绪准则取决于使用者是否当天填假单,而不是事后补登」)。

不合格范例:只产出一个 Persona(「HR 经理」),把「核定预算」和「每天填假单」这两个不同的 Job 硬塞进同一个模糊原型——这个输出 FAIL 此 Hard Gate。

```
| 栏位 | Persona 1: [暱称] | Persona 2: [暱称] | Persona 3: [暱称] |
|---|---|---|---|
| 用途 / 任务 / 动机 | | | |
| 规模（SIZE） | | | |
| 问题 / 挑战 / 驱动力 | | | |
| 现在做法与理由 | | | |
| 频率 | | | |
| 相关资讯来源 | | | |
| 采用/执行过程的问题 | | | |
```

说明切分逻辑；检查是否 MECE（互斥且完整覆盖）；指出核心 TA 和次要 TA。

### 🎯 Persona 优先排序 reasoning（Hard Gate）

只说「指出核心 TA」而没有具体 reasoning 不符合此 Hard Gate。优先排序的陈述必须指出**一个** Persona 为核心,并用**该产品 go-to-market 动态的具体语言**解释为什么——而不是泛泛的「使用频率高」这类理由。

**B2B 产品**若有多个 user persona,reasoning 必须**至少引用一个**下列 B2B 专属动态(用这些词汇或显然等价的概念):

- **Champion vs Buyer** — 谁在组织内倡导采用 vs 谁签合约;champion-led adoption 通常在 B2B 优先序中胜出,即使 buyer 是「更资深」的 persona
- **Adoption multiplier** — 谁的采用会解锁整个组织的扩散(例如 HR Specialist 每日使用会种下其他 persona 后续依赖的 system-of-record)
- **Switching-trigger ownership** — 哪个 persona 感受到让组织从既有工具切换的痛;拥有 switching trigger 的 persona 即使不是最重使用者,也是优先序候选
- **Budget authority** — 谁掌控预算项目;当 buyer ≠ user 时相关,买方的评估准则主导初始成交决策
- **Audit / compliance pressure ownership** — 稽核发现出事时谁的角色受影响;在 regulated B2B segment 中,承受合规压力的 persona 通常主导优先序

纯粹「Persona X 使用频率更高」或「Persona Y 用户数更多」的 reasoning 对 B2B 产品 FAIL 此 Hard Gate。频率是必要条件、非充分条件——B2B 切换由组织压力驱动,不是个别使用率。

**B2C 产品**的 reasoning 至少引用一个:switching-trigger ownership、JTBD severity differential、network-effect seeding、willingness-to-pay differential。纯频率 reasoning 对 B2C 也 FAIL。

### 📝 Persona 品质自检清单
- ✅ 切分是否基于「用途/任务/动机」而非人口统计？
- ✅ 各 Persona 之间是否 MECE（互斥且完整覆盖目标市场）？
- ✅ 是否明确指出核心 TA vs 次要 TA？
- ✅ 每个 Persona 的「问题/挑战」是否来自真实观察或合理推论？
- ✅ 「现在做法与理由」是否具体到可以识别 Workaround？
- ❌ 常见问题：按年龄性别分群、Persona 之间差异不明显、痛点太笼统

## 1.2 建立 Persona 卡片

```
## [Persona 暱称]：[一句话描述]

**基本资讯**：年龄 / 性别 / 职业 / 所在地 / 个性特质
**背景**：[与产品相关的背景描述]
**目标 / 任务**：[目标1]、[目标2]
**现行做法与理由**：[目前怎么做、为什么这样做]
**资讯来源**：[从哪里获取相关资讯]
**阻碍 / 问题 / 挑战 / 不满意**：[痛点1]、[痛点2]、[痛点3]
```

---

## 📎 本阶段的文件整合提示

如果使用者在此阶段上传了文件，Claude 依据以下规则整合：

| 上传内容 | 整合到 | 整合动作 |
|---------|-------|---------|
| 用户访谈逐字稿 / 录音文字 | 1.1 Persona + 1.3 JTBD | 提取：用户背景 → Persona 栏位；痛点 + 现行做法 → JTBD 深挖五问；情绪反应 → 情感性/社交性 Job |
| 用户调研报告（PDF） | 1.1 + 1.2 + 1.3 | 提取量化数据（用户分群比例）填入 Persona 规模；提取质化洞见填入 JTBD |
