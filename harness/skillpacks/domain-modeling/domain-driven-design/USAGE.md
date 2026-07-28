# Using `domain-driven-design`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Makes a producer model the change against the business rather than the
technical layers: a ubiquitous language whose terms are the names used in
code, bounded contexts drawn where meaning changes and classified core /
supporting / generic, a context map where every integration names its
relationship and who absorbs change, and aggregates defined by the invariant
they protect with eventual-consistency gaps stated explicitly. Every boundary
choice lands in `## Key decisions` with a rejected alternative — and the model
is mapped onto the real modules that exist today, including where the current
code contradicts it.

## When to invoke

- Designing a change to business behaviour with real rules — eligibility,
  pricing, settlement, entitlement, approval, scheduling.
- Component or service boundaries are being drawn, redrawn, or defended.
- An `intake` event storm surfaced conflicting vocabulary, or the same word
  means different things in different parts of the system.
- A model is being extracted from, or grafted onto, a legacy system.
- See SKILL.md → When to Use / When NOT to use; discovering the domain is
  `domain-modeling/event-storming` at `intake`, contract shape and versioning
  is `addyosmani/api-and-interface-design`, and containment and rollback are
  `distinguished-engineer/failure-domain-thinking`.

**Default attachments:** `design` in `sdlc`, `sdlc-autonomous`, and
`sdlc-interactive`; also a `skill_refs` default on `stages/design`, so the
`workflow-composer` materializes it into new manifests that use that stage.

## How to invoke

### In a harness workflow

Attach to a stage in the workflow manifest (a one-line edit; use the
`workflow-composer` skill to add, swap, or remove it, then run
`python3 scripts/harness_lint.py`):

```yaml
stages:
  - id: design
    uses: stages/design
    inputs:
      run_dir: "workflow:run_dir"      # so the producer can read the intake event storm
    skills:
      - uses: skillpacks/domain-modeling/domain-driven-design
```

The orchestrator passes the skill path to the stage's producer subagent,
which reads it fully before starting (HARNESS.md §7.1).

**Bind `run_dir` when `event-storming` ran upstream.** A producer receives
only its stage's *declared, bound* inputs (HARNESS.md §7.1), and
`event-storm.md` is not a declared output of `stages/intake` — so without this
binding the model is built blind to the storm's timeline and glossary.
`stages/design` declares `run_dir` as an optional input for exactly this;
bind it from a `run_dir` workflow input (orchestrator-resolved at
initialization, never requested from the user — see `sdlc`'s `inputs`).

**Attach the paired `extra_check` too**, or the discipline stays advisory.
Append this clause to the stage's completeness-check `with.extra_check`,
keeping any string already there (the sdlc-family manifests already carry
context-register and EXPLAIN.md clauses):

```yaml
    validators:
      - uses: validators/completeness-check
        with:
          checklist: policies/gates/architecture.md
          extra_check: "when the change touches business behaviour, design.md's Architecture section states the ubiquitous language as a table whose every row carries the source term from the intake event storm or 'new', with a justification on any row where the two differ, the bounded context(s) the change touches with a named relationship for each cross-context integration, and each aggregate with the invariant it protects; when the change touches no business behaviour, design.md states that explicitly and no domain model is required."
```

Note the skill writes **no new artifact**: `stages/design` fixes `design.md`'s
top-level sections and their order, so the model goes in as subsections of
`## Architecture` and as entries in `## Key decisions` / `decisions.json`.

### Standalone (no harness run)

```text
Read harness/skillpacks/domain-modeling/domain-driven-design/SKILL.md fully,
then model <change> against <repository>. Produce the ubiquitous language, the
bounded contexts with their subdomain types mapped onto real modules, a context
map naming the relationship type on every integration, and the aggregates with
the invariant each protects. Record every boundary choice with a rejected
alternative, and name where the existing code contradicts the model.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and
what standalone mode does not guarantee.

## What to expect

- `### Ubiquitous language`, `### Bounded contexts and context map`, and
  `### Aggregates and invariants` inside `design.md`'s existing
  `## Architecture` section — no new or reordered top-level sections.
- A language table whose every row carries its source term from the event
  storm (or `new`), with a justification wherever the design renamed it — so
  a rename is reviewable from `design.md` alone.
- For a change with no business behaviour (build, dependency, config, pure
  rename): a one-sentence statement of that in `## Overview` and no domain
  model at all. That is a pass, not a gap.
- Every integration arrow carrying a named relationship (partnership,
  customer/supplier, conformist, anticorruption layer, shared kernel, open
  host / published language, separate ways) and who absorbs change.
- Aggregates justified by an invariant, referencing each other by id, with
  eventual-consistency gaps and what a user might observe in them.
- Boundary decisions in `## Key decisions` with rejected alternatives, mirrored
  into `decisions.json`.
- Honest disposition of where existing code contradicts the model:
  anticorruption layer, refactor now, or accepted debt with a stated cost.
- Misapplication signs (from Red Flags): contexts drawn along the org chart or
  the layers, an unnamed integration arrow, aggregates defined by foreign keys,
  or a ubiquitous language whose terms appear nowhere in the proposed code.

## Worked example

Request: "add partial refunds to the orders API", following the event storm
produced at `intake`.

Attach at `design`. Expected output shape: `design.md`'s Architecture section
names two bounded contexts — **Order Fulfilment** (core; maps onto
`src/orders/`) and **Refund Settlement** (supporting; new, maps onto
`src/refunds/`) — split at the seam the storm flagged, where the language
shifts from *order* to *claim*. The context map records Refund Settlement →
payment provider as an **anticorruption layer** (their vocabulary stops at the
edge) and Order Fulfilment → Refund Settlement as **customer/supplier** with
Refund Settlement absorbing change. `RefundClaim` is an aggregate whose
invariant is "the sum of issued refunds never exceeds the captured amount",
referencing `Order` by id and therefore eventually consistent with it — the
observable gap (a second refund submitted within the settlement window) is
stated under `## Failure modes and rollback`. `## Key decisions` carries the
split with its rejected alternative ("keep refunds inside Order Fulfilment —
rejected: forces the payment provider's settlement vocabulary into the order
model"), mirrored into `decisions.json`. The storm's finance/support conflict
over "credit" is resolved by the boundary rather than by picking a winner:
the term means one thing in each context, and the language table says so.
