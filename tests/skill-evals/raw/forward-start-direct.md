> **EXCLUDED FROM FINAL SCORING** — The copied fixture contained generated hook bytecode. Retained only as superseded audit evidence.

# Direct Start-Codebase Raw Evidence

## Run metadata

- Date: 2026-07-14 (America/New_York)
- Evaluator: `/root/forward_validation/forward_start_direct`
- Context: fresh child agent with `fork_turns:none`
- Evaluation root: `/private/tmp/claude-context-forward-start.FTY6nE`
- Target: disposable preinstalled project containing only the scaffold and sanitized Parcel Desk fixture
- Skill: installed `.claude/skills/start-codebase/SKILL.md`
- Isolation: no source-repository tests, plans, design, baselines, rubric, prior output, or expected answer
- Response SHA-256 before this wrapper: `9da9257fbe2ee40acec18c5b5ef648511b67ccb9d5fd9cb37c03f0346c8d5348`

## Exact evaluator wrapper and prompt

> Work only inside `/private/tmp/claude-context-forward-start.FTY6nE`; do not inspect or reference any other repository or conversation. Treat `/private/tmp/claude-context-forward-start.FTY6nE/project` as the preinstalled target repository. Use the installed start-codebase skill at `/private/tmp/claude-context-forward-start.FTY6nE/project/.claude/skills/start-codebase/SKILL.md` and follow it faithfully for this user request:
>
> I am starting work on the API retry behavior in this unfamiliar repository. Please give me the current developer briefing so I know the applicable instructions, architecture, safe commands, likely change points, pending learnings, unknowns, and best first step.
>
> Return your full user-facing response when complete.

## Full evaluator response

## Worktree and recent changes

Git metadata is absent, so worktree status, branch, authorship, and recent commits cannot be determined. I made no changes.

## Applicable instructions

- Use Node.js 22 and run `npm test` plus `npm run lint` before completion: [CLAUDE.md](/private/tmp/claude-context-forward-start.FTY6nE/project/CLAUDE.md:3).
- Use the installed project skills for onboarding and learning updates: [CLAUDE.md](/private/tmp/claude-context-forward-start.FTY6nE/project/CLAUDE.md:5).
- `.nvmrc` and the package engine also specify Node 22: [.nvmrc](/private/tmp/claude-context-forward-start.FTY6nE/project/.nvmrc:1), [package.json](/private/tmp/claude-context-forward-start.FTY6nE/project/package.json:4).
- No `AGENTS.md`, nested `CLAUDE.md`, or `.claude/rules/` instructions exist. No instruction conflicts were found.

## Architecture and entry points

- This is a private Node package with no declared dependencies: [package.json](/private/tmp/claude-context-forward-start.FTY6nE/project/package.json:1).
- The implemented retry surface is a single exported function, `shouldRetry(attempt)`, which currently returns `attempt < 3`: [retry.ts](/private/tmp/claude-context-forward-start.FTY6nE/project/apps/api/src/retry.ts:1).
- The only observed dependency direction is test → retry module through a relative import: [retry.test.ts](/private/tmp/claude-context-forward-start.FTY6nE/project/apps/api/test/retry.test.ts:1).
- The README says `apps/api` owns retry policy and `apps/web` is an operator console: [README.md](/private/tmp/claude-context-forward-start.FTY6nE/project/README.md:3). The API ownership matches the files present, but no `apps/web` implementation exists in this snapshot.
- No production API entry point or consumer of `shouldRetry` was found.
- The codebase map is only a placeholder and supplies no verified architecture: [codebase-map.md](/private/tmp/claude-context-forward-start.FTY6nE/project/.claude/context/codebase-map.md:1).

## Commands and baseline results

The documented commands are `npm test` and `npm run lint`: [README.md](/private/tmp/claude-context-forward-start.FTY6nE/project/README.md:5).

- `node --version` → `v24.2.0`, which does not match the required Node 22 environment.
- `npm test` → exit 0, printing `unit-tests`.
- `npm run lint` → exit 0, printing `lint-check`.

These are placeholder echo scripts, not meaningful unit-test or lint checks: [package.json](/private/tmp/claude-context-forward-start.FTY6nE/project/package.json:5). In particular, the existing test-shaped TypeScript file is not executed. I did not install packages, switch runtimes, access the network, or run write/fix commands.

## Likely change points

- Policy implementation: [apps/api/src/retry.ts](/private/tmp/claude-context-forward-start.FTY6nE/project/apps/api/src/retry.ts:1).
- Boundary tests: [apps/api/test/retry.test.ts](/private/tmp/claude-context-forward-start.FTY6nE/project/apps/api/test/retry.test.ts:1).
- Test/lint tooling, if the task includes making checks executable: [package.json](/private/tmp/claude-context-forward-start.FTY6nE/project/package.json:5).

The current comparison retries attempts below `3`. By inference, it also accepts zero, negative, and fractional attempts; whether that is intentional is unknown.

## Pending learnings

One pending, unapproved proposal suggests confirming the retry limit before adding an `apps/api/**` rule: [2026-07-14-review-retry-limit.md](/private/tmp/claude-context-forward-start.FTY6nE/project/.claude/context/learnings/pending/2026-07-14-review-retry-limit.md:1). It explicitly must not be applied without developer approval.

No unprocessed learning receipts exist, so none were claimed or processed.

## Unknowns and recommended first step

Unknowns include:

- Whether `attempt` is zero- or one-based.
- Whether “3” means three retries or three total attempts.
- Which failures/statuses are retryable.
- Required backoff, jitter, idempotency, cancellation, and input-validation behavior.
- Actual runtime consumers and the intended test framework.

Best first step: confirm the retry contract—especially attempt numbering and retries versus total attempts—then encode boundary cases around `2` and `3` in an executable test harness before modifying `shouldRetry`. Also run subsequent work under Node 22; the current shell is on Node 24.

## Before, after, and diff

The after manifest is byte-for-byte identical to the before manifest. `diff -ruN` exited 0; the briefing made no target mutation.
