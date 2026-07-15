# Using `code-explainers`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Makes the producer deliver a nontrivial change as a literate explainer —
background first, intuition before details, then a prose-led code walk in
teaching order — instead of a raw diff, so human understanding of the change
is itself a deliverable.

## When to invoke

- The routing cues live in SKILL.md → When to Use (and When NOT to use for
  the trivial-change exclusion).
- The router has classified a feature or bug-fix delivery through the
  `sdlc` workflow and the requester or reviewer does not know the subsystem
  being changed.
- The request itself asks for understanding: "walk me through what you
  did", "explain the change to the team", "I must review code I didn't
  write".
- You are attaching `understanding-quizzes` anyway — an explainer is the
  document the quiz closes out (the pack chains explainer → quiz →
  micro-world).

**Default attachments:** none — ad hoc. No stage `skill_refs` or shipped
workflow manifest attaches it; the pack README names the `implement` or
`verify` stage of the `sdlc` workflow as its natural home, so the delivered
change arrives with its explainer.

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
      - uses: skillpacks/geoffreylitt/code-explainers
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/geoffreylitt/code-explainers/SKILL.md fully, then
write an explainer for the change on this branch (diff against main),
following its output contract.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- Two extra artifacts per change: a canonical markdown explainer and a
  self-contained, build-free HTML rendering, under the stage's artifact
  directory in `runs/<run-id>/` (or where the operator directs standalone).
- The document opens with skippable background on the affected system,
  states the essence and rejected alternatives before any code, then walks
  the diff in narrative order with prose before each hunk.
- It ends with a quiz per `understanding-quizzes` and hands off to
  `micro-worlds` when static explanation cannot carry the intuition (the
  pack's chain), rather than growing into an app itself.
- "Done" is the SKILL.md Verification checklist: background, essence,
  narrative code walk, rationale, both formats, closing quiz.
- Misapplication signs (from Red Flags): the document opens with a file
  list or the raw diff; only one output format; decorative interactive
  figures a sentence could replace.

## Worked example

Request: "Add rate limiting to the public API" runs through `sdlc`; the
owner has never touched the middleware layer. Attach to `verify` (as above,
with `id: verify` / `uses: stages/verify`) so the explainer covers the
change as actually implemented. Expected in the verify stage's artifact
directory: `explainer.md` and `explainer.html`, opening with how requests
flow through the middleware chain today, then "token bucket per API key
over fixed windows because …", then code walked from the bucket data model
outward, ending with a quiz the owner must pass before requesting review.
