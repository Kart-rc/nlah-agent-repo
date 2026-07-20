---
name: problem-framing
description: Turns unowned, cross-cutting ambiguity into a crisp, falsifiable problem statement before any solutioning. Use when a problem spans teams with no owner, when stakeholders disagree on what the problem even is, when a request arrives pre-shaped as a solution, or when work keeps stalling because its goal is contested.
---

# Problem Framing

## Overview

The hardest problems in an organization are the ones nobody owns: they span
teams, arrive disguised as solutions, and stall because everyone is solving
a different version of them. The distinguished engineer's first move is not
a design — it is a problem statement sharp enough to be wrong. This skill
is the discipline of framing before solving.

## When to Use

- A problem spans multiple teams and no one owns it
- Stakeholders keep talking past each other about what the problem *is*
- A request arrives pre-shaped as a solution ("we need a service mesh")
- Work in an area repeatedly stalls or reboots because its goal is contested

**When NOT to use:** Routine requirements-gathering for a well-owned feature
request — that is the `intake` stage's job, with
`addyosmani/interview-me`. If a crisp problem statement already exists and
is agreed, move on; re-framing settled problems is procrastination with
extra steps.

## Name the Problem, Not the Solution

Requests arrive as solutions; problems must be excavated from them.

- When handed a solution ("we need X"), ask what becomes possible or stops
  hurting once X exists — *that* is the problem. Record it separately from
  the proposed X, which is now merely one candidate.
- Push up the **why-chain** until you hit something a stakeholder would pay
  to change; push no further. Framing at too high an altitude ("improve
  reliability") is as useless as too low ("add a retry here").
- One problem per statement. "And also" is where framings go to die —
  split conjoined problems and let each earn its own priority.

## Make the Forces Visible

A frame that hides the forces produces solutions that snap back.

- Name the **actors**: who feels the pain, who causes it (usually
  innocently), who can change it, who will resist and why. A problem
  without a person feeling it is a hobby.
- Name the **constraints** that any solution must respect — compliance,
  cost ceilings, systems that cannot change on this horizon — and separate
  real constraints from incumbent habits wearing constraint costumes.
- State **why this is hard** and **why now**. If nothing changed, the
  problem was survivable yesterday and will be survivable tomorrow — the
  frame must say what broke, grew, or shifted.

## Falsifiable Problem Statements

A statement no evidence could contradict is a mood, not a frame.

- State the **current condition measurably**: what happens today, how
  often, costing what. "Deploys are painful" becomes "a routine deploy
  takes 6 hours of engineer attention and fails one time in five."
- State the **cost of doing nothing** on a horizon — the frame must make
  inaction a choice with a price, or prioritization against funded work is
  impossible.
- Write **decidable done-criteria**: the observable conditions under which
  this problem would be declared solved. If reasonable people could
  disagree about whether it is solved, the frame is not done.
- Include the **disconfirming test**: what evidence would show this problem
  is smaller or different than claimed. A frame that cannot be wrong
  cannot be trusted.

## Carve an Ownable First Slice

Org-shaped problems die of their own size; frames must cut.

- From the full problem, carve a **first slice** small enough for one team
  to own end-to-end and valuable enough to matter on its own — the slice
  proves the frame, not just the solution.
- Choose the slice that **maximizes learning per unit of commitment**: the
  one whose outcome most changes what you would do next.
- Name the owner of the slice before circulating the frame. A framing
  document without a candidate owner is a petition.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Everyone already knows what the problem is" | Then writing it down is cheap. Disagreement discovered in writing costs a page; discovered in production costs a quarter. |
| "The requester asked for X, so build X" | The requester diagnosed under their own constraints. Honor the pain, audit the prescription. |
| "We can't measure it, but it's clearly bad" | Unmeasured problems lose planning fights to measured ones. Even a defensible estimate beats an adjective. |
| "Scoping it down loses the big picture" | An unowned big picture solves nothing. The slice is how the big picture gets its first proof. |

## Red Flags

- The "problem statement" contains a product name
- No named person or team who feels the pain
- "Improve", "modernize", or "streamline" doing load-bearing work
- No answer to "why now?"
- Done-criteria that a reasonable person could argue either way
- A frame that has survived two quarters without anyone owning a slice of it

## Verification

- [ ] Problem stated separately from any proposed solution, one problem per statement
- [ ] Actors named: who hurts, who causes, who can change, who will resist
- [ ] Real constraints separated from habits; each constraint sourced
- [ ] Current condition stated measurably; cost of doing nothing priced on a horizon
- [ ] "Why now" answered with what changed
- [ ] Done-criteria decidable; disconfirming evidence identified
- [ ] First slice carved: ownable by one team, valuable alone, with a candidate owner
