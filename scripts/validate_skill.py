#!/usr/bin/env python
"""Portable acceptance tests for pm-interview-transcript-review."""
from __future__ import annotations

import importlib.util
import json
import os
import py_compile
import re
import shutil
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "references/scoring-and-diagnosis.md",
    "references/pm-competency-taxonomy.md",
    "references/history-and-calibration.md",
    "references/media-pipeline.md",
    "references/external-design-notes.md",
    "references/test-report.md",
    "templates/full-review.md",
    "templates/interview-record.schema.json",
    "scripts/install_skill.py",
    "scripts/interview_os.py",
    "scripts/transcribe_media.py",
    "scripts/render_review.py",
    "examples/simulated-transcript.md",
    "examples/simulated-jd.md",
    "examples/simulated-resume.md",
    "examples/simulated-record.json",
    "examples/test-run-output.html",
]
STANDARD_FRONTMATTER_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
OUTPUT_CHAPTERS = [
    "Executive Summary",
    "Interview Structure",
    "Complete Question Map",
    "Follow-up Trees",
    "Competency Mapping",
    "Key Answer Reviews",
    "Evidence & Quotes",
    "Shortcoming Cards",
    "Anti-patterns",
    "Project Probe Depth",
    "Role-specific Review",
    "Interviewer Signals",
    "Reverse Interview Intelligence",
    "Shadow JD",
    "Cross-interview Update",
    "Next Interview Actions",
]


