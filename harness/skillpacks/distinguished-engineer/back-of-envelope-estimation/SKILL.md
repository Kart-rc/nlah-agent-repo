---
name: back-of-envelope-estimation
description: Sanity-checks designs and claims with order-of-magnitude arithmetic before anything is built. Use when a design implies a latency, throughput, storage, or cost profile nobody has computed, when options differ mainly by a number, or when a claim like "it won't scale" or "it'll be cheap" deserves a ten-minute check.
---

# Back-of-Envelope Estimation

## Overview

Every design implies numbers — requests per second, bytes per record,
dollars per month — whether or not anyone has computed them. The systems
that fail in production usually violated arithmetic that ten minutes with
an envelope would have caught. This skill is the discipline of estimating
before building, and of turning design arguments into sums.

## When to Use

- A design implies a latency, throughput, storage, or cost profile that
  nobody has written down
- Options in a decision differ mainly by a number (cost, capacity, time)
- A claim like "that won't scale", "it'll be cheap", or "the cache will
  save us" is steering a decision unquantified
- Capacity planning, quota requests, or "can we afford this?" questions

**When NOT to use:** When the real number is cheaply measurable — an
estimate is a substitute for a measurement you cannot yet take, not for
one you are avoiding. And when precision genuinely matters (billing,
SLAs), the envelope only brackets the answer; it does not sign contracts.

## Carry Your Numbers

Estimation runs on a small table of anchors you maintain like a tool.

- Keep calibrated anchors for your domain: rough costs of a disk seek, an
  SSD read, a same-region round trip, a cross-region round trip; rough
  throughput of a modern core, a database node, a queue partition; rough
  price of a GB stored, a GB transferred, a vCPU-month.
- Anchors decay — hardware, pricing, and platforms move. Re-derive yours
  when you touch a new stack; an estimate from 2015 anchors is confidently
  wrong.
- Know your **workload constants**: current QPS, record sizes, growth
  rate, peak-to-average ratio. Estimators who know their own system's
  numbers are the ones whose envelopes get trusted.

## The Fermi Discipline

The method is decomposition, not clairvoyance.

- **Decompose** the quantity into factors you can anchor: users × actions
  per user × bytes per action. Multiply. The skill is choosing a
  decomposition whose factors you actually know.
- Work in **powers of ten**; suppress precision. "About 10^5 QPS" is a
  usable answer; "87,300 QPS" from guessed inputs is fiction with
  four significant figures.
- **Bound it from both sides**: an optimistic and a pessimistic pass. If
  the design only works in the optimistic half, that is a finding.
- Write every **assumption down** as you go. An estimate whose assumptions
  are invisible cannot be checked, updated, or fairly attacked.

## Estimate Before You Argue

Numbers end arguments that adjectives sustain.

- When a design review stalls on "too slow" versus "fast enough", stop the
  debate and do the arithmetic together. Ten minutes of multiplication
  regularly settles what an hour of opinion cannot.
- Find the **dominating assumption** — the one factor that moves the
  answer by an order of magnitude. That is where measurement or a spike
  should go next; refining the other factors is decoration.
- Check claims against **physical and platform limits**: line rate, disk
  bandwidth, partition throughput, rate limits. A design that needs a
  component to exceed its documented ceiling is not aggressive; it is
  wrong.
- An estimate that survives is a **prediction** — when the real number
  arrives, compare. Being wrong by 10x is how anchors get recalibrated;
  never comparing is how they stay wrong.

## Show the Envelope

An estimate kept private is an opinion; published, it is a review artifact.

- Put the arithmetic **in the design doc** — factors, anchors, assumptions,
  result — where reviewers can attack the weakest factor rather than the
  conclusion.
- State the **so-what**: "at ~10^5 QPS, one partition saturates; we need
  the keyed design" ties the number to the decision it drives. A number
  without a consequence is trivia.
- Label it an estimate and give its confidence. The reader must be able to
  tell an envelope from a benchmark at a glance.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "We'll load-test it later" | Load tests validate a built system. The envelope is how you avoid building the wrong one. |
| "It's cloud — it scales" | It scales at a price, to a quota, until a partition gets hot. The envelope finds which of those bites first. |
| "I don't have exact inputs" | Estimation exists precisely because you don't. Bound it; a factor-of-ten answer beats a shrug. |
| "The estimate might be embarrassingly wrong" | An estimate wrong in review costs ten minutes. The same error found in production costs the quarter. |

## Red Flags

- A design doc with architecture diagrams and not a single number
- Capacity claims with adjectives ("huge scale", "minimal cost") where
  factors should be
- Precision theater: four significant figures built on guessed inputs
- An estimate nobody can check because its assumptions were never written
- A component required to exceed its documented limits for the design to work
- Estimates that are never compared against reality once it arrives

## Verification

- [ ] The quantity decomposed into factors, each traceable to an anchor or a stated assumption
- [ ] Powers-of-ten arithmetic; no unearned precision
- [ ] Optimistic and pessimistic bounds both computed
- [ ] Dominating assumption identified and flagged for measurement or spike
- [ ] Result checked against physical/platform ceilings
- [ ] Envelope published in the artifact with its so-what stated
- [ ] Prediction recorded so reality can recalibrate the anchors
