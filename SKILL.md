---
name: latex-academic-revision
description: Academic LaTeX revision workflow for thesis, paper, report, and manuscript prose. Use when Codex is asked to revise LaTeX content, reduce generic or AI-like academic phrasing, humanize wording, polish Chinese or English academic writing, preserve citations/equations/commands, produce a revision diff, or prepare ethically auditable academic text without fabricating sources or evading disclosure.
---

# LaTeX Academic Revision

## Boundaries

Use this skill to improve clarity, specificity, coherence, and natural academic voice. Do not promise a detector score, optimize against a named AI detector, fabricate authorship, fabricate citations, hide AI assistance, or remove required disclosure. If the user asks for "lower AI rate", treat it as a request to reduce generic, template-like, over-smooth prose while preserving academic integrity.

Never rewrite LaTeX commands, citation keys, labels, references, formulas, code, tables, figures, bibliography entries, or package configuration unless the user explicitly asks for technical LaTeX edits.

## Standard Workflow

1. Identify the document type, language, target venue, and requested scope.
2. If working on `.tex`, run `scripts/latex_segmenter.py extract` on the file or selected chapter to identify editable prose blocks.
3. Read `references/latex-protection.md` before editing LaTeX-heavy files.
4. Read `references/revision-prompts.md` when composing or applying revision prompts.
5. Revise only prose-bearing segments:
   - Preserve technical meaning and claim strength.
   - Keep citations and cross-references exactly intact.
   - Keep equations, variables, units, dataset names, method names, and proper nouns stable.
   - Prefer concrete domain wording over generic adjectives.
   - Preserve paragraph count unless restructuring is explicitly requested.
6. Return either a patch, a table of original/revised passages, or a rewritten LaTeX block, depending on the user's requested output.
7. For file edits, run `scripts/latex_segmenter.py check original.tex revised.tex` when possible to catch protected-token drift.

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

Do not claim the result will pass or reduce scores in any detector. Say "this reduces generic AI-like phrasing" if the user asks about AI rate.

## Tools

Use the segmenter for `.tex` files:

```powershell
python C:/Users/pqcmm/.codex/skills/latex-academic-revision/scripts/latex_segmenter.py extract path/to/main.tex --json segments.json
python C:/Users/pqcmm/.codex/skills/latex-academic-revision/scripts/latex_segmenter.py check original.tex revised.tex
```

The extractor is conservative: it skips math, comments, code-like environments, and short fragments. If it misses a passage, revise the selected passage manually with the same protection rules.
