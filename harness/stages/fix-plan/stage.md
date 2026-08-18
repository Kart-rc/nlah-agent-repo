---
id: fix-plan
summary: "Break each issue's fix into small, ordered, independently verifiable steps scoped to that issue's future worktree."
producer: planner
inputs:
  - name: issue_briefs
    description: "Per-issue briefs with acceptance criteria (from issue-intake)."
    format: markdown
    required: true
  - name: issue_manifest
    description: "Machine-readable issue list (from issue-intake)."
    format: json
    required: true
  - name: target_repo
    description: "Path to the codebase to plan against."
    format: path
    required: true
outputs:
  - name: fix_plan
    file: fix_plan.md
    format: markdown
    description: "Per-issue ordered fix steps with files, verification commands, and rollback notes, plus cross-issue ordering."
acceptance_criteria:
  - "Every issue id in issue_manifest.json has its own plan section, and no section exists for an issue id absent from the manifest."
  - "Every step names the files it touches and a concrete verification: a command runnable inside that issue's worktree, or an observable check."
  - "Each issue's plan maps every one of its acceptance criteria to the step(s) and verification command(s) that will prove it (per-issue traceability)."
  - "Steps for one issue stay within that issue's scope; where two issues touch the same files, the conflict is declared in the cross-issue section with an explicit fix order or an isolation argument."
  - "Each issue's plan states what is deliberately out of scope or deferred."
default_validators:
  - uses: validators/completeness-check
    with:
      extra_check: "every issue id in issue_manifest.json appears as a section heading in fix_plan.md; every acceptance criterion of every issue appears in that issue's traceability table."
  - uses: validators/adversarial-reviewer
    with:
      focus: "acceptance criteria with no proving step, cross-issue file conflicts not declared, verification commands that cannot actually discriminate pass from fail"
knowledge_slots: [org-context]
skill_refs:
  - skillpacks/addyosmani/planning-and-task-breakdown
permissions:
  writes: [own_artifact_dir]
---

# Fix Plan

## Purpose

Turn each issue brief into steps a builder can execute mechanically inside
that issue's worktree. Judgment about how to fix lives here, where it is
gated, so the implementing stage can follow the plan without improvising.

## Procedure

1. Read the briefs and the manifest fully; read the relevant code in the
   target repo for every issue.
2. Per issue, break the fix into small ordered steps. Each step names its
   files, states the change, gives a `Verify:` command runnable inside that
   issue's worktree, and notes how to roll the step back.
3. Build the per-issue traceability table: every acceptance criterion from
   the brief mapped to the step(s) and verification(s) that will prove it.
4. Compare issues for shared files or interacting behavior. Declare every
   conflict with an explicit fix order, or argue why the issues are isolated.
5. State per issue what is deliberately out of scope or deferred.
6. A brief too vague to plan (or marked needs-clarification) gets a section
   that records the gap and plans nothing — never guess a fix into existence.

## Output format constraints

`fix_plan.md` sections in order: `# Fix Plan`, `## Issues` (one `### ISS-<n>`
subsection per issue: numbered steps each with `Files:`, `Change:`,
`Verify:`, `Rollback:` lines, then a `Traceability:` table mapping criterion
to steps), `## Cross-issue ordering and conflicts` ("none" if none),
`## Deferred / out of scope`, `## Knowledge gaps`.

## Knowledge consumption

- `org-context`: coding standards, test conventions, or internal library docs
  if attached; otherwise follow the target repo's own conventions and note
  assumptions under `## Knowledge gaps`.

## Boundaries

- Do NOT write code, create branches or worktrees, or modify the target repo.
- Do NOT introduce new architecture or expand an issue's scope beyond its
  brief — scope changes belong upstream (F4).
- Do NOT plan around a too-vague brief by guessing; record the gap and stop
  planning that issue.

## Self-check before submitting

Walk each issue's traceability table backwards: every criterion reachable
from at least one step, every step's verification actually able to fail if
the fix is wrong. Confirm the issue-id set matches the manifest exactly.

## Summary requirement

Write `summary.md` (≤200 words): issues planned, the declared fix order and
why, any cross-issue conflicts, and issues left unplanned with the reason.
