---
name: architectural-judgement
description: Heuristics for judging architectures rather than designing them. Use when assessing a design doc, RFC, or system against requirements, when arbitrating between competing designs, or when a verdict (approve/reject) must be defended.
---

# Architectural Judgement

## Overview

Designing an architecture and judging one are different skills. The judge's
questions are not "how would I build this?" but "will this survive contact
with production, operations, and three years of change — and is its
complexity paying rent?" This skill collects the heuristics that make an
architectural verdict defensible.

## When to Use

- Reviewing a design doc, RFC, or existing system for a verdict
- Arbitrating between teams' competing designs
- Deciding whether a proposed pattern becomes a platform standard
- Writing the conditions attached to an approval

**When NOT to use:** Producing the design yourself (that is design work, not
judgment — and judging your own design is the conflict the harness exists to
prevent).

## Reversibility Is the First Question

Before evaluating quality, ask: **if this is wrong, what does it cost to
change?**

- One-way doors in architecture: data models and their migrations, public
  API contracts, choice of persistence semantics, multi-tenant boundaries,
  anything that accumulates data gravity.
- A mediocre-but-reversible design can ship and be corrected; an elegant
  one-way door deserves the full weight of scrutiny.
- Judge whether the design *knows* which of its own decisions are one-way,
  and isolates them. A design that treats everything as equally permanent —
  or equally revisable — has not thought about time.

## Boring Technology Bias

Innovation is a budget, not a virtue.

- Each novel technology in a design spends an innovation token: unknown
  failure modes, thin operational experience, hiring and on-call load.
  A design spending three tokens at once is usually spending someone else's.
- The burden of proof sits on the novel choice: what requirement does the
  boring, known option actually fail? "It's outdated" is not a failure;
  a named requirement it cannot meet is.
- Respect existing paved roads: a design that departs from the
  organization's operational patterns needs a reason proportional to the
  departure.

## Total Cost Outranks Elegance

- Ask **who runs this at 3am**: on-call surface, failure diagnosis, upgrade
  path, capacity model. An architecture the owning team cannot operate is
  wrong for that team, however sound the diagram.
- Complexity must pay rent — every moving part (service, queue, cache,
  consistency domain) needs a requirement that demands it. Speculative
  generality ("we might need to scale to...") is the most common unpaid rent.
- Weigh migration cost from the current state, not just target-state beauty.
  The best architecture you cannot migrate to loses to the good one you can.

## Evolutionary Fitness

- Prefer designs that defer decisions to the **last responsible moment** —
  interfaces now, implementations when forced — over big-design-up-front
  that pre-decides what cheaper information would decide later.
- Look for **fitness functions**: measurable properties (p99 latency, cost
  per request, coupling limits, error budgets) that will tell the team the
  architecture is degrading before users do. A design with no measurable
  health signals cannot be held to its own promises.
- Ask what the *second* version looks like: which parts are expected to be
  replaced, and does the structure permit it?

## Verdict Discipline

A review that ends without a verdict is a book club.

- Exactly one of: **approve / approve-with-conditions / reject** — stated
  first, justified in a paragraph.
- **Conditions must be decidable**: what must change, how it will be
  verified, by when. "Consider improving observability" is not a condition;
  "add per-tenant request metrics before GA, verified in the dashboard
  review" is.
- **A vague condition is a hidden reject** — it withholds approval while
  pretending not to. If you would not approve once the named conditions are
  met, the verdict is reject; say so.
- Every finding cites evidence in the artifact under review (section, file,
  diagram). Findings from general principle without a location in the
  subject are opinions, and belong in a different document.
- Severity-rank findings (blocker / major / minor), and let the blockers
  determine the verdict — a review where nits and blockers carry equal
  weight teaches authors to ignore all of it.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The team is excited about this stack" | Enthusiasm is real but depreciates; the pager schedule does not. Count the tokens. |
| "Rejecting will demoralize them" | A hidden reject via vague conditions demoralizes slower and costs more. Clear verdicts respect the work. |
| "It works at Google" | It works at Google's scale, with Google's platform teams. Judge it at this org's scale and staffing. |
| "We can always fix it later" | Only if it is a two-way door. That is why reversibility is the first question. |

## Red Flags

- A design that cannot name its own one-way doors
- Multiple novel technologies with no named requirement forcing any of them
- No operational story: unclear ownership, no failure modes, no health metrics
- Conditions that no one could verify, attached to an "approval"
- Findings citing principles but no location in the subject
- A verdict that hedges ("approve, but with reservations about the whole approach")

## Verification

- [ ] Reversibility of the design's key decisions classified first
- [ ] Novel-technology choices each justified against a boring alternative
- [ ] Operational cost assessed: who runs it, how failure is seen, upgrade path
- [ ] Fitness signals identified (or their absence flagged as a finding)
- [ ] Verdict is exactly one of approve / approve-with-conditions / reject
- [ ] Every condition decidable; every finding evidence-cited and severity-ranked
