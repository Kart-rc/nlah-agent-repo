# Using `interview-me`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Extracts what the user actually wants (not what they think they should want)
through a one-question-at-a-time interview — each question carrying the
agent's own guess — until the agent reaches ~95% confidence and the user
explicitly confirms a written restate of intent.

## When to invoke

See SKILL.md → When to Use / When NOT to use for the full criteria. Harness
routing cues:

- Any intake stage where the request arrives underspecified: missing the
  who, the why-now, the success criterion, or the binding constraint.
- Explicit user invocations: "interview me", "grill me", "are we sure?",
  "stress-test my thinking".
- Every shipped workflow starts with it at intake, so the router rarely
  needs to add it — but detach it (or expect degraded behavior) for
  non-interactive runs: SKILL.md → Loading Constraints forbids using it
  where no live user can answer, and the producer must flag the gap as a
  blocker instead of guessing.
- Skip for unambiguous self-contained asks, pure information requests, and
  mechanical operations (per SKILL.md).

**Default attachments:** suggested by `stages/intake` `skill_refs`; attached
to the `intake` stage of all four shipped workflows — `sdlc` (alongside
`spec-driven-development`), `tech-decision`, `architecture-review`, and
`proposal`.

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
      - uses: skillpacks/addyosmani/interview-me
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/addyosmani/interview-me/SKILL.md fully, then
interview me about <request> until you can produce a confirmed statement
of intent per its Output section.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- The producer opens with a one-sentence hypothesis plus an honest
  confidence number, then asks exactly one question per turn, each with its
  own guess attached (SKILL.md → The Process).
- Sophistication-signaling answers ("scalable", "clean") get probed with
  "what would you actually want if you didn't have to justify it?".
- The deliverable is a confirmed statement of intent: a 6-line restate
  (Outcome / User / Why now / Success / Constraint / Out of scope) plus an
  explicit "yes" — in a harness run it lands in the intake artifact under
  `runs/<run-id>/`.
- Downstream stages consume the confirmed intent, not the original ask;
  handoffs to `idea-refine` or `spec-driven-development` are framed on it.
- Misapplication signs (from SKILL.md → Red Flags): three or more questions
  batched in one message, a question with no guess attached, or accepting
  "whatever you think is best" as a terminal answer.

## Worked example

Request: "build me a dashboard for our metrics". The router starts an sdlc
run; the shipped manifest attaches this skill at intake:

```yaml
  - id: intake
    uses: stages/intake
    skills:
      - uses: skillpacks/addyosmani/interview-me
      - uses: skillpacks/addyosmani/spec-driven-development
```

The intake producer hypothesizes ("standup status check, ~30% confidence"),
asks one question at a time, and discovers — as in SKILL.md's own example —
that the real need is a personal experiment list, not a dashboard. The
confirmed restate (with an Out-of-scope line) becomes the intake artifact
that the design stage specs against.
