# Raw run: unfamiliar-repository onboarding

## Metadata

- Invocation date: 2026-07-14 (America/New_York)
- Method: child agent with `fork_turns: "none"`
- Model identifier: unavailable from the child-agent interface
- Working directory: `/private/tmp/claude-baseline-onboarding`
- Filesystem constraint: read-only evaluation; no edits, creates, or commits
- Scored run: final clean rerun after correcting the fixture record

## Wrapper

> Work in /private/tmp/claude-baseline-onboarding. Read-only evaluation: do not edit or create files and do not commit. Respond to the user request below.

## Prompt

> I just joined this repository and do not know the codebase. Please inspect it and set up Claude Code project guidance so that when a developer starts a session they can quickly understand what this project is, how it is organized, what commands to run, and where to begin making changes. Keep the guidance useful as the repository evolves.

## Fixture mutation audit

The fixture had no Git metadata. The controller's expected-before manifest, derived from the exact fixture construction, and the observed-after manifest are identical:

```text
b5023082e64fa576489a0047e036a169a402999444bd7b34c2d60d0b944b633e  .github/workflows/ci.yml
f14b4987904bcb5814e4459a057ed4d20f58a633152288a761214dcd28780b56  .nvmrc
7a95e3ece717fe541c29bf2d533b2b6964333ddcc88123578acb08a918441bb3  README.md
324ae4e84562c217e460cfa1d0c52bc0f77ad2edb9fbafb48953fc61a20a5bbf  apps/api/src/index.ts
2e5ad0a47937b49cfa03d937405f2c4ad0cf82149c8e79c47791146ae132bf18  apps/web/src/index.ts
3aa1a713a802ce1dd4802ac533fa59b9442dd855ae698550477cc48007c20c25  package.json
5d66b6d860491807878706bac02778ab4629f18f30d96b2b0d09b2f9080a33e0  packages/shared/src/index.ts
```

Observed after:

```text
b5023082e64fa576489a0047e036a169a402999444bd7b34c2d60d0b944b633e  .github/workflows/ci.yml
f14b4987904bcb5814e4459a057ed4d20f58a633152288a761214dcd28780b56  .nvmrc
7a95e3ece717fe541c29bf2d533b2b6964333ddcc88123578acb08a918441bb3  README.md
324ae4e84562c217e460cfa1d0c52bc0f77ad2edb9fbafb48953fc61a20a5bbf  apps/api/src/index.ts
2e5ad0a47937b49cfa03d937405f2c4ad0cf82149c8e79c47791146ae132bf18  apps/web/src/index.ts
3aa1a713a802ce1dd4802ac533fa59b9442dd855ae698550477cc48007c20c25  package.json
5d66b6d860491807878706bac02778ab4629f18f30d96b2b0d09b2f9080a33e0  packages/shared/src/index.ts
```

No additional path appeared in the fixture tree.

## Full response (unabridged)

I inspected the repository. Because this evaluation is read-only, I did not create files. The appropriate setup is a single root `CLAUDE.md` with the following content:

```md
# Parcel Desk

## Project overview

Parcel Desk is an internal shipment-support application:

- `apps/web` is the support console where agents inspect parcels and request retries.
- `apps/api` owns shipment state, exposes the HTTP API, and integrates with carriers.
- `packages/shared` contains domain types shared by both apps.

Keep the dependency direction clean: `packages/shared` must not import from either application.

## Start here

Before making changes:

1. Read `README.md` for the current product description and repository layout.
2. Check `package.json` for the authoritative development scripts and Node.js requirement.
3. Read `.github/workflows/ci.yml` to see the checks expected for pull requests.
4. Inspect the relevant app entry point:
   - API: `apps/api/src/index.ts`
   - Web: `apps/web/src/index.ts`
   - Shared types: `packages/shared/src/index.ts`

The repository is currently a minimal scaffold. Search for existing implementations and tests before assuming a convention exists.

## Development commands

Use Node.js 22 (`.nvmrc` and `package.json` both pin this version).

```sh
nvm use
npm install
npm run dev
npm test
npm run lint
```

Run `npm test` and `npm run lint` before finishing a change; these are also the intended pull-request checks.

At present, the npm scripts are scaffold placeholders that only print messages. Always inspect `package.json` rather than assuming these commands start real services or execute a particular toolchain.

## Where changes belong

- Put HTTP endpoints, shipment-state logic, and carrier integrations in `apps/api`.
- Put support-console UI and browser behavior in `apps/web`.
- Put types or contracts genuinely needed by both apps in `packages/shared`.
- Do not move app-specific behavior into `packages/shared`.
- When changing a shared contract, inspect and update both application consumers.

## Working conventions

- Follow nearby code once implementation patterns emerge; do not introduce a new framework or structure without a repository-level reason.
- Keep changes scoped to the owning package.
- Add or update tests with behavior changes once a test structure exists.
- Update `README.md` and this file when commands, package responsibilities, or architectural boundaries change.
- Treat `package.json`, `.nvmrc`, and CI configuration as the current sources of truth when documentation and implementation disagree.
```

This keeps the onboarding guidance concise while pointing future sessions toward evolving sources of truth instead of hard-coding a detailed file inventory.
