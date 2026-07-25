---
id: document
summary: "Materialize the delivered change into the target repo's documentation: user-facing docs updated, lasting decisions recorded as ADRs."
producer: builder
inputs:
  - name: change_summary
    description: "The implement stage's change record."
    format: markdown
    required: true
  - name: decisions
    description: "Machine-readable decision list from the design stage (decisions.json)."
    format: json
    required: true
  - name: target_repo
    description: "Path to the changed codebase."
    format: path
    required: true
outputs:
  - name: docs_change_summary
    file: docs_update.md
    format: markdown
    description: "Per-file record of every documentation change made in the target repo: what, why, and the behavior change it reflects."
  - name: docs_manifest
    file: docs_manifest.json
    format: json
    description: "JSON array of {path, action} for every documentation file created or modified in the target repo."
acceptance_criteria:
  - "Every user-visible behavior change in the change summary is reflected in the target repo's documentation, or docs_update.md declares it not doc-worthy with a stated reason."
  - "Every decision in decisions.json with lasting architectural impact is captured as an ADR following the target repo's existing ADR convention - or, if the repo has none, docs_update.md states where decisions are recorded instead."
  - "docs_manifest.json lists documentation files only - no source-code paths."
  - "Documentation claims match the change summary: nothing aspirational, nothing describing behavior that does not exist."
  - "Every target-repo file modified by this stage appears in docs_update.md with a rationale."
default_validators:
  - uses: validators/completeness-check
    with:
      target_repo: "workflow:target_repo"
  - uses: validators/persona-reviewer
    with:
      persona: "New team member using only the updated docs to understand, run, and roll back the change"
      target_repo: "workflow:target_repo"
knowledge_slots: [org-context]
skill_refs:
  - skillpacks/addyosmani/documentation-and-adrs
  - skillpacks/geoffreylitt/code-explainers
permissions:
  writes: [own_artifact_dir, target_repo]
---

# Document

## Purpose

Close the gap between what the code now does and what the repo says it does.
The implement stage changed behavior; this stage makes the repository the
system of record again — READMEs, API docs, changelogs, and ADRs for the
decisions that will outlive this change.

## Procedure

1. Read the change summary and decisions.json; list every user-visible
   behavior change and every decision with lasting impact.
2. Survey the target repo's documentation layout and conventions (README,
   docs/, existing ADR directory and format, changelog style). Follow what
   exists; invent nothing new without noting it in docs_update.md.
3. Update the documentation the behavior changes touch. Where a change needs
   no doc update, record why in docs_update.md.
4. Materialize ADRs: one record per lasting decision, in the repo's existing
   ADR format. ADRs are point-in-time records — supersede, never rewrite,
   earlier ones.
5. Write `docs_update.md` (per-file what/why) and `docs_manifest.json`
   (`[{"path": ..., "action": "created"|"modified"}]`).

## Output format constraints

`docs_update.md` sections in order: `# Documentation Update`, `## Behavior
changes covered` (change → doc location, or reason not doc-worthy),
`## Decisions recorded` (decision → ADR path, with inferred rationale flagged
as inferred), `## Files changed` (path → what/why), `## Knowledge gaps`.
`docs_manifest.json` is a JSON array of objects with exactly `path` and
`action` keys.

## Knowledge consumption

- `org-context`: documentation and ADR conventions of the organization, if
  attached; otherwise follow the target repo's visible conventions and note
  the gap under `## Knowledge gaps`.

## Boundaries

- Do NOT modify source code, tests, or configuration — documentation files
  only. The docs_manifest is checked for exactly this.
- Do NOT document behavior the change summary does not support; where the
  rationale for a decision is inferred rather than stated in decisions.json,
  flag it as inferred rather than presenting it as fact.
- Do NOT commit or push; leave changes in the working tree.

## Self-check before submitting

Cross-check docs_manifest.json against `git status` in the target repo: every
modified file is listed, every listed file is a documentation file. Re-read
each updated doc as the new-team-member persona: can they understand, run,
and roll back the change from the docs alone?

## Summary requirement

Write `summary.md` (≤200 words): how many docs and ADRs were touched, the
most important doc a reviewer should read, and any behavior change left
undocumented with its reason.
