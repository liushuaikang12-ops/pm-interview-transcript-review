# pm-interview-transcript-review

本地 Hermes Skill：面向 Product Manager / AI PM / Growth PM / Strategy PM 的 **Interview Review OS**。

## 设计目标

不是会议纪要，而是把真实录音、视频或 Transcript 转换为：Follow-up Tree、Interviewer Intent、Competency Mapping、五维评分、Root Cause、Evidence-grounded Better Answer、Shortcoming Cards、Anti-pattern 趋势、Project Probe Depth、Reverse Interview Intelligence、Shadow JD 与下一场 Drill。

## 安装位置

`$HERMES_HOME/skills/productivity/pm-interview-transcript-review/`

调用 Skill 自带脚本时优先使用 Hermes 注入的 `${HERMES_SKILL_DIR}`，不要硬编码本机路径。

运行数据不写进 Skill 包，而写入：

`$HERMES_HOME/interview-review-os/`

这样 Skill 更新与面试历史解耦；每场 `record.json` 是事实源，aggregates 可重建。

## 使用

自然语言：

> 使用 pm-interview-transcript-review 完整复盘这场面试。重点恢复面试官追问树，分析我的回答证据链和 AI 产品能力，不要只做问题摘要。

Slash command：

```text
/pm-interview-transcript-review 完整复盘这个 transcript，并结合 JD 和简历更新跨场题库。
```

支持模式：Full Review（默认）、Question Extraction、Answer Critique、Interviewer Intelligence、Cross Interview Review、Next Round Prep。

## Full Review 输出结构（16 章）

1. **Executive Summary** — 执行摘要：最大优势、最大风险、最可能在下一轮追问被拆穿的断点
2. **Interview Structure** — 面试阶段划分与各阶段权重
3. **Complete Question Map** — 全部问题 + 追问 + 表面问题 + 考察意图 + 能力维度
4. **Follow-up Trees** — 追问树（把追问归到根问题）
5. **Competency Mapping** — 能力 → 证据 → 信号强度 → 置信度
6. **Key Answer Reviews** — 关键回答五维评分（Substance/Structure/Relevance/Credibility/Differentiation）+ 根因
7. **Evidence & Quotes** — 证据与原文引用（Fact/Inference 分层）
8. **Shortcoming Cards** — 短板卡（按严重度排序）
9. **Anti-patterns** — 反模式趋势（反复出现的坏习惯）
10. **Project Probe Depth** — 项目深挖层次（面试官挖到第几层）
11. **AI PM / Growth PM Special Review** — 岗位专项诊断（动态启用）
12. **Interviewer Signals** — 面试官信号（建设性深入 vs 打发）
13. **Reverse Interview Intelligence** — 反问环节的情报提取
14. **Shadow JD** — 反推岗位真实画像与能力权重
15. **Cross-interview Update** — 跨场更新（多场面试的题库累积）
16. **Next Interview Actions** — 下一场行动（P0/P1/P2 优先级）

## 实录与回答建议

- **实录前置**：复盘最前面可加「面试官问题原文 + 追问 + 回复」实录，问题原文用引用格式、连续编号，追问与回复分别标注「面试官」「候选人」。
- **回答建议版（Answer Playbook）**：用户要求生成备考文档时，把「候选人实际回答」替换为「回答建议」（Better Answer），文档主体变为「问题原文 + 追问 + 回答建议」，实际回答不展示。回答建议只使用已有事实，缺口用 `[这里需要补充：…]` 占位，假设题/设计题标注「建议 / 假设」。
- **反问保留原文**：候选人反问部分（反问 + 面试官回答）保留原文，不做「建议版」改写。

## 本地媒体转写

本机具备 ffmpeg 与 faster-whisper 时：

```bash
python scripts/transcribe_media.py interview.mp4 --output-dir transcript-output --language zh --model small
```

脚本输出 TXT、Markdown、VTT、segments JSON 和 metadata。它不做 speaker diarization，初始标签一律为 `Unknown Speaker`，后续必须基于证据识别。

## 历史数据库

```bash
python scripts/interview_os.py init
python scripts/interview_os.py status
python scripts/interview_os.py save --record record.json --review review.md
python scripts/interview_os.py rebuild
python scripts/interview_os.py outcome --id <interview_id> --status advanced
```

## 验证

```bash
python scripts/validate_skill.py
```

模拟测试资料位于 `references/examples/`，覆盖：自我介绍、PM 项目、至少五次连续追问、数据异常、AI 产品、Growth、反问和明显失误。

详细验收记录见 `references/test-report.md`；完整 Markdown/HTML 样例与 Atomic Claim 回归样例位于 `references/examples/`。

## Evidence 与隐私

- Transcript 是事实源；推断必须显式标记。
- Better Answer 不得编造；缺失事实使用 `[这里需要补充：XXX]`。
- 默认 local-only，不自动上传录音、简历或反馈。
- Transcript 与逐场历史不写入 Mem0/MEMORY。

## 结构说明

- `SKILL.md`：路由、模式、主流程、Output Contract、证据与防幻觉规则。
- `references/`：评分、PM taxonomy、历史校准、媒体链路、外部设计研究、模拟测试。
- `templates/`：Full Review 与 JSON record contract。
- `scripts/`：本地 ASR、历史聚合、HTML 渲染、验收测试。

本项目只吸收外部项目的设计思想，不复制其实现文本。来源与差异见 `references/external-design-notes.md`。
