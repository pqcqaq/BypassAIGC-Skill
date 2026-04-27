# Agent Workflow

Use this workflow when revising real `.tex` projects.

## Modes

- **Inspect**: read project structure, identify main `.tex`, audit labels/refs/cites.
- **Plan**: define scope, language, chapter order, and output format.
- **Extract**: create segment JSON or revision packet.
- **Diagnose**: for Chinese thesis prose, run style lint to find template-like or overloaded sentences.
- **Prompt**: render section-aware prompts from the revision packet.
- **Revise**: rewrite only prose fields or selected LaTeX blocks.
- **Lint**: check model output before applying it.
- **Apply**: apply approved revisions back to `.tex`.
- **Validate**: check protected tokens and, if available, compile LaTeX.
- **Report**: summarize what changed and what remains risky.

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

8. Apply revisions:

```bash
python scripts/apply_segment_revisions.py main.tex revision_packet.json --out main.revised.tex
```

9. Check protected tokens:

```bash
python scripts/latex_segmenter.py check main.tex main.revised.tex
```

10. Compile with the project's existing command when available.

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
