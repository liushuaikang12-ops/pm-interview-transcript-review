#!/usr/bin/env python
"""Publish a validated Markdown interview review to a fixed Feishu Wiki."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from feishu_common import (
    FeishuAPI,
    FeishuAPIError,
    atomic_json,
    feishu_config,
    load_config,
    quote_path,
    require_feishu_credentials,
    wiki_url,
)
from validate_review import validate

BLOCK_TYPES = {
    "text": 2,
    "heading1": 3,
    "heading2": 4,
    "heading3": 5,
    "heading4": 6,
    "heading5": 7,
    "heading6": 8,
    "bullet": 12,
    "ordered": 13,
    "code": 14,
    "quote": 15,
    "divider": 22,
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def chunks(value: str, limit: int = 1500) -> Iterable[str]:
    value = value.strip("\n")
    if not value:
        return
    for start in range(0, len(value), limit):
        yield value[start : start + limit]


def text_block(kind: str, content: str) -> dict[str, Any]:
    if kind == "divider":
        return {"block_type": BLOCK_TYPES[kind], "divider": {}}
    return {
        "block_type": BLOCK_TYPES[kind],
        kind: {
            "elements": [
                {
                    "text_run": {
                        "content": content,
                        "text_element_style": {},
                    }
                }
            ]
        },
    }


def markdown_to_blocks(markdown: str) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    paragraph: list[str] = []
    code: list[str] = []
    in_code = False

    def flush_paragraph() -> None:
        if not paragraph:
            return
        content = "\n".join(paragraph).strip()
        paragraph.clear()
        for part in chunks(content):
            blocks.append(text_block("text", part))

    def flush_code() -> None:
        content = "\n".join(code).rstrip()
        code.clear()
        for part in chunks(content):
            blocks.append(text_block("code", part))

    for raw in markdown.splitlines():
        line = raw.rstrip()
        if line.strip().startswith("```"):
            flush_paragraph()
            if in_code:
                flush_code()
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code.append(line)
            continue
        if not line.strip():
            flush_paragraph()
            continue
        if re.fullmatch(r"\s*(---+|___+|\*\*\*+)\s*", line):
            flush_paragraph()
            blocks.append(text_block("divider", ""))
            continue
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            flush_paragraph()
            kind = f"heading{len(heading.group(1))}"
            for part in chunks(heading.group(2)):
                blocks.append(text_block(kind, part))
            continue
        bullet = re.match(r"^\s*[-*+]\s+(.+)$", line)
        if bullet:
            flush_paragraph()
            for part in chunks(bullet.group(1)):
                blocks.append(text_block("bullet", part))
            continue
        ordered = re.match(r"^\s*\d+[.)、]\s+(.+)$", line)
        if ordered:
            flush_paragraph()
            for part in chunks(ordered.group(1)):
                blocks.append(text_block("ordered", part))
            continue
        quote = re.match(r"^\s*>\s?(.*)$", line)
        if quote:
            flush_paragraph()
            for part in chunks(quote.group(1)):
                blocks.append(text_block("quote", part))
            continue
        if line.lstrip().startswith("|") and line.rstrip().endswith("|"):
            flush_paragraph()
            blocks.append(text_block("code", line))
            continue
        paragraph.append(line)
    flush_paragraph()
    if in_code:
        flush_code()
    return blocks


def create_wiki_node(api: FeishuAPI, config: dict[str, Any], title: str) -> tuple[str, str]:
    space_id = str(config["space_id"])
    body: dict[str, Any] = {
        "obj_type": "docx",
        "node_type": "origin",
        "title": title[:255],
    }
    parent = str(config.get("parent_node_token", "")).strip()
    if parent:
        body["parent_node_token"] = parent
    response = api.request(
        "POST", f"/wiki/v2/spaces/{quote_path(space_id)}/nodes", body
    )
    node = response.get("data", {}).get("node") or response.get("data", {})
    node_token = str(node.get("node_token", "")).strip()
    obj_token = str(node.get("obj_token", "")).strip()
    if not node_token or not obj_token:
        raise FeishuAPIError("create Wiki node response lacked node_token or obj_token")
    return node_token, obj_token


def append_blocks(api: FeishuAPI, document_id: str, blocks: list[dict[str, Any]]) -> None:
    encoded = quote_path(document_id)
    for start in range(0, len(blocks), 50):
        api.request(
            "POST",
            f"/docx/v1/documents/{encoded}/blocks/{encoded}/children",
            {"children": blocks[start : start + 50], "index": -1},
        )


def verify_blocks(api: FeishuAPI, document_id: str) -> int:
    encoded = quote_path(document_id)
    response = api.request(
        "GET", f"/docx/v1/documents/{encoded}/blocks?page_size=50"
    )
    items = response.get("data", {}).get("items", [])
    if len(items) <= 1:
        raise FeishuAPIError("post-write verification found no document content blocks")
    return len(items)


def publish(
    review: Path,
    title: str,
    *,
    config_file: str | None = None,
    manifest_path: Path | None = None,
    dry_run: bool = False,
    force_new: bool = False,
) -> dict[str, Any]:
    review = review.expanduser().resolve()
    content = review.read_text(encoding="utf-8-sig")
    errors = validate(content, automated=True)
    if errors:
        raise ValueError("review validation failed: " + "; ".join(errors))
    blocks = markdown_to_blocks(content)
    if not blocks:
        raise ValueError("Markdown conversion produced no blocks")
    source_hash = sha256(review)
    manifest = manifest_path or review.with_suffix(".feishu-manifest.json")
    if manifest.exists() and not force_new:
        existing = json.loads(manifest.read_text(encoding="utf-8-sig"))
        if existing.get("source_sha256") == source_hash and existing.get("status") == "verified":
            return existing
        raise RuntimeError(
            f"publication manifest already exists: {manifest}; use --force-new only after reviewing it"
        )
    if dry_run:
        return {
            "status": "dry-run",
            "title": title,
            "source_sha256": source_hash,
            "block_count": len(blocks),
        }
    config = load_config(config_file)
    feishu = feishu_config(config)
    app_id, app_secret = require_feishu_credentials()
    api = FeishuAPI(app_id, app_secret)
    node_token, obj_token = create_wiki_node(api, feishu, title)
    partial = {
        "status": "node-created",
        "source": str(review),
        "source_sha256": source_hash,
        "title": title,
        "space_id": feishu["space_id"],
        "node_token": node_token,
        "obj_token": obj_token,
        "url": wiki_url(str(feishu["tenant_domain"]), node_token),
        "created_at": now_iso(),
    }
    atomic_json(manifest, partial)
    append_blocks(api, obj_token, blocks)
    verified_blocks = verify_blocks(api, obj_token)
    completed = {
        **partial,
        "status": "verified",
        "block_count": len(blocks),
        "verified_block_count": verified_blocks,
        "verified_at": now_iso(),
    }
    atomic_json(manifest, completed)
    return completed


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish a verified interview review to Feishu Wiki")
    parser.add_argument("review")
    parser.add_argument("--title")
    parser.add_argument("--config")
    parser.add_argument("--manifest")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force-new", action="store_true")
    args = parser.parse_args()
    review = Path(args.review)
    title = args.title or review.stem
    result = publish(
        review,
        title,
        config_file=args.config,
        manifest_path=Path(args.manifest).expanduser() if args.manifest else None,
        dry_run=args.dry_run,
        force_new=args.force_new,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
