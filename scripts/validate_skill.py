#!/usr/bin/env python
"""Portable acceptance tests for pm-interview-transcript-review."""
from __future__ import annotations

import copy
import importlib.util
import json
import os
import py_compile
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "pm-interview-transcript-review"
REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "agents/openai.yaml",
    "requirements-feishu.txt",
    "references/scoring-and-diagnosis.md",
    "references/pm-competency-taxonomy.md",
    "references/history-and-calibration.md",
    "references/media-pipeline.md",
    "references/codex-feishu-automation.md",
    "references/external-design-notes.md",
    "references/test-report.md",
    "templates/full-review.md",
    "templates/interview-record.schema.json",
    "templates/organization-config.example.json",
    "scripts/install_skill.py",
    "scripts/interview_os.py",
    "scripts/transcribe_media.py",
    "scripts/render_review.py",
    "scripts/feishu_common.py",
    "scripts/set_feishu_credentials.ps1",
    "scripts/feishu_websocket_probe.py",
    "scripts/list_feishu_wikis.py",
    "scripts/setup_codex_feishu.py",
    "scripts/doctor.py",
    "scripts/validate_review.py",
    "scripts/publish_feishu_wiki.py",
    "scripts/codex_feishu_bridge.py",
    "examples/simulated-transcript.md",
    "examples/simulated-jd.md",
    "examples/simulated-resume.md",
    "examples/simulated-record.json",
    "examples/test-run-output.html",
]
EXPECTED_PACKAGE_FILES = frozenset(
    {
        "SKILL.md",
        "README.md",
        "LICENSE",
        "agents/openai.yaml",
        "requirements-feishu.txt",
        "scripts/install_skill.py",
        "scripts/interview_os.py",
        "scripts/transcribe_media.py",
        "scripts/render_review.py",
        "scripts/validate_skill.py",
        "scripts/feishu_common.py",
        "scripts/set_feishu_credentials.ps1",
        "scripts/feishu_websocket_probe.py",
        "scripts/list_feishu_wikis.py",
        "scripts/setup_codex_feishu.py",
        "scripts/doctor.py",
        "scripts/validate_review.py",
        "scripts/publish_feishu_wiki.py",
        "scripts/codex_feishu_bridge.py",
        "templates/full-review.md",
        "templates/interview-record.schema.json",
        "templates/organization-config.example.json",
        "references/codex-feishu-automation.md",
        "references/external-design-notes.md",
        "references/history-and-calibration.md",
        "references/media-pipeline.md",
        "references/pm-competency-taxonomy.md",
        "references/scoring-and-diagnosis.md",
        "references/test-report.md",
        "examples/atomic-claim-regression.md",
        "examples/simulated-jd.md",
        "examples/simulated-record.json",
        "examples/simulated-resume.md",
        "examples/simulated-transcript.md",
        "examples/test-run-output.html",
        "examples/test-run-output.md",
    }
)
STANDARD_FRONTMATTER_FIELDS = {
    "name",
    "description",
    "license",
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


def validate_frontmatter_mapping(frontmatter: dict, directory_name: str, errors: list[str]) -> None:
    name = frontmatter.get("name")
    check(name == directory_name, "frontmatter name must match the skill directory", errors)
    check(
        isinstance(name, str)
        and 1 <= len(name) <= 64
        and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) is not None,
        "name must be 1-64 lowercase alphanumeric characters separated by single hyphens",
        errors,
    )
    description = frontmatter.get("description", "")
    check(isinstance(description, str) and 1 <= len(description) <= 1024, "description must be 1-1024 characters", errors)
    check(
        isinstance(description, str)
        and "interview" in description.lower()
        and "product manager" in description.lower(),
        "description lacks routing keywords",
        errors,
    )
    check(frontmatter.get("license") == "MIT", "license must be MIT", errors)
    check(set(frontmatter).issubset(STANDARD_FRONTMATTER_FIELDS), "frontmatter contains non-standard top-level fields", errors)
    metadata = frontmatter.get("metadata", {})
    check(
        isinstance(metadata, dict)
        and all(isinstance(k, str) and isinstance(v, str) for k, v in metadata.items()),
        "metadata must map strings to strings for Agent Skills portability",
        errors,
    )


