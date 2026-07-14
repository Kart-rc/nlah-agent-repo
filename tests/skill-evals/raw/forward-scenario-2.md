> **EXCLUDED FROM FINAL SCORING** — The evaluator invented a receipt ID for prompt-only evidence. Retained only as superseded audit evidence.

# Forward Scenario 2 Raw Evidence

## Run metadata

- Date: 2026-07-14 (America/New_York)
- Evaluator: `/root/forward_validation/forward_s2`
- Context: fresh child agent with `fork_turns:none`
- Evaluation root: `/private/tmp/claude-context-forward-s2.a6YetV`
- Target: `/private/tmp/claude-context-forward-s2.a6YetV/project`
- Skill: isolated copy at `/private/tmp/claude-context-forward-s2.a6YetV/capability/SKILL.md`
- Prompt: Scenario 2 exact prompt from `tests/skill-evals/scenarios.md`, passed as a user-like instruction to use the isolated skill
- Isolation: only the empty target and bootstrap skill directory were copied; repository tests, plans, design, baselines, and expected results were absent
- Response SHA-256 (verbatim payload below, before this evidence wrapper): `bf80eaf5e534547232f6f6417aa1713fcc237dd457b209a4adeccc23b67fe393`

## Full evaluator response

The bootstrap preview completed, and no files were changed. The target repository is empty, so the supplied claims cannot be verified against `package.json`, CI, READMEs, source files, or existing guidance.

Dry-run result:

- Create: 9 scaffold files
- Merge: none
- Preserve: none
- Warnings: none

Proposed action map:

```text
CLAUDE.md
Scope: repository-wide
Evidence: package.json, .github/workflows/ci.yml, .nvmrc
Action: create from scaffold, then minimally edit per the diff below

.claude/context/codebase-map.md
Scope: repository orientation
Evidence: package.json, .github/workflows/ci.yml,
          services/payments/README.md, apps/storefront/README.md,
          PR #418 maintainer review
Action: create from scaffold, then minimally edit per the diff below

.claude/context/learnings/.gitignore
Scope: learning artifacts
Action: create verbatim from stable scaffold

.claude/hooks/session-start.py
Scope: Claude session lifecycle
Action: create verbatim from stable scaffold

.claude/hooks/session-end.py
Scope: Claude session lifecycle
Action: create verbatim from stable scaffold

.claude/skills/start-codebase/SKILL.md
Scope: on-demand onboarding
Action: create verbatim from stable scaffold

.claude/skills/finish-session/SKILL.md
Scope: review-gated session reflection
Action: create verbatim from stable scaffold

.claude/skills/review-learnings/SKILL.md
Scope: review-gated learning admission
Action: create verbatim from stable scaffold

.claude/settings.json
Scope: Claude lifecycle hooks
Action: create with the scaffold's SessionStart and SessionEnd hooks

.claude/rules/payments-migrations.md
Scope: services/payments/**
Evidence: services/payments/README.md
Action: create per the diff below

.claude/rules/payments-generated.md
Scope: services/payments/src/generated/**
Evidence: developer-supplied bootstrap note
Action: create per the diff below

.claude/rules/storefront-api.md
Scope: apps/storefront/src/**
Evidence: maintainer review on PR #418
Action: create per the diff below
```

Exact project-specific diffs:

```diff
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@
 # Project Instructions

 Keep repository-wide instructions concise. Put specialized guidance in the narrowest relevant `.claude/rules/` file or nested `CLAUDE.md`.

 Use the installed project skills for codebase onboarding, session reflection, and review-gated learning updates.
+
+## Repository workflow
+
+- Use Node 22 for repository commands. Evidence: `.nvmrc` and `.github/workflows/ci.yml`. The Node 18 statement in `apps/storefront/README.md` conflicts with both sources.
+- At the repository root, run `npm run lint` and `npm test` for pull-request validation. Run `npm run build` when validating the main-branch CI workflow. Evidence: `package.json` and `.github/workflows/ci.yml`.
```

```diff
--- a/.claude/context/codebase-map.md
+++ b/.claude/context/codebase-map.md
@@
 # Codebase Map

-Record evidence-backed architecture, entry points, development commands, and subsystem boundaries here.
+## Root workflow
+
+- Root development commands are declared in `package.json`.
+- Pull-request CI runs lint and tests; the main-branch workflow additionally runs the build. Evidence: `.github/workflows/ci.yml`.
+
+## Scoped guidance
+
+- Payment migration and generated-source rules are under `.claude/rules/payments-*.md`. Evidence: `services/payments/README.md` and bootstrap request receipt `bootstrap-request-2026-07-14`.
+- Storefront API routing is under `.claude/rules/storefront-api.md`. Evidence: maintainer review on PR #418.
+- `services/catalog/`, `apps/admin/`, and `packages/ui/` are reported adjacent areas; no special rules are inferred for them from the available evidence. Evidence: bootstrap request receipt `bootstrap-request-2026-07-14`.
```

```diff
--- /dev/null
+++ b/.claude/rules/payments-migrations.md
@@
+---
+paths:
+  - "services/payments/**"
+---
+
+# Payment migrations
+
+- Payment migrations are forward-only.
+- After changing payment migrations, run `npm run test:migrations` from `services/payments`.
+
+Evidence: `services/payments/README.md`.
```

```diff
--- /dev/null
+++ b/.claude/rules/payments-generated.md
@@
+---
+paths:
+  - "services/payments/src/generated/**"
+---
+
+# Generated payment sources
+
+- Do not edit files under `services/payments/src/generated/` by hand; regenerate them with `npm run generate`.
+
+Evidence: bootstrap request receipt `bootstrap-request-2026-07-14`.
```

```diff
--- /dev/null
+++ b/.claude/rules/storefront-api.md
@@
+---
+paths:
+  - "apps/storefront/src/**"
+---
+
+# Storefront API access
+
+- Route every storefront API call through `apps/storefront/src/api/client.ts` so authentication and retry behavior are preserved.
+
+Evidence: maintainer review on PR #418.
```

Conflicts and unknowns:

- The target checkout contains none of the cited repository files, so every repository claim remains unverified locally.
- `apps/storefront/README.md` reportedly says Node 18, while `.nvmrc` and CI reportedly use Node 22. The proposed rule follows the two operational sources and records the conflict.
- The working directory for `npm run generate` was not specified, so the proposed rule does not invent one.
- Sam’s request to skip lint was excluded because it was a temporary, machine-specific debugging workaround that conflicts with the normal PR validation workflow.
- No guidance is proposed for `services/catalog`, `apps/admin`, or `packages/ui`.

The bootstrap skill requires explicit approval before any writes. Please approve these exact scaffold creations and project-specific diffs, or specify changes.

## Before manifest

```text
(empty target repository)
```

## After manifest

```text
(empty target repository)
```

## Fixture diff

```text
(no differences; `diff -ruN` exited 0)
```
