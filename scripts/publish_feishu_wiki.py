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

from build_feishu_review import validate_feishu_review
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


def list_blocks(
    api: FeishuAPI,
    document_id: str,
    *,
    direct_children_only: bool = False,
) -> list[dict[str, Any]]:
    encoded = quote_path(document_id)
    items: list[dict[str, Any]] = []
    page_token = ""
    seen_tokens: set[str] = set()
    while True:
        if direct_children_only:
            path = (
                f"/docx/v1/documents/{encoded}/blocks/{encoded}/children"
                "?page_size=500&with_descendants=false"
            )
        else:
            path = f"/docx/v1/documents/{encoded}/blocks?page_size=50"
        if page_token:
            path += f"&page_token={quote_path(page_token)}"
        response = api.request("GET", path)
        data = response.get("data", {})
        items.extend(data.get("items", []))
        if not data.get("has_more"):
            break
        next_token = str(data.get("page_token", "")).strip()
        if not next_token or next_token in seen_tokens:
            raise FeishuAPIError("block-list pagination did not advance")
        seen_tokens.add(next_token)
        page_token = next_token
    return items


def delete_direct_children(
    api: FeishuAPI,
    document_id: str,
    *,
    batch_size: int = 50,
) -> int:
    """Delete only the document root's direct children, in tail-first batches."""
    if batch_size < 1 or batch_size > 50:
        raise ValueError("batch_size must be between 1 and 50")
    encoded = quote_path(document_id)
    remaining = len(list_blocks(api, document_id, direct_children_only=True))
    original = remaining
    while remaining:
        start = max(0, remaining - batch_size)
        api.request(
            "DELETE",
            (
                f"/docx/v1/documents/{encoded}/blocks/{encoded}/children/batch_delete"
                "?document_revision_id=-1"
            ),
            {"start_index": start, "end_index": remaining},
        )
        remaining = start
    if list_blocks(api, document_id, direct_children_only=True):
        raise FeishuAPIError("document still has root children after replacement delete")
    return original


def _text_runs(value: Any) -> list[str]:
    results: list[str] = []
    if isinstance(value, dict):
        text_run = value.get("text_run")
        if isinstance(text_run, dict) and isinstance(text_run.get("content"), str):
            results.append(text_run["content"])
        for child in value.values():
            results.extend(_text_runs(child))
    elif isinstance(value, list):
        for child in value:
            results.extend(_text_runs(child))
    return results


def _block_texts(blocks: list[dict[str, Any]]) -> list[str]:
    """Compare text per block; Feishu may split one submitted run into several runs."""
    return ["".join(_text_runs(block)) for block in blocks]


def verify_replacement(
    api: FeishuAPI,
    document_id: str,
    blocks: list[dict[str, Any]],
) -> int:
    actual = list_blocks(api, document_id)
    expected_count = len(blocks) + 1
    if len(actual) != expected_count:
        raise FeishuAPIError(
            "post-replacement verification block count differed: "
            f"expected {expected_count}, got {len(actual)}"
        )
    if _block_texts(actual[1:]) != _block_texts(blocks):
        raise FeishuAPIError("post-replacement verification text payload differed")
    return len(actual)


def replace_blocks(
    api: FeishuAPI,
    document_id: str,
    blocks: list[dict[str, Any]],
) -> tuple[int, int]:
    """Replace one existing document in place and verify its exact text payload."""
    removed = delete_direct_children(api, document_id)
    append_blocks(api, document_id, blocks)
    return removed, verify_replacement(api, document_id, blocks)


def verify_blocks(
    api: FeishuAPI,
    document_id: str,
    *,
    expected_content_blocks: int | None = None,
) -> int:
    total = len(list_blocks(api, document_id))
    if total <= 1:
        raise FeishuAPIError("post-write verification found no document content blocks")
    if expected_content_blocks is not None and total < expected_content_blocks + 1:
        raise FeishuAPIError(
            "post-write verification found fewer blocks than were written: "
            f"expected at least {expected_content_blocks + 1}, got {total}"
        )
    return total


