#!/usr/bin/env python3
"""Conservative LaTeX prose segment extractor and protected-token checker."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List, Tuple


PROTECTED_ENVS = {
    "equation",
    "equation*",
    "align",
    "align*",
    "gather",
    "gather*",
    "multline",
    "multline*",
    "figure",
    "figure*",
    "table",
    "table*",
    "tabular",
    "tabularx",
    "array",
    "algorithm",
    "algorithmic",
    "lstlisting",
    "minted",
    "verbatim",
    "tikzpicture",
    "thebibliography",
}

PROTECTED_COMMAND_RE = re.compile(
    r"\\(?:cite|citep|citet|parencite|textcite|ref|autoref|cref|Cref|eqref|pageref|label|url|href|includegraphics|input|include|gls|Gls|acrshort|acrlong|acrfull)\*?(?:\[[^\]]*\])*\{[^{}]*\}"
)

BEGIN_END_RE = re.compile(r"\\(?:begin|end)\{([^{}]+)\}")


@dataclass
class Segment:
    index: int
    start: int
    end: int
    line_start: int
    line_end: int
    text: str


def read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "gb18030"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise SystemExit(f"Could not decode file: {path}")


def line_number_at(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def ranges_for_regex(text: str, regex: re.Pattern[str]) -> List[Tuple[int, int]]:
    return [(m.start(), m.end()) for m in regex.finditer(text)]


def comment_ranges(text: str) -> List[Tuple[int, int]]:
    ranges: List[Tuple[int, int]] = []
    for m in re.finditer(r"(?<!\\)%.*", text):
        ranges.append((m.start(), m.end()))
    return ranges


def math_ranges(text: str) -> List[Tuple[int, int]]:
    patterns = [
        re.compile(r"\\\[(?s:.*?)\\\]"),
        re.compile(r"\\\((?s:.*?)\\\)"),
        re.compile(r"\$\$(?s:.*?)\$\$"),
        re.compile(r"(?<!\\)\$(?:\\.|[^$])*(?<!\\)\$"),
    ]
    ranges: List[Tuple[int, int]] = []
    for pattern in patterns:
        ranges.extend(ranges_for_regex(text, pattern))
    return ranges


def environment_ranges(text: str) -> List[Tuple[int, int]]:
    ranges: List[Tuple[int, int]] = []
    for env in sorted(PROTECTED_ENVS, key=len, reverse=True):
        escaped = re.escape(env)
        pattern = re.compile(
            rf"\\begin\{{{escaped}\}}(?s:.*?)\\end\{{{escaped}\}}"
        )
        ranges.extend(ranges_for_regex(text, pattern))
    return ranges


def preamble_range(text: str) -> List[Tuple[int, int]]:
    m = re.search(r"\\begin\{document\}", text)
    if not m:
        return []
    return [(0, m.end())]


def document_end_range(text: str) -> List[Tuple[int, int]]:
    m = re.search(r"\\end\{document\}", text)
    if not m:
        return []
    return [(m.start(), len(text))]


def merge_ranges(ranges: Iterable[Tuple[int, int]]) -> List[Tuple[int, int]]:
    ordered = sorted((s, e) for s, e in ranges if s < e)
    if not ordered:
        return []
    merged = [ordered[0]]
    for start, end in ordered[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


def protected_ranges(text: str) -> List[Tuple[int, int]]:
    ranges: List[Tuple[int, int]] = []
    ranges.extend(preamble_range(text))
    ranges.extend(document_end_range(text))
    ranges.extend(comment_ranges(text))
    ranges.extend(math_ranges(text))
    ranges.extend(environment_ranges(text))
    return merge_ranges(ranges)


def mask_text(text: str, ranges: List[Tuple[int, int]]) -> str:
    chars = list(text)
    for start, end in ranges:
        for i in range(start, end):
            if chars[i] != "\n":
                chars[i] = " "
    return "".join(chars)


def extract_segments(text: str, min_chars: int = 80) -> List[Segment]:
    masked = mask_text(text, protected_ranges(text))
    segments: List[Segment] = []
    pattern = re.compile(r"(?:^|\n\s*\n)([^\n](?s:.*?))(?=\n\s*\n|$)")
    for m in pattern.finditer(masked):
        start, end = m.start(1), m.end(1)
        original = text[start:end].strip()
        if len(re.sub(r"\s+", "", original)) < min_chars:
            continue
        if original.startswith("\\") and "\n" not in original:
            continue
        if not re.search(r"[A-Za-z\u4e00-\u9fff]", original):
            continue
        segments.append(
            Segment(
                index=len(segments),
                start=start,
                end=end,
                line_start=line_number_at(text, start),
                line_end=line_number_at(text, end),
                text=original,
            )
        )
    return segments


def protected_tokens(text: str) -> List[str]:
    tokens = PROTECTED_COMMAND_RE.findall(text)
    tokens.extend(m.group(0) for m in BEGIN_END_RE.finditer(text))
    return sorted(tokens)


def cmd_extract(args: argparse.Namespace) -> int:
    path = Path(args.input)
    text = read_text(path)
    segments = extract_segments(text, min_chars=args.min_chars)
    payload = {
        "file": str(path),
        "segment_count": len(segments),
        "segments": [asdict(s) for s in segments],
    }
    output = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.json:
        Path(args.json).write_text(output, encoding="utf-8")
    else:
        print(output)
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    original = read_text(Path(args.original))
    revised = read_text(Path(args.revised))
    left = protected_tokens(original)
    right = protected_tokens(revised)
    if left == right:
        print("OK: protected LaTeX command/reference token multiset is unchanged.")
        return 0
    missing = sorted((set(left) - set(right)))
    added = sorted((set(right) - set(left)))
    print("Protected token drift detected.")
    if missing:
        print("Missing tokens:")
        for token in missing:
            print(f"  - {token}")
    if added:
        print("Added tokens:")
        for token in added:
            print(f"  + {token}")
    return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    extract = sub.add_parser("extract", help="extract editable prose segments")
    extract.add_argument("input", help="input .tex file")
    extract.add_argument("--json", help="write JSON output to this file")
    extract.add_argument("--min-chars", type=int, default=80)
    extract.set_defaults(func=cmd_extract)

    check = sub.add_parser("check", help="compare protected LaTeX tokens")
    check.add_argument("original", help="original .tex file")
    check.add_argument("revised", help="revised .tex file")
    check.set_defaults(func=cmd_check)
    return parser


def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
