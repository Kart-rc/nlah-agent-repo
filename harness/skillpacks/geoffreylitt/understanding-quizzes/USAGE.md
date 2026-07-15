# Using `understanding-quizzes`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Has the producer write a short (default five-question) comprehension quiz
about an agent-written change, targeting decisions and behavior rather than
trivia, and enforces the speed-regulator rule: code is not sent for human
review until the responsible human passes the quiz.

## When to invoke

- The routing cues live in SKILL.md → When to Use (and When NOT to use for
  the trivial-change and quiz-the-agent exclusions).
- Whenever `code-explainers` is attached — an explainer's output contract
  ends with a quiz per this skill, so the two normally travel together (the
  pack chains explainer → quiz → micro-world).
- A delivery routed through `sdlc` will end with a human requesting review
  from teammates, and you want an honest check that the requester actually
  understands the change first.
- Long-running agentic projects where the operator wants a periodic probe
  for accumulating cognitive debt, or a human has said "I read it" and the
  stakes make it worth verifying that reading produced understanding.

**Default attachments:** none — ad hoc. No stage `skill_refs` or shipped
workflow manifest attaches it; the pack README names the `implement` or
`verify` stage of the `sdlc` workflow as its natural home, so the delivered
change arrives with its quiz.

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
      - uses: skillpacks/geoffreylitt/understanding-quizzes
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/geoffreylitt/understanding-quizzes/SKILL.md fully,
then write a quiz for the change on this branch (diff against main) that I
must pass before sending it for review.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- A quiz artifact per change: five medium-difficulty questions including at
  least one prediction ("what happens if X?"), one rationale ("why Y over
  Z?"), and one boundary ("where would this break?"), with answers hidden
  from the question view.
- The speed-regulator rule stated alongside the quiz, and — in a harness
  run — the outcome recorded (passed / retaken / waived-with-reason) next
  to the stage artifacts, so a waiver is visible rather than silent.
- A human step in the loop: review handoff waits on a pass; a fail routes
  back to re-reading the explainer, questioning the agent, or exploring a
  `micro-worlds` artifact (the pack's chain), then retaking.
- "Done" is the SKILL.md Verification checklist, including the recorded
  outcome.
- Misapplication signs (from Red Flags): questions answerable by scrolling
  and pattern-matching (names, counts, headings); a failed quiz followed by
  a review request anyway with no recorded waiver.

## Worked example

Request: an agent has landed a large auth-flow refactor via `sdlc`, and the
owner is about to ask teammates for review. Attach to `verify` (as above,
with `id: verify` / `uses: stages/verify`), alongside `code-explainers`,
whose document it closes out. Expected output: the explainer ends with five
questions such as "a request arrives with an expired refresh token — what
does the new flow return?" (prediction) and "why rotate tokens on refresh
rather than on login?" (rationale), an answer key in a collapsed section,
the no-review-before-pass rule stated, and the outcome recorded in the
verify stage's artifacts.
