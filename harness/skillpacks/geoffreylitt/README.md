# Skill Pack: geoffreylitt

Practice skills for **understanding the code your agents write**: literate
explainer documents instead of raw diffs, comprehension quizzes as a speed
regulator before review, and ephemeral interactive micro-worlds for
inhabiting runtime behavior.

Adapted from Geoffrey Litt's talk *"Understanding code that AI writes for
you"* (AI Engineer, design engineering track —
https://www.youtube.com/watch?v=WkBPX-oDMnA). The framing: humans understand
not merely to *verify* agent output but to *participate* — to keep the rich
mental model that produces the next idea — and letting that model degrade is
**cognitive debt** that compounds like technical debt.

- **Contents:** 3 skills, each a `<skill-name>/SKILL.md`
- **Format:** same as the other packs — `name`/`description` frontmatter,
  practice-discipline body the producer reads before working

## What this pack is for

These are **practice skills**: discipline documents a stage's producer
subagent reads before doing its work. They are attached to workflow stages
via the manifest:

```yaml
stages:
  - id: implement
    uses: stages/implement
    skills:
      - uses: skillpacks/geoffreylitt/code-explainers
      - uses: skillpacks/geoffreylitt/understanding-quizzes
```

Attaching, detaching, or swapping a practice skill is a one-line manifest
edit. The orchestrator passes attached skill *paths* to the producer subagent
with an instruction to read them before starting (see `HARNESS.md` → Prompt
Templates).

## Skill → default attachment map

| Skill | Discipline | Attached by default at |
|---|---|---|
| `code-explainers` | Literate explainer docs for changes: background first, intuition before details, literate code diff, markdown + HTML output ending in a quiz | `document` (stage `skill_refs` + the `sdlc-autonomous` / `sdlc-interactive` manifests) |
| `understanding-quizzes` | ~5-question comprehension quiz per change; the speed-regulator rule: no review request until the responsible human passes | `sdlc-interactive`: `document` and `deliver` |
| `micro-worlds` | Ephemeral interactive artifacts (state debuggers, step-through replays, simulations) wired to real code, built to be inhabited then discarded | none (ad hoc — see below) |

All three are deliberately standalone: attach them ad hoc with a one-line
manifest edit wherever agent-written code must be *understood by a human*,
not just delivered. Natural homes in the `sdlc` workflow: `code-explainers`
and `understanding-quizzes` on the `implement` or `verify` stage (so the
delivered change arrives with its explainer and quiz), `micro-worlds` on
`implement` or `verify` when the change involves complex runtime state or
a many-step migration. The three chain: an explainer ends with a quiz, and
hands off to a micro-world when static explanation isn't enough.

They also work well outside the harness — see
`docs/using-skills-standalone.md`.

## Relationship to workflows

The sdlc family's `document` stage attaches `code-explainers` by default,
and `sdlc-interactive` closes its `document` and `deliver` stages with
`understanding-quizzes`; beyond that they are opt-in overlays for work
where human understanding of agent-written code is itself a deliverable.
Stage documents suggest defaults in their `skill_refs` frontmatter; the
workflow-composer materializes those into new manifests, where you can
freely add these skills.

After adding or renaming a skill here, run `python3 scripts/harness_lint.py`
— manifests referencing removed/renamed skills will fail the lint.
