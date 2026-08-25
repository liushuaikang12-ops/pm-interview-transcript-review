# PM Interview Review — Full Review（验收自测）

> **本文件为 Skill 验收自测产物，输入均为虚构测试数据，未写入真实历史工作区 `~/.pm-interview-review-os/`。** 所有推断显式写“推断”。

## Source Manifest

| source_id | 类型 | 路径 | 时间戳 | 语言 | 可信用途 |
|---|---|---|---|---|---|
| SRC-T | Transcript | examples/simulated-transcript.md | 有（00:00:05–00:21:00） | zh | 事实源（唯一事实源） |
| SRC-J | JD | examples/simulated-jd.md | 无 | zh | 岗位匹配 / Shadow JD 校验 |
| SRC-R | Resume | examples/simulated-resume.md | 无 | zh | 事实交叉校验（F2） |
| SRC-H | History | — | — | — | **无历史基线（首场）** |

Speaker：单面试官；`Interviewer` / `Candidate`（陈辰）。Transcript 完整、带时间戳、speaker 可靠 → 本场 Confidence 取 **High**。

---

# 0. 面试实录与回答建议

## 0.1 面试官提问与候选人回复

### Q01 — Root
- Parent：Root
- 问题时间：`[00:00:05–00:01:12]`
- 面试官原文：
  > 先做一个两分钟以内的自我介绍，重点说和这个岗位最相关的经历。
- 回答时间：`[00:01:13–00:03:25]`
- 候选人原回复：
  > 我叫陈辰，有两段产品实习。最近在晨光阅读负责新用户增长，主要参与注册流程和新手任务，也跟着做过数据看板。之前在校内做过一个 AI 写作助手。我觉得我执行力比较强，也愿意学习，希望在 AI 产品方向继续发展。除此之外我还做过很多需求，比如会员页改版、Push 文案优化和活动配置，整体上都有参与。

### Q02 — Root
- Parent：Root
- 问题时间：`[00:03:28–00:03:35]`
- 面试官原文：
  > 你挑一个最能体现产品判断的项目讲。
- 回答时间：`[00:03:36–00:05:10]`
- 候选人原回复：
  > 我讲晨光阅读的新用户激活。我们发现新用户留存不好，所以做了新手任务。我的工作是梳理需求、画原型、跟研发上线。上线后任务完成率是 42%，D1 留存从 24% 到 28%。

#### Q02.1 — Follow-up
- Parent：Q02
- 问题时间：`[00:05:12–00:05:20]`
- 面试官原文：
  > 为什么当时要做这个项目，而不是别的问题？
- 回答时间：`[00:05:21–00:06:02]`
- 候选人原回复：
  > 因为留存很重要，而且当时老板比较关注。新用户如果留不下来，后面付费也不会好，所以我们就优先做了。

#### Q02.2 — Follow-up
- Parent：Q02
- 问题时间：`[00:06:05–00:06:13]`
- 面试官原文：
  > 你们怎么发现问题发生在新用户激活，而不是内容供给？
- 回答时间：`[00:06:14–00:07:08]`
- 候选人原回复：
  > 我们看了漏斗，发现注册后很多人没有完成阅读。也访谈了几个用户，他们说不知道先看什么。所以我觉得需要引导。

##### Q02.2.1 — Evidence challenge
- Parent：Q02.2
- 问题时间：`[00:07:10–00:07:16]`
- 面试官原文：
  > 具体有什么数据？样本和口径是什么？
- 回答时间：`[00:07:17–00:08:02]`
- 候选人原回复：
  > 大概有六成用户注册后没有完成首次阅读，访谈可能是七八个用户。数据是数据同学给的，具体窗口我记不太清，应该是当周新用户。

#### Q02.3 — Follow-up
- Parent：Q02
- 问题时间：`[00:08:05–00:08:13]`
- 面试官原文：
  > 为什么选新手任务？还有哪些方案，为什么没选？
- 回答时间：`[00:08:14–00:09:05]`
- 候选人原回复：
  > 新手任务比较常见，开发也比较快。其他方案可能有推荐优化或者新人书单，但当时没有做，主要还是资源有限。

#### Q02.4 — Follow-up
- Parent：Q02
- 问题时间：`[00:09:08–00:09:15]`
- 面试官原文：
  > 你们用什么指标判断它有效？
- 回答时间：`[00:09:16–00:10:12]`
- 候选人原回复：
  > 主要看任务完成率和 D1 留存。任务完成率 42%，D1 从 24% 到 28%，所以项目是有效的。我们也看了 DAU，但没有太大变化。

##### Q02.4.1 — Evidence challenge
- Parent：Q02.4
- 问题时间：`[00:10:15–00:10:25]`
- 面试官原文：
  > D1 上涨就能证明是新手任务带来的吗？实验怎么做的？
- 回答时间：`[00:10:26–00:11:18]`
- 候选人原回复：
  > 我们是全量上线，没有做 A/B，因为工期比较紧。上线那周 D1 涨了 4 个点，我觉得主要就是这个功能带来的，应该没有别的大活动。

#### Q02.5 — Follow-up
- Parent：Q02
- 问题时间：`[00:11:21–00:11:30]`
- 面试官原文：
  > 上线后有没有异常数据？
- 回答时间：`[00:11:31–00:12:28]`
- 候选人原回复：
  > 有，任务奖励领取率很高，但完成首次阅读的人没有同比例增加。另外 D7 没有明显上涨，付费转化还从 2.1% 降到 1.8%。我当时判断是奖励不够大，所以建议提高积分，不过后来没有排期。

##### Q02.5.1 — Evidence challenge
- Parent：Q02.5
- 问题时间：`[00:12:31–00:12:41]`
- 面试官原文：
  > 为什么付费下降？你怎么验证“奖励不够大”这个判断？
- 回答时间：`[00:12:42–00:13:18]`
- 候选人原回复：
  > 这个我没有具体分析。可能是用户只为了拿奖励，也可能是样本波动。因为我后面换项目了，所以没有继续跟。

#### Q02.6 — Follow-up
- Parent：Q02
- 问题时间：`[00:13:22–00:13:32]`
- 面试官原文：
  > 你刚才说“我做了新手任务”，你个人做的关键决策是什么？
- 回答时间：`[00:13:33–00:14:12]`
- 候选人原回复：
  > 方案是大家一起讨论的。我主要画原型、写 PRD、跟进开发，关键决策应该是产品经理带着我们定的。

#### Q02.7 — Follow-up
- Parent：Q02
- 问题时间：`[00:14:16–00:14:25]`
- 面试官原文：
  > 如果现在让你重做一次，你会怎么做？
- 回答时间：`[00:14:26–00:15:15]`
- 候选人原回复：
  > 我还是会做新手任务，但会先做 A/B，也会看 D7 和付费。奖励可以分层，完成阅读再发更多积分。至于推荐优化和新人书单哪个更好，[停顿]我需要再看数据。

### Q03 — Root
- Parent：Root
- 问题时间：`[00:15:20–00:15:28]`
- 面试官原文：
  > 说说你对 AI 写作产品的理解。怎么提高用户第一次生成成功率？
- 回答时间：`[00:15:29–00:16:32]`
- 候选人原回复：
  > 我觉得 AI 产品首先要解决真实用户问题，不能为了 AI 而 AI。体验要简单，Prompt 要写好，模型能力也很重要。可以优化输入框和引导，让用户更容易使用，也可以换更好的模型，这样第一次生成成功率就会提升。

#### Q03.1 — Follow-up
- Parent：Q03
- 问题时间：`[00:16:35–00:16:45]`
- 面试官原文：
  > 你说的“成功”怎么定义？失败以后怎么 recovery？
- 回答时间：`[00:16:46–00:17:20]`
- 候选人原回复：
  > 成功就是用户觉得好用。失败可以让用户重新生成，或者给一些模板。具体指标我还没有系统想过。

### Q04 — Root
- Parent：Root
- 问题时间：`[00:17:24–00:17:34]`
- 面试官原文：
  > 如果这个产品 D7 留存下降，你会做什么增长策略？
- 回答时间：`[00:17:35–00:18:28]`
- 候选人原回复：
  > 我会先发 Push 召回，也可以做签到、积分和邀请好友。不同用户发不同内容，再配一些限时活动，应该能把留存拉回来。

