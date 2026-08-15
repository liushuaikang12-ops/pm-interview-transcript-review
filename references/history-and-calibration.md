# Cross-interview History & Outcome Calibration

## 1. Design Principle

单场记录是 source of truth；Question Bank、Competency Matrix、Anti-pattern、Probe Depth、Story Bank 都是可重建 projection。不要把计数散落在 Markdown 里手工维护。

默认 workspace（可通过 `PM_INTERVIEW_REVIEW_HOME` 覆盖）：

```text
~/.pm-interview-review-os/
├── config.json
├── interviews/
│   └── <interview_id>/
│       ├── source-manifest.json
│       ├── transcript.normalized.md
│       ├── review.md
│       └── record.json
├── aggregates/
│   ├── question-bank.json
│   ├── competency-matrix.json
│   ├── anti-patterns.json
│   ├── project-probe-depth.json
│   ├── story-bank.json
│   └── calibration.json
└── calibration-events.jsonl
```

原始大型媒体可留在原位置，manifest 保存路径与 hash（若用户允许）；不要无意义复制。路径不存在时标 source unavailable。

## 2. Interview Record

按 `templates/interview-record.schema.json` 保存。关键字段：

- interview metadata：company、role、date、round、mode
- source manifest 与 transcript completeness
- complete questions + parent_id
- key answer reviews + evidence anchors
- competencies
- anti-pattern counts + eligible answer count
- project probe depth
- story candidates
- interviewer/reverse intelligence（Fact/Inference 分开）
- Shadow JD evidence
- verdict + confidence + original prediction timestamp
- outcome（可后补）

不要存无来源的“Best Answer”。Suggested Answer 中 placeholder 必须原样保留。

## 3. Question Bank Update

标准化问题时保留原文与 canonical form：

- 原文不同但 intent 相同，可以共享 canonical question。
- Frequency 至少同时存 `interview_count` 与 `occurrence_count`，避免一场连问 5 次被误解成 5 家都高频。
- Companies 去重；Last Asked 用实际日期；未知日期不猜。
- Best Answer 指向 story/answer ID，不复制一份会漂移的文本。
- Current Score 优先用最近 3 次同类回答的 Evidence-weighted average；不足 3 次显示样本数。

## 4. Competency Matrix

每场只使用 decisive answers。每个 competency 保存：

- observations：interview_id、Q ID、score、confidence、evidence
- current：最近最多 3 场的加权均值
- trend：最近最多 3 场 vs 前最多 3 场
- sample_size

权重建议：High confidence=1.0，Medium=0.7，Low=0.4。两窗均至少 2 条观察且差值绝对值 ≥0.5，才判 `Improving/Worsening`；否则 `Stable`。历史不足写 `Insufficient history`。

## 5. Anti-pattern Trend

计数先归一化：

`incidence_rate = occurrence_count / eligible_answer_count`

eligible answer 指该反模式有机会出现的独立 Q&A 节点。无 eligible 数据时可显示 raw count，但不得与不同长度面试直接比较。

输出：

- 本场：count / eligible
- 历史累计：count / eligible
- 最近 3 场、最近 5 场 rate
- Trend

趋势规则：至少 3 场且存在可比基线。最近窗口相对前一窗口下降 ≥20%，且绝对下降 ≥0.10 → Improving；上升同阈值 → Worsening；否则 Stable。样本不足 → Insufficient history。

## 6. Project Probe Depth

按项目稳定 ID 聚合，不只按名称字符串。每场保存各层 Evidence status。聚合显示：

- 当前连续深度
- 历史最高“有证据深度”
- 最近一次断点
- 需要补证据的层

深度提升必须来自新的事实/训练结果，不是模型把同一材料重新解释得更乐观。

## 7. Story Bank

Story 类型：Leadership、Failure、Data、Growth、Conflict、AI、Experiment、Ownership、Trade-off。

每个 story 保存：

- `story_id/title/type`
- source interview/Q&A
- facts（带 source anchor）
- candidate contribution
- decision/trade-off
- metrics 与 evidence status
- usable_for_questions
- current score
- missing facts/placeholders
- last rehearsed / last used

同一项目可生成多个角度，但不能把缺失事实补成故事。

## 8. Outcome Calibration

Outcome 枚举：`advanced / rejected / offer / withdrew / unknown`，可附 recruiter/hiring manager 原文和日期。

收到 outcome 后：

1. 保留原 verdict、score、confidence，不回写历史预测。
2. append calibration event：prediction、actual outcome、feedback evidence。
3. 产生 `prediction_error_hypotheses`，每条标 Inference。
4. 检查是否系统性高估表达、低估 role fit、低估某 competency/concern。
5. 只有累计多场且方向一致，才调整评分权重；单一 outcome 不足以证明模型错在某一项。

禁止从 rejected 反推“本场所有回答都差”，也禁止从 advanced 反推“所有 concern 都不重要”。录用受 HC、竞争者、流程等不可见因素影响。

## 9. Commands

```bash
# 初始化与查看
python scripts/interview_os.py init
python scripts/interview_os.py status

# 校验并保存一场（record 是事实源）
python scripts/interview_os.py save --record record.json --review review.md

# 重建所有 aggregates
python scripts/interview_os.py rebuild

# 后补结果；feedback 与 feedback-file 二选一，均可省略
python scripts/interview_os.py outcome --id <interview_id> --status rejected --feedback "岗位匹配不足"
python scripts/interview_os.py outcome --id <interview_id> --status rejected --feedback-file feedback.txt
```

脚本只做文件与聚合的确定性工作，不替代 LLM 的语义判断。

## 10. Privacy / Deletion

- 本地优先；不自动上传媒体、简历、Transcript、feedback。
- 不把逐场内容写进 Agent 的通用用户画像或长期个人记忆。
- 删除一场：删除对应 interview directory 后运行 rebuild；报告聚合变化。
- Outcome feedback 可能包含第三方个人信息；只保留复盘所需最小内容。
- Workspace 备份与加密由用户自行选择；Skill 不宣称默认加密。