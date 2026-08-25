# External Design Research & Decisions

研究日期：2026-08-14。只吸收设计思想；本 Skill 的文本、schema 与脚本为独立实现。

## 1. CatNum — interview-transcript-review

用户给出的 `CatNum/Fork-skills` 当前为 404，不能断言只是改名。可验证的公开来源是：

- Repo: https://github.com/CatNum/personal-skills
- 固定提交: https://github.com/CatNum/personal-skills/tree/49320ede07c9e71b541be1641da2a863f0e17ed9
- Skill: `skills/interview-transcript-review/SKILL.md`
- Markdown/HTML templates: `skills/interview-transcript-review/assets/review-template.md` / `.html`
- Trigger evals: `skills/interview-transcript-review/evals/trigger-eval.json`
- Design doc: `docs/superpowers/specs/2026-06-15-interview-transcript-review-design.md`

### 吸收

- Transcript、JD、resume aware 的单场骨架。
- 按问题分析：意图、回答评价、改进与面试官/公司视角。
- Markdown + HTML 双输出。
- `evals` 作为行为契约，而不只做文件存在测试；公开 `trigger-eval.json` 含 13 条 prompt-only eval，覆盖正/负触发、清洗边界、必备字段和输出结构。
- 该 Skill 的公开实现只有 `SKILL.md`、两个 assets 模板和 eval 文件，没有 `scripts/`、`references/` 或独立评分程序；因此不能把它描述成确定性分析引擎。

### 不照搬 / 扩展

- 本 OS 把 Follow-up Tree、PM Evidence Chain、AI/Growth 专项、跨场数据库、Outcome Calibration 提升为一级架构。
- HTML 只是 view，不是事实层；所有长期数据写结构化 record。
- JD/简历只能补充 provenance，不能伪装成 Candidate 在面试时说过。

## 2. noamseg/interview-coach-skill

- Repo: https://github.com/noamseg/interview-coach-skill
- 固定提交: https://github.com/noamseg/interview-coach-skill/tree/634a8dd8689e0420c21e5f0c8ae3cfa9e1a7ab7e
- Detailed rubrics: `references/rubrics-detailed.md`
- Analyze workflow: `references/commands/analyze.md`
- Calibration engine: `references/calibration-engine.md`
- State schema: `references/coaching-state-schema.md`
- Progress workflow: `references/commands/progress.md`

### 吸收

- 原项目按 1–5 分给出五维文字锚点：Substance、Structure、Relevance、Credibility、Differentiation。
- Root Cause 不停在低分；识别表层症状下的系统性原因。
- Story Bank、Weakness Tracking、Drill、Cross-session Progress、Outcome Calibration。
- Calibration 需要样本门槛：公开设计中 outcome 少于 3 时保持 uncalibrated，完整趋势也需要更多 scored sessions。

### 不照搬 / 扩展

- 原项目主要是 Markdown 协议和单一 coaching state，不是确定性评分引擎；本 OS 新增 JSON schema、原子写入、从单场 records 重建 aggregates。
- 五维分改为 1–10，并按问题类型动态权重；加入 Relevance/Credibility caps，避免漂亮表达掩盖空内容。
- 单场多次出现可以生成 High Shortcoming，但只有跨场独立证据才升级为长期 weakness。

## 3. raphaotten/claude-interview-coach

- Repo: https://github.com/raphaotten/claude-interview-coach
- 固定提交: https://github.com/raphaotten/claude-interview-coach/tree/6cad936fa9eb353272a5fa6fba4f32255e7f05d6
- Debrief skill: `.claude/skills/debrief/SKILL.md`
- Mock/history update workflow: `framework/mock-interview.md`
- Interview summary template: `framework/templates/interview-summary.md`

### 吸收

- Anti-pattern 采用事件记录，而不是印象标签。
- 每场 session log → summary → count / last seen / trend 的更新链。
- 将 credibility/trust 与普通表达分开；跟踪 coached answers 和 pressure points。

### 证据边界

