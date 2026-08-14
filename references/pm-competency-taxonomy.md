# PM Competency Taxonomy & Probe Models

## 1. Tagging Rule

每个 Root Question 选 1–3 个 primary tags；follow-up 可覆盖更细标签。标签表达“面试官在验证什么（推断）”，不是仅看题面关键词。不要为完整性把所有标签打上。

## 2. Product Fundamentals

- Problem Definition
- User Insight
- Product Sense
- Requirement Analysis
- Prioritization
- Product Design
- User Experience
- Trade-off
- Decision Making

判断重点：问题是谁的、发生在哪个场景、证据是什么、为什么值得做、方案如何从 insight 推导、为什么此时做。

## 3. Data & Experimentation

- Metrics
- Data Analysis
- Funnel Analysis
- Experiment Design
- A/B Test
- Attribution
- Root Cause Analysis
- Guardrail Metrics
- Statistical Awareness

检查：指标定义、分母/窗口、baseline、sample、随机化/对照、显著性意识、confounder、guardrail、异常解释、相关与因果边界。

## 4. Growth

- Acquisition
- Activation
- Retention
- Engagement
- Referral
- Lifecycle
- Growth Loop
- Channel Strategy
- Incentive Mechanism
- DAU
- Conversion

### Growth mechanism test

`User Motivation → Trigger → Activation → First Value → Habit → Retention → Growth Loop`

补充检查：Segment、Frequency、Lifecycle、User Asset、Referral、Network/Content/Creation Loop、成本与作弊/补贴依赖。

以下只是 tactic，不自动证明 Growth 能力：Push、签到、积分、活动、补贴。必须解释目标 segment、行为机制、增量、Attribution、长期留存与副作用。

## 5. AI Product

- AI-native Product Thinking
- Model Capability Understanding
- Prompt / Context Design
- Agent
- RAG
- Tool Use
- Model Evaluation
- AI UX
- Latency / Cost / Quality Trade-off
- Human-in-the-loop
- Failure Recovery
- Model Limitation
- AI Growth Loop

### AI mechanism test

至少沿以下链条定位：

`User Intent → Context → Model/Tool Capability → Generation/Action → Evaluation → First Success → Retry/Edit → Failure Recovery → Feedback/Memory → Re-use/Growth`

关键诊断项：

- 用户 intent 是否可判定；输入不完整如何补齐。
- 为什么用模型/Agent/RAG/Tool，而非规则或人工。
- capability boundary、hallucination、non-determinism。
- eval set、online/offline metric、quality rubric、failure taxonomy。
- latency/cost/quality trade-off 与 fallback。
- First Success、retry rate、edit cost、abandonment。
- HITL 的触发点与责任边界。
- Context/Memory 的来源、更新、隐私与污染风险。
- AI UX 是否让用户理解不确定性并可恢复。
- 是否形成数据/创作/反馈 loop，而非只把 AI 当功能按钮。

如果回答只有“AI 要解决真实问题”“体验很重要”等正确口号，缺机制、指标、边界，标 `AI Product Depth Insufficient`，且 Differentiation 不高于 5。

## 6. Strategy

- Business Understanding
- Competitive Analysis
- Monetization
- ROI
- Resource Allocation
- Market Insight

检查：value chain、business model、market structure、竞争差异、投入/回报、机会成本、短中长期取舍、策略如何落到可执行实验。

## 7. Execution

- Cross-functional Collaboration
- Project Management
- Stakeholder Management
- Delivery
- Ownership

检查：目标/责任、冲突来源、信息与决策机制、风险、升级路径、候选人亲自做了什么、结果与复盘。

## 8. Communication

- Structure
- Concision
- Persuasiveness
- Credibility
- Executive Communication
- Listening

Listening 的 Evidence 包括：主动确认歧义、针对追问调整、引用 interviewer 的约束。不要把语速或口音直接等同能力。

## 9. PM Evidence Chain

对项目使用统一链：

1. **Problem**：具体用户/业务问题与边界。
2. **Evidence**：数据、调研、case、来源。
3. **Insight**：从证据得出的机制判断。
4. **Decision**：目标、优先级、标准。
5. **Solution**：机制而非功能清单。
6. **Experiment**：验证假设的设计。
7. **Metric**：主指标、guardrail、口径。
8. **Attribution**：为什么认为结果由方案导致。
9. **Iteration**：异常与下一轮。
10. **Reflection**：边界、trade-off、重做选择。

标记每环：`Strong / Partial / Missing / Contradicted / Insufficient Evidence`。

## 10. Project Probe Depth（连续证据深度）

| Layer | Probe | 通过标准 |
|---:|---|---|
| 1 | What did you do? | 角色、动作、产出清楚 |
| 2 | Why? | 问题与目标清楚 |
| 3 | Evidence? | 数据/用户证据及来源 |
| 4 | Why this solution? | insight→机制→方案 |
| 5 | Alternative? | 比较方案与取舍 |
| 6 | Metrics? | 指标、口径、guardrail |
| 7 | Unexpected result? | 异常/失败事实 |
| 8 | Root cause? | 非表面归因，有验证 |
| 9 | Iteration? | 基于根因的下一步 |
| 10 | What differently? | 有边界意识和反事实 |

`Current Probe Depth = 从 Layer 1 起连续达到 Strong/Partial 且有 Evidence 的最深层`。若 L4 缺失，即使 L6 有结果，也写 `3/10，L4 开始断裂；L6 有孤立证据`。不要把“面试官问到了第 8 层”写成“能扛 8 层”。

## 11. Interviewer Intent Patterns（均为推断）

- “为什么做？” → Problem Definition / Prioritization / Ownership
- “怎么发现？” → User Insight / Evidence quality
- “有什么数据？” → Metrics / Credibility
- “为什么这个方案？” → Decision Making / Product Sense
- “其他方案呢？” → Alternatives / Trade-off
- “指标怎么设计？” → Metric tree / Guardrail / Causality
- “为什么上涨？” → Attribution / Root Cause
- “你具体做了什么？” → Ownership / Contribution
- “如果重来？” → Reflection / Learning velocity

同一句题面可验证不同能力，必须结合前后追问和岗位上下文。

## 12. Reverse Interview Taxonomy

提取并分别保存 Fact/Inference：

- Team：职责、组织关系、协作边界
- Product：产品与用户
- KPI：DAU、Retention、Revenue、Conversion 等
- Current Problem：当前真正要解的问题
- Candidate Role：实际工作内容
- Expectation：对 Intern/PM 的要求
- Work Style：节奏、决策、协作方式
- Hiring Signal：面试官明确透露的偏好

只分析 Interview Style：Data-driven、Strategy-heavy、Product Sense、Execution-heavy、Detail-oriented、Adversarial、Friendly、Structured、Resume-driven。不得推断人格、善恶或团队文化全貌。