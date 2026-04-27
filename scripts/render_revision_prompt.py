#!/usr/bin/env python3
"""Render section-aware revision prompts from a LaTeX revision packet."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, Iterable, List

from latex_segmenter import protected_tokens, read_text


SECTION_KEYWORDS = {
    "abstract": ["abstract", "摘要"],
    "introduction": ["introduction", "intro", "引言", "绪论"],
    "related-work": ["related work", "literature review", "background", "相关工作", "文献综述", "研究现状"],
    "methods": ["method", "methodology", "approach", "model", "方法", "研究设计", "模型"],
    "results": ["result", "experiment", "evaluation", "结果", "实验", "评价", "评估"],
    "discussion": ["discussion", "conclusion", "limitation", "讨论", "结论", "局限"],
}


def detect_language(text: str) -> str:
    chinese = len(re.findall(r"[\u4e00-\u9fff]", text))
    english = len(re.findall(r"[A-Za-z]", text))
    if chinese and chinese >= english / 3:
        return "Chinese"
    if english:
        return "English"
    return "Mixed"


def detect_mode(text: str, requested: str, section_hint: Dict | None = None) -> str:
    if requested != "auto":
        return requested
    hint_title = ((section_hint or {}).get("title") or "").lower()
    for mode, keywords in SECTION_KEYWORDS.items():
        if any(keyword.lower() in hint_title for keyword in keywords):
            return mode

    lowered = text.lower()
    for mode, keywords in SECTION_KEYWORDS.items():
        strong_keywords = [keyword for keyword in keywords if len(keyword) > 6 or not keyword.isascii()]
        if any(keyword.lower() in lowered for keyword in strong_keywords):
            return mode
    language = detect_language(text)
    if language == "Chinese":
        return "chinese"
    if language == "English":
        return "english"
    return "universal"


def bullet_tokens(tokens: Iterable[str]) -> str:
    items = list(tokens)
    if not items:
        return "- (none detected)"
    return "\n".join(f"- `{token}`" for token in items)


def load_packet(path: Path) -> Dict:
    return json.loads(read_text(path))


def render_prompt(segment: Dict, mode: str, output: str) -> str:
    text = segment["text"]
    section_hint = segment.get("section_hint") or {}
    resolved_mode = detect_mode(text, mode, section_hint)
    language = detect_language(text)
    tokens = protected_tokens(text)
    schema = (
        '{\n'
        '  "revised_text": "revised LaTeX segment here",\n'
        '  "revision_note": "one concise sentence explaining the change",\n'
        '  "risk_flags": []\n'
        '}'
    )
    output_contract = (
        "Return only the revised LaTeX segment. Do not wrap it in Markdown."
        if output == "latex"
        else "Return only strict JSON matching this schema:\n\n```json\n" + schema + "\n```"
    )

    return f"""You are revising one LaTeX academic prose segment.

Task frame:
- Section mode: `{resolved_mode}`
- Section hint: `{section_hint.get('command', '')} {section_hint.get('title', '')}`
- Detected language: `{language}`
- Segment index: `{segment.get('index')}`
- Source lines: {segment.get('line_start')}-{segment.get('line_end')}

Safety boundary:
- Do not promise, target, or discuss AI detector scores.
- Do not fabricate citations, data, examples, experiments, or claims.
- Preserve the original claim strength or make it more cautious when the source is vague.
- Keep the original language.

LaTeX boundary:
- Preserve every protected token byte-for-byte.
- Preserve all LaTeX commands, math, citations, labels, refs, variables, and environment syntax.
- Protected tokens detected:
{bullet_tokens(tokens)}

Revision objective:
- Reduce generic AI-like phrasing by improving specificity, local logic, and authorial judgment.
- Replace vague transitions with the actual relation between ideas.
- Prefer bounded, evidence-aware claims over broad promotional wording.
- Keep paragraph boundaries and meaning stable.

Output contract:
{output_contract}

Original segment:

```latex
{text}
```
"""


def write_prompts(packet: Dict, args: argparse.Namespace) -> None:
    segments: List[Dict] = packet.get("segments", [])
    selected: List[Dict]
    if args.segment is None:
        selected = segments
    else:
        selected = [seg for seg in segments if int(seg.get("index", -1)) == args.segment]
        if not selected:
            raise SystemExit(f"Segment not found: {args.segment}")

    if args.out_dir:
        out_dir = Path(args.out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        for segment in selected:
            prompt = render_prompt(segment, args.mode, args.output)
            path = out_dir / f"segment_{segment['index']:04d}.prompt.md"
            path.write_text(prompt, encoding="utf-8")
        print(f"Wrote {len(selected)} prompt file(s) to {out_dir}")
        return

    print("\n\n---\n\n".join(render_prompt(seg, args.mode, args.output) for seg in selected))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", help="revision packet JSON")
    parser.add_argument("--segment", type=int, help="render one segment index")
    parser.add_argument(
        "--mode",
        default="auto",
        choices=["auto", "universal", "chinese", "english", "abstract", "introduction", "related-work", "methods", "results", "discussion"],
    )
    parser.add_argument("--output", default="json", choices=["json", "latex"])
    parser.add_argument("--out-dir", help="write prompts to a directory")
    args = parser.parse_args()

    packet = load_packet(Path(args.packet))
    write_prompts(packet, args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
