# Acceptance Test Report

Test dates: 2026-08-14 (behavior baseline), 2026-08-15 (Agent Skills portability migration)

## 1. Portability Migration Scope

本轮目标不是只改 README，而是把 Skill 从 Hermes-specific package 改为符合 Agent Skills 开放标准的跨客户端包：

- `SKILL.md` frontmatter 只保留标准字段：`name`、`description`、`license`、`compatibility`、字符串 metadata。
- 主流程不再依赖 `HERMES_HOME`、`HERMES_SKILL_DIR`、`skill_view` 或某个 Agent 的专属工具名。
- 历史工作区改为 `${PM_INTERVIEW_REVIEW_HOME}`，默认 `~/.pm-interview-review-os/`。
- 新增零第三方依赖安装器 `scripts/install_skill.py`。
- 安装器只复制显式的 23 文件发布白名单，不复制仓库中的任何额外文件。
- README 明确说明默认文件产物、16 章结构、Answer Playbook、六种模式和证据边界。
- Role-specific Review 统一覆盖 AI PM、Growth PM、Strategy PM。

## 2. Portable Static / Fixture Contract

Command:

```bash
python scripts/validate_skill.py
```

Final result:

```json
{
  "status": "PASS",
  "standard": "Agent Skills",
  "required_files": 20,
  "package_files": 23,
  "questions": 17,
  "q02_followups": 10,
  "shortcoming_cards": 3,
  "installer_smoke_test": true,
  "portable_workspace": true,
  "test_run_output_present": true
}
```

Validated:

- UTF-8 `SKILL.md` frontmatter at byte 0；
- negative fixtures reject double-hyphen names, nested metadata values, UTF-8 BOM, missing template chapters and reordered README chapters；
- Agent Skills standard fields and metadata string mapping；
- directory name equals frontmatter `name`；
- no vendor-specific runtime dependency in `SKILL.md`；
- README contains install paths, artifact-level output contract and all 16 chapters；
- required files and Python syntax；
- JSON Schema and semantic record validation；
- unique Q IDs, valid parents and nested Follow-up Trees；
- five-dimensional scores, Evidence, 3–7 Shortcoming Cards and Shadow JD grounding；
- 16-chapter sample output and Atomic Claim regression；
- actual installation output exactly matches the 23-file package allowlist；
- regression fixture confirms that an untracked `.env` and private interview transcript are not copied；
- `PM_INTERVIEW_REVIEW_HOME` override is honored。

## 3. Installer Matrix

User-scope dry runs passed for:

| Agent target | Resolved directory on the test machine |
|---|---|
| universal / Codex / Copilot / VS Code | `C:\Users\24425\.agents\skills\pm-interview-transcript-review` |
| Claude Code | `C:\Users\24425\.claude\skills\pm-interview-transcript-review` |
| Cursor | `C:\Users\24425\.cursor\skills\pm-interview-transcript-review` |
| Gemini CLI | `C:\Users\24425\.gemini\skills\pm-interview-transcript-review` |
| OpenCode | `C:\Users\24425\.config\opencode\skills\pm-interview-transcript-review` |
| Hermes Agent | `C:\hermes\skills\pm-interview-transcript-review` |

Project-scope dry runs passed for `.agents/skills`、`.claude/skills`、`.cursor/skills`、`.gemini/skills` 和 `.opencode/skills`。`--target` was also exercised by the installer smoke test in a temporary directory.

The installer refuses to overwrite an existing target unless `--force` is supplied, refuses symbolic-link, Windows junction/reparse-point and non-directory targets, rejects recursive installation inside its own source repository even when an ancestor junction resolves back into the source, and copies only its explicit package allowlist. Extra files—including `.env` files and private transcripts—are excluded by construction rather than by a fragile ignore list.

## 4. Real Client Discovery Tests

Three isolated Git repositories were created. The Skill was installed into each client's documented project directory. The prompt asked for two fields that exist in the loaded Skill but were not supplied in the installation command:

```text
Next Interview Actions | PM_INTERVIEW_REVIEW_HOME
```

### Codex CLI 0.147.0

- Install location: `.agents/skills/pm-interview-transcript-review/`
- Invocation: explicit `$pm-interview-transcript-review`
- Result: **PASS**
- Returned exactly: `Next Interview Actions | PM_INTERVIEW_REVIEW_HOME`

### Claude Code 2.1.233

