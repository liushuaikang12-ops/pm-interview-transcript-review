#!/usr/bin/env python
"""Per-user Feishu bot bridge that spends the current user's Codex quota."""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from feishu_common import (
    ConfigurationError,
    feishu_config,
    load_config,
    require_feishu_credentials,
    runtime_home,
)
from publish_feishu_wiki import publish
from validate_review import validate

MEDIA_SUFFIXES = {".mp3", ".m4a", ".wav", ".ogg", ".aac", ".flac", ".mp4", ".mov", ".mkv", ".webm"}
TEXT_SUFFIXES = {".md", ".txt", ".vtt", ".srt"}


def personal_codex_env() -> dict[str, str]:
    env = os.environ.copy()
    for name in ("OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_API_BASE"):
        env.pop(name, None)
    return env


def ensure_personal_codex() -> str:
    codex = shutil.which("codex")
    if not codex:
        raise ConfigurationError("codex not found on PATH")
    completed = subprocess.run(
        [codex, "login", "status"],
        env=personal_codex_env(),
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=30,
        check=False,
    )
    if completed.returncode != 0 or "chatgpt" not in completed.stdout.lower():
        raise ConfigurationError(
            "this Windows/macOS/Linux user must run `codex login` with their own ChatGPT account"
        )
    return codex


def safe_name(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in ".-_" else "_" for ch in value)
    return cleaned.strip("._")[:120] or "recording"


def job_id(message_id: str, file_key: str) -> str:
    return hashlib.sha256(f"{message_id}:{file_key}".encode("utf-8")).hexdigest()[:16]


def run_checked(
    command: list[str],
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
    timeout_seconds: int = 4 * 60 * 60,
) -> None:
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            env=env,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            f"command timed out after {timeout_seconds}s: {' '.join(command[:3])}"
        ) from exc
    if completed.returncode != 0:
        tail = completed.stdout[-4000:]
        raise RuntimeError(f"command failed ({completed.returncode}): {' '.join(command[:3])}\n{tail}")


def process_downloaded(
    source: Path,
    *,
    job_dir: Path,
    codex: str,
    config_file: str | None,
    title: str,
) -> dict[str, Any]:
    scripts = Path(__file__).resolve().parent
    transcript_dir = job_dir / "transcript"
    if source.suffix.lower() in TEXT_SUFFIXES:
        transcript = source
    else:
        run_checked(
            [
                sys.executable,
                str(scripts / "transcribe_media.py"),
                str(source),
                "--output-dir",
                str(transcript_dir),
                "--language",
                "zh",
            ],
            cwd=job_dir,
        )
        transcript = transcript_dir / "transcript.md"
    review = job_dir / "review.md"
    last_message = job_dir / "codex-last-message.txt"
    prompt = (
        "Use $pm-interview-transcript-review to complete an automated Full Review. "
        f"The transcript is at {transcript}. Write the complete Markdown report to {review}. "
        "The report must begin with the interviewer's original questions, follow-ups, candidate replies, "
        "and evidence-grounded answer suggestions; preserve candidate reverse questions and the interviewer's "
        "original replies when present; then include all numbered 16 Full Review chapters. "
        "Do not invent missing facts. Do not publish externally yourself. "
        "Finish only after the file exists and you have checked its structure."
    )
    run_checked(
        [
            codex,
            "exec",
            "--ephemeral",
            "--sandbox",
            "workspace-write",
            "--skip-git-repo-check",
            "-C",
            str(job_dir),
            "--output-last-message",
            str(last_message),
            prompt,
        ],
        cwd=job_dir,
        env=personal_codex_env(),
    )
    if not review.exists():
        raise RuntimeError("Codex completed without creating review.md")
    errors = validate(review.read_text(encoding="utf-8-sig"), automated=True)
    if errors:
        raise RuntimeError("generated review failed validation: " + "; ".join(errors))
    return publish(
        review,
        title,
        config_file=config_file,
        manifest_path=job_dir / "publication.json",
    )


