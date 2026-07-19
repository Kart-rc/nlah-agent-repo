---
name: large-scale-migration-design
description: Designs migrations that are incremental, observable, and reversible at every step. Use when moving data, traffic, or dependents between systems at a scale where a big-bang cutover would be unrecoverable - datastore swaps, API platform moves, monolith strangling, or multi-team dependency shifts.
---

# Large-Scale Migration Design

## Overview

Migrations are where architectures go to die: the old system is
load-bearing, the new one is unproven, and the org's patience is finite.
The graveyard is full of big-bang rewrites that were 80% done for three
years. This skill is the discipline of designing migrations as a sequence
of small, observable, reversible steps — where the risky moment is never
larger than one step, and "done" includes the old system's funeral.

## When to Use

- Moving data, traffic, or dependents between systems where botching the
  cutover is unrecoverable or unaffordable
- Datastore swaps, API platform moves, monolith strangling, auth or
  identity migrations, multi-team dependency shifts
- Reviewing a migration plan for survivability

**When NOT to use:** Deprecation policy, sunset timelines, and user
communication are `addyosmani/deprecation-and-migration` — that skill
retires the old thing; this one designs the mechanics of getting to the
new one. A refactor within one codebase behind stable interfaces needs
`addyosmani/code-simplification`, not a migration design.

## No Big Bang

The cutover you cannot rehearse is the cutover you should not take.

- **Strangle, don't replace**: route slices of traffic, data, or dependents
  through the new system while the old one keeps working. The old system
  is load-bearing until measurement — not hope — says otherwise.
- Slice so each increment **pays for itself**: a tenant served better, a
  query faster, a team unblocked. A migration whose value all arrives at
  the end will be cancelled in the middle, and deserves to be.
- Sequence by **risk-and-learning**: migrate a representative-but-
  survivable slice first. The first slice's job is to falsify the design
  cheaply; the whales come last, when the path is worn smooth.
- Assume **mid-migration is a resting state**. Priorities shift; the plan
  must leave the system coherent — both halves operable, no data
  stranded — if the org pauses at any step. A plan that is only safe when
  finished is a trap with a roadmap.

## Parallel Run and Shadow Verification

Correctness is demonstrated in production shadow, not asserted in review.

- **Dual-write / shadow-read**: write to both systems, serve from the old,
  compare answers continuously. The new system earns traffic by agreeing
  with reality, not by passing its own tests.
- Define a **divergence budget** before the run: which mismatches block
  cutover, which are known-acceptable (and why), and the rate below which
  you may proceed. Undefined tolerance becomes negotiated-under-deadline
  tolerance.
- **Reconcile continuously**, not once: divergence found weeks later is
  archaeology; found in minutes it is a stack trace. Alert on divergence
  like the production incident it is about to become.
- Shadow the **full read path** under real traffic patterns — synthetic
  benchmarks flatter the new system; production data is where the edge
  cases live.

## Reversible Cutover

Every step forward must know its way back.

- Every step ships with a **tested rollback**: not a paragraph, a
  procedure — exercised before the step runs, with the data-consistency
  story stated (what happens to writes accepted since the step?).
- Name the **point of no return** explicitly — the step after which
  rollback becomes restore-from-backup. Gate it on the divergence budget,
  a soak period, and a human decision made in daylight.
- Prefer **flags and percentage ramps** over deploy-shaped cutovers:
  moving 1% → 10% → 50% of traffic with observation between ramps turns
  the cliff into a staircase.
- Keep the old path **warm during soak**: a rollback target that has taken
  no traffic for a month is not a rollback target; it is a second
  migration.

## The End State Is Part of the Design

A migration that never ends is a permanent tax with two systems' overhead.

- Write **exit criteria** at design time: the observable conditions
  (traffic percentages, dependent counts at zero, data parity confirmed)
  under which the old system dies. "When we're confident" is not a
  criterion; it is a mood.
- **Decommissioning is in scope**: shutting down the old system, deleting
  the dual-write shims, removing the compatibility layers, ending the
  contracts. The migration is done when the old path is gone — not when
  the new path works.
- Track the **long tail by name**: the last 5% of dependents are the
  expensive ones — enumerate them, assign owners and dates, and burn the
  list down publicly. Untracked tails become permanent residents.
- Budget the **double-run cost** honestly (infra, oncall, cognitive load
  of two systems) and give it a deadline. That cost is the strongest
  argument for finishing — use it.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "A clean cutover weekend is simpler" | Simpler to describe, unrecoverable to botch. The weekend plan is a bet of the whole system on zero surprises. |
| "The new system passed all its tests" | Its own tests. Production data holds the edge cases nobody imagined; shadow traffic finds them without casualties. |
| "We'll figure out rollback if we need it" | A rollback designed during the incident is improvisation with an audience. |
| "99% migrated is basically done" | The remaining 1% costs two systems' oncall forever. Basically-done is the most expensive state a migration has. |
| "We'll decommission it next quarter" | Next quarter has its own priorities. Undated funerals don't happen. |

## Red Flags

- A cutover date but no ramp plan between 0% and 100%
- No divergence budget — or one negotiated after mismatches appeared
- Rollback documented but never exercised; no data story for post-step writes
- Value backloaded: nothing improves until the final step
- A plan that is incoherent if paused mid-way
- No named exit criteria, no decommission owner, an unenumerated long tail
- The old system's deletion missing from the plan entirely

## Verification

- [ ] Migration decomposed into slices; each pays for itself; first slice chosen to falsify cheaply
- [ ] System coherent at every intermediate state - a pause strands nothing
- [ ] Parallel run designed: dual-write/shadow-read with continuous reconciliation
- [ ] Divergence budget defined before the run; alerting on divergence in place
- [ ] Every step has a tested rollback with an explicit data-consistency story
- [ ] Point of no return named and gated on budget, soak, and daylight decision
- [ ] Exit criteria observable; decommissioning scoped, owned, and dated
- [ ] Long tail enumerated with owners; double-run cost budgeted with a deadline
