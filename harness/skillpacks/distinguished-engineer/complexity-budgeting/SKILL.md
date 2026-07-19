---
name: complexity-budgeting
description: Treats system complexity as a budget to be spent deliberately, audited, and clawed back. Use when a system has accreted concepts faster than capabilities, when choosing between a design that adds a mechanism and one that removes one, when scheduling deprecation or deletion work, or when judging whether new complexity pays rent.
---

# Complexity Budgeting

## Overview

Systems do not become unmaintainable in one decision. They accrete: a flag
here, a special case there, a second queue because the first was busy —
each defensible, the sum lethal. Complexity is the one resource every
project spends and almost none accounts for. This skill is the discipline
of treating it as a budget: counted, audited, and clawed back, with
deletion as first-class engineering work.

## When to Use

- A system has accreted concepts faster than capabilities
- Choosing between a design that adds a mechanism and one that removes one
- Scheduling deprecation, consolidation, or deletion work against feature
  pressure
- Judging whether a proposal's new complexity pays rent

**When NOT to use:** Behavior-preserving code-level cleanup — renames,
extractions, dead-code sweeps within a module — is
`addyosmani/code-simplification`. This skill works a level up: concepts,
services, mechanisms, and config surfaces across a system or portfolio.

## Complexity Is Spend

You cannot budget what you refuse to count.

- Count **concepts, not lines**: every service, queue, flag, config
  dimension, consistency domain, and "mode" is a thing every future
  engineer must load into their head before touching the system. Lines
  are cheap; concepts compound.
- Each concept charges **recurring rent**: onboarding time, debugging
  surface, test matrix rows, upgrade coordination, documentation drift.
  The purchase price is the smallest payment you will ever make on it.
- Concepts **multiply, not add**: three flags is eight states; a mode
  crossed with a tenant type is a test matrix. Budget for the
  interactions, because production will find them whether you counted
  them or not.
- Judge spend against **carrying capacity** — the team as staffed, not as
  wished. A complexity load that assumes the departed expert still works
  here is already in default.

## Hunt Accidental Complexity

Most complexity is not the problem's; it is the history's.

- Separate **essential from accidental**: essential complexity mirrors the
  problem domain; accidental complexity mirrors the org chart, the
  outage-of-the-week it was built after, and the framework fashions of
  its birth year. Only the first kind is untouchable.
- Practice **complexity archaeology**: for each suspicious mechanism, ask
  what it protects against and whether that threat still exists. Systems
  are full of armor for wars that ended — load-shedding for a traffic
  pattern retired in 2019, an abstraction layer for a second backend that
  never came.
- The tell of accidental complexity is **explanation by narrative**: if
  the answer to "why is this here?" is a story about the past rather than
  a requirement in the present, it is a deletion candidate.
- Beware **speculative generality** — the plugin system with one plugin,
  the multi-cloud abstraction on one cloud. Optionality you are not
  exercising is complexity you are financing.

## Deletion Is a Feature

Code is a liability; capability is the asset.

- Schedule **deletion as roadmap work** with the same standing as
  features: named projects, owners, and celebrated completions. What is
  only ever done "when there's slack" is never done — there is no slack.
- Give new mechanisms **sunset criteria at birth**: the conditions under
  which this flag, shim, or compatibility layer gets removed, and who
  owns removing it. A temporary mechanism without an owner and a date is
  permanent — everyone in the room knows it.
- **Deprecate loudly, delete on schedule**: mark it, warn on use, measure
  remaining callers, burn the list down by name. Half-deprecated is the
  worst state — the maintenance cost of alive, the trust of dead.
- Measure simplification by **concepts removed**, not lines: a refactor
  that shrinks the concept count changed what the system costs to think
  about; one that only shuffles lines changed its haircut.

## Prefer Concept-Removing Designs

The best response to new requirements is sometimes a smaller system.

- When comparing designs, weigh **net concept count**: the design that
  meets the requirement by *generalizing* an existing mechanism beats the
  one that adds a sibling. Two similar mechanisms is a merge waiting to
  happen — or worse, one that never does.
- Ask of every new mechanism: **what does this make unnecessary?** The
  strongest designs pay for their complexity by retiring more than they
  add. A design that only ever adds is running a deficit.
- Resist the **special case** at the door: today's if-branch for one
  tenant is tomorrow's mode, next year's parallel system. Either the case
  generalizes into the model or it earns a documented, sunset-dated
  exception.
- Sometimes the winning proposal is **subtraction**: the requirement
  dissolves when the two half-redundant systems become one. The engineer
  who spots that move saves more than any feature ships.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "It's just one more flag" | Flags multiply states, not add them. The eighth flag is the 256th state, and QA tests twelve of them. |
| "We might need the general version later" | The general version costs now and forever; "later" may never come. Build for the requirement you have. |
| "Deleting it is risky - something might depend on it" | Not knowing your dependents is the risk; the dead code is just where it hides. Measure callers, then delete. |
| "There's no time for cleanup this quarter" | The rent gets paid either way - as scheduled work or as slower everything, forever. |
| "It works, why touch it?" | It charges rent whether or not it breaks: onboarding, debugging surface, test rows. Working is not free. |

## Red Flags

- Nobody can enumerate the system's modes, flags, and their interactions
- Mechanisms whose explanation is a history lesson, not a requirement
- "Temporary" shims with no owner, no sunset date, and a second birthday
- A plugin architecture with one plugin; a multi-backend layer with one backend
- Deprecations announced years ago with callers still growing
- Roadmaps that only ever add: no deletion project in living memory
- Special cases accumulating per-tenant, per-region, per-legacy-client

## Verification

- [ ] New complexity counted in concepts and interactions, not lines
- [ ] Each new concept's recurring rent named and judged against team carrying capacity
- [ ] Accidental complexity distinguished from essential; archaeology done on suspects
- [ ] Every new mechanism carries sunset criteria and a removal owner from birth
- [ ] Deletion/consolidation work scheduled as named roadmap items
- [ ] Competing designs compared on net concept count; "what does this retire?" answered
- [ ] Special cases either generalized into the model or documented with a sunset date
