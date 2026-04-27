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

## Chinese Thesis Humanization Prompt

Use this for Chinese graduation-thesis or technical-report prose that has been flagged as generic, AI-like, too neat, too abstract, or too verbose.

Task:
- First diagnose the sentence-level problems.
- Then rewrite into concise, concrete, thesis-appropriate Chinese.
- Keep the wording natural enough to sound like an author explaining a real project, but not casual or chatty.

High-priority issues to fix:
- Empty objective chains: "设计/实现/构建/提供/形成" plus "机制/链路/能力/体系/方案".
- Over-neat parallelism: repeated "关注……目标是……" or list-like summaries that hide the actual work.
- Abstract noun stacking: too many "机制、链路、闭环、价值、能力、支撑、沉淀、复用".
- Unsupported value claims: "降低风险、提升效率、提供保护、具备能力" without a concrete scene.
- Boilerplate transitions: "基于上述问题、这表明、需要补充说明的是、全文共分为六章".
- Meta thesis self-reference: "毕业设计周期、毕业论文中、论文写作时、本毕业设计" used inside normal thesis prose.
- Long overloaded sentences mixing background, method, value, and implementation.

Rewrite rules:
- Preserve all LaTeX commands, citations, labels, equations, code identifiers, module names, and technical terms.
- Do not add facts, citations, experiments, source-code details, or examples that are not already present.
- Shorten before adding detail.
- Do not mention "graduation thesis/design", "paper writing", or assignment-cycle context in the revised passage unless the source section explicitly requires that topic.
- Use concrete anchors already present in the source: commands, modules, APIs, logs, tests, workflows, pages, endpoints, or code files.
- Prefer "用来识别/先提示/接到具体链路里/把范围缩小/在该原型中" over "提供帮助/具备能力/形成闭环".
- Keep claim strength unchanged or slightly more cautious.

Output format:

```json
{
  "diagnosis": [
    {
      "original": "source sentence",
      "issue": "short issue label",
      "revision": "revised sentence",
      "note": "why this is better"
    }
  ],
  "revised_text": "full revised passage"
}
```

Text:

```latex
{{TEXT}}
```

## Chinese AI-Like Sentence Diagnosis Prompt

Review the Chinese thesis sentences below. Do not rewrite yet.

Return a compact table with:

- sentence
- severity: high / medium / low
- pattern
- concrete rewrite direction

Judge severity by:

- high: empty value claim, heavy template wording, long overloaded list, or unsupported "降低/提升/提供/形成" claim.
- high: self-referential thesis context such as "毕业设计周期" or "论文写作时" inside normal prose.
- medium: mechanical objective sentence, repeated thesis subject, abstract noun density, or boilerplate transition.
- low: minor smoothness or rhythm issue.

Text:

```text
{{TEXT}}
```

## Compress And Concretize Prompt

Rewrite the Chinese academic passage by compressing filler and adding concreteness only from the source.

Constraints:
- Keep all citations, LaTeX commands, equations, module names, command names, and code identifiers unchanged.
- Do not add new facts.
- Split sentences longer than 90 Chinese characters when possible.
- Replace broad phrases such as "提供帮助", "具备能力", "形成闭环", "完成集成与重组" with concrete action.
- Remove self-referential thesis context such as "毕业设计周期" unless the section is explicitly about project management or teaching requirements.
- Preserve thesis tone.

Output only the revised passage.

## Chinese Rewrite Examples

These examples show the preferred direction. They are not detector guarantees.

| AI-like sentence | Better revision | Reason |
| --- | --- | --- |
| 这种渐进式实现方式符合毕业设计周期，也能降低单点失败风险。 | 按模块分阶段做，可以先把各层分别调通；哪一层出问题，也能先缩小范围，而不是让整套系统一起停住。 | Removes self-referential graduation-design wording and keeps the engineering logic. |
| 它不要求企业先建设庞大的AIOps平台，却能在最常用的运维入口提供保护。 | 这套方案不需要先搭一整套 AIOps 平台，而是先守住 Shell 这个最常用、也最容易出错的入口。 | Replaces "提供保护" with the actual protected entry point. |
| 这表明，本课题并非从零构造全部技术能力，而是在现有技术基础上完成面向业务链的集成与重组。 | 因此，本课题的重点不在于重新发明这些基础能力，而是把它们接到命令拦截、异常诊断和知识复用这条具体链路里。 | Removes boilerplate and names the chain. |
| 设计基于大语言模型与RAG的诊断链路，实现命令异常的结构化解释与建议生成。 | 接入大语言模型和 RAG 后，系统可以把命令输出、日志片段和相似案例整理到同一条诊断流程里，再生成原因说明和下一步建议。 | Names the inputs and output of the chain. |
| 上层的大语言模型调用、Sentence-BERT向量化、Faiss相似检索以及React + Ant Design + Oak界面组织也已有较成熟方案。 | 上层能力也不需要从零做起。模型调用可以接入现有大语言模型接口，向量化和相似检索分别由 Sentence-BERT 与 Faiss 承担，前端则沿用 React、Ant Design 和 Oak 的组合。 | Splits an overloaded technical list. |

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
