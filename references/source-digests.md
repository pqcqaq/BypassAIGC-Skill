# Source Digests

This file records the outside projects reviewed while expanding this skill. It is a distillation log, not a vendored copy of those projects.

## License And Use Filter

When using outside prompt repositories, apply these rules:

- Prefer high-level workflow ideas, checklists, and prompt architecture over copied prompt text.
- Do not import detector-evasion instructions, deliberate errors, hidden Unicode tricks, or "guaranteed score" claims.
- Keep license constraints visible. CC BY-NC-SA and AGPL sources should inform methodology only unless this repository's license is changed or a compatible reuse path is chosen.
- If a source repository has no license, treat it as "read for inspiration only" and do not copy text.
- Attribute sources in `NOTICE` and this file when a meaningful idea is distilled.

## Reviewed Sources

| Source | Cloned Path | License Observed | Safe Distillation |
| --- | --- | --- | --- |
| `chi111i/BypassAIGC` | `D:\Develop\Projects\tmps\BypassAIGC` | CC BY-NC-SA 4.0 | Staged paper polishing, segmentation before model calls, configurable prompts, history/style compression, and visible academic integrity warnings. |
| `brandonwise/humanizer` | `D:\Develop\Projects\tmps\humanizer` | MIT | Pattern-based style diagnostics: significance inflation, vague attribution, formulaic structure, repeated phrase families, sentence uniformity, and hidden Unicode warnings. |
| `BevalZ/awesome-prompt-for-academic` | `D:\Develop\Projects\tmps\awesome-prompt-for-academic` | MIT | Academic prompt organization by task, placeholder-driven templates, clarity/coherence checklists, and multilingual prompt consistency. |
| `xuhangc/ChatGPT-Academic-Prompt` | `D:\Develop\Projects\tmps\ChatGPT-Academic-Prompt` | MIT | LaTeX-preserving academic polishing patterns, modification tables, section-aware prompts, and conference-paper editing scenarios. |
| `ahmetbersoz/chatgpt-prompts-for-academic-writing` | `D:\Develop\Projects\tmps\chatgpt-prompts-for-academic-writing` | No license file found | High-level task taxonomy only: research questions, abstracts, literature review, clarity, coherence, proofreading, and planning. |
| `federicodeponte/opendraft` | `D:\Develop\Projects\tmps\opendraft` | MIT | Research workflow phases, citation verification, narrative consistency QA, voice unification QA, fact-check QA, and quality gates. |
| `linshenkx/prompt-optimizer` | `D:\Develop\Projects\tmps\prompt-optimizer` | AGPL-3.0-only | Prompt iteration method only: analyze, test, evaluate, compare, then revise prompt variables and constraints. No code or prompt text is reused. |
| `f/awesome-chatgpt-prompts` | `D:\Develop\Projects\tmps\awesome-chatgpt-prompts` | MIT / CC0 files present | Generic prompt-library conventions: role, task, input placeholder, output contract. Evasion-oriented prompts are explicitly rejected. |

## Distilled Workflow Additions

### 1. Source-Grounded Intake

Before revising a real academic passage, identify:

- document type, section type, language, and target reader;
- supplied evidence: source text, project files, datasets, logs, citations, or examples;
- protected elements: LaTeX commands, citations, labels, math, variables, numbers, proper nouns, and claim boundaries;
- missing facts that should be marked as `needs_author_input` rather than invented.

### 2. Diagnosis Before Rewrite

Run or mentally apply these checks before editing:

- generic thesis wording: empty objective chains, boilerplate transitions, over-neat parallelism;
- inflated significance: broad "important", "critical", "transformative", or "显著提升" claims without scope;
- vague attribution: "studies show", "研究表明", or similar phrases without a visible source;
- rhythm issues: all sentences similar length, repeated openings, excessive list structure;
- chat artifacts: assistant greetings, "hope this helps", "下面我将", or Markdown wrappers in prose;
- obfuscation artifacts: zero-width characters, soft hyphens, non-breaking spaces, or hidden direction controls.

### 3. Rewrite Policy

Use the smallest edit that fixes the issue:

- shorten filler before adding new detail;
- replace abstract nouns with objects already present in the source;
- keep value claims bounded to a scenario, method, result, module, or citation;
- preserve paragraph count unless restructuring is requested;
- keep section voice consistent: methods should be reproducible, results should separate observation from interpretation, conclusions should retain limitations.

### 4. QA After Rewrite

After revision, check:

- protected tokens are unchanged;
- no new citation, dataset, result, personal memory, or source-code fact was invented;
- vague attribution is either cited or rewritten;
- terminology is consistent across nearby paragraphs;
- the revision did not insert Markdown fences, chatbot wrappers, or hidden Unicode;
- any remaining unresolved detail is reported as `needs_author_input`.

### 5. Prompt Iteration Loop

When creating or improving a prompt for this skill:

1. Write the task frame, boundaries, LaTeX protection, objective, and output contract.
2. Test it on a small representative segment.
3. Evaluate output against the quality rubric.
4. Compare the prompt and output with the prior version.
5. Revise the prompt by adding only constraints that address observed failures.
6. Avoid adding vague style goals that cannot be audited.
