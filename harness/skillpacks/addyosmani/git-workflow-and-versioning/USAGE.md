# Using `git-workflow-and-versioning`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Disciplines version control as the safety net for agent-speed development:
trunk-based flow, small atomic commits with why-focused messages, the
save-point pattern (commit each verified slice), and a versioning contract
for consumers — semantic versions, immutable tags, curated changelogs.

## When to invoke

- SKILL.md → When to Use says "always"; any builder-persona stage committing
  to the target repo is a candidate — attach it where hygiene matters most.
- The implement stage of a feature or fix run, so work lands as reviewable
  atomic commits with change summaries rather than one giant diff.
- Release work: cutting a version, choosing the semver bump, tagging, or
  writing the changelog — natural for a `deliver` stage.
- Parallel agent work that should be isolated in worktrees, or a repo whose
  git hygiene (missing `.gitignore`, mixed-concern commits) is the problem.

**Default attachments:** none — ad hoc: attach it to the `implement` stage
(and `deliver`, for release/versioning work) of `sdlc` runs; it complements
`shipping-and-launch`, which handles the release itself.

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
      - uses: skillpacks/addyosmani/git-workflow-and-versioning
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/addyosmani/git-workflow-and-versioning/SKILL.md
fully, then apply its discipline while implementing <task>: atomic commits
per verified slice, typed messages explaining the why, and a change summary
at the end.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- Work lands as small atomic commits (~100 lines target), each doing one
  logical thing, committed after tests pass — the save-point pattern — with
  `type: description` messages explaining intent.
- Refactoring, formatting, and feature changes are kept in separate commits
  (and ideally separate PRs); branches are short-lived and named by
  convention (`feature/…`, `fix/…`).
- After modifications the producer emits the structured change summary from
  SKILL.md: CHANGES MADE, THINGS I DIDN'T TOUCH, POTENTIAL CONCERNS.
- Pre-commit hygiene runs every time: staged-diff review, secret grep, tests,
  lint, type check; `.gitignore` gaps get fixed rather than worked around.
- Release outputs include the correct semver bump, an annotated tag as the
  source of truth, and a changelog entry grouped by impact — written with the
  change, not reconstructed later.
- Misapplication signs: "fix"/"update" commit messages, large uncommitted
  changes accumulating, or a breaking change shipped under a patch bump
  (see SKILL.md → Red Flags and per-commit/per-release checklists).

## Worked example

Request: "Add CSV task import and cut the 1.4.0 release of the client
library."

The router runs `sdlc`; attach this skill to `implement` and `deliver`. The
builder works on `feature/csv-import`, landing four commits — parser,
endpoint wiring, UI, tests — each after a green test run, then posts the
CHANGES MADE / DIDN'T TOUCH / CONCERNS summary. The deliver stage judges the
change additive (minor bump), tags `v1.4.0` with the version derived from
the tag, and adds the changelog entry under `### Added` by user impact.
