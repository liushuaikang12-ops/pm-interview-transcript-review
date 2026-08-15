#!/usr/bin/env python
"""Install this repository as an Agent Skill without third-party dependencies."""
from __future__ import annotations

import argparse
import os
import shutil
import tempfile
from pathlib import Path

SKILL_NAME = "pm-interview-transcript-review"
SOURCE_ROOT = Path(__file__).resolve().parents[1]
SUPPORTED_AGENTS = (
    "universal",
    "codex",
    "claude",
    "cursor",
    "gemini",
    "opencode",
    "copilot",
    "vscode",
    "hermes",
)
PACKAGE_FILES = (
    "SKILL.md",
    "README.md",
    "LICENSE",
    "scripts/install_skill.py",
    "scripts/interview_os.py",
    "scripts/transcribe_media.py",
    "scripts/render_review.py",
    "scripts/validate_skill.py",
    "templates/full-review.md",
    "templates/interview-record.schema.json",
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
    if agent in {"universal", "codex", "copilot", "vscode"}:
        return home / ".agents" / "skills"
    if agent == "claude":
        return home / ".claude" / "skills"
    if agent == "cursor":
        return home / ".cursor" / "skills"
    if agent == "gemini":
        return home / ".gemini" / "skills"
    if agent == "opencode":
        config = Path(os.environ.get("XDG_CONFIG_HOME", home / ".config"))
        return config / "opencode" / "skills"
    if agent == "hermes":
        return Path(os.environ.get("HERMES_HOME", home / ".hermes")) / "skills"
    raise ValueError(f"unsupported agent: {agent}")


def project_root(agent: str, project_dir: Path) -> Path:
    if agent in {"universal", "codex", "copilot", "vscode"}:
        return project_dir / ".agents" / "skills"
    if agent == "claude":
        return project_dir / ".claude" / "skills"
    if agent == "cursor":
        return project_dir / ".cursor" / "skills"
    if agent == "gemini":
        return project_dir / ".gemini" / "skills"
    if agent == "opencode":
        return project_dir / ".opencode" / "skills"
    if agent == "hermes":
        raise ValueError("Hermes project-scope discovery is not assumed; use --scope user or --target")
    raise ValueError(f"unsupported agent: {agent}")


def resolve_destination(args: argparse.Namespace) -> Path:
    if args.target:
        return Path(args.target).expanduser().resolve() / SKILL_NAME
    if args.scope == "user":
        root = user_root(args.agent)
    else:
        project_dir = Path(args.project_dir or Path.cwd()).expanduser().resolve()
        root = project_root(args.agent, project_dir)
    return root.expanduser().resolve() / SKILL_NAME


def is_link_like(path: Path) -> bool:
    """Detect symbolic links and Windows reparse points such as junctions."""
    if path.is_symlink():
        return True
    if os.name == "nt" and path.exists():
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
        return bool(attributes & 0x400)  # FILE_ATTRIBUTE_REPARSE_POINT
    return False


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
    if is_link_like(destination):
        raise SystemExit(f"refusing to replace a symbolic-link or reparse-point destination: {destination}")
    if destination.exists() and not destination.is_dir():
        raise SystemExit(f"destination exists but is not a directory: {destination}")
    if destination.exists() and not force:
        raise SystemExit(f"destination already exists: {destination}; rerun with --force to replace it")

    package_sources: list[tuple[str, Path]] = []
    for relative in PACKAGE_FILES:
        source = SOURCE_ROOT / relative
        if is_link_like(source) or not source.is_file():
            raise SystemExit(f"invalid source package file: {source}")
        resolved_source = source.resolve()
        if source_root not in resolved_source.parents:
            raise SystemExit(f"source package file escapes the repository: {source}")
        package_sources.append((relative, source))

    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f"{SKILL_NAME}-") as temporary:
        staged = Path(temporary) / SKILL_NAME
        staged.mkdir()
        for relative, source in package_sources:
            staged_file = staged / relative
            staged_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, staged_file)
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(staged, destination)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install pm-interview-transcript-review into an Agent Skills directory"
    )
    parser.add_argument("--agent", choices=SUPPORTED_AGENTS, default="universal")
    parser.add_argument("--scope", choices=("user", "project"), default="user")
    parser.add_argument("--project-dir", help="project root for --scope project; defaults to current directory")
    parser.add_argument("--target", help="custom Skills root; overrides --agent and --scope")
    parser.add_argument("--force", action="store_true", help="replace an existing installation")
    parser.add_argument("--dry-run", action="store_true", help="print the destination without writing files")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    destination = resolve_destination(args)
    if args.dry_run:
        print(destination)
        return
    install(destination, args.force)
    print(f"Installed {SKILL_NAME} to {destination}")
    print(f"Verified SKILL.md: {(destination / 'SKILL.md').is_file()}")


if __name__ == "__main__":
    main()
