> **EXCLUDED FROM FINAL SCORING** — The evaluator moved a storefront-scoped Node conflict into root guidance. Retained only as superseded audit evidence.

# Forward Scenario 2 Rerun Raw Evidence

## Run metadata

- Date: 2026-07-14 (America/New_York)
- Evaluator: `/root/forward_validation/forward_s2_rerun`
- Context: fresh child agent with `fork_turns:none`
- Evaluation root: `/private/tmp/claude-context-forward-s2-rerun.BDlyja`
- Target: `/private/tmp/claude-context-forward-s2-rerun.BDlyja/project`
- Skill: clean isolated copy after the evidence-artifact wording fix at `/private/tmp/claude-context-forward-s2-rerun.BDlyja/capability/SKILL.md`
- Prompt: Scenario 2 exact prompt from `tests/skill-evals/scenarios.md`, passed as a user-like instruction to use the isolated skill
- Isolation: only the empty target and bootstrap skill directory were copied; the first-run output, repository tests, plans, design, baselines, rubric, and expected results were absent
- Response SHA-256 (verbatim payload below, before this evidence wrapper): `bd83f7f797a12b5cb1ab9ac09676df7e8fe0acb939aad40446c65c4778655dac`

## Full evaluator response

I reached the required approval checkpoint without modifying the target repository.

The target repository is currently empty, so none of the supplied claims could be verified from files. The installer preview completed successfully:

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

Proposed write map:

```text
CLAUDE.md
Scope: repository-wide
Evidence: unverified developer-provided notes naming package.json, .github/workflows/ci.yml, .nvmrc, and apps/storefront/README.md
Action: create from the stable scaffold, then apply the exact diff below
Conflicts/unknowns: Node 18 in apps/storefront/README.md conflicts with Node 22 reportedly used by .nvmrc and CI; the proposal follows .nvmrc and CI.

.claude/context/codebase-map.md
Scope: repository orientation
Evidence: unverified developer-provided notes naming the reported monorepo areas
Action: create from the stable scaffold, then apply the exact diff below
Conflicts/unknowns: directory existence and ownership boundaries could not be verified.

.claude/rules/payments-migrations.md
Scope: services/payments/**
Evidence: unverified developer-provided note naming services/payments/README.md and npm run test:migrations
Action: create with the exact content below
Conflicts/unknowns: command availability and migration layout could not be verified.

.claude/rules/payments-generated.md
Scope: services/payments/src/generated/**
Evidence: unverified developer-provided note naming services/payments/src/generated/ and npm run generate
Action: create with the exact content below
Conflicts/unknowns: the generator command’s required working directory could not be verified.

.claude/rules/storefront-api.md
Scope: apps/storefront/**
Evidence: unverified developer-provided note describing maintainer review on PR #418 and naming apps/storefront/src/api/client.ts
Action: create with the exact content below
Conflicts/unknowns: the review and client implementation could not be inspected.

.claude/context/learnings/.gitignore
Scope: learning-loop artifacts
Action: create verbatim from the stable scaffold
Exact content:
  receipts/
  *.tmp

.claude/hooks/session-start.py
Scope: Claude Code lifecycle
Action: create verbatim from the stable scaffold
Purpose: report receipt and pending-proposal counts; never modify instructions

.claude/hooks/session-end.py
Scope: Claude Code lifecycle
Action: create verbatim from the stable scaffold
Purpose: atomically record a minimal session receipt under the ignored receipts directory

.claude/skills/start-codebase/SKILL.md
Scope: on-demand onboarding
Action: create verbatim from the stable scaffold

.claude/skills/finish-session/SKILL.md
Scope: review-gated learning proposals
Action: create verbatim from the stable scaffold

.claude/skills/review-learnings/SKILL.md
Scope: approval, rejection, revision, and application of learning proposals
Action: create verbatim from the stable scaffold

.claude/settings.json
Scope: Claude Code lifecycle
Action: create with SessionStart and SessionEnd hooks pointing to the two scaffold scripts
Conflicts/unknowns: none
```

