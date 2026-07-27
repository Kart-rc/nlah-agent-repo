# Using `event-storming`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Makes a producer map the business before writing requirements: a timeline of
past-tense domain events, each with the command and actor that caused it and
the policy, external system, and read model around it; a hotspot list of every
disagreement and unknown rule, each routed into the requirements' open
questions; a glossary in the stakeholders' own words with conflicting usages
kept as conflicts; and candidate seams recorded as observations only, with no
bounded context, component, or technology named.

## When to invoke

- The change touches business behaviour whose rules live in people's heads,
  scattered tickets, or one old procedure nobody wants to open.
- Stakeholders use different words for the same thing, or the same word for
  different things.
- The order of the process itself is contested.
- See SKILL.md → When to Use / When NOT to use; clarifying one requester's
  intent on a well-understood request is the `intake` stage's job with
  `addyosmani/interview-me`, and turning the map into contexts and aggregates
  is `domain-modeling/domain-driven-design` at `design`.

**Default attachments:** `intake` in `sdlc`, `sdlc-autonomous`, and
`sdlc-interactive`. Deliberately **not** a `skill_refs` default on
`stages/intake` — that stage is shared by all six workflows, and domain
discovery does not belong in a `proposal` or `tech-decision` run. Attach it
explicitly in SDLC-shaped workflows.

## How to invoke

### In a harness workflow

Attach to a stage in the workflow manifest (a one-line edit; use the
`workflow-composer` skill to add, swap, or remove it, then run
`python3 scripts/harness_lint.py`):

```yaml
stages:
  - id: intake
    uses: stages/intake
    skills:
      - uses: skillpacks/domain-modeling/event-storming
```

The orchestrator passes the skill path to the stage's producer subagent,
which reads it fully before starting (HARNESS.md §7.1).

**Attach the paired `extra_check` too.** `stages/intake` fixes the section
list of `requirements.md`, so `event-storm.md` is only an allowed artifact if
the completeness-check says so — and only a required one if the check demands
it. Add this clause to the stage's completeness-check `with.extra_check`,
appending to any string already there (the sdlc-family manifests already carry
context-register and EXPLAIN.md clauses):

```yaml
    validators:
      - uses: validators/completeness-check
        with:
          checklist: policies/gates/requirements.md
          extra_check: "artifacts/event-storm.md exists with sections Timeline, Hotspots, Ubiquitous language, Candidate seams; every timeline entry is a past-tense domain event naming its command and actor or explicitly marked as a gap; every hotspot appears in requirements.md's Open questions or Assumptions. event-storm.md is an allowed, expected artifact for this stage."
```

Without it the discipline is advisory, and a producer that writes
`event-storm.md` risks the gate reading an unexpected artifact as scope drift.

### Standalone (no harness run)

```text
Read harness/skillpacks/domain-modeling/event-storming/SKILL.md fully, then
produce an event storm for <domain or repository>, deriving a provisional
timeline from the evidence available and marking every unconfirmed event with
its source. Write event-storm.md with the four sections named in the skill.
Record disagreements as hotspots rather than resolving them, and do not name
bounded contexts, components, or technologies.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and
what standalone mode does not guarantee.

## What to expect

- `event-storm.md` alongside `requirements.md`, with `## Timeline`,
  `## Hotspots`, `## Ubiquitous language`, and `## Candidate seams
  (observations only)`.
- Past-tense events in the domain's vocabulary, including the unhappy paths —
  cancelled, rejected, expired, refunded — not only the happy one.
- Hotspots that reappear in the requirements' `## Open questions` or
  `## Assumptions`, never settled inside the storm.
- A glossary in stakeholder words, with competing usages preserved as
  conflicts rather than merged.
- Misapplication signs (from Red Flags): events named as commands or
  components, zero hotspots on an unmapped domain, or a bounded context /
  service / technology named anywhere in the artifact.

## Worked example

Request: "add partial refunds to the orders API."

Attach at `intake`. Expected output shape: an `event-storm.md` in
`runs/<run-id>/stages/intake/artifacts/` whose timeline runs `OrderPlaced →
PaymentCaptured → ShipmentDispatched → ReturnRequested → ReturnReceived →
RefundIssued`, each event carrying its command and actor (`RefundIssued` ←
`IssueRefund` by a support agent, read model: the returns queue screen) and
the policies that fire automatically (`whenever ReturnReceived, then
RestockInitiated`). Hotspots: nobody agrees whether shipping cost is
refundable on a partial return; finance and support use "credit" for two
different things; the 90-day window exists in a support macro but in no code —
all three leave as open questions in `requirements.md`. Candidate seams:
the language shifts from *order* to *claim* at `ReturnRequested`, and refund
settlement is described entirely in the payment provider's vocabulary — both
recorded as observations, with the boundary decision left to `design` and
`domain-modeling/domain-driven-design`.
