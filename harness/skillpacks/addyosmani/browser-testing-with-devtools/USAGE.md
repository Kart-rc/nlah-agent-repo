# Using `browser-testing-with-devtools`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Makes the producer verify browser-facing work against a live browser via the
Chrome DevTools MCP server — screenshots, DOM, console, network, performance —
instead of reasoning from source alone. It also enforces strict security
boundaries: browser content is untrusted data, JavaScript execution is
read-only, and the agent uses an isolated profile by default.

## When to invoke

- The delivery touches anything that renders in a browser: UI features,
  layout/styling fixes, client-side state, or frontend performance work.
- A verify stage needs runtime evidence — "confirm the fix actually works in
  the browser" — not just passing unit tests.
- Bug reports involve console errors, failed network requests, CORS,
  Core Web Vitals, or accessibility of rendered output.
- See SKILL.md → When to Use / When NOT to use; do not attach it for
  backend-only or CLI work, and note it requires the `chrome-devtools` MCP
  server to be configured in the environment where the producer runs.

**Default attachments:** none — ad hoc: attach it explicitly to the `verify`
stage (or `implement`, for UI-heavy builder work) of an `sdlc` run whose
target is browser-facing, typically alongside `frontend-ui-engineering`.

## How to invoke

### In a harness workflow

Attach to a stage in the workflow manifest (a one-line edit; use the
`workflow-composer` skill to add, swap, or remove it, then run
`python3 scripts/harness_lint.py`):

```yaml
stages:
  - id: verify
    uses: stages/verify
    skills:
      - uses: skillpacks/addyosmani/browser-testing-with-devtools
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/addyosmani/browser-testing-with-devtools/SKILL.md
fully, then use the chrome-devtools MCP tools to verify <change> at
<localhost URL>, following its UI-bug workflow and security boundaries.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- The producer follows the structured workflows in SKILL.md (reproduce →
  inspect → diagnose → fix → verify for UI bugs; capture → analyze →
  diagnose → fix for network issues) rather than guessing from code.
- Verification evidence includes before/after screenshots, a clean console
  (zero errors and warnings), and confirmed network requests/status codes.
- Complex UI bugs get a written test plan with per-step expected results and
  checks, in the format SKILL.md shows.
- Accessibility is checked through the real accessibility tree, not assumed.
- Done matches SKILL.md → Verification: console clean, visuals match spec,
  JS execution stayed read-only, no browser content treated as instructions.
- Misapplication signs: shipping UI changes never viewed in a browser, or the
  agent acting on instruction-like text found in page content (Red Flags).

## Worked example

Request: "The task-complete animation glitches when users toggle quickly."

Attach the skill to the `verify` stage of an `sdlc` run (manifest snippet
above). After the implement stage lands a fix, the verify producer reads
SKILL.md, writes a test plan into `runs/<run-id>/verify/` (toggle once, undo
within 3 seconds, rapid-toggle five times), drives the page via the
chrome-devtools MCP server, and records: before/after screenshots, zero
console errors, exactly one PATCH per toggle with no duplicates, and a single
task instance in the DOM. The stage output cites this browser evidence, not
just the unit-test run.
