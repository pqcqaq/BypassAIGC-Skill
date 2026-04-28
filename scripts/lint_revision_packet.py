#!/usr/bin/env python3
"""Lint filled revised_text fields in a LaTeX revision packet."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List

from latex_segmenter import protected_tokens, read_text


RISKY_PHRASES = [
    "ai detector",
    "undetectable",
    "bypass",
    "guarantee",
    "detector score",
    "human fingerprint",
    "检测率",
    "ai率",
    "降ai率",
    "绕过",
    "规避检测",
    "不可检测",
    "人类指纹",
    "保证通过",
]

HIDDEN_UNICODE_RE = re.compile(r"[\u200b-\u200f\u202a-\u202e\u2060\ufeff\u00ad]")


def load_packet(path: Path) -> Dict:
    return json.loads(read_text(path))


def language_kind(text: str) -> str:
    chinese = len(re.findall(r"[\u4e00-\u9fff]", text))
    english = len(re.findall(r"[A-Za-z]", text))
    if chinese and chinese >= english / 3:
        return "zh"
    if english:
        return "en"
    return "mixed"


def length_ratio(original: str, revised: str) -> float:
    original_len = max(len(original.strip()), 1)
    return len(revised.strip()) / original_len


def lint_segment(segment: Dict, max_ratio: float, min_ratio: float) -> List[str]:
    errors: List[str] = []
    warnings: List[str] = []
    revised = (segment.get("revised_text") or "").strip()
    if not revised:
        return []
    original = segment.get("text", "")
    idx = segment.get("index")

    if protected_tokens(original) != protected_tokens(revised):
        errors.append(f"ERROR segment {idx}: protected token drift")

    ratio = length_ratio(original, revised)
    if ratio > max_ratio:
        warnings.append(f"WARN segment {idx}: revised_text is long ({ratio:.2f}x original)")
    if ratio < min_ratio:
        warnings.append(f"WARN segment {idx}: revised_text is short ({ratio:.2f}x original)")

    if language_kind(original) != "mixed" and language_kind(revised) != language_kind(original):
        warnings.append(f"WARN segment {idx}: language appears to have changed")

    lowered = revised.lower()
    for phrase in RISKY_PHRASES:
        if phrase.lower() in lowered:
            warnings.append(f"WARN segment {idx}: risky phrase appears: {phrase}")

    if "```" in revised:
        errors.append(f"ERROR segment {idx}: revised_text contains Markdown fence")

    if HIDDEN_UNICODE_RE.search(revised):
        errors.append(f"ERROR segment {idx}: revised_text contains hidden Unicode control characters")

    return errors + warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", help="revision packet JSON")
    parser.add_argument("--max-ratio", type=float, default=1.8)
    parser.add_argument("--min-ratio", type=float, default=0.45)
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    args = parser.parse_args()

    packet = load_packet(Path(args.packet))
    messages: List[str] = []
    for segment in packet.get("segments", []):
        messages.extend(lint_segment(segment, args.max_ratio, args.min_ratio))

    if not messages:
        print("OK: revision packet lint passed.")
        return 0

    for message in messages:
        print(message)

    has_error = any(message.startswith("ERROR") for message in messages)
    has_warning = any(message.startswith("WARN") for message in messages)
    if has_error or (args.strict and has_warning):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
