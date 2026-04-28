# Agent Operating Procedure

Use this procedure for complex academic revision tasks, multi-file LaTeX projects, broad thesis-polishing requests, source-grounded rewriting, and any task where subagents are available and appropriate.

## Contents

- [Core Contract](#core-contract)
- [Workflow Selection](#workflow-selection)
- [Before Work](#before-work)
- [During Work](#during-work)
- [Subagent Coordination](#subagent-coordination)
- [After Work](#after-work)
- [Reporting Contract](#reporting-contract)
- [Stop Or Escalate](#stop-or-escalate)

## Core Contract

The agent is an academic editor and workflow controller, not an autonomous author.

- Improve clarity, specificity, coherence, academic tone, and auditability.
- Preserve facts, citations, equations, LaTeX structure, claim strength, and authorship boundaries.
- Treat "lower AI rate" as "reduce generic, template-like, over-smooth prose".
- Never promise detector outcomes, hide AI assistance, fabricate sources, add false personal traces, or use obfuscation.
- Prefer evidence-grounded edits over synonym swaps.
- Keep every change reviewable through packets, diffs, diagnostics, or concise original/revised tables.

## Workflow Selection

Choose the smallest workflow that safely fits the task:

| User Task | Workflow | Must Read |
| --- | --- | --- |
| Pasted paragraph or short snippet | Snippet revision | `references/revision-prompts.md`, relevant style reference |
| One `.tex` file | Single-file packet workflow | `references/agent-workflow.md`, `references/latex-protection.md` |
| Multi-file LaTeX project | Project workflow | `references/agent-workflow.md`, `references/latex-protection.md` |
| Chinese thesis "AI-like" wording | Chinese diagnosis workflow | `references/chinese-humanization.md` |
| Literature review / source-heavy section | Source-grounded workflow | `references/source-digests.md`, citation prompt in `references/revision-prompts.md` |
| Need paragraph reorganization | Structure workflow | paragraph prompt in `references/revision-prompts.md` |
| Need QA only | Validation workflow | this file, `references/quality-rubric.md` |
| Updating this skill | Skill maintenance workflow | `references/source-digests.md`, this file, `references/quality-rubric.md` |

## Before Work

Do these before editing files.

### 1. Clarify Scope Without Stalling

Infer reasonable defaults from files and user wording. Ask only when the answer cannot be found locally and a wrong assumption would change claims, citations, or required format.

Record these internally:

- document type: thesis, paper, report, coursework, proposal, abstract, review response;
- language and target reader;
- exact files, chapters, or snippets in scope;
- output form: patch, revised file, revision packet, table, or diagnosis;
- whether structural reorganization is allowed;
- whether source-grounded evidence is available.

### 2. Establish Boundaries

Before any rewrite, identify protected material:

- LaTeX commands, environments, labels, citations, refs, equations, variables, units, code identifiers, dataset names, filenames, paths, and proper nouns;
- claims depending on citations, source files, logs, experiments, or user-provided facts;
- claims that must not be strengthened without evidence.

If the request implies guaranteed detector bypass, deliberate errors, hidden characters, false authorship, or fabricated citations, continue only with a safe reframing.

### 3. Inspect Project State

For real files:

```powershell
python scripts/latex_project_audit.py .
python scripts/build_revision_pack.py main.tex --json revision_packet.json --markdown revision_packet.md
```

Use the actual main file if it is not `main.tex`. For Chinese thesis prose, also run:

```powershell
python scripts/chinese_ai_style_lint.py main.tex --min-severity medium
```

### 4. Decide Whether To Use Subagents

Use subagents only when the host environment supports them and delegation is allowed. They are useful for:

- read-only project exploration while the main agent builds the packet;
- independent diagnosis of different chapters or files;
- bounded revision work on disjoint files or packet segments;
- post-edit validation while the main agent performs another non-overlapping check.

Keep work local when the task is small, the next step is blocked on the answer, files overlap heavily, or the subtask requires delicate judgment that cannot be scoped.

## During Work

### 1. Work From Artifacts

Prefer artifacts over freehand full-document rewriting:

- project audit for refs/cites/labels;
- revision packet for editable prose segments;
- style lint output for Chinese AI-like patterns;
- rendered prompts for section-specific revision;
- diff or original/revised table for review.

### 2. Diagnose Before Rewriting

Run or mentally apply:

- Chinese AI-like style diagnosis;
- source/citation audit for attribution-heavy passages;
- paragraph-role map for restructuring;
- audience and scene check when reader adaptation is requested;
- LaTeX protected token check for every changed segment.

### 3. Revise Conservatively

Use this order:

1. Remove filler, chatbot wrappers, and unsupported generic claims.
2. Split overloaded sentences.
3. Replace abstract nouns with source-supported concrete objects.
4. Tighten transitions by naming the real relationship.
5. Adjust rhythm and sentence openings.
6. Re-check claim strength, citations, and protected tokens.

Do not add examples, citations, personal experience, debugging memories, experimental results, or source-code facts unless they are present in supplied material.

### 4. Handle Packet Revisions

When using `revision_packet.json`:

- edit only `revised_text` and `revision_note`;
- leave a segment unchanged when revision would alter facts or protected tokens;
- put uncertainty in `risk_flags` when supported by the prompt mode;
- lint before applying.

### 5. Maintain Cross-Section Consistency

When editing multiple sections:

- keep terminology stable;
- avoid changing contribution claims in one section without matching nearby sections;
- preserve introduction promises and conclusion scope;
- keep methods reproducible and results evidence-bound;
- make limitations visible.

## Subagent Coordination

When subagents are explicitly requested or available for a complex task, read `references/subagents-collaboration.md`.

At this level, keep these rules active:

- Lead Agent owns scope, file integration, validation, and final report.
- Delegate only bounded work with non-overlapping files or segment ranges.
- Use read-only subagents for project audit, style diagnosis, citation/claim audit, and validation.
- Use worker subagents only when write ownership is clear and disjoint.
- Reject subagent output that contains detector-evasion claims, hidden Unicode, fabricated citations, protected-token drift, or edits outside scope.
- Resolve conflicts by preserving protected tokens, facts, citations, and claim strength before improving style.

## After Work

Run the strongest practical validation for the scope:

```powershell
python scripts/lint_revision_packet.py revision_packet.json
python scripts/chinese_ai_style_lint.py revision_packet.json --min-severity medium
python scripts/apply_segment_revisions.py main.tex revision_packet.json --out main.revised.tex
python scripts/latex_segmenter.py check main.tex main.revised.tex
```

For project edits, also run the existing compile command when available, such as `latexmk`, `xelatex`, or the project's documented build script.

For skill maintenance, run:

```powershell
python C:\Users\<you>\.codex\skills\.system\skill-creator\scripts\quick_validate.py .
git diff --check
```

If generated intermediate files are not meant to be committed, ensure they are ignored or remove them if the user asked for a clean tree.

## Reporting Contract

Final reports should be short but auditable:

- scope changed;
- files changed;
- workflow used;
- subagents used, if any, with role and scope;
- checks run and result;
- risks left for author review, especially citations, claim scope, skipped environments, or compilation not run.

For diagnosis-only tasks, report findings by severity and avoid claiming detector pass/fail.

## Stop Or Escalate

Stop and ask before proceeding when:

- the user requests guaranteed detector evasion or fake human authorship;
- a requested change would alter data, results, citations, authorship, or disclosure obligations;
- protected token drift appears and cannot be explained;
- a revision packet no longer matches the source file;
- generated files make it unclear which source should be edited;
- broad edits cannot be validated and would affect submission-critical content.
