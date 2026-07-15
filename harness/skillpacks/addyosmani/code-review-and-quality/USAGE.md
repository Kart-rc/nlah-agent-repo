# Using `code-review-and-quality`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Structures a five-axis review — correctness, readability, architecture,
security, performance — applied to every change before merge, with
severity-labelled findings, named structural remedies, and an approval
standard of "definitely improves code health", not perfection.

## When to invoke

- A run's output is a code change that needs an evaluated verdict before it
  merges — especially when one agent wrote code another must judge.
- The request is itself a review: "review this PR", "assess this diff",
  "is this refactor an improvement?".
- A bug-fix delivery needs both the fix and its regression test reviewed.
- A change is large or structural and needs the skill's change-sizing and
  splitting guidance applied.
- See SKILL.md → When to Use; it also links `references/security-checklist.md`
  and `references/performance-checklist.md` for the deeper per-axis checks.

**Default attachments:** none — ad hoc: attach it to the `verify` stage of an
`sdlc` run when the verification should include a structured review of the
implement stage's diff, or use it standalone on any pending change.

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
      - uses: skillpacks/addyosmani/code-review-and-quality
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/addyosmani/code-review-and-quality/SKILL.md fully,
then apply its five-axis review to the diff in <path or PR>, labelling every
finding Critical / Required / Optional / Nit and ending with a verdict.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- The review follows the five-step process in SKILL.md: context first, tests
  before implementation, all five axes per file, categorized findings, then a
  check of the author's verification story.
- Every finding carries a severity prefix, and findings are ordered by
  leverage — correctness and security ahead of nits.
- Structural problems come with a named remedy (extract a dispatcher, delete
  a pass-through wrapper, split a file) rather than a bare complaint.
- Dead code is listed explicitly with a "safe to remove these?" question, not
  silently deleted or ignored.
- Done means the review checklist in SKILL.md is filled and a verdict is
  given (Approve or Request changes), with Critical/Required items resolved.
- Misapplication signs: "LGTM" with no evidence of review, or feedback that
  only checks whether tests pass (see SKILL.md → Red Flags).

## Worked example

Request: "The implement stage produced a 600-line diff adding task sharing —
review it before we merge."

Attach this skill to the `verify` stage (snippet above). The verify producer
reads SKILL.md and writes `runs/<run-id>/verify/review.md`: it flags a
Critical missing authorization check on the share endpoint, a Required
structural finding (sharing logic added to the shared `db.ts` module, with
the remedy of moving it into the tasks package), two Nits, and — because the
diff exceeds the ~300-line comfort zone — recommends splitting the schema
migration into its own change. Verdict: Request changes, with the checklist
attached.
