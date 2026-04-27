---
name: latex-academic-revision
description: Academic LaTeX revision workflow for thesis, paper, report, and manuscript prose. Use when Codex is asked to revise LaTeX content, diagnose and rewrite Chinese thesis sentences that look generic or AI-like, reduce template-like academic phrasing, humanize wording, polish Chinese or English academic writing, preserve citations/equations/commands, produce a revision diff, or prepare ethically auditable academic text without fabricating sources or evading disclosure.
---

# LaTeX Academic Revision

## Boundaries

Use this skill to improve clarity, specificity, coherence, and natural academic voice. Do not promise a detector score, optimize against a named AI detector, fabricate authorship, fabricate citations, hide AI assistance, or remove required disclosure. If the user asks for "lower AI rate", treat it as a request to reduce generic, template-like, over-smooth prose while preserving academic integrity.

Never rewrite LaTeX commands, citation keys, labels, references, formulas, code, tables, figures, bibliography entries, or package configuration unless the user explicitly asks for technical LaTeX edits.

## Operating Modes

- **Snippet mode**: revise pasted LaTeX or plain academic prose. Use the rules below and return revised text plus a short audit note.
- **Single-file mode**: revise one `.tex` file. Extract or build a revision packet before editing.
- **Project mode**: revise a multi-file LaTeX project. Audit the project first, then work by chapter or file.
- **Validation mode**: compare original and revised files for protected-token drift and report risks.
- **Chinese style diagnosis mode**: scan Chinese thesis prose for empty objective chains, over-neat parallelism, abstract noun stacking, boilerplate transitions, and long overloaded sentences before rewriting.

## Mandatory Workflow

1. Identify document type, language, target venue, and requested scope.
2. For real `.tex` files, read `references/agent-workflow.md`.
3. For LaTeX-heavy files, read `references/latex-protection.md`.
4. For revision wording, read `references/prompt-engineering.md`, `references/revision-prompts.md`, and `references/quality-rubric.md`.
5. For Chinese "AI-like", "AI rate", "more human", or graduation-thesis wording tasks, read `references/chinese-humanization.md` and run `scripts/chinese_ai_style_lint.py` on the target text, packet, file, or project before revising when a file is available.
6. Choose the workflow:
   - Project: run `scripts/latex_project_audit.py`.
   - Single file: run `scripts/build_revision_pack.py` or `scripts/latex_segmenter.py extract`.
   - Chinese style diagnosis: run `scripts/chinese_ai_style_lint.py`.
   - Approved batch revisions: run `scripts/apply_segment_revisions.py`.
   - Prompt generation from a packet: run `scripts/render_revision_prompt.py`; use `--mode chinese-humanize` for Chinese thesis passages that were flagged as template-like.
   - Packet safety lint: run `scripts/lint_revision_packet.py`.
   - Final check: run `scripts/latex_segmenter.py check`.
7. Revise only prose-bearing segments:
   - Preserve technical meaning and claim strength.
   - Keep citations and cross-references exactly intact.
   - Keep equations, variables, units, dataset names, method names, and proper nouns stable.
   - Prefer concrete domain wording over generic adjectives.
   - Preserve paragraph count unless restructuring is explicitly requested.
8. Return a patch, revised LaTeX block, or original/revised table according to the user's requested output.
9. Report checks run and any remaining risks.

## Revision Strategy

Revise for human scholarly texture, not detector evasion:

- Replace vague transitions with the real relationship between ideas.
- Convert generic claims into bounded, evidence-aware claims.
- Vary sentence rhythm without adding informal tone.
- Restructure paragraphs only when requested: extract each paragraph's core point, improve progression, and preserve meaning.
- Adapt vocabulary to the intended reader when specified, keeping formal academic sections precise and restrained.
- Retain field terminology, but remove boilerplate phrasing.
- Add authorial judgment only when supported by the source text.
- Keep limitations, uncertainty, and method constraints visible.
- For Chinese text, reduce slogan-like parallelism and overly uniform connective words.
- For Chinese graduation-thesis text, shorten mechanical "design/implement/build/provide/form" chains, split overloaded technical lists, and anchor value claims to actual commands, modules, logs, tests, or workflow steps already present in the source.
- Do not write self-referential assignment context such as "graduation thesis cycle", "in this graduation thesis", or "during paper writing" into normal thesis prose; recast it as implementation order, scope control, testability, or validation boundary.
- For English text, reduce stacked abstract nouns and repeated "this study aims to" patterns.
- For quote rewriting, preserve attribution and citation keys while converting direct quotation into faithful paraphrase or synthesis.
- For flowchart requests, extract only source-supported steps, inputs, outputs, and decision points.
- Add first-person or emotional texture only in suitable reflective or informal contexts and only when source-grounded.

## LaTeX Editing Rules

Before changing LaTeX, protect these as immutable unless explicitly asked:

- Inline and display math: `$...$`, `\(...\)`, `\[...\]`, `equation`, `align`, `gather`, `multline`.
- Citations and references: `\cite{}`, `\citep{}`, `\citet{}`, `\ref{}`, `\autoref{}`, `\eqref{}`, `\label{}`.
- Structural commands: `\section`, `\subsection`, `\caption`, `\begin`, `\end`, `\item`, `\footnote` command syntax.
- Tables, figures, algorithms, listings, minted/verbatim blocks, bibliography, and preamble.

It is acceptable to revise natural-language text inside section titles, captions, footnotes, and list items if the command structure and labels remain unchanged.

## Output Contract

When revising user text, include:

- The revised text or patch.
- A concise note about what changed: clarity, specificity, flow, terminology, or tone.
- Any preserved elements worth mentioning, such as citations and equations.
- Validation results when files were edited.

When doing Chinese style diagnosis, include flagged sentence, issue, revision, and reason. Keep the reason brief and do not claim detector pass/fail.

Do not claim the result will pass or reduce scores in any detector. Say "this reduces generic AI-like phrasing" if the user asks about AI rate.

## Tools

Use the Python tools in this order when handling files:

```powershell
python scripts/latex_project_audit.py .
python scripts/chinese_ai_style_lint.py main.tex --min-severity medium
python scripts/build_revision_pack.py main.tex --json revision_packet.json --markdown revision_packet.md
python scripts/render_revision_prompt.py revision_packet.json --segment 0 --mode chinese-humanize
python scripts/lint_revision_packet.py revision_packet.json
python scripts/apply_segment_revisions.py main.tex revision_packet.json --out main.revised.tex
python scripts/latex_segmenter.py check main.tex main.revised.tex
```

Tool roles:

- `latex_project_audit.py`: discover root candidates, labels, refs, cites, duplicate labels, and unresolved refs.
- `chinese_ai_style_lint.py`: flag Chinese thesis sentences that look template-like, abstract, overloaded, or mechanically organized.
- `latex_segmenter.py`: extract editable prose segments or compare protected tokens.
- `build_revision_pack.py`: create JSON/Markdown packets for controlled agent revision.
- `render_revision_prompt.py`: render section-aware prompts for one or all packet segments.
- `lint_revision_packet.py`: validate filled `revised_text` fields before applying them.
- `apply_segment_revisions.py`: apply approved `revised_text` fields back to a `.tex` file with protected-token checks.

The tools are conservative. If they miss a passage, revise the selected passage manually with the same protection rules.

## Stop Conditions

Stop and ask before editing when:

- The requested change alters claims, data, citations, or authorship.
- Protected tokens drift and the cause is not obvious.
- The revision packet no longer matches the source file.
- The user asks for guaranteed detector evasion or score reduction.
- The project cannot be compiled or validated and the change is broad.