async def run_bridge(config_file: str | None) -> None:
    try:
        from lark_channel import FeishuChannel, PolicyConfig
    except ImportError as exc:
        raise ConfigurationError("lark-channel-sdk is not installed") from exc

    config = load_config(config_file)
    feishu = feishu_config(config)
    app_id, app_secret = require_feishu_credentials()
    codex = ensure_personal_codex()
    allowed_chats = [str(x) for x in feishu.get("allowed_chat_ids", []) if str(x)]
    policy = PolicyConfig(
        dm_policy="open" if feishu.get("dm_enabled", True) else "disabled",
        group_policy="allowlist" if allowed_chats else "disabled",
        group_allowlist=allowed_chats or None,
        require_mention=False,
    )
    channel = FeishuChannel(app_id=app_id, app_secret=app_secret, policy=policy)
    active: set[asyncio.Task[Any]] = set()
    inflight: set[str] = set()

    async def process_resource(message: Any, resource: Any) -> None:
        identifier = job_id(message.message_id, resource.file_key)
        if identifier in inflight:
            await channel.send(
                message.chat_id,
                {"text": f"任务 {identifier} 已在处理中，请勿重复发送。"},
                {"reply_to": message.message_id},
            )
            return
        inflight.add(identifier)
        try:
            folder = runtime_home() / "jobs" / identifier
            folder.mkdir(parents=True, exist_ok=True)
            manifest = folder / "publication.json"
            if manifest.exists():
                existing = json.loads(manifest.read_text(encoding="utf-8-sig"))
                if existing.get("status") == "verified":
                    await channel.send(
                        message.chat_id,
                        {"markdown": f"这条录音已经处理完成：{existing.get('url', '')}"},
                        {"reply_to": message.message_id},
                    )
                    return
            await channel.send(
                message.chat_id,
                {"markdown": f"已接收录音，任务 `{identifier}` 正在转写和复盘。"},
                {"reply_to": message.message_id},
            )
            file_name = resource.file_name or {
                "audio": "recording.ogg",
                "video": "recording.mp4",
                "file": "recording.bin",
            }[resource.type]
            file_name = safe_name(file_name)
            suffix = Path(file_name).suffix.lower()
            if suffix not in MEDIA_SUFFIXES | TEXT_SUFFIXES:
                await channel.send(
                    message.chat_id,
                    {"text": f"不支持的附件格式：{suffix or 'unknown'}"},
                    {"reply_to": message.message_id},
                )
                return
            source = await channel.download_resource_to_file(
                resource.file_key,
                resource_type=resource.type,
                message_id=message.message_id,
                dest_dir=folder,
                file_name=file_name,
            )
            title = f"{datetime.now().strftime('%Y-%m-%d')} 面试复盘 - {Path(file_name).stem}"
            published = await asyncio.to_thread(
                process_downloaded,
                Path(source),
                job_dir=folder,
                codex=codex,
                config_file=config_file,
                title=title,
            )
            await channel.send(
                message.chat_id,
                {"markdown": f"复盘完成并已验证归档：[{title}]({published['url']})"},
                {"reply_to": message.message_id},
            )
        except Exception as exc:
            folder = runtime_home() / "jobs" / identifier
            folder.mkdir(parents=True, exist_ok=True)
            failure = {"status": "failed", "job_id": identifier, "error": str(exc)[:2000]}
            (folder / "failure.json").write_text(
                json.dumps(failure, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            await channel.send(
                message.chat_id,
                {"text": f"任务 {identifier} 失败：{str(exc)[:800]}"},
                {"reply_to": message.message_id},
            )
        finally:
            inflight.discard(identifier)

    async def process_message(message: Any) -> None:
        resources = [
            item
            for item in message.resources
            if item.type in {"audio", "video", "file"}
        ]
        for resource in resources:
            await process_resource(message, resource)

    async def on_message(message: Any) -> None:
        task = asyncio.create_task(process_message(message))
        active.add(task)
        task.add_done_callback(active.discard)

    channel.on("message", on_message)
    print("Codex Feishu bridge starting with personal ChatGPT login; secrets are redacted.")
    await channel.connect()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the personal Codex Feishu recording bridge")
    parser.add_argument("--config")
    args = parser.parse_args()
    try:
        asyncio.run(run_bridge(args.config))
    except (ConfigurationError, KeyboardInterrupt) as exc:
        if isinstance(exc, ConfigurationError):
            print(f"configuration error: {exc}", file=sys.stderr)
            raise SystemExit(2)


if __name__ == "__main__":
    main()
