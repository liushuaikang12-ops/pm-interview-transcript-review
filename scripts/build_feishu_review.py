#!/usr/bin/env python
"""Build the privacy-safe Feishu edition from a private Full Review."""
from __future__ import annotations

import argparse
import re
from pathlib import Path


PRIVACY_NOTICE = (
    "> 隐私说明：本知识库版本仅在第 1 节移除候选人原回复及回答定位；"
    "回答建议、反问以及后续 16 章完整复盘均保留。"
)

QUESTION_HEADING = re.compile(
    r"^(#{3,6})\s+((?:Q|A)\d+(?:\.\d+)*)"
    r"(?:\s*[·—-]\s*|\s+)?(.*?)\s*$",
    flags=re.IGNORECASE,
)
GENERIC_TITLES = {
    "",
    "root",
    "follow-up",
    "follow up",
    "followup",
    "administrative",
    "question",
    "根问题",
    "追问",
    "流程问题",
    "回答建议",
}
ANSWER_BOUNDARY = re.compile(
    r"^(?:[-*]\s*)?(?:回答\s*(?:anchor|时间)|answer\s*anchor|状态|"
    r"speaker\s*[:：]\s*candidate|候选人原回复)",
    flags=re.IGNORECASE,
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


def _tail(lines: list[str], start_pattern: str) -> list[str]:
    start = next(
        (index for index, line in enumerate(lines) if re.match(start_pattern, line.strip())),
        None,
    )
    if start is None:
        raise ValueError(f"private review is missing section: {start_pattern}")
    return lines[start:]


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


def _clean_quote(line: str) -> str:
    value = re.sub(r"^\s*>\s?", "", line).strip()
    value = re.sub(r"^\[[^\]]+\]\s*", "", value)
    return value


def _question_excerpt(lines: list[str], *, limit: int = 42) -> str:
    """Return a deterministic, evidence-only title from the question block."""
    quotes: list[str] = []
    for line in lines:
        stripped = line.strip()
        if ANSWER_BOUNDARY.match(stripped):
            break
        if stripped.startswith(">"):
            value = _clean_quote(stripped)
            if value:
                quotes.append(value)
            continue
        inline = re.match(
            r"^(?:[-*]\s*)?(?:\*\*)?面试官原文(?:\*\*)?\s*[:：]\s*(.+)$",
            stripped,
        )
        if inline:
            quotes.append(inline.group(1).strip())
    text = re.sub(r"\s+", " ", " ".join(quotes)).strip()
    text = re.sub(
        r"^(?:(?:那|然后|所以|就是|嗯|好的|ok|OK)[，,。.!！?？\s]*)+",
        "",
        text,
    ).strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip("，,。.!！?？；;：: ") + "…"


def normalize_question_headings(markdown: str) -> str:
    """Replace structural Q/A headings with stable titles grounded in question text."""
    lines = markdown.replace("\r\n", "\n").replace("\r", "\n").splitlines()
    titles: dict[str, str] = {}

    for index, line in enumerate(lines):
        match = QUESTION_HEADING.match(line.strip())
        if not match:
            continue
        level, question_id, current = match.groups()
        question_id = question_id.upper()
        current = current.strip()
        if current.casefold() not in GENERIC_TITLES:
            titles.setdefault(question_id, current)
            continue
        end = next(
            (
                candidate
                for candidate in range(index + 1, len(lines))
                if re.match(r"^#{1,6}\s+", lines[candidate].strip())
            ),
            len(lines),
        )
        excerpt = _question_excerpt(lines[index + 1 : end])
        if excerpt:
            titles.setdefault(question_id, excerpt)

    for index, line in enumerate(lines):
        match = QUESTION_HEADING.match(line.strip())
        if not match:
            continue
        level, question_id, current = match.groups()
        question_id = question_id.upper()
        current = current.strip()
        if current.casefold() in GENERIC_TITLES and question_id in titles:
            lines[index] = f"{level} {question_id} — {titles[question_id]}"

    return "\n".join(lines).strip() + "\n"


def build_feishu_review(private_markdown: str) -> str:
    normalized = normalize_question_headings(private_markdown)
    lines = normalized.splitlines()
    questions = _section(lines, r"^##\s+0\.1\b", r"^##\s+0\.2\b")
    suggestions = _section(lines, r"^##\s+0\.2\b", r"^##\s+0\.3\b")
    chapter_one = r"^#{1,3}\s+1[.、]\s*"
    reverse = _section(lines, r"^##\s+0\.3\b", chapter_one)
    diagnostics = _tail(lines, chapter_one)
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
        "",
        *diagnostics,
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
    for number in range(1, 17):
        if not re.search(rf"^#{{1,3}}\s+{number}[.、]\s*", text, flags=re.MULTILINE):
            errors.append(f"missing numbered Full Review chapter {number}")
    lines = text.replace("\r\n", "\n").replace("\r", "\n").splitlines()
    try:
        question_section = "\n".join(
            _section(lines, r"^##\s+1\.\s+面试官问题与追问", r"^##\s+2\.")
        )
    except ValueError as exc:
        errors.append(str(exc))
        question_section = ""
    forbidden = (
        r"候选人原回复",
        r"candidate answer",
        r"(?m)^\s*[-*]\s*回答\s*(?:anchor|时间)",
        r"speaker\s*[:：]\s*candidate",
    )
    for pattern in forbidden:
        if re.search(pattern, question_section, flags=re.IGNORECASE):
            errors.append(f"privacy-forbidden content remains in question transcript: {pattern}")
    for line in text.splitlines():
        match = QUESTION_HEADING.match(line.strip())
        if not match:
            continue
        _level, question_id, title = match.groups()
        if title.strip().casefold() in GENERIC_TITLES:
            errors.append(f"question heading lacks a meaningful title: {question_id.upper()}")
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
