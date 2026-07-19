# Skill Pack: distinguished-engineer

Practice skills for **Distinguished Engineer technical mastery**: setting
multi-year direction, framing unowned problems, estimating before building,
designing for failure, diagnosing what others could not, landing large
migrations, controlling complexity, and multiplying judgment through
artifacts rather than authority. The deep-IC counterpart to the
`tech-director` pack's organizational judgment. Original content authored
for this harness (not vendored).

- **Contents:** 8 skills, each a `<skill-name>/SKILL.md`
- **Format:** same as the other packs — `name`/`description` frontmatter,
  practice-discipline body the producer reads before working

## What this pack is for

These are **practice skills**: judgment discipline documents that a stage's
producer subagent reads before doing its work. They are attached to workflow
stages via the manifest:

```yaml
stages:
  - id: design
    uses: stages/design
    skills:
      - uses: skillpacks/distinguished-engineer/failure-domain-thinking
```

Attaching, detaching, or swapping a practice skill is a one-line manifest
edit. The orchestrator passes attached skill *paths* to the producer subagent
with an instruction to read them before starting (see `HARNESS.md` → Prompt
Templates).

## Skill → default attachment map

| Skill | Discipline | Attached by default at |
|---|---|---|
| `back-of-envelope-estimation` | Order-of-magnitude arithmetic before anything is built: carried numbers, Fermi decomposition, dominating assumptions | `stages/options` (skill_refs); `options` stage of the tech-decision workflow |
| `failure-domain-thinking` | Blast radius, degradation ladders, backpressure, idempotency, incident learning | `stages/design` and `stages/assess` (skill_refs); `design` stage of the sdlc workflow |
| `technical-strategy` | Diagnosis-first strategy, stepping stones, bet sizing, kill criteria, adoption rings | none (ad hoc — see below) |
| `problem-framing` | Unowned ambiguity → falsifiable problem statements before solutioning | none (ad hoc — see below) |
| `deep-system-debugging` | Escalation-tier diagnosis: invariants, hypothesis trees, bisection, minimal repros | none (ad hoc — see below) |
| `large-scale-migration-design` | Strangler slices, parallel run, reversible cutover, explicit end state | none (ad hoc — see below) |
| `complexity-budgeting` | Complexity as spend: concept counting, deletion as roadmap work | none (ad hoc — see below) |
| `force-multiplication` | Paved paths, exemplar artifacts, teaching reviews, delegating problems | none (ad hoc — see below) |

## Ad hoc by design

Most of this pack is deliberately unwired: these disciplines fire on *kinds
of work* (a migration, a hard bug, a strategy document), not on stages every
run passes through. Attach them with a one-line manifest edit where the work
calls for them:

- `technical-strategy` — the `draft` stage of the proposal workflow when the
  proposal *is* a strategy, roadmap, or platform direction.
- `problem-framing` — an `intake` stage when the request is unowned,
  cross-cutting, or arrives pre-shaped as a solution.
- `deep-system-debugging` — the `verify` stage of sdlc when a hard bug
  emerges, alongside or replacing `addyosmani/debugging-and-error-recovery`.
- `large-scale-migration-design` — the `design` and `plan` stages of sdlc
  when the work is a data, traffic, or dependency migration.
- `complexity-budgeting` — an `assess` stage when the review is
  complexity-dominated, or `design` for refactor and consolidation work.
- `force-multiplication` — any stage whose output must change how *other
  engineers* work: standards proposals, review guides, platform templates.

## Boundaries with neighboring packs

Descriptions are the router's only guardrail, so the fault lines are explicit:

- `deep-system-debugging` is escalation-tier: cross-system, intermittent,
  unowned-territory failures. Routine in-repo root-causing is
  `addyosmani/debugging-and-error-recovery`.
- `large-scale-migration-design` designs the technical mechanics of a
  migration (slices, parallel run, cutover). Deprecation policy and user
  communication is `addyosmani/deprecation-and-migration`.
- `complexity-budgeting` works at the system/portfolio level — concepts,
  services, config dimensions. Behavior-preserving code-level refactors are
  `addyosmani/code-simplification`.
- `force-multiplication` scales IC judgment through artifacts and defaults.
  Management practice (delegation levels, feedback, team health) is
  `tech-director/people-leadership`; coalition-building for a specific
  proposal is `tech-director/influence-without-authority`.
- `technical-strategy` sets direction across years. A single bounded
  decision belongs to the tech-decision workflow and
  `tech-director/options-and-tradeoffs`.
- `failure-domain-thinking` designs containment *into* a system.
  Instrumenting it is `addyosmani/observability-and-instrumentation`;
  registering project risks is `tech-director/risk-mitigation`.

## Relationship to workflows

The shipped `tech-decision` workflow attaches `back-of-envelope-estimation`
at its `options` stage, and `sdlc` attaches `failure-domain-thinking` at its
`design` stage, per the map above. Stage documents suggest defaults in their
`skill_refs` frontmatter; the workflow-composer materializes those into new
manifests, where you can freely override them.

After adding or renaming a skill here, run `python3 scripts/harness_lint.py`
— manifests referencing removed/renamed skills will fail the lint.
