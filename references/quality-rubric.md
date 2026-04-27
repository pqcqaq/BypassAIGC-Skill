# Quality Rubric

Use this rubric to judge revised academic prose.

## Must Preserve

- Claim meaning and strength.
- Citation attribution.
- Method sequence.
- Numerical values, units, dataset names, model names, and variables.
- LaTeX command syntax.

## Improve

- Specificity: replace broad claims with bounded statements.
- Flow: make transitions express actual relationships.
- Sentence rhythm: vary length without becoming casual.
- Terminology: preserve field terms and remove filler.
- Accountability: make clear what the paper shows, assumes, or leaves open.
- Paragraph progression: make each paragraph's role clear and reduce abrupt jumps.
- Audience fit: adjust terminology depth to the declared reader group.
- Style consistency: match formal, persuasive, explanatory, or reflective tone to the scene.

## Chinese AI-Like Style Rubric

Use this rubric when the target is Chinese thesis prose.

Score each dimension as low / medium / high risk:

- **Boilerplate density**: repeated "本文/本课题/基于上述/这表明/全文共分为".
- **Abstraction density**: many "机制/链路/能力/体系/方案/闭环/价值/意义" terms in one sentence.
- **Mechanical verbs**: repeated "设计/实现/构建/提供/提升/降低/形成/具备".
- **Parallelism**: neat but hollow structures such as "X 关注……目标是……".
- **Meta self-reference**: normal thesis prose mentions "毕业设计周期", "毕业论文中", "论文写作时", or assignment context.
- **Concrete evidence**: absence of commands, modules, logs, test cases, pages, APIs, or workflow steps already available in the source.
- **Sentence load**: one sentence carries background, method, implementation, and value at once.
- **Author presence**: wording sounds like a summary template rather than an author explaining implementation decisions.

Revision passes this rubric when:

- At least one abstract phrase is replaced by a concrete project object where possible.
- Long sentences are split without changing meaning.
- Value claims are bounded to a scenario or softened when evidence is limited.
- Self-referential assignment context is rewritten as engineering scope, implementation order, testability, or validation boundary.
- Required thesis structure remains, but bookkeeping sentences are shorter.

## Optional Task Rubric

Use this when the user requests broader rewriting beyond sentence polishing.

- **Paragraph structure**: each paragraph has one core point, a clear role, and a natural handoff to adjacent paragraphs.
- **Reader adaptation**: general-reader versions explain necessary terms; expert-reader versions keep precise terminology and avoid over-explaining basics.
- **Complexity control**: complex sentences are split before vocabulary polishing; no sentence carries unrelated claims.
- **Rhythm**: adjacent sentences do not repeat the same opening or length pattern without reason.
- **Precision expansion**: added details come from the source or are explicitly marked as needing author input.
- **Quote synthesis**: direct quotations are paraphrased or summarized without losing attribution or changing the cited claim.
- **Flowchart conversion**: every node corresponds to a source-supported step, decision, input, or output.
- **Personal perspective**: first-person or emotional wording appears only in suitable reflective or informal contexts and is grounded in provided material.

## Avoid

- Detector-score promises.
- "Groundbreaking", "significant" or "important" without evidence.
- Added citations or invented details.
- Overly casual wording in academic sections.
- Flattening all sentences into the same structure.
- Adding data, examples, personal memories, or emotional claims not present in the source.
- Using double negatives or synonym swaps in ways that reduce clarity.

## Final Checklist

- The revised text still says the same thing.
- All citations and labels remain unchanged.
- Equations and inline math remain unchanged.
- Chinese style findings from `chinese_ai_style_lint.py` were addressed or intentionally left.
- Paragraph, audience, quote, diagram, or personal-perspective requests followed their specific constraints.
- No Markdown syntax was introduced into `.tex`.
- The final answer names checks that were run.
