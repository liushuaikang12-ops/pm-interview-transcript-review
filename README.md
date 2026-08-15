# PM Interview Transcript Review

> 面向 Product Manager、AI PM、Growth PM、Strategy PM 的跨 Agent 面试复盘 Skill。把录音、视频或 Transcript 转换为可追溯的问答树、能力诊断、回答改写、Shadow JD 和下一轮训练计划，而不是一份会议纪要。

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-open%20standard-6f42c1)](https://agentskills.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 你最终会得到什么

一次完整复盘默认产出三层结果：

1. **回看层**：面试实录、全部问题、追问关系和面试结构。
2. **诊断层**：能力映射、关键回答评分、证据账本、根因、短板卡和面试官信号。
3. **行动层**：Better Answer、Answer Playbook、Shadow JD、跨场趋势和下一轮 P0/P1/P2 训练计划。

它不是普通 Transcript Summary，也不会只给“回答不够结构化”这类空泛建议。每条重要判断必须绑定时间戳、Q&A ID 或原文片段；推断必须标记为推断。

## 适用于哪些 Agent

本仓库遵循 [Agent Skills 开放标准](https://agentskills.io/specification)：技能是一个包含 `SKILL.md`、脚本、参考资料和模板的目录。

- **原生安装**：Codex、Claude Code、Cursor、Gemini CLI、OpenCode、GitHub Copilot / VS Code、Hermes Agent，以及其他支持 Agent Skills 的客户端。
- **通用降级**：如果某个 Agent 尚不支持 Skills 自动发现，只要它能读取文件，就让它读取本仓库的 `SKILL.md` 并按其中流程执行；此时不能保证自动触发，但复盘方法和输出契约仍可使用。

> “任何 Agent 可安装”指格式和运行流程不绑定单一厂商；不同客户端的技能发现目录仍然不同，因此本仓库提供统一安装器。

## 安装

### 方式一：统一安装器（推荐）

先克隆仓库：

```bash
git clone https://github.com/liushuaikang12-ops/pm-interview-transcript-review.git
cd pm-interview-transcript-review
```

安装到通用 Agent Skills 用户目录：

```bash
python scripts/install_skill.py --agent universal --scope user
```

安装到指定 Agent：

```bash
python scripts/install_skill.py --agent codex --scope user
python scripts/install_skill.py --agent claude --scope user
python scripts/install_skill.py --agent cursor --scope user
python scripts/install_skill.py --agent gemini --scope user
python scripts/install_skill.py --agent opencode --scope user
python scripts/install_skill.py --agent hermes --scope user
```

安装到当前项目而非全局用户目录：

```bash
python scripts/install_skill.py --agent universal --scope project --project-dir /path/to/project
```

安装到任意自定义 Skills 根目录：

```bash
python scripts/install_skill.py --target /path/to/your-agent/skills
```

目标位置已经存在时，安装器默认拒绝覆盖；确认更新时添加 `--force`。先查看但不写入：

```bash
python scripts/install_skill.py --agent universal --scope user --dry-run
```

### 方式二：从干净 Clone 手动复制

仅从**干净的 Git clone** 中复制发布包内容到客户端 Skills 根目录；不要复制混有真实 Transcript、`.env` 或其他私有资料的工作目录。优先使用上面的安装器：它按显式 23 文件白名单复制，不会带走未列入发布包的额外文件。

最终结构至少为：

```text
<skills-root>/
└── pm-interview-transcript-review/
    ├── SKILL.md
    ├── README.md
    ├── LICENSE
    ├── scripts/
    ├── templates/
    ├── references/
    └── examples/
```

常见发现路径：

| Client | 用户级 | 项目级 |
|---|---|---|
| Codex / 通用 Agent Skills / VS Code | `~/.agents/skills/` | `.agents/skills/` |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Cursor | `~/.cursor/skills/` 或 `~/.agents/skills/` | `.cursor/skills/` 或 `.agents/skills/` |
| Gemini CLI | `~/.gemini/skills/` 或 `~/.agents/skills/` | `.gemini/skills/` 或 `.agents/skills/` |
| OpenCode | `~/.config/opencode/skills/` 或 `~/.agents/skills/` | `.opencode/skills/` 或 `.agents/skills/` |
| Hermes Agent | `$HERMES_HOME/skills/`（未设置时通常为 `~/.hermes/skills/`） | 使用用户级安装或客户端自定义目录 |

安装后新开一个 Agent 会话；部分客户端也支持自动检测变更。

## 如何调用

自然语言即可，不依赖某个产品的 Slash Command：

> 使用 pm-interview-transcript-review 完整复盘这场面试。恢复所有追问关系，评价关键回答，生成 Shadow JD 和下一轮训练计划。所有结论必须引用证据，不得编造我没有说过的经历或指标。

也可以指定模式：

> 只做 Question Extraction，输出完整问题清单和 Follow-up Trees。

> 对比最近三场复盘，找出重复短板并生成下一轮 Drill Plan。

不同 Agent 的显式调用语法可能是 `/skill-name`、`$skill-name`、技能选择器或 `@` 引用；自然语言触发最通用。

## 支持的输入

输入可以单独提供，也可以组合提供：

1. 面试录音：`.mp3`、`.m4a`、`.wav`。
2. 面试视频。
3. ASR 结果、`.md`、`.txt`、`.vtt`、`.srt` Transcript。
4. Job Description。
5. 候选人简历。
6. 项目资料或数据口径说明。
7. 过去的面试复盘与结构化 `record.json`。
8. Recruiter / HR / Hiring Manager feedback。
9. 面试结果：advanced、rejected、offer、withdrew、unknown。

**Transcript 是回答评价的事实源。** 没有 Transcript 时可以分析 JD、简历和岗位要求，但不能声称评估过候选人的真实回答。

## 默认交付物

完整模式通常生成以下文件：

```text
~/.pm-interview-review-os/
├── config.json
├── interviews/
│   └── <interview_id>/
│       ├── source-manifest.json        # 输入来源、完整性、时间戳与可信用途
│       ├── transcript.normalized.md    # 清洗后实录，不覆盖原文件
│       ├── review.md                   # 面向人的完整 16 章复盘
│       ├── record.json                 # 面向机器的单场事实记录
│       ├── answer-playbook.md          # 可选：问题 + 建议答案备考版
│       └── review.html                 # 可选：HTML 阅读版
├── aggregates/
│   ├── question-bank.json              # 跨场题库
│   ├── competency-matrix.json          # 能力矩阵与趋势
│   ├── anti-patterns.json              # 反模式统计
│   ├── project-probe-depth.json        # 项目深挖层级
│   ├── story-bank.json                 # 可复用故事索引
│   └── calibration.json                # 预测与真实结果校准
└── calibration-events.jsonl            # append-only 结果事件
```

工作区可通过环境变量覆盖：

```bash
export PM_INTERVIEW_REVIEW_HOME=/path/to/private/workspace
```

或每次运行脚本时传入 `--root`。面试材料默认仅保存在本地，不会因为安装 Skill 而自动上传。

## Full Review 的内容与 16 章结构

### 可选前置：Question Transcript

在诊断报告之前放一份可快速回看的问答实录：

```text
Q01 面试官原始问题
├── Q01.1 第一层追问
│   └── Q01.1.1 证据挑战
└── Q01.2 替代方案 / Trade-off 追问

面试官：……
候选人：……
```

它保留问题原文、追问和候选人回复，并以时间戳或稳定段落定位。无法确认的专有名词标记为“录音转写不清”，不猜测补齐。

### 1. Executive Summary

回答三个最重要的问题：**本场最大优势是什么、最大风险是什么、下一层追问最可能在哪里击穿。**

包含：

- Overall Performance 与 Confidence；
- Strongest Areas、Biggest Risks；
- Likely Interviewer Concerns（推断）；
- Positive Signals 与 Uncertain Areas；
- 支撑总评的 Evidence anchors。

不输出没有依据的“通过率 80%”。

### 2. Interview Structure

还原整场面试的阶段、顺序和权重，例如自我介绍、项目深挖、Case、岗位专项、反问。每一阶段带时间范围或 Q&A anchor。

### 3. Complete Question Map

列出所有有效问题，而不只保留“重点题”：

| 字段 | 含义 |
|---|---|
| ID / Parent | `Q01`、`Q01.1` 等层级关系 |
| Surface Question | 面试官实际问法 |
| Answer Anchor | 候选人回答所在位置 |
| Underlying Intent | 考察意图，显式标记为推断 |
| Competency | 主要能力标签，最多 1–3 个 |
| Type | Root、Follow-up、Challenge、Administrative 等 |

报告会对账：原始抽取问题数、树节点数、流程问题数和 parent 不确定数。

### 4. Follow-up Trees

把围绕同一项目、证据链或 concern 的追问恢复为树，而不是按时间平铺。每棵树解释：

- 根问题在验证什么；
- 候选人的哪句话触发了下一问；
- 追问是在补证据、挑战因果、确认个人贡献，还是测试 Trade-off；
- 无法确定 parent 时为什么保持 `Uncertain`。

### 5. Competency Mapping

将问题和证据映射到 PM 能力矩阵：Problem Framing、User Insight、Strategy、Execution、Data、Experiment、Attribution、Ownership、Stakeholder、Reflection，以及 AI/Growth/Strategy 专项能力。

核心证据链：

```text
Problem → Evidence → Insight → Decision → Solution → Experiment
→ Metric → Attribution → Iteration → Reflection
```

### 6. Key Answer Reviews

只深评决定录用判断、被连续追问、明显失误或特别强的回答。每个重点回答使用固定结构：

1. Surface Question；
2. Underlying Intent（推断 + confidence）；
3. Candidate Answer — Clean Version；
4. Raw Evidence（必要时）；
5. 五维评分：Substance / Structure / Relevance / Credibility / Differentiation；
6. Weight profile、cap/penalty 与 Overall Score；
7. Gap Type：Capability / Communication / Evidence / Knowledge；
8. Root Cause；
9. Recommended Structure；
10. Suggested Answer；
11. Provenance Check：每条事实对应哪个 source anchor，哪些位置仍是 placeholder。

Suggested Answer 不允许凭空生成经历、动作、指标或用户洞察；缺失事实保留：

```text
[这里需要补充：数据口径 / 个人动作 / 实验结果 / 来源]
```

### 7. Evidence & Quotes

建立证据账本：Evidence ID、时间戳/Q&A anchor、Speaker、短原话、用途和证据等级。

- `F1 Transcript Fact`：Transcript 原话明确出现；
- `F2 Corroborated Fact`：Transcript 与简历/JD/项目材料一致；
- `I1 Inference`：从行为或上下文推断，必须给 confidence。

### 8. Shortcoming Cards

只输出最关键的 3–7 张短板卡，并按“录用影响 × 重复性 × 可修复性”排序。每张卡包含：

- Name；
- Severity 与 Frequency；
- Evidence；
- Root Cause；
- Interview Risk（推断）；
- Corrective Principle；
- Drill 与完成标准。

### 9. Anti-patterns

识别反复出现的坏习惯，例如结论后置、指标无口径、个人贡献不清、因果跳跃、机械 STAR、AI 概念化或 Growth 运营化。

有历史时展示本场、历史累计、最近 3 场、最近 5 场和 `Improving / Stable / Worsening`；样本不足时明确写 `Insufficient history`。

### 10. Project Probe Depth

按十层检查项目能被追问到哪里：

```text
What → Why → Evidence → Why this solution → Alternative
→ Metrics → Unexpected result → Root cause → Iteration → What differently
```

输出 `Current Probe Depth: x/10`、首个断点、已有孤立强证据和下一步需要补齐的证据。

### 11. Role-specific Review

根据岗位和问题动态启用：

- **AI PM**：User Intent、Model Capability/Limit、Context/Memory/Tool、Evaluation、AI UX、Latency-Cost-Quality、Failure Recovery、HITL、Feedback Loop；
- **Growth PM**：Segment、Trigger、Activation、First Value、Habit、Retention、Growth Loop、Attribution、Guardrail；
- **Strategy PM**：Business Model、Market/Competition、Resource Allocation、ROI、Trade-off 和执行闭环。

未命中专项时不会强行填充，而是写明 `Not activated`。

### 12. Interviewer Signals

基于可观察行为区分 `Positive Signal / Neutral / Concern / Strong Concern`，同时给出 alternative explanation 和 confidence。

它只是一种行为信号推断，不等于真实评分或录用结论；连续追问既可能是质疑，也可能是兴趣深挖。

### 13. Reverse Interview Intelligence

单独还原候选人反问与面试官回答，并提取：Team、Product、KPI、Current Problem、Candidate Role、Expectation、Work Style、Hiring Signal。

原话是 Fact；归纳和判断是 Inference。

### 14. Shadow JD

把官方 JD 与面试证据合并，反推出团队真正需要的人：

| Official JD | Interview Evidence | Shadow JD（推断） | Confidence |
|---|---|---|---|

Shadow JD 不复述职位描述，而是回答：实际工作重心是什么、团队当前卡点是什么、最在意哪些能力、候选人入职后可能承担什么角色。

### 15. Cross-interview Update

更新跨场资产：Question Bank、Competency Matrix、Anti-pattern、Project Probe Depth、Story Bank 和 Outcome Calibration。

单场 `record.json` 是事实源；聚合结果从 records 重建，避免手工累计漂移。真实结果后补时保留原预测，不为了迎合结果倒改历史诊断。

### 16. Next Interview Actions

只给少量、可验收的行动：

- `P0`：下一场前必须修，通常 1–3 项；
- `P1`：建议修，通常 1–3 项；
- `P2`：长期积累，通常 1–2 项。

每项都包含训练对象、具体动作、完成标准和复测问题，不使用“加强 AI 理解”之类无法执行的建议。

## Answer Playbook：问题 + 回答建议版

当目标从“诊断本场”切换为“准备下一场”时，可以额外生成 `answer-playbook.md`：

```text
问题原文
├── 追问 1
├── 追问 2
└── 回答建议
    ├── Recommended Structure
    ├── Suggested Answer
    └── Missing Facts / Placeholders
```

这个版本可以不展示候选人的实际回答，但仍必须执行 Atomic Claim Audit。候选人反问与面试官回答保留原文，不改写成建议答案。

## 六种运行模式

| Mode | 主要产出 | 适用场景 |
|---|---|---|
| A — Full Review | Question Transcript + 16 章 + 结构化记录 | 默认；完整复盘 |
| B — Question Extraction | Complete Question Map、Follow-up Trees、Intent、Competency | 只整理面经和追问结构 |
| C — Answer Critique | 关键回答评分、Root Cause、Better Answer、Shortcoming Cards | 集中修回答 |
| D — Interviewer Intelligence | Interviewer Signals、Reverse Interview、Shadow JD | 判断岗位真实需求 |
| E — Cross Interview Review | 题库、能力矩阵、反模式、项目深度、Outcome Calibration | 对比多场趋势 |
| F — Next Round Prep | P0/P1/P2、Answer Playbook、项目/Story Drill、问题预测 | 准备下一轮 |

模式只裁剪输出，不降低 Evidence 标准。用户没有指定模式时采用 Mode A。

## 可选脚本

Skill 本体是 Agent 指令，不依赖 Python；以下能力需要本地脚本。

### 本地媒体转写

依赖 `ffmpeg`、`ffprobe`、`faster-whisper`：

```bash
python scripts/transcribe_media.py interview.mp4 \
  --output-dir transcript-output \
  --language zh \
  --model small
```

输出 TXT、Markdown、VTT、segments JSON 和 metadata。脚本不做 speaker diarization，初始标签统一为 `Unknown Speaker`。

### 历史数据库

```bash
python scripts/interview_os.py init
python scripts/interview_os.py status
python scripts/interview_os.py save --record record.json --review review.md
python scripts/interview_os.py rebuild
python scripts/interview_os.py outcome --id <interview_id> --status advanced
```

可使用 `PM_INTERVIEW_REVIEW_HOME` 或 `--root /path/to/workspace` 指定私有工作区。

### Markdown 转 HTML

依赖 Python `markdown` 包：

```bash
python scripts/render_review.py review.md --output review.html
```

## 证据与防幻觉边界

1. Transcript 是候选人“本场说过什么”的事实源；简历和 JD 不能冒充 Transcript。
2. 每条重大 finding 必须绑定时间戳、Q&A ID 或稳定段落 anchor。
3. Fact、Corroborated Fact 与 Inference 必须分层。
4. Better Answer 中每个过去动作、数字、结果、因果结论和个人贡献都要通过 provenance check。
5. 缺失事实必须删除或写 placeholder，不能在无证据主张后补一个括号来“洗白”。
6. 单场失误只能称为本场信号；至少跨两场重复且有独立证据，才升级为长期 weakness。
7. 不根据面试氛围、追问次数或单一结果生成伪精确的录用概率。

## 验证

安装开发依赖后运行：

```bash
python -m pip install pyyaml jsonschema markdown
python scripts/validate_skill.py
```

测试覆盖：

- Agent Skills frontmatter 和目录契约；
- Python 脚本语法；
- JSON Schema 与单场 record 语义校验；
- 至少五层追问、嵌套证据挑战与问题对账；
- 五维评分、Evidence、Shortcoming Cards、Shadow JD；
- 16 章输出；
- Atomic Claim / negative-entailment 防编造回归；
- 跨平台安装目标与自定义目录安装。

完整模拟输入、Markdown/HTML 输出和测试记录位于 `examples/` 与 `references/test-report.md`。

## 仓库结构

```text
pm-interview-transcript-review/
├── SKILL.md                              # Agent 路由、工作流、输出与证据规则
├── README.md                             # 安装、使用和交付结构
├── LICENSE
├── scripts/
│   ├── install_skill.py                  # 跨 Agent 安装器
│   ├── interview_os.py                   # 本地历史与确定性聚合
│   ├── transcribe_media.py               # 本地 ASR
│   ├── render_review.py                  # Markdown → HTML
│   └── validate_skill.py                 # 验收测试
├── examples/                             # 模拟输入、Markdown/HTML 输出与回归样例
├── references/                           # 评分、能力 taxonomy、历史、媒体与测试
└── templates/
    ├── full-review.md                    # 16 章报告模板
    └── interview-record.schema.json      # 单场机器记录契约
```

## License

MIT。见 [LICENSE](LICENSE)。
