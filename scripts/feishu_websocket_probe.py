#!/usr/bin/env python3
"""Open a Feishu WebSocket connection for first-use console verification."""

from __future__ import annotations

import os

from lark_channel import FeishuChannel


def credential(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if value or os.name != "nt":
        return value

    import winreg

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            stored, _ = winreg.QueryValueEx(key, name)
    except FileNotFoundError:
        return ""
    return str(stored).strip()


def main() -> None:
    app_id = credential("FEISHU_APP_ID")
    app_secret = credential("FEISHU_APP_SECRET")
    if not app_id or not app_secret:
        raise SystemExit("FEISHU_APP_ID and FEISHU_APP_SECRET must be configured.")

    print(f"Opening Feishu WebSocket for App ID {app_id}...")
    channel = FeishuChannel(app_id=app_id, app_secret=app_secret)
    channel.start()


if __name__ == "__main__":
    main()