公开仓库引用了 `coaching/anti-pattern-tracker.md`，但该运行时文件被 gitignore，完整真实模板不可验证。因此本 OS 只吸收公开可证的接口思想，自行定义 schema 与趋势算法。

### 不照搬 / 扩展

- 按 eligible answers 归一化 incidence rate，避免长面试天然出现更多问题。
- Trend 有最小样本与绝对/相对阈值；不足直接写 Insufficient history。
- 区分“本场信号”和“跨场长期 anti-pattern”。

## 4. Composio Community — Meeting Insights Analyzer

- Repo: https://github.com/composio-community/awesome-codex-skills
- Skill: https://github.com/composio-community/awesome-codex-skills/tree/master/meeting-insights-analyzer
- Core file: `meeting-insights-analyzer/SKILL.md`

定位：这是 `composio-community` 的技能集合，不是 Composio 核心 SDK 内的分析引擎。公开目录只有 Skill 指令，没有确定性分析代码或测试。

### 吸收

- Evidence-first：timestamp + quote + finding + actionable suggestion。
- 分析 speaking ratio、filler、interrupt、question/statement、回避冲突等表达行为。
- 不只给数字，要解释 pattern、影响与 practice plan。

### 不照搬 / 扩展

- 指标必须声明分母和可计算条件；普通 VTT 无重叠轨道时不能可靠判断 interrupt。
- PM 面试的核心不是一般沟通风格，而是 Evidence/Insight/Decision/Experiment/Attribution 链。
- 每条重大评价统一为 `Finding → Frequency → Evidence → Root Cause → Why it matters → Better approach`。

## 5. jftuga/transcript-critic

- Repo: https://github.com/jftuga/transcript-critic
- Main workflow: `transcribe.sh`
- Analysis prompt: `ANALYSIS_PROMPT.md`
- Skill instructions: `SKILL.md`

### 吸收

公开实现的核心链路是：已有 VTT 直接分析；本地/URL 媒体经 ffmpeg/yt-dlp 处理为音频，再由 whisper.cpp / whisper-cli 输出 TXT 与 WebVTT；分析严格基于 Transcript。

### 不照搬 / 扩展

- 本 OS 默认不下载 URL 媒体，避免来源与隐私复杂度。
- 本机实际有 ffmpeg 和 faster-whisper，因此实现 `scripts/transcribe_media.py`：输出 WAV、TXT、Markdown、VTT、segments JSON、metadata。
- faster-whisper 不自带 diarization；初始 speaker 必须是 Unknown，不能把 segment 当人名。

## 6. Codex Skill Specification

权威文档：https://developers.openai.com/codex/skills

### 落地决策

1. 安装到 Codex 当前支持的用户目录 `~/.agents/skills/pm-interview-transcript-review/`。
2. `SKILL.md` 保持主流程；大块 taxonomy、rubric、history contract 放 `references/`；输出契约放 `templates/`；确定性处理放 `scripts/`。
3. 使用 progressive disclosure：只在对应模式加载 reference。
4. `agents/openai.yaml` 提供 Codex UI 与调用元数据；开发验收样例保留在顶层 `examples/`，运行数据不写入 Skill 包。
5. Skill 是程序性知识包，不当作运行数据库；逐场数据放 `~/.pm-interview-review-os/`，避免 Skill 更新或重装覆盖历史。
6. Skill 提供 `agents/openai.yaml`，自动化通过当前用户的 `codex exec` 调用，不共享登录或 OpenAI API Key。

## 7. 本 OS 的新增核心

外部项目均未同时提供以下完整组合：

- PM 专用 Follow-up Tree + Probe Depth。
- F1 Transcript Fact / F2 Corroborated Fact / I1 Inference 三层证据账本。
- 问题类型动态五维权重与 cap。
- Better Answer 的逐句 provenance / placeholder 规则。
- AI PM 与 Growth PM mechanism test。
- Reverse Interview → Shadow JD。
- 单场 JSON source-of-truth → 可重建跨场 aggregates。
- Append-only Outcome Calibration。
- Windows/MSYS 路径兼容与本地可执行测试。
