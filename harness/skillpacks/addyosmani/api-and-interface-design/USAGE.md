# Using `api-and-interface-design`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Enforces contract-first interface design: define typed inputs/outputs, one
consistent error strategy, boundary-only validation, and additive (never
breaking) evolution before any implementation begins. It applies Hyrum's Law
and the One-Version Rule to anything with consumers — REST/GraphQL endpoints,
module boundaries, or component props.

## When to invoke

- The request adds or changes any public surface: new endpoints, a shared
  module's exports, component prop interfaces, or a schema that shapes an API.
- The router classified the work as a feature whose design stage must produce
  an interface contract before the implement stage starts.
- A frontend and backend (or two teams/agents) will build against each other
  in parallel and need a stable contract to work from.
- An existing public interface must change — the skill forces the
  additive-over-breaking analysis before anyone edits it.
- See SKILL.md → When to Use for the full list; skip it for purely internal
  refactors that touch no consumer-visible surface.

**Default attachments:** suggested by `stages/design` `skill_refs`; attached
to the `design` stage of the `sdlc` workflow.

## How to invoke

### In a harness workflow

Attach to a stage in the workflow manifest (a one-line edit; use the
`workflow-composer` skill to add, swap, or remove it, then run
`python3 scripts/harness_lint.py`):

```yaml
stages:
  - id: design
    uses: stages/design
    skills:
      - uses: skillpacks/addyosmani/api-and-interface-design
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/addyosmani/api-and-interface-design/SKILL.md fully,
then apply its discipline to design the interface contract for <feature>,
producing typed input/output schemas and error semantics before any
implementation.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- The design artifact leads with explicit contracts (interfaces or schemas)
  rather than implementation sketches — the types come first.
- Error handling is specified once, as a single consistent format with a
  status-code mapping, instead of per-endpoint improvisation.
- Validation is placed only at system boundaries (routes, forms, third-party
  responses, env loading), with third-party data explicitly untrusted.
- List endpoints get pagination and filtering from the start; naming follows
  the conventions table in SKILL.md.
- Done means the SKILL.md → Verification checklist passes: typed schemas for
  every endpoint, one error format, additive-only field changes.
- Warning signs it is misapplied: endpoints returning different shapes by
  condition, verbs in REST URLs, or validation scattered through internal
  code (see SKILL.md → Red Flags).

## Worked example

Request: "Add a comments feature to tasks — API plus UI."

The router runs the `sdlc` workflow; the `design` stage already carries this
skill (with `spec-driven-development`). The design producer reads SKILL.md and
emits a contract in `runs/<run-id>/design/`: a `CommentAPI` interface,
`GET/POST /api/tasks/:id/comments` with a paginated list response, a
`CreateCommentInput` Zod schema validated at the route handler, and the shared
`APIError` shape. The implement stage then builds against that contract, and
the verify stage can check responses against the committed schemas instead of
reverse-engineering intent from code.
