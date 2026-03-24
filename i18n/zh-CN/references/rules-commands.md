# 🔧 框架选单 + 补充指令

> 当使用者要求「列出框架」「给我看有哪些框架」或使用补充指令时载入。

## 指定框架

**触发方式有两种：**

**方式 A（使用者直接说框架名称）：** 直接进入该框架引导流程，不需要再问。

**方式 B（使用者说「我想指定框架」「列出所有框架」等）：** 呈现以下选单：

```
📚 可指定的框架清单，请填写编号或名称：

【理解用户】
 1. JTBD（Jobs to Be Done）— 找出用户真正想完成的工作
 2. Persona — 建立用途/任务/动机导向的用户角色
 3. User Journey Map — 绘制用户完整体验旅程
 4. Continuous Discovery — 建立每周接触用户的持续习惯

【定义问题】
 5. OST / 机会解法树 — 系统化链接机会与解法
 6. Positioning / April Dunford — 找出真正的竞争场域和差异化
 7. HMW — 将痛点转化为设计问题

【解法设计】
 8. Working Backwards / PR-FAQ — 从用户结果出发倒推解法
 9. Pre-mortem / 事前验尸 — 在失败前预测并预防失败
10. GEM — Growth / Engagement / Monetization 三维优先排序
11. RICE — 量化功能优先排序
12. MVP — 定义最小可行产品范围

【策略层】
13. Strategy / Strategy Blocks — Mission → Vision → Strategy 层级结构
14. DHM Model — Delight / Hard to copy / Margin-enhancing 机会检验
15. LNO Framework — Leverage / Neutral / Overhead 时间分配
16. Empowered Teams — 赋能型团队 vs 功能型团队

【衡量层】
17. North Star / 北极星指标 — 定义代表核心用户价值的单一指标
18. PMF — 判断产品市场契合度的四个等级
19. Sean Ellis Score — 量化 PMF 热情程度

【商业层】
20. 商业模式与定价 — 收费模式选择与价值定价对齐
21. GTM 策略 — Go-to-Market 上市与获客策略

【开发衔接】
22. Dev Handoff / 开发交接包 — 产出 CLAUDE.md + TASKS.md + TICKETS.md，衔接 Claude Code 开发

请输入框架编号或名称（可多选，用逗号分隔）：
```

## 跳过 Discovery / 直接进实作

当使用者说「跳过用户研究」「问题已知」「直接进到 Develop」时，读取 `references/rules-build.md` 并依照直接实作模式步骤序列执行。

> 提醒使用者：「跳过用户研究阶段，代表解法建立在假设上。建议执行后尽快进行 Continuous Discovery 验证。」

## 功能扩充模式触发

- 「新增功能」/「我要在现有产品加一个功能」/「加新功能」→ 触发功能扩充模式（读取 `references/rules-build.md` → 功能扩充快速路径）

## 补充指令

| 指令 | 行为 |
|------|------|
| `「切换到 [框架]」` | 立即切换，保留已完成内容 |
| `「我想改变目标对象」` | 重新调整框架优先序和呈现方式 |
| `「跳过这个步骤」` | 提醒必要性后尊重决定，进入下一步 |
| `「回到 [步骤/框架名称]」` | 回到指定的任意步骤重新引导（见 `references/rules-change-propagation.md`） |
| `「帮我简化」` / `「帮我展开」` | 浓缩核心要点 / 深入补充分析 |
| `「产出报告」` | 读取 `references/06-html-report.md`，产出 HTML 企划报告 |
| `「产出 PRD」` / `「产出给工程师的文件」` | 读取 `references/04b-solutions.md`，整合 PR-FAQ + MVP + User Story + Pre-mortem，**自动一并产出：流程图（Mermaid）+ DB schema（Mermaid ERD）+ UI wireframe（HTML）** |
| `「产出流程图」` / `「帮我画流程图」` | 以 Mermaid 语法产出流程图（单独触发） |
| `「产出 DB schema」` / `「帮我设计数据库」` | 产出 DB schema（Mermaid ERD 语法）（单独触发） |
| `「产出 UI wireframe」` / `「帮我画线框图」` | 以 HTML/SVG 产出低保真 UI 线框图（单独触发） |
| `「产出简报」` / `「帮我做成 PPT」` | 呼叫系统 pptx skill |
| `「把文件调整成给 [对象] 看的版本」` | 重新编排框架重点和呈现语言 |
| `「我只有 15 分钟」` | 给出最关键的三个决策问题或行动 |
| `「帮我做完整性评估」` | 评估哪些环节完整、哪些有风险 |
| `「帮我找出假设」` | 识别所有尚未验证的核心假设清单 |
| `「做一次 Pre-mortem」` | 对任何解法立即进行事前验尸 |
| `「产出给不同对象的版本」` | 自动产出多个对象版本的摘要 |
| `「这个产品在 PMF 哪个等级？」` | 判断 PMF 等级并说明下一步里程碑 |
| `「帮我找出瓶颈」` | 分析最影响 Aha Moment 到达率的障碍 |
| `「我要改版，不是新产品」` | 切换改版模式（读取 `references/rules-revision.md`） |
| `「我要说服老板批准」` | 切换老板模式，突出商业价值和资源逻辑 |
| `「进入开发」` / `「产出开发交接包」` | 读取 `references/07a-handoff-core.md`，确认技术栈后产出完整开发交接包 |
| `「帮我建专案」` / `「接到 Claude Code」` | 同上 |
| `「暂停」` / `「存档」` / `「先做别的」` | 依 `references/rules-progress.md` 存档 |
| `「继续」` / `「回到企划」` | 依 `references/rules-progress.md` 恢复 |
| `「清除进度」` / `「重新开始」` | 删除进度文件，从头开始 |
| `/export [format]` | 导出为指定格式。format = `pdf` / `docx` / `pptx` / `html` / `md`。读取 `references/rules-export-document.md`，首次使用时先载入 `references/rules-document-tools.md` 检查工具。 |
| `/parse [file]` | 解析上传的文件为 Markdown。支持 PDF / DOCX / PPTX / 图片。读取 `references/rules-import-document.md`，首次使用时先载入 `references/rules-document-tools.md` 检查工具。 |

**上下文相关指令提示**：每个步骤完成时，根据当前进度主动提示 2-3 个最相关的可用指令。
