# Future Workflows

The harness ships with `sdlc` and `proposal`. This document maps the router's
full work-type taxonomy to workflows (existing and future) and walks through
composing the two next candidates — **roadmap** and **LOE estimation** — to
show that new workflows are compositions, not construction projects.

## Work type → workflow mapping

| Router work type | Workflow (v1) | Future |
|---|---|---|
| new-feature | `sdlc` | — |
| bug-fix | `sdlc` | possible slim `bugfix` variant (drop design for localized fixes) |
| api-interface-change | `sdlc` | + data gate checklist on design when schemas move |
| performance-cost-change | `sdlc` | + baseline/re-measure criteria via a `benchmark` stage |
| refactor-simplification | `sdlc` | behavior-preservation `extra_check` on verify |
| proposal, idea-refinement | `proposal` | — |
| vague-requirement | clarify → route | — |
| data-change | F7 → composer | `data-change`: sdlc stages + data gate checklists + backfill stage |
| infrastructure-change | F7 → composer | `infra-change`: sdlc stages + security/observability checklists throughout |
| security-sensitive-change | F7 → composer (or `sdlc` at High/Critical risk, which auto-adds red-team + approval) | dedicated workflow with doubt-driven-development attached |
| migration-deprecation | F7 → composer | `migration`: plan-heavy, adds compatibility-window + backout stages |
| observability-change | F7 → composer | slim workflow: design → implement → verify with observability checklist |
| production-launch | F7 → composer | `launch`: release-gate-centric, no implement stage |

Until a dedicated workflow exists, the router offers the composer with the
suggested composition above (failure class F7 — never guess-and-run).

## Walkthrough 1: composing a `roadmap` workflow

What the composer session would produce (abridged):

**Interview** → id `roadmap`; deliverable: a prioritized, time-phased roadmap
document; triggers: "build a roadmap for …", "what should we do next quarter";
inputs: `request`, `horizon` (e.g. "2 quarters"), `audience`.

**Catalog** → reuse `intake` (verbatim) and `research` (verbatim — its
contract is "gather evidence for a decision", which a roadmap is). Gap: no
stage turns evidence into a *prioritized sequence* — that is a genuinely new
judgment, so add one new stage per `docs/adding-a-stage.md`:

- `prioritize` — producer: planner; inputs: `requirements`, `research_digest`;
  output: `prioritized_backlog` (items with value/effort/dependency scores and
  an explicit scoring rubric); acceptance criteria: every item scored under a
  stated rubric; dependencies acyclic; cut-lines justified; default
  validators: completeness-check + adversarial-reviewer (focus: "score
  gaming, dependency omissions, pet-project bias").

Then reuse `draft` and `finalize` with roadmap-flavored parameters.

**Scaffold** (manifest core):

```yaml
stages:
  - { id: intake,     uses: stages/intake,     needs: [] }
  - id: research
    uses: stages/research
    needs: [intake]
    knowledge:
      - uses: knowledge/enterprise-mcp     # org initiatives, capacity
      - uses: knowledge/second-brain       # requester's strategy notes
  - { id: prioritize, uses: stages/prioritize, needs: [research] }
  - id: draft
    uses: stages/draft
    needs: [prioritize]
    validators:
      - uses: validators/completeness-check
      - uses: validators/adversarial-reviewer
      - uses: validators/persona-reviewer
        with: { persona: "Engineering lead who must staff this roadmap with a fixed team" }
  - { id: finalize,   uses: stages/finalize,   needs: [draft] }
```

One new stage document; everything else is attachment lines.

## Walkthrough 2: composing an `loe` (level-of-effort) workflow

**Interview** → id `loe`; deliverable: a defensible effort estimate with
uncertainty ranges; triggers: "how big is …", "estimate the effort for …";
inputs: `request`, `target_repo` (optional), `constraints`.

**Catalog** → reuse `intake`, `research` (evidence: comparable past work via
enterprise-mcp/second-brain; codebase reconnaissance if `target_repo` given).
Gap: one new stage:

- `estimate` — producer: planner; inputs: `requirements`, `research_digest`;
  output: `loe_estimate` (work breakdown with three-point estimates
  (best/likely/worst), stated assumptions, confidence level, and what would
  change the number); acceptance criteria: every breakdown item has a
  three-point estimate; assumptions enumerated; comparables cited or their
  absence declared; no point estimates without ranges. Default validators:
  completeness-check + adversarial-reviewer (focus: "optimism bias, missing
  work categories — testing, review, deployment, coordination") +
  persona-reviewer (`persona: "Delivery manager who will be held to this
  estimate"`).

Then `finalize` packages the estimate for the audience.

```yaml
stages:
  - { id: intake,   uses: stages/intake,   needs: [] }
  - id: research
    uses: stages/research
    needs: [intake]
    knowledge:
      - uses: knowledge/enterprise-mcp
      - uses: knowledge/second-brain
  - { id: estimate, uses: stages/estimate, needs: [research] }
  - { id: finalize, uses: stages/finalize, needs: [estimate] }
```

Again: one new stage document, one manifest.

## The pattern

Every future workflow so far decomposes into: **intake (shared) → evidence
(shared research + knowledge adapters) → one domain-specific judgment stage
(new, small) → packaging (shared draft/finalize) — with rigor supplied by
validator attachments, not new machinery.** That is the magnetic thesis
holding in practice.
