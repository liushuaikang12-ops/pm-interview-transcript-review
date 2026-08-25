# PM Interview Review — Full Review Template

> Source Manifest：列出 Transcript / JD / Resume / Project Docs / History / Outcome。所有推断显式写“推断”。
>
> 隐私边界：本模板生成的是本地私密 Full Review。飞书自动化不得直接发布本文件，必须先生成知识库脱敏版。

# 0. 面试实录与回答建议

> 本章必须从通过校验的 `record.json` 渲染，不得边读取 Transcript 边自由改写。原文不润色；只有可靠来源能够确认时才修正 ASR，否则标记「录音转写不清」。

## 0.1 面试官提问与候选人回复

### Qxx — <Surface Question，一句话问题标题>

- Parent：Root
- 问题时间：`<question anchor>`
- 面试官原文：
  > <verbatim question>
- 回答时间：`<answer anchor>`
- 候选人原回复：
  > <verbatim answer；没有回答时写 No answer captured>

#### Qxx.1 — <Surface Question，一句话追问标题>

- Parent：Qxx（无法确定时写 `Parent uncertain`）
- 问题时间：`<question anchor>`
- 面试官原文：
  > <verbatim follow-up>
- 回答时间：`<answer anchor>`
- 候选人原回复：
  > <verbatim answer；没有回答时写 No answer captured>

> 对账：root/follow-up 节点 n；已捕获回复 n；No answer captured n；Parent uncertain n。每个节点在本节有且仅有一次。

## 0.2 回答建议

> 仅覆盖有候选人回答的 root/follow-up；Administrative 与 candidate-reverse-question 不进入本节。只使用 Transcript/简历/JD 已有事实，缺口写 `[这里需要补充：…]`，假设题标「建议/假设」。

### Qxx

- Recommended Structure：
  1. ...
- Suggested Answer：
  > <Better Answer>
- Missing Facts：
  - <placeholder；没有则写 None>
- Provenance Check：
  - `<atomic claim> → <source anchor>`

> 对账：eligible questions n；answer suggestions n；provenance-complete n。三者必须相等。

## 0.3 候选人反问与面试官回答原文

### RQxx

- 对应 Question ID：Qxx
- 候选人反问时间：`<candidate anchor>`
- 候选人反问原文：
  > <verbatim candidate question>
- 面试官回答时间：`<interviewer anchor>`
- 面试官回答原文：
  > <verbatim interviewer answer；没有回答时写 No answer captured>

> 本节不生成 Better Answer。第 13 章只提取信息与推断，不重复整段原文。

# 1. Executive Summary

> 一段锋利结论：最大优势、最大风险、下一层追问最可能断在哪里。至少 2 个 Evidence anchors。禁止套话。

## Interview Verdict
- Overall Performance: x/10 或 range
- Confidence: High / Medium / Low（原因）
- Strongest Areas: 3–5
- Biggest Risks: 3–5
- Likely Interviewer Concerns（推断）
- Positive Signals（行为信号推断）
- Uncertain Areas

# 2. Interview Structure

| Stage | Time/Anchor | What happened | Weight in interview |
|---|---|---|---|

# 3. Complete Question Map

| ID | Parent | Speaker | Surface Question | Answer Anchor | Underlying Intent（推断） | Competency | Type |
|---|---|---|---|---|---|---|---|

对账：Pass 1 有效问题 n；树节点 n；Administrative n；Uncertain parent n。

# 4. Follow-up Trees

```text
Q01 Root question
├── Q01.1 Follow-up
│   └── Q01.1.1 Evidence challenge
└── Q01.2 Alternative / trade-off
```

每棵核心树补充：Probe 的统一 concern、触发下一问的 Candidate answer、parent uncertainty（如有）。

# 5. Competency Mapping

| Competency | Evidence | Current signal | Confidence |
|---|---|---|---|

PM Evidence Chain：Problem → Evidence → Insight → Decision → Solution → Experiment → Metric → Attribution → Iteration → Reflection。

# 6. Key Answer Reviews

