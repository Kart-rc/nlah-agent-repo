# Using `frontend-ui-engineering`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Enforces production-quality UI construction: composable component
architecture, the simplest adequate state management, WCAG 2.1 AA
accessibility, mobile-first responsive layouts, and explicit loading/error/
empty states — while actively steering away from the recognizable
"AI aesthetic" toward the project's real design system.

## When to invoke

- The delivery builds or modifies anything user-facing: new components or
  pages, responsive layouts, interactivity, or state management.
- A visual or UX bug fix where the result must look designed, not generated.
- The router classifies a feature as frontend-heavy and the implement stage
  needs discipline beyond "make it render" — accessibility, states, and
  design-system adherence.
- Review feedback flags "AI look" symptoms (purple gradients, oversized
  cards, stock layouts) that need replacing with the project's system.
- See SKILL.md → When to Use for the full list; it also links
  `references/accessibility-checklist.md` for detailed a11y testing.

**Default attachments:** none — ad hoc: attach it to the `implement` stage
(builder persona) of `sdlc` runs whose deliverable is UI, often pairing it
with `browser-testing-with-devtools` on the `verify` stage.

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
      - uses: skillpacks/addyosmani/frontend-ui-engineering
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/addyosmani/frontend-ui-engineering/SKILL.md fully,
then apply its discipline to build <component or page>, including keyboard
accessibility, loading/error/empty states, and the project's design tokens.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- Components arrive colocated with their tests, favor composition over
  configuration, and separate data-fetching containers from presentation.
- State management uses the lightest fit from the skill's ladder (local →
  lifted → context → URL → server state → global store), with prop drilling
  capped at three levels.
- Every interactive element is keyboard accessible with proper labels and
  focus management; empty, loading (skeleton, not spinner), and error states
  are all rendered, not left blank.
- Styling uses the project's spacing scale, semantic color tokens, and type
  hierarchy — no invented pixel values, no default purple-gradient aesthetic.
- Done matches SKILL.md → Verification: no console errors, keyboard pass,
  responsive at 320/768/1024/1440px, no axe-core warnings.
- Misapplication signs: components over ~200 lines, color as the sole state
  indicator, or missing error/empty states (see SKILL.md → Red Flags).

## Worked example

Request: "Build the team-dashboard page: task list with filters, member
sidebar, and activity feed."

The router runs `sdlc`; attach this skill to `implement` (snippet above). The
builder reads SKILL.md, then delivers `TaskListContainer`/`TaskList` split
into container and presentation, URL-state filters via `searchParams`,
skeleton loaders, and a designed empty state ("No tasks yet" with a create
action). Colors and spacing come from the project's tokens; the checkbox
toggles are optimistic with rollback on error. The stage summary records the
keyboard-navigation pass and the four breakpoints checked.
