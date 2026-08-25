#!/usr/bin/env python
"""Install this repository into a Codex skills directory."""
from __future__ import annotations

import argparse
import os
import shutil
import tempfile
from pathlib import Path

SKILL_NAME = "pm-interview-transcript-review"
SOURCE_ROOT = Path(__file__).resolve().parents[1]
SUPPORTED_AGENTS = (
    "codex",
)
PACKAGE_FILES = (
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
)


def user_root(agent: str) -> Path:
    home = Path.home()
    if agent == "codex":
        return home / ".agents" / "skills"
    raise ValueError(f"unsupported agent: {agent}")


def project_root(agent: str, project_dir: Path) -> Path:
    if agent == "codex":
        return project_dir / ".agents" / "skills"
    raise ValueError(f"unsupported agent: {agent}")


def resolve_destination(args: argparse.Namespace) -> Path:
    if args.target:
        return Path(args.target).expanduser().absolute() / SKILL_NAME
    if args.scope == "user":
        root = user_root(args.agent)
    else:
        project_dir = Path(args.project_dir or Path.cwd()).expanduser().absolute()
        root = project_root(args.agent, project_dir)
    return root.expanduser().absolute() / SKILL_NAME


def is_link_like(path: Path) -> bool:
    """Detect symbolic links and Windows reparse points such as junctions."""
    if path.is_symlink():
        return True
    if os.name == "nt" and path.exists():
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
        return bool(attributes & 0x400)  # FILE_ATTRIBUTE_REPARSE_POINT
    return False


def first_link_like_component(path: Path) -> Path | None:
    """Return the first symlink/reparse point in an absolute lexical path."""
    absolute = path.expanduser().absolute()
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        if is_link_like(current):
            return current
    return None


def install(destination: Path, force: bool) -> None:
    if not (SOURCE_ROOT / "SKILL.md").is_file():
        raise SystemExit(f"invalid source package: {SOURCE_ROOT / 'SKILL.md'} is missing")
    if destination.name != SKILL_NAME:
        raise SystemExit(f"invalid destination name: expected {SKILL_NAME}, got {destination.name}")
    source_root = SOURCE_ROOT.resolve()
    resolved_destination = destination.resolve(strict=False)
    if (
        destination == SOURCE_ROOT
        or SOURCE_ROOT in destination.parents
        or resolved_destination == source_root
        or source_root in resolved_destination.parents
    ):
        raise SystemExit(
            "refusing to install inside the source repository; choose another --project-dir or --target"
        )
    linked_destination_component = first_link_like_component(destination)
    if linked_destination_component is not None:
        raise SystemExit(
            "refusing a destination whose path contains a symbolic link or reparse point: "
            f"{linked_destination_component}"
        )
    if destination.exists() and not destination.is_dir():
        raise SystemExit(f"destination exists but is not a directory: {destination}")
    if destination.exists() and not force:
        raise SystemExit(f"destination already exists: {destination}; rerun with --force to replace it")

    package_sources: list[tuple[str, Path]] = []
    for relative in PACKAGE_FILES:
        source = SOURCE_ROOT / relative
        linked_source_component = first_link_like_component(source)
        if linked_source_component is not None:
            raise SystemExit(
                "source package path contains a symbolic link or reparse point: "
                f"{linked_source_component}"
            )
        if not source.is_file():
            raise SystemExit(f"invalid source package file: {source}")
        resolved_source = source.resolve()
        if source_root not in resolved_source.parents:
            raise SystemExit(f"source package file escapes the repository: {source}")
        package_sources.append((relative, source))

    destination.parent.mkdir(parents=True, exist_ok=True)
    linked_destination_component = first_link_like_component(destination.parent)
    if linked_destination_component is not None:
        raise SystemExit(
            "refusing a destination whose path contains a symbolic link or reparse point: "
            f"{linked_destination_component}"
        )

    staged = Path(tempfile.mkdtemp(prefix=f".{SKILL_NAME}.staged-", dir=destination.parent))
    backup: Path | None = None
    try:
        for relative, source in package_sources:
            staged_file = staged / relative
            staged_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, staged_file)

        if destination.exists():
            backup = Path(tempfile.mkdtemp(prefix=f".{SKILL_NAME}.backup-", dir=destination.parent))
            backup.rmdir()
            destination.replace(backup)
        try:
            staged.replace(destination)
        except Exception:
            if backup is not None and backup.exists() and not destination.exists():
                backup.replace(destination)
            raise
        if backup is not None and backup.exists():
            shutil.rmtree(backup, ignore_errors=True)
    finally:
        if staged.exists():
            shutil.rmtree(staged, ignore_errors=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install pm-interview-transcript-review into a Codex skills directory"
    )
    parser.add_argument("--agent", choices=SUPPORTED_AGENTS, default="codex")
    parser.add_argument("--scope", choices=("user", "project"), default="user")
    parser.add_argument("--project-dir", help="project root for --scope project; defaults to current directory")
    parser.add_argument("--target", help="custom Skills root; overrides --agent and --scope")
    parser.add_argument("--force", action="store_true", help="replace an existing installation")
    parser.add_argument("--dry-run", action="store_true", help="print the destination without writing files")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        destination = resolve_destination(args)
    except ValueError as exc:
        parser.error(str(exc))
    if args.dry_run:
        print(destination)
        return
    install(destination, args.force)
    print(f"Installed {SKILL_NAME} to {destination}")
    print(f"Verified SKILL.md: {(destination / 'SKILL.md').is_file()}")


if __name__ == "__main__":
    main()
