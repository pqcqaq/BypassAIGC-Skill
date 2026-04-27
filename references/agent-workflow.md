# Agent Workflow

Use this workflow when revising real `.tex` projects.

## Modes

- **Inspect**: read project structure, identify main `.tex`, audit labels/refs/cites.
- **Plan**: define scope, language, chapter order, and output format.
- **Extract**: create segment JSON or revision packet.
- **Revise**: rewrite only prose fields or selected LaTeX blocks.
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

3. Revise `revised_text` fields only. Leave a field empty if no change is needed.

4. Apply revisions:

```bash
python scripts/apply_segment_revisions.py main.tex revision_packet.json --out main.revised.tex
```

5. Check protected tokens:

```bash
python scripts/latex_segmenter.py check main.tex main.revised.tex
```

6. Compile with the project's existing command when available.

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
- Protected checks run.
- Whether compilation was run.
- Any unresolved risks, such as unresolved refs or skipped environments.
