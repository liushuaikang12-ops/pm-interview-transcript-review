# Scoring & Root Cause Playbook

## 1. 五维评分定义

每维 1–10，先写 Evidence，再评分。没有可定位 Evidence 时该维 confidence 降为 Low；不要用“听起来不错”评分。

| 分段 | 含义 |
|---|---|
| 1–2 | 未回答、明显错误或与问题冲突 |
| 3–4 | 有零散信息，但关键链路缺失，担忧未解除 |
| 5–6 | 基本回答问题；方法/证据/差异化不稳定 |
| 7–8 | 结论清晰、证据可信、能扛主要追问 |
| 9–10 | 证据闭环且展现高质量决策；10 仅用于近乎无明显缺口的稀有回答 |

- **Substance**：是否有 Problem、Insight、Decision、Action、Metric、Attribution、Reflection 等真正信息。
- **Structure**：结论是否前置；层级、长度与逻辑是否服务问题。
- **Relevance**：是否直接回答 interviewer 的问题，而不是背相邻故事。
- **Credibility**：事实口径、证据来源、因果边界、个人贡献是否可信。
- **Differentiation**：是否体现候选人独有的判断、机制理解、取舍与复盘，而非正确口号。

## 2. Dynamic Weight Profiles

Overall raw score = `Σ(dimension_score × weight)`。在报告中写 profile 名称与权重。

| Question Type | S | Str | R | C | D |
|---|---:|---:|---:|---:|---:|
| Project Deep Dive | .30 | .15 | .20 | .25 | .10 |
| Data / Experiment / Attribution | .25 | .10 | .20 | .35 | .10 |
| Product Sense / Design | .30 | .20 | .25 | .10 | .15 |
| AI Product Mechanism | .30 | .15 | .20 | .20 | .15 |
| Growth Strategy | .30 | .15 | .20 | .20 | .15 |
| Strategy / Business | .30 | .10 | .20 | .20 | .20 |
| Behavioral / Collaboration | .20 | .20 | .25 | .25 | .10 |
| Self-introduction / Motivation | .20 | .25 | .30 | .15 | .10 |

无法归类时用 Project Deep Dive，但要声明。

### Caps（先算 raw，再取最低适用上限）

- Relevance ≤3：Overall ≤4.5。
- Credibility ≤3，且核心结论依赖未证实数据/因果：Overall ≤5.0。
- Candidate 没有回答：Overall ≤2.0。
- 回答只给正确口号、无岗位机制：AI/Growth mechanism question Overall ≤5.0。
- 有明显编造/前后矛盾迹象：不判定“撒谎”；标 `Credibility Strong Concern`，Overall ≤4.0，等待核验。

不要因 Structure 很好掩盖空内容，也不要因表达不流畅否定有证据的高质量判断。

## 3. Overall Interview Score

不是所有问题平均：

1. 选择 3–8 个 decisive answers。
2. 按面试分配的时间、follow-up depth、JD relevance 分 `Critical/Important/Supporting`。
3. 默认权重 `Critical 3 / Important 2 / Supporting 1`。
4. 再检查 hard concern：关键项目 Credibility、岗位核心能力、明显失配。
5. 给 score range 或 1 位小数；Transcript 不完整时不输出伪精确小数。

Confidence：

- **High**：完整 Transcript + speaker/timestamp 可靠 + JD/关键上下文足够。
- **Medium**：Transcript 基本完整，但 speaker/JD/部分片段有缺口。
- **Low**：节选、无可靠 speaker、关键内容缺失或 ASR 严重。

## 4. Root Cause Codes

每个低分 finding 只选 1 个 primary root cause，可加至多 2 个 secondary。

### Understanding / Relevance
- `RC-UNDERSTAND` 问题理解错误
- `RC-NONANSWER` 没回答核心问题
- `RC-STORY-MISMATCH` Story 与问题不匹配
- `RC-DEFENSIVE` 主要在自我辩护，未解除 concern