def make_directory_link(link: Path, target: Path) -> None:
    if os.name == "nt":
        result = subprocess.run(
            ["cmd.exe", "/c", "mklink", "/J", str(link), str(target)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        if result.returncode != 0:
            raise OSError(result.stderr.decode(errors="replace"))
    else:
        link.symlink_to(target, target_is_directory=True)


def remove_directory_link(link: Path) -> None:
    if not link.exists() and not link.is_symlink():
        return
    if os.name == "nt":
        os.rmdir(link)
    else:
        link.unlink()


def make_file_link(link: Path, target: Path) -> bool:
    try:
        if os.name == "nt":
            result = subprocess.run(
                ["cmd.exe", "/c", "mklink", str(link), str(target)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return result.returncode == 0
        link.symlink_to(target)
        return True
    except OSError:
        return False


def copy_package(source_root: Path, destination_root: Path, package_files: tuple[str, ...]) -> None:
    for relative in package_files:
        source = source_root / relative
        destination = destination_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def main() -> None:
    errors: list[str] = []
    for rel in REQUIRED_FILES:
        check((ROOT / rel).exists(), f"missing file: {rel}", errors)

    raw_skill = (ROOT / "SKILL.md").read_bytes()
    starts_with_fence = raw_skill.startswith(b"---") and len(raw_skill) > 3 and raw_skill[3] in (10, 13)
    check(starts_with_fence and not raw_skill.startswith(b"\xef\xbb\xbf"), "SKILL.md must start with --- at byte 0 and use UTF-8 without BOM", errors)
    skill = raw_skill.decode("utf-8")
    frontmatter = parse_frontmatter(skill, errors)
    validate_frontmatter_mapping(frontmatter, SKILL_NAME, errors)

    valid_fixture = dict(frontmatter)
    negative_frontmatter_fixtures = {
        "empty mapping": ({}, SKILL_NAME),
        "double-hyphen name": ({**valid_fixture, "name": "bad--name"}, "bad--name"),
        "nested metadata": ({**valid_fixture, "metadata": {"author": {"name": "nested"}}}, SKILL_NAME),
    }
    for label, (fixture, directory_name) in negative_frontmatter_fixtures.items():
        fixture_errors: list[str] = []
        validate_frontmatter_mapping(fixture, directory_name, fixture_errors)
        check(bool(fixture_errors), f"negative frontmatter fixture was accepted: {label}", errors)
    bom_fixture = b"\xef\xbb\xbf" + raw_skill
    check(not bom_fixture.startswith(b"---"), "negative frontmatter fixture was accepted: UTF-8 BOM", errors)
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
    for forbidden in ("skill_view",):
        check(forbidden not in skill, f"vendor-specific runtime dependency remains in SKILL.md: {forbidden}", errors)

    expected_chapters = [(str(index), title) for index, title in enumerate(OUTPUT_CHAPTERS, start=1)]
    if "## Output Contract" in skill:
        output_contract = skill.split("## Output Contract", 1)[1].split("### 第 0 章", 1)[0]
        skill_chapters = [
            (number, re.split(r"[：:]", title, maxsplit=1)[0].strip())
            for number, title in re.findall(r"^(\d{1,2})\.\s+(.+?)\s*$", output_contract, flags=re.MULTILINE)
        ]
    else:
        skill_chapters = []
    check(skill_chapters == expected_chapters, "SKILL Output Contract must contain exactly the ordered 16 chapters", errors)

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    check("面向 Codex" in readme and ".agents\\skills" in readme, "README lacks current Codex installation instructions", errors)
    check("codex login" in readme and "自己的 ChatGPT" in readme, "README lacks the personal Codex quota boundary", errors)
    check("codex_feishu_bridge.py" in readme and "组织固定知识库" in readme, "README lacks Feishu automation instructions", errors)
    check(all(title in readme for title in OUTPUT_CHAPTERS), "README does not name all 16 Full Review chapters", errors)

    template = (ROOT / "templates/full-review.md").read_text(encoding="utf-8")
    template_chapters = re.findall(r"^#\s+([1-9]\d*)\.\s+(.+?)\s*$", template, flags=re.MULTILINE)
    check(template_chapters == expected_chapters, "full-review template must contain exactly the ordered 16 chapters", errors)
    for heading in (
        "# 0. 面试实录与回答建议",
        "## 0.1 面试官提问与候选人回复",
        "## 0.2 回答建议",
        "## 0.3 候选人反问与面试官回答原文",
    ):
        check(heading in template, f"full-review template missing stable front module: {heading}", errors)
    check("No answer captured" in template, "full-review template lacks an explicit unanswered state", errors)
    check("本章不重复 Suggested Answer" in template, "chapter 6 does not de-duplicate Better Answers", errors)

    for script in (
        "install_skill.py", "interview_os.py", "transcribe_media.py", "render_review.py",
        "validate_skill.py", "feishu_common.py", "setup_codex_feishu.py", "doctor.py",
        "validate_review.py", "publish_feishu_wiki.py", "codex_feishu_bridge.py",
    ):
        try:
            py_compile.compile(str(ROOT / "scripts" / script), doraise=True)
        except Exception as exc:
            errors.append(f"script syntax error {script}: {exc}")

    installer = load_module(ROOT / "scripts" / "install_skill.py", "install_skill_under_test")
    package_files = set(installer.PACKAGE_FILES)
    check(
        package_files == EXPECTED_PACKAGE_FILES,
        "installer PACKAGE_FILES must match the Codex release contract exactly",
        errors,
    )
    check(len(package_files) == len(installer.PACKAGE_FILES), "installer package allowlist contains duplicates", errors)
    check(set(REQUIRED_FILES).issubset(package_files), "installer package allowlist omits required files", errors)
    check(
        all(not Path(relative).is_absolute() and ".." not in Path(relative).parts for relative in package_files),
        "installer package allowlist contains an absolute or parent-traversal path",
        errors,
    )
    with tempfile.TemporaryDirectory(prefix="pm-review-installer-test-") as temp:
        temp_path = Path(temp)
        parser = installer.build_parser()
        for agent in installer.SUPPORTED_AGENTS:
            user_args = parser.parse_args(["--agent", agent, "--scope", "user"])
            check(
                installer.resolve_destination(user_args)
                == installer.user_root(agent).expanduser().absolute() / installer.SKILL_NAME,
                f"wrong user-scope destination for {agent}",
                errors,
            )
            project_dir = temp_path / f"project-{agent}"
            project_args = parser.parse_args(
                ["--agent", agent, "--scope", "project", "--project-dir", str(project_dir)]
            )
            check(
                installer.resolve_destination(project_args)
                == installer.project_root(agent, project_dir.absolute()).absolute() / installer.SKILL_NAME,
                f"wrong project-scope destination for {agent}",
                errors,
            )

        custom_root = temp_path / "custom-target"
        custom_result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/install_skill.py"), "--target", str(custom_root)],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            capture_output=True,
        )
        check(custom_result.returncode == 0, "installer --target execution failed", errors)
        check(
            (custom_root / installer.SKILL_NAME / "SKILL.md").is_file(),
            "installer --target did not create the expected skill directory",
            errors,
        )
        destination = temp_path / "skills" / installer.SKILL_NAME
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

            rollback_destination = temp_path / "rollback" / installer.SKILL_NAME
            installer.install(rollback_destination, force=False)
            rollback_marker = rollback_destination / "keep-me.txt"
            rollback_marker.write_text("existing installation", encoding="utf-8")
            original_copy2 = installer.shutil.copy2
            try:
                installer.shutil.copy2 = lambda *_args, **_kwargs: (_ for _ in ()).throw(
                    OSError("simulated staging copy failure")
                )
                try:
                    installer.install(rollback_destination, force=True)
                    errors.append("installer did not surface a simulated staging copy failure")
                except OSError:
                    pass
            finally:
                installer.shutil.copy2 = original_copy2
            check(
                rollback_marker.is_file(),
                "installer --force removed the working installation after a staging copy failure",
                errors,
            )

            destination_path_class = type(rollback_destination)
            original_replace = destination_path_class.replace

            def fail_staged_swap(path: Path, target: Path) -> Path:
                if path.name.startswith(f".{installer.SKILL_NAME}.staged-") and Path(target).name == installer.SKILL_NAME:
                    raise OSError("simulated post-backup staged rename failure")
                return original_replace(path, target)

            try:
                destination_path_class.replace = fail_staged_swap
                try:
                    installer.install(rollback_destination, force=True)
                    errors.append("installer did not surface a simulated staged rename failure")
                except OSError:
                    pass
            finally:
                destination_path_class.replace = original_replace
            check(
                rollback_marker.is_file(),
                "installer --force did not restore the previous installation after a staged rename failure",
                errors,
            )
            rollback_leftovers = [
                path
                for path in rollback_destination.parent.iterdir()
                if path.name.startswith(f".{installer.SKILL_NAME}.")
            ]
            check(not rollback_leftovers, "installer left staging or backup directories after rollback", errors)

            junction_source = temp_path / "source-ancestor-junction"
            copy_package(ROOT, junction_source, installer.PACKAGE_FILES)
            redirected_examples = junction_source / "redirected-examples"
            (junction_source / "examples").replace(redirected_examples)
            source_examples_link = junction_source / "examples"
            make_directory_link(source_examples_link, redirected_examples)
            try:
                installer.SOURCE_ROOT = junction_source
                try:
                    installer.install(temp_path / "source-junction-output" / installer.SKILL_NAME, force=False)
                    errors.append("installer accepted a source ancestor symlink/junction")
                except SystemExit:
                    pass
            finally:
                installer.SOURCE_ROOT = original_source_root
                remove_directory_link(source_examples_link)

            direct_source = temp_path / "source-direct-link"
            copy_package(ROOT, direct_source, installer.PACKAGE_FILES)
            direct_source_file = direct_source / "SKILL.md"
            direct_source_file.unlink()
            direct_source_link_created = make_file_link(direct_source_file, direct_source / "README.md")
            if direct_source_link_created:
                try:
                    installer.SOURCE_ROOT = direct_source
                    try:
                        installer.install(temp_path / "direct-source-output" / installer.SKILL_NAME, force=False)
                        errors.append("installer accepted a direct source symlink")
                    except SystemExit:
                        pass
                finally:
                    installer.SOURCE_ROOT = original_source_root
                    direct_source_file.unlink(missing_ok=True)

            real_destination_parent = temp_path / "real-destination-parent"
            real_destination_parent.mkdir()
            linked_destination_parent = temp_path / "linked-destination-parent"
            make_directory_link(linked_destination_parent, real_destination_parent)
            try:
                try:
                    installer.install(linked_destination_parent / installer.SKILL_NAME, force=False)
                    errors.append("installer accepted a destination ancestor symlink/junction")
                except SystemExit:
                    pass
                linked_target_result = subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "scripts/install_skill.py"),
                        "--target",
                        str(linked_destination_parent),
                    ],
                    cwd=ROOT,
                    text=True,
                    encoding="utf-8",
                    capture_output=True,
                )
                check(
                    linked_target_result.returncode != 0
                    and not (real_destination_parent / installer.SKILL_NAME).exists(),
                    "installer CLI accepted a --target ancestor symlink/junction",
                    errors,
                )
            finally:
                remove_directory_link(linked_destination_parent)

            direct_destination_target = temp_path / "direct-destination-target"
            direct_destination_target.mkdir()
            direct_destination_parent = temp_path / "direct-destination-parent"
            direct_destination_parent.mkdir()
            direct_destination_link = direct_destination_parent / installer.SKILL_NAME
            make_directory_link(direct_destination_link, direct_destination_target)
            try:
                try:
                    installer.install(direct_destination_link, force=True)
                    errors.append("installer accepted a direct destination symlink/junction")
                except SystemExit:
                    pass
            finally:
                remove_directory_link(direct_destination_link)
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
    legacy_record = copy.deepcopy({
        key: value
        for key, value in record.items()
        if key not in {"question_transcript", "answer_suggestions"}
    })
    legacy_record["schema_version"] = "1.0"
    suggestion_by_id = {item["question_id"]: item for item in record["answer_suggestions"]}
    for review in legacy_record["key_answer_reviews"]:
        review.pop("answer_suggestion_ref", None)
        review["suggested_answer"] = suggestion_by_id[review["question_id"]]["suggested_answer"]
    check(
        not interview_os.validate_record(legacy_record),
        "interview_os no longer accepts legacy schema 1.0 records",
        errors,
    )
    missing_pair_record = copy.deepcopy(record)
    missing_pair_record["question_transcript"].pop()
    check(
        bool(interview_os.validate_record(missing_pair_record)),
        "negative record fixture accepted a missing question/answer pair",
        errors,
    )
    reverse_suggestion_record = copy.deepcopy(record)
    reverse_suggestion = copy.deepcopy(reverse_suggestion_record["answer_suggestions"][0])
    reverse_suggestion["question_id"] = "Q05"
    reverse_suggestion_record["answer_suggestions"].append(reverse_suggestion)
    check(
        bool(interview_os.validate_record(reverse_suggestion_record)),
        "negative record fixture accepted a Better Answer for a candidate reverse question",
        errors,
    )
    missing_exchange_record = copy.deepcopy(record)
    missing_exchange_record["reverse_interview"]["exchanges"] = []
    check(
        bool(interview_os.validate_record(missing_exchange_record)),
        "negative record fixture accepted an unpaired candidate reverse question",
        errors,
    )
    questions = record["questions"]
    eligible_question_ids = {
        item["id"] for item in questions if item["type"] in {"root", "follow-up"}
    }
    reverse_question_ids = {
        item["id"] for item in questions if item["type"] == "candidate-reverse-question"
    }
    transcript_question_ids = {item["question_id"] for item in record["question_transcript"]}
    suggestion_question_ids = {item["question_id"] for item in record["answer_suggestions"]}
    reverse_exchange_ids = {
        item["question_id"] for item in record["reverse_interview"]["exchanges"]
    }
    check(transcript_question_ids == eligible_question_ids, "structured transcript coverage drifted from questions", errors)
    check(suggestion_question_ids == eligible_question_ids, "answer suggestions do not cover every eligible question", errors)
    check(reverse_exchange_ids == reverse_question_ids, "reverse exchanges do not cover every candidate reverse question", errors)
    check(not (suggestion_question_ids & reverse_question_ids), "candidate reverse question received a Better Answer", errors)
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
        any("[这里需要补充：" in item.get("suggested_answer", "") for item in record["answer_suggestions"]),
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
        sample_chapters = re.findall(r"^#\s+([1-9]\d*)\.\s+(.+?)\s*$", text, flags=re.MULTILINE)
        check(sample_chapters == expected_chapters, "test-run output must contain exactly the ordered 16 chapters", errors)
        front_match = re.search(
            r"^# 0\. 面试实录与回答建议\s*$([\s\S]*?)(?=^# 1\. Executive Summary\s*$)",
            text,
            flags=re.MULTILINE,
        )
        check(front_match is not None, "test-run output is missing the complete chapter 0", errors)
        front = front_match.group(1) if front_match else ""
        raw_section = front.split("## 0.1 面试官提问与候选人回复", 1)[-1].split("## 0.2 回答建议", 1)[0]
        suggestion_section = front.split("## 0.2 回答建议", 1)[-1].split("## 0.3 候选人反问与面试官回答原文", 1)[0]
        reverse_section = front.split("## 0.3 候选人反问与面试官回答原文", 1)[-1]
        sample_raw_ids = re.findall(r"^#{3,5}\s+(Q[0-9]{2,}(?:\.[0-9]+)*)\b", raw_section, flags=re.MULTILINE)
        sample_suggestion_ids = re.findall(r"^###\s+(Q[0-9]{2,}(?:\.[0-9]+)*)\s*$", suggestion_section, flags=re.MULTILINE)
        sample_reverse_ids = re.findall(r"^###\s+(RQ[0-9]{2,})\s*$", reverse_section, flags=re.MULTILINE)
        check(len(sample_raw_ids) == len(set(sample_raw_ids)), "chapter 0.1 repeats a Q ID", errors)
        check(set(sample_raw_ids) == eligible_question_ids, "chapter 0.1 does not cover every root/follow-up", errors)
        check(len(sample_suggestion_ids) == len(set(sample_suggestion_ids)), "chapter 0.2 repeats a Q ID", errors)
        check(set(sample_suggestion_ids) == suggestion_question_ids, "chapter 0.2 does not match structured answer suggestions", errors)
        expected_reverse_ids = {item["exchange_id"] for item in record["reverse_interview"]["exchanges"]}
        check(set(sample_reverse_ids) == expected_reverse_ids, "chapter 0.3 does not match reverse exchanges", errors)
        check(raw_section.count("候选人原回复：") == len(eligible_question_ids), "chapter 0.1 has missing or duplicate candidate replies", errors)
        for label in ("Recommended Structure", "Suggested Answer", "Missing Facts", "Provenance Check"):
            check(
                suggestion_section.count(f"- {label}：") == len(suggestion_question_ids),
                f"chapter 0.2 does not contain exactly one {label} per suggestion",
                errors,
            )
        for row in record["question_transcript"]:
            qid = row["question_id"]
            check(row["question"]["raw_text"] in raw_section, f"chapter 0.1 changed or omitted raw question {qid}", errors)
            if row["answer"]["status"] == "captured":
                check(row["answer"]["raw_text"] in raw_section, f"chapter 0.1 changed or omitted raw answer {qid}", errors)
        for item in record["answer_suggestions"]:
            check(item["suggested_answer"] in suggestion_section, f"chapter 0.2 drifted from answer suggestion {item['question_id']}", errors)
        for item in record["reverse_interview"]["exchanges"]:
            check(item["candidate_question"]["raw_text"] in reverse_section, f"chapter 0.3 omitted {item['exchange_id']} candidate question", errors)
            check(item["interviewer_answer"]["raw_text"] in reverse_section, f"chapter 0.3 omitted {item['exchange_id']} interviewer answer", errors)
        diagnostics = text.split("# 1. Executive Summary", 1)[-1]
        check("### Part B — Suggested Answer" not in diagnostics, "chapter 6 duplicates Suggested Answers from chapter 0.2", errors)
        check("Better version（如需）" not in diagnostics, "chapter 13 rewrites candidate reverse questions", errors)
        check("Q02.2.1" in text and "Q02.4.1" in text and "Q02.5.1" in text, "test-run output missing nested follow-up", errors)
        check("推断" in text and "Evidence" in text, "test-run output lacks fact/inference or evidence labeling", errors)
        check("[这里需要补充：" in text, "test-run Better Answer may have invented missing facts", errors)
        check("知道用户常常不知道该怎么描述需求" not in text, "fixture caught an unsupported insight inferred only from '做过用户访谈'", errors)
        check("Insufficient history" in text and "首场" in text, "test-run invented or omitted first-session trend state", errors)
        html_path = ROOT / "examples/test-run-output.html"
        check(html_path.exists(), "rendered HTML fixture is missing", errors)
        if html_path.exists():
            html_text = html_path.read_text(encoding="utf-8-sig")
            check("0.1 面试官提问与候选人回复" in html_text, "rendered HTML omitted chapter 0.1", errors)
            check("RQ01" in html_text and "北极星还是创作 DAU" in html_text, "rendered HTML omitted reverse-interview originals", errors)
            check("Part B — Suggested Answer" not in html_text, "rendered HTML retained duplicated chapter 6 Better Answers", errors)

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
                "standard": "Codex Skill",
                "skill": str(ROOT),
                "required_files": len(REQUIRED_FILES),
                "package_files": len(installer.PACKAGE_FILES),
                "questions": len(questions),
                "question_transcript": len(record["question_transcript"]),
                "answer_suggestions": len(record["answer_suggestions"]),
                "reverse_exchanges": len(record["reverse_interview"]["exchanges"]),
                "q02_followups": len(q02_descendants),
                "shortcoming_cards": len(record["shortcoming_cards"]),
                "installer_smoke_test": True,
                "personal_codex_quota": True,
                "test_run_output_present": expected.exists(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
