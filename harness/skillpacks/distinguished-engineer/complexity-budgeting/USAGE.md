# Using `complexity-budgeting`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Makes a producer account for complexity as spend: new mechanisms counted
in concepts and interactions with their recurring rent named, accidental
complexity separated from essential via archaeology, every new mechanism
born with sunset criteria and a removal owner, deletion scheduled as
first-class roadmap work, and competing designs compared on net concept
count — with "what does this retire?" asked of every addition.

## When to invoke

- A system has accreted concepts faster than capabilities and a review or
  refactor must decide what goes.
- An `assess`-stage review is complexity-dominated: the question is less
  "is this sound?" than "can the team afford to think about it?"
- A `design` stage where the candidate solutions differ mainly in how
  many mechanisms they add or retire.
- See SKILL.md → When to Use / When NOT to use; code-level
  behavior-preserving cleanup is `addyosmani/code-simplification`.

**Default attachments:** none (ad hoc). Natural homes: `assess` for
complexity-dominated reviews; `design` for refactor and consolidation
work.

## How to invoke

### In a harness workflow

Attach to a stage in the workflow manifest (a one-line edit; use the
`workflow-composer` skill to add, swap, or remove it, then run
`python3 scripts/harness_lint.py`):

```yaml
stages:
  - id: assess
    uses: stages/assess
    skills:
      - uses: skillpacks/distinguished-engineer/complexity-budgeting
```

The orchestrator passes the skill path to the stage's producer subagent,
which reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read
harness/skillpacks/distinguished-engineer/complexity-budgeting/SKILL.md
fully, then audit <system/design> as complexity spend: count the concepts,
separate accidental from essential, and identify what can be deleted or
must carry a sunset date.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and
what standalone mode does not guarantee.

## What to expect

- Complexity counted in concepts and their interactions (flags × modes ×
  tenant types), never in lines; each concept's recurring rent named and
  judged against the team as actually staffed.
- Suspicious mechanisms interrogated by archaeology — the ones explained
  by history rather than a present requirement flagged as deletion
  candidates.
- Every proposed mechanism carrying sunset criteria and a removal owner
  from birth; "temporary" without a date treated as permanent.
- Deletion and consolidation surfaced as named, schedulable work items,
  not "when there's slack."
- Design comparisons scored on net concept count, with additions asked
  what they retire.
- Misapplication signs (from Red Flags): a plugin system with one plugin
  going unquestioned, or simplification measured in lines moved.

## Worked example

Request: "Review the notification service — every change there takes
weeks."

Attach this skill at `assess`. Expected output shape: an assessment in
`runs/<run-id>/` counting the service's concepts (3 delivery queues, 11
feature flags, 4 tenant modes, 2 template engines — a nominal state space
of thousands, ~20 states actually exercised); archaeology findings (the
second template engine served an A/B test that ended in 2022; the
per-tenant "priority lane" protects against a throughput ceiling raised
two hardware generations ago); a deletion slate (retire engine B — 3
remaining templates, owner named; collapse 7 always-on flags); the one
essential complexity defended (per-region queues mirror a data-residency
requirement); and a verdict that conditions approval of the next feature
on the deletion slate landing first — net concept count must go down.
