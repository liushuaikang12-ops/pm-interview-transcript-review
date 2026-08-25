#!/usr/bin/env python
"""Create the per-user non-secret Codex + Feishu automation configuration."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from feishu_common import (
    FIXED_TENANT_DOMAIN,
    FIXED_WIKI_SPACE_ID,
    atomic_json,
    config_path,
    load_config,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Configure a personal Codex runner that publishes to the organization Wiki"
    )
    parser.add_argument(
        "--space-id", default=FIXED_WIKI_SPACE_ID, help="fixed organization Wiki space_id"
    )
    parser.add_argument("--parent-node-token", default="", help="fixed Wiki parent node")
    parser.add_argument(
        "--tenant-domain", default=FIXED_TENANT_DOMAIN, help="fixed organization Feishu domain"
    )
    parser.add_argument("--chat-id", action="append", default=[], help="allowed group chat_id; repeatable")
    parser.add_argument("--disable-dm", action="store_true", help="reject direct messages")
    parser.add_argument("--config", help="configuration destination")
    parser.add_argument("--print", action="store_true", dest="print_config")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.tenant_domain.strip() != FIXED_TENANT_DOMAIN:
        raise SystemExit(f"tenant domain is fixed to {FIXED_TENANT_DOMAIN}")
    if args.space_id.strip() != FIXED_WIKI_SPACE_ID:
        raise SystemExit(f"Wiki space is fixed to {FIXED_WIKI_SPACE_ID}")
    destination = config_path(args.config)
    existing = load_config(destination) if destination.exists() else {}
    config = {
        **existing,
        "schema_version": "2.0",
        "codex": {
            "auth_mode": "chatgpt",
            "require_personal_login": True,
            "strip_api_key_from_child": True,
        },
        "feishu": {
            "tenant_domain": args.tenant_domain.strip(),
            "space_id": args.space_id.strip(),
            "parent_node_token": args.parent_node_token.strip(),
            "allowed_chat_ids": sorted(set(x.strip() for x in args.chat_id if x.strip())),
            "dm_enabled": not args.disable_dm,
            "auto_publish": True,
            "include_raw_audio": False,
        },
    }
    atomic_json(destination, config)
    print(f"Wrote non-secret configuration: {destination}")
    print("Set FEISHU_APP_ID and FEISHU_APP_SECRET in this user's environment.")
    print("Next: python scripts/doctor.py")
    if args.print_config:
        print(json.dumps(config, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
