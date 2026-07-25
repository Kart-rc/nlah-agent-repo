# Skill Pack: teaching

Practice skills for **human-in-the-loop workflows**: making agent work
legible, teachable, and approvable at human checkpoints. Where the
`geoffreylitt` pack teaches humans the *code* agents write, this pack
teaches humans the *work* agents do — stage by stage.

Derived from the executable-agent-skills proposal
(`docs/proposals/2026-07-23-executable-agent-skills-sdlc.md`, Scenario B):
every human-invoked stage emits a teaching output alongside its artifact,
and unresolved ambiguity reaches the human as questions rather than
dissolving into silent assumptions.

- **Contents:** 1 skill, `explain-your-work/SKILL.md` (+ `USAGE.md`)
- **Format:** same as the other packs — `name`/`description` frontmatter,
  practice-discipline body the producer reads before working

## What this pack is for

These are **practice skills**: discipline documents a stage's producer
subagent reads before doing its work, attached via the workflow manifest:

```yaml
stages:
  - id: design
    uses: stages/design
    skills:
      - uses: skillpacks/teaching/explain-your-work
```

## Skill → default attachment map

| Skill | Discipline | Attached by default at |
|---|---|---|
| `explain-your-work` | EXPLAIN.md teaching artifact per stage: what/why/assumptions/alternatives/checks/questions, cited to the context register when present | every stage of `sdlc-interactive` |

**Enforcement note:** attaching the skill instructs the producer; the
paired `extra_check` on that stage's completeness-check (see the skill's
USAGE.md) is what guarantees — and allows — the extra artifact. Without it,
completeness-check flags EXPLAIN.md as scope drift (F4).

## Relationship to workflows

`sdlc-interactive` attaches `explain-your-work` to every stage and pairs it
with the extra_check; no other shipped workflow attaches it by default.
Attach it ad hoc to any stage a human must approve or learn from.

After adding or renaming a skill here, run `python3 scripts/harness_lint.py`
— manifests referencing removed/renamed skills will fail the lint.
