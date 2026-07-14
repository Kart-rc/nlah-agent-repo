> **EXCLUDED FROM FINAL SCORING** — The evaluator combined generated-path ownership with service-wide migration guidance. Retained only as superseded audit evidence.

# Forward Scenario 2 Final Raw Evidence

## Run metadata

- Date: 2026-07-14 (America/New_York)
- Evaluator: `/root/forward_validation/forward_s2_final`
- Context: fresh child agent with `fork_turns:none`
- Evaluation root: `/private/tmp/claude-context-forward-s2-final.w4tx0S`
- Target: empty disposable project
- Skill: isolated bootstrap skill copied after the scoped-conflict fix
- Isolation: no source-repository tests, plans, design, baselines, rubric, prior output, or expected answer
- Response SHA-256 before this wrapper: `c87111c34c86a32029b9db864654bf1d927bfa1c349a9bebfbc2d7ee0bf764f0`

## Exact evaluator wrapper

The evaluator was told to work only inside the evaluation root, treat its empty `project` directory as the target, use the isolated bootstrap `SKILL.md`, and then received the exact Scenario 2 prompt from `scenarios.md`. It was told only to return its full user-facing response at the skill checkpoint.

## Full evaluator response

The required dry run completed successfully against the empty target repository.

Dry-run result:

```json
{
  "create": [
    "CLAUDE.md",
    ".claude/context/codebase-map.md",
    ".claude/context/learnings/.gitignore",
    ".claude/hooks/session-start.py",
    ".claude/hooks/session-end.py",
    ".claude/skills/start-codebase/SKILL.md",
    ".claude/skills/finish-session/SKILL.md",
    ".claude/skills/review-learnings/SKILL.md",
    ".claude/settings.json"
  ],
  "merge": [],
  "preserve": [],
  "warning": []
}
```

The target contains no repository files, so the referenced manifests, CI configuration, documentation, and PR comment could not be inspected. Every project-specific claim below is therefore explicitly labeled as an unverified developer-provided note.

## Proposed write map

| Path | Scope | Action |
|---|---|---|
| `CLAUDE.md` | Repository-wide | Create from stable scaffold, then apply the exact diff below |
| `.claude/context/codebase-map.md` | On-demand repository orientation | Create from stable scaffold, then apply the exact diff below |
| `.claude/rules/payments.md` | `services/payments/**` | Create with the exact content below |
| `.claude/rules/storefront.md` | `apps/storefront/**` | Create with the exact content below |
| `.claude/context/learnings/.gitignore` | Learning artifacts | Create unchanged from the stable scaffold |
| `.claude/hooks/session-start.py` | Lifecycle hook | Create unchanged from the stable scaffold |
| `.claude/hooks/session-end.py` | Lifecycle hook | Create unchanged from the stable scaffold |
| `.claude/skills/start-codebase/SKILL.md` | On-demand onboarding | Create unchanged from the stable scaffold |
| `.claude/skills/finish-session/SKILL.md` | Review-gated reflection | Create unchanged from the stable scaffold |
| `.claude/skills/review-learnings/SKILL.md` | Explicit learning review | Create unchanged from the stable scaffold |
| `.claude/settings.json` | Claude lifecycle settings | Create with the stable scaffold’s `SessionStart` and `SessionEnd` hooks |

There are no merge or preserve actions.

## Exact project-specific diffs

`CLAUDE.md`:

```diff
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@
 # Project Instructions

 Keep repository-wide instructions concise. Put specialized guidance in the narrowest relevant `.claude/rules/` file or nested `CLAUDE.md`.

 Use the installed project skills for codebase onboarding, session reflection, and review-gated learning updates.
+
+## Repository-wide workflow
+
+- Use Node 22 for repository work.
+  Evidence: unverified developer-provided note naming `.nvmrc` and `.github/workflows/ci.yml`.
+- The root verification commands are `npm run lint`, `npm test`, and `npm run build`. CI runs lint and tests for every pull request and runs the build on `main`.
+  Evidence: unverified developer-provided note naming `package.json` and `.github/workflows/ci.yml`.
```

`.claude/context/codebase-map.md`:

```diff
--- a/.claude/context/codebase-map.md
+++ b/.claude/context/codebase-map.md
@@
 # Codebase Map

-Record evidence-backed architecture, entry points, development commands, and subsystem boundaries here.
+All entries currently originate from unverified developer-provided notes. Confirm them against the cited repository paths when those files are available.
+
+## Automation
+
+- `.github/workflows/ci.yml` reportedly runs root lint and tests on every pull request and runs the root build only on `main`.
+- `.nvmrc` and `.github/workflows/ci.yml` reportedly select Node 22.
+
+## Payments
+
+- `services/payments/README.md` reportedly defines the forward-only migration policy and the service-local `npm run test:migrations` check.
+- `services/payments/src/generated/` is reportedly produced by `npm run generate`.
+
+## Storefront
+
+- `apps/storefront/README.md` reportedly contains a stale Node 18 requirement that conflicts with `.nvmrc` and `.github/workflows/ci.yml`.
+- `apps/storefront/src/api/client.ts` is the required API path according to an unverified developer-provided note about a maintainer review comment on PR #418.
```

`.claude/rules/payments.md`:

```diff
--- /dev/null
+++ b/.claude/rules/payments.md
@@
+---
+paths:
+  - "services/payments/**"
+---
+
+# Payments
+
+- Payment migrations are forward-only. From `services/payments`, validate migration changes with `npm run test:migrations`.
+  Evidence: unverified developer-provided note naming `services/payments/README.md`.
+- Do not edit files under `services/payments/src/generated/` by hand; regenerate them with `npm run generate`.
+  Evidence: unverified developer-provided note naming `services/payments/src/generated/` and `npm run generate`.
```

`.claude/rules/storefront.md`:

```diff
--- /dev/null
+++ b/.claude/rules/storefront.md
@@
+---
+paths:
+  - "apps/storefront/**"
+---
+
+# Storefront
+
+- Route every storefront API call through `apps/storefront/src/api/client.ts` so authentication and retry behavior are preserved.
+  Evidence: unverified developer-provided note about a maintainer review comment on PR #418 naming `apps/storefront/src/api/client.ts`.
+- Do not follow the Node 18 requirement in `apps/storefront/README.md`; use the repository-wide Node 22 runtime selected by `.nvmrc` and `.github/workflows/ci.yml`.
+  Evidence: unverified developer-provided note naming all three files.
```

## Conflicts, exclusions, and unknowns

- The reported Node 18 statement in `apps/storefront/README.md` conflicts with the reported Node 22 configuration in `.nvmrc` and CI. The proposal makes Node 22 repository-wide and keeps the stale-document warning storefront-scoped.
- The working directory for `npm run generate` was not specified, so the rule does not invent one.
- Sam’s request to skip lint is excluded as a temporary, machine-specific workaround. It does not override the reported pull-request CI requirement.
- No rules are proposed for `services/catalog`, `apps/admin`, or `packages/ui`; the notes provide no conventions for those areas.
- PR #418 and every cited repository file remain unverified because the target is empty.

No files have been written. Please explicitly approve this exact write map and diff if you want me to apply it.

## Before, after, and diff

Both manifests are empty. `diff -ruN` exited 0 with no output; the approval checkpoint made no target mutation.
