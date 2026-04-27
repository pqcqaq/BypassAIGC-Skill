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
- `chinese-humanize`: Chinese thesis prose flagged as template-like, abstract, overloaded, or too mechanically organized.
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

For `chinese-humanize`, also include:

- Findings from `scripts/chinese_ai_style_lint.py` when available.
- The suspected pattern: empty objective chain, over-neat parallelism, abstract noun stacking, unsupported value claim, boilerplate transition, detached "本文/本课题" subject, or long overloaded sentence.
- A reminder to shorten before adding detail.
- A reminder to anchor claims only to facts already present in the source.
- A reminder to remove self-referential assignment context such as "毕业设计周期" or "论文写作时" from normal thesis prose.

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
- "diagnose template-like Chinese thesis prose and make it shorter, more concrete, and source-grounded"

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

## Chinese Humanization Prompt Shape

For Chinese thesis prose that has already been flagged, use this compact task frame:

```text
先诊断再改写。重点查找空泛目标句、并列堆叠、抽象名词过密、价值判断无锚点、论文套话、自我提到毕业论文/写作过程的元话语和过长句。
保留 LaTeX、引用、术语、事实和结论强度。
先删减，再把保留下来的判断落到已有命令、模块、日志、接口、测试样例或章节事实上。
不要在正文里写“符合毕业设计周期”“论文写作时”这类站在论文外说论文的话。
输出：原句、问题、修改后、简短说明。
```

Do not ask the model to add deliberate mistakes, casual slang, or unverifiable personal traces.