- Install location: `.claude/skills/pm-interview-transcript-review/`
- Result: **PASS**
- Returned exactly: `Next Interview Actions | PM_INTERVIEW_REVIEW_HOME`
- Environment note: Claude Code emitted unrelated `unrecognized_model` warnings for the locally configured session-title/helper models, but the main Skill result was correct.

### Gemini CLI 0.54.0

- Install location: `.gemini/skills/pm-interview-transcript-review/`
- File installation and documented target resolution: **PASS**
- End-to-end model invocation: **BLOCKED BY CLIENT AUTH**, not by the Skill
- The installed CLI returned `IneligibleTierError / UNSUPPORTED_CLIENT` for the user's legacy Gemini Code Assist individual tier before Agent execution. Therefore this report does **not** claim a Gemini model-level activation pass.
- Running `gemini skills list` without trust correctly skipped project agents; retrying with `--skip-trust` still hit the same authentication blocker.

This distinction matters: a copied file is not evidence of runtime activation. Only Codex and Claude are counted as end-to-end client passes in this environment.

## 5. Local Workspace Lifecycle

An isolated temporary workspace was exercised through the real script:

```bash
python scripts/interview_os.py --root <temp> init
python scripts/interview_os.py --root <temp> status
```

Result: **PASS**.

Created:

```text
aggregates/
calibration-events.jsonl
config.json
interviews/
```

Initial status correctly reported zero interviews, questions, competencies, anti-patterns, projects, stories and outcomes.

## 6. Full Review Behavior Baseline

The fictional fixture covers:

- self-introduction；
- one PM project；
- 10 follow-up nodes under one root, including nested `Q02.2.1`、`Q02.4.1`、`Q02.5.1`；
- data anomaly and Attribution failure；
- AI Product and Growth questions；
- reverse interview；
- an obvious ownership mistake。

Artifacts:

- `examples/test-run-output.md`
- `examples/test-run-output.html`

Observed:

- all 16 chapters generated；
- Q02 follow-ups hierarchical rather than flat；
- important reviews showed dynamic weights, cap, Evidence and Root Cause；
- Shortcoming Cards prioritized；
- Shadow JD grounded in reverse-interview Evidence；
- first-session history marked `Insufficient history`；
- Chapter 11 uses `Role-specific Review`; Strategy was correctly marked `Not activated` for the fictional AI Growth role。

## 7. Atomic Claim Regression

The initial full-output test expanded resume evidence “做过用户访谈和原型” into the unsupported insight “用户常常不知道怎么描述需求”. A placeholder appended after that claim did not make the unsupported claim grounded.

Fixes retained in the portable version:

1. mandatory Atomic Claim Audit；
2. action evidence does not prove the action's result or insight；
3. hypothetical proposals must be framed as proposal/hypothesis；
4. unsupported claims must be deleted or wholly replaced by placeholders；
5. negative-entailment check；
6. fixture-level regression assertion。

Artifact: `examples/atomic-claim-regression.md`

Result: **PASS**. “用户不会描述需求” appears only as a labeled hypothesis, not as a fabricated past finding.

## 8. History / Outcome Calibration Baseline

A temporary workspace was initialized, the simulated record was validated and saved, and a rejected outcome was appended.

Deterministic result:

- interviews: 1
- question-bank items: 16 interviewer questions
- competencies: 3
- anti-patterns: 4
- projects: 1
- stories: 1
- outcomes: 1
- calibration events: 1
- original verdict preserved: true

The script supports distinct `--feedback` text and `--feedback-file` inputs with mutual exclusion.

## 9. Media Pipeline Baseline

A 20.102-second Chinese synthetic WAV was previously processed through the actual local pipeline:

```text
WAV → ffmpeg 16k mono WAV → faster-whisper
→ TXT / Markdown / VTT / segments JSON / metadata
```

Result:

- detected language: zh
- segment count: 3
- speaker labels: 3 × `Unknown Speaker`
- output files: 6
- timestamped output: present

The pipeline correctly did not invent speaker identity. It does not claim reliable acoustic diarization, and ASR errors remain possible.

## Final Acceptance

**PASS for Agent Skills format, deterministic scripts, installer, Codex discovery, Claude Code discovery, report structure and behavior regressions.**

**Gemini end-to-end activation remains unverified because the installed client was rejected by Google's account-tier authentication before Agent execution.** OpenCode and Cursor path compatibility is based on their documented discovery locations plus installer tests; those clients were not available for model-level execution in this environment.
