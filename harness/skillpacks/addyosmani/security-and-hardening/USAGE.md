# Using `security-and-hardening`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Enforces security-first development: threat-model before hardening (trust
boundaries, STRIDE, abuse cases), then apply a three-tier boundary system
(Always / Ask First / Never) and OWASP prevention patterns — including the
LLM Top 10 for AI features — to every line touching untrusted data.

## When to invoke

See SKILL.md → When to Use for the full criteria. Harness routing cues:

- Runs whose implement stage handles user input, authentication or
  authorization, sensitive data storage, file uploads, webhooks, payments,
  or third-party integrations.
- Requests the router tags as elevated delivery risk for security reasons —
  the natural companion to a security risk overlay.
- Any run adding LLM-backed features (chatbots, agents, RAG): the skill's
  AI/LLM section treats model output as untrusted input.
- Also useful on a verification stage: its Security Review Checklist gives
  a validator concrete gates to check against.

**Default attachments:** none — ad hoc: attach it explicitly on the
`implement` stage of the `sdlc` workflow when the work touches a trust
boundary, or on `verify` when a security review of the produced change is
the point (the `red-team` validator persona probes along the same lines).

## How to invoke

### In a harness workflow

Attach to a stage in the workflow manifest (a one-line edit; use the
`workflow-composer` skill to add, swap, or remove it, then run
`python3 scripts/harness_lint.py`):

```yaml
stages:
  - id: implement
    uses: stages/implement
    skills:
      - uses: skillpacks/addyosmani/security-and-hardening
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/addyosmani/security-and-hardening/SKILL.md fully,
then threat-model and harden <feature or endpoint>, applying its
Always / Ask First / Never boundaries and review checklist.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- The producer starts by naming trust boundaries and assets and running a
  quick STRIDE pass, writing abuse cases next to use cases before coding.
- "Ask first" items — new auth flows, new sensitive-data categories, CORS
  changes, file uploads — surface as explicit approval requests; in a
  harness run these route through the workflow's approval gates.
- Input validation lands at system boundaries, queries are parameterized,
  secrets stay in the environment, `npm audit` findings get triaged via the
  skill's decision tree, and LLM output is validated before use.
- Done means SKILL.md → Verification passes (no critical/high audit
  findings, authz on every protected endpoint, no SSRF-able fetches); the
  pack's `references/security-checklist.md` holds the detailed list.
- Misapplication signs (SKILL.md → Red Flags): user input concatenated into
  queries or HTML, or endpoints shipping without authorization checks.

## Worked example

Request: "Add a webhook endpoint so customers can push events into their
account." Use `workflow-composer` to add this skill to the run's implement
stage:

```yaml
  - id: implement
    uses: stages/implement
    skills:
      - uses: skillpacks/addyosmani/incremental-implementation
      - uses: skillpacks/addyosmani/security-and-hardening
```

The builder threat-models first (spoofed senders, SSRF via callback URLs,
replay), implements signature verification, schema validation, rate limits,
and an allowlisted URL fetch per SKILL.md's SSRF pattern, and flags the new
external integration as an "Ask first" approval before merging.
