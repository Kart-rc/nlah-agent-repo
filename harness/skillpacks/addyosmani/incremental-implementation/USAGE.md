# Using `incremental-implementation`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Enforces building in thin vertical slices — implement, test, verify, commit,
then expand — so the codebase stays working and compilable between steps,
with simplicity and scope discipline as standing rules.

## When to invoke

See SKILL.md → When to Use / When NOT to use for the full criteria. Harness
routing cues:

- Any feature or bug-fix run whose implement stage will touch more than one
  file — for the sdlc workflow this is the default, so it is already there.
- Requests phrased as "build", "implement", "add feature", or "refactor"
  where the producer would otherwise land everything in one large diff.
- Runs with a task breakdown from `planning-and-task-breakdown`: this skill
  is the execution discipline that consumes those tasks slice by slice.
- Skip it only for single-file, single-function changes where scope is
  already minimal (per SKILL.md).

**Default attachments:** suggested by `stages/implement` `skill_refs`;
attached to the `implement` stage of the `sdlc` workflow (alongside
`test-driven-development`).

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
      - uses: skillpacks/addyosmani/incremental-implementation
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/addyosmani/incremental-implementation/SKILL.md
fully, then implement <task> in thin vertical slices, verifying and
committing each slice before starting the next.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- The producer (a `builder` persona modifying the target repo per its stage
  contract) works the increment cycle — implement → test → verify → commit —
  one slice at a time, choosing a slicing strategy (vertical, contract-first,
  or risk-first) per SKILL.md.
- Commit history becomes a sequence of small, individually revertable
  commits, each leaving build and tests green — not one large drop.
- Out-of-scope issues get recorded as "noticed but not touching" notes
  instead of being fixed opportunistically.
- Done means SKILL.md → Verification passes: every increment tested and
  committed, full suite green, clean build, no uncommitted changes.
- Misapplication signs (SKILL.md → Red Flags): 100+ lines written without
  running tests, unrelated changes mixed into one increment, or a broken
  build between slices.

## Worked example

Request: "Add CSV export to the reports page (API endpoint + download
button + tests)." The router classifies this as an sdlc feature; the
shipped manifest already attaches this skill to `implement`:

```yaml
  - id: implement
    uses: stages/implement
    skills:
      - uses: skillpacks/addyosmani/incremental-implementation
      - uses: skillpacks/addyosmani/test-driven-development
```

The builder lands slice 1 (serializer + unit tests), slice 2 (endpoint +
API test), slice 3 (UI button wired end-to-end), committing after each with
tests green, and reports the slice-by-slice trail in its stage output under
`runs/<run-id>/`.