#### Q04.1 — Follow-up
- Parent：Q04
- 问题时间：`[00:18:30–00:18:38]`
- 面试官原文：
  > 用户为什么要回来？你认为 retention driver 是什么？
- 回答时间：`[00:18:39–00:19:16]`
- 候选人原回复：
  > 主要还是有奖励，还有 AI 比较新鲜。如果活动持续做，用户应该会形成习惯。具体 driver 可能要上线后看数据。

> 对账：root/follow-up 节点 16；已捕获回复 16；No answer captured 0；Parent uncertain 0。

## 0.2 回答建议

### Q01
- Recommended Structure：岗位定位 → 最相关经历 → 与 AI Growth 岗位的连接。
- Suggested Answer：我有两段产品实习经历。最近在晨光阅读参与新用户增长，负责需求梳理、原型、PRD 和研发跟进，也接触过数据看板；此前做过校园 AI 写作助手。我希望继续在 AI 产品方向发展。[这里需要补充：两段经历中最能证明岗位匹配的个人结果]。
- Missing Facts：两段经历中最能证明岗位匹配的个人结果。
- Provenance Check：参与晨光阅读新用户增长、数据看板及校园 AI 写作助手 → `[00:01:13–00:03:25]`；需求梳理、原型、PRD 和研发跟进 → `[00:03:36–00:05:10]`、`[00:13:33–00:14:12]`。

### Q02
- Recommended Structure：问题与证据 → 个人动作 → 结果与证据边界。
- Suggested Answer：我选择晨光阅读的新用户激活项目。团队发现新用户留存不好后上线了新手任务；我负责需求梳理、画原型和跟研发上线。上线后任务完成率为 42%，D1 从 24% 到 28%，但因为没有 A/B，这只能说明同期变化，不能严格证明因果。
- Missing Facts：None。
- Provenance Check：个人动作及结果 → `[00:03:36–00:05:10]`；未做 A/B → `[00:10:26–00:11:18]`。

### Q02.1
- Recommended Structure：当时目标 → 优先级依据 → 缺失的比较标准。
- Suggested Answer：当时团队优先处理新用户留存，因为老板关注这一指标，也认为新用户留不下来会影响后续付费。不过现有材料没有记录我们如何比较其他问题的影响和投入，[这里需要补充：优先级评分、机会规模或资源比较]。
- Missing Facts：优先级评分、机会规模或资源比较。
- Provenance Check：老板关注留存且认为会影响后续付费 → `[00:05:21–00:06:02]`。

### Q02.2
- Recommended Structure：漏斗证据 → 访谈证据 → 证据限制。
- Suggested Answer：我们先看漏斗，发现约六成注册用户没有完成首次阅读；随后访谈了约七八位用户，得到“不知道先看什么”的反馈，因此把问题定位到首次阅读引导。但具体数据窗口我当时没有记清，[这里需要补充：数据周期、样本定义和内容供给对照证据]。
- Missing Facts：数据周期、样本定义和内容供给对照证据。
- Provenance Check：漏斗、访谈和用户反馈 → `[00:06:14–00:08:02]`。

### Q02.2.1
- Recommended Structure：指标定义 → 样本与窗口 → 可信度边界。
- Suggested Answer：现有数据是约六成注册用户未完成首次阅读，访谈样本约七八人；数据由数据同学提供，我只记得可能是当周新用户。准确口径和窗口我不能确认，[这里需要补充：SQL/看板定义、时间窗口和样本量]。
- Missing Facts：SQL/看板定义、时间窗口和样本量。
- Provenance Check：六成、七八人及窗口不确定 → `[00:07:17–00:08:02]`。

### Q02.3
- Recommended Structure：候选方案 → 选择理由 → 未完成的 trade-off。
- Suggested Answer：当时考虑过新手任务、推荐优化和新人书单。选择新手任务的现有理由是开发较快、资源有限；但我们没有留下完整的方案比较，[这里需要补充：各方案的用户影响、成本、风险和验证周期]。
- Missing Facts：各方案的用户影响、成本、风险和验证周期。
- Provenance Check：三个方案及资源限制 → `[00:08:14–00:09:05]`。

### Q02.4
- Recommended Structure：主指标 → 护栏指标 → 归因限制。
- Suggested Answer：我们观察了任务完成率、D1 和 DAU：完成率 42%，D1 从 24% 到 28%，DAU 没有明显变化。后续还发现 D7 没涨、付费从 2.1% 降到 1.8%。因此不能只凭 D1 判断项目有效，还需要实验和护栏指标。
- Missing Facts：None。
- Provenance Check：完成率、D1 与 DAU → `[00:09:16–00:10:12]`；D7 与付费异常 → `[00:11:31–00:12:28]`。

### Q02.4.1
- Recommended Structure：承认无法严格归因 → 替代解释 → 重做实验。
- Suggested Answer：这次是全量上线，没有做 A/B，因此只能说明 D1 与上线同期上涨，不能严格证明因果。[这里需要补充：同期活动、渠道和版本变化]。如果重做，我会设置对照组，同时观察 D1、D7 和付费护栏。
- Missing Facts：同期活动、渠道和版本变化。
- Provenance Check：全量上线且没有 A/B → `[00:10:26–00:11:18]`；重做方案 → `[00:14:26–00:15:15]`。

### Q02.5
- Recommended Structure：异常事实 → 原判断 → 未验证假设。
- Suggested Answer：上线后的异常是奖励领取率高，但首次阅读没有同比增加；D7 没有明显上涨，付费从 2.1% 降到 1.8%。我当时提出“奖励不够大”，但没有完成验证，所以它只能算假设。
- Missing Facts：异常数据的分群、显著性和后续验证。
- Provenance Check：奖励领取、D7、付费及未排期 → `[00:11:31–00:12:28]`。

### Q02.5.1
- Recommended Structure：明确未分析 → 假设 → 验证设计。
- Suggested Answer：我当时没有具体分析付费下降，也没有验证“奖励不够大”。用户只为奖励而来和样本波动都只是可能解释。[这里需要补充：付费漏斗分群、显著性、同期变化和验证结果]。
- Missing Facts：付费漏斗分群、显著性、同期变化和验证结果。
- Provenance Check：未具体分析且未继续跟进 → `[00:12:42–00:13:18]`。

### Q02.6
- Recommended Structure：个人职责 → 决策归属 → 可证明的个人影响。
- Suggested Answer：方案由团队共同讨论，关键决策由产品经理带领确定。我的个人职责是画原型、写 PRD 和跟进开发；现有材料不能证明我独立做了关键产品决策。[这里需要补充：我提出并被采用的具体判断或取舍]。
- Missing Facts：个人提出并被采用的具体判断或取舍。
- Provenance Check：个人职责及关键决策归属 → `[00:13:33–00:14:12]`。

### Q02.7
- Recommended Structure：原项目缺口 → 重做实验 → 护栏与方案比较。
- Suggested Answer：如果重做，我会先设计 A/B，并同时观察 D1、D7 和付费；奖励可以分层，在完成阅读后再发更多积分。推荐优化和新人书单哪个更好，需要先基于数据比较，不能直接下结论。
- Missing Facts：A/B 分流、样本量和方案选择标准。
- Provenance Check：A/B、D7、付费和分层奖励 → `[00:14:26–00:15:15]`。

### Q03
- Recommended Structure：定义 First Success → 拆解生成链路 → 评估与恢复。
- Suggested Answer：我的建议是先把第一次生成成功定义为[这里需要补充：用户行为与质量标准]，再拆解输入完整度、生成质量、重试和编辑成本。可以把输入引导和模型能力作为假设，但当前材料没有真实评估或上线经验，不能写成已完成事实。
- Missing Facts：First Success 行为与质量标准、真实评估或上线经验。
- Provenance Check：候选人提出输入引导和模型能力 → `[00:15:29–00:16:32]`。

### Q03.1
- Recommended Structure：成功定义 → 失败类型 → recovery 指标。
- Suggested Answer：这是方案建议：我会把成功拆成生成质量和用户行为两层，并观察首次采纳、重试、编辑和放弃。[这里需要补充：产品当前质量标准和基线]。失败后可提供重试或模板，但还要按失败原因选择恢复路径。
- Missing Facts：产品当前质量标准和基线。
- Provenance Check：候选人提出重新生成和模板 → `[00:16:46–00:17:20]`。