### Evidence / Credibility
- `RC-NO-EVIDENCE` 结论无证据
- `RC-METRIC-DEFINITION` 指标口径/窗口/样本不清
- `RC-CAUSAL-LEAP` 数据无法证明结论，Attribution 不成立
- `RC-SOURCE-QUALITY` 数据来源可靠性未说明
- `RC-CONTRIBUTION` 个人与团队贡献混淆
- `RC-CONTRADICTION` 前后陈述冲突，需核验

### Product / Decision
- `RC-NO-PROBLEM` Problem definition 不清
- `RC-NO-INSIGHT` 缺 User Insight/Business Insight
- `RC-NO-WHY` 只讲做了什么，不讲 why
- `RC-NO-DECISION-LOGIC` 缺判断标准
- `RC-NO-ALTERNATIVE` 没比较替代方案
- `RC-NO-TRADEOFF` 没讲代价、边界、Guardrail
- `RC-NO-VALIDATION` 缺实验或验证
- `RC-NO-RESULT` 缺结果
- `RC-NO-ITERATION` 没有异常、迭代、反思闭环

### Role-specific
- `RC-AI-CONCEPTUAL` AI 回答停留在口号/概念
- `RC-AI-NO-EVAL` 未说明 evaluation/failure handling
- `RC-GROWTH-TACTIC` Growth 只剩 Push/补贴/活动等手段
- `RC-GROWTH-NO-LOOP` 缺 Activation→Value→Retention→Loop
- `RC-BUSINESS-THIN` 缺 business model/ROI/resource logic

### Communication
- `RC-CONCLUSION-LATE` 结论后置
- `RC-BACKGROUND-LONG` 背景过长
- `RC-TOO-LONG` 冗长且信息密度低
- `RC-TOO-SHORT` 过短，关键链路未展开
- `RC-HEDGING` 过度“可能/大概/应该”
- `RC-TEMPLATE` 模板痕迹重，无法适配追问

## 5. Finding Contract

每条重要诊断使用：

```markdown
### Finding
- Frequency: n（统计单位：Q&A node）
- Evidence: [timestamp] / Qxx
- What happened: 可观察行为，不夹推断
- Root Cause: RC-...（为何）
- Gap Type: Capability / Communication / Evidence / Knowledge
- Why it matters: 面试官可能产生的岗位风险（推断）
- Better approach: 可执行原则
```

## 6. Interviewer Signal Rules

- **Positive**：明确认可；基于回答继续建设性深入；主动关联岗位。
- **Neutral**：常规切题、时间控制、无明确情绪信息。
- **Concern**：重复索要同一证据、挑战口径/因果、要求具体个人动作。
- **Strong Concern**：明确否定/纠正，或 Candidate 多次仍无法回答岗位核心问题。

追问本身不等于 Concern。报告中同时列“兴趣深挖”与“担忧未解除”两种解释，除非后续证据能区分。

## 7. Shortcoming Card Prioritization

按 ordinal triage，而非虚构数学精度：

1. 是否影响岗位核心能力判断？
2. 是否在多个关键回答重复？
3. 是否触发 interviewer concern？
4. 是否能在下一场前修复？

High：核心能力 + 多个 Evidence/Strong Concern；Medium：局部但会降低可信度；Low：不影响主判断。每场保留 3–7 张，其余放普通 findings。

## 8. 表达层指标的可计算边界

仅在 Transcript 完整、speaker 可靠、时间戳连续时计算：

- Candidate / Interviewer speaking time ratio
- 单次回答平均/中位长度
- 超长回答数（阈值必须声明）
- filler word rate（每千字或每分钟）
- interruption（只能在重叠时间戳/明确标记下判断）
- conclusion position（前 20% / 中段 / 后 20%，需人工语义判断）

不具备条件时写 `Not reliably measurable`，不得从文本行数冒充 speaking time。