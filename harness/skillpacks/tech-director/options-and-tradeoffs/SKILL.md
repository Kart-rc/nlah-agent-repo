---
name: options-and-tradeoffs
description: Builds decision-grade option matrices. Use when a decision has more than one viable path and someone must later defend the choice - technology selection, build-vs-buy, architectural direction, vendor evaluation.
---

# Options and Trade-offs

## Overview

A decision is only as good as the option space it was made in. This skill
covers structuring that space: deriving decision drivers from requirements
*before* looking at options, scoring options honestly against those drivers,
and exposing the trade-offs so the eventual call can be defended — or
overturned — on evidence.

The discipline exists to defeat the most common decision failure: choosing
first and constructing the analysis afterwards.

## When to Use

- Choosing between technologies, architectures, vendors, or approaches
- Build-vs-buy questions
- Any decision expensive enough that someone will later ask "what else did you consider?"
- Preparing the option matrix a decision record will trace to

**When NOT to use:** Decisions with one viable path (document why and move
on), trivially reversible choices where trying beats analyzing, or decisions
already made above your head (record the constraint, don't re-litigate it).

## Drivers Before Options

Derive decision drivers — the dimensions that matter and their weights — from
the requirements *before* enumerating options.

- Every driver traces to a requirement or stated constraint. A weight you
  cannot trace is a preference wearing a costume.
- Weights are relative and explicit (e.g. 1-5), agreed before scoring begins.
- Typical driver families: fitness for the requirement, total cost,
  operational load, reversibility, team capability, time to value, risk.
- If a new driver appears mid-analysis, stop: either it traces to a
  requirement (add it openly and re-score everything) or it is a preference
  smuggled in to rescue a favorite.

## Matrix Discipline

- Score **every option against every driver**, with a one-line justification
  per cell. A cell you cannot justify is an assumption — label it as one.
- Justifications cite evidence (research, benchmarks, prior art), not vibes.
- **Sensitivity check:** ask "which single weight or assumption change flips
  the ranking?" If a small, plausible change flips it, say so — the decision
  is closer than the totals suggest, and the decider deserves to know.
- The classic fraud is reverse-engineering: adjusting weights until the
  favorite wins. The tell is weights that cannot be traced to requirements,
  or that changed after scoring started.

## Cost Realism

Sticker price is the smallest number. Price every option as total cost of
ownership:

- **Build cost** — engineering time to first value, including integration.
- **Run cost** — hosting, licenses, upgrades, on-call, the team that carries
  the pager.
- **Opportunity cost** — what the same people would otherwise ship.
- A "free" option with high operational load is rarely free; say what it
  actually costs.

## Reversibility as a Scored Dimension

Classify every option as a **one-way door** (expensive or impossible to
reverse: data migrations, public API contracts, vendor lock-in with data
gravity) or a **two-way door** (walk it back cheaply). Reversibility changes
how much analysis the decision deserves and how much risk the chosen option
can carry. State the reasoning — misclassifying a one-way door as reversible
is the costliest single error in this discipline.

## Fairness Tests

- **Do-nothing gets full-strength advocacy.** Status quo is a real option
  with real advantages (zero migration cost, known failure modes). If
  do-nothing is missing from the matrix, the analysis is a sales document.
- **The boring option gets a real defense** before scoring. If you cannot
  write a convincing paragraph for an option, you have not understood it well
  enough to reject it.
- Each option's *dominant risk* is named — the single most likely way it
  goes wrong.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Everyone already knows the answer" | Then the matrix is cheap to build and will confirm it. If it doesn't, you just avoided a bad call. |
| "Do-nothing isn't an option" | It is always an option. If it truly loses, the matrix will show it losing — fairly. |
| "We can tune the weights later" | Weights changed after scoring began are the signature of a rigged matrix. |
| "TCO is too hard to estimate" | A labeled rough range beats an omitted cost. Omission is an estimate of zero. |

## Red Flags

- A matrix with no do-nothing/status-quo row
- Weights that cannot be traced to a requirement
- Scores without justifications, or justifications without sources
- Every driver conveniently favoring the same option
- No sensitivity note — rankings presented as more decisive than they are
- Reversibility not classified, or all options called "reversible"

## Verification

Before handing the matrix on:

- [ ] Every driver traces to a requirement; weights stated before scoring
- [ ] Every option scored on every driver with a justification or labeled assumption
- [ ] Do-nothing present and fairly advocated
- [ ] Each option has TCO (build + run + opportunity), reversibility class, and dominant risk
- [ ] Sensitivity note states what would flip the ranking
- [ ] No recommendation — the matrix ranks; the decider chooses
