#!/usr/bin/env python
"""Preflight checks for a personal Codex + Feishu administrator deployment."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from feishu_common import (
    FeishuAPI,
    FeishuAPIError,
    ConfigurationError,
    feishu_config,
    load_config,
    quote_path,
    require_feishu_credentials,
)


def result(name: str, ok: bool, detail: str, *, warning: bool = False) -> dict[str, Any]:
    return {"name": name, "ok": ok, "warning": warning, "detail": detail}


def personal_codex_env() -> dict[str, str]:
    env = os.environ.copy()
    for name in ("OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_API_BASE"):
        env.pop(name, None)
    return env


def command_output(command: list[str], *, env: dict[str, str] | None = None) -> tuple[int, str]:
    try:
        completed = subprocess.run(
            command,
            env=env,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=30,
            check=False,
        )
        return completed.returncode, completed.stdout.strip()
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 127, str(exc)


def run_checks(config_file: str | None, offline: bool) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    codex = shutil.which("codex")
    checks.append(result("codex_binary", bool(codex), codex or "codex not found on PATH"))
    if codex:
        code, output = command_output([codex, "--version"])
        checks.append(result("codex_version", code == 0, output or f"exit={code}"))
        code, output = command_output([codex, "login", "status"], env=personal_codex_env())
        chatgpt = code == 0 and "chatgpt" in output.lower()
        checks.append(
            result(
                "personal_codex_login",
                chatgpt,
                output or "run `codex login` and select your own ChatGPT account",
            )
        )
    api_key_present = bool(os.environ.get("OPENAI_API_KEY"))
    checks.append(
        result(
            "shared_openai_key_guard",
            True,
            "OPENAI_API_KEY is set but will be removed from the Codex child process"
            if api_key_present
            else "no OPENAI_API_KEY inherited",
            warning=api_key_present,
        )
    )

    for binary in ("ffmpeg", "ffprobe"):
        value = shutil.which(binary)
        checks.append(result(binary, bool(value), value or f"{binary} not found on PATH"))
    checks.append(
        result(
            "faster_whisper",
            importlib.util.find_spec("faster_whisper") is not None,
            "installed" if importlib.util.find_spec("faster_whisper") else "pip install faster-whisper",
        )
    )
    checks.append(
        result(
            "lark_channel_sdk",
            importlib.util.find_spec("lark_channel") is not None,
            "installed" if importlib.util.find_spec("lark_channel") else "pip install lark-channel-sdk",
        )
    )

    try:
        config = load_config(config_file)
        feishu = feishu_config(config)
        checks.append(result("configuration", True, "non-secret configuration loaded"))
    except (ConfigurationError, OSError, json.JSONDecodeError) as exc:
        checks.append(result("configuration", False, str(exc)))
        return checks

    try:
        app_id, app_secret = require_feishu_credentials()
        checks.append(result("feishu_credentials", True, f"app_id={app_id[:8]}...; secret is not printed"))
    except ConfigurationError as exc:
        checks.append(result("feishu_credentials", False, str(exc)))
        return checks

    if offline:
        checks.append(result("feishu_live_access", True, "skipped by --offline", warning=True))
        return checks

    try:
        api = FeishuAPI(app_id, app_secret)
        api.tenant_token()
        checks.append(result("feishu_tenant_token", True, "token acquired and redacted"))
        space_id = quote_path(str(feishu["space_id"]))
        response = api.request("GET", f"/wiki/v2/spaces/{space_id}/nodes?page_size=1")
        items = response.get("data", {}).get("items", [])
        checks.append(
            result(
                "fixed_wiki_read_access",
                True,
                f"space is readable; sampled_nodes={len(items)}",
            )
        )
    except FeishuAPIError as exc:
        suffix = f"; log_id={exc.log_id}" if exc.log_id else ""
        checks.append(result("feishu_live_access", False, f"{exc}{suffix}"))
    return checks


def main() -> None:
    parser = argparse.ArgumentParser(description="Check personal Codex and fixed Feishu Wiki access")
    parser.add_argument("--config")
    parser.add_argument("--offline", action="store_true", help="skip Feishu network calls")
    args = parser.parse_args()
    checks = run_checks(args.config, args.offline)
    failed = [x for x in checks if not x["ok"]]
    print(json.dumps({"status": "FAIL" if failed else "PASS", "checks": checks}, ensure_ascii=False, indent=2))
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
