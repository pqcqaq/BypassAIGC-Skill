# Subagents Collaboration

Use this reference when the task explicitly involves subagents, delegated review, parallel chapter work, independent validation, or multi-agent academic revision.

## Contents

- [Principles](#principles)
- [Roles](#roles)
- [Collaboration Boundaries](#collaboration-boundaries)
- [Input Contract](#input-contract)
- [Output Contract](#output-contract)
- [Parallel And Serial Rules](#parallel-and-serial-rules)
- [Conflict Handling](#conflict-handling)
- [Failure Handling](#failure-handling)
- [Handoff Templates](#handoff-templates)

## Principles

- Lead Agent owns user communication, final decisions, file integration, and final report.
- Subagents help with bounded work. They do not decide authorship, citation truth, disclosure obligations, or final acceptance.
- Give each subagent a concrete scope, file list, segment range, protected constraints, and output schema.
- Prefer read-only subagents for audit, diagnosis, and validation.
- Use worker subagents only for disjoint write scopes.
- Never let subagents silently fix conflicts involving facts, citations, results, or claim strength.

## Roles

| Role | Purpose | Allowed Actions | Forbidden Actions |
| --- | --- | --- | --- |
| Lead Agent | Plan, coordinate, edit critical sections, integrate, validate, report | Read/write within user scope | Offload final responsibility |
| Project Auditor | Find root files, includes, labels, refs, cites, generated files, build commands | Read-only analysis | Rewrite prose or files |
| Style Diagnoser | Identify Chinese AI-like wording, boilerplate, abstract claims, rhythm issues | Read-only findings | Rewrite unless reassigned |
| Revision Agent | Revise assigned prose segments or one chapter | Edit assigned `revised_text` or assigned file only | Touch protected tokens or other scopes |
| Citation/Claim Auditor | Check attribution, claim strength, new facts, source grounding | Read-only findings and risk flags | Invent or repair citations |
| LaTeX Validator | Check protected tokens, packet match, compile risk, environment drift | Read-only validation or assigned checks | Rewrite content to make checks pass |
| Report Agent | Summarize changes, risks, and checks from artifacts | Read-only synthesis | Hide unresolved risks |

## Collaboration Boundaries

- Subagents must not overwrite source files unless Lead Agent gives explicit write ownership.
- Subagents must not modify another subagent's output; they may report conflicts.
- Subagents must not edit generated packet metadata such as `start`, `end`, `line_start`, `line_end`, or original `text`.
- Subagents must not decide to add citations, data, experiments, personal experiences, or AI-use disclosures.
- All factual additions or claim-strength changes return to Lead Agent as `needs_author_input` or `claim_scope` risk.
- A subagent output that cannot be traced to a source file, segment, or supplied evidence is advisory only.

## Input Contract

Every subagent prompt should include:

```text
Task:
Scope:
Files or segment range:
Allowed edits:
Protected constraints:
References to read:
Checks to run:
Output format:
Coordination note: other agents may be working; do not revert unrelated changes.
```

Minimum required fields:

- `Task`: one sentence with the concrete result needed.
- `Scope`: exact file paths, chapter names, or segment indices.
- `Allowed edits`: `read-only`, `revision_packet fields only`, or exact file ownership.
- `Protected constraints`: citations, labels, math, commands, claim strength, language, paragraph count.
- `Output format`: one of the contracts below.

## Output Contract

### Audit Subagent

```json
{
  "summary": "short summary",
  "findings": [
    {
      "location": "file:line or segment",
      "severity": "high | medium | low",
      "issue": "what is wrong",
      "evidence": "source-grounded evidence",
      "suggestion": "safe next step"
    }
  ],
  "risk_flags": [],
  "confidence": "high | medium | low"
}
```

Audit subagents must not include full rewrites unless explicitly asked.

### Revision Subagent

```json
{
  "summary": "short summary",
  "proposed_changes": [
    {
      "segment_index": 0,
      "revised_text": "revised prose only",
      "revision_note": "one sentence",
      "risk_flags": []
    }
  ],
  "checks_run": [],
  "confidence": "high | medium | low"
}
```

Revision output must preserve protected tokens. If the subagent is editing files directly, it must also list changed file paths.

### Validation Subagent

```json
{
  "summary": "validation summary",
  "checks_run": [],
  "failures": [
    {
      "location": "file:line or segment",
      "failure": "protected_token_drift | packet_mismatch | claim_drift | citation_risk | compile_risk",
      "evidence": "observed evidence",
      "recommended_action": "what Lead Agent should do"
    }
  ],
  "risk_flags": [],
  "confidence": "high | medium | low"
}
```

## Parallel And Serial Rules

Can run in parallel:

- project audit and style diagnosis;
- citation risk scan and LaTeX root detection;
- independent chapter revisions with non-overlapping files;
- validation review while Lead Agent checks a different artifact.

Must be serial:

- revision after audit/diagnosis when protected structure is unknown;
- apply after packet lint;
- final validation after all revisions are integrated;
- report after validation and conflict resolution.

Multiple revision subagents may work in parallel only when their segment ranges or files do not overlap. Shared abstract, introduction, conclusion, macros, bibliography, and preamble usually stay with Lead Agent.

## Conflict Handling

When outputs conflict, Lead Agent chooses by this order:

1. Preserves protected tokens.
2. Preserves facts and citation attribution.
3. Keeps claim strength equal or more cautious.
4. Stays traceable to source evidence.
5. Fits section voice and surrounding terminology.
6. Improves readability.

Specific rules:

- Citation accuracy beats smoother prose.
- Source grounding beats more "human" style.
- LaTeX validity beats paragraph-level style.
- If two rewrites are both safe, choose the smaller edit.
- If conflict involves facts, citations, results, authorship, or disclosure, do not silently merge; report it or ask the user.

## Failure Handling

Reject or quarantine subagent output when it contains:

- Markdown fences inside `revised_text`;
- hidden Unicode, zero-width characters, or soft hyphens;
- detector-bypass promises or score claims;
- fabricated citations, DOI values, datasets, experiments, or personal memories;
- protected token drift;
- edits outside assigned scope;
- untraceable claims.

If the failure is repairable, Lead Agent may revise the output locally after rechecking protected tokens. If it changes facts or citations, ask the user or mark `needs_author_input`.

## Handoff Templates

### Project Auditor Prompt

```text
Task: Audit the LaTeX project structure.
Scope: <repo or project path>
Allowed edits: read-only.
Protected constraints: do not modify files or generate revisions.
References to read: SKILL.md, references/agent-workflow.md, references/latex-protection.md.
Checks to run: latex_project_audit if available; otherwise inspect files.
Output format: Audit Subagent JSON with root candidates, included files, labels/refs/cites risks, generated-file risks, and suggested build command.
Coordination note: other agents may be working; do not revert unrelated changes.
```

### Style Diagnoser Prompt

```text
Task: Diagnose Chinese thesis prose for template-like or AI-like phrasing.
Scope: <file or segment range>
Allowed edits: read-only.
Protected constraints: do not rewrite; do not mention detector pass/fail.
References to read: references/chinese-humanization.md, references/quality-rubric.md.
Checks to run: chinese_ai_style_lint if available.
Output format: Audit Subagent JSON with severity, location, pattern, evidence, and rewrite direction.
Coordination note: other agents may be working; do not revert unrelated changes.
```

### Revision Agent Prompt

```text
Task: Revise only assigned prose segments.
Scope: <segment indices or file path>
Allowed edits: revision_packet fields only: revised_text, revision_note, risk_flags.
Protected constraints: preserve citations, labels, refs, math, commands, proper nouns, numbers, claim strength, language, and paragraph count.
References to read: references/revision-prompts.md, references/quality-rubric.md, and relevant style reference.
Checks to run: self-check protected tokens; run packet lint if assigned.
Output format: Revision Subagent JSON or changed file list plus checks.
Coordination note: other agents may be working; do not revert unrelated changes.
```

### Citation/Claim Auditor Prompt

```text
Task: Check revised passages for claim drift and citation risks.
Scope: <diff, packet, or file range>
Allowed edits: read-only.
Protected constraints: do not invent or repair citations.
References to read: references/revision-prompts.md Citation And Claim Audit Prompt, references/quality-rubric.md.
Checks to run: compare original and revised claims manually; inspect citation context.
Output format: Validation Subagent JSON.
Coordination note: other agents may be working; do not revert unrelated changes.
```

### LaTeX Validator Prompt

```text
Task: Validate LaTeX safety after revisions.
Scope: <original file, revised file, packet>
Allowed edits: read-only unless explicitly assigned fixes.
Protected constraints: do not rewrite prose to hide failures.
References to read: references/latex-protection.md, references/agent-workflow.md.
Checks to run: lint_revision_packet, latex_segmenter check, compile command if available.
Output format: Validation Subagent JSON.
Coordination note: other agents may be working; do not revert unrelated changes.
```
