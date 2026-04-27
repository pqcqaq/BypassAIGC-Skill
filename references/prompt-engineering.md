# Prompt Engineering Protocol

Use this protocol when creating prompts for LaTeX academic revision.

## Prompt Stack

Each prompt should have five layers in this order:

1. **Task frame**: state the section type and language.
2. **Safety boundary**: no detector promises, no fabricated claims, no citation changes.
3. **LaTeX boundary**: preserve commands, math, references, labels, environments.
4. **Revision objective**: reduce generic AI-like phrasing by improving specificity, flow, and claim discipline.
5. **Output contract**: return either only revised LaTeX or a strict JSON object.

## Section Mode Selection

Select the most specific mode:

- `abstract`: abstract, 摘要.
- `introduction`: introduction, intro, 引言, 绪论.
- `related-work`: related work, literature review, 相关工作, 文献综述.
- `methods`: method, methodology, approach, 方法, 研究设计.
- `results`: results, experiment, evaluation, 结果, 实验, 评价.
- `discussion`: discussion, conclusion, 讨论, 结论.
- `chinese`: Chinese prose outside a clearer section mode.
- `english`: English prose outside a clearer section mode.
- `universal`: mixed or uncertain text.

## Prompt Requirements

Always include:

- Original passage.
- Detected language.
- Section mode.
- Section hint when available.
- Protected LaTeX tokens found in the passage.
- Explicit instruction not to alter protected tokens.
- Explicit instruction not to add citations, data, or claims.
- Output schema.

## Output Schemas

For packet editing, prefer JSON:

```json
{
  "revised_text": "...",
  "revision_note": "...",
  "risk_flags": []
}
```

Rules:

- `revised_text` must contain valid LaTeX text only.
- `revision_note` must be one sentence.
- `risk_flags` must list uncertainties such as `claim_strength`, `citation_context`, `needs_author_review`, or be empty.

For direct snippet revision, use LaTeX-only output when the user asks for direct replacement.

## Anti-Patterns

Avoid prompts that say:

- "bypass AI detection"
- "make it undetectable"
- "guarantee lower AI score"
- "rewrite aggressively"
- "add human errors"
- "change wording until detector passes"

Use instead:

- "reduce generic AI-like phrasing"
- "make claims more bounded and context-aware"
- "preserve academic integrity and LaTeX structure"

## Auto-Mode Heuristic

Prefer explicit section hints over words inside the paragraph. For example, the word "method" inside an introduction paragraph does not make the passage a methods section. When a packet contains `section_hint`, choose mode from that heading first and use paragraph text only as a fallback.

## Self-Check Prompt

After drafting a revision, run this mental checklist:

1. Did any protected token change?
2. Did the revision add a claim not present in the original?
3. Did the revision inflate certainty or novelty?
4. Did the revision preserve the original language?
5. Does the revised paragraph still fit the surrounding section?

If any answer is unsafe, revise again before returning.
