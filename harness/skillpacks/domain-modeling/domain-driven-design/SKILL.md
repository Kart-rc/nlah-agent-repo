---
name: domain-driven-design
description: Models a change against the business domain rather than the technical layers - bounded contexts as language boundaries, a context map whose every integration names its relationship, a ubiquitous language carried into code, and aggregates whose invariants define transactional boundaries. Use when designing a change to non-trivial business behaviour, when component boundaries are being drawn or redrawn, or when the same word means different things in different parts of the system.
---

# Domain-Driven Design

## Overview

Designs drift toward the shape of the technology: a controller layer, a
service layer, a table per noun. That shape is easy to draw and expensive to
live in, because the business changes along seams the layers do not have.
Domain-driven design puts the seams where the *language* changes — one model
per bounded context, one meaning per term, one invariant per aggregate — and
then makes every boundary an argued decision rather than an accident of who
wrote the code first.

## When to Use

- Designing a change to business behaviour with real rules: eligibility,
  pricing, settlement, entitlement, approval, scheduling
- Component or service boundaries are being drawn, redrawn, or defended
- The same word means different things in different parts of the system, or
  an event storm surfaced conflicting vocabulary
- A model is being extracted from, or grafted onto, a legacy system

**When NOT to use:** Discovering the domain in the first place is
`domain-modeling/event-storming` at `intake`. Designing the *contract* of a
module or API — versioning, compatibility, error shape — is
`addyosmani/api-and-interface-design`; this skill decides what the contract is
*about*. Containment, blast radius, and rollback are
`distinguished-engineer/failure-domain-thinking`. And skip it entirely when
there is no domain: CRUD screens, config plumbing, reporting pass-throughs,
and build changes get worse when modelled, not better.

## Language Before Structure

The model's nouns are the business's nouns, or the model is fiction.

- Take the vocabulary **from the event storm or the stakeholders**, not from
  the existing schema. If `intake` produced an `event-storm.md`, its glossary
  is the starting language; any rename must be **justified in the design**,
  not performed silently.
- The chosen terms are the **names used in code** — types, functions,
  modules, events. A ubiquitous language that stops at the design doc is a
  glossary, and glossaries do not survive contact with a sprint.
- Where the storm recorded a **conflict** (two groups, one word, two
  meanings), do not merge it. Resolving it by picking a winner destroys the
  signal; resolving it by *drawing a boundary* is usually the right answer.
- Ban the **anaemic vocabulary**: `Manager`, `Handler`, `Processor`, `Data`,
  `Info`, `Helper`. A name nobody in the business would say marks a concept
  nobody in the business owns.

## Bounded Contexts Are Language Boundaries

A context is the region where one term has exactly one meaning.

- Draw the boundary where the **meaning changes**, not where the org chart
  or the deployment topology changes. *Customer* in billing (a payer with a
  balance) and *customer* in support (a person with a history) are two models,
  and forcing them into one produces a class with thirty nullable fields.
- Classify each area as **core, supporting, or generic** and spend
  accordingly: model the core carefully, keep the supporting simple, buy or
  copy the generic. Lovingly hand-modelling a generic subdomain — auth,
  notifications, PDF generation — is the most common way this skill is wasted.
- A bounded context is a **model boundary, not necessarily a deployment
  boundary**. Two contexts in one process is a normal, cheap, correct answer;
  a service per context is a decision with an operations bill attached.
- **Prefer fewer contexts than the storm suggests.** Splitting later is
  refactoring; merging later is a migration.

## The Context Map Is a Decision, Not a Diagram

Every arrow between contexts is a relationship someone has to maintain.

- Name the **relationship type** on every integration — partnership,
  customer/supplier, conformist, anticorruption layer, shared kernel, open
  host service / published language, separate ways. See
  `references/pattern-catalog.md` for when each is appropriate. An unnamed
  arrow is an undecided relationship, and it will be decided by whoever is on
  call.
- State the **direction of dependency and who absorbs change**. "Both teams
  coordinate" is a partnership and costs meetings; "we accept their model" is
  conformist and costs autonomy; "we translate at the edge" is an
  anticorruption layer and costs code. Pick one, price it.
- Put an **anticorruption layer** wherever an external or legacy model would
  otherwise leak in. This is the single highest-value pattern in brownfield
  work: it is what keeps the new model from becoming a thin wrapper over the
  old schema.
- **Shared kernel is a liability**, not a shortcut: it couples two contexts'
  release cycles. Justify it explicitly or use a published language instead.

## Aggregates Are Consistency Boundaries

Start from the rule that must never be violated, not from the object graph.

- For each invariant, ask **what must be true at every commit**, and make the
  aggregate the *smallest* thing that can enforce it in one transaction.
  "Order total equals the sum of its lines" is an aggregate boundary;
  "orders belong to customers" is a reference.