### Q04
- Recommended Structure：定位分群和行为断点 → retention driver 假设 → 实验。
- Suggested Answer：这是方案建议：我不会先默认使用 Push 或积分，而会先按[这里需要补充：用户分群]定位 D7 前没有完成的核心价值行为，再提出 retention driver 假设，并用实验验证召回或产品改动的增量效果。
- Missing Facts：用户分群、行为断点和留存基线。
- Provenance Check：原回答提出 Push、签到、积分和邀请 → `[00:17:35–00:18:28]`。

### Q04.1
- Recommended Structure：持续价值 → 区分奖励和真实驱动力 → 验证方法。
- Suggested Answer：奖励和 AI 新鲜感目前都只是候选假设，不能直接认定为 retention driver。我会先观察留存用户是否持续完成创作、编辑或发布等核心行为，再通过分群与实验验证。[这里需要补充：真实用户行为数据]。
- Missing Facts：真实用户行为数据。
- Provenance Check：原回答把奖励和 AI 新鲜感作为可能驱动 → `[00:18:39–00:19:16]`。

> 对账：eligible questions 16；answer suggestions 16；provenance-complete 16。

## 0.3 候选人反问与面试官回答原文

### RQ01
- 对应 Question ID：Q05
- 候选人反问时间：`[00:19:28–00:19:40]`
- 候选人反问原文：
  > 团队现在最核心的目标和这个岗位会负责的事情是什么？
- 面试官回答时间：`[00:19:41–00:20:48]`
- 面试官回答原文：
  > 我们负责 AI 创作产品的增长，北极星还是创作 DAU，但当前更具体的问题是新用户第一次生成成功率和 D7。这个岗位会参与 onboarding、站内导流和生命周期实验，也要和算法一起定义生成质量评估。我们希望候选人既能看增长漏斗，也能理解从输入、生成、编辑到发布的完整链路，不只是做活动。团队节奏比较快，每周看实验复盘。

> 对账：candidate-reverse-question 1；reverse exchanges 1；Better Answer 0。

---

# 1. Executive Summary

**一句话结论：陈辰是一枚“诚实的执行者”，但没有拿出岗位核心要求的三件事——实验归因、AI 生成机制、留存增长机制——中的任何一件；最致命的不是答错，而是他亲手给出的异常数据（D7 没涨、付费 2.1%→1.8%）反过来推翻了自己的主结论“新手任务有效”。**

下一层追问最可能断在这里：当面试官顺着“第一次生成成功率”继续问“你的成功口径是什么、重试率/放弃率是多少、怎么评估模型质量”时，候选人没有可交付的机制与指标，只有口号（Evidence：[00:16:46]“成功就是用户觉得好用……指标我还没有系统想过”）。

## Interview Verdict
- **Overall Performance: 约 4.3 / 10（range 4.0–4.5）**
- **Confidence: High** —— Transcript 完整、时间戳连续、单面试官、JD/简历齐备。
- **Strongest Areas:**
  1. 坦诚披露不利事实（承认无 A/B、关键决策是 PM 定的、付费下降），无编造迹象。
  2. 执行动作叙述清晰：需求分析、画原型、写 PRD、跟进开发（F2，与简历一致）。
  3. 能复述基础漏斗与留存数字（完成率 42%、D1 24%→28%）。
  4. 有反思意愿（[00:14:26]“会先做 A/B，也会看 D7 和付费”）。
- **Biggest Risks:**
  1. 归因方法缺失：无对照仍主张因果（[00:10:26]），且被自家 D7/付费数据反驳（[00:11:31]）。
  2. AI 产品理解停留在正确口号，无指标/eval/失败恢复（[00:15:29]、[00:16:46]）。
  3. Growth 只剩 Push/签到/积分手段，无 retention 机制（[00:17:35]、[00:18:39]）。
  4. 个人贡献混淆，无法说出一个个人关键决策（[00:13:33]）。
  5. 数据口径模糊、hedging 高（[00:07:17]“记不太清”、[00:12:42]“可能……可能……”）。
- **Likely Interviewer Concerns（推断，High）**：数据与实验能力、AI 机制理解、Growth 机制、Ownership。
- **Positive Signals（行为信号推断）**：无明确正向认可。唯一中性偏正的信号是反问环节面试官愿意详细展开岗位与团队（[00:19:41]，推断，Medium confidence，可能只是标准流程）。
- **Uncertain Areas**：面试官最终评分与是否进入下一轮、D1 涨 4 点的真实原因、付费下降的真实归因（均无证据，不推测）。

---

# 2. Interview Structure

| Stage | Time/Anchor | What happened | Weight in interview |
|---|---|---|---|
| 自我介绍 | 00:00:05–00:03:25 | 候选人自述两段实习 + 校园 AI 项目 | 低（约 12%） |
| 项目深挖（晨光阅读·新用户激活） | 00:03:28–00:15:15 | 11 连问，从“讲项目”一路下沉到归因、异常、个人贡献、反思 | 主体（约 55%） |
| AI 写作产品理解 | 00:15:20–00:17:20 | 首次生成成功率 + 成功定义/recovery | 中（约 12%） |
| Growth 策略 | 00:17:24–00:19:16 | D7 留存下降策略 + retention driver | 中（约 12%） |
| 反问环节 | 00:19:22–00:20:48 | 候选人问 1 问，面试官展开岗位 | 低（约 7%） |
| 收尾 | 00:20:51–00:21:00 | 结束语（Administrative） | — |

---

# 3. Complete Question Map

| ID | Parent | Speaker | Surface Question | Answer Anchor | Underlying Intent（推断） | Competency | Type |
|---|---|---|---|---|---|---|---|
| Q01 | Root | Interviewer | 先做两分钟自我介绍，重点说和岗位最相关的经历 | 00:01:13–00:03:25 | 定位相关经历与自我定位（推断） | Communication / Self-positioning | Self-intro |
| Q02 | Root | Interviewer | 挑一个最能体现产品判断的项目讲 | 00:03:36–00:05:10 | 验证项目深度与产品判断（推断） | Project Deep Dive / Product Sense | Project Deep Dive |
| Q02.1 | Q02 | Interviewer | 为什么当时要做这个项目，而不是别的问题？ | 00:05:21–00:06:02 | Problem Definition / Prioritization（推断） | Prioritization / Problem Definition | Follow-up |
| Q02.2 | Q02 | Interviewer | 怎么发现问题发生在新用户激活，而不是内容供给？ | 00:06:14–00:07:08 | User Insight / Evidence quality（推断） | User Insight / Funnel Analysis | Follow-up |
| Q02.2.1 | Q02.2 | Interviewer | 具体有什么数据？样本和口径是什么？ | 00:07:17–00:08:02 | Metrics / Credibility（推断） | Metrics / Data Analysis | Evidence challenge |
| Q02.3 | Q02 | Interviewer | 为什么选新手任务？还有哪些方案，为什么没选？ | 00:08:14–00:09:05 | Decision Making / Alternatives（推断） | Decision Making / Trade-off | Follow-up |
| Q02.4 | Q02 | Interviewer | 你们用什么指标判断它有效？ | 00:09:16–00:10:12 | Metrics / Guardrail（推断） | Metrics / Attribution | Follow-up |
| Q02.4.1 | Q02.4 | Interviewer | D1 上涨就能证明是新手任务带来的吗？实验怎么做的？ | 00:10:26–00:11:18 | Attribution / Experiment Design（推断） | Attribution / A/B Test | Evidence challenge |
| Q02.5 | Q02 | Interviewer | 上线后有没有异常数据？ | 00:11:31–00:12:28 | Iteration / Unexpected result（推断） | Root Cause Analysis / Iteration | Follow-up |
| Q02.5.1 | Q02.5 | Interviewer | 为什么付费下降？你怎么验证“奖励不够大”这个判断？ | 00:12:42–00:13:18 | Root Cause / Validation（推断） | Root Cause Analysis / Experiment Design | Evidence challenge |
| Q02.6 | Q02 | Interviewer | 你个人做的关键决策是什么？ | 00:13:33–00:14:12 | Ownership / Contribution（推断） | Ownership / Execution | Follow-up |
| Q02.7 | Q02 | Interviewer | 如果现在让你重做一次，你会怎么做？ | 00:14:26–00:15:15 | Reflection / Learning velocity（推断） | Reflection | Follow-up |
| Q03 | Root | Interviewer | 说说你对 AI 写作产品的理解，怎么提高用户第一次生成成功率？ | 00:15:29–00:16:32 | AI Product Mechanism（推断） | AI Product / Model Evaluation | AI Product |
| Q03.1 | Q03 | Interviewer | 你说的“成功”怎么定义？失败以后怎么 recovery？ | 00:16:46–00:17:20 | AI eval / Failure Recovery（推断） | Model Evaluation / Failure Recovery | Follow-up |
| Q04 | Root | Interviewer | 如果这个产品 D7 留存下降，你会做什么增长策略？ | 00:17:35–00:18:28 | Growth mechanism（推断） | Growth / Retention / Growth Loop | Growth |
| Q04.1 | Q04 | Interviewer | 用户为什么要回来？你认为 retention driver 是什么？ | 00:18:39–00:19:16 | Retention mechanism（推断） | Retention / User Insight | Follow-up |
| Q05 | Root | Interviewer | 你有什么想问我的？ | 00:19:28–00:19:40 | 给候选人反问机会（推断） | Reverse Interview | Reverse |

