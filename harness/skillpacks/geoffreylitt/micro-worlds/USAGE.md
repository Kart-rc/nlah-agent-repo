# Using `micro-worlds`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Has the producer build a small, ephemeral, interactive artifact — a
state-over-time debugger, a step-through replay of a migration, a
drag-to-explore simulation — wired to the real code and data, whose only
purpose is to let a human inhabit how the system behaves. The artifact is
scaffolding: never shipped, tested, or maintained.

## When to invoke

- The routing cues live in SKILL.md → When to Use (and When NOT to use —
  build the cheapest thing that works; try `code-explainers` first).
- It is the last link in the pack's chain (explainer → quiz → micro-world):
  attach it when runtime behavior — evolving internal state, a many-step
  migration — will not be feelable from a static explainer, or a failed
  comprehension quiz shows reading alone is not producing understanding.
- A delivery routed through `sdlc` touches an interpreter, state machine,
  or algorithm whose behavior the human owner must steward afterward.
- Debugging or verification work where the operator wants peripheral vision
  of the machine, not only the narrow fix — or the human has said "I read
  it, but I have no feel for what it's doing".

**Default attachments:** none — ad hoc. No stage `skill_refs` or shipped
workflow manifest attaches it; the pack README names the `implement` or
`verify` stage of the `sdlc` workflow as its natural home when the change
involves complex runtime state or a many-step migration.

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
      - uses: skillpacks/geoffreylitt/micro-worlds
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/geoffreylitt/micro-worlds/SKILL.md fully, then build
a step-through replay of the migration script in <path> so I can watch what
it does one step at a time before running it for real.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- One disposable interactive artifact — typically a single self-contained
  HTML file or small script, openable with no build step or dependencies —
  kept in the run's artifact directory (or uncommitted) only while it is
  actively teaching.
- It is driven by the real code and real data (actual state fields, paths,
  values), with any simplification declared inside the world itself.
- The producer names the understanding gap that justified building it; the
  human is expected to spend time inside — predicting, scrubbing, stepping
  — and to be able to state what surprised them.
- "Done" per the SKILL.md Verification checklist: any instrumentation added
  to real code removed or gated before delivery, and the artifact's fate
  (discarded, or temporarily kept) explicit.
- Misapplication signs (from Red Flags): the world renders a story about
  the code rather than its actual execution; the artifact acquires tests,
  CI, or feature requests; the human never actually opened it.

## Worked example

Request: "Migrate our flat asset directory into the new content-addressed
store" runs through `sdlc`; the script moves thousands of files and the
owner's honest model is "a bunch of files go a bunch of places". Attach to
`implement` (as in the snippet above). Expected output: alongside the
migration script, a single `replay.html` in the stage's artifact directory
with a "next step" button showing each real move command and the
before/after directory trees side by side, driven by the script's actual
planned operations. The owner steps through it, notes what surprised them
(e.g. collision handling), and the file is discarded once the migration is
understood and delivered.
