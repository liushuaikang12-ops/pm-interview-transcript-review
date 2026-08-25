#!/usr/bin/env python
"""Build the privacy-safe Feishu edition from a private Full Review."""
from __future__ import annotations

import argparse
import re
from pathlib import Path


PRIVACY_NOTICE = (
    "> 隐私说明：本知识库版本不包含候选人的回答内容与相关定位信息，也不包含评分、"
    "表现诊断、短板或反模式；完整复盘仅保存在提交者本机。"
)


def _section(lines: list[str], start_pattern: str, end_pattern: str | None) -> list[str]:
    start = next(
        (index for index, line in enumerate(lines) if re.match(start_pattern, line.strip())),
        None,
    )
    if start is None:
        raise ValueError(f"private review is missing section: {start_pattern}")
    end = len(lines)
    if end_pattern is not None:
        end = next(
            (
                index
                for index in range(start + 1, len(lines))
                if re.match(end_pattern, lines[index].strip())
            ),
            len(lines),
        )
    return lines[start + 1 : end]


def _question_only(lines: list[str]) -> list[str]:
    output: list[str] = []
    suppress_answer = False
    for line in lines:
        if re.match(r"^#{3,6}\s+", line.strip()):
            suppress_answer = False
            output.append(line)
            continue
        stripped = line.strip()
        answer_boundary = bool(
            re.match(
                r"^[-*]\s*(?:回答\s*(?:anchor|时间)|answer\s*anchor|状态|"
                r"speaker\s*[:：]\s*candidate|候选人原回复)",
                stripped,
                flags=re.IGNORECASE,
            )
            or re.match(
                r"^(?:\*\*)?(?:候选人原回复|candidate answer)(?:\*\*)?\s*[:：]?$",
                stripped,
                flags=re.IGNORECASE,
            )
        )
        if answer_boundary:
            suppress_answer = True
            continue
        if not suppress_answer:
            output.append(line)
    return output


def build_feishu_review(private_markdown: str) -> str:
    lines = private_markdown.replace("\r\n", "\n").replace("\r", "\n").splitlines()
    questions = _section(lines, r"^##\s+0\.1\b", r"^##\s+0\.2\b")
    suggestions = _section(lines, r"^##\s+0\.2\b", r"^##\s+0\.3\b")
    reverse = _section(lines, r"^##\s+0\.3\b", r"^#\s+1\.")
    sections = [
        "# 面试问题与回答建议（知识库脱敏版）",
        "",
        PRIVACY_NOTICE,
        "",
        "## 1. 面试官问题与追问",
        *_question_only(questions),
        "",
        "## 2. 回答建议",
        *suggestions,
        "",
        "## 3. 候选人反问与面试官回答原文",
        *reverse,
    ]
    result = "\n".join(sections).strip() + "\n"
    errors = validate_feishu_review(result)
    if errors:
        raise ValueError("privacy-safe Feishu review validation failed: " + "; ".join(errors))
    return result


def validate_feishu_review(text: str) -> list[str]:
    errors: list[str] = []
    required = (
        "知识库脱敏版",
        "## 1. 面试官问题与追问",
        "## 2. 回答建议",
        "## 3. 候选人反问与面试官回答原文",
    )
    for marker in required:
        if marker not in text:
            errors.append(f"missing required marker: {marker}")
    forbidden = (
        r"候选人原回复",
        r"candidate answer",
        r"(?m)^\s*[-*]\s*回答\s*(?:anchor|时间)",
        r"speaker\s*[:：]\s*candidate",
        r"clean version",
        r"raw evidence",
        r"key answer reviews",
        r"shortcoming cards",
        r"anti-patterns",
        r"overall performance",
    )
    for pattern in forbidden:
        if re.search(pattern, text, flags=re.IGNORECASE):
            errors.append(f"privacy-forbidden content remains: {pattern}")
    if re.search(r"^#\s+(?:[1-9]|1[0-6])\.", text, flags=re.MULTILINE):
        errors.append("private diagnostic chapters remain in Feishu edition")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a privacy-safe Feishu interview review")
    parser.add_argument("private_review")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    source = Path(args.private_review).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        build_feishu_review(source.read_text(encoding="utf-8-sig")),
        encoding="utf-8",
    )
    print(output)


if __name__ == "__main__":
    main()
