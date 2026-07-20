---
name: failure-domain-thinking
description: Designs and reviews systems by their failure domains - blast radius, degradation, backpressure, and recovery. Use when designing anything that takes production traffic, when reviewing a design's failure modes and rollback story, or when extracting systemic lessons from an incident rather than patching the instance.
---

# Failure Domain Thinking

## Overview

Every system is drawn healthy: boxes up, arrows flowing, caches warm. But
systems spend their interesting hours partially broken, and the
architecture decides whether partial failure stays partial. This skill is
the discipline of designing containment in — asking not "will it fail?"
but "what does one failure reach, and what does the user see while it
burns?"

## When to Use

- Designing any system or change that takes production traffic
- Reviewing a design's failure modes, rollback story, or operational
  readiness
- Turning an incident into systemic lessons rather than a patched instance
- Deciding isolation boundaries: cells, shards, tenancy, regions

**When NOT to use:** Choosing metrics, logs, and alerts is
`addyosmani/observability-and-instrumentation` — observability sees
failure; this skill contains it. Cataloguing project risks with owners and
triggers is `tech-director/risk-mitigation` — a register records what
might happen; this skill changes what *can* happen.

## Blast Radius First

The first design question is not throughput; it is reach.

- For each component, ask: **what is the largest thing one bad deploy, one
  poison message, or one corrupted config can take down?** That reach is
  the failure domain, and it is a design choice, not a discovery.
- Partition by **bulkheads**: cells, shards, per-tenant pools, regional
  independence. The unit of isolation should match the unit you are
  willing to lose — if losing one cell is survivable, make sure a cell is
  actually a wall, not a chalk outline.
- Hunt **shared fate**: the config service, the auth dependency, the DNS
  zone, the one library everyone links. Every shared dependency merges
  failure domains that the diagram shows as separate.
- Stage rollouts so the blast radius of a change starts smaller than one
  domain: canary, one cell, many, all. A global deploy is a global
  experiment.

## Degrade, Don't Die

Between "fully up" and "down" there is a ladder, and it must be built.

- Design the **brownout ladder** explicitly: which features shed first,
  what gets served stale, what gets queued, what finally gets refused —
  each rung decided at design time, not improvised at 3am.
- Distinguish **critical from optional** on every path: the checkout must
  survive the recommendation engine's death. If the dependency graph
  doesn't encode this, every dependency is critical by default.
- Serving **stale beats serving nothing** for most reads; a cached answer
  with a timestamp is a feature, not a bug, during a dependency outage.
- Degraded modes that are never exercised do not exist. If the fallback
  path last ran in a design doc, the ladder has one rung: down.

## Backpressure and Idempotency

Overload turns into outage when demand has nowhere to go but in.

- Every queue and buffer needs a **bound and a policy** for when it fills:
  shed, spill, or slow the producer. An unbounded queue is a promise to
  fall over later, with interest.
- Set **timeout and retry budgets** end-to-end, not per-hop: retries
  multiply load exactly when the system can least afford it. A retry storm
  is self-inflicted DDoS with good intentions.
- Make operations **idempotent** wherever a retry can reach; idempotency
  is the license retries require. Exactly-once is a costly fiction —
  at-least-once plus idempotent handlers is the honest contract.
- Shed load **early and cheaply**: rejecting at the front door costs a
  connection; rejecting after the database call costs the database.

## Learning from Incidents

An incident is a paid-for probe of the real failure domains.

- Chase **contributing factors, not a single root cause**: real incidents
  are conjunctions — the bug *and* the alert gap *and* the runbook drift.
  A single-cause story is a comforting fiction that fixes one leg of a
  four-legged failure.
- Fix the **class, not the instance**: after the bad config took down a
  cell, the question is what other configs can do that, and what makes
  the whole class impossible or survivable.
- Compare the incident against the design's assumptions: which imagined
  wall did the failure walk through? That gap — designed containment
  versus actual reach — is the highest-value finding.
- Feed lessons back into the ladder, the budgets, and the bulkheads. An
  incident review whose actions are all "be more careful" has extracted
  nothing.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "That failure is extremely unlikely" | Unlikely × enough traffic × enough time = scheduled. Design for its reach, not its odds. |
| "Retries will handle transient errors" | Unbudgeted retries turn a transient error into a load spike wearing a bandage. |
| "We have great monitoring" | Monitoring watches the fire. Bulkheads decide how big it can get. They are different investments. |
| "The fallback is implemented, we're covered" | Unexercised fallbacks fail on first use with high reliability. Covered means drilled. |
| "The postmortem found the root cause" | Singular. That's how you know it stopped early. |

## Red Flags

- A design doc with no failure-modes section, or one written after the
  design was done
- Any component whose failure reaches every user
- Unbounded queues, per-hop timeouts that sum past the caller's, retries
  without budgets
- Fallback paths never exercised in production conditions
- Critical user journeys with hard dependencies on optional features
- Incident actions that are all vigilance ("add review", "be careful") and
  no structure

## Verification

- [ ] Failure domain of each component stated: what one failure can reach
- [ ] Shared-fate dependencies enumerated; each justified or walled off
- [ ] Brownout ladder explicit: shed order, stale policy, refusal point
- [ ] Critical vs optional distinguished on every user-facing path
- [ ] Every queue bounded with a stated overflow policy
- [ ] Timeout/retry budgets set end-to-end; retried operations idempotent
- [ ] Rollback and fallback paths exercised, not merely designed
- [ ] Incident learnings (where applicable) fix the class and update the design's assumptions