**对账：Pass 1 有效问题 = 17；树节点 = 17；Administrative = 1（[00:20:51–00:21:00] 结束语，非问题）；Uncertain parent = 0。**

---

# 4. Follow-up Trees

## Q02 —— 晨光阅读·新用户激活（核心树）

```text
Q02 挑一个最能体现产品判断的项目讲
├── Q02.1 为什么做这个项目，而不是别的问题？            (Why / Prioritization)
├── Q02.2 怎么发现问题在新用户激活，而不是内容供给？      (Discovery / Evidence)
│   └── Q02.2.1 具体有什么数据？样本和口径是什么？        (Metrics / Credibility)
├── Q02.3 为什么选新手任务？还有哪些方案，为什么没选？    (Decision / Alternatives)
├── Q02.4 你们用什么指标判断它有效？                     (Metrics / Guardrail)
│   └── Q02.4.1 D1 上涨就能证明吗？实验怎么做的？         (Attribution / Experiment)
├── Q02.5 上线后有没有异常数据？                         (Unexpected / Iteration)
│   └── Q02.5.1 为什么付费下降？怎么验证“奖励不够大”？    (Root Cause / Validation)
├── Q02.6 你个人做的关键决策是什么？                     (Ownership / Contribution)
└── Q02.7 如果重做一次，你会怎么做？                     (Reflection)
```

- **统一 concern**：验证“项目真实决策质量与归因可靠性”，沿 `做了什么 → 为什么 → 证据 → 方案取舍 → 指标 → 归因 → 异常 → 个人贡献 → 反思` 逐层下沉。
- **触发下一问的 Candidate answer**：Q02.2.1 因“六成未完成首次阅读、访谈七八个、窗口记不太清”触发口径追问；Q02.4.1 因“全量上线没做 A/B 仍主张功能带来上涨”触发归因质疑；Q02.5.1 因“奖励领取率高但首读没同比例增、D7 没涨、付费下降”触发对“奖励不够大”判断的验证追问。
- **Parent uncertainty**：无。单面试官，追问显式指代同一项目/同一组数据，结构清晰。

## Q03 —— AI 写作产品

```text
Q03 对 AI 写作产品的理解，怎么提高首次生成成功率？
└── Q03.1 “成功”怎么定义？失败后怎么 recovery？
```

## Q04 —— D7 留存增长

```text
Q04 如果 D7 留存下降，你会做什么增长策略？
└── Q04.1 用户为什么要回来？retention driver 是什么？
```

---

# 5. Competency Mapping

| Competency | Evidence | Current signal | Confidence |
|---|---|---|---|
| Attribution | Q02.4.1 无 A/B 仍主张因果；Q02.5.1 付费下降未分析 | **Weak** | High |
| Experiment Design | Q02.4.1 全量上线、工期紧 | **Missing** | High |
| Metrics / Data Analysis | Q02.2.1 口径/窗口不清、“数据同学给的” | **Weak** | High |
| User Insight | Q02.2 漏斗 + 访谈，但样本/口径弱 | **Partial** | Medium |
| Decision Making / Prioritization | Q02.1 “老板关注”，Q02.3 “资源有限” | **Weak** | High |
| AI Product Mechanism | Q03/Q03.1 口号化、无指标无 eval | **Weak** | High |
| Growth Mechanism | Q04/Q04.1 手段堆砌、无 retention driver | **Weak** | High |
| Ownership | Q02.6 “关键决策是产品经理带着定的” | **Weak** | High |
| Reflection | Q02.7 “会做 A/B、看 D7 付费”，但无根因 | **Partial** | Medium |
| Communication / Structure | 各回答结论不前置、hedging 多 | **Partial** | Medium |

## PM Evidence Chain —— 晨光阅读·新用户激活项目

1. Problem：**Partial**（“新用户留存不好”，但未界定具体用户/场景/边界）
2. Evidence：**Partial**（六成未完成首读、访谈 7–8 人，但口径/窗口/样本来源弱）
3. Insight：**Missing**（“不知道先看什么→需要引导”是现象复述，不是机制判断）
4. Decision：**Weak**（“老板关注 + 资源有限”，无优先级标准）
5. Solution：**Partial**（新手任务，无 insight→机制的推导）
6. Experiment：**Missing**（全量上线，无 A/B）
7. Metric：**Partial**（完成率 + D1，无 guardrail，口径不清）
8. Attribution：**Contradicted**（主张 D1 涨=功能有效，但 D7 没涨、付费 2.1%→1.8%）
9. Iteration：**Weak**（“建议提高积分”未验证、未排期，换项目后未跟）
10. Reflection：**Partial**（要 A/B、看 D7/付费，但无根因与反事实）

---

# 6. Key Answer Reviews

## Q02 —— 挑一个最能体现产品判断的项目讲

- **Surface Question**：挑一个最能体现产品判断的项目讲。
- **Underlying Intent（推断，High）**：让候选人用一个自选项目展示产品判断与证据闭环，作为后续深挖的锚点。
- **Candidate Answer — Clean Version**：讲晨光阅读新用户激活；发现新用户留存不好，做新手任务；我负责梳理需求、画原型、跟研发上线；上线后任务完成率 42%，D1 留存从 24% 到 28%。
- **Raw Evidence**：[00:03:36–00:05:10]（数字与口径原文见 Evidence Ledger E2）。

### Score

| Dimension | Score | Evidence-based reason |
|---|---:|---|
| Substance | 5 | 有 Problem/Solution/Metric 骨架，但缺 Insight、Attribution、Iteration |
| Structure | 5 | 平铺，无结论前置，无 why 链条 |
| Relevance | 7 | 选了最相关项目，方向正确 |
| Credibility | 5 | 数字给了但口径不清，后续“无 A/B”削弱因果可信度 |
| Differentiation | 3 | “新手任务”是常见做法，无独有判断 |

- Weight profile：**Project Deep Dive**（S .30 / Str .15 / R .20 / C .25 / D .10）
- Raw weighted score：5×.30 + 5×.15 + 7×.20 + 5×.25 + 3×.10 = **5.2**
- Cap/penalty：无（Credibility=5，未触发 ≤3 的归因 cap）
- **Overall Score：5.2 / 10**
- **Gap Type**：Evidence（缺 insight 与口径）+ Communication（结构平铺）

### Root Cause

`Finding：项目叙述有骨架但无 insight 与证据闭环 → 无“为什么新手任务能解决‘不知道先看什么’”的机制推导 → RC-NO-INSIGHT（primary）+ RC-METRIC-DEFINITION（secondary）→ Why it matters：面试官后续 11 连问正是为了验证这层骨架下的真实判断，而每一层追问都暴露了骨架的空心。`

