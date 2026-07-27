---
name: event-storming
description: Discovers a business domain as a timeline of past-tense domain events with the commands, actors, policies, external systems, and read models around them, and records the hotspots where nobody agrees. Use when a change touches business behaviour whose rules, vocabulary, or process order are written down nowhere, when stakeholders describe the same process with different words, or before requirements are frozen on a domain nobody has mapped.
---

# Event Storming

## Overview

Requirements written from a request describe the system someone imagines.
Event storming describes the business that already exists: what actually
happens, in what order, caused by whom, and where the people who run it
disagree. It works because a past-tense event is the one thing domain experts,
analysts, and engineers can all point at without translating. The output is
not a diagram — it is a timeline plus an honest list of what nobody could
answer.

## When to Use

- A change touches business behaviour whose rules live in people's heads,
  scattered tickets, or one very old stored procedure
- Two stakeholders describe the same process using different words, or the
  same word for different things
- The process order itself is contested ("does approval happen before or
  after reservation?")
- Before requirements are frozen on a domain that has never been mapped

**When NOT to use:** Extracting one person's intent for a well-understood
request is `addyosmani/interview-me` — that clarifies what the requester
wants; this maps what the business does. Turning the map into contexts and
aggregates is `domain-modeling/domain-driven-design` at the `design` stage.
Skip it entirely for changes with no business behaviour: a build fix, a
dependency bump, a rename, a config change.

## Events First, in the Past Tense

The timeline is the artifact; everything else hangs off it.

- Write every event as **something that already happened**, in the domain's
  words: `OrderPlaced`, `PaymentCaptured`, `ShipmentDelayed`. Not
  `PlaceOrder` (that is a command), not `OrderService` (that is a component),
  not `OrderStatusUpdated` (that is a database row learning to talk).
- Put them in **rough business order and refine by argument**. Disagreement
  about order is a finding, not noise — it usually means two teams are
  running two different processes and have never noticed.
- Include the **unhappy paths**: cancelled, rejected, expired, refunded,
  reversed. A timeline with only the happy path describes a demo, not a
  business.
- Prefer **too many events, then merge**. Splitting later is cheap;
  discovering a missing event after the design is not.

## The Grammar Around Each Event

An event alone is a claim. The grammar is what makes it checkable.

- **Command + actor**: what request caused it, and who or what issued that
  request — a person in a role, a scheduled job, an inbound integration. An
  event with no cause is a gap: either the command is missing or the event is
  really a policy's output.
- **Policy**: the "whenever *this* happened, then *that* must follow" rule
  that fires automatically. Policies are where the business logic actually
  lives, and where it is most often undocumented.
- **External system**: the third party or upstream system that participates.
  Anything outside the org's control changes the failure conversation later.
- **Read model**: what the actor was looking at when they decided. "They
  approve it from the queue screen" tells you a query exists that nobody
  listed as a requirement.

## Hotspots Are the Deliverable

The value is concentrated in what could not be resolved.

- Record a **hotspot** wherever you hit a disagreement, an unknown rule, an
  "it depends", or a step everyone describes differently. Mark what is
  disputed and who would know.
- **Never resolve a hotspot by choosing.** Guessing here is how an assumption
  gets laundered into a requirement. This is also the `intake` stage's own
  rule: ambiguity is surfaced, not silently settled.
- Every hotspot must **leave the storm**: it becomes an open question in the
  requirements, or an explicit assumption with its owner named. A hotspot
  that dies inside `event-storm.md` was never really found.
- Note **frequency and pain** where you can ("happens ~200×/day, two people
  manually fix it"). Un-sized hotspots all look equally urgent, so none are.

## Ubiquitous Language Starts Here

Vocabulary discovered now is vocabulary the code can keep.

- Record terms **in the stakeholder's own words**, with who says it. Do not
  tidy `booking` into `reservation` because it reads better.
- When two groups use **different words for the same thing, or the same word
  for different things**, that is a hotspot and very often a context
  boundary — record both usages side by side and let `design` decide.
- Reject **system nouns** in the glossary: `record`, `entry`, `flag`,
  `payload`, `job`. If the business would not say it out loud, it is
  implementation vocabulary wearing a domain hat.

## Stay in the Problem Space

At `intake`, solution content is scope drift (failure class F4).

- You may record **candidate seams**: pivotal events, points where the
  language visibly changes, handoffs between different groups of actors.
  Record them as *observations with the open question they raise*.
- You may **not** name bounded contexts, aggregates, services, tables,
  queues, APIs, or technologies — even as "obvious". The boundary decision
  belongs to `design`, where it must carry a rejected alternative.
- If the storm makes a design conclusion feel inevitable, write it as a
  candidate seam with the evidence that suggests it. Inevitable conclusions
  are exactly the ones that deserve to be argued at the next stage.

## Running It Solo or Async

Most harness runs have no room full of stakeholders. Run it anyway, and be
honest about the sourcing.

- Derive a **provisional timeline from evidence**: the codebase's state
  transitions, notification templates, audit-log entries, scheduled jobs,
  ticket and incident history, support macros.
- Mark every provisional event with **where it came from**; unsourced events
  are hotspots until someone confirms them.
- Take the **contradictions as hotspots** rather than reconciling them — the
  code and the runbook disagreeing is a real finding about the business.
- Consult `references/notation-and-formats.md` when you need the sticky-note
  colour grammar, the big-picture / process / design-level session split, or
  facilitation timeboxes for a live session.

## Output: `event-storm.md`

Write it alongside the stage's required artifact, never instead of it. Use
these sections:

- `# Event storm`
- `## Timeline` — ordered past-tense events; per event: command, actor,
  policy, external system, read model, and source if provisional
- `## Hotspots` — what is disputed or unknown, who would know, frequency/pain
  if known, and where it went in the requirements
- `## Ubiquitous language` — term → definition → who says it → conflicting
  usage if any
- `## Candidate seams (observations only)` — pivotal events and language
  shifts, each with the open question it raises

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The ticket already describes the process" | It describes the step someone noticed. The timeline is where the other eleven steps live. |
| "We know this domain well" | Then the storm takes an hour and produces no hotspots. That result is worth an hour. |
| "That edge case is rare" | Rare cases are where the undocumented rules are, and where the manual workarounds hide. |
| "Both teams basically mean the same thing" | "Basically" is the sound of a bounded-context boundary being paved over. |
| "It's obvious this splits into two services" | Then it will survive being argued at `design` with a rejected alternative. Say it as a seam, not a decision. |

## Red Flags

- Events named as commands, CRUD verbs, or component names
- A timeline with no cancellation, rejection, expiry, or reversal
- Events with no command or actor attached
- Zero hotspots on a domain nobody had mapped before
- Hotspots resolved inside the storm instead of leaving as open questions
- A glossary of system nouns rather than business terms
- Bounded contexts, services, tables, or technologies named anywhere

## Verification

- [ ] Every timeline entry is past tense and in the domain's vocabulary
- [ ] Every event names its command and actor, or is marked as a gap
- [ ] Policies ("whenever … then …") are recorded, not folded into events
- [ ] Unhappy paths appear on the timeline
- [ ] Every hotspot names what is disputed and who would know
- [ ] Every hotspot leaves as an open question or a named assumption
- [ ] Glossary terms are stakeholder words, with conflicts recorded as conflicts
- [ ] Candidate seams are phrased as observations plus open questions
- [ ] No bounded context, aggregate, component, or technology is named
