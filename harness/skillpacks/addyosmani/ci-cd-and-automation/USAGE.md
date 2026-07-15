# Using `ci-cd-and-automation`

> Companion usage guide for [SKILL.md](SKILL.md) — for humans and
> orchestrators deciding when and how to attach this skill. Producer
> subagents read SKILL.md only; this file adds invocation guidance without
> taxing producer context.

## What it does

Enforces automated quality gates as the delivery mechanism: every change must
pass lint, type check, tests, build, and audit in a pipeline before merge,
with no gate skippable. It also covers deployment discipline — preview
deploys, feature flags, staged rollouts, rollback plans, and secrets kept out
of CI config.

## When to invoke

- The delivery request is itself pipeline work: "set up CI for this repo",
  "add an integration-test job", "make deploys go through staging".
- A feature delivery includes deployment changes — new environment variables,
  a new service, or anything that alters how the project ships.
- CI failures are the bug being fixed, or the pipeline is slow enough
  (over ~10 minutes) that its optimization ladder applies.
- The router flags a delivery as high-risk and the run needs rollback and
  staged-rollout planning as part of the work.
- See SKILL.md → When to Use for the full list.

**Default attachments:** none — ad hoc: attach it to the `implement` stage
(builder persona) when the deliverable is pipeline or deployment
configuration, or to the `deliver` stage when release automation is in scope.

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
      - uses: skillpacks/addyosmani/ci-cd-and-automation
```

The orchestrator passes the skill path to the stage's producer subagent, which
reads it fully before starting (HARNESS.md §7.1).

### Standalone (no harness run)

```text
Read harness/skillpacks/addyosmani/ci-cd-and-automation/SKILL.md fully, then
set up the quality-gate pipeline for this repository, following its GitHub
Actions patterns and secrets rules.
```

See `docs/using-skills-standalone.md` for sequencing multiple skills and what
standalone mode does not guarantee.

## What to expect

- Pipeline changes follow the full gate sequence from SKILL.md (lint → types
  → tests → build → integration → audit); the producer fixes failing gates
  rather than disabling rules or skipping tests.
- Credentials land in GitHub Secrets or a vault — never hardcoded — and CI
  never receives production secrets.
- Deployment work comes with a rollback mechanism and, where relevant,
  feature flags with a planned cleanup date.
- Slow pipelines get the optimization ladder applied in order: caching,
  parallel jobs, path filters, matrix sharding.
- Done matches SKILL.md → Verification: all gates present, failures block
  merge via branch protection, pipeline under ~10 minutes.
- Misapplication signs: tests silenced to turn CI green, or deploys shipping
  without a rollback path (see SKILL.md → Red Flags).

## Worked example

Request: "Our repo has no CI — add a pipeline with tests against Postgres and
preview deploys."

The router classifies this as an infrastructure feature and runs `sdlc`;
attach this skill to the `implement` stage as in the snippet above. The
builder producer reads SKILL.md, then adds `.github/workflows/ci.yml` with
parallel lint/typecheck/test jobs, a Postgres service container using a
`CI_DB_PASSWORD` secret, and a Vercel preview-deploy job gated on
`pull_request`. Its stage output notes branch protection settings to enable
and confirms the pipeline runs in about six minutes.