### Answer Suggestion Reference
- 参见：`0.2 / Q02`
- 本章不重复 Suggested Answer 或 Provenance Check。

---

## Q02.4.1 —— D1 上涨就能证明是新手任务带来的吗？实验怎么做的？

- **Surface Question**：D1 上涨就能证明是新手任务带来的吗？实验怎么做的？
- **Underlying Intent（推断，High）**：验证 Attribution 方法——是否用实验/对照排除混淆，而非只看前后对比。
- **Candidate Answer — Clean Version**：我们是全量上线，没有做 A/B，因为工期比较紧。上线那周 D1 涨了 4 个点，我觉得主要就是这个功能带来的，应该没有别的大活动。
- **Raw Evidence**：[00:10:26–00:11:18]。

### Score

| Dimension | Score | Evidence-based reason |
|---|---:|---|
| Substance | 2 | 没有归因方法，只承认“没做 A/B”，且仍下因果结论 |
| Structure | 5 | 简短、结论明确，但完整度不足 |
| Relevance | 7 | 直接回应了“实验怎么做”，坦白无实验 |
| Credibility | 2 | “主要就是这个功能带来的”“应该没有别的大活动”无对照支撑，且被后续 D7/付费数据反驳 |
| Differentiation | 2 | 无任何归因替代方案（同期 baseline、分群、断点） |

- Weight profile：**Data / Experiment / Attribution**（S .25 / Str .10 / R .20 / C .35 / D .10）
- Raw weighted score：2×.25 + 5×.10 + 7×.20 + 2×.35 + 2×.10 = **3.3**
- Cap/penalty：Credibility=2 且核心结论依赖未证实因果 → 触发 ≤5.0 上限；3.3 未触碰，不额外扣分。
- **Overall Score：3.3 / 10**
- **Gap Type**：Capability（归因/实验方法缺失）+ Evidence（无对照）。

### Root Cause

`Finding：全量上线无对照仍主张“功能带来上涨” → 把前后相关当因果，且后续异常数据直接反驳该结论 → RC-NO-VALIDATION（primary）+ RC-CAUSAL-LEAP（secondary）→ Why it matters：JD 明确“分析漏斗与留存数据、推动实验迭代”，归因是岗位核心；此回答会被判定为无法判断功能真实价值，且连带 D7/付费的异常说明候选人没有后续验证习惯。`

### Answer Suggestion Reference
- 参见：`0.2 / Q02.4.1`
- 本章不重复 Suggested Answer 或 Provenance Check。

---

## Q02.6 —— 你个人做的关键决策是什么？

- **Surface Question**：你刚才说“我做了新手任务”，你个人做的关键决策是什么？
- **Underlying Intent（推断，High）**：区分个人贡献与团队贡献，验证 Ownership。
- **Candidate Answer — Clean Version**：方案是大家一起讨论的。我主要画原型、写 PRD、跟进开发，关键决策应该是产品经理带着我们定的。
- **Raw Evidence**：[00:13:33–00:14:12]。

### Score

| Dimension | Score | Evidence-based reason |
|---|---:|---|
| Substance | 3 | 明确承认关键决策不是自己的，无个人判断产出 |
| Structure | 5 | 清晰但直接暴露贡献薄弱 |
| Relevance | 8 | 直接回答，未回避 |
| Credibility | 6 | 坦诚（不夸大贡献），但正因坦诚暴露了执行者定位 |
| Differentiation | 2 | 无个人取舍或判断 |
- Weight profile：**Behavioral / Collaboration**（S .20 / Str .20 / R .25 / C .25 / D .10）
- Raw weighted score：3×.20 + 5×.20 + 8×.25 + 6×.25 + 2×.10 = **5.3**
- Cap/penalty：无。
- **Overall Score：5.3 / 10**
- **Gap Type**：Capability（贡献层个人判断缺失）。

### Root Cause

`Finding：把“我做了新手任务”的实际个人动作收窄到执行（画原型/写 PRD/跟进），关键决策归给 PM → RC-CONTRIBUTION（primary）→ Why it matters：JD 要求“执行力强”但岗位也评估产品判断；简历写“负责需求分析、原型、PRD 与研发跟进”，访谈却把决策权让给 PM，形成 F2 vs F1 的落差，会被解读为只做执行、未形成判断。`

### Answer Suggestion Reference
- 参见：`0.2 / Q02.6`
- 本章不重复 Suggested Answer 或 Provenance Check。

---

## Q03 —— 对 AI 写作产品的理解，怎么提高首次生成成功率？

- **Surface Question**：说说你对 AI 写作产品的理解。怎么提高用户第一次生成成功率？
- **Underlying Intent（推断，High）**：验证 AI 产品机制——是否理解“输入→生成→评估→失败恢复”的完整链路，而非喊口号。
- **Candidate Answer — Clean Version**：AI 产品首先要解决真实用户问题，不能为了 AI 而 AI；体验要简单，Prompt 要写好，模型能力也很重要；可以优化输入框和引导，也可以换更好的模型，这样第一次生成成功率就会提升。
- **Raw Evidence**：[00:15:29–00:16:32]。

### Score

| Dimension | Score | Evidence-based reason |
|---|---:|---|
| Substance | 3 | 只有“真实问题/简单/写好 Prompt/换模型”等口号，无机制、指标、边界 |
| Structure | 5 | 有分点，但每点都是方向而非机制 |
| Relevance | 6 | 扣题提到“首次生成成功率”，但未拆解成功因子 |
| Credibility | 4 | “换更好模型”未考虑成本/质量权衡，无可验证依据 |
| Differentiation | 2 | 纯正确口号，无独有判断（AI Product Depth Insufficient） |

- Weight profile：**AI Product Mechanism**（S .30 / Str .15 / R .20 / C .20 / D .15）
- Raw weighted score：3×.30 + 5×.15 + 6×.20 + 4×.20 + 2×.15 = **3.95**
- Cap/penalty：只给正确口号、无岗位机制 → 触发 AI/Growth mechanism ≤5.0 上限；3.95 未触碰。
- **Overall Score：4.0 / 10**
- **Gap Type**：Capability（AI 机制缺失）+ Knowledge（缺 eval/failure 概念）。

### Root Cause

`Finding：把“首次生成成功率”答成“体验简单 + 换好模型”的泛化口号，追问“成功怎么定义/怎么 recovery”时回答“成功就是用户觉得好用”“指标没系统想过”（[00:16:46]）→ RC-AI-CONCEPTUAL（primary）+ RC-AI-NO-EVAL（secondary）→ Why it matters：JD 明确“和算法一起定义生成质量评估”“理解输入→生成→编辑→发布完整链路”，口号化回答会被判定为不具备 AI 产品机制理解。`

### Answer Suggestion Reference
- 参见：`0.2 / Q03`
- 本章不重复 Suggested Answer 或 Provenance Check。

---

## Q04 —— 如果 D7 留存下降，你会做什么增长策略？

- **Surface Question**：如果这个产品 D7 留存下降，你会做什么增长策略？
- **Underlying Intent（推断，High）**：验证 Growth 机制——是否从“用户为什么回来”出发设计，而非堆砌触达手段。
- **Candidate Answer — Clean Version**：先发 Push 召回，也可以做签到、积分和邀请好友；不同用户发不同内容，再配一些限时活动，应该能把留存拉回来。
- **Raw Evidence**：[00:17:35–00:18:28]。

### Score

| Dimension | Score | Evidence-based reason |
|---|---:|---|
| Substance | 3 | 只有 Push/签到/积分/邀请/活动等手段清单，无 segment/trigger/机制/增量 |
| Structure | 5 | 列了点，但无逻辑主线 |
| Relevance | 7 | 直接回应增长策略，方向对 |
| Credibility | 4 | 无数据与增量概念支撑，“应该能拉回来”是口号 |
| Differentiation | 2 | 全是通用手段，无机制判断 |

- Weight profile：**Growth Strategy**（S .30 / Str .15 / R .20 / C .20 / D .15）
- Raw weighted score：3×.30 + 5×.15 + 7×.20 + 4×.20 + 2×.15 = **4.15**
- Cap/penalty：Growth 手段堆砌无机制 → 触发 ≤5.0 上限；4.15 未触碰。
- **Overall Score：4.2 / 10**
- **Gap Type**：Capability（Growth 机制缺失）。

