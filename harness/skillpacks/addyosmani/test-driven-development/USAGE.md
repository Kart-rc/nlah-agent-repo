# Using `test-driven-development`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Drives implementation with the red-green-refactor cycle — a failing test
before the code that passes it — and the Prove-It Pattern for bugs
(reproduce with a failing test before fixing), backed by test-pyramid
sizing and state-over-interaction testing guidance.

## When to invoke

See SKILL.md → When to Use / When NOT to use for the full criteria. Harness
routing cues:

- Any sdlc run implementing logic or changing behavior — it is a default on
  the implement stage, so the router rarely needs to add it.
- Bug-fix runs especially: the Prove-It Pattern makes the reproduction test
  the first deliverable, giving validators a concrete regression guard.
- Requests phrased as "prove it works", "add tests for", or any change to
  existing functionality that could silently break behavior.
- Skip pure configuration, documentation, or static-content changes with no
  behavioral impact (per SKILL.md).

**Default attachments:** suggested by `stages/implement` `skill_refs`;
attached to the `implement` stage of the `sdlc` workflow (alongside
`incremental-implementation`).

## How to invoke

### In a harness workflow

Attach to a stage in the workflow manifest (a one-line edit; use the
`workflow-composer` skill to add, swap, or remove it, then run
`python3 scripts/harness_lint.py`):

```yaml
stages:
  - id: implement
    uses: stages/implement
    skills:
      - uses: skillpacks/addyosmani/test-driven-development
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/addyosmani/test-driven-development/SKILL.md fully,
then fix <bug> using its Prove-It Pattern: write the failing reproduction
test first, then the fix, then run the full suite.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- The producer writes each test first and shows it failing before writing
  the minimal code to pass it; bug fixes always begin with a reproduction
  test that fails against current code.
- Test distribution follows the pyramid (~80% small unit tests); tests
  assert outcomes rather than internal call sequences, prefer real
  implementations over mocks, and read as a specification (DAMP naming,
  arrange-act-assert, one assertion per concept).
- Done means SKILL.md → Verification passes: every new behavior has a test,
  the suite is green, bug fixes carry their reproduction test, nothing
  skipped or disabled.
- Misapplication signs (SKILL.md → Red Flags): tests that pass on first
  run, "all tests pass" with no tests actually run, or re-running the same
  test command with no intervening code change.

## Worked example

Bug report: "Completing a task doesn't set its completedAt timestamp." An
sdlc bug fix; the shipped manifest already attaches this skill:

```yaml
  - id: implement
    uses: stages/implement
    skills:
      - uses: skillpacks/addyosmani/incremental-implementation
      - uses: skillpacks/addyosmani/test-driven-development
```

The builder writes `it('sets completedAt when task is completed')`, runs it
and records the failure, adds the missing field to the update call, shows
the test passing, then runs the full suite — the stage output under
`runs/<run-id>/` includes both the red and green runs as evidence.
