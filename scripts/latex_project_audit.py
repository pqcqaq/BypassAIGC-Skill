#!/usr/bin/env python3
"""Audit a LaTeX project for files, roots, labels, refs, cites, and includes."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Set


CITE_RE = re.compile(
    r"\\(?:cite|citep|citet|parencite|textcite|autocite)\*?(?:\[[^\]]*\])*\{([^{}]+)\}"
)
LABEL_RE = re.compile(r"\\label\{([^{}]+)\}")
REF_RE = re.compile(r"\\(?:ref|autoref|cref|Cref|eqref|pageref)\*?\{([^{}]+)\}")
INPUT_RE = re.compile(r"\\(?:input|include)\{([^{}]+)\}")
DOCUMENTCLASS_RE = re.compile(r"\\documentclass(?:\[[^\]]*\])?\{[^{}]+\}")
BEGIN_DOCUMENT_RE = re.compile(r"\\begin\{document\}")


@dataclass
class FileAudit:
    path: str
    is_root_candidate: bool
    labels: List[str]
    refs: List[str]
    cites: List[str]
    inputs: List[str]


def read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "gb18030"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return ""


def split_keys(raw: str) -> List[str]:
    return [part.strip() for part in raw.split(",") if part.strip()]


def unique_sorted(items: Iterable[str]) -> List[str]:
    return sorted(set(items))


def resolve_input(base_file: Path, raw: str) -> str:
    candidate = Path(raw)
    if candidate.suffix == "":
        candidate = candidate.with_suffix(".tex")
    if not candidate.is_absolute():
        candidate = (base_file.parent / candidate).resolve()
    try:
        return str(candidate.relative_to(Path.cwd()))
    except ValueError:
        return str(candidate)


def audit_file(path: Path) -> FileAudit:
    text = read_text(path)
    cites: List[str] = []
    for match in CITE_RE.finditer(text):
        cites.extend(split_keys(match.group(1)))
    inputs = [resolve_input(path, m.group(1)) for m in INPUT_RE.finditer(text)]
    return FileAudit(
        path=str(path),
        is_root_candidate=bool(DOCUMENTCLASS_RE.search(text) or BEGIN_DOCUMENT_RE.search(text)),
        labels=unique_sorted(m.group(1) for m in LABEL_RE.finditer(text)),
        refs=unique_sorted(m.group(1) for m in REF_RE.finditer(text)),
        cites=unique_sorted(cites),
        inputs=unique_sorted(inputs),
    )


def find_tex_files(root: Path) -> List[Path]:
    if root.is_file():
        return [root]
    files = []
    for path in root.rglob("*.tex"):
        if any(part.startswith(".") for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def build_audit(root: Path) -> Dict:
    files = [audit_file(path) for path in find_tex_files(root)]
    all_labels: List[str] = []
    all_refs: List[str] = []
    all_cites: List[str] = []
    label_locations: Dict[str, List[str]] = {}
    for item in files:
        all_labels.extend(item.labels)
        all_refs.extend(item.refs)
        all_cites.extend(item.cites)
        for label in item.labels:
            label_locations.setdefault(label, []).append(item.path)

    labels_set: Set[str] = set(all_labels)
    refs_set: Set[str] = set(all_refs)
    duplicate_labels = {
        label: paths for label, paths in sorted(label_locations.items()) if len(paths) > 1
    }

    return {
        "root": str(root),
        "tex_file_count": len(files),
        "root_candidates": [item.path for item in files if item.is_root_candidate],
        "files": [asdict(item) for item in files],
        "summary": {
            "label_count": len(labels_set),
            "ref_count": len(refs_set),
            "cite_key_count": len(set(all_cites)),
            "duplicate_labels": duplicate_labels,
            "unresolved_refs": sorted(refs_set - labels_set),
            "unreferenced_labels": sorted(labels_set - refs_set),
        },
    }


def print_text_report(payload: Dict) -> None:
    summary = payload["summary"]
    print(f"LaTeX project: {payload['root']}")
    print(f"TeX files: {payload['tex_file_count']}")
    print("Root candidates:")
    for path in payload["root_candidates"] or ["(none found)"]:
        print(f"  - {path}")
    print(f"Labels: {summary['label_count']}")
    print(f"Refs: {summary['ref_count']}")
    print(f"Cite keys: {summary['cite_key_count']}")
    print(f"Duplicate labels: {len(summary['duplicate_labels'])}")
    if summary["duplicate_labels"]:
        for label, paths in summary["duplicate_labels"].items():
            print(f"  - {label}: {', '.join(paths)}")
    print(f"Unresolved refs: {len(summary['unresolved_refs'])}")
    for label in summary["unresolved_refs"]:
        print(f"  - {label}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", help="LaTeX project directory or .tex file")
    parser.add_argument("--json", help="write JSON report to this path")
    parser.add_argument(
        "--fail-on-unresolved",
        action="store_true",
        help="exit with status 2 when unresolved refs or duplicate labels exist",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    payload = build_audit(root)
    if args.json:
        Path(args.json).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        print_text_report(payload)

    summary = payload["summary"]
    if args.fail_on_unresolved and (summary["unresolved_refs"] or summary["duplicate_labels"]):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
