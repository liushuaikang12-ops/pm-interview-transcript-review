---
name: pm-interview-transcript-review
description: Review Product Manager interview recordings or transcripts into evidence-grounded question transcripts, Better Answers, Follow-up Trees, diagnostics, Shadow JD, next-round drills, and verified Feishu Wiki documents. Use for PM, AI PM, Growth PM, or Strategy PM interview debriefs and configured Feishu recording automation; not for generic meeting summaries.
license: MIT
metadata:
  author: liushuaikang12-ops
  version: "3.1.0"
  short-description: PM 面试录音复盘与飞书知识库自动归档
---

# PM Interview Review OS

## Overview

这是面向 Product Manager、AI Product Manager、Growth/Strategy PM 的面试复盘操作系统，不是会议纪要、流水账或通用 STAR 生成器。目标是把单场 Transcript 转换为可验证的诊断，并把多场结果沉淀为可校准的 Question Bank、Competency Matrix、Anti-pattern Library、Project Probe Depth、Story Bank 与 Drill Plan。

核心链路：

`Input → Transcript Processing → Speaker Identification → Q&A Reconstruction → Follow-up Tree → Interviewer Intent → Competency Mapping → Evidence-grounded Evaluation → Root Cause → Better Answer → Shortcoming Cards → Interviewer Intelligence → Shadow JD → History Update → Next Drill`

始终以 Transcript 为事实源；简历、JD、项目资料只用于补充上下文与校验，不得覆盖 Candidate 实际说过的话。

## Trigger Conditions

当用户表达以下或近似意图时加载：

- “帮我复盘这场面试 / 整理面经 / 看看表现”
- “分析这个录音、视频、transcript、Markdown、TXT”
- “提取所有面试官问题 / 面试官到底在考什么”
- “恢复追问树 / 诊断回答 / 优化答案”
- “根据这场面试准备下一轮”
- “对比最近几场 / 更新面试题库 / 记录面试结果或 HR feedback”
- 飞书机器人收到面试录音、视频或 transcript，并要求自动复盘归档

不要用于普通会议纪要、模拟面试出题、纯简历改写或与 PM 无关的通用职业面试；这些任务除非用户明确要求套用本 OS。

## Modes

| Mode | 产出 | 何时使用 |
|---|---|---|
| A — Full Review | 第 0 章实录与回答建议 + 16 章诊断 + 历史更新 | 默认 |
| B — Question Extraction | 全量问题、Q&A ID、Follow-up Tree、Intent | 用户只要问题结构 |
| C — Answer Critique | 关键回答评分、Root Cause、Better Answer | 用户只要回答诊断 |
| D — Interviewer Intelligence | 反问信息、Interview Style、Shadow JD | 用户只关心岗位与面试官信号 |
| E — Cross Interview Review | 跨场趋势、题库、能力矩阵、反模式、校准 | 输入多场或明确比较 |
| F — Next Round Prep | Answer Playbook、P0/P1/P2、Story/Project drill、问题预测；不输出完整诊断 | 准备下一轮 |

用户未指定时采用 **Mode A — Full Review**。模式只裁剪输出，不降低 Evidence 标准。

## Inputs

可单独或组合接收：

1. `.mp3/.m4a/.wav` 录音；视频文件。
2. ASR 文本、`.md/.txt/.vtt/.srt` Transcript。
3. JD、简历、项目资料。
4. 既往复盘、Question Bank、Shortcoming Cards。
5. Recruiter/HR/Hiring Manager feedback 与结果。

建立 Source Manifest，逐项标记：`source_id`、类型、路径/URL、是否含时间戳、语言、可信用途。输入已经是 Transcript 时不得重新 ASR。缺 JD/简历不阻塞 Transcript 复盘，只把岗位匹配与 Shadow JD confidence 降级；缺 Transcript 时不能声称做过回答评价。

## Progressive Disclosure

按任务加载，不要把所有参考一次塞入上下文：

