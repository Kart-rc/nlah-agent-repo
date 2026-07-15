---
name: micro-worlds
description: Build a small, ephemeral, interactive artifact (debugger, timeline scrubber, step-through simulation) whose only purpose is to let a human inhabit and feel how a piece of code behaves. Use when reading the code or an explainer leaves no intuitive grasp of runtime behavior, when internal state is complex, or when a script's effects are easier to watch than to read.
---

# Micro-Worlds

## Overview

Kids learn French by living in France; Seymour Papert asked where a child
would live to learn math the same way. A micro-world is that answer applied
to code: a purpose-built, throwaway interactive environment — a state
visualizer, a timeline scrubber over an interpreter, a click-through replay
of a migration — that lets a human *inhabit* how the system behaves rather
than only read about it. The point is never the artifact. The point is the
changed human: agents can write code to help us understand code, where
nothing built is meant to ship.

## When to Use

- An algorithm, interpreter, or state machine whose internal state evolves
  in ways prose and diffs make feel harder than they are
- A migration or script that moves many things, where "a bunch of files
  went a bunch of places" is the honest current level of understanding
- Debugging where you want peripheral vision — a feel for the machine —
  not just the narrow fix
- The moment you catch yourself saying "I read it, but I have no feel for
  what it's doing"

**When NOT to use:** When a static explainer already produces genuine
understanding (build the cheapest thing that works — see `code-explainers`
first), or when the system's behavior is trivial enough that interaction
would demonstrate nothing.

## Forms That Work

- **State-over-time debugger:** run the real system step by step, record
  every state, and put a scrub bar over the timeline. Watching state evolve
  builds the intuition that a description of state cannot.
- **Step-through replay:** for scripts and migrations, a "next" button that
  performs (or simulates) one real step at a time, showing the commands
  being run and the before/after world side by side — doing the port by
  hand, minus the pain.
- **Drag-to-explore simulation:** for spatial, geometric, or parametric
  logic, direct manipulation with live readouts of the underlying values
  and computations.
- **Annotation surface:** let the explorer leave comments pinned to
  timeline points or states, so the understanding built is captured where
  it happened.

## Truthfulness

A micro-world teaches only if it is wired to the truth.

- Drive it from the **real code and real data** — instrument the actual
  interpreter, replay the actual script's operations, render the actual
  state. A hand-waved animation of how the system *probably* works teaches
  a fiction.
- Show real values: actual coordinates, actual file paths, actual state
  fields — not stylized stand-ins.
- If the world must simplify, say so in the world itself, and never
  simplify the part the human is trying to understand.

## Ephemerality

The artifact is scaffolding, and scaffolding comes down.

- Build it cheap: a single self-contained HTML file or a small script,
  openable immediately, with no build step and no dependencies to install.
- No production bar applies: no tests, no error handling beyond what the
  exploration needs, no review, and it is never shipped or maintained.
- It is disposable once understanding is achieved. Keep it (uncommitted, or
  in the run's artifact directory) only as long as it is actively teaching;
  resist the urge to productize it.
- Instrumentation added to real code to feed the world must be removed (or
  explicitly gated) before the change is delivered.

## Inhabit It

Understanding comes from living in the world, not from having built it.

- Spend real time inside: scrub the timeline, step the migration, drag the
  parameters, try to predict the next state before revealing it.
- Use it to do narrow work — fix the bug, verify the step — and collect
  the peripheral vision that comes for free: the feel for the machine that
  an agent-only fix never gives you.
- Note what surprised you; surprises are precisely the gaps between your
  model and the system, which is what the exercise exists to find.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Building a UI just to understand is wasteful" | Code is cheap now. An hour of agent-built micro-world against a system you'll steward for years is one of the cheapest purchases available. |
| "I'll just read the code more carefully" | You already did. Some behavior is feelable only by watching state evolve; that is why debuggers exist. |
| "This visualizer is nice — let's ship it" | Then it becomes software: tests, review, maintenance. The point was the changed human, not the artifact. Shipping it is a separate, deliberate decision. |
| "A mocked animation is faster to build" | A fiction that looks like the system installs a wrong model more durably than no model at all. Wire it to the truth or don't build it. |

## Red Flags

- The micro-world renders a story about the code rather than the code's
  actual execution or data
- A build step, dependency install, or deployment between the human and
  opening it
- The artifact acquiring tests, CI, or feature requests (it is becoming a
  product without a decision)
- Instrumentation for the world left in delivered code
- The human who needed understanding never actually used it
- A micro-world built where one static diagram would have done

## Verification

- [ ] A named understanding gap justified building the world (and a static explanation was considered first)
- [ ] The world is driven by real code/data, with any simplifications declared
- [ ] Self-contained and instantly openable — no build step or dependencies
- [ ] The human spent time inside it and can state what surprised them
- [ ] Any instrumentation added to real code removed or gated before delivery
- [ ] The artifact's fate is explicit: discarded, or kept in the run's artifact directory while still teaching
