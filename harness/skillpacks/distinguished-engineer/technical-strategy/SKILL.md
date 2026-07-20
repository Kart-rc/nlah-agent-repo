---
name: technical-strategy
description: Sets multi-year technical direction as a portfolio of sized bets with kill criteria. Use when writing or judging a technical strategy, north-star architecture, or roadmap, when sequencing stepping-stone investments, or when deciding whether an emerging technology is worth adopting now, trialing, or merely watching.
---

# Technical Strategy

## Overview

Most documents titled "strategy" are lists of aspirations with dates. A
strategy is something else: a diagnosis of the situation, a policy for
dealing with it, and a coherent set of actions that follow — placed as bets
you can size, sequence, and kill. This skill is the discipline of setting
technical direction that survives three years of changing facts.

## When to Use

- Writing or judging a technical strategy, north-star architecture, or
  multi-year roadmap
- Sequencing platform investments when everything looks important
- Annual or quarterly planning where technical direction is on the table
- Deciding whether an emerging technology deserves adoption, a trial, or a
  watchful distance

**When NOT to use:** A single bounded decision ("which queue do we pick?") —
that is the tech-decision workflow and
`tech-director/options-and-tradeoffs`. Packaging a decided strategy for
executives is `tech-director/executive-communication`.

## Strategy Is Diagnosis, Not Goals

"Be the best platform team" is a wish. Strategy starts with what is true.

- Lead with a **diagnosis**: the handful of facts about the system, the org,
  and the market that explain why the current trajectory is not good enough.
  If the diagnosis is wrong, everything downstream is decoration.
- From the diagnosis, one **guiding policy** — the approach that addresses
  it — and from the policy, **coherent actions** that visibly implement it.
  Actions that do not trace to the policy are somebody's pet project wearing
  a strategy's badge.
- A real strategy says **no** to specific attractive things. If nothing was
  excluded, nothing was decided — a strategy that permits everything is a
  budget allocation, not a direction.

## North Star and Stepping Stones

The target architecture is a direction, not a destination.

- Describe the **north star** in terms of properties (what becomes possible,
  what becomes cheap) rather than boxes and arrows. Diagrams of a future
  that far out are fiction with confidence intervals.
- Sequence **stepping stones**: each step must be independently valuable
  even if the north star is later abandoned. A three-year plan whose payoff
  all arrives in year three is a hostage situation.
- Re-derive the path when facts change; keep the diagnosis current. A
  strategy document that has not been revised in a year is a historical
  artifact.

## Bet Sizing and Kill Criteria

Direction-setting is portfolio management under uncertainty.

- Classify each investment by size and reversibility: many small two-way
  bets, few named one-way ones. The one-way bets get the scrutiny; the
  two-way ones get speed.
- Write **kill criteria before evidence arrives**: what observable result,
  by what date, means this bet is dead. Deciding what failure looks like
  after you are emotionally invested is how zombie projects are born.
- Killing a bet on its criteria is the system working, not a failure to
  punish. A portfolio where nothing ever dies is not a portfolio; it is a
  backlog with tenure.

## Adoption Rings for Emerging Tech

New technology is a stream of claims; the strategy needs a filter.

- Place each candidate in a ring — **adopt / trial / assess / hold** — and
  make movement between rings an explicit, evidenced decision, not osmosis.
- A **trial** is a bounded bet: one team, one real workload, an exit date,
  and kill criteria like any other bet. "We're trying it" without a
  boundary is adoption by drift.
- Filter hype by asking what the technology makes *cheap* that the diagnosis
  says is *expensive*. A technology that solves no named problem in the
  diagnosis belongs in assess or hold, however loud the conference talks.
- Account for innovation tokens across the portfolio: several concurrent
  novel adoptions spend operational attention the strategy has not budgeted.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The goals are ambitious — that's the strategy" | Ambition without diagnosis is a wish list. The strategy is the explanation of *how*, and what it excludes. |
| "We'll evaluate the big bet at the end" | By then sunk cost votes. Kill criteria written at the start are the only honest evaluation. |
| "Everything on the roadmap is critical" | Then nothing is. A strategy that cannot rank has not decided. |
| "We can't afford to fall behind on <new tech>" | Fear of missing out is not a diagnosis. Name what it makes cheap that you need cheap, or hold. |
| "The plan pays off in year three" | Facts will change by then. Steps must pay for themselves, or the strategy is a hostage negotiation. |

## Red Flags

- A strategy document with goals and dates but no diagnosis
- No named thing the strategy chooses *not* to do
- Stepping stones that are worthless unless the entire vision lands
- Big bets with no kill criteria, or criteria invented after the evidence
- Technology adoption happening by drift — no ring, no boundary, no exit date
- A "strategy" untouched since the facts it rests on changed

## Verification

- [ ] Diagnosis stated first: the facts that make the current trajectory insufficient
- [ ] One guiding policy; every proposed action traces to it
- [ ] At least one attractive option explicitly excluded, with reasoning
- [ ] Every stepping stone independently valuable if the north star is abandoned
- [ ] Each bet sized and classified by reversibility; one-way bets named
- [ ] Kill criteria written for every major bet — observable result and date
- [ ] Emerging-tech positions placed in adopt/trial/assess/hold with evidence
