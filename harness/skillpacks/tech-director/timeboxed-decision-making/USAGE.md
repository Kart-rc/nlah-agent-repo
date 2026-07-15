# Using `timeboxed-decision-making`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Makes a producer decide on time at stated confidence instead of producing an
un-decision: one-way/two-way door classification drives the amount of process,
the 70% rule calibrates deciding on partial information, and disagree-and-commit
with observable revisit triggers stops decisions being quietly re-made.

## When to invoke

- The request is decision-shaped with a date attached, or analysis is dragging
  past its value — the router runs the `tech-decision` workflow, whose
  `decide` stage carries this skill by default.
- A decision others disagreed with must be recorded so it sticks, or a
  previously "made" decision keeps getting reopened.
- The upstream option matrix is done and someone must now actually choose.
- See SKILL.md → When to Use / When NOT to use; skip it for one-way doors
  where cheap information is still available before the deadline, or
  decisions that belong to a different owner.

**Default attachments:** suggested by `stages/decide` `skill_refs` (alongside
`executive-communication` and `addyosmani/documentation-and-adrs`), and
attached to the `decide` stage of the shipped `tech-decision` workflow.

## How to invoke

### In a harness workflow

Attach to a stage in the workflow manifest (a one-line edit; use the
`workflow-composer` skill to add, swap, or remove it, then run
`python3 scripts/harness_lint.py`):

```yaml
stages:
  - id: decide
    uses: stages/decide
    skills:
      - uses: skillpacks/tech-director/timeboxed-decision-making
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/tech-director/timeboxed-decision-making/SKILL.md
fully, then make and record the call on <decision> from the option matrix at
<path>, classifying the door type and stating confidence.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- The decision record opens with a door classification (one-way / two-way)
  with reasoning, and the process weight visibly matches it.
- A decide-by date and an explicit default ("if no decision by X, Y happens")
  appear on every open decision; deferrals carry a date and a reason or are
  called out as abdication.
- Confidence is stated honestly against the information available ("deciding
  at moderate confidence because the deadline binds and the door is two-way").
- Contested decisions carry a steelmanned dissent section answered with
  substance, plus concrete revisit triggers ("reopen if p99 >200ms in
  production"), an owner, and an inform-list.
- Done looks like SKILL.md → Verification (six items, all from the record).
- Misapplication signs (from Red Flags): revisit conditions no one could
  observe or measure, or a record with no dissent section on a decision that
  was clearly contested.

## Worked example

Request: "Pick our message broker by Friday — the team has argued Kafka vs
NATS for three sprints and the platform launch is blocked on it."

The router runs `tech-decision`; the shipped manifest attaches this skill at
`decide`, consuming the `options` stage's matrix. Expected output shape: a
record in `runs/<run-id>/` classifying the choice as a two-way door while the
abstraction layer holds, deciding for NATS at stated moderate confidence,
steelmanning the Kafka camp's ecosystem argument, setting revisit triggers
("reopen if we need replayable multi-consumer streams, or throughput exceeds
50k msg/s sustained"), and naming the decide-by default that the launch slips
one sprint if Friday passes undecided.