### Root Cause

`Finding：D7 留存下降直接答成“Push/签到/积分/邀请/活动”手段堆砌，追问 retention driver 时答“有奖励、AI 新鲜、活动持续做会形成习惯、具体 driver 上线后看数据”（[00:18:39]）→ RC-GROWTH-TACTIC（primary）+ RC-GROWTH-NO-LOOP（secondary）→ Why it matters：面试官反问环节强调“不只是做活动”（[00:19:41]），与候选人此前的回答形成直接对照，暴露其把增长等同为运营活动的底层偏差。`

### Answer Suggestion Reference
- 参见：`0.2 / Q04`
- 本章不重复 Suggested Answer 或 Provenance Check。

---

# 7. Evidence & Quotes

| Evidence ID | Anchor | Speaker | Quote（清理 filler，保原意） | Level | Used for |
|---|---|---|---|---|---|
| E1 | 00:01:13–00:03:25 | Candidate | 晨光阅读新用户增长实习，参与注册流程、新手任务、数据看板；校内做过 AI 写作助手 | F1 | 背景 |
| E2 | 00:03:36–00:05:10 | Candidate | 新手任务完成率 42%，D1 留存 24%→28% | F2（与简历一致） | Q02 |
| E3 | 00:05:21–00:06:02 | Candidate | “因为留存很重要，而且当时老板比较关注” | F1 | Q02.1 优先级 |
| E4 | 00:06:14–00:07:08 | Candidate | 看漏斗发现注册后很多人没完成阅读；访谈用户说“不知道先看什么” | F1 | Q02.2 |
| E5 | 00:07:17–00:08:02 | Candidate | 六成用户注册后没完成首次阅读；访谈七八个；数据是数据同学给的，窗口记不太清 | F1 | Q02.2.1 口径 |
| E6 | 00:08:14–00:09:05 | Candidate | 新手任务常见、开发快；推荐优化/新人书单没做，资源有限 | F1 | Q02.3 取舍 |
| E7 | 00:09:16–00:10:12 | Candidate | 看任务完成率 42% 和 D1 24→28；DAU 没太大变化 | F1 | Q02.4 |
| E8 | 00:10:26–00:11:18 | Candidate | 全量上线，没做 A/B，工期紧；D1 涨 4 点，“主要就是这个功能带来的，应该没有别的大活动” | F1 | Q02.4.1 归因 |
| E9 | 00:11:31–00:12:28 | Candidate | 奖励领取率很高但完成首次阅读没同比例增加；D7 没明显涨；付费 2.1%→1.8%；判断“奖励不够大”，建议提积分，没排期 | F1 | Q02.5 异常 |
| E10 | 00:12:42–00:13:18 | Candidate | “这个我没有具体分析”；“可能是用户只为了拿奖励，也可能是样本波动”；换项目了没继续跟 | F1 | Q02.5.1 无根因 |
| E11 | 00:13:33–00:14:12 | Candidate | 方案一起讨论；我画原型、写 PRD、跟进开发；“关键决策应该是产品经理带着我们定的” | F1 | Q02.6 贡献 |
| E12 | 00:14:26–00:15:15 | Candidate | 还是做新手任务，但先做 A/B、看 D7 和付费；奖励分层；“推荐优化和新人书单哪个更好，我需要再看数据” | F1 | Q02.7 反思 |
| E13 | 00:15:29–00:16:32 | Candidate | “解决真实问题，不能为了 AI 而 AI”；体验简单、Prompt 写好、换更好模型 | F1 | Q03 AI 口号 |
| E14 | 00:16:46–00:17:20 | Candidate | “成功就是用户觉得好用”；失败可重新生成或给模板；“具体指标我还没有系统想过” | F1 | Q03.1 无 eval |
| E15 | 00:17:35–00:18:28 | Candidate | Push 召回、签到、积分、邀请好友、不同内容、限时活动 | F1 | Q04 手段堆砌 |
| E16 | 00:18:39–00:19:16 | Candidate | “主要还是有奖励，还有 AI 比较新鲜”；“具体 driver 可能要上线后看数据” | F1 | Q04.1 无机制 |
| E17 | 00:19:41–00:20:48 | Interviewer | 北极星是创作 DAU；当前问题是新用户第一次生成成功率与 D7；岗位参与 onboarding、站内导流、生命周期实验，和算法一起定义生成质量评估；希望理解输入→生成→编辑→发布完整链路，“不只是做活动”；每周看实验复盘 | F1 | Shadow JD / Q04 对照 |
| I1 | 00:07:10 / 00:10:15 / 00:12:31 / 00:13:22 | Interviewer | 连续索要数据口径、挑战因果、要求个人决策 | I1（推断） | 面试官信号 |
| I2 | 00:16:35 / 00:18:30 | Interviewer | 追问“成功定义/recovery”“retention driver” | I1（推断） | 面试官信号 |

> 说明：E17 为面试官原话（Fact），作为 Shadow JD 与 Q04 改写的约束事实使用；不用于给候选人能力贴标签。

---

# 8. Shortcoming Cards

> 总数 5 张，按「对录用判断的影响 × 重复性 × 可修复性」排序。

## Card 1 — 无对照却下因果结论（Attribution 缺失）

- **Severity: High**
- **Frequency: 2 / 2 个相关节点**（Q02.4.1、Q02.5.1）
- **Evidence**：[00:10:26] 全量无 A/B 仍说“主要就是这个功能带来的”；[00:11:31] D7 没涨、付费 2.1%→1.8%，与“有效”结论直接矛盾。
- **Root Cause**：RC-NO-VALIDATION（primary）+ RC-CAUSAL-LEAP（secondary）
- **Interview Risk（推断）**：JD 要求“分析数据、推动实验迭代”，归因是核心；会被判定为无法判断功能真实价值，且暴露无验证习惯。
- **Corrective Principle**：区分“相关”与“因果”；下结论前必须有对照（A/B 或准实验/分群/同期 baseline）。
- **Drill**：为晨光项目补出“无对照下如何补救归因”的口头方案（分群对比 + 同期 baseline + 后续 A/B），完成标准 = 能口头解释“D1 涨 4 点为什么不能直接算新手任务的功劳”。

## Card 2 — Growth 停留在手段堆砌，无 retention 机制

- **Severity: High**
- **Frequency: 2 / 2 个相关节点**（Q04、Q04.1）
- **Evidence**：[00:17:35] Push/签到/积分/邀请/活动；[00:18:39] “有奖励 + AI 新鲜”“具体 driver 上线后看数据”。
- **Root Cause**：RC-GROWTH-TACTIC（primary）+ RC-GROWTH-NO-LOOP（secondary）
- **Interview Risk（推断）**：面试官反问环节明确“不只是做活动”（[00:19:41]），直接对照候选人的回答；会被判定为不具备增长机制思考。
- **Corrective Principle**：先归因（谁、哪一步、何时流失），再提 retention driver 假设，再设计机制实验；手段是机制的下游，不是答案本身。
- **Drill**：为 AI 创作产品写一个 D7 留存诊断框架（segment × 流失节点 × 回访动机假设 × 对应实验），完成标准 = 能从“用户为什么回来”出发回答，而非列手段。

## Card 3 — AI 产品理解口号化，无指标/eval/失败恢复

- **Severity: High**
- **Frequency: 2 / 2 个相关节点**（Q03、Q03.1）
- **Evidence**：[00:15:29] “解决真实问题/体验简单/写好 Prompt/换更好模型”；[00:16:46] “成功就是用户觉得好用”“指标没系统想过”。
- **Root Cause**：RC-AI-CONCEPTUAL（primary）+ RC-AI-NO-EVAL（secondary）
- **Interview Risk（推断）**：JD 要求“和算法一起定义生成质量评估”“理解完整链路”；口号化会被判定为不具备 AI 产品机制理解（AI Product Depth Insufficient）。
- **Corrective Principle**：任何 AI 结论落到可测口径（成功率/重试率/编辑率/放弃率）+ 失败恢复 + eval；不给无机制的“正确口号”。
- **Drill**：为“校园 AI 写作助手”补机制拆解（成功口径、失败率/重试率、意图→生成→质量链条、一个 eval 指标），完成标准 = 能说出“成功”的可测口径 + 至少一个 recovery 设计。

