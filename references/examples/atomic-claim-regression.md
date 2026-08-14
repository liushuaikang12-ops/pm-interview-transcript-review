# Atomic Claim Audit 回归测试 — Q03 / Q03.1（AI Product）

> 本文件是修复后的 Atomic Claim Audit 回归测试，非真实面试，不更新历史。
> 输入：`simulated-transcript.md`、`simulated-resume.md`（均为虚构测试数据）。
> 范围：仅 Q03 / Q03.1 的 AI Product 回答，Mode C — Answer Critique。
> 测试陷阱：Resume 只证明候选人「做过用户访谈和产品原型」，未证明用户说过「不会描述需求」；不得把后者写进 Suggested Answer 的既有事实。

---

## 0. Q&A Anchor（仅本次诊断涉及的节点）

| ID | Surface Question | 时间戳 | 能力标签（推断） |
|---|---|---|---|
| Q03 | 说说你对 AI 写作产品的理解。怎么提高用户第一次生成成功率？ | [00:15:20] | AI-native Product Thinking, Model Evaluation, Failure Recovery |
| Q03.1 | 你说的「成功」怎么定义？失败以后怎么 recovery？ | [00:16:35] | Model Evaluation, Failure Recovery, AI UX |

- Q03 Underlying Intent（推断，Confidence: High）：验证候选人是否理解「生成成功率」不是口号问题，而是一个需要定义成功、诊断失败原因、设计机制与评估的 AI 产品问题。
- Q03.1 追问触发（推断，Confidence: High）：Q03 首答未定义「成功」，故追问定义与 recovery——即 concern 未解除的典型信号。

---

## 1. Evidence（证据账本）

### F1 — Transcript Fact（原话明确出现）

- `[00:15:29–00:16:32]` Candidate：「AI 产品首先要解决真实用户问题，不能为了 AI 而 AI。体验要简单，Prompt 要写好，模型能力也很重要。可以优化输入框和引导，让用户更容易使用，也可以换更好的模型，这样第一次生成成功率就会提升。」
- `[00:16:46–00:17:20]` Candidate：「成功就是用户觉得好用。失败可以让用户重新生成，或者给一些模板。具体指标我还没有系统想过。」

### F2 — Corroborated Fact（Transcript 与简历一致）

- 校园 AI 写作助手：简历写「与 3 人团队完成课程项目，负责用户访谈和产品原型」。
- 简历明确注明：「未提供模型选型、evaluation、上线用户量或留存数据」。

### 关键缺口（Insufficient Evidence）

- 无任何证据证明：用户在访谈中说过「不会描述需求」「不知道怎么用」「不知道怎么表达需求」等具体洞察。
- 无任何证据证明：候选人定义过「生成成功」的可测量口径，或做过模型评估 / 失败分类 / recovery 机制设计。

> 结论：Resume 的「做过用户访谈和产品原型」**只**证明「做过访谈动作 + 做过原型动作」，不蕴含任何访谈结论。这是本回归测试的核心约束。

---

## 2. 五维动态评分

Weight Profile：**AI Product Mechanism**（S .30 / Str .15 / R .20 / C .20 / D .15）。
Confidence：Medium（模拟数据，但 transcript 完整、带时间戳、单面试官，speaker 可靠）。

### Q03 — AI 写作产品理解 + 提高首次生成成功率

| 维度 | 分 | Evidence 依据 |
|---|---|---|
| Substance | 3 | 只有「解决真实问题 / 体验简单 / Prompt 写好 / 模型重要」等口号；无成功定义、无失败原因诊断、无评估、无 HITL / retry / edit cost 机制。 |
| Structure | 4 | 散点列举，缺「定义成功 → 诊断失败 → 机制 → 评估」逻辑链。 |
| Relevance | 4 | 提及输入框 / 引导 / 模型，但未直接回答「如何提高首次成功率」的核心（定义 + 诊断 + 评估）。 |
| Credibility | 3 | 未引用任何个人 AI 项目证据；「换更好的模型」是无来源的常识断言；简历的 AI 项目无 evaluation / 数据。 |
| Differentiation | 2 | 「换更好的模型」是任何候选人都会说的，无独有判断、无 trade-off、无边界。 |

