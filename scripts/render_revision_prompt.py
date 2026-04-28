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


def mode_guidance(mode: str, language: str) -> str:
    if mode == "source-grounded":
        return """- Treat the source passage as the only evidence base.
- Preserve all claims, citations, terminology, numbers, and caveats unless the user supplied source material justifies a change.
- Replace vague claims with bounded source-grounded wording; if a necessary detail is missing, mark it as `needs_author_input` in `risk_flags` instead of inventing it.
- Check for vague attribution such as "studies show" or "research indicates"; keep it only when a citation or supplied source supports it.
- Improve clarity, logic, and academic tone without inflating novelty or certainty."""
    if mode == "chinese-humanize":
        return """- Diagnose Chinese thesis prose before rewriting: empty objective chains, over-neat parallelism, abstract noun stacking, unsupported value claims, fixed "首先/其次/最后" transitions, boilerplate transitions, repeated "本文/本课题" subjects, and long overloaded sentences.
- Make each sentence shorter, more concrete, and closer to author reasoning while preserving thesis tone.
- Prefer checkable anchors already present in the source: command names, module names, source-code facts, APIs, logs, test cases, or workflow steps.
- Replace "提供帮助/提供保护/具备能力/形成闭环/完成集成与重组" with what the prototype actually does.
- Remove meta thesis self-reference such as "毕业设计周期", "毕业论文中", or "论文写作时" from normal prose; express the point as implementation order, scope control, testability, or validation boundary.
- Improve paragraph handoff when context is available; keep one local claim per paragraph.
- Match vocabulary to the intended reader if specified: explain jargon for general readers, preserve precise terms for experts.
- Vary sentence rhythm by splitting overloaded sentences and avoiding repeated openings; do not add rhetorical questions to formal thesis sections.
- Do not add invented examples, personal memories, unsupported first-person claims, or casual wording."""
    if mode == "chinese":
        return """- Reduce slogan-like parallelism and empty connective chains.
- Replace broad verbs such as "进行/开展/实现优化" with concrete actions when the source supports it.
- Keep a restrained academic tone."""
    if mode == "english":
        return """- Reduce stacked nominalizations and template phrases.
- Prefer precise verbs and bounded claims.
- Keep formal academic tone."""
    if mode in {"abstract", "introduction", "related-work", "methods", "results", "discussion"}:
        return f"- Follow the `{mode}` section purpose and keep claims bounded by the source text."
    if language == "Chinese":
        return "- Keep Chinese academic prose specific, concise, and context-aware."
    if language == "English":
        return "- Keep English academic prose specific, concise, and formally readable."
    return "- Keep the prose specific, concise, and faithful to the source."


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

Mode-specific guidance:
{mode_guidance(resolved_mode, language)}

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
        choices=[
            "auto",
            "universal",
            "chinese",
            "chinese-humanize",
            "source-grounded",
            "english",
            "abstract",
            "introduction",
            "related-work",
            "methods",
            "results",
            "discussion",
        ],
    )
    parser.add_argument("--output", default="json", choices=["json", "latex"])
    parser.add_argument("--out-dir", help="write prompts to a directory")
    args = parser.parse_args()

    packet = load_packet(Path(args.packet))
    write_prompts(packet, args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