- 所有评分与 Root Cause：`references/scoring-and-diagnosis.md`
- PM/AI PM/Growth 标签与 Probe Depth：`references/pm-competency-taxonomy.md`
- 历史数据库、趋势、Outcome Calibration：`references/history-and-calibration.md`
- 音视频/ASR：`references/media-pipeline.md`
- Codex 连接飞书、固定知识库与自动归档：`references/codex-feishu-automation.md`
- Full Review 格式：`templates/full-review.md`
- 跨场 JSON 记录：`templates/interview-record.schema.json`

## Workflow

### 0. Preflight 与工作区

先从当前客户端提供的 Skill metadata、已加载文件路径或当前 `SKILL.md` 所在位置确定 **Skill directory**。所有 `references/...`、`templates/...` 和 `scripts/...` 都相对该目录解析；不要猜全局安装路径，也不要假设客户端提供某个厂商专属环境变量。

默认历史工作区为 `${PM_INTERVIEW_REVIEW_HOME}`；未设置时，脚本使用用户目录下的 `~/.pm-interview-review-os/`。不要把面试材料和跨场历史写进 Skill 安装目录。需要确定性历史聚合时运行：

```bash
python "<skill-directory>/scripts/interview_os.py" init
python "<skill-directory>/scripts/interview_os.py" status
```

客户端没有 shell/Python 能力时，仍可完成基于当前输入的 Markdown 复盘，但必须把 History 标为 `Unavailable in this client`，不得声称已保存记录或更新跨场聚合。先读取工作区历史索引；没有历史时明确写“无历史基线”，不要虚构趋势。完成条件：输入清单、模式、岗位类型、Skill directory 和历史可用性均已记录。

### 1. Transcript Processing

- 音视频：按 `references/media-pipeline.md` 先本地转写并保留 timestamp。ASR 不可用时报告缺口并请求 Transcript；不得靠听感或文件名编内容。
- 文本：保留原始文件，只创建 normalized/clean 版本。
- 允许去除 filler、口吃和 ASR 明显重复，但不得改变语义、数字、否定词、责任主体或因果关系。
- 关键回答同时保留 `Clean Version` 与必要的 `Raw Evidence`。

完成条件：每段可定位到 timestamp 或稳定段落/Q&A anchor；原始源未被覆盖。

### 2. Speaker Identification

至少区分 `Candidate` 与 `Interviewer`；多人面使用 `Interviewer A/B/C`。仅根据称谓、问答轮次、内容角色和已知声纹标签判断。无法可靠确定时写 `Unknown Speaker`，不得猜。ASR 的 speaker label 也只是一条待校验证据。

完成条件：所有有效段落有 speaker label 或明确 Unknown。

### 3. Q&A Reconstruction（先全量，再归树）

做两遍：

1. **Pass 1 — Exhaustive extraction**：抽取所有有效问题、隐含 challenge、要求举例/澄清/量化的问题；寒暄与纯流程提示另标 `Administrative`。
2. **Pass 2 — Hierarchy reconstruction**：把围绕同一能力/证据链的追问归到 Root Question 下，生成 `Q01`、`Q01.1`、`Q01.2.1`。不得按时间平铺。

追问归属依据按优先级：显式指代（“这个数据/刚才方案”）→同一项目/命题→同一未解除 concern→时间邻近。证据不足时标 `Parent uncertain`，不要强行挂树。

每个核心节点包含：

- `Surface Question`
- Question anchor 与问题原文
- `Underlying Intent`（标记为 `推断`）
- Candidate Answer anchor、原回复与 `captured / no-answer / uncertain` 状态
- Follow-up trigger：面试官为何继续追问（可多解时列 alternatives）
- Competency tags

候选人反问使用 `candidate-reverse-question`，单独保存候选人问题原文与面试官回答原文的配对；它不进入 Better Answer。寒暄、结束语等 `administrative` 节点不进入回答建议。完成条件：Pass 1 的每个有效问题都在树中或被明确标为独立 Root/Administrative；每个可回答节点都有对应回复或显式 `No answer captured`；数量可对账。

### 4. Evidence Ledger

分析前先建立证据账本。每条重大 finding 必须绑定：

- 有时间戳：`[00:23:18–00:24:02]`
- 无时间戳：`Q08 Candidate Answer` 或稳定段落 anchor
- speaker + 短原话；引用保持原意
- `Fact` 或 `Inference`

