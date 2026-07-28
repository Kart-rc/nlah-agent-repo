# DDD pattern catalog: strategic and tactical

Optional deep-dive for `SKILL.md`. Read it when choosing a context-map
relationship, when deciding whether a concept is an entity or a value object,
or when sizing an aggregate. The discipline and the output contract are in
`SKILL.md`; nothing here overrides them.

## Strategic patterns

### Subdomain types

| Type | What it is | How much modelling it deserves |
|---|---|---|
| **Core** | The reason the business wins; the part a competitor cannot buy | Model it carefully. This is where the effort goes. |
| **Supporting** | Necessary, specific to this business, not differentiating | Keep it simple and explicit. Plain code beats patterns. |
| **Generic** | Solved everywhere: auth, notifications, payments plumbing, PDF | Buy, adopt, or copy. Hand-modelling it is the classic waste. |

Getting this wrong is expensive in both directions: an under-modelled core
becomes an unmaintainable pile of special cases; an over-modelled generic
subdomain burns the design budget on something a vendor sells.

### Context-map relationship types

Every arrow on the context map is one of these. Name it, and name who absorbs
change.

| Relationship | Shape | Choose it when | It costs |
|---|---|---|---|
| **Partnership** | Two contexts succeed or fail together; coordinated releases | Two teams genuinely cannot ship independently | Continuous coordination; the slowest team sets the pace |
| **Customer / supplier** | Downstream's needs enter the upstream's backlog | There is real organizational leverage downstream | Upstream planning overhead; needs an actual agreement |
| **Conformist** | Downstream adopts the upstream model as-is, no translation | The upstream is stable, sane, and not worth translating | Upstream's model shape leaks into yours forever |
| **Anticorruption layer (ACL)** | Downstream translates at the edge into its own model | The upstream model is legacy, external, or hostile to yours | Translation code and mapping maintenance |
| **Shared kernel** | Two contexts share a small explicit model subset | Duplication is genuinely worse than coupling, and both teams agree to the ceremony | Coupled release cycles; every change is a two-team change |
| **Open host service / published language** | Upstream publishes a stable protocol for many consumers | Many downstreams, and you do not want N bespoke integrations | Designing and versioning a real public contract |
| **Separate ways** | No integration at all; duplicate the small overlap | The overlap is small and integration costs more than duplication | Two implementations to keep roughly aligned |

Rules of thumb:

- Default to **ACL** at any boundary with a legacy or third-party system.
  It is the pattern that keeps a new model from silently becoming a wrapper
  over an old schema.
- **Conformist** is a legitimate, cheap choice — but only when you have
  genuinely accepted the upstream vocabulary in your own code and stopped
  pretending otherwise.
- **Shared kernel** should be rare and small, and should have a named owner.
  If nobody owns it, it is not a kernel, it is a shared mutable global.
- If you cannot name the relationship, the integration is undesigned.

### Big ball of mud

A legitimate map entry. Marking a region as an unstructured legacy area with
an ACL between it and the new model is honest design; pretending the region
has a clean model is not.

## Tactical patterns

### Entity vs value object

- **Entity** — identity persists through change. `Order`, `Customer`,
  `Shipment`. Two entities with identical attributes are still different
  things.
- **Value object** — defined entirely by its attributes; immutable and
  interchangeable. `Money`, `DateRange`, `Address`, `EmailAddress`,
  `PostalCode`.
- **Test:** if two instances with identical fields are interchangeable, it is
  a value object. Most domains have far more value objects than teams write —
  primitive obsession (`amount: float`, `currency: str`) is the usual symptom.

### Aggregate and aggregate root

- The **aggregate** is a cluster enforcing one or more invariants inside a
  single transaction. The **root** is the only entry point; nothing outside
  holds a reference to an internal member.
- Sizing rules:
  1. Start from the invariant, not the object graph or the foreign keys.
  2. Prefer the smallest cluster that can enforce it.
  3. One aggregate modified per transaction; reference others by id.
  4. If two users routinely edit different parts concurrently, split it.
  5. If a "rule" is only checked on read, it was never an invariant.
- **Test:** can you state, in one sentence, the rule that would break if this
  cluster were split? No sentence means no aggregate.

### Domain service

- Behaviour that belongs to the domain but to no single entity — a transfer
  between two accounts, a pricing calculation spanning several aggregates.
- **Test:** if the behaviour *could* sit on an entity or value object, put it
  there. A domain layer that is mostly services is an anaemic model with
  procedural code beside it.

### Repository

- One per aggregate root. Loads and persists whole aggregates. The collection
  illusion: `orders.add(order)`, `orders.byId(id)`.
- **Test:** a repository returning fragments, projections, or arbitrary query
  results is a DAO. Read models are the correct home for those queries.

### Factory

- Encapsulates construction when creating a valid aggregate is itself
  non-trivial (invariants must hold from birth).
- **Test:** if the constructor can enforce the invariants, no factory is
  needed. Factories that only forward arguments are noise.

### Domain event

- A recorded business fact, past tense, usually straight from the event
  storm's timeline: `PaymentCaptured`, `ShipmentDelayed`.
- Carries what happened and the ids involved; not the whole aggregate.
- **Test:** would the business care that it happened, and would a person name
  it that way? `OrderRowUpdated` fails both.

### Application layer

- Orchestration only: load the aggregate, invoke it, persist, publish events,
  handle transactions and authorization.
- **Test:** any `if` that encodes a business rule belongs in the model. This
  is the single most reliable smell for an anaemic domain.

### Read model / projection

- Query-side shapes built for a screen or report, derived from events or
  aggregates. Free to denormalize; never the source of truth.
- Event storming already surfaced these as the "what were they looking at?"
  element — reuse those findings instead of inventing new screens.

## Brownfield sequencing

Applying this to an existing system, in order:

1. Draw the context map of **what exists today**, including the mud, with
   honest relationship names.
2. Pick **one** context to model properly — normally the core subdomain the
   current change touches.
3. Put an **ACL** between it and everything legacy it must talk to.
4. Move the invariants into aggregates **inside that context only**; leave the
   rest alone.
5. Record what was left as **accepted debt with a stated cost**, not as a
   silent gap.

A design that only becomes true after a rewrite is a rewrite proposal. If the
model requires one, say that explicitly and let it be decided as a decision,
not smuggled in as a design.
