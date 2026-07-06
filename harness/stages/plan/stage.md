---
id: plan
summary: "Break the approved design into small, ordered, independently verifiable implementation steps."
producer: planner
inputs:
  - name: requirements
    description: "Approved requirements (from intake)."
    format: markdown
    required: true
  - name: design
    description: "Approved design document (from design)."
    format: markdown
    required: true
outputs:
  - name: implementation_plan
    file: plan.md
    format: markdown
    description: "Ordered steps, each with scope, files touched, verification command/check, and rollback note."
acceptance_criteria:
  - "Every requirement traces to at least one plan step (traceability section)."
  - "Every step names the files/modules it touches and a concrete verification (a command to run or an observable check)."
  - "Steps are small vertical slices: each leaves the system working and is independently verifiable."
  - "Steps only use design elements from the approved design - no new architecture appears in the plan."
  - "The plan states what is deliberately deferred or out of scope."
default_validators:
  - uses: validators/completeness-check
    with:
      extra_check: "every requirement id in requirements.md appears in the plan's traceability section"
  - uses: validators/adversarial-reviewer
knowledge_slots: [org-context]
skill_refs:
  - skillpacks/addyosmani/planning-and-task-breakdown
permissions:
  writes: [own_artifact_dir]
---

# Plan

## Purpose

Convert the design into an execution recipe the implement stage can follow
without making architectural decisions. Small verified steps are the harness's
main defense against large uncontrolled diffs.

## Procedure

1. Read requirements and design fully; extract requirement ids and design
   elements.
2. Slice the work into ordered steps. Each step: goal, files touched, the
   change in one or two sentences, its verification (command or observable
   check), and a rollback note (how to undo just this step).
3. Order steps so the system stays working after each one; call out any step
   where that is impossible and why.
4. Build the traceability section: requirement id → step number(s).
5. List deferred work and out-of-scope items explicitly.

## Output format constraints

`plan.md` sections in order: `# Implementation Plan`, `## Steps` (numbered;
each step has `Files:`, `Change:`, `Verify:`, `Rollback:` lines),
`## Traceability` (requirement id → steps), `## Deferred / out of scope`,
`## Knowledge gaps`.

## Knowledge consumption

- `org-context`: verify assumed tooling/CI conventions if an adapter is
  attached; otherwise record assumptions under `## Knowledge gaps`.

## Boundaries

- Do NOT introduce design decisions absent from the design doc; if a gap in
  the design blocks planning, record it in the summary and stop.
- Do NOT write code. `Verify:` lines name commands; they don't implement them.

## Self-check before submitting

For each step ask: "could this step alone be reviewed and verified?" If a step
touches more than ~5 files or lacks a runnable verification, split or tighten
it. Confirm traceability covers every requirement id.

## Summary requirement

Write `summary.md` (≤200 words): number of steps, the riskiest step and why,
and anything deferred that the requester might expect to be included.
