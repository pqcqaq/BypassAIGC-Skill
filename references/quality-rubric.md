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

## Avoid

- Detector-score promises.
- "Groundbreaking", "significant" or "important" without evidence.
- Added citations or invented details.
- Overly casual wording in academic sections.
- Flattening all sentences into the same structure.

## Final Checklist

- The revised text still says the same thing.
- All citations and labels remain unchanged.
- Equations and inline math remain unchanged.
- Chinese style findings from `chinese_ai_style_lint.py` were addressed or intentionally left.
- No Markdown syntax was introduced into `.tex`.
- The final answer names checks that were run.
