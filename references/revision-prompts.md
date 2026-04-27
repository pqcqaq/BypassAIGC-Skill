# Revision Prompt Library

These prompts are safe replacements for detector-evasion prompts. They target generic AI-like prose while preserving academic integrity and LaTeX structure.

## Segment JSON Prompt

Use this when filling a `revision_packet.json` segment.

You are revising one LaTeX academic prose segment.

Context:
- Section mode: `{{SECTION_MODE}}`
- Section hint: `{{SECTION_HINT}}`
- Detected language: `{{LANGUAGE}}`
- Protected tokens that must remain byte-for-byte unchanged:
{{PROTECTED_TOKENS}}

Non-negotiable constraints:
- Preserve every protected token exactly.
- Preserve LaTeX syntax, math, citations, labels, references, commands, and environment names.
- Do not add citations, data, examples, experimental results, or claims not present in the source.
- Do not promise or discuss detector scores.
- Keep the original language.
- Keep the claim strength the same or more cautious.

Revision objectives:
- Reduce generic AI-like phrasing by improving specificity and local logic.
- Replace vague transitions with the real relation between ideas.
- Use field-appropriate terminology without adding unsupported jargon.
- Keep paragraph boundaries and overall meaning stable.

Return only strict JSON:

```json
{
  "revised_text": "revised LaTeX segment here",
  "revision_note": "one concise sentence explaining the change",
  "risk_flags": []
}
```

Original segment:

```latex
{{TEXT}}
```

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
- Replace broad verbs such as "进行分析", "开展研究", "实现优化" with concrete actions when the source supports it.
- Use cautious academic wording for unquantified claims, such as "说明", "表明", "在该场景下".
- Keep technical terms, dataset names, model names, variables, citations, and formulas unchanged.
- Prefer restrained academic prose over promotional tone.
- Keep meaning and claim strength unchanged.

Output only the revised LaTeX passage.

## English Academic Prose

Revise the English academic LaTeX passage below.

Focus:
- Replace vague phrases such as "comprehensive analysis", "significant improvement", and "plays an important role" with precise statements supported by the source text.
- Reduce stacked nominalizations where a verb gives clearer agency.
- Replace template phrases such as "this paper aims to", "in recent years", and "with the rapid development of" when they do not add information.
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
- Make the contribution, method, and scope explicit only when already present.

Output only the revised abstract.

## Introduction Revision

Revise the introduction passage for motivation, scope, and problem framing.

Constraints:
- Do not overstate novelty or importance.
- Make the research problem and scope clearer when already present.
- Preserve citations and attribution.
- Avoid generic openings such as "with the rapid development of" unless they carry specific context.

Output only the revised LaTeX passage.

## Related Work Revision

Revise the related-work passage to improve synthesis.

Constraints:
- Preserve citation groupings and citation keys exactly.
- Do not change what each cited work is credited with.
- Improve transitions by naming the actual relationship: extension, contrast, limitation, shared assumption, or methodological difference.
- Avoid generic phrases like "many scholars have studied".
- Do not merge citation groups if it changes attribution.
- Do not imply criticism of cited work unless the source already states it.

Output only the revised LaTeX passage.

## Methods Revision

Revise the methods passage for reproducibility and precision.

Constraints:
- Preserve equations, variable names, hyperparameters, algorithm names, and implementation details.
- Clarify sequence and dependencies between steps.
- Do not add implementation details that are absent from the source.
- Keep formal tone.
- Prefer reproducible verbs: "compute", "initialize", "sample", "normalize", "compare", "estimate", when they match the source.

Output only the revised LaTeX passage.

## Results Revision

Revise the results or experiment passage for precision.

Constraints:
- Preserve all metrics, values, dataset names, baselines, and statistical wording.
- Do not turn an observed result into a general proof.
- Distinguish measured results from interpretation.
- Keep tables, figure references, and equation references unchanged.

Output only the revised LaTeX passage.

## Discussion Or Conclusion Revision

Revise the discussion or conclusion passage for balanced academic judgment.

Constraints:
- Preserve limitations and uncertainty.
- Do not inflate contributions.
- Make implications specific to the evaluated setting.
- Avoid promotional closure phrases.

Output only the revised LaTeX passage.

## Self-Review Prompt

Review the revised LaTeX passage against the original.

Return:

```json
{
  "meaning_preserved": true,
  "protected_tokens_preserved": true,
  "claim_strength_changed": false,
  "new_claims_added": false,
  "notes": []
}
```

If any value is unsafe, revise again before final output.

## Audit Summary Prompt

After revising, summarize changes in 3 bullets:

- Clarity:
- Specificity:
- Preserved LaTeX elements:

Do not mention detector scores or make pass/fail claims.
