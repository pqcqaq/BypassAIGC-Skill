#!/usr/bin/env python3
"""Apply approved segment revisions from a revision packet to a LaTeX file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

from latex_segmenter import protected_tokens, read_text


def load_packet(path: Path) -> Dict:
    return json.loads(read_text(path))


def validate_revision(original: str, revised: str, index: int) -> List[str]:
    errors: List[str] = []
    if not revised.strip():
        return errors
    original_tokens = protected_tokens(original)
    revised_tokens = protected_tokens(revised)
    if original_tokens != revised_tokens:
        errors.append(f"segment {index}: protected token drift")
    return errors


def apply_revisions(source_text: str, packet: Dict) -> str:
    segments = sorted(packet.get("segments", []), key=lambda item: item["start"], reverse=True)
    result = source_text
    errors: List[str] = []

    for segment in segments:
        revised = segment.get("revised_text", "")
        if not revised.strip():
            continue

        start = int(segment["start"])
        end = int(segment["end"])
        original = segment["text"]
        current = result[start:end].strip()
        if current != original.strip():
            errors.append(
                f"segment {segment['index']}: source text no longer matches packet at bytes {start}-{end}"
            )
            continue

        errors.extend(validate_revision(original, revised, int(segment["index"])))
        result = result[:start] + revised.rstrip() + result[end:]

    if errors:
        raise SystemExit("Revision validation failed:\n" + "\n".join(f"- {err}" for err in errors))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="source .tex file")
    parser.add_argument("packet", help="revision packet JSON with revised_text fields")
    parser.add_argument("--out", required=True, help="output .tex file")
    parser.add_argument(
        "--allow-file-token-drift",
        action="store_true",
        help="skip whole-file protected token comparison after applying revisions",
    )
    args = parser.parse_args()

    source_path = Path(args.source)
    source_text = read_text(source_path)
    packet = load_packet(Path(args.packet))
    revised_text = apply_revisions(source_text, packet)

    if not args.allow_file_token_drift and protected_tokens(source_text) != protected_tokens(revised_text):
        raise SystemExit("Whole-file protected token drift detected after applying revisions.")

    Path(args.out).write_text(revised_text, encoding="utf-8")
    print(f"Wrote revised file: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