def check(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def parse_frontmatter(skill: str, errors: list[str]) -> dict:
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z", skill, flags=re.S)
    check(match is not None, "SKILL.md must contain frontmatter at byte 0 followed by a body", errors)
    if not match:
        return {}
    try:
        frontmatter = yaml.safe_load(match.group(1))
    except Exception as exc:
        errors.append(f"invalid YAML frontmatter: {exc}")
        return {}
    check(isinstance(frontmatter, dict), "frontmatter must be a YAML mapping", errors)
    check(bool(match.group(2).strip()), "SKILL.md body must be non-empty", errors)
    return frontmatter if isinstance(frontmatter, dict) else {}


def main() -> None:
    errors: list[str] = []
    for rel in REQUIRED_FILES:
        check((ROOT / rel).exists(), f"missing file: {rel}", errors)

    raw_skill = (ROOT / "SKILL.md").read_bytes()
    starts_with_fence = raw_skill.startswith(b"---") and len(raw_skill) > 3 and raw_skill[3] in (10, 13)
    check(starts_with_fence and not raw_skill.startswith(b"\xef\xbb\xbf"), "SKILL.md must start with --- at byte 0 and use UTF-8 without BOM", errors)
    skill = raw_skill.decode("utf-8")
    frontmatter = parse_frontmatter(skill, errors)
    if frontmatter:
        name = frontmatter.get("name")
        check(name == ROOT.name, "frontmatter name must match the skill directory", errors)
        check(
            isinstance(name, str)
            and 1 <= len(name) <= 64
            and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) is not None,
            "name must be 1-64 lowercase alphanumeric characters separated by single hyphens",
            errors,
        )
        description = frontmatter.get("description", "")
        check(isinstance(description, str) and 1 <= len(description) <= 1024, "description must be 1-1024 characters", errors)
        check("interview" in description.lower() and "product manager" in description.lower(), "description lacks routing keywords", errors)
        compatibility = frontmatter.get("compatibility", "")
        check(isinstance(compatibility, str) and 1 <= len(compatibility) <= 500, "compatibility must be a 1-500 character string", errors)
        check(frontmatter.get("license") == "MIT", "license must be MIT", errors)
        check(set(frontmatter).issubset(STANDARD_FRONTMATTER_FIELDS), "frontmatter contains non-standard top-level fields", errors)
        metadata = frontmatter.get("metadata", {})
        check(
            isinstance(metadata, dict)
            and all(isinstance(k, str) and isinstance(v, str) for k, v in metadata.items()),
            "metadata must map strings to strings for Agent Skills portability",
            errors,
        )
    check(len(skill) <= 100_000, "SKILL.md exceeds the 100,000-character portability budget", errors)
    check(len(skill.splitlines()) <= 500, "SKILL.md exceeds the 500-line progressive-disclosure budget", errors)
    for section in (
        "Trigger Conditions",
        "Inputs",
        "Workflow",
        "Output Contract",
        "History / Persistence Behavior",
        "Evidence Rules",
        "Safety against Hallucination",
    ):
        check(f"## {section}" in skill, f"missing SKILL section: {section}", errors)
    for term in ("Follow-up Tree", "Root Cause", "Shortcoming", "Shadow JD", "Outcome Calibration", "AI PM", "Growth PM", "Strategy PM"):
        check(term in skill, f"core concept absent from SKILL.md: {term}", errors)
    for forbidden in ("HERMES_HOME", "HERMES_SKILL_DIR", "skill_view"):
        check(forbidden not in skill, f"vendor-specific runtime dependency remains in SKILL.md: {forbidden}", errors)

    expected_chapters = [(str(index), title) for index, title in enumerate(OUTPUT_CHAPTERS, start=1)]
    if "## Output Contract" in skill:
        output_contract = skill.split("## Output Contract", 1)[1].split("### 实录前置", 1)[0]
        skill_chapters = [
            (number, re.split(r"[：:]", title, maxsplit=1)[0].strip())
            for number, title in re.findall(r"^(\d{1,2})\.\s+(.+?)\s*$", output_contract, flags=re.MULTILINE)
        ]
    else:
        skill_chapters = []
    check(skill_chapters == expected_chapters, "SKILL Output Contract must contain exactly the ordered 16 chapters", errors)

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    check("Agent Skills 开放标准" in readme, "README does not explain the portability standard", errors)
    check("scripts/install_skill.py" in readme and "--target" in readme, "README lacks portable installation instructions", errors)
    check("默认交付物" in readme and "review.md" in readme and "record.json" in readme, "README lacks artifact-level output contract", errors)
    readme_chapters = re.findall(r"^###\s+(\d{1,2})\.\s+(.+?)\s*$", readme, flags=re.MULTILINE)
    check(readme_chapters == expected_chapters, "README must document exactly the ordered 16 chapters", errors)

    template = (ROOT / "templates/full-review.md").read_text(encoding="utf-8")
    template_chapters = re.findall(r"^#\s+(\d{1,2})\.\s+(.+?)\s*$", template, flags=re.MULTILINE)
    check(template_chapters == expected_chapters, "full-review template must contain exactly the ordered 16 chapters", errors)

    for script in ("install_skill.py", "interview_os.py", "transcribe_media.py", "render_review.py", "validate_skill.py"):
        try:
            py_compile.compile(str(ROOT / "scripts" / script), doraise=True)
        except Exception as exc:
            errors.append(f"script syntax error {script}: {exc}")

    installer = load_module(ROOT / "scripts" / "install_skill.py", "install_skill_under_test")
    package_files = set(installer.PACKAGE_FILES)
    check(len(package_files) == len(installer.PACKAGE_FILES), "installer package allowlist contains duplicates", errors)
    check(set(REQUIRED_FILES).issubset(package_files), "installer package allowlist omits required files", errors)
    check(
        all(not Path(relative).is_absolute() and ".." not in Path(relative).parts for relative in package_files),
        "installer package allowlist contains an absolute or parent-traversal path",
        errors,
    )
    with tempfile.TemporaryDirectory(prefix="pm-review-installer-test-") as temp:
        destination = Path(temp) / "skills" / installer.SKILL_NAME
        try:
            installer.install(destination, force=False)
            check((destination / "SKILL.md").is_file(), "installer did not copy SKILL.md", errors)
            check((destination / "references").is_dir(), "installer did not copy references", errors)
            check((destination / "templates" / "full-review.md").is_file(), "installer did not copy templates", errors)
            check(not (destination / ".git").exists(), "installer copied repository metadata", errors)
            marker = destination / "local-change.txt"
            marker.write_text("must be removed by --force", encoding="utf-8")
            try:
                installer.install(destination, force=False)
                errors.append("installer overwrote an existing destination without --force")
            except SystemExit:
                pass
            installer.install(destination, force=True)
            check(not marker.exists(), "installer --force did not replace the previous directory", errors)
            installed_files = {
                path.relative_to(destination).as_posix()
                for path in destination.rglob("*")
                if path.is_file()
            }
            check(
                installed_files == set(installer.PACKAGE_FILES),
                "installer output differs from the explicit package allowlist",
                errors,
            )
            try:
                installer.install(Path(temp) / "wrong-skill-name", force=False)
                errors.append("installer accepted a destination whose name does not match the skill")
            except SystemExit:
                pass
            try:
                installer.install(ROOT / ".agents" / "skills" / installer.SKILL_NAME, force=False)
                errors.append("installer accepted a recursive destination inside the source repository")
            except SystemExit:
                pass

            source_copy = Path(temp) / "source-with-private-files"
            for relative in installer.PACKAGE_FILES:
                source = ROOT / relative
                copied = source_copy / relative
                copied.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, copied)
            (source_copy / ".env").write_text("PRIVATE_TOKEN=must-not-copy", encoding="utf-8")
            private_transcript = source_copy / "examples" / "private-interview.md"
            private_transcript.write_text("private interview content", encoding="utf-8")
            original_source_root = installer.SOURCE_ROOT
            try:
                installer.SOURCE_ROOT = source_copy
                privacy_destination = Path(temp) / "privacy" / installer.SKILL_NAME
                installer.install(privacy_destination, force=False)
                check(not (privacy_destination / ".env").exists(), "installer copied a private .env file", errors)
                check(
                    not (privacy_destination / "examples" / "private-interview.md").exists(),
                    "installer copied an unlisted private transcript",
                    errors,
                )
            finally:
                installer.SOURCE_ROOT = original_source_root
        except Exception as exc:
            errors.append(f"portable installer smoke test failed: {exc}")

    interview_os = load_module(ROOT / "scripts" / "interview_os.py", "interview_os_under_test")
    original_review_home = os.environ.get("PM_INTERVIEW_REVIEW_HOME")
    try:
        with tempfile.TemporaryDirectory(prefix="pm-review-home-test-") as temp:
            os.environ["PM_INTERVIEW_REVIEW_HOME"] = temp
            check(interview_os.default_root() == Path(temp), "PM_INTERVIEW_REVIEW_HOME is not honored", errors)
    finally:
        if original_review_home is None:
            os.environ.pop("PM_INTERVIEW_REVIEW_HOME", None)
        else:
            os.environ["PM_INTERVIEW_REVIEW_HOME"] = original_review_home

    schema = json.loads((ROOT / "templates/interview-record.schema.json").read_text(encoding="utf-8"))
    record = json.loads((ROOT / "examples/simulated-record.json").read_text(encoding="utf-8"))
    try:
        import jsonschema

        jsonschema.validate(record, schema)
    except Exception as exc:
        errors.append(f"JSON schema validation failed: {exc}")

    errors.extend(f"record semantic validation: {item}" for item in interview_os.validate_record(record))
    questions = record["questions"]
    q02_descendants = [question for question in questions if question["id"].startswith("Q02.")]
    check(len(q02_descendants) >= 5, "fixture lacks a root question with at least five follow-ups", errors)
    check(any(question["parent_id"] is not None for question in questions), "fixture flattened all follow-ups", errors)
    check(any(question["id"].count(".") >= 2 for question in questions), "fixture lacks a nested evidence challenge", errors)
    check(
        all(
            question["underlying_intent"] is None
            or question["underlying_intent"].get("label") == "inference"
            for question in questions
        ),
        "intent not explicitly marked inference",
        errors,
    )
    check(all(item.get("evidence") for item in record["key_answer_reviews"]), "key answer without evidence", errors)
    check(
        any("[这里需要补充：" in item.get("suggested_answer", "") for item in record["key_answer_reviews"]),
        "Better Answer fixture does not preserve fact gaps",
        errors,
    )
    check(3 <= len(record["shortcoming_cards"]) <= 7, "Shortcoming Card count outside 3-7", errors)
    check(
        all(item.get("evidence_anchors") and item.get("label") == "inference" for item in record["shadow_jd"]),
        "Shadow JD grounding failed",
        errors,
    )

    transcript = (ROOT / "examples/simulated-transcript.md").read_text(encoding="utf-8")
    for coverage in ("自我介绍", "为什么当时要做", "异常数据", "AI 写作", "D7 留存", "想问我的"):
        check(coverage in transcript, f"fixture missing coverage: {coverage}", errors)

    expected = ROOT / "examples/test-run-output.md"
    if expected.exists():
        text = expected.read_text(encoding="utf-8-sig")
        sample_chapters = re.findall(r"^#\s+(\d{1,2})\.\s+(.+?)\s*$", text, flags=re.MULTILINE)
        check(sample_chapters == expected_chapters, "test-run output must contain exactly the ordered 16 chapters", errors)
        check("Q02.2.1" in text and "Q02.4.1" in text and "Q02.5.1" in text, "test-run output missing nested follow-up", errors)
        check("推断" in text and "Evidence" in text, "test-run output lacks fact/inference or evidence labeling", errors)
        check("[这里需要补充：" in text, "test-run Better Answer may have invented missing facts", errors)
        check(
            text.count("### Part B — Suggested Answer") == text.count("### Provenance Check"),
            "every Suggested Answer needs a Provenance Check",
            errors,
        )
        check("知道用户常常不知道该怎么描述需求" not in text, "fixture caught an unsupported insight inferred only from '做过用户访谈'", errors)
        check("Insufficient history" in text and "首场" in text, "test-run invented or omitted first-session trend state", errors)

    regression = ROOT / "examples/atomic-claim-regression.md"
    check(regression.exists(), "missing Atomic Claim regression artifact", errors)
    if regression.exists():
        regression_text = regression.read_text(encoding="utf-8-sig")
        check("Atomic Claim Audit" in regression_text and "Negative-entailment check" in regression_text, "regression missing claim-level audit", errors)
        check("这是我的假设，不是已验证洞察" in regression_text, "unsupported user insight was not framed as a hypothesis", errors)
        check("没有把「访谈过用户」扩写成任何具体用户洞察" in regression_text, "regression did not close the fabrication trap", errors)

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(
        json.dumps(
            {
                "status": "PASS",
                "standard": "Agent Skills",
                "skill": str(ROOT),
                "required_files": len(REQUIRED_FILES),
                "package_files": len(installer.PACKAGE_FILES),
                "questions": len(questions),
                "q02_followups": len(q02_descendants),
                "shortcoming_cards": len(record["shortcoming_cards"]),
                "installer_smoke_test": True,
                "portable_workspace": True,
                "test_run_output_present": expected.exists(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
