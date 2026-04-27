---
name: latex-academic-revision
description: Academic LaTeX revision workflow for thesis, paper, report, and manuscript prose. Use when Codex is asked to revise LaTeX content, reduce generic or AI-like academic phrasing, humanize wording, polish Chinese or English academic writing, preserve citations/equations/commands, produce a revision diff, or prepare ethically auditable academic text without fabricating sources or evading disclosure.
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

## Mandatory Workflow

1. Identify document type, language, target venue, and requested scope.
2. For real `.tex` files, read `references/agent-workflow.md`.
3. For LaTeX-heavy files, read `references/latex-protection.md`.
4. For revision wording, read `references/prompt-engineering.md`, `references/revision-prompts.md`, and `references/quality-rubric.md`.
5. Choose the workflow:
   - Project: run `scripts/latex_project_audit.py`.
   - Single file: run `scripts/build_revision_pack.py` or `scripts/latex_segmenter.py extract`.
   - Approved batch revisions: run `scripts/apply_segment_revisions.py`.
   - Prompt generation from a packet: run `scripts/render_revision_prompt.py`.
   - Packet safety lint: run `scripts/lint_revision_packet.py`.
   - Final check: run `scripts/latex_segmenter.py check`.
6. Revise only prose-bearing segments:
   - Preserve technical meaning and claim strength.
   - Keep citations and cross-references exactly intact.
   - Keep equations, variables, units, dataset names, method names, and proper nouns stable.
   - Prefer concrete domain wording over generic adjectives.
   - Preserve paragraph count unless restructuring is explicitly requested.
7. Return a patch, revised LaTeX block, or original/revised table according to the user's requested output.
8. Report checks run and any remaining risks.

## Revision Strategy

Revise for human scholarly texture, not detector evasion:

- Replace vague transitions with the real relationship between ideas.
- Convert generic claims into bounded, evidence-aware claims.
- Vary sentence rhythm without adding informal tone.
- Retain field terminology, but remove boilerplate phrasing.
- Add authorial judgment only when supported by the source text.
- Keep limitations, uncertainty, and method constraints visible.
- For Chinese text, reduce slogan-like parallelism and overly uniform connective words.
- For English text, reduce stacked abstract nouns and repeated "this study aims to" patterns.

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

Do not claim the result will pass or reduce scores in any detector. Say "this reduces generic AI-like phrasing" if the user asks about AI rate.

## Tools

Use the Python tools in this order when handling files:

```powershell
python scripts/latex_project_audit.py .
python scripts/build_revision_pack.py main.tex --json revision_packet.json --markdown revision_packet.md
python scripts/render_revision_prompt.py revision_packet.json --segment 0 --mode auto
python scripts/lint_revision_packet.py revision_packet.json
python scripts/apply_segment_revisions.py main.tex revision_packet.json --out main.revised.tex
python scripts/latex_segmenter.py check main.tex main.revised.tex
```

Tool roles:

- `latex_project_audit.py`: discover root candidates, labels, refs, cites, duplicate labels, and unresolved refs.
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
