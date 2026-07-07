---
name: risk-mitigation
description: Turns vague worry into an actionable risk register. Use when assessing an initiative's risks, writing the risk sections of decisions and proposals, or running a pre-mortem before committing to a course of action.
---

# Risk Mitigation

## Overview

Every plan carries risk; the leadership act is making it *legible* — named,
scored, owned, and watched — so risk is taken deliberately instead of
discovered operationally. This skill covers register discipline, the
mitigation/contingency distinction, and the pre-mortem method for finding
the risks a forward-looking analysis misses.

## When to Use

- Writing the risks section of a decision record, assessment, or proposal
- Standing up or reviewing a risk register for an initiative
- Before committing to a one-way door
- After a near-miss, to capture what almost happened

**When NOT to use:** Cataloging every conceivable misfortune. A register
with forty entries and no tolerance line is a liability disclaimer, not a
management tool.

## Risks Are Concrete Events

A risk is a specific event with a causal consequence: "**X happens, causing
Y**."

- Bad: "security risk", "timeline risk", "vendor risk" — these are
  categories, not risks. You cannot mitigate a category.
- Good: "The vendor deprecates the v2 API before our migration completes,
  causing a 6-week unplanned rewrite."
- Score each risk **likelihood × impact** on a stated scale (e.g. 1-5 each),
  and draw a **tolerance line**: above it, full treatment; below it,
  acknowledged and left alone. The scale and line must be written down, or
  scores are theater.

## Coverage Without Padding

Sweep the standard categories, then explicitly rule out the empty ones:
**technical, delivery/schedule, people/organizational, dependency/vendor,
security/compliance, cost**. "No material people risk identified, because
the team is stable and the skills exist in-house" is a finding; silence is a
gap.

## Mitigation vs Contingency

Two different instruments, never the same text:

- **Mitigation** reduces likelihood or impact *now*, before the event:
  "run both systems in parallel for one billing cycle."
- **Contingency** is what you execute *when the trigger fires*: "if
  reconciliation diverges >0.1%, cut back to the legacy path within one day."
- The register anti-pattern is writing the same sentence in both columns.
  If mitigation and contingency read alike, one of them does not exist.
- Not every risk deserves both. **Accepting** a risk is legitimate — when it
  is written down as accepted, with the reason.

## Owners and Triggers

- **Every risk above the line has one named owner** — a person, not a team.
  A risk owned by "the platform team" is owned by no one; a risk with no
  owner is an accepted risk in denial.
- Give each owned risk a **leading-indicator trigger**: an observable signal
  that fires *before* the impact lands ("error budget burn >2x for two
  consecutive weeks"), not after ("customers churn"). Lagging triggers make
  the contingency a post-mortem.

## The Pre-mortem

Forward analysis finds the risks you already believe in. The pre-mortem
finds the others:

1. Assume total failure: "It is six months later. This initiative failed."
2. Each participant (or you, in multiple honest passes) writes the story of
   *why* — narrative, not bullet points; stories surface causal chains.
3. Map each story back to register entries. A failure story with no
   corresponding risk is a register gap — add it.
4. Pay special attention to stories about people and organizations; those
   are the risks technical registers systematically omit.

## Register Lifecycle

- A register is a living document with a **review cadence** matched to the
  initiative's tempo; each review re-scores, checks triggers, retires risks.
- **Retire** risks whose window has passed — a register that only grows
  stops being read.
- Keep the **accepted risks** section honest and visible: what is
  consciously not being mitigated, and why. That section is where most of
  the register's integrity lives.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Listing risks makes the plan look weak" | Discovered risks kill plans; declared risks get budgets and owners. |
| "We'll deal with it if it happens" | That is a contingency — so write it down, with the trigger that invokes it. |
| "Everything is low probability" | Multiply by impact. Rare × catastrophic is what registers exist for. |
| "The team owns it collectively" | Collective ownership is how risks sit on registers while projects die of them. |

## Red Flags

- Category names ("security risk") in place of events
- No stated scoring scale or tolerance line
- Mitigation and contingency columns containing the same words
- Owners that are teams; triggers that are lagging indicators
- No accepted-risks section (nothing is ever consciously accepted?)
- A register untouched since kickoff

## Verification

- [ ] Every risk is an "X happens, causing Y" event, scored on a stated scale
- [ ] Standard categories covered or explicitly ruled out
- [ ] Above-the-line risks each have one named owner, a leading-indicator trigger, a mitigation, and a distinct contingency
- [ ] Pre-mortem run; every failure story maps to a register entry
- [ ] Accepted risks written down with reasons
- [ ] Review cadence stated
