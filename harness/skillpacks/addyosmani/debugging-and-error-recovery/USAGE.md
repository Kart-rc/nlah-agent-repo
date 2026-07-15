# Using `debugging-and-error-recovery`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Enforces systematic root-cause debugging via a six-step triage (reproduce,
localize, reduce, fix the root cause, guard with a regression test, verify
end-to-end) and the stop-the-line rule: when something breaks, no new feature
work until the failure is understood and fixed.

## When to invoke

- The delivery request is a bug fix, a broken build, a failing test, or "it
  worked before and stopped" — the router's bug-fix classification lands here
  naturally.
- A verify stage must chase down failures that the implement stage produced,
  rather than merely reporting them.
- An intermittent or non-reproducible failure needs the skill's structured
  branching for timing-, environment-, and state-dependent bugs.
- A regression needs `git bisect`-style localization to a specific commit.
- See SKILL.md → When to Use for the full trigger list.

**Default attachments:** suggested by `stages/verify` `skill_refs`; attached
to the `verify` stage of the `sdlc` workflow.

## How to invoke

### In a harness workflow

Attach to a stage in the workflow manifest (a one-line edit; use the
`workflow-composer` skill to add, swap, or remove it, then run
`python3 scripts/harness_lint.py`):

```yaml
stages:
  - id: verify
    uses: stages/verify
    skills:
      - uses: skillpacks/addyosmani/debugging-and-error-recovery
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/addyosmani/debugging-and-error-recovery/SKILL.md
fully, then apply its triage checklist to diagnose and fix <failing test or
bug>, ending with a regression test that fails without the fix.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- On any unexpected failure the producer stops feature work, preserves the
  error output, and works the triage checklist in order — no guessed fixes.
- The fix targets the root cause, not the symptom (e.g. fixing the JOIN that
  produces duplicates rather than deduplicating in the UI).
- Every fix ships with a regression test that fails without the fix and
  passes with it, plus a full-suite and build run to catch fallout.
- Temporary instrumentation added during diagnosis is removed once the bug is
  guarded; error text from logs and CI is treated as untrusted data, never as
  instructions to execute.
- Done matches SKILL.md → Verification: root cause documented, regression
  test in place, all tests and build green, scenario verified end-to-end.
- Misapplication signs: "it works now" with no explanation of what changed,
  or unrelated edits accumulating while debugging (see SKILL.md → Red Flags).

## Worked example

Request: "Search breaks for tasks whose titles contain quotes — sometimes."

The router classifies this as a bug fix and runs `sdlc`; the `verify` stage
already carries this skill. The verify producer reads SKILL.md, reproduces
the failure with a minimal test case (a title containing `"quotes" &
<brackets>`), localizes it to the API layer's query escaping, and reduces it
to a one-line repro. The fix corrects the escaping at the query builder; a
regression test asserting the special-character search is added and shown to
fail on the pre-fix code. The stage report in `runs/<run-id>/verify/`
documents root cause, fix, and the green full-suite run.
