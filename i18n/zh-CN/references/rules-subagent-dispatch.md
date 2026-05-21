# 🤝 Sub-Agent 委派规则

> 在进入任一模式的 S2 时载入（专家委派可能首次套用的步骤）。三个专家 subagent 在独立 context window 中运作——在对的步骤委派，而不是把所有事情塞进 main agent 的 context。

## 何时委派给 `discovery-specialist`

触发条件：
- **Full Mode**：S2（Persona）→ S3（JTBD）→ S4（OST）→ S5（Journey Map）→ S6（Continuous Discovery 假设）
- **Revision Mode**：S2（现状使用者分析）→ S3（痛点综整）→ S4（机会点辨识）
- **Build Mode**：S2（以 JTBD 视角厘清问题）
- **Custom Mode**：任何选用 Persona / JTBD / OST / Journey Map / Continuous Discovery 的步骤

如何调用：

> 使用 `discovery-specialist` subagent 为 [产品描述] 产出 [Persona | JTBD | OST | Journey Map]。目标客群：[B2C / B2B / B2B2C]。可用研究资料：[列出上传的文件，或「无 —— 标记为 low confidence」]。以 [语言] 回复。

将回传的 YAML 整合进步骤输出。在步骤的确认提示中向使用者揭露 `open_questions`。

---

## 何时委派给 `strategy-critic`

在使用者**完成任何策略产物后立即**委派：
- Strategy Blocks 完成后（Full Mode S7）
- Rumelt Good Strategy Kernel 完成后（Full Mode S8）
- DHM Model 完成后（Full Mode S9）
- Empowered Teams charter 完成后（任何模式）
- 任何时候使用者用一般叙述写下「这就是我们的策略」而未指名框架

如何调用：

> 使用 `strategy-critic` subagent 批判以下策略产物：[逐字贴上]。此产物为 [框架名称，或「generic strategy doc」]。以 [语言] 回复。

Critic 回传的是批判，不是改写。把 `three_questions_to_ask_the_writer` 逐字呈现给使用者，不得软化。若使用者据此修订，对修订后版本重新调用 critic。

---

## 何时委派给 `pre-mortem-runner`

触发条件：
- **Full Mode**：S10（MVP scoping 完成后）
- **Build Mode**：S4（architecture-grounded pre-mortem）
- **Revision Mode**：S8
- **Feature Extension Mode**：S3（风险评估）
- 任何时候使用者明确要求 pre-mortem / 风险分析 /「可能会出什么错」

如何调用：

> 使用 `pre-mortem-runner` subagent 对以下 [产品 | 功能 | 策略] 进行 pre-mortem：[逐字贴上]。Mode：[build_mode_architecture_grounded | standard | feature_extension]。若为 build mode，可用的 architecture context：[贴上相关文件内容或摘要]。以 [语言] 回复。

Runner 回传 15+ 个 scenario。在面向使用者的输出中，先呈现 `priority_three` 与 `pre_launch_experiments`。完整 scenario 清单放在可折叠区块或附件。

---

## 委派卫生守则

1. **一个步骤一个 sub-agent**。不要在同一轮串接多个 sub-agent——让使用者先确认中间产物。
2. **明确传递语言**。Sub-agent 从你的 prompt 侦测语言；务必指明使用者的工作语言。
3. **尊重 `status: out_of_scope`**。Sub-agent 的 scope refusal 是一项功能，不是失败——遵循它的路由建议。
4. **Hard Gate 继承**。Sub-agent 继承「规划过程不写 code」规则。即使你要求，它们也会拒绝写档。
5. **品质自检仍适用**。整合 sub-agent 输出后，执行 `rules-quality-review.md` 的品质自检（或使用模式规则档中的内联 6 项清单）。