- Raw = 3×.30 + 4×.15 + 4×.20 + 3×.20 + 2×.15 = **3.2**
- Cap 命中：「回答只给正确口号、无岗位机制」→ Overall ≤ 5.0（不触发更低上限）。
- **Overall = 3.2 / 10**（`AI Product Depth Insufficient`，Differentiation ≤ 5 已符合）。

### Q03.1 — 成功定义 + recovery

| 维度 | 分 | Evidence 依据 |
|---|---|---|
| Substance | 2 | 「用户觉得好用」不是可测量指标；明确承认「具体指标我还没有系统想过」。 |
| Structure | 3 | 无「定义 → 失败诊断 → recovery」逻辑链，仅两个孤立动作。 |
| Relevance | 3 | 部分回答 recovery（重新生成 / 模板），但回避了「成功怎么定义」这一追问核心。 |
| Credibility | 2 | 明确自陈无系统指标思考，无任何数据支撑。 |
| Differentiation | 2 | 无。 |

- Raw = 2×.30 + 3×.15 + 3×.20 + 2×.20 + 2×.15 = **2.35**
- Cap 命中：「只给正确口号、无岗位机制」→ ≤ 5.0；未命中「没有回答」（candidate 部分回答了 recovery），故不压到 2.0。
- **Overall = 2.4 / 10**。

---

## 3. Root Cause

### Finding — Q03/Q03.1 把 AI 产品问题当通用产品问题答

- Frequency: 1（Q&A node：Q03 与 Q03.1 属同一失败链，按同一回答链计 1 次，不重复计）
- Evidence: `[00:15:29–00:16:32]`、`[00:16:46–00:17:20]`
- What happened: 用「解决真实需求 + 体验简单 + 好模型」覆盖「如何提高首次生成成功率」；被追问「成功怎么定义 / 怎么 recovery」后，给出主观定义并自陈「指标还没系统想过」。
- Root Cause:
  - Primary: `RC-AI-NO-EVAL` — 未说明 evaluation 与 failure handling，把「成功率」当成静态结果而非需要定义、评估、迭代的机制问题。
  - Secondary: `RC-AI-CONCEPTUAL`（停留口号）、`RC-NO-INSIGHT`（无任何真实用户洞察支撑机制选择）。
- Gap Type: **Knowledge Gap**（缺 AI 成功定义 / 失败 taxonomy / evaluation 机制）叠加 **Capability Gap**（缺「定义成功 → 诊断失败 → 机制 → 评估」的判断框架）。**不是 Communication Gap**——「指标没系统想过」表明思考本身缺失，而非表达失效。
- Why it matters（推断）: 面试官在 [00:19:41] 明确岗位要求「和算法一起定义生成质量评估」「理解输入→生成→编辑→发布完整链路，不只做活动」，候选人在这两题上的表现恰好落在岗位最看重的机制与评估盲区。
- Better approach: 先把「成功」定义成可测量口径，再拆失败原因假设，逐条给机制并用实验验证（见下节）。

---

## 4. Recommended Structure（Part A）

对「怎么提高第一次生成成功率」的机制顺序：

1. 先定义「第一次生成成功」的可测量口径（否则无法优化）。
2. 拆解首次生成失败的候选原因（输入表达 / 模型能力 / 预期与可恢复性），每条标为待验证假设。
3. 逐条给对应机制（输入引导、模板、Prompt 改写、模型替换、recovery），并说明取舍与边界。
4. 定义评估指标（成功率、重试率、编辑成本、放弃率）与实验验证方式。
5. 明确「换模型 vs 优化输入引导」这类选择要用实验比较，不默认哪个更优。

---

## 5. Suggested Answer（Part B）

> 只使用 Transcript / Resume 已有事实；所有具体用户洞察写成假设或 placeholder，不冒充已验证事实。

「我会先把『第一次生成成功』定义清楚，再谈怎么提高——没有口径，成功率无法测量。定义是 `[这里需要补充：成功口径，例如“首次生成内容被采纳/发布且无需大规模返工”或“生成结果通过质量阈值”]`。

第二步，拆解首次生成失败的可能原因，逐条假设验证：

1. 输入表达不清——用户可能不会清晰描述需求，Prompt 写不好。对应机制是输入框优化、引导、模板、Prompt 改写。这是我的假设，不是已验证洞察：我在校园 AI 写作助手只做过用户访谈和产品原型，`[这里需要补充：访谈结论——用户首次生成失败的主要原因，及是否有数据支撑]`。
2. 模型能力不足——换更好的模型或调参可提升质量，但需权衡 `[这里需要补充：latency / cost 约束]`，换模型不是唯一解。
3. 失败后可恢复性——失败后提供重新生成、模板等 recovery，降低放弃与编辑成本。

