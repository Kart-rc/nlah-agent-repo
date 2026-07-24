# Using `context-register`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Gives a run end-to-end context visibility: the gathering stage (intake or
research) emits `context-register.md` — every source consulted, with
provenance and relevance — and consuming stages (design, plan) cite
`[context: CR-n]` on load-bearing decisions. The `retrospect` stage then
reports cited vs never-cited entries (wasted retrieval) and uncited
load-bearing claims (fabrication risk).

## When to invoke

- Always attach to gathering and consuming stages **together** — a register
  nobody cites proves nothing, and citations without a register resolve to
  nothing.
- Both `sdlc-autonomous` and `sdlc-interactive` attach it by default
  (intake gathers; design and plan cite).
- Attach ad hoc wherever a delivery's rationale must be auditable back to
  sources: compliance-sensitive work, externally-researched proposals,
  onboarding runs where the human wants to see what the agent looked at.

## How to invoke

### In a harness workflow

Attach to the gathering stage with its enforcement `extra_check` (which both
requires and allows the extra artifact — completeness-check otherwise flags
it as scope drift, F4):

```yaml
stages:
  - id: intake
    uses: stages/intake
    validators:
      - uses: validators/completeness-check
        with:
          extra_check: "artifacts/context-register.md exists as a table with columns id, source, provenance, relevance, key claim it supports; ids are CR-<n>. context-register.md is an allowed, expected artifact for this stage."
    skills:
      - uses: skillpacks/provenance/context-register
```

and to each consuming stage with the citation check:

```yaml
  - id: design
    uses: stages/design
    validators:
      - uses: validators/completeness-check
        with:
          extra_check: "load-bearing decisions in the design cite [context: CR-n] entries or explicitly state that no external context informed them."
    skills:
      - uses: skillpacks/provenance/context-register
```

### Standalone (no harness run)

```text
Read harness/skillpacks/provenance/context-register/SKILL.md fully. While
researching, maintain context-register.md per its format; when writing the
deliverable, cite [context: CR-n] on every load-bearing decision.
```

## What to expect

- One extra artifact in the gathering stage's directory
  (`context-register.md`), and `[context: CR-n]` markers inside downstream
  artifacts — the register itself is never modified downstream.
- The completeness-check citation `extra_check` is mechanical (citations
  present); whether the *right* entries are cited is judgment — point the
  adversarial-reviewer's `focus` at unsupported claims when that matters.
- `retrospect` closes the loop: its Context usage section quantifies
  retrieved-vs-cited and lists never-cited entries, turning context waste
  and fabrication risk into run metrics.
- Pairs with `skillpacks/teaching/explain-your-work`: EXPLAIN.md's What/Why
  sections cite the same `CR-n` ids.
