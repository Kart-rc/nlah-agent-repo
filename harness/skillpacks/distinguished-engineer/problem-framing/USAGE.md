# Using `problem-framing`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Makes a producer excavate the problem from a request before any solutioning:
the problem named separately from any proposed solution, the actors and real
constraints made visible, the current condition stated measurably with the
cost of doing nothing priced, decidable done-criteria plus disconfirming
evidence, and a first slice carved small enough for one team to own.

## When to invoke

- The request spans teams with no owner, or stakeholders disagree about
  what the problem even is.
- The request arrives pre-shaped as a solution ("we need a service mesh")
  and the underlying pain has never been written down.
- Work in an area keeps stalling or rebooting because its goal is
  contested.
- See SKILL.md → When to Use / When NOT to use; routine requirements
  gathering for a well-owned feature is the `intake` stage's job with
  `addyosmani/interview-me`.

**Default attachments:** none (ad hoc). Natural home: an `intake` stage
when the request is unowned, cross-cutting, or solution-shaped.

## How to invoke

### In a harness workflow

Attach to a stage in the workflow manifest (a one-line edit; use the
`workflow-composer` skill to add, swap, or remove it, then run
`python3 scripts/harness_lint.py`):

```yaml
stages:
  - id: intake
    uses: stages/intake
    skills:
      - uses: skillpacks/distinguished-engineer/problem-framing
```

The orchestrator passes the skill path to the stage's producer subagent,
which reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/distinguished-engineer/problem-framing/SKILL.md
fully, then produce a problem statement for <request>, separating the
problem from the proposed solution and making it falsifiable before any
option is discussed.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and
what standalone mode does not guarantee.

## What to expect

- The problem stated separately from any proposed solution — the original
  request's solution appears demoted to "one candidate."
- Actors named (who hurts, who causes, who can change, who resists) and
  real constraints separated from incumbent habits.
- A measurable current condition and a priced cost of doing nothing;
  "why now" answered with what changed.
- Decidable done-criteria plus the disconfirming test that would show the
  problem is smaller or different than claimed.
- A first slice ownable by one team, valuable alone, with a candidate
  owner named.
- Misapplication signs (from Red Flags): a product name inside the problem
  statement, or done-criteria reasonable people could argue either way.

## Worked example

Request: "We need a service mesh."

Attach this skill at `intake`. Expected output shape: a frame in
`runs/<run-id>/` recording the actual pain (three teams each maintain
bespoke retry/mTLS/discovery code; two outages last quarter traced to
divergent retry policies), actors (platform team can change it; the payments
team will resist another sidecar), the measurable condition (~15% of oncall
pages involve inter-service communication), the cost of nothing (each new
service re-implements the stack, ~3 weeks each), done-criteria (common
policy enforced on the top-10 call paths; zero bespoke mTLS
implementations), a disconfirming test (if pages don't cluster on bespoke
stacks, the mesh premise weakens) — and a first slice: standardized client
libraries for the two highest-traffic paths, owned by platform, which
proves or falsifies the frame without buying a mesh.
