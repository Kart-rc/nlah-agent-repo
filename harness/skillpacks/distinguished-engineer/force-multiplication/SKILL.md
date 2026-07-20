---
name: force-multiplication
description: Scales one engineer's judgment across an organization through artifacts and paved paths rather than meetings and mandates. Use when the same guidance is being repeated one-to-one, when a standard needs adoption without authority to mandate it, when reviews should teach beyond the diff at hand, or when delegating a problem someone will grow by owning.
---

# Force Multiplication

## Overview

A distinguished engineer's ceiling is not what they can build; it is what
the organization builds differently because they exist. The failure mode is
the hero bottleneck: the expert whose judgment is excellent and whose
calendar is the org's critical path. This skill is the discipline of
scaling judgment through things — paved paths, exemplar artifacts,
teaching reviews, delegated problems — instead of through presence.

## When to Use

- You are repeating the same guidance one-to-one for the third time
- A standard or practice needs adoption across teams you cannot mandate
- Reviews are correcting the same class of issue diff after diff
- Delegating work that someone will grow by owning
- Your review queue or meeting load is the org's bottleneck

**When NOT to use:** Management practice — delegation levels, feedback
conversations, team-health signals — is
`tech-director/people-leadership`. Building a coalition for one specific
proposal is `tech-director/influence-without-authority`; this skill builds
the artifacts that make the next ten proposals unnecessary.

## Paved Paths Over Mandates

Make the right way the easy way, and enforcement becomes unnecessary.

- A **paved path** is a default that works: the template repo, the
  scaffolded service, the blessed pipeline — where the secure, observable,
  compliant choice is also the one that takes an afternoon. Adoption
  follows gradient, not decree.
- Keep the **escape hatch open but priced**: teams may leave the path if
  they own the difference — their security review, their upgrade burden.
  Sealed paths breed resentment and shadow infrastructure; priced exits
  keep the path honest and the mavericks accountable.
- **Measure adoption, don't decree it.** A standard nobody follows is
  feedback, not disobedience: the path is too steep, the escape too
  cheap, or the standard wrong. Instrument usage and treat abandonment as
  a bug report on the path.
- Maintain the path like a product: deprecation policy, upgrade autoroll,
  a changelog. A paved path that rots becomes the cautionary tale the
  next mandate-lover cites.

## Exemplar Artifacts

One excellent worked example outteaches ten guideline documents.

- Build the **reference implementation**: a real, running, boring-in-the-
  best-way service or module that embodies the standard. Engineers copy
  working code, not bullet points — make the thing they copy excellent.
- Write **guides as worked examples**: start from a real problem, show
  the decisions and their reasons, arrive at the pattern. Principles
  stated without a worked instance evaporate on contact with a deadline.
- **Curate the exemplars**: mark them, keep them current, and retire them
  when the pattern moves on. An outdated exemplar teaches the old way
  with your endorsement attached.
- Put judgment into **checkable form** where possible: the lint rule, the
  scaffold, the CI check that encodes the decision. A rule that runs
  scales infinitely further than a rule that must be remembered.

## Reviews That Teach

A review comment read once fixes a diff; written well, it trains a cohort.

- Write for the **hundredth reader**: state the principle, then its
  application — "we isolate retries behind idempotency keys (principle);
  this handler can double-charge (instance)." The author learns the rule,
  not just the correction.
- **Distinguish blocking from teaching**: severity-mark comments so
  authors know what must change versus what is offered. Reviews where
  nits and blockers look identical teach authors to discount all of it.
- When the same comment recurs across authors, **the artifact is the
  fix**: promote it to a lint rule, a template default, or a guide
  section — then stop writing it by hand. Recurring manual comments are
  a scaling bug filed against you.
- Review the **decision, not the diff**, when the stakes warrant:
  fifteen minutes at design time replaces fifty comments at review time.
  Move your leverage upstream of the code.

## Delegate Problems, Not Tasks

Handing someone your solution rents their hands; handing them the problem
grows an owner.

- Delegate the **problem statement, constraints, and context** — not the
  decomposed task list. The task list keeps you the architect of record
  and the permanent bottleneck; the problem transfers judgment.
- **Let the solve be theirs**, including the parts you would do
  differently. Overriding a workable approach because it is not your
  approach converts an owner back into a hands-for-hire — at the price
  of every future delegation.
- Stay available as a **consultant, not a checkpoint**: they pull advice
  when needed; you do not gate their progress. Name the genuinely
  irreversible decisions where you *do* want a say, and make that list
  short and explicit.
- Success is **succession**: the discipline pays off when the next
  problem in that area goes to them directly — and your absence from the
  loop is unremarkable. A bus factor of one, where you are the one, is a
  failure you built.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "It's faster to just do it myself" | Faster this once. The tenth time, you are the bottleneck and nobody else has learned - slowest of all. |
| "We need a mandate or nobody will comply" | Mandates without paved paths produce compliance theater. A path that saves an afternoon produces adoption. |
| "People should read the guidelines doc" | Nobody copies a doc under deadline; they copy the nearest working example. Make the nearest example excellent. |
| "I have to review everything to keep the bar" | A bar held by one calendar is a bar the org loses on your vacation. Encode it - in exemplars, rules, and people. |
| "They'll do it wrong without my task list" | Maybe, once - recoverable. With your task list they'll do it right and learn nothing - permanent. |

## Red Flags

- Your calendar or review queue is on the critical path of multiple teams
- The same guidance dispensed one-to-one, verbally, for the third time
- A "standard" existing only as a doc, with no template, scaffold, or check
- Escape hatches either sealed (shadow infra incoming) or free (path is a suggestion)
- Review comments recurring across authors with no artifact promoted from them
- Delegations that come back as "is this what you wanted?" at every step
- Areas of the system where your absence stops decisions entirely

## Verification

- [ ] Repeated guidance identified and promoted into an artifact: path, exemplar, rule, or guide
- [ ] Paved path exists as working, maintained scaffolding - not only prose
- [ ] Escape hatches open and explicitly priced; adoption measured, abandonment investigated
- [ ] Exemplars current, marked, and retired when the pattern moves
- [ ] Review comments state principle plus instance; severity distinguished
- [ ] Recurring review comments converted to checks or templates
- [ ] Delegations hand over problem, constraints, and context - solve stays with the owner
- [ ] Succession visible: the next problem in the area routes past you