第三步，定义评估与验证：以首次生成成功率、重试率、编辑成本、放弃率作为主指标与 guardrail，用 `[这里需要补充：实验设计 / 基线 / 口径]` 验证，而不是上线后单看一个数。换模型与优化输入引导孰优，我会用实验比较后再定。」

---

## 6. Atomic Claim Audit

> 对 Suggested Answer 逐条拆最小事实单元，映射 source anchor，并做 negative-entailment check（「该 source 不增加任何假设，能否推出这句原子主张？」）。

| # | 原子主张 | 类型 | Source Anchor | 判定 |
|---|---|---|---|---|
| 1 | 先定义「第一次生成成功」口径 | 建议（proposed） | 无 anchor（结构化建议） | PASS（非过去事实） |
| 2 | 首次失败可能原因含「用户不会清晰描述需求」 | **假设（hypothesis）** | 无 anchor；已标注「假设/可能」 | PASS（hypothesis，非事实） |
| 3 | 对应机制：输入框优化 / 引导 / 模板 / Prompt 改写 | F1 | `[00:15:29–00:16:32]`（输入框、引导、Prompt）+ `[00:16:46–00:17:20]`（模板） | PASS |
| 4 | 我在校园 AI 写作助手做过用户访谈和产品原型 | F2 | Resume「负责用户访谈和产品原型」 | PASS |
| 5 | 访谈结论（用户为何失败） | — | 无 anchor | PASS → 已写 placeholder `[这里需要补充：访谈结论…]` |
| 6 | 换更好的模型 / 调参可提升质量 | F1 + 假设 | `[00:15:29–00:16:32]`（换更好的模型）；trade-off 为建议 | PASS |
| 7 | 失败后提供重新生成、模板 recovery | F1 | `[00:16:46–00:17:20]` | PASS |
| 8 | 评估指标：成功率 / 重试率 / 编辑成本 / 放弃率 | 建议（proposed framework） | 无 anchor（非候选人已用指标） | PASS |
| 9 | 用实验比较「换模型 vs 优化引导」 | 建议（proposed） | 无 anchor（非候选人已做实验） | PASS |

### Negative-entailment check（核心陷阱）

- 主张「用户不会描述需求」← source「简历：负责用户访谈和产品原型」：**不增加任何假设，推不出**。
  - 若写成过去事实 → FAIL（本稿已改写为假设 + placeholder，PASS）。
- 主张「访谈得出了任何具体用户洞察」← 同一 source：**推不出**。
  - 本稿所有具体洞察均无 anchor，已改写为假设或 placeholder，PASS。
- 结论：**没有把「访谈过用户」扩写成任何具体用户洞察。** 陷阱通过。

---

## 7. Provenance Check

逐条 claim → source anchor：

| Claim | Source Anchor |
|---|---|
| 解决真实用户问题 / 体验简单 / Prompt 写好 / 模型重要 / 输入框与引导 / 换更好的模型 | F1 `[00:15:29–00:16:32]` |
| 失败后重新生成 / 给模板 / 「成功就是用户觉得好用」 | F1 `[00:16:46–00:17:20]` |
| 做过用户访谈和产品原型（校园 AI 写作助手） | F2 Resume |
| 用户不会描述需求（作为已验证洞察） | **不存在 → 已改写为 hypothesis** |
| 访谈结论 | **不存在 → placeholder** `[这里需要补充：访谈结论…]` |

Placeholders 汇总：
- `[这里需要补充：成功口径]`
- `[这里需要补充：访谈结论——用户首次生成失败的主要原因，及是否有数据支撑]`
- `[这里需要补充：latency / cost 约束]`
- `[这里需要补充：实验设计 / 基线 / 口径]`

---

## 结论

- 陷阱测试：**PASS**。「做过用户访谈和产品原型」未被扩写成任何具体用户洞察（含「用户不会描述需求」）。
- 诊断结论：Q03 = 3.2/10，Q03.1 = 2.4/10，根因 `RC-AI-NO-EVAL`（Knowledge + Capability Gap），非表达问题。