使用三层置信标签：

- `F1 Transcript Fact`：原话明确出现。
- `F2 Corroborated Fact`：Transcript 与简历/JD/资料一致。
- `I1 Inference`：从行为或上下文推断，必须写“推断”并给 confidence。

找不到证据时写 `Insufficient Evidence`，不得用常识补齐。

### 5. Competency Mapping 与 Intent

加载 PM taxonomy。对 Root Question 和关键追问映射 1–3 个主能力标签，避免标签泛滥。重点检查 PM 证据链：

`Problem → Evidence → Insight → Decision → Solution → Experiment → Metric → Attribution → Iteration → Reflection`

Intent 不是面试官心理事实。格式：`Underlying Intent（推断，Confidence: Medium）：验证 Attribution 与证据可靠性。`

### 6. Key Answer Evaluation

只深评决定性回答、被多次追问的回答、明显失误和最强回答；其余保留在 Complete Question Map。按问题类型动态权重计算五维 1–10 分：

- Substance
- Structure
- Relevance
- Credibility
- Differentiation

`Overall Score` 不是简单平均，必须展示使用的 weight profile，并应用 `references/scoring-and-diagnosis.md` 的 cap/penalty。分数要能被 Evidence 解释，不得默认高分。

同时区分：

- `Capability Gap`：底层判断/方法本身缺失或错误。
- `Communication Gap`：事实或思考存在，但本次表达结构/长度/结论位置失效。
- `Evidence Gap`：结论可能对，但现有材料无法证明。
- `Knowledge Gap`：必要概念或机制不理解。

一次失误只能称“本场信号”；至少跨 2 场重复、且有独立 Evidence，才升级为长期 weakness/anti-pattern。

### 7. Root Cause Diagnosis

低分项不得停在“回答不好”。沿链条定位最小可修根因：问题理解、Relevance、结论位置、Evidence、数据口径、因果/Attribution、User Insight、Why/Decision Logic、Alternative、Trade-off、Experiment、Result、Reflection、个人贡献、故事匹配、冗长/过短、Defensive/Hedging、AI 概念化、Growth 运营化等。

输出链：

`Finding → Frequency → Evidence → What happened → Root Cause → Why it matters → Better approach`

不要把症状当根因。例如“被追问很多”不是根因；可能是首答缺数据口径、因果证据或个人决策。

### 8. Better Answer（零编造）

每个重点改写分两部分：

**Part A — Recommended Structure**：列信息顺序与决策逻辑。

**Part B — Suggested Answer**：只能使用 Transcript、简历、JD、项目资料中已有事实。任何缺失用 `[这里需要补充：数据口径/个人动作/结果/来源]`。不得创造项目、指标、动作、结果、失败或 interviewer feedback。

改写后必须做 **Atomic Claim Audit**：

1. 把 Suggested Answer 拆成最小事实单元：每个过去动作、用户观察/原话、数字、结果、因果结论、个人贡献。
2. 每个事实单元都映射到精确 source anchor。来源只证明“做过用户访谈”时，**不能**顺带推导访谈对象说了什么或得出了什么 insight。
3. 假设题/Case 允许提出新方案，但必须表述为 `我会先验证…` / `我的假设是…` / `建议…`，不能改写成候选人过去做过的事实。
4. 无 anchor 的事实必须整句删除或整句改为 placeholder；在一个无证据结论后面追加 placeholder，并不能让前半句变得有证据。
5. 做 negative-entailment check：问“该 source 不增加任何假设，能否推出这句原子主张？”不能则判定失败。

最后输出 `Provenance Check`：逐条列 `claim → source anchor` 与全部 placeholders。

### 9. Interviewer Signal

依据追问、重复确认、认可、challenge、要求举例、质疑证据、纠正、切题等行为输出：`Positive Signal / Neutral / Concern / Strong Concern`。必须附证据并声明：**这是行为信号推断，不等于真实评分或录用结论**。快速切题既可能是满意也可能是放弃追问；无其他证据时保持 Neutral/Uncertain。

### 10. Shortcoming Cards 与 Anti-pattern