- **One aggregate per transaction.** Reference other aggregates **by id**, not
  by object, and accept eventual consistency between them — then say
  explicitly *where* the system is eventually consistent and what a user might
  observe in the gap.
- Keep aggregates **small**. A large aggregate is a contention hotspot with a
  domain-sounding name; if two users routinely edit different parts of it,
  it is two aggregates.
- Every command lands on **exactly one aggregate**, which either accepts it
  and records the resulting domain event or rejects it with a domain reason.
  Rules enforced in the application layer are rules that can be bypassed.

## Tactical Patterns Earn Their Place

Each pattern has a test. Failing the test means do not use it.

- **Entity vs value object** — does identity persist through change? An
  `Order` is an entity; a `Money` or `DateRange` is a value object. Test: if
  two instances with identical fields are interchangeable, it is a value.
- **Domain service** — behaviour that genuinely belongs to no single entity
  (a transfer between two accounts). Test: if it *could* live on an entity, it
  should. Domain services are where anaemic models go to hide.
- **Repository** — one per aggregate root, returning whole aggregates. Test:
  a repository that returns fragments or accepts arbitrary queries is a DAO
  with better branding.
- **Domain event** — a recorded business fact, past tense, from the storm's
  timeline. Test: would the business care that it happened? A field-change
  notification is not a domain event.
- **Application layer** — orchestrates: load aggregate, call it, persist,
  publish. Test: any business rule found here belongs in the model.

## Grounded in This Codebase

The `design` stage requires real file and module references; so does the model.

- Map each bounded context onto the **real modules and directories** it
  corresponds to today, and name the ones that do not exist yet.
- Say honestly where the **existing code contradicts the model** — a shared
  table, a god object, a leaked schema — and choose per case: anticorruption
  layer now, refactor now, or accepted debt with the cost stated. Silence
  here is what turns a design into a fiction the implement stage cannot
  follow.
- **Do not describe a greenfield system.** A model that only works after a
  rewrite is a rewrite proposal, and it should say so out loud.
- Prefer the **smallest useful model**: the contexts and aggregates this
  change actually touches. Modelling the whole business at design time is how
  a two-week change becomes a quarter.

## Output: fold into `design.md`

The `design` stage fixes `design.md`'s top-level sections and their order.
**Do not add or reorder top-level sections.** Place the model as subsections:

- Under `## Architecture`: `### Ubiquitous language` (term → meaning → the
  code name it maps to), `### Bounded contexts and context map` (each context,
  its subdomain type, the real modules it maps onto, and every integration
  with its named relationship), `### Aggregates and invariants` (each
  aggregate, the invariant it protects, its transactional boundary, and the
  aggregates it references by id).
- Under `## Key decisions`: every boundary choice — where a context line was
  drawn, why a relationship type was chosen, why an aggregate was split or
  merged — each with its `Rejected alternative(s):` and a concrete reason.
- Mirror those decisions into `decisions.json` like any other key decision.
- Eventual-consistency gaps and the failure behaviour of cross-context
  integrations belong under `## Failure modes and rollback`.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "One shared Customer model is simpler" | Simpler to draw. It becomes the class every team must change and no team owns. |
| "We'll extract the bounded contexts later" | Later means after every module imports the shared model. Boundaries are cheap only before code. |
| "A context per service is cleaner" | Contexts are model boundaries. Turning each into a service buys network calls you have no requirement for. |
| "The aggregate needs to load the whole graph" | Then the transaction does too. That is not a model, it is a lock. |
| "Everything is eventually consistent anyway" | Only where you said so, with the observable gap described. Unstated eventual consistency is a bug backlog. |
| "The domain experts approved the diagram" | They approved boxes. Ask them to read the ubiquitous language table out loud instead. |

## Red Flags

- Contexts drawn along the org chart, the deployment topology, or the layers
- An integration arrow with no named relationship type
- One model shared by two contexts "to avoid duplication"
- Aggregates defined by object graph or database foreign keys rather than by
  an invariant
- A transaction spanning two aggregates, or an aggregate loaded to enforce a
  rule that lives elsewhere
- Business rules in the application layer or in controllers
- A ubiquitous language table whose terms appear nowhere in the proposed code
- A design that requires a rewrite before any of it is true

## Verification

- [ ] Every term in the ubiquitous language maps to a name used in the design
- [ ] Terms renamed from the intake event storm are justified in the design
- [ ] Each bounded context states its subdomain type (core/supporting/generic)
- [ ] Each context maps onto real modules/directories, or is named as new
- [ ] Every cross-context integration names its relationship type and who
      absorbs change
- [ ] Each aggregate is defined by the invariant it protects, and references
      other aggregates by id
- [ ] Every eventual-consistency gap is stated with what a user may observe
- [ ] Each boundary decision appears in `## Key decisions` with a rejected
      alternative, and in `decisions.json`
- [ ] Contradictions with the existing codebase are named and dispositioned
- [ ] No top-level section was added to or reordered in `design.md`
