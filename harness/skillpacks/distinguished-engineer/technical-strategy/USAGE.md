# Using `technical-strategy`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Makes a producer treat direction-setting as a portfolio: a diagnosis of why
the current trajectory is insufficient, one guiding policy with actions that
trace to it, stepping stones that each pay for themselves, bets sized by
reversibility with kill criteria written before evidence arrives, and
emerging technology placed in explicit adopt/trial/assess/hold rings.

## When to invoke

- The artifact under production *is* a technical strategy, north-star
  architecture, or multi-year roadmap — commonly a `proposal` workflow run
  whose subject is direction rather than a single change.
- Planning cycles where platform investments must be sequenced and some
  attractive options must be explicitly declined.
- An emerging-technology position ("should we be on X?") needs a ringed,
  evidenced answer rather than a mood.
- See SKILL.md → When to Use / When NOT to use; a single bounded decision
  belongs to the tech-decision workflow with
  `tech-director/options-and-tradeoffs` instead.

**Default attachments:** none (ad hoc). Natural home: the `draft` stage of
the `proposal` workflow when the proposal is a strategy or roadmap.

## How to invoke

### In a harness workflow

Attach to a stage in the workflow manifest (a one-line edit; use the
`workflow-composer` skill to add, swap, or remove it, then run
`python3 scripts/harness_lint.py`):

```yaml
stages:
  - id: draft
    uses: stages/draft
    skills:
      - uses: skillpacks/distinguished-engineer/technical-strategy
```

The orchestrator passes the skill path to the stage's producer subagent,
which reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/distinguished-engineer/technical-strategy/SKILL.md
fully, then draft the technical strategy for <area>, starting from a
diagnosis grounded in <inputs> before proposing any investment.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and
what standalone mode does not guarantee.

## What to expect

- The document opens with a diagnosis — the facts that make the current
  trajectory insufficient — before any goal or investment appears.
- One guiding policy; every proposed action traces to it, and at least one
  attractive option is explicitly declined with reasoning.
- Stepping stones are sequenced so each is independently valuable even if
  the north star is later abandoned.
- Every major bet carries a size, a reversibility class, and kill criteria
  (observable result, date) written before any evidence arrives.
- Emerging-technology positions appear as adopt/trial/assess/hold placements
  tied to what the diagnosis says must become cheap.
- Misapplication signs (from Red Flags): goals with dates but no diagnosis,
  or a plan whose payoff all arrives in the final year.

## Worked example

Request: "Write our data-platform strategy for the next three years."

Attach this skill to the `draft` stage of a `proposal` run. Expected output
shape: a strategy in `runs/<run-id>/` whose diagnosis names the three facts
that hurt (ingest doubling yearly, 40% of engineer time on pipeline
firefighting, two teams building redundant serving layers); a guiding
policy (consolidate on one governed serving path before adding capabilities);
stepping stones (unify ingestion for the two highest-volume sources first —
valuable alone as an oncall reduction); a big bet (replatform serving)
carrying kill criteria ("if shadow-read parity is below 99.9% after two
quarters, stop"); and a declined option (a lakehouse migration, held with
reasons). Streaming-native engines sit in `trial` — one team, one workload,
exit date — with vector databases in `assess`.
