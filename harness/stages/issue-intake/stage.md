---
id: issue-intake
summary: "Turn a raw list of issues into per-issue briefs: understood root cause, affected files, and testable acceptance criteria for every issue."
producer: planner
inputs:
  - name: issues
    description: "The issue list, verbatim: pasted descriptions, a path to a file listing them, or public issue URLs (fetchable)."
    format: markdown
    required: true
  - name: target_repo
    description: "Path to the codebase the issues are reported against."
    format: path
    required: true
outputs:
  - name: issue_briefs
    file: issue_briefs.md
    format: markdown
    description: "Human-readable per-issue brief: problem, root-cause hypothesis with code evidence, acceptance criteria, open questions."
  - name: issue_manifest
    file: issue_manifest.json
    format: json
    description: "Machine-readable issue list: [{id, slug, title, summary, root_cause_hypothesis, affected_files, branch, acceptance_criteria, open_questions}]."
acceptance_criteria:
  - "issue_manifest.json parses as a JSON array with exactly one entry per input issue - no issue is dropped, merged, split, or invented; ids are ISS-<n> and each entry carries id, slug, title, summary, root_cause_hypothesis, affected_files, branch, and acceptance_criteria."
  - "Every issue has at least one testable acceptance criterion: a check someone could run in the repo and get a yes/no answer (a command, a reproducible scenario, or an observable behavior)."
  - "Every root_cause_hypothesis cites concrete evidence from the target repo (file path plus symbol or line) or is explicitly marked 'unconfirmed' with the investigation still needed."
  - "Slugs are unique kebab-case; every branch is fix/<slug> and a valid git ref name; no two issues share a slug or branch."
  - "Ambiguities are recorded per issue under open_questions, never silently resolved; an issue too vague to yield a testable criterion is marked status needs-clarification in the brief rather than given invented criteria."
default_validators:
  - uses: validators/completeness-check
    with:
      extra_check: "every issue that appears in issue_briefs.md appears in issue_manifest.json with the same id, and vice versa; acceptance_criteria arrays are non-empty for every issue not marked needs-clarification."
  - uses: validators/adversarial-reviewer
    with:
      focus: "untestable acceptance criteria, misdiagnosed root causes, issues silently merged or dropped, criteria that restate the fix instead of the observable outcome"
knowledge_slots: [org-context, personal-notes]
skill_refs:
  - skillpacks/addyosmani/spec-driven-development
permissions:
  writes: [own_artifact_dir]
---

# Issue Intake

## Purpose

The batch counterpart of intake: turn a raw list of issues into a set of
independently actionable briefs, each with testable acceptance criteria. Every
downstream gate in a batch-fix run judges against what this stage writes, so
the criteria here define what "fixed" means per issue.

## Procedure

1. Enumerate the issues from the `issues` input. If it is a path, read the
   file; if entries are URLs, fetch each one and record the fetch date; if it
   is pasted text, split it into individual issues without merging or
   dropping any.
2. Per issue, read the target repo to locate the implicated code. Write a
   root-cause hypothesis citing file paths and symbols or lines; if the code
   does not confirm it, mark it `unconfirmed` and state what investigation
   would settle it.
3. Derive acceptance criteria per issue: runnable yes/no checks (a command, a
   reproducible scenario, an observable behavior). Criteria describe the
   observable outcome, never the intended code change.
4. Assign each issue an id `ISS-<n>` (in input order), a unique kebab-case
   slug, and branch `fix/<slug>`.
5. Record per-issue ambiguities under open questions; an issue too vague for
   a testable criterion gets status `needs-clarification`, not invented
   criteria.
6. Note cross-issue overlaps (shared files, conflicting fixes) so planning
   can order the work.

## Output format constraints

`issue_briefs.md` sections in order: `# Issue Briefs`, `## Issues` (one
`### ISS-<n>: <title>` subsection each with `Slug:`, `Branch:`, `Summary:`,
`Root cause hypothesis:`, `Acceptance criteria:` numbered list,
`Open questions:`), `## Cross-issue notes` (shared files or conflicts; "none"
if none), `## Knowledge gaps`. `issue_manifest.json`: JSON array of
`{"id", "slug", "title", "summary", "root_cause_hypothesis",
"affected_files", "branch", "acceptance_criteria", "open_questions"}`.

## Knowledge consumption

- `org-context`: issue-tracker context, prior related fixes, and owning-team
  conventions if attached; cite as "per <source>".
- `personal-notes`: the requester's earlier notes on these issues if attached.
- No adapter attached or adapter fails: proceed from the issue text and the
  repo alone, and record what was unavailable under `## Knowledge gaps`.

## Boundaries

- Do NOT fix anything, write code, or create branches or worktrees — this
  stage only defines the work.
- Do NOT invent issues or acceptance criteria the issue text and code
  evidence do not support.
- Do NOT collapse similar issues into one entry; note the overlap in
  cross-issue notes instead.

## Self-check before submitting

Per issue, ask: could someone run each criterion and get an unambiguous
yes/no? Count entries in both artifacts and confirm each matches the input
list exactly, with ids agreeing between the two.

## Summary requirement

Write `summary.md` (≤200 words): issue count, the hardest issue, any
unconfirmed root causes, and open questions that block planning.