The exact project-specific instruction diff would be:

```diff
diff --git a/CLAUDE.md b/CLAUDE.md
new file mode 100644
--- /dev/null
+++ b/CLAUDE.md
@@
+# Project Instructions
+
+Keep repository-wide instructions concise. Put specialized guidance in the narrowest relevant `.claude/rules/` file or nested `CLAUDE.md`.
+
+Use the installed project skills for codebase onboarding, session reflection, and review-gated learning updates.
+
+## Toolchain and root validation
+
+- Use Node 22. `apps/storefront/README.md` reportedly still says Node 18, but `.nvmrc` and `.github/workflows/ci.yml` reportedly agree on Node 22. Evidence: unverified developer-provided note naming those paths.
+- The root `package.json` reportedly defines `npm run lint`, `npm test`, and `npm run build`. Evidence: unverified developer-provided note naming `package.json`.
+- For pull-request-equivalent validation, run `npm run lint` and `npm test` from the repository root. Include `npm run build` for main-equivalent validation. Evidence: unverified developer-provided note naming `.github/workflows/ci.yml`.
+
+Follow the path-scoped rules under `.claude/rules/` when working in payments or storefront code.
diff --git a/.claude/context/codebase-map.md b/.claude/context/codebase-map.md
new file mode 100644
--- /dev/null
+++ b/.claude/context/codebase-map.md
@@
+# Codebase Map
+
+This map currently records unverified developer-provided orientation. Verify each entry against the named repository path before relying on it.
+
+## Reported areas
+
+- `services/payments/`: payment service with local migration and generated-code rules.
+- `apps/storefront/`: storefront application with a shared API client rule.
+- `services/catalog/`, `apps/admin/`, and `packages/ui/`: separate areas with no project-specific guidance admitted during this bootstrap.
+
+## Reported command sources
+
+- Root commands and scripts: `package.json`.
+- CI command selection and Node version: `.github/workflows/ci.yml`.
+- Repository Node version: `.nvmrc`.
+- Payments-specific guidance: `services/payments/README.md`.
+- Storefront runtime documentation: `apps/storefront/README.md`.
diff --git a/.claude/rules/payments-migrations.md b/.claude/rules/payments-migrations.md
new file mode 100644
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
+Treat payment migrations as forward-only. Test migration changes by running `npm run test:migrations` from `services/payments/`.
+
+Evidence: unverified developer-provided note naming `services/payments/README.md` and the service-local command.
diff --git a/.claude/rules/payments-generated.md b/.claude/rules/payments-generated.md
new file mode 100644
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
+Do not edit files under `services/payments/src/generated/` by hand. Recreate them with `npm run generate`; verify the command's working directory before running it.
+
+Evidence: unverified developer-provided note naming `services/payments/src/generated/` and `npm run generate`.
diff --git a/.claude/rules/storefront-api.md b/.claude/rules/storefront-api.md
new file mode 100644
--- /dev/null
+++ b/.claude/rules/storefront-api.md
@@
+---
+paths:
+  - "apps/storefront/**"
+---
+
+# Storefront API access
+
+Route all storefront API calls through `apps/storefront/src/api/client.ts` so its authentication and retry behavior is preserved.
+
+Evidence: unverified developer-provided note describing a maintainer correction on PR #418 and naming `apps/storefront/src/api/client.ts`.
```

The proposed `.claude/settings.json` is:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.py\""
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/session-end.py\""
          }
        ]
      }
    ]
  }
}
```

Sam’s request to skip lint is intentionally excluded because it was a temporary, machine-specific debugging workaround. No rules are proposed for `services/catalog`, `apps/admin`, or `packages/ui`.

Please explicitly approve or reject these exact writes. If approved, I’ll apply only this map and diff, validate the scaffold, inspect the final diff for scope and secrets, and report any remaining warnings.

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
