#!/usr/bin/env python
"""Render a Markdown review as a standalone local HTML file."""
from __future__ import annotations

import argparse
import os
from pathlib import Path


def as_path(value: str) -> Path:
    if os.name == "nt" and len(value) >= 3 and value[0] == "/" and value[1].isalpha() and value[2] == "/":
        value = f"{value[1].upper()}:{value[2:]}"
    return Path(value).expanduser()


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("markdown_file")
    p.add_argument("--output")
    args = p.parse_args()
    source = as_path(args.markdown_file).resolve()
    target = as_path(args.output).resolve() if args.output else source.with_suffix(".html")
    try:
        import markdown
    except ImportError as exc:
        raise SystemExit(f"Python package 'markdown' is required: {exc}")
    body = markdown.markdown(source.read_text(encoding="utf-8-sig"), extensions=["tables", "fenced_code", "toc"])
    html = f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{source.stem}</title><style>
:root{{--bg:#0b0d12;--card:#141824;--text:#e8ecf3;--muted:#9aa4b2;--gold:#f3c969;--line:#2a3242}}
body{{margin:0;background:var(--bg);color:var(--text);font:16px/1.7 system-ui,-apple-system,'Segoe UI','Microsoft YaHei',sans-serif}}
main{{max-width:1080px;margin:40px auto;padding:32px;background:var(--card);border:1px solid var(--line);border-radius:16px}}
h1,h2,h3{{line-height:1.3;color:#fff}}h1{{border-bottom:2px solid var(--gold);padding-bottom:.4em}}h2{{margin-top:2em;color:var(--gold)}}
table{{border-collapse:collapse;width:100%;display:block;overflow:auto}}th,td{{border:1px solid var(--line);padding:8px 10px;vertical-align:top}}th{{background:#202637}}
blockquote{{margin-left:0;padding:.5em 1em;border-left:4px solid var(--gold);background:#10141d}}code{{background:#202637;padding:.15em .35em;border-radius:4px}}pre{{overflow:auto;background:#090b10;padding:16px;border-radius:8px}}a{{color:#8ec5ff}}.meta{{color:var(--muted);font-size:14px}}
</style></head><body><main><div class="meta">Local PM Interview Review OS export</div>{body}</main></body></html>"""
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
