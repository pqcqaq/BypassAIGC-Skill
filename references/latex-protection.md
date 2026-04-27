# LaTeX Protection Rules

## Immutable Tokens

Keep these byte-for-byte unless the user asks for LaTeX syntax changes:

- Citation and bibliography commands: `\cite`, `\citep`, `\citet`, `\parencite`, `\textcite`, `\bibliography`, `\addbibresource`.
- Reference commands: `\ref`, `\autoref`, `\cref`, `\Cref`, `\eqref`, `\pageref`, `\label`.
- Acronym and glossary commands: `\gls`, `\Gls`, `\acrshort`, `\acrlong`, `\acrfull`.
- Math delimiters and content: `$...$`, `\(...\)`, `\[...\]`, equation-like environments.
- URLs and file paths: `\url`, `\href`, `\includegraphics`, `\input`, `\include`.
- Environments: preserve every `\begin{...}` and `\end{...}` pair.

## Editable Text Locations

Usually editable:

- Body paragraphs outside protected environments.
- Section and subsection titles, while keeping command syntax intact.
- Captions, while preserving labels and references.
- Footnote prose, while preserving nested citations and commands.
- List item prose, while preserving `\item` and math.

Usually skip:

- Preamble before `\begin{document}`.
- `abstract` can be edited, but keep word limits and keywords stable.
- `tabular`, `table`, `figure`, `algorithm`, `lstlisting`, `minted`, `verbatim`, `tikzpicture`.
- `.bib` entries unless the user explicitly requests bibliography cleanup.

## Revision Checks

Before finalizing, verify:

- Citation keys are unchanged.
- Label names are unchanged.
- Equation text and variable names are unchanged.
- The number of `\begin` and `\end` commands still matches.
- No Markdown formatting was introduced into LaTeX.
- Chinese punctuation and English punctuation follow the document language style.

## Safe Transformations

Good:

```latex
Original: This study aims to provide a comprehensive analysis of the proposed method.
Revised: This study analyzes how the proposed method behaves under the selected experimental conditions.
```

Good:

```latex
Original: 本文通过实验验证了方法的有效性。
Revised: 本文借助实验结果说明该方法在测试场景中的有效性。
```

Avoid:

```latex
Revised: This groundbreaking study undoubtedly proves...
```

Reason: it overstates evidence and adds unsupported rhetorical force.
