#!/usr/bin/env python3
"""Build a revision packet from a LaTeX file for agent-assisted prose editing."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List

from latex_segmenter import extract_segments, protected_tokens, read_text


PACKET_VERSION = "1.0"
HEADING_RE = re.compile(
    r"\\(?P<cmd>chapter|section|subsection|subsubsection|paragraph)\*?(?:\[[^\]]*\])?\{(?P<title>[^{}]+)\}"
)


def section_hints(text: str) -> List[Dict]:
    return [
        {
            "start": match.start(),
            "command": match.group("cmd"),
            "title": match.group("title"),
        }
        for match in HEADING_RE.finditer(text)
    ]


def section_hint_for(headings: List[Dict], offset: int) -> Dict:
    current = {"command": "", "title": ""}
    for heading in headings:
        if heading["start"] <= offset:
            current = {"command": heading["command"], "title": heading["title"]}
        else:
            break
    return current


def build_packet(tex_path: Path, min_chars: int) -> Dict:
    text = read_text(tex_path)
    segments = extract_segments(text, min_chars=min_chars)
    headings = section_hints(text)
    return {
        "version": PACKET_VERSION,
        "source_file": str(tex_path),
        "segment_count": len(segments),
        "protected_token_count": len(protected_tokens(text)),
        "instructions": [
            "Revise only revised_text values.",
            "Keep every protected LaTeX command, citation, reference, label, equation, and environment unchanged.",
            "Do not add claims, citations, data, or detector-score promises.",
            "Leave revised_text empty for segments that should not be changed.",
        ],
        "segments": [
            {
                **asdict(segment),
                "section_hint": section_hint_for(headings, segment.start),
                "revised_text": "",
                "revision_note": "",
            }
            for segment in segments
        ],
    }


def packet_to_markdown(packet: Dict) -> str:
    lines: List[str] = []
    lines.append("# LaTeX Revision Packet")
    lines.append("")
    lines.append(f"- Source: `{packet['source_file']}`")
    lines.append(f"- Segments: {packet['segment_count']}")
    lines.append(f"- Protected tokens: {packet['protected_token_count']}")
    lines.append("")
    lines.append("## Agent Instructions")
    lines.append("")
    for item in packet["instructions"]:
        lines.append(f"- {item}")
    lines.append("")
    for segment in packet["segments"]:
        lines.append(f"## Segment {segment['index']}")
        lines.append("")
        lines.append(f"Lines: {segment['line_start']}-{segment['line_end']}")
        lines.append("")
        lines.append("Original:")
        lines.append("")
        lines.append("```latex")
        lines.append(segment["text"])
        lines.append("```")
        lines.append("")
        lines.append("Revised:")
        lines.append("")
        lines.append("```latex")
        lines.append("")
        lines.append("```")
        lines.append("")
        lines.append("Revision note:")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="input .tex file")
    parser.add_argument("--min-chars", type=int, default=80)
    parser.add_argument("--json", help="write machine-readable packet")
    parser.add_argument("--markdown", help="write human-readable packet")
    args = parser.parse_args()

    packet = build_packet(Path(args.input), args.min_chars)
    if not args.json and not args.markdown:
        print(json.dumps(packet, ensure_ascii=False, indent=2))
        return 0
    if args.json:
        Path(args.json).write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.markdown:
        Path(args.markdown).write_text(packet_to_markdown(packet), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