每场只生成最关键 3–7 张卡，按“对录用判断的影响 × 重复性 × 可修复性”排序。每张包含：Name、Severity、Frequency、Evidence、Root Cause、Interview Risk、Corrective Principle、Drill。

Anti-pattern 统计单位必须定义（默认：一次独立回答/Q&A 节点出现算 1 次，同一回答内重复口头禅不重复计为多个结构问题）。输出本场次数；有历史时输出累计、最近 3 场、最近 5 场、`Improving/Stable/Worsening`。样本少于 3 场写 `Insufficient history`，不硬判趋势。

### 11. Project Probe Depth

对每个重要项目按 10 层检查：What → Why → Evidence → Why this solution → Alternative → Metrics → Unexpected result → Root cause → Iteration → What differently。`Current Probe Depth: x/10` 指连续有可靠证据支撑的最深层，不是问到的最深层。指出从哪层开始变弱及缺失证据。

### 12. Role-specific Review

- AI PM/AI-native/Agent/AI Growth：必须额外检查 User Intent、Model Capability/Limit、Context/Memory/Tool、Generation Quality、Evaluation、Latency/Cost/Quality、First Success/Retry/Edit Cost、Failure Recovery、HITL、Feedback Loop、AI UX。只有正确口号而无机制时标 `AI Product Depth Insufficient`。
- Growth PM：检查 `Motivation → Activation → Value Delivery → Habit → Retention → Growth Loop`，以及 Segment、Trigger、Lifecycle、Incentive、Frequency、User Asset、Referral 与归因。Push/签到/积分/补贴本身不等于增长能力。
- Strategy PM：检查 business model、market/competition、resource allocation、ROI、trade-off 与可执行闭环。

### 13. Reverse Interview、Shadow JD、Interviewer Model

单独提取候选人反问及面试官透露的 Team、Product、KPI、Current Problem、Candidate Role、Expectation、Work Style、Hiring Signal。面试官原话是 Fact；归纳是 Inference。

`Shadow JD = Official JD + Interview Evidence + Inference`。每条 Shadow JD 都要给 Evidence 和 confidence。只分析 Interview Style（Data-driven、Strategy-heavy、Execution-heavy、Detail-oriented、Resume-driven 等），不得猜人格。

### 14. Cross-interview Update 与 Outcome Calibration

分析完成并通过 Evidence/placeholder 检查后，再保存本场 `record.json` 与 `review.md`，然后从所有 records 重建聚合表，避免手工累计漂移。加载 `references/history-and-calibration.md`。

用户后来提供结果/反馈时：追加真实 outcome、比较先前 verdict 与实际结果、记录 prediction error hypothesis。不得为了匹配结果倒改旧复盘；校准记录是 append-only。面试结果不能证明某一单点诊断必然正确，只能更新权重假设。

### 15. Next Interview Actions

只给少量行动：

- `P0`：下一场前必须修，通常 1–3 项。
- `P1`：建议修，通常 1–3 项。
- `P2`：长期积累，通常 1–2 项。

每项包含：训练对象、具体动作、完成标准、复测问题。禁止“加强 AI 理解”式空话。

## Output Contract

Full Review 严格按 `templates/full-review.md` 输出：先生成第 0 章的「面试官提问与候选人原回复」「回答建议」「候选人反问与面试官回答原文」，再输出以下 16 章诊断：

1. Executive Summary
2. Interview Structure
3. Complete Question Map
4. Follow-up Trees
5. Competency Mapping
6. Key Answer Reviews
7. Evidence & Quotes
8. Shortcoming Cards
9. Anti-patterns
10. Project Probe Depth
11. Role-specific Review：AI PM / Growth PM / Strategy PM（动态启用）
12. Interviewer Signals
13. Reverse Interview Intelligence
14. Shadow JD
15. Cross-interview Update
16. Next Interview Actions

Executive Summary 必须给“最大优势、最大风险、最可能在下一层追问暴露的断点”，并带 Evidence anchor；禁止“总体不错、仍有空间”。总评包含 Overall Performance、Confidence、Strongest Areas、Biggest Risks、Likely Concerns、Positive Signals、Uncertain Areas。不要给无证据的“通过率 xx%”。

