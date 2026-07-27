# Skill Pack: domain-modeling

Practice skills for **the business domain itself**: discovering how the
business actually behaves before requirements are frozen, and modelling the
change against that behaviour rather than against the technical layers.

The two skills are deliberately a pair, split along the harness's own
problem-space / solution-space boundary:

- `event-storming` runs in the **problem space** — a timeline of past-tense
  domain events with the commands, actors, policies, external systems, and
  read models around them, plus the hotspots where nobody actually agrees.
  It names no components and picks no technologies.
- `domain-driven-design` runs in the **solution space** — it turns that
  discovery into decided bounded contexts, a context map with named
  integration relationships, a ubiquitous language carried into code, and
  aggregates whose invariants define transactional boundaries.

Lineage: event storming as described by Alberto Brandolini; domain-driven
design as described by Eric Evans (*Domain-Driven Design*, 2003) and Vaughn
Vernon (*Implementing Domain-Driven Design*, 2013). Both are restated here as
harness practice disciplines, scoped to what a producer subagent can actually
do inside a stage contract.

- **Contents:** 2 skills — `event-storming/SKILL.md` and
  `domain-driven-design/SKILL.md` (each with `USAGE.md` and a
  `references/` deep-dive)
- **Format:** same as the other packs — `name`/`description` frontmatter,
  practice-discipline body the producer reads before working

## What this pack is for

These are **practice skills**: discipline documents a stage's producer
subagent reads before doing its work, attached via the workflow manifest:

```yaml
stages:
  - id: intake
    uses: stages/intake
    skills:
      - uses: skillpacks/domain-modeling/event-storming

  - id: design
    uses: stages/design
    skills:
      - uses: skillpacks/domain-modeling/domain-driven-design
```

## Skill → default attachment map

| Skill | Discipline | Attached by default at |
|---|---|---|
| `event-storming` | Walk the business timeline as past-tense domain events; attach the command, actor, policy, external system, and read model around each; record hotspots and the ubiquitous language instead of resolving them | `sdlc`, `sdlc-autonomous`, `sdlc-interactive`: `intake` |
| `domain-driven-design` | Bounded contexts as language boundaries, a context map whose every integration names its relationship, aggregates defined by the invariant they protect, tactical patterns only where they earn their place | `sdlc`, `sdlc-autonomous`, `sdlc-interactive`: `design` (also a `skill_refs` default on `stages/design`) |

**Enforcement note:** like `provenance/context-register`, each skill instructs
the producer while a paired `extra_check` on that stage's completeness-check is
what makes the output required — and, for `event-storm.md`, what makes the
extra artifact *allowed* at all. The exact strings are in each skill's
`USAGE.md`. Attaching the skill without the `extra_check` leaves the discipline
advisory.

## Relationship to workflows

The three sdlc-family workflows attach both by default. The stage split is not
cosmetic: `stages/intake` forbids solution content ("Do NOT design solutions,
name technologies, or sketch implementations — requirements only"), so
`event-storming` records candidate seams as *observations with open questions*
and leaves every boundary decision to `design`, where `domain-driven-design`
makes it explicitly and records the rejected alternative.

`domain-driven-design` is listed in `harness/stages/design/stage.md`
`skill_refs`, so the `workflow-composer` materializes it into future manifests
that use the design stage. `event-storming` is deliberately **not** in
`stages/intake` `skill_refs` — intake is shared by all six workflows, and
domain discovery does not belong in a `proposal` or `tech-decision` run.
Attach it per workflow with the one-liner above.

Both skills also work standalone; see each `USAGE.md` and
`docs/using-skills-standalone.md`.

After adding or renaming a skill here, run `python3 scripts/harness_lint.py`
— manifests referencing removed/renamed skills will fail the lint.
