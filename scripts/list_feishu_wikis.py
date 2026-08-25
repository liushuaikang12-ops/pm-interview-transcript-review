#!/usr/bin/env python3
"""List Feishu Wiki spaces visible to the configured application."""

from __future__ import annotations

import json

from feishu_common import FeishuAPI, require_feishu_credentials


def main() -> None:
    api = FeishuAPI(*require_feishu_credentials())
    response = api.request("GET", "/wiki/v2/spaces?page_size=50")
    spaces = []
    for item in response.get("data", {}).get("items", []):
        spaces.append(
            {
                "space_id": item.get("space_id"),
                "name": item.get("name"),
                "description": item.get("description"),
                "visibility": item.get("visibility"),
            }
        )
    print(json.dumps({"count": len(spaces), "spaces": spaces}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
