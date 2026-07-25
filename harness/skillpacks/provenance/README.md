# Skill Pack: provenance

Practice skills for **context visibility**: making it auditable which
gathered context actually shaped a run's decisions — and which was
retrieved, paid for, and never used.

Derived from the executable-agent-skills proposal
(`docs/proposals/2026-07-23-executable-agent-skills-sdlc.md`): summarized
handoff between stages loses task-critical detail (the NLAH paper's
information-handoff-recall finding), so context must flow as a
path-addressable register with citations, not as prose that silently drops
its sources.

- **Contents:** 1 skill, `context-register/SKILL.md` (+ `USAGE.md`)
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
      - uses: skillpacks/provenance/context-register
```

## Skill → default attachment map

| Skill | Discipline | Attached by default at |
|---|---|---|
| `context-register` | Gathering stages write `context-register.md` (source, provenance, relevance per row); consuming stages cite `[context: CR-n]` on load-bearing decisions; `retrospect` reports cited vs never-cited | `sdlc-autonomous` and `sdlc-interactive`: intake (gather), design + plan (cite) |

**Enforcement note:** the skill instructs the producer; the paired
`extra_check` strings on completeness-check (see the skill's USAGE.md) are
what guarantee — and allow — the register and its citations. Attach the
skill to gathering and consuming stages together, or the register proves
nothing.

## Relationship to workflows

`sdlc-autonomous` and `sdlc-interactive` attach it by default; the original
`sdlc` workflow does not (attach ad hoc when a run's rationale must be
auditable back to sources). The `retrospect` stage consumes the citations
without any attachment — its contract scans for the `[context: CR-n]`
marker whenever a register exists in the run.

After adding or renaming a skill here, run `python3 scripts/harness_lint.py`
— manifests referencing removed/renamed skills will fail the lint.
