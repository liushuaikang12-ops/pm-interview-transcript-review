#!/usr/bin/env python
"""Static and fixture-level acceptance tests for pm-interview-transcript-review."""
from __future__ import annotations

import importlib.util
import json
import py_compile
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "references/scoring-and-diagnosis.md",
    "references/pm-competency-taxonomy.md",
    "references/history-and-calibration.md",
    "references/media-pipeline.md",
    "references/external-design-notes.md",
    "references/test-report.md",
    "templates/full-review.md",
    "templates/interview-record.schema.json",
    "scripts/interview_os.py",
    "scripts/transcribe_media.py",
    "scripts/render_review.py",
    "references/examples/simulated-transcript.md",
    "references/examples/simulated-jd.md",
    "references/examples/simulated-resume.md",
    "references/examples/simulated-record.json",
    "references/examples/test-run-output.html",
]


def check(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("interview_os_under_test", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def main() -> None:
    errors: list[str] = []
    for rel in REQUIRED_FILES:
        check((ROOT / rel).exists(), f"missing file: {rel}", errors)

    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8-sig")
    check(skill.startswith("---\n"), "SKILL.md must start with frontmatter at byte 0", errors)
    match = re.search(r"\n---\s*\n", skill[3:])
    check(match is not None, "SKILL.md frontmatter closing fence missing", errors)
    if match:
        fm = yaml.safe_load(skill[3:match.start() + 3])
        check(fm.get("name") == "pm-interview-transcript-review", "frontmatter name mismatch", errors)
        desc = fm.get("description", "")
        check(len(desc) <= 60 and desc.startswith("Use when ") and desc.endswith("."), "description routing contract failed", errors)
    check(len(skill) <= 100_000, "SKILL.md exceeds Hermes limit", errors)
    for section in ("Trigger Conditions", "Inputs", "Workflow", "Output Contract", "Memory / History Behavior", "Evidence Rules", "Safety against Hallucination"):
        check(f"## {section}" in skill, f"missing SKILL section: {section}", errors)
    for term in ("Follow-up Tree", "Root Cause", "Shortcoming", "Shadow JD", "Outcome Calibration", "AI PM", "Growth PM"):
        check(term in skill, f"core concept absent from SKILL.md: {term}", errors)

    for script in ("interview_os.py", "transcribe_media.py", "render_review.py", "validate_skill.py"):
        try:
            py_compile.compile(str(ROOT / "scripts" / script), doraise=True)
        except Exception as exc:
            errors.append(f"script syntax error {script}: {exc}")

    schema = json.loads((ROOT / "templates/interview-record.schema.json").read_text(encoding="utf-8"))
    record = json.loads((ROOT / "references/examples/simulated-record.json").read_text(encoding="utf-8"))
    try:
        import jsonschema
        jsonschema.validate(record, schema)
    except Exception as exc:
        errors.append(f"JSON schema validation failed: {exc}")

    module = load_module(ROOT / "scripts" / "interview_os.py")
    errors.extend(f"record semantic validation: {x}" for x in module.validate_record(record))

    questions = record["questions"]
    q02_descendants = [q for q in questions if q["id"].startswith("Q02.")]
    check(len(q02_descendants) >= 5, "fixture lacks a root question with at least five follow-ups", errors)
    check(any(q["parent_id"] is not None for q in questions), "fixture flattened all follow-ups", errors)
    check(any(q["id"].count(".") >= 2 for q in questions), "fixture lacks nested evidence challenge", errors)
    check(all((q["underlying_intent"] is None or q["underlying_intent"].get("label") == "inference") for q in questions), "intent not explicitly marked inference", errors)
    check(all(x.get("evidence") for x in record["key_answer_reviews"]), "key answer without evidence", errors)
    check(any("[这里需要补充：" in x.get("suggested_answer", "") for x in record["key_answer_reviews"]), "Better Answer fixture does not preserve fact gaps", errors)
    check(3 <= len(record["shortcoming_cards"]) <= 7, "Shortcoming Card count outside 3-7", errors)
    check(all(x.get("evidence_anchors") and x.get("label") == "inference" for x in record["shadow_jd"]), "Shadow JD grounding failed", errors)

    transcript = (ROOT / "references/examples/simulated-transcript.md").read_text(encoding="utf-8")
    for coverage in ("自我介绍", "为什么当时要做", "异常数据", "AI 写作", "D7 留存", "想问我的"):
        check(coverage in transcript, f"fixture missing coverage: {coverage}", errors)

    expected = ROOT / "references/examples/test-run-output.md"
    if expected.exists():
        text = expected.read_text(encoding="utf-8-sig")
        for n in range(1, 17):
            check(re.search(rf"^# {n}\. ", text, flags=re.M) is not None, f"test-run output missing section {n}", errors)
        check("Q02.2.1" in text and "Q02.4.1" in text and "Q02.5.1" in text, "test-run output missing nested follow-up", errors)
        check("推断" in text and "Evidence" in text, "test-run output lacks fact/inference or evidence labeling", errors)
        check("[这里需要补充：" in text, "test-run Better Answer may have invented missing facts", errors)
        check(text.count("### Part B — Suggested Answer") == text.count("### Provenance Check"), "every Suggested Answer needs a Provenance Check", errors)
        check("知道用户常常不知道该怎么描述需求" not in text, "fixture caught unsupported insight inferred only from '做过用户访谈'", errors)
        check("Insufficient history" in text and "首场" in text, "test-run invented or omitted first-session trend state", errors)

    regression = ROOT / "references/examples/atomic-claim-regression.md"
    check(regression.exists(), "missing Atomic Claim regression artifact", errors)
    if regression.exists():
        regression_text = regression.read_text(encoding="utf-8-sig")
        check("Atomic Claim Audit" in regression_text and "Negative-entailment check" in regression_text, "regression missing claim-level audit", errors)
        check("这是我的假设，不是已验证洞察" in regression_text, "unsupported user insight was not framed as hypothesis", errors)
        check("没有把「访谈过用户」扩写成任何具体用户洞察" in regression_text, "regression did not close the fabrication trap", errors)

    if errors:
        print("FAIL")
        for e in errors:
            print(f"- {e}")
        raise SystemExit(1)
    print(json.dumps({
        "status": "PASS",
        "skill": str(ROOT),
        "required_files": len(REQUIRED_FILES),
        "questions": len(questions),
        "q02_followups": len(q02_descendants),
        "shortcoming_cards": len(record["shortcoming_cards"]),
        "test_run_output_present": expected.exists()
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
