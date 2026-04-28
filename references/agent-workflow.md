# Agent Workflow

Use this workflow when revising real `.tex` projects.

For broad orchestration, read `references/agent-operating-procedure.md` first. For delegated or parallel work, also read `references/subagents-collaboration.md`.

## Modes

- **Inspect**: read project structure, identify main `.tex`, audit labels/refs/cites.
- **Plan**: define scope, language, chapter order, and output format.
- **Extract**: create segment JSON or revision packet.
- **Diagnose**: for Chinese thesis prose, run style lint to find template-like or overloaded sentences.
- **Source Audit**: identify citation-dependent claims, project facts, missing evidence, and author-review risks.
- **Prompt**: render section-aware prompts from the revision packet.
- **Revise**: rewrite only prose fields or selected LaTeX blocks.
- **Lint**: check model output before applying it.
- **Apply**: apply approved revisions back to `.tex`.
- **Validate**: check protected tokens and, if available, compile LaTeX.
- **Report**: summarize what changed and what remains risky.

## Before / Intake

1. Classify the request: diagnosis, snippet revision, single-file edit, multi-file project, validation, prompt generation, or read-only review.
2. Confirm edit permission from the user wording. If the user asks for review, analysis, or audit only, stay read-only.
3. Identify the minimal reference set to read. Do not load every reference file by default.
4. Identify risk level:
   - low: grammar and clarity edits inside one snippet;
   - medium: file edits, Chinese AI-like wording, source-grounded claim edits;
   - high: citations, results, data, authorship, disclosure, detector-evasion wording, broad project rewrites.
5. Ask only for blocking information: main file, target chapter, output format, or permission to edit.

## Read-Only Mode

When read-only:

- allowed: inspect files, run audits that do not write artifacts, search text, report findings;
- disallowed: applying revisions, writing packet JSON/Markdown, formatting files, modifying source, or creating replacement `.tex` outputs;
- if a script normally writes output, either skip it or ask permission to create the artifact.

## Stage Gates

Do not skip these gates for file edits:

1. **Inspect gate**: know the target file and protected structure.
2. **Plan gate**: define scope, mode, and whether source-grounding is required.
3. **Extract gate**: build or identify editable prose segments.
4. **Diagnose gate**: run style/source checks when relevant.
5. **Revise gate**: change only prose-bearing segments in scope.
6. **Lint gate**: lint packet or changed file before applying.
7. **Apply gate**: apply revisions only after lint is clean or risks are understood.
8. **Validate gate**: protected-token check and compile/build when available.
9. **Report gate**: separate executed checks, skipped checks, residual risks, and author-review items.

## Required Sequence For File Edits

1. Run project audit:

```bash
python scripts/latex_project_audit.py .
```

2. Extract or build a packet:

```bash
python scripts/build_revision_pack.py main.tex --json revision_packet.json --markdown revision_packet.md
```

3. For Chinese thesis prose or "AI-like" wording tasks, run style diagnosis:

```bash
python scripts/chinese_ai_style_lint.py main.tex --min-severity medium
python scripts/chinese_ai_style_lint.py revision_packet.json --min-severity medium
```

Use the findings to prioritize revisions. Treat them as heuristic style warnings, not detector predictions.

4. Render prompts for the target segments:

```bash
python scripts/render_revision_prompt.py revision_packet.json --segment 0 --mode auto
python scripts/render_revision_prompt.py revision_packet.json --segment 0 --mode chinese-humanize
```

Use `chinese-humanize` when the segment contains Chinese graduation-thesis prose with empty objective chains, abstract noun stacking, or over-neat parallelism.

Use `source-grounded` when the segment contains claims that depend on supplied citations, project files, datasets, logs, or implementation facts:

```bash
python scripts/render_revision_prompt.py revision_packet.json --segment 0 --mode source-grounded
```

5. Revise `revised_text` fields only. Leave a field empty if no change is needed.

6. Lint the packet:

```bash
python scripts/lint_revision_packet.py revision_packet.json
```

7. Re-run Chinese style diagnosis on the packet when the revision target is Chinese prose:

```bash
python scripts/chinese_ai_style_lint.py revision_packet.json --min-severity medium
```

Remaining findings are acceptable when a term is technically required or further changes would alter the claim.
Pay particular attention to high-severity findings such as hidden Unicode, vague attribution without citation, and meta thesis self-reference.

8. Apply revisions:

```bash
python scripts/apply_segment_revisions.py main.tex revision_packet.json --out main.revised.tex
```

9. Check protected tokens:

```bash
python scripts/latex_segmenter.py check main.tex main.revised.tex
```

10. Compile with the project's existing command when available.

## During / Execution Rules

- Work in batches by chapter, file, or segment range for long projects.
- Re-check packet freshness if the user changes scope or files change during work.
- Keep generated packet metadata stable; edit only approved fields.
- Preserve original language unless translation is explicitly requested.
- Mark missing evidence as `needs_author_input`; do not fill it from memory.
- Prefer smaller edits when two revisions are both acceptable.
- If a user interrupts with a new requirement, make the newest request authoritative and revalidate any existing packet or plan.

## After / Reporting

Final reports must distinguish:

- checks run and their outcomes;
- checks not run and why;
- changed files or produced artifacts;
- findings intentionally left unchanged;
- unresolved risks, especially citation context, claim scope, skipped LaTeX environments, and compilation not run.

When stopping early, report the stop reason, exact location if known, and the next safe action.

## Stop Conditions

Stop and ask the user before editing when:

- The project has generated `.tex` files and the source is unclear.
- The requested scope includes rewriting claims, results, or citations.
- The packet no longer matches the current file.
- Protected token drift appears and cannot be explained.
- The user asks for detector bypass guarantees.

## Output Standards

For each revision batch, report:

- Files changed.
- Scope revised.
- Chinese style findings addressed or intentionally left.
- Protected checks run.
- Whether compilation was run.
- Any unresolved risks, such as unresolved refs or skipped environments.