## Qxx — [问题]

### Surface Question
### Underlying Intent（推断 + confidence）
### Candidate Answer — Clean Version
### Raw Evidence（必要时）
### Score

| Dimension | Score | Evidence-based reason |
|---|---:|---|
| Substance | /10 | |
| Structure | /10 | |
| Relevance | /10 | |
| Credibility | /10 | |
| Differentiation | /10 | |

- Weight profile: ...
- Raw weighted score: ...
- Cap/penalty: ...
- Overall Score: ...
- Gap Type: Capability / Communication / Evidence / Knowledge

### Root Cause
`Finding → What happened → Root Cause code → Why it matters`

### Answer Suggestion Reference
- 参见：`0.2 / Qxx`
- 本章不重复 Suggested Answer 或 Provenance Check。

# 7. Evidence & Quotes

| Evidence ID | Anchor | Speaker | Quote | Level (F1/F2/I1) | Used for |
|---|---|---|---|---|---|

# 8. Shortcoming Cards

## Card 1 — [问题名称]
- Severity: High / Medium / Low
- Frequency: n / eligible n
- Evidence:
- Root Cause:
- Interview Risk（推断）:
- Corrective Principle:
- Drill（动作 + 完成标准）:

> 总数 3–7，按优先级。

# 9. Anti-patterns

| Anti-pattern | 本场 | 历史累计 | 最近 3 场 | 最近 5 场 | Trend | Evidence |
|---|---:|---:|---:|---:|---|---|

样本不足写 `Insufficient history`。声明统计单位和 eligible answers。

# 10. Project Probe Depth

## [Project]
- Current Probe Depth: x/10
- 连续证据到：Layer x
- 首个断点：Layer y
- 孤立强证据（如有）：
- 下一步补证据：

| Layer | Status | Evidence | Missing |
|---:|---|---|---|

# 11. Role-specific Review

仅动态启用匹配模块；不匹配时写 `Not activated — 岗位/问题无足够证据`。

## AI Product Depth
User Intent / Capability / Limitation / Context / Memory / Tool / Evaluation / AI UX / Latency-Cost-Quality / Failure Recovery / HITL / Feedback Loop。

## Growth Mechanism
Motivation → Trigger → Activation → First Value → Habit → Retention → Growth Loop；补充 Segment、Lifecycle、Attribution、Guardrail。

## Strategy Depth
Business Model / Market / Competition / Resource Allocation / ROI / Trade-off / Execution loop。

# 12. Interviewer Signals

| Anchor | Observable behavior | Signal | Alternative explanation | Confidence |
|---|---|---|---|---|

> 行为信号推断，不等于真实评分或录用结论。

## Interviewer Model（Interview Style only）
- Style:
- Evidence:
- 不推断人格。

# 13. Reverse Interview Intelligence

## Candidate Questions
| ID | Question | Answer anchor | Quality |
|---|---|---|---|

> 候选人问题与面试官回答原文参见 `0.3 / RQxx`；本章不改写反问，也不重复整段原文。

## Information Revealed
| Category | Transcript Fact | Anchor | Inference（可选） | Confidence |
|---|---|---|---|---|

Category：Team / Product / KPI / Current Problem / Candidate Role / Expectation / Work Style / Hiring Signal。

# 14. Shadow JD

| Official JD | Interview Evidence | Shadow JD（推断） | Confidence |
|---|---|---|---|

没有 Official JD 时写 unavailable；仍可从面试证据归纳，但 confidence 降级。

# 15. Cross-interview Update

- History baseline: n 场 / 无历史
- Question Bank changes:
- Competency Matrix changes:
- Anti-pattern changes:
- Project Probe Depth changes:
- Story Bank candidates:
- Outcome Calibration: none / appended event
- Saved artifacts:

# 16. Next Interview Actions

## P0 — 下一场前必须修
1. **对象**：
   - 动作：
   - 完成标准：
   - 复测问题：

## P1 — 建议修

## P2 — 长期积累

> 总数保持少；每项可执行、可验收。
