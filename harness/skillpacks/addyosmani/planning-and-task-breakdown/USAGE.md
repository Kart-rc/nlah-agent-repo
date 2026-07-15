# Using `planning-and-task-breakdown`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Decomposes a spec into small, dependency-ordered, vertically-sliced tasks,
each with explicit acceptance criteria and a verification step, plus
checkpoints between phases — the plan an implement stage executes against.

## When to invoke

See SKILL.md → When to Use / When NOT to use for the full criteria. Harness
routing cues:

- Any sdlc run that reaches the plan stage with a validated spec — this is
  the default attachment there, so the router rarely needs to add it.
- Requests where the work "feels too large to start", needs scope
  communicated to a human, or could be parallelized across producers.
- Runs where implementation order is non-obvious (schema, API, and UI all
  in play) and a dependency graph must be made explicit.
- Skip for single-file changes with obvious scope, or when the incoming
  spec already contains well-defined tasks (per SKILL.md).

**Default attachments:** suggested by `stages/plan` `skill_refs`; attached
to the `plan` stage of the `sdlc` workflow.

## How to invoke

### In a harness workflow

Attach to a stage in the workflow manifest (a one-line edit; use the
`workflow-composer` skill to add, swap, or remove it, then run
`python3 scripts/harness_lint.py`):

```yaml
stages:
  - id: plan
    uses: stages/plan
    skills:
      - uses: skillpacks/addyosmani/planning-and-task-breakdown
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/addyosmani/planning-and-task-breakdown/SKILL.md
fully, then break the spec at <path> into ordered, verifiable tasks using
its plan and task templates.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- The producer (a read-only `planner` persona) writes no code: it reads the
  spec and codebase, maps the dependency graph, and slices vertically so
  each task delivers working end-to-end functionality.
- Every task follows SKILL.md's structure — description, acceptance
  criteria, verification commands, dependencies, files likely touched, size
  estimate — with anything L-or-larger broken down further.
- Checkpoints appear after every 2–3 tasks, high-risk tasks come early, and
  parallelization opportunities are called out explicitly.
- SKILL.md names `tasks/plan.md` and `tasks/todo.md` as its output
  convention; in a harness run the planner writes these documents into the
  stage's artifact directory under `runs/<run-id>/` instead.
- Done means SKILL.md → Verification passes: every task has acceptance
  criteria and a verification step, dependencies are ordered, no task
  touches more than ~5 files, and a human has approved the plan.
- Misapplication signs (SKILL.md → Red Flags): tasks that just say
  "implement the feature", all tasks XL-sized, or no checkpoints.

## Worked example

Request: "Add multi-tenant workspaces to the app", with a validated spec
from the design stage. The shipped sdlc manifest already attaches this
skill:

```yaml
  - id: plan
    uses: stages/plan
    skills:
      - uses: skillpacks/addyosmani/planning-and-task-breakdown
```

The planner maps schema → models → endpoints → UI dependencies, then emits
a phased plan: Task 1 "workspace table + migration" (S), Task 2 "user can
create a workspace end-to-end" (M), a checkpoint, and so on — each with
test commands as verification — ready for the implement stage to consume
one slice at a time.
