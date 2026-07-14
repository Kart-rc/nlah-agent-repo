# Forward Scenario 2 Narrow-Scope Final Raw Evidence

## Run metadata

- Date: 2026-07-14 (America/New_York)
- Evaluator: `/root/forward_validation/forward_s2_scope_final`
- Context: fresh child agent with `fork_turns:none`
- Evaluation root: `/private/tmp/claude-context-forward-s2-scope-final.DOYAd5`
- Target: empty disposable project
- Skill: isolated bootstrap skill after the separate-narrow-scope instruction
- Isolation: no source-repository tests, plans, design, baselines, rubric, prior output, generated caches, or expected answer
- Prompt: exact unchanged Scenario 2 prompt from `scenarios.md`, passed as a user-like instruction to use the isolated skill
- Response SHA-256 before this wrapper: `a99dea427d0b42115fc103eeb39c8c6db42b2b146ffc859c3f7f14de2e32c2e8`

## Full evaluator response

I reached the required approval checkpoint. No files have been written.

The supplied target repository is empty, so none of the developer-provided paths or claims can be inspected directly. All project-specific guidance below will therefore be labeled as unverified developer-provided notes until the repository contents are available.

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

Proposed action map:

| Path | Scope | Action | Purpose |
|---|---|---|---|
| `CLAUDE.md` | Repository-wide | Create from scaffold, then minimally edit | Lean root commands, Node version, CI expectations, and routing |
| `.claude/context/codebase-map.md` | On-demand repository orientation | Create from scaffold, then minimally edit | Detailed evidence, conflicts, subsystem notes, and unknowns |
| `.claude/context/learnings/.gitignore` | Learning receipts | Create unchanged | Ignore transient receipts and temporary files |
| `.claude/hooks/session-start.py` | Claude lifecycle | Create unchanged | Surface receipt and pending-proposal counts |
| `.claude/hooks/session-end.py` | Claude lifecycle | Create unchanged | Record a minimal session receipt |
| `.claude/skills/start-codebase/SKILL.md` | On-demand workflow | Create unchanged | Evidence-based repository briefing |
| `.claude/skills/finish-session/SKILL.md` | On-demand workflow | Create unchanged | Propose durable learnings without editing instructions |
| `.claude/skills/review-learnings/SKILL.md` | On-demand workflow | Create unchanged | Review-gated application of learning proposals |
| `.claude/settings.json` | Claude lifecycle | Create unchanged | Register session-start and session-end hooks |
| `.claude/rules/payments-migrations.md` | `services/payments/**` | Create | Forward-only migrations and local migration test |
| `.claude/rules/payments-generated.md` | `services/payments/src/generated/**` | Create | Exact generated-directory protection |
| `.claude/rules/storefront.md` | `apps/storefront/**` | Create | API-client invariant and stale Node 18 warning |

The narrow scopes avoid imposing payments or storefront conventions on unrelated `services/catalog`, `apps/admin`, or `packages/ui` work. The payment migration rule cannot be narrowed to a migration directory because that directory was not identified. The generated rule can be scoped to the exact confirmed directory.

Exact project-specific diff:

```diff
diff --git a/CLAUDE.md b/CLAUDE.md
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@
 # Project Instructions

-Keep repository-wide instructions concise. Put specialized guidance in the narrowest relevant `.claude/rules/` file or nested `CLAUDE.md`.
+Use Node 22 for repository work. Evidence: unverified developer-provided note citing `.nvmrc` and `.github/workflows/ci.yml`.
+
+Root validation commands are:
+
+- `npm run lint`
+- `npm test`
+- `npm run build`
+
+Evidence: unverified developer-provided note citing `package.json`. Pull-request CI runs lint and test; build runs on `main`. Evidence: unverified developer-provided note citing `.github/workflows/ci.yml`.
+
+Follow the path-scoped rules under `.claude/rules/` for payments and storefront work.

 Use the installed project skills for codebase onboarding, session reflection, and review-gated learning updates.
diff --git a/.claude/context/codebase-map.md b/.claude/context/codebase-map.md
--- a/.claude/context/codebase-map.md
+++ b/.claude/context/codebase-map.md
@@
 # Codebase Map

-Record evidence-backed architecture, entry points, development commands, and subsystem boundaries here.
+## Evidence status
+
+The supplied target was empty during bootstrap. Every repository-specific claim below is an unverified developer-provided note and must be checked against the cited path when repository contents become available.
+
+## Runtime and root commands
+
+- Use Node 22. Cited evidence: `.nvmrc` and `.github/workflows/ci.yml`.
+- `apps/storefront/README.md` reportedly says Node 18; this conflicts with `.nvmrc` and CI and is treated as stale.
+- Root commands reportedly defined by `package.json`:
+  - `npm run lint`
+  - `npm test`
+  - `npm run build`
+
+## Continuous integration
+
+- Pull requests run lint and test.
+- Builds run on `main`.
+- Cited evidence: `.github/workflows/ci.yml`.
+
+## Payments
+
+- Payment migrations are forward-only.
+- Test payment migrations with `npm run test:migrations` from `services/payments/`.
+- Cited evidence: `services/payments/README.md`.
+- `services/payments/src/generated/` is generated by `npm run generate` and must not be edited manually.
+- The note does not establish the generator command's required working directory or input paths; verify those in package manifests before running it.
+
+## Storefront
+
+- Storefront API calls must go through `apps/storefront/src/api/client.ts` to preserve authentication and retry behavior.
+- Evidence: unverified developer-provided note citing a maintainer review comment on PR #418.
+- The repository-wide Node 22 configuration supersedes the Node 18 claim in `apps/storefront/README.md`.
+
+## Other named areas
+
+- `services/catalog`
+- `apps/admin`
+- `packages/ui`
+
+No architecture or conventions are inferred for these unrelated areas.
+
+## Unknowns
+
+- All cited files and commands require verification because the supplied target was empty.
+- The payment migration directory is unknown.
+- The inputs and working directory for `npm run generate` are unknown.
+- PR #418's review comment is not present as a repository artifact.
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
+- Payment migrations are forward-only. Evidence: unverified developer-provided note citing `services/payments/README.md`.
+- For payment migration changes, run `npm run test:migrations` from `services/payments/`. Evidence: unverified developer-provided note citing `services/payments/README.md`.
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
+Do not edit files under `services/payments/src/generated/` by hand; regenerate them with `npm run generate`. Evidence: unverified developer-provided note naming this directory and command.
diff --git a/.claude/rules/storefront.md b/.claude/rules/storefront.md
new file mode 100644
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
+- Route all storefront API calls through `apps/storefront/src/api/client.ts` so authentication and retry behavior are preserved. Evidence: unverified developer-provided note citing a maintainer review comment on PR #418.
+- Treat the Node 18 requirement in `apps/storefront/README.md` as stale; use the repository's Node 22 configuration. Evidence: unverified developer-provided note citing `apps/storefront/README.md`, `.nvmrc`, and `.github/workflows/ci.yml`.
```

Sam’s suggestion to skip lint is excluded. It is a machine-specific, session-only workaround and does not pass the durability admission gate.

After approval, I will apply exactly the scaffold and diff above, run the installer’s validation mode, inspect the final diff for scope and secrets, and report any warnings or unverified claims. Claude Code should then be restarted because lifecycle hooks load at session startup.

Please explicitly approve these exact writes, or specify revisions.

## Before, after, and diff

Both manifests are empty. `diff -ruN` exited 0 with no output; the evaluator stopped at the approval checkpoint.
