# Using `code-simplification`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Guides behavior-preserving refactoring: reduce complexity in recently changed
code so a new team member understands it faster, while keeping every input,
output, side effect, and error path identical. Its five principles (preserve
behavior, follow project conventions, clarity over cleverness, balance,
scope to what changed) guard against churn and over-simplification.

## When to invoke

- The router receives an explicit cleanup request: "this module works but is
  unreadable", "untangle this function", "reduce the nesting here".
- A feature just landed and its implementation is heavier than needed — run a
  simplification pass as a separate, follow-up change.
- Review of a run's diff flagged readability or complexity findings that
  deserve their own focused refactoring stage.
- Merges introduced duplication or inconsistency worth consolidating.
- See SKILL.md → When to Use / When NOT to use — notably, do not attach it
  when the code is not yet understood or is about to be rewritten anyway.

**Default attachments:** none — ad hoc: attach it to the `implement` stage
(builder persona) of an `sdlc` run whose deliverable is a refactor, kept
separate from feature-work runs per the skill's own discipline.

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
      - uses: skillpacks/addyosmani/code-simplification
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/addyosmani/code-simplification/SKILL.md fully, then
apply its process to simplify <file or function> without changing behavior,
one incremental change at a time with tests run after each.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- The producer starts with the Chesterton's Fence questions — responsibility,
  callers, edge cases, git blame — before touching anything.
- Changes target the concrete patterns in SKILL.md's tables (deep nesting,
  generic names, dead code, one-use abstractions), applied one at a time with
  the test suite run between each.
- Existing tests pass without modification; a simplification that needs test
  edits is treated as a behavior change and reverted.
- Refactoring stays scoped to the assigned code — no drive-by cleanups — and
  ships separately from any feature or fix.
- Done matches SKILL.md → Verification: tests, build, and lint green; clean
  reviewable diff; conventions followed; no error handling weakened.
- Misapplication signs: a "simplified" version that is longer and harder to
  follow, or many changes batched into one commit (see SKILL.md → Red Flags).

## Worked example

Request: "`parseImportRows()` in `src/lib/import.ts` is 180 lines of nested
conditionals — clean it up without changing what it does."

The router treats this as a refactor delivery and runs `sdlc` with this skill
on the `implement` stage (snippet above). The builder reads SKILL.md, answers
the fence questions (the odd date fallback exists for legacy CSV exports —
kept), then lands four incremental commits: guard clauses replacing the
nesting, two extracted helpers with descriptive names, a rename of `data` to
`importRows`, and deletion of an unreachable branch. Tests pass unmodified
after each commit, and the stage summary notes what was intentionally left
untouched.