def replace_existing(
    review: Path,
    title: str | None,
    *,
    manifest_path: Path,
    config_file: str | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Replace a previously published Wiki document while preserving its URL."""
    review = review.expanduser().resolve()
    content = review.read_text(encoding="utf-8-sig")
    errors = validate_feishu_review(content)
    if errors:
        raise ValueError("review validation failed: " + "; ".join(errors))
    blocks = markdown_to_blocks(content)
    if not blocks:
        raise ValueError("Markdown conversion produced no blocks")
    manifest_path = manifest_path.expanduser().resolve()
    existing = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    obj_token = str(existing.get("obj_token", "")).strip()
    node_token = str(existing.get("node_token", "")).strip()
    if not obj_token or not node_token:
        raise ValueError("existing manifest lacks obj_token or node_token")
    resolved_title = title or str(existing.get("title", "")).strip() or review.stem
    config = load_config(config_file)
    feishu = feishu_config(config)
    if str(existing.get("space_id", "")) != str(feishu["space_id"]):
        raise ValueError("existing manifest does not target the configured fixed Wiki")
    source_hash = sha256(review)
    if dry_run:
        return {
            "status": "dry-run-replace",
            "title": resolved_title,
            "source_sha256": source_hash,
            "block_count": len(blocks),
            "node_token": node_token,
            "obj_token": obj_token,
            "privacy_safe": True,
        }
    app_id, app_secret = require_feishu_credentials()
    # Destructive requests are deliberately not retried: an ambiguous retry could
    # remove a second batch after Feishu already applied the first request.
    api = FeishuAPI(app_id, app_secret, max_attempts=1)
    if existing.get("status") == "replacement-started":
        if existing.get("replacement_source_sha256") != source_hash:
            raise ValueError(
                "replacement-started manifest targets different content; inspect before retry"
            )
        verified_blocks = verify_replacement(api, obj_token, blocks)
        completed = {
            **existing,
            "status": "verified",
            "source": str(review),
            "source_sha256": source_hash,
            "title": resolved_title,
            "privacy_safe": True,
            "block_count": len(blocks),
            "verified_block_count": verified_blocks,
            "replaced_block_count": int(existing.get("block_count", 0)),
            "replacement_recovered": True,
            "verified_at": now_iso(),
        }
        atomic_json(manifest_path, completed)
        return completed
    started = {
        **existing,
        "status": "replacement-started",
        "replacement_source": str(review),
        "replacement_source_sha256": source_hash,
        "replacement_started_at": now_iso(),
    }
    atomic_json(manifest_path, started)
    removed, verified_blocks = replace_blocks(api, obj_token, blocks)
    completed = {
        **existing,
        "status": "verified",
        "source": str(review),
        "source_sha256": source_hash,
        "title": resolved_title,
        "privacy_safe": True,
        "block_count": len(blocks),
        "verified_block_count": verified_blocks,
        "replaced_block_count": removed,
        "verified_at": now_iso(),
    }
    atomic_json(manifest_path, completed)
    return completed


def publish(
    review: Path,
    title: str,
    *,
    config_file: str | None = None,
    manifest_path: Path | None = None,
    dry_run: bool = False,
    force_new: bool = False,
    privacy_safe: bool = True,
) -> dict[str, Any]:
    review = review.expanduser().resolve()
    content = review.read_text(encoding="utf-8-sig")
    if not privacy_safe:
        raise ValueError("private Full Reviews cannot be published to the organization Wiki")
    errors = validate_feishu_review(content)
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
            "privacy_safe": privacy_safe,
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
        "privacy_safe": privacy_safe,
    }
    atomic_json(manifest, partial)
    append_blocks(api, obj_token, blocks)
    verified_blocks = verify_blocks(
        api, obj_token, expected_content_blocks=len(blocks)
    )
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
    parser.add_argument(
        "--replace-existing",
        action="store_true",
        help="replace the document referenced by --manifest without changing its Wiki URL",
    )
    args = parser.parse_args()
    review = Path(args.review)
    if args.replace_existing:
        if not args.manifest:
            parser.error("--replace-existing requires --manifest")
        if args.force_new:
            parser.error("--replace-existing cannot be combined with --force-new")
        result = replace_existing(
            review,
            args.title,
            config_file=args.config,
            manifest_path=Path(args.manifest),
            dry_run=args.dry_run,
        )
    else:
        result = publish(
            review,
            args.title or review.stem,
            config_file=args.config,
            manifest_path=Path(args.manifest).expanduser() if args.manifest else None,
            dry_run=args.dry_run,
            force_new=args.force_new,
            privacy_safe=True,
        )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