## Card 4 — 个人贡献混淆，无法说出关键决策

- **Severity: Medium-High**
- **Frequency: 3 / 17 个回答节点**（Q02.1“老板关注”、Q02.3“资源有限”、Q02.6“PM 带着定”）
- **Evidence**：[00:13:33] “关键决策应该是产品经理带着我们定的”；简历写“负责需求分析、原型、PRD 与研发跟进”，访谈把决策权让给 PM（F2 vs F1 落差）。
- **Root Cause**：RC-CONTRIBUTION（primary）
- **Interview Risk（推断）**：实习岗会评估 ownership 与产品判断，可能被判定为“只做执行、未形成判断”。
- **Corrective Principle**：用“我独立做的判断 + 依据 + 取舍 + 结果”替换“我们/老板/资源有限”；执行动作与判断产出分开表述。
- **Drill**：为每个项目写至少 1 个“个人关键决策 + 依据 + 取舍”，完成标准 = 被问“你个人做了什么决策”时能即时给出有依据的个人动作。

## Card 5 — 数据口径模糊 + 优先级判断缺逻辑

- **Severity: Medium**
- **Frequency: 3 / 17 个回答节点**（Q02.1、Q02.2.1、Q02.5.1）
- **Evidence**：[00:07:17] “窗口记不太清、数据同学给的”；[00:05:21] “老板比较关注”；[00:12:42] “可能……可能……”。
- **Root Cause**：RC-METRIC-DEFINITION（primary）+ RC-NO-DECISION-LOGIC（secondary）
- **Interview Risk（推断）**：JD 要求“数据敏感”，口径不清 + hedging 高会系统性降低可信度。
- **Corrective Principle**：每个关键数字讲清分母/窗口/来源；优先级判断用“问题规模 × 可影响性 × 成本”而非“老板关注/资源有限”。
- **Drill**：为晨光项目补口径卡片（每个数字的分母/窗口/来源），完成标准 = 所有关键数字可脱口给出口径，hedging 明显下降。

---

# 9. Anti-patterns

> 统计单位：一次独立 Q&A 节点出现算 1 次；同一回答内重复口头禅不重复计。Eligible answers = 17（本场全部候选回答节点）。

| Anti-pattern | 本场 | 历史累计 | 最近 3 场 | 最近 5 场 | Trend | Evidence |
|---|---:|---:|---:|---:|---|---|
| 归因跳跃（无对照下因果） | 2 | Insufficient history | — | — | Insufficient history | Q02.4.1、Q02.5.1 |
| Growth 手段堆砌（无机制） | 2 | Insufficient history | — | — | Insufficient history | Q04、Q04.1 |
| AI 概念化（无指标/eval） | 2 | Insufficient history | — | — | Insufficient history | Q03、Q03.1 |
| 贡献/责任混淆 | 3 | Insufficient history | — | — | Insufficient history | Q02.1、Q02.3、Q02.6 |
| Hedging / 口径模糊 | 3 | Insufficient history | — | — | Insufficient history | Q02.2.1、Q02.5.1、Q04.1 |

> **本场为首场测试，无历史基线，不判定任何跨场趋势，也不写 Improving/Stable/Worsening。**

---

# 10. Project Probe Depth

## 晨光阅读 · 新用户激活

- **Current Probe Depth: 3 / 10**（L1–L3 有 Partial 证据，L4 开始断裂）
- **连续证据到：Layer 3（Evidence）**
- **首个断点：Layer 4（Why this solution）** —— 候选人说“新手任务常见、开发快”，未给出 insight→机制→方案的推导
- **孤立强证据：Layer 7（Unexpected result）** —— [00:11:31] 奖励领取率高但首读没同比例增、付费 2.1%→1.8%，是真实有价值的异常披露，但因 L4–L6 断裂而孤立
- **下一步补证据**：L4（为什么新手任务）、L6（guardrail 与口径）、L8（付费下降根因）、L9（基于根因的迭代）

| Layer | Status | Evidence | Missing |
|---:|---|---|---|
| 1 What | Partial | [00:03:36] 梳理需求/画原型/PRD/上线 | 个人决策边界 |
| 2 Why | Partial | [00:05:21] 留存重要 + 老板关注 | 问题规模/优先级标准 |
| 3 Evidence | Partial | [00:07:17] 六成未首读、访谈七八个 | 口径/窗口/样本来源 |
| 4 Why this solution | **Missing** | “常见、开发快” | insight→机制推导 |
| 5 Alternative | Partial | [00:08:14] 提到推荐优化/新人书单 | 未比较取舍 |
| 6 Metrics | Partial | [00:09:16] 完成率 42% + D1 | guardrail、口径 |
| 7 Unexpected | Partial | [00:11:31] 领取率高但首读未同增、付费降 | 归因 |
| 8 Root cause | Missing | [00:12:42] “没具体分析” | 付费下降根因 |
| 9 Iteration | Missing | 换项目后未跟 | 基于根因的下一步 |
| 10 What differently | Partial | [00:14:26] 做 A/B、看 D7/付费 | 反事实与边界 |

> 说明：L7 有异常事实，但 L4–L6 断裂，故连续深度定为 3/10，不因“面试官问到了第 8 层”而写成 8/10。

---

# 11. Role-specific Review

> 岗位为「AI 创作增长 PM」，AI Product 与 Growth 两个模块均启用。

## AI Product Depth

| 检查项 | 状态 | Evidence |
|---|---|---|
| User Intent | Missing | 未谈意图判定/输入补齐（[00:15:29]） |
| Model Capability / Limitation | Weak | 只说“换更好模型”，无能力边界/幻觉/非确定性 |
| Context / Memory / Tool | Missing | 未提及 |
| Generation Quality / Evaluation | **Missing** | “指标没系统想过”（[00:16:46]） |
| Latency / Cost / Quality Trade-off | Missing | “换更好模型”未提代价 |
| First Success / Retry / Edit Cost | Weak | “重新生成/给模板”（[00:16:46]）但无指标 |
| Failure Recovery | Weak | 只有重新生成/模板，无机制 |
| HITL | Missing | 未提及 |
| Feedback Loop | Missing | 未提及 |
| AI UX | Weak | “体验简单/引导”停留在口号 |

**结论：AI Product Depth Insufficient**（[00:15:29]、[00:16:46]）。候选人只有正确口号，无机制、指标、边界，Differentiation 已按规则压到 ≤5。

## Growth Mechanism

`User Motivation → Trigger → Activation → First Value → Habit → Retention → Growth Loop`

| 环节 | 状态 | Evidence |
|---|---|---|
| Segment | Missing | “不同用户发不同内容”无 segment 定义 |
| Trigger / Activation | Weak | Push/签到/积分/限时活动 |
| First Value / Value Delivery | Missing | 未谈用户获得什么价值 |
| Habit | Weak | “活动持续做会形成习惯”，无机制 |
| Retention driver | **Missing** | “有奖励 + AI 新鲜，具体 driver 上线后看数据”（[00:18:39]） |
| Growth Loop | Missing | 无 loop 设计 |
| Attribution / Guardrail | Missing | 无增量口径、无防补贴/作弊 |

**结论：Growth 能力停留在 tactic 层**（Push/签到/积分/补贴），未通过 `Activation→Value→Retention→Loop` 机制测试，与面试官“不只是做活动”（[00:19:41]）的要求直接不符。

## Strategy Depth

`Not activated — 本场岗位与问题没有提供足够的 Strategy PM 证据。`

---

# 12. Interviewer Signals

| Anchor | Observable behavior | Signal | Alternative explanation | Confidence |
|---|---|---|---|---|
| 00:07:10 | “具体有什么数据？样本和口径是什么？” | Concern（口径未解除） | 常规深挖证据 | High |
| 00:10:15 | “D1 上涨就能证明吗？实验怎么做的？” | Concern（挑战因果） | 兴趣深挖归因 | High |
| 00:12:31 | “为什么付费下降？怎么验证‘奖励不够大’？” | Concern（挑战未验证判断） | 兴趣深挖异常 | High |
| 00:13:22 | “你个人做的关键决策是什么？” | Concern（贡献边界） | 常规 ownership 检查 | Medium |
| 00:16:35 | “成功怎么定义？失败怎么 recovery？” | Concern（AI 机制未达预期） | 岗位核心探测 | Medium |
| 00:18:30 | “用户为什么要回来？retention driver 是什么？” | Concern（growth 机制未达预期） | 岗位核心探测 | Medium |
| 00:19:41 | 详细展开岗位并强调“不只是做活动” | Neutral–纠正（推断） | 也可能只是标准岗位说明 | Medium |

