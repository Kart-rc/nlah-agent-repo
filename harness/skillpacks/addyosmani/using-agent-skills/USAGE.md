# Using `using-agent-skills`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

The pack's meta-skill: a decision tree that maps a task to the right
lifecycle skill(s), a set of always-on operating behaviors (surface
assumptions, manage confusion, push back, enforce simplicity, scope
discipline, verify), and the typical lifecycle sequence across the other
23 skills.

## When to invoke

SKILL.md has no "When to Use" section, so route on these cues:

- You are working standalone (no harness run) and want a lightweight router:
  `docs/using-skills-standalone.md` explicitly designates this skill as the
  standalone substitute for the harness's routing.
- At the start of a standalone session touching this pack, so skill
  selection and the core operating behaviors are loaded once up front.
- You are unsure which pack skill fits a task and want the decision tree
  and the phase/skill quick-reference table rather than reading 24 SKILL.md
  files.
- Do not use it inside a harness run: there, work-type routing is the
  `agentic-delivery-router`'s job and stage skills arrive via the manifest —
  a producer routing itself would conflict with the orchestration protocol
  (HARNESS.md).

**Default attachments:** none — ad hoc: this meta-skill is not attached to
any stage or suggested by any `skill_refs`; it is meant for standalone use.

## How to invoke

### In a harness workflow

Not typically attached. Stage producers receive their skills from the
manifest, so a router-skill has nothing to route; the harness's
`agentic-delivery-router` and `workflow-composer` own selection. If you
believe a stage genuinely needs it, attach it like any other skill
(`uses: skillpacks/addyosmani/using-agent-skills`) via `workflow-composer`
and run `python3 scripts/harness_lint.py` — but prefer attaching the
specific lifecycle skill its decision tree would have picked.

### Standalone (no harness run)

```text
Read harness/skillpacks/addyosmani/using-agent-skills/SKILL.md fully, then
use its discovery tree to pick the right skill(s) for <task>, read those
skills, and follow them — keeping its Core Operating Behaviors active
throughout.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- The session starts by classifying the task against the discovery tree
  (SKILL.md → Skill Discovery) and naming which skill(s) apply, possibly a
  sequence (e.g. spec → plan → implement → test).
- The six Core Operating Behaviors apply for the rest of the session:
  assumptions surfaced in an explicit block, confusion stopped and named
  rather than guessed through, pushback on flawed approaches, simplicity
  and scope discipline enforced, verification required before "done".
- Selected skills are treated as workflows, not suggestions — steps in
  order, verification steps never skipped (SKILL.md → Skill Rules).
- Referenced skills must still be read individually; this skill only routes
  and sets behavior, it does not inline the others' content.
- Signs it is being applied wrong (from SKILL.md → Failure Modes): plowing
  ahead when lost, sycophantic agreement with a flawed approach, building
  without a spec because "it's obvious", or skipping verification.

## Worked example

Standalone session, no harness run: "There's a race condition in our job
queue — fix it, and I want the fix properly tested and reviewed."

```text
Read harness/skillpacks/addyosmani/using-agent-skills/SKILL.md fully, then
route and execute this task: fix the race condition in src/queue/, with
tests and a review pass.
```

The agent walks the tree — "something broke" → `debugging-and-error-recovery`,
then `test-driven-development` (reproduction test first), then
`code-review-and-quality` — reads each of those SKILL.md files in turn, and
executes the sequence with assumptions surfaced up front, exactly the
lightweight-router usage `docs/using-skills-standalone.md` describes.
