# Acceptance Test Report

Test date: 2026-08-14

## Scope

The fixture covers self-introduction, one PM project, 10 follow-up nodes under one root (including nested Q02.2.1 / Q02.4.1 / Q02.5.1), data anomaly, Attribution failure, AI Product question, Growth question, reverse interview and an obvious ownership mistake.

## 1. Static / Fixture Contract

Command:

```bash
python scripts/validate_skill.py
```

Final result:

```json
{
  "status": "PASS",
  "required_files": 18,
  "questions": 17,
  "q02_followups": 10,
  "shortcoming_cards": 3,
  "test_run_output_present": true
}
```

Validated: frontmatter, required files, Python syntax, JSON schema, unique Q IDs, valid parents, five-dimensional scores, Evidence, 3–7 Shortcoming Cards, Shadow JD evidence, full 16-chapter output and nested Follow-up Tree.

## 2. Full Hermes Fresh-session Test

Invocation: `/pm-interview-transcript-review` in a fresh `hermes chat -q` process.

Session: `20260814_141432_bed5fb`

Artifact:

- `references/examples/test-run-output.md`
- `references/examples/test-run-output.html`

Observed:

- Skill triggered and loaded its Full Review template, scoring, PM taxonomy and history references.
- Generated all 16 chapters.
- Q02 follow-ups were hierarchical rather than flat.
- Important reviews showed dynamic weights, cap, Evidence and Root Cause.
- Five Shortcoming Cards were prioritized.
- Shadow JD used reverse-interview Evidence.
- First-session history was correctly marked `Insufficient history`.

## 3. Defect Found and Fixed

The initial full output expanded resume evidence “做过用户访谈和原型” into the unsupported insight “用户常常不知道怎么描述需求”. A placeholder appended after that claim did not make it grounded. This violated the no-fabrication contract even though the child session's self-check incorrectly reported zero fabrication.

Fixes applied:

1. Patched `SKILL.md` with mandatory Atomic Claim Audit and negative-entailment check.
2. Clarified that a source proving an action does not prove the action's result or insight.
3. Required hypothetical proposals to be explicitly framed as proposal/hypothesis.
4. Patched the sample output to replace the unsupported insight with a full placeholder.
5. Added a fixture-level regression assertion.

## 4. Atomic Claim Regression

Fresh Hermes session: `20260814_143332_e567e7`

Artifact: `references/examples/atomic-claim-regression.md`

Result: **PASS**.

The output explicitly states that “做过用户访谈” cannot entail a specific user insight. “用户不会描述需求” appears only as a clearly labeled hypothesis, and the missing real interview finding remains a placeholder. The regression includes an Atomic Claim table and negative-entailment check.

## 5. History / Outcome Calibration

A temporary workspace was initialized, the simulated record was validated and saved, then an inline rejected outcome was added.

Final deterministic result:

- interviews: 1
- question-bank items: 16 interviewer questions
- competencies: 3
- anti-patterns: 4
- projects: 1
- stories: 1
- outcomes: 1
- calibration events: 1
- original verdict preserved: true

The first run exposed an ergonomics issue: argparse treated the abbreviated `--feedback` as `--feedback-file`. The script was fixed to support distinct `--feedback` text and `--feedback-file` inputs, with mutual exclusion.

## 6. Media Pipeline

A 20.102-second Chinese SAPI-generated WAV was processed through the actual local pipeline:

`WAV → ffmpeg 16k mono WAV → faster-whisper → TXT / Markdown / VTT / segments JSON / metadata`

Result:

- detected language: zh
- segment count: 3 (base model final run; small model was also exercised)
- speaker labels: 3 × `Unknown Speaker`
- output files: 6
- timestamped output: present
- triple-blank formatting regression: false

The pipeline correctly did **not** invent speaker identity. Base/small ASR still made minor recognition errors on synthetic speech, so source audio and raw evidence must be retained.

## Final Acceptance

**PASS after two defects were found and fixed.**

The tests prove installation, trigger loading, transcript analysis, Follow-up Tree reconstruction, evidence behavior, HTML rendering, deterministic history aggregation, outcome append and local ASR execution. They do not prove reliable acoustic diarization or perfect ASR accuracy on noisy real interviews.