默认产出 Markdown；用户要求时再渲染 HTML。长复盘写入工作区文件并在回复中给路径与锋利摘要，不要把所有历史 JSON 倾倒到聊天，也不得因篇幅静默省略问题或章节。完整 Full Review 是本地私密文件，不得直接上传组织共享知识库。

生成顺序固定为两阶段：

- **Phase 1 — `Transcript → record.json`**：先完成逐轮问答配对、Q&A ID、追问 parent、原文、anchor、回答建议和反问 exchange，并通过 Schema/语义对账。
- **Phase 2 — `record.json → review.md / answer-playbook.md`**：再按模板渲染。不得边读 Transcript 边自由组织最终报告。

### 第 0 章：实录与回答建议

第 0 章严格分为三个子模块：

1. `0.1 面试官提问与候选人回复`：每个 `root / follow-up` 节点按 Q ID 输出问题 anchor、面试官原文、回答 anchor、候选人原回复；追问紧跟所属 Root。无回答写 `No answer captured`，不得省略。
2. `0.2 回答建议`：覆盖每个有候选人回答的 `root / follow-up` 节点，按同一 Q ID 输出 Recommended Structure、Suggested Answer、Missing Facts 与 Provenance Check。
3. `0.3 候选人反问`：按 `RQxx` 输出候选人反问原文和对应的面试官回答原文；无回答写 `No answer captured`。不得为反问生成 Better Answer。

“原文”指 Transcript 中的文本，不润色、不改语序、不删除口头语。只有音频复核或其他可靠来源能够确认时才能修正 ASR；否则保留原转写并标记 `录音转写不清`。`Clean Version` 与 `Suggested Answer` 必须另行标注，不能冒充原文。

### 回答建议版（Answer Playbook）

Full Review 中，第 0.2 节展示回答建议，第 6 章只做关键回答诊断并引用对应的 `0.2 / Qxx`，不得再次粘贴 Suggested Answer。用户只要备考文档时采用 Mode F：仅输出 Answer Playbook 与下一轮训练，不输出候选人实际回答或 16 章诊断。回答建议只使用 Transcript/简历/JD 已有事实，缺口用 `[这里需要补充：…]` 占位，假设题/设计题标注「建议 / 假设」；每个符合条件的问题都要做 provenance check。候选人反问不做建议改写，只保留原问与面试官回答原文。

### Codex + 飞书自动归档

当任务来自已配置的飞书机器人时，必须生成两个文件：本地 `review.private.md` 保存「完整实录 + 回答建议 + 16 章诊断」，飞书只发布由确定性脚本生成并校验的 `review.feishu.md`。知识库版仅保留面试官问题/追问、回答建议、候选人反问与面试官回答；删除候选人回答正文、回答定位、评分和个人表现诊断。读取 `references/codex-feishu-automation.md`，遵守以下不变量：

- 每位管理员在自己的系统账户中运行 `codex login`；桥接程序只能调用该账户下的 `codex exec`，不得携带组织共享 OpenAI API Key。
- 每位管理员配置自己的飞书 App ID/Secret；Secret 只从环境变量读取，不写入 Skill、配置文件、报告或日志。
- 归档目标固定为 `vcnvx4cwol1n.feishu.cn` 的知识库 `7677796340709133492` 根目录；不得改投其他空间，创建文档前仍必须验证当前应用确实有读写权限。
- 指定群/私聊中的录音视为管理员部署时的一次性自动处理授权；其他会话不得自动处理。
- 使用飞书 `message_id + file_key` 幂等，重试不得重复建文档。
- `publish_feishu_wiki.py` 只能接受通过知识库隐私契约校验的脱敏版，不能用参数绕过并上传 Full Review。
- 本地 ASR 与 Codex 复盘成功不等于归档成功；必须回读知识库节点和文档块后才能回复最终链接。
- 默认不上传原始录音；只发布验证通过的复盘文档和配置允许的 transcript。

## History / Persistence Behavior