> 以上为行为信号推断，不等于真实评分或录用结论。本场未观察到明确的 Positive 认可信号。

## Interviewer Model（Interview Style only）
- **Style**：Data-driven、Detail-oriented、Mechanism/Execution-heavy。
- **Evidence**：反复索要数据口径/样本/实验（[00:07:10]、[00:10:15]）、追问异常与根因（[00:12:31]）、追问机制（[00:16:35]、[00:18:30]）、强调“完整链路”与“每周实验复盘”（[00:19:41]）。
- 不做人格推断。

---

# 13. Reverse Interview Intelligence

## Candidate Questions

| ID | Question | Answer anchor | Quality |
|---|---|---|---|
| RQ01 | 团队现在最核心的目标和这个岗位会负责的事情是什么？ | 00:19:41–00:20:48 | 中规中矩：问到岗位核心信息，但只有 1 问，未继续追问协作、评估或期望反馈 |

> 候选人反问与面试官回答原文参见 `0.3 / RQ01`。本章不改写反问，也不重复整段原文。

## Information Revealed

| Category | Transcript Fact | Anchor | Inference（可选） | Confidence |
|---|---|---|---|---|
| Product | AI 创作产品（增长方向） | 00:19:41 | — | High |
| KPI | 北极星 = 创作 DAU；短期焦点 = 首次生成成功率 + D7 | 00:19:41 | — | High |
| Current Problem | 新用户第一次生成成功率、D7 留存 | 00:19:41 | — | High |
| Candidate Role | onboarding、站内导流、生命周期实验；与算法一起定义生成质量评估 | 00:19:41 | — | High |
| Expectation | 既能看增长漏斗，也能理解输入→生成→编辑→发布完整链路，“不只是做活动” | 00:19:41 | — | High |
| Work Style | 节奏快、每周看实验复盘 | 00:19:41 | — | High |
| Team | 与算法团队协同（跨算法协作） | 00:19:41 | — | High |
| Hiring Signal | 强调“完整链路理解、不只是活动” | 00:19:41 | 面试官可能在纠正候选人“活动堆砌”的倾向（推断） | Medium |

---

# 14. Shadow JD

| Official JD | Interview Evidence（反问环节） | Shadow JD（推断） | Confidence |
|---|---|---|---|
| 参与新用户增长与生命周期策略 | “岗位参与 onboarding、站内导流、生命周期实验” [00:19:41] | 核心工作 = 增长漏斗实验（onboarding/站内/生命周期） | High |
| 分析漏斗与留存数据，推动实验迭代 | “每周看实验复盘”“理解完整链路” [00:19:41] | 对数据 + 实验能力是硬要求，非加分项 | High |
| 协同算法、设计、研发优化 AI 创作体验 | “和算法一起定义生成质量评估” [00:19:41] | 需要跨算法协作、理解生成质量，具备一定技术/算法对话能力 | High |
| （JD 未细化北极星） | “北极星还是创作 DAU，当前更具体的问题是首次生成成功率与 D7” [00:19:41] | 短期考核 = 首次生成成功率 + D7，而非泛泛 DAU | High |
| 对 AIGC/Agent 有兴趣和理解 | “理解从输入、生成、编辑到发布的完整链路，不只是做活动” [00:19:41] | 岗位偏「AI Growth」，要求 AI 产品机制理解，非纯运营活动岗 | High |
| 执行力强 | “团队节奏比较快，每周看实验复盘” [00:19:41] | 要求能快速产出并跟进实验，执行密度高（推断） | Medium |

> 关键结论：Shadow JD 显示该岗位本质是「AI 创作产品的增长与生成质量」，面试官明确“不只是做活动”——这解释了本场对 Attribution、AI 机制、Growth 机制的三连深挖，也构成候选人三个核心短板（Card 1/2/3）的岗位风险来源。

---

# 15. Cross-interview Update

- **History baseline：0 场（本场为验收自测首场，无历史基线）。**
- **本场不写入真实历史工作区 `~/.pm-interview-review-os/`**；因此无 records 可重建聚合，不产生任何跨场趋势结论。
- **Question Bank changes**：无历史对比；本场 17 问（见 Chapter 3）可作未来题库的候选初始项，但本测试未持久化。
- **Competency Matrix changes**：无历史；本场 observations 见 Chapter 5，仅为本场单点信号。
- **Anti-pattern changes**：无历史；本场计数见 Chapter 9，一律 `Insufficient history`。
- **Project Probe Depth changes**：无历史；本场「晨光阅读·新用户激活」3/10（见 Chapter 10）。
- **Story Bank candidates**（未持久化，仅标注）：
  - 「晨光阅读·新用户激活」—— 可作 Data/Experiment/Growth 角度 story，但 Attribution 缺口大，须先补实验事实（placeholder 见 Q02.4.1）。
  - 「校园 AI 写作助手」—— 可作 AI 角度 story，但缺上线用户量/eval/留存数据（简历已明示未提供），暂不能作强 story。
- **Outcome Calibration**：none（无结果反馈，无可校准事件）。

> 明确声明：以上均为首场初始值，**不存在、也不得虚构任何跨场改善趋势**。

---

# 16. Next Interview Actions

## P0 — 下一场前必须修

1. **对象**：晨光阅读新用户激活项目的归因与数据口径。
   - 动作：补齐上线周历史同期 baseline、是否有并行活动、完成任务 vs 未完成任务分群 D1/D7/付费对比；写出“为什么 D1 涨 4 点不能直接归因到新手任务”。
   - 完成标准：能口述该项目“哪些结论有实验/对照支撑、哪些只是相关”，并回答“重做如何设计 A/B”。
   - 复测问题：D1 涨 4 点能证明新手任务有效吗？为什么？

2. **对象**：AI 首次生成成功率机制。
   - 动作：为“校园 AI 写作助手”补机制拆解：成功口径、失败率/重试率、输入质量→意图→模型→输出质量链条、一个 eval 指标、一个 failure recovery 设计。
   - 完成标准：能说出“首次生成成功”的可测口径 + 至少一个 recovery 设计 + 一个 eval 指标。
   - 复测问题：你说的“成功”怎么定义？失败后怎么 recovery？

3. **对象**：Growth retention driver。
   - 动作：针对 AI 创作产品写 D7 留存诊断框架（segment × 流失节点 × 回访动机假设 × 对应实验 + guardrail）。
   - 完成标准：能从“用户为什么回来”的机制角度回答，而非列 Push/签到/积分。
   - 复测问题：用户为什么要回来？retention driver 是什么？

## P1 — 建议修

1. **对象**：Ownership 表达。
   - 动作：为每个项目准备“我个人的关键决策 + 判断依据 + 取舍 + 结果”，把“我们/老板/资源有限”替换为可证的个人动作。
   - 完成标准：能说出每个项目至少 1 个个人关键决策及其取舍。
   - 复测问题：你个人做的关键决策是什么？

2. **对象**：优先级判断逻辑。
   - 动作：把“老板关注/资源有限”替换为“问题规模 × 可影响性 × 成本”的判断标准。
   - 完成标准：能解释“为什么做 A 不做 B”的决策标准。
   - 复测问题：为什么做这个而不是别的？

## P2 — 长期积累

1. **对象**：AI 产品机制积累（eval、failure taxonomy、HITL、context/memory、cost-latency-quality 权衡）。
   - 动作：研读 1–2 个 AIGC 产品的生成质量评估/失败恢复案例，形成自己的机制 checklist。
   - 完成标准：能独立拆解任意一个 AI 写作/创作产品的“意图→生成→评估→恢复→再生成”链条。
   - 复测问题：换更好的模型就能提升首次成功率吗？代价是什么？
