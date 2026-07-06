---
id: implement
summary: "Execute the implementation plan step by step in the target repo, with tests accompanying every behavior change."
producer: builder
inputs:
  - name: plan
    description: "Approved implementation plan (from plan)."
    format: markdown
    required: true
  - name: design
    description: "Approved design document (from design)."
    format: markdown
    required: true
  - name: target_repo
    description: "Path to the codebase to change."
    format: path
    required: true
outputs:
  - name: change_summary
    file: change_summary.md
    format: markdown
    description: "Per-step record: what changed, files, verification command + actual output, deviations from plan."
  - name: diff_manifest
    file: diff_manifest.json
    format: json
    description: "Machine-readable change list: [{path, action: added|modified|deleted, step}]."
acceptance_criteria:
  - "Every plan step is either executed (with its verification output recorded verbatim) or explicitly skipped with a reason."
  - "Every behavior change is accompanied by a new or updated test, or the change_summary explains why testing was infeasible."
  - "All verifications recorded in change_summary.md actually passed - no step reports failing output as done."
  - "The diff touches only files the plan named, or deviations are declared in a Deviations section with reasons."
  - "No secrets, credentials, or sensitive data appear in code, config, or logged output."
default_validators:
  - uses: validators/completeness-check
  - uses: validators/red-team
knowledge_slots: [org-context]
skill_refs:
  - skillpacks/addyosmani/incremental-implementation
  - skillpacks/addyosmani/test-driven-development
permissions:
  writes: [own_artifact_dir, target_repo]
---

# Implement

## Purpose

The only stage that changes the target system. It follows the validated plan
mechanically — small steps, each verified as it lands — so that judgment stays
where it was validated (design/plan) and evidence accumulates as work proceeds.

## Procedure

1. Read the plan and design fully. Read every attached practice skill before
   writing any code.
2. Execute steps in order. Per step: make the change, run the step's `Verify:`
   command, record the actual output in `change_summary.md`. A failing
   verification stops the step — fix it before moving on; if unfixable within
   the plan, record the blocker and stop the stage.
3. Write or update tests with each behavior change (test-driven where the
   attached skill directs).
4. Match the codebase's existing style, naming, and comment density.
5. If reality forces a deviation from the plan (a file moved, an API differs),
   keep it minimal, record it under Deviations with the reason, and do NOT
   redesign — a deviation that changes architecture means stop + summary.
6. Maintain `diff_manifest.json` as you go.

## Output format constraints

`change_summary.md` sections in order: `# Change Summary`, `## Steps` (one
subsection per plan step: `Status:` done/skipped, `Files:`, `Verification:`
fenced block with the command and its verbatim output), `## Deviations`
("none" if none), `## Test coverage` (which behaviors got which tests),
`## Knowledge gaps`. `diff_manifest.json`: JSON array of
`{"path", "action", "step"}`.

## Knowledge consumption

- `org-context`: coding standards or internal library docs if attached;
  otherwise follow the target repo's own conventions and note assumptions
  under `## Knowledge gaps`.

## Boundaries

- Do NOT change requirements, design, or plan — implement them. Architectural
  improvisation is scope drift (F4).
- Do NOT perform unrelated cleanup, drive-by refactors, or dependency
  additions the plan doesn't call for.
- Do NOT write outside the target repo and your artifact directory.
- Do NOT commit or push — delivery is the deliver stage's job.

## Self-check before submitting

Re-run the full verification set (all step `Verify:` commands, plus the target
repo's test suite if one exists) and confirm the recorded outputs are current.
Scan the diff for secrets and for files not named in the plan.

## Summary requirement

Write `summary.md` (≤200 words): steps completed/skipped, test status,
deviations if any, and the single riskiest part of the diff for reviewers to
focus on.