- 过程性历史存 `${PM_INTERVIEW_REVIEW_HOME}`；未设置时使用 `~/.pm-interview-review-os/`。不要写入 Agent 的通用用户画像、长期个人记忆或 Skill 安装目录；Transcript、评分和结果会变，且可能包含敏感信息。
- 每次先读历史索引，再分析当前场；历史只能用于趋势比较，不能预先给当前回答贴标签。
- 记录层以单场 `record.json` 为事实源，聚合层可重建。
- 最佳答案只能由用户事实构成；Story Bank 条目保存 source interview/Q&A 与 evidence status。
- 用户要求删除某场时，删除对应 record 后重建聚合；不要只减计数。
- 原始录音、简历、feedback 默认仅保存在本机，不上传外部服务，除非用户明确要求。

## Evidence Rules

1. 评价、数字、项目事实、业务信息、面试官信号都必须有 Evidence anchor。
2. Transcript Fact、Corroborated Fact、Inference 明确分层。
3. 无时间戳时用 Q&A ID；不得伪造 timestamp。
4. 引用可清理 filler，但不得改数字、否定、主体、因果；有争议时同时给 Raw Evidence。
5. Speaking ratio、平均回答长度、filler 次数等指标只有在输入完整且可可靠分 speaker 时计算；否则写无法可靠计算。
6. “面试官连续追问”只证明 concern 未解除或深挖兴趣，不能单独证明不满意。

## Safety against Hallucination

禁止：虚构经历/数据/反馈；把推断写成事实；用简历事实冒充面试时已说；为了完整硬填 Uncertain；机械 STAR；所有回答给高分；把表达问题与能力问题混为一谈；把单场失误升级为长期弱点；无证据预测录用概率。

遇到事实缺口时保留 `[这里需要补充：XXX]`。遇到 speaker、parent question、interviewer signal 不确定时明确 `Unknown/Uncertain`。宁可少结论，不要假精确。

## Common Pitfalls

1. **问题平铺**：先 Pass 1 对账，再 Pass 2 归树；同一 concern 的追问必须共享 Root。
2. **追问即不满**：同时考虑兴趣深挖与证据质疑，证据不足时保持 Uncertain。
3. **分数伪精确**：展示 weight 与 cap；confidence 低时不做小数点幻觉。
4. **Better Answer 脑补**：逐句 provenance check，缺口用 placeholder。
5. **历史累计漂移**：从 records 重建 aggregates，不手改总数。
6. **把手段当能力**：Growth 不等于活动，AI PM 不等于口号。
7. **报告过长失焦**：第 0.1 节保留全量问答，第 0.2 节覆盖所有可回答节点，第 6 章只深评决定性回答并引用第 0.2 节，不重复 Suggested Answer。

## Verification Checklist

- [ ] 输入与历史基线已清点，原始材料未覆盖。
- [ ] Speaker 不确定处标 Unknown。
- [ ] Pass 1 问题数与 Follow-up Tree 节点可对账，未把追问全部平铺。
- [ ] 每个 root/follow-up 都有原问题、anchor、候选人原回复或 `No answer captured`。
- [ ] 每个可回答节点在第 0.2 节有且仅有一条回答建议；Administrative 与候选人反问没有 Better Answer。
- [ ] 每条候选人反问都与面试官回答原文或 `No answer captured` 配对。
- [ ] 每条重大 finding 有 timestamp/Q&A Evidence。
- [ ] Fact 与 Inference 明确区分。
- [ ] 五维评分使用动态权重并解释 cap。
- [ ] Root Cause 是可修根因，不是症状复述。
- [ ] Better Answer 所有事实均有 provenance；缺失处为 placeholder。
- [ ] Shortcoming Cards 为 3–7 张且按优先级排序。
- [ ] Shadow JD 每条有 Interview Evidence 与 confidence。
- [ ] 单场信号未误写成长期 anti-pattern。
- [ ] History 从 records 重建，Outcome 不覆写旧预测。
- [ ] Next Actions 数量少、动作具体、完成标准可验证。
- [ ] 自动归档任务使用当前系统用户自己的 ChatGPT/Codex 登录，没有共享 OpenAI Key。
- [ ] 飞书任务通过 `message_id + file_key` 去重，写入后已回读验证并返回真实链接。
- [ ] 本地存在 `review.private.md`，飞书发布源是 `review.feishu.md`；知识库版无候选人回答、回答定位、评分或个人诊断。
