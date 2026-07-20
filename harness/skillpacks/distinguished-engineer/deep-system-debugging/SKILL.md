---
name: deep-system-debugging
description: Diagnoses cross-system and unfamiliar-territory failures that have resisted routine debugging. Use when a bug spans services, layers, or codebases nobody fully owns, when the failure is intermittent or environment-dependent, or when you are the escalation point after other attempts have stalled.
---

# Deep System Debugging

## Overview

Some bugs do not yield to the routine loop of read-the-stack-trace,
find-the-commit, write-the-fix. They live between systems, reproduce only
under moon phases, and arrive at your desk precisely because three other
capable people have already stalled. This skill is the escalation-tier
discipline: method that works when familiarity does not, because at this
tier method is all you have.

## When to Use

- The failure spans services, layers, or codebases that no one fully owns
- The bug is intermittent, environment-dependent, or "impossible"
- You are the escalation point: others have already tried the obvious
- The symptom and the cause are plausibly far apart (data corruption,
  clock skew, cache coherence, partial deploys)

**When NOT to use:** Routine in-repo debugging — a failing test, a clear
stack trace, a recent suspect commit — is
`addyosmani/debugging-and-error-recovery`. Reaching for escalation-tier
method on a routine bug is procrastination dressed as rigor.

## Establish the Invariants

Do not chase the symptom; find the first broken promise.

- List what **must be true** for the system to behave: orderings,
  uniqueness, monotonic clocks, at-most-once delivery, schema agreement.
  Then test them — the bug lives at the first invariant that fails, which
  is usually several systems upstream of the symptom.
- An "impossible" error is a **wrong assumption wearing a mask**. When the
  logs show what cannot happen, one of your certainties is false;
  enumerate them and start checking the ones you are most sure of.
- Trust **evidence over testimony**. "That service can't be the problem,
  we didn't change it" is a hypothesis, not a fact — dependencies,
  traffic, and data change systems that nobody touched.
- Write down what you have **verified versus assumed**. At the escalation
  tier the two lists are always different, and the bug is on the second
  one.

## Hypothesis Trees, Not Hunches

Escalated bugs have survived hunches; they do not survive bookkeeping.

- Enumerate **competing explanations** before testing any — a tree of
  hypotheses, each with the evidence that would confirm or kill it. One
  hypothesis at a time is how the first three attempts stalled.
- Choose the next experiment by **information per cost**: prefer the
  cheap test that halves the tree over the expensive one that confirms a
  favorite. You are buying bits, not vindication.
- **Record kills.** A hypothesis eliminated with its evidence is progress
  someone else can build on; an untracked kill will be re-investigated by
  the next person — often you, on Thursday.
- When all hypotheses are dead, the tree was too small: widen a layer
  (hardware, clock, config distribution, deploy skew) rather than
  re-testing the corpse of a favorite.

## Bisect Every Axis

Bisection is not just for commits; every axis of variation cuts.

- **Time**: when did it last work? Commits, deploys, config pushes,
  certificate rotations, dependency bumps — the changelog of every system
  in the path, not just yours.
- **Space**: which hosts, regions, cells, tenants exhibit it? A failure
  that respects a boundary is telling you which wall it lives inside.
- **Data**: shrink the triggering input; find the record, the character,
  the size threshold. Working versus broken payloads differ by something —
  diff them.
- **Environment and config**: what differs between where it fails and
  where it does not? Flags, versions, kernels, locales, limits. Divide the
  difference set in half and test.
- Keep each bisection **honest**: one variable per step. Changing two
  things and seeing recovery teaches you nothing you can keep.

## The Minimal Repro Obligation

The repro is a deliverable, not a private convenience.

- Shrink the reproduction until every remaining element is **load-bearing**
  — remove any piece and the bug vanishes. What remains is the bug's true
  shape, and often names the culprit by itself.
- A minimal repro converts an escalation into a bug **anyone can fix**:
  it survives handoffs, timezone gaps, and your vacation.
- For intermittent failures, the repro target is a **rate**: from "sometimes
  in prod" to "one in twenty runs of this script" is a diagnosis-grade
  improvement — amplify with load, delay injection, or forced orderings.
- If a true repro is impossible, the fallback deliverable is a
  **falsifiable narrative**: the timeline of events, each step evidenced,
  that an instrumented next occurrence will confirm or refute. Ship the
  instrumentation before closing.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "It's probably the same as last time" | Pattern-matching is how the first three attempts stalled. At this tier, evidence outranks resemblance. |
| "We didn't change anything" | Your dependencies, data, traffic, and certificates did. "No changes" means "no changes we noticed." |
| "It stopped happening, closing it" | An undiagnosed disappearance is a scheduled reappearance — at higher load, on a worse day. |
| "Adding logging everywhere will find it" | Undirected logging is noise with storage costs. Instrument the hypothesis, not the codebase. |
| "I'm close, no time to write it down" | Untracked state evaporates at the first interruption. The bookkeeping *is* the speed. |

## Red Flags

- Fixes attempted before any hypothesis was written down
- The same hypothesis investigated twice because its first death went
  unrecorded
- "Impossible" in the incident channel without an assumption audit
  following it
- Two variables changed in one experiment, recovery declared victory
- A "fix" shipped without a mechanism story linking cause to symptom
- Mitigation mistaken for diagnosis: restarts cure the symptom and the
  investigation

## Verification

- [ ] Invariants listed and tested; first violated invariant identified
- [ ] Verified facts separated from assumptions, in writing
- [ ] Hypothesis tree with competing explanations; kills recorded with evidence
- [ ] Experiments chosen by information-per-cost, one variable each
- [ ] Bisection run on the relevant axes: time, space, data, config
- [ ] Minimal repro produced (or rate-repro / instrumented falsifiable narrative)
- [ ] Fix explains the full mechanism from cause to observed symptom
