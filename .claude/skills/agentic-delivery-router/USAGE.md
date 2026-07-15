# Using `agentic-delivery-router`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans deciding when
> and how to invoke this Claude Code runtime skill. Claude reads SKILL.md
> automatically when the skill triggers; this file is not auto-loaded and
> exists purely as invocation guidance.

## What it does

The entry point for delivery work in this repository: it classifies a request
by work type and risk, selects a workflow manifest by intent match, applies
the risk overlay (extra validators and approval checkpoints) from
`harness/policies/risk-policy.yaml`, then orchestrates the run per
`HARNESS.md` §3 and reports with verification evidence.

## When to invoke

- Per `CLAUDE.md`, **any** delivery request — feature, bug fix, proposal,
  refactor, migration, technical decision, architecture review — routes
  through this skill. See SKILL.md → Step 2 for the full work-type table.
- To resume an interrupted run: "resume run <run-id>" (SKILL.md → Step 7).
- Not for trivial work — typo fixes, formatting-only changes, tiny doc edits
  skip the harness entirely (SKILL.md → Overview).
- If no workflow matches the request, the router itself offers the
  `workflow-composer` skill rather than forcing a bad fit (SKILL.md → Step 4).

**Discovery:** auto-discovered from `.claude/skills/`; its frontmatter
`description` triggers it on any non-trivial engineering or delivery request,
and `CLAUDE.md` makes that routing mandatory for this repo.

## How to invoke

### In conversation

Explicit invocation:

```text
/agentic-delivery-router Add per-tenant rate limiting to the public API.
```

Natural-language requests that trigger it via the frontmatter description:

```text
Fix the flaky retry logic in the payments worker — orders are double-charging.
```

```text
Resume run 2026-07-15-rate-limiting-01.
```

### Requirements

Run it with this repository as the working directory: it needs
`HARNESS.md`, `harness/workflows/*/workflow.yaml`,
`harness/policies/risk-policy.yaml`, and write access to `runs/`. Builder
stages additionally need the target repo available on disk.

## What to expect

- Before anything runs, a filled REQUEST CLASSIFICATION block (work type,
  risk, workflow, gates, assumptions, verification plan) — recorded in the
  run's `task_state.json`.
- A run directory `runs/<run-id>/` containing `request.md`, `inputs.json`,
  `workflow.lock.yaml` (with the risk overlay already applied),
  `task_state.json`, and per-stage artifact directories.
- For High/Critical risk: an approval prompt (plan, rollback, verification)
  that blocks all producing stages until you approve or adjust.
- On gate exhaustion, an escalation report naming the specific human decision
  needed — not a silent pass.
- On completion, a SUMMARY block filled from real artifacts, including
  verification evidence or an honest statement of why it could not run.
- Warning signs it is misapplied: a run starts without the classification
  block, or a workflow is guessed when several plausibly match (SKILL.md →
  Anti-patterns).

## Worked example

You say: "Add per-tenant rate limiting to the public API." The router
classifies it `api-interface-change`, High risk (public contract), selects
the `sdlc` workflow, and locks `workflow.lock.yaml` with the High overlay
from `harness/policies/risk-policy.yaml`. It then presents the plan,
rollback strategy, and verification approach and waits for your approval.
After you approve, stages execute under `HARNESS.md` §3; you get a SUMMARY
listing files changed, tests run, and follow-up risks, with everything
auditable under `runs/<run-id>/`.
