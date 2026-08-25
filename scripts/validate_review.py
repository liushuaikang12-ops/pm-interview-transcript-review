#!/usr/bin/env python
"""Validate observable structure before an automated Feishu publication."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def validate(text: str, *, automated: bool = False) -> list[str]:
    errors: list[str] = []
    if len(text.strip()) < 1000:
        errors.append("review is unexpectedly short")
    for number in range(1, 17):
        if not re.search(rf"^#{{1,3}}\s+{number}[.、]\s*", text, flags=re.M):
            errors.append(f"missing numbered Full Review chapter {number}")
    if automated:
        transcript_markers = (
            "面试实录",
            "面试官提问",
            "问题原文",
            "Question Transcript",
            "面试官问题",
        )
        suggestion_markers = ("回复建议", "回答建议", "Suggested Answer")
        if not any(marker in text for marker in transcript_markers):
            errors.append("automated report lacks the question transcript section")
        if not any(marker in text for marker in suggestion_markers):
            errors.append("automated report lacks answer suggestions")
        summary = re.search(r"^#{1,3}\s+1[.、]\s*", text, flags=re.M)
        first_transcript = min(
            (text.find(marker) for marker in transcript_markers if marker in text),
            default=-1,
        )
        if summary and first_transcript > summary.start():
            errors.append("question transcript must appear before chapter 1")
    if "通过率" in text and "%" in text:
        errors.append("report contains an unsupported pass-rate percentage")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a generated interview review")
    parser.add_argument("review")
    parser.add_argument("--automated", action="store_true")
    args = parser.parse_args()
    path = Path(args.review).expanduser().resolve()
    text = path.read_text(encoding="utf-8-sig")
    errors = validate(text, automated=args.automated)
    print(json.dumps({"status": "FAIL" if errors else "PASS", "path": str(path), "errors": errors}, ensure_ascii=False, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
