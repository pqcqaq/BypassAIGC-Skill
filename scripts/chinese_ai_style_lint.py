#!/usr/bin/env python3
"""Heuristic lint for generic or AI-like Chinese thesis prose."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

from latex_segmenter import extract_segments, line_number_at, read_text


TEXT_EXTENSIONS = {".tex", ".md", ".txt"}
SEVERITY_ORDER = {"low": 1, "medium": 2, "high": 3}

ABSTRACT_NOUNS = [
    "机制",
    "能力",
    "链路",
    "体系",
    "平台",
    "方案",
    "闭环",
    "价值",
    "意义",
    "支撑",
    "沉淀",
    "复用",
    "诊断",
    "分级",
    "重组",
    "保护",
]

GENERIC_VERBS = [
    "设计",
    "实现",
    "构建",
    "提出",
    "完成",
    "提供",
    "形成",
    "提升",
    "降低",
    "具备",
    "开展",
    "进行",
    "优化",
    "沉淀",
    "复用",
]

PHRASE_RULES: Sequence[Tuple[str, str, str, str, str]] = [
    (
        "generic-value-claim",
        "high",
        r"(?:提供帮助|提供保护|提供支撑|具备持续积累|降低单点失败风险|降低犯错成本|提升诊断效率|减少重复解释)",
        "价值判断过于顺滑，缺少具体场景或证据锚点。",
        "把价值限定到命令入口、异常输出、知识条目或测试样例等具体位置。",
    ),
    (
        "closed-loop-cliche",
        "high",
        r"(?:形成闭环|业务链的集成与重组|从零构造全部技术能力|较成熟方案|持续积累经验)",
        "出现论文式套话，读起来像总结模板。",
        "改成具体链路：谁产生输入，哪个模块处理，结果落到哪里。",
    ),
    (
        "mechanical-objective",
        "medium",
        r"(?:设计|实现|构建|提出|完成).{0,24}(?:机制|链路|体系|平台|方案|能力|解释|建议生成|快速匹配|分级)",
        "目标句偏机械，动词和抽象名词组合过多。",
        "改成“用来处理什么”的句式，并保留一个可核对的对象或例子。",
    ),
    (
        "boilerplate-transition",
        "medium",
        r"(?:基于上述问题|本文主要做了以下工作|全文共分为六章|这表明|需要补充说明的是|总体来看|综上所述)",
        "过渡语偏模板化。",
        "删短过渡，把篇幅留给实现事实或前后逻辑关系。",
    ),
    (
        "meta-thesis-self-reference",
        "high",
        r"(?:毕业设计周期|毕业论文中|毕业论文里|本毕业设计|毕业设计训练目标|论文写作时|本文写作时|论文正文中)",
        "正文站在论文外评价论文或写作过程，读起来像自我说明。",
        "改回工程事实、模块安排、测试约束或章节内容，不要在正文里解释“这是毕业论文”。",
    ),
    (
        "chain-target-template",
        "medium",
        r"(?:关注).{2,28}(?:目标是)",
        "“关注……目标是……”结构过于整齐，容易显得机械。",
        "拆成更自然的两句，说明该链路实际接收什么、输出什么。",
    ),
    (
        "thesis-subject-template",
        "medium",
        r"^(?:本文|本课题|本研究|该系统|本系统|该方案).{0,16}(?:旨在|主要|尝试|能够|可以|具备|实现|提供)",
        "主语和谓语都偏论文模板。",
        "优先改用模块、命令、日志、接口或测试场景作主语。",
    ),
]


@dataclass
class Finding:
    source: str
    line_start: int
    line_end: int
    severity: str
    rule: str
    message: str
    excerpt: str
    suggestion: str
    segment_index: int | None = None


def chinese_count(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def compact(text: str, limit: int = 120) -> str:
    collapsed = re.sub(r"\s+", " ", text).strip()
    if len(collapsed) <= limit:
        return collapsed
    return collapsed[: limit - 1] + "…"


def split_sentences(text: str) -> List[Tuple[int, int, str]]:
    spans: List[Tuple[int, int, str]] = []
    pattern = re.compile(r"[^。！？；!?;\n]+[。！？；!?;]?")
    for match in pattern.finditer(text):
        sentence = match.group(0).strip()
        if chinese_count(sentence) >= 8:
            spans.append((match.start(), match.end(), sentence))
    return spans


def count_hits(sentence: str, words: Iterable[str]) -> int:
    return sum(1 for word in words if word in sentence)


def add_finding(
    findings: List[Finding],
    *,
    source: str,
    base_text: str,
    base_offset: int,
    sentence_start: int,
    sentence_end: int,
    severity: str,
    rule: str,
    message: str,
    sentence: str,
    suggestion: str,
    segment_index: int | None,
) -> None:
    start = base_offset + sentence_start
    end = base_offset + sentence_end
    findings.append(
        Finding(
            source=source,
            line_start=line_number_at(base_text, start),
            line_end=line_number_at(base_text, end),
            severity=severity,
            rule=rule,
            message=message,
            excerpt=compact(sentence),
            suggestion=suggestion,
            segment_index=segment_index,
        )
    )


def lint_sentence(
    sentence: str,
    findings: List[Finding],
    *,
    source: str,
    base_text: str,
    base_offset: int,
    sentence_start: int,
    sentence_end: int,
    segment_index: int | None,
) -> None:
    stripped = sentence.strip()
    for rule, severity, pattern, message, suggestion in PHRASE_RULES:
        if re.search(pattern, stripped):
            add_finding(
                findings,
                source=source,
                base_text=base_text,
                base_offset=base_offset,
                sentence_start=sentence_start,
                sentence_end=sentence_end,
                severity=severity,
                rule=rule,
                message=message,
                sentence=stripped,
                suggestion=suggestion,
                segment_index=segment_index,
            )

    zh_len = chinese_count(stripped)
    separator_count = stripped.count("、") + stripped.count("，") + stripped.count(",")
    if zh_len >= 115 or (zh_len >= 90 and separator_count >= 5):
        add_finding(
            findings,
            source=source,
            base_text=base_text,
            base_offset=base_offset,
            sentence_start=sentence_start,
            sentence_end=sentence_end,
            severity="high" if zh_len >= 130 else "medium",
            rule="long-overloaded-sentence",
            message="句子过长且信息堆叠，容易呈现机器式概括。",
            sentence=stripped,
            suggestion="先拆句，再分别处理背景、实现、价值或例子。",
            segment_index=segment_index,
        )

    list_count = stripped.count("、") + stripped.count("以及") + stripped.count("和")
    if list_count >= 5:
        add_finding(
            findings,
            source=source,
            base_text=base_text,
            base_offset=base_offset,
            sentence_start=sentence_start,
            sentence_end=sentence_end,
            severity="medium",
            rule="overpacked-list",
            message="并列项过多，像技术名词清单。",
            sentence=stripped,
            suggestion="保留关键项，把其余项拆到下一句或按模块说明作用。",
            segment_index=segment_index,
        )

    abstract_hits = count_hits(stripped, ABSTRACT_NOUNS)
    generic_hits = count_hits(stripped, GENERIC_VERBS)
    if abstract_hits >= 5 and zh_len >= 38:
        add_finding(
            findings,
            source=source,
            base_text=base_text,
            base_offset=base_offset,
            sentence_start=sentence_start,
            sentence_end=sentence_end,
            severity="medium",
            rule="abstract-noun-density",
            message="抽象名词密度较高，缺少可核对对象。",
            sentence=stripped,
            suggestion="删掉一两个抽象名词，换成命令、模块、接口、日志或测试样例。",
            segment_index=segment_index,
        )
    if generic_hits >= 4 and abstract_hits >= 2:
        add_finding(
            findings,
            source=source,
            base_text=base_text,
            base_offset=base_offset,
            sentence_start=sentence_start,
            sentence_end=sentence_end,
            severity="medium",
            rule="generic-verb-density",
            message="通用动词过密，句子像任务清单而不是作者叙述。",
            sentence=stripped,
            suggestion="减少“设计/实现/提供/提升”等动词，改写为具体动作和对象。",
            segment_index=segment_index,
        )


def lint_text(source: str, text: str, min_chars: int) -> List[Finding]:
    findings: List[Finding] = []
    if source.endswith(".tex"):
        segments = extract_segments(text, min_chars=min_chars)
        for segment in segments:
            for start, end, sentence in split_sentences(segment.text):
                lint_sentence(
                    sentence,
                    findings,
                    source=source,
                    base_text=text,
                    base_offset=segment.start,
                    sentence_start=start,
                    sentence_end=end,
                    segment_index=segment.index,
                )
        return findings

    for start, end, sentence in split_sentences(text):
        lint_sentence(
            sentence,
            findings,
            source=source,
            base_text=text,
            base_offset=0,
            sentence_start=start,
            sentence_end=end,
            segment_index=None,
        )
    return findings


def lint_packet(path: Path, min_chars: int) -> List[Finding]:
    packet = json.loads(read_text(path))
    if not isinstance(packet, dict) or "segments" not in packet:
        return []
    source = str(path)
    findings: List[Finding] = []
    for segment in packet.get("segments", []):
        text = segment.get("revised_text") or segment.get("text") or ""
        if chinese_count(text) < min_chars:
            continue
        source_line = int(segment.get("line_start") or 1)
        fake_base = ("\n" * max(source_line - 1, 0)) + text
        fake_offset = max(source_line - 1, 0)
        for start, end, sentence in split_sentences(text):
            lint_sentence(
                sentence,
                findings,
                source=source,
                base_text=fake_base,
                base_offset=fake_offset,
                sentence_start=start,
                sentence_end=end,
                segment_index=segment.get("index"),
            )
    return findings


def iter_inputs(paths: Sequence[str]) -> Iterable[Path]:
    for item in paths:
        path = Path(item)
        if path.is_dir():
            for child in path.rglob("*"):
                if ".git" in child.parts:
                    continue
                if child.suffix.lower() in TEXT_EXTENSIONS or child.suffix.lower() == ".json":
                    yield child
        else:
            yield path


def lint_path(path: Path, min_chars: int) -> List[Finding]:
    if path.suffix.lower() == ".json":
        return lint_packet(path, min_chars)
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return []
    text = read_text(path)
    return lint_text(str(path), text, min_chars)


def filter_findings(findings: List[Finding], min_severity: str) -> List[Finding]:
    threshold = SEVERITY_ORDER[min_severity]
    return [finding for finding in findings if SEVERITY_ORDER[finding.severity] >= threshold]


def print_text(findings: List[Finding]) -> None:
    if not findings:
        print("OK: no Chinese AI-like thesis style findings.")
        return
    for finding in findings:
        location = f"{finding.source}:{finding.line_start}"
        if finding.line_end != finding.line_start:
            location += f"-{finding.line_end}"
        segment = f" segment={finding.segment_index}" if finding.segment_index is not None else ""
        print(f"{finding.severity.upper()} {location}{segment} {finding.rule}")
        print(f"  issue: {finding.message}")
        print(f"  text: {finding.excerpt}")
        print(f"  suggestion: {finding.suggestion}")


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", help="files or directories to scan")
    parser.add_argument("--json", action="store_true", help="print JSON instead of text")
    parser.add_argument("--min-severity", choices=sorted(SEVERITY_ORDER), default="low")
    parser.add_argument("--min-chars", type=int, default=24, help="minimum Chinese chars to scan")
    parser.add_argument("--fail-on", choices=sorted(SEVERITY_ORDER), help="return 2 if this severity or above appears")
    args = parser.parse_args(argv)

    findings: List[Finding] = []
    for path in iter_inputs(args.inputs):
        try:
            findings.extend(lint_path(path, args.min_chars))
        except (OSError, json.JSONDecodeError, UnicodeDecodeError) as exc:
            print(f"WARN {path}: {exc}", file=sys.stderr)

    findings = filter_findings(findings, args.min_severity)
    findings.sort(key=lambda item: (item.source, item.line_start, -SEVERITY_ORDER[item.severity], item.rule))

    if args.json:
        print(json.dumps([asdict(finding) for finding in findings], ensure_ascii=False, indent=2))
    else:
        print_text(findings)

    if args.fail_on:
        threshold = SEVERITY_ORDER[args.fail_on]
        if any(SEVERITY_ORDER[finding.severity] >= threshold for finding in findings):
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
