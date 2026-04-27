# Revision Prompt Library

These prompts are safe replacements for detector-evasion prompts. They target generic AI-like prose while preserving academic integrity and LaTeX structure.

## Universal LaTeX Revision Prompt

Revise the following LaTeX academic prose for clarity, specificity, and natural scholarly voice.

Constraints:
- Preserve all LaTeX commands, citations, labels, references, equations, variables, and environment syntax exactly.
- Do not add citations, data, claims, or examples that are not present in the source.
- Keep the original language.
- Keep paragraph boundaries unless a restructure is requested.
- Reduce generic AI-like phrasing by making claims more bounded, concrete, and context-aware.
- Output only the revised LaTeX passage.

Text:

```latex
{{TEXT}}
```

## Chinese Academic Prose

Revise the Chinese academic LaTeX passage below.

Focus:
- Replace empty connective chains with specific logical relations.
- Reduce repetitive patterns such as "首先/其次/最后", "具有重要意义", "本文旨在".
- Keep technical terms, dataset names, model names, variables, citations, and formulas unchanged.
- Prefer restrained academic prose over promotional tone.
- Keep meaning and claim strength unchanged.

Output only the revised LaTeX passage.

## English Academic Prose

Revise the English academic LaTeX passage below.

Focus:
- Replace vague phrases such as "comprehensive analysis", "significant improvement", and "plays an important role" with precise statements supported by the source text.
- Reduce stacked nominalizations where a verb gives clearer agency.
- Vary sentence rhythm while keeping formal academic tone.
- Preserve all LaTeX syntax, citations, labels, equations, and technical terms.
- Do not add new claims or citations.

Output only the revised LaTeX passage.

## Abstract Revision

Revise the abstract for clarity and natural academic flow.

Constraints:
- Preserve method, dataset, metric, and result claims exactly.
- Do not inflate novelty.
- Keep the abstract concise.
- Keep LaTeX commands and citations unchanged.
- If the abstract lacks concrete results, do not invent them.

Output only the revised abstract.

## Related Work Revision

Revise the related-work passage to improve synthesis.

Constraints:
- Preserve citation groupings and citation keys exactly.
- Do not change what each cited work is credited with.
- Improve transitions by naming the actual relationship: extension, contrast, limitation, shared assumption, or methodological difference.
- Avoid generic phrases like "many scholars have studied".

Output only the revised LaTeX passage.

## Methods Revision

Revise the methods passage for reproducibility and precision.

Constraints:
- Preserve equations, variable names, hyperparameters, algorithm names, and implementation details.
- Clarify sequence and dependencies between steps.
- Do not add implementation details that are absent from the source.
- Keep formal tone.

Output only the revised LaTeX passage.

## Audit Summary Prompt

After revising, summarize changes in 3 bullets:

- Clarity:
- Specificity:
- Preserved LaTeX elements:

Do not mention detector scores or make pass/fail claims.
