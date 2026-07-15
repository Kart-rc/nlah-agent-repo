# Using `source-driven-development`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Grounds every framework-specific implementation decision in official
documentation via a detect → fetch → implement → cite loop: read the
dependency file for exact versions, fetch the relevant docs page, follow the
documented pattern, and cite the source — never implement from memory.

## When to invoke

See SKILL.md → When to Use / When NOT to use for the full criteria. Harness
routing cues:

- Implement stages building framework-heavy code where the recommended
  approach matters: forms, routing, data fetching, state management, auth.
- Requests asking for "current best practices", "documented", "verified",
  or "correct" implementations — or boilerplate that will be copied across
  the project.
- Runs against fast-moving frameworks (React, Next.js, Django) where
  training-data patterns are likely stale or deprecated.
- Skip for version-independent work (renames, typo fixes, pure logic) or
  when the user explicitly wants speed over verification (per SKILL.md).

**Default attachments:** none — ad hoc: attach it explicitly on the
`implement` stage of the `sdlc` workflow when the change is
framework-specific and correctness matters; it complements the stage's
default `incremental-implementation` and `test-driven-development`.

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
      - uses: skillpacks/addyosmani/source-driven-development
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/addyosmani/source-driven-development/SKILL.md fully,
then implement <feature> with every framework-specific pattern verified
against and cited to official documentation.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- The producer opens with a "STACK DETECTED" statement naming exact
  versions from the dependency file, asking rather than guessing when
  versions are ambiguous. It needs fetch access to documentation sites;
  without network access it degrades to flagging patterns as unverified.
- It fetches the specific docs page per feature (never the homepage),
  citing only official docs, official blogs/changelogs, web standards
  references, or compatibility tables — never Stack Overflow or tutorials.
- Delivered code carries full-URL citations for framework-specific
  decisions; anything uncheckable is marked "UNVERIFIED", not hedged.
- Conflicts — docs vs. existing code, or docs vs. docs — are surfaced as
  explicit options for a human to pick, not silently resolved.
- Done means SKILL.md → Verification passes: versions identified, sources
  official, no deprecated APIs, conflicts surfaced. Misapplication signs
  (SKILL.md → Red Flags): "I believe this API..." instead of a citation, or
  code shipped without reading `package.json`.

## Worked example

Request: "Add a signup form to our React app using whatever the current
recommended pattern is." Use `workflow-composer` to add this skill to the
run's implement stage:

```yaml
  - id: implement
    uses: stages/implement
    skills:
      - uses: skillpacks/addyosmani/incremental-implementation
      - uses: skillpacks/addyosmani/source-driven-development
```

The builder detects React 19.1 from `package.json`, fetches
`react.dev/reference/react/useActionState`, notices the codebase still uses
manual `useState` pending-flags, surfaces that conflict as an A/B choice,
and delivers the form with the source URL cited above the hook call.
