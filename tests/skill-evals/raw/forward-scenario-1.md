# Forward Scenario 1 Raw Evidence

## Run metadata

- Date: 2026-07-14 (America/New_York)
- Evaluator: `/root/forward_validation/forward_s1`
- Context: fresh child agent with `fork_turns:none`
- Evaluation root: `/private/tmp/claude-context-forward-s1.pjWrvM`
- Target: `/private/tmp/claude-context-forward-s1.pjWrvM/project`
- Skill: isolated copy at `/private/tmp/claude-context-forward-s1.pjWrvM/capability/SKILL.md`
- Prompt: Scenario 1 exact prompt from `tests/skill-evals/scenarios.md`, passed as a user-like instruction to use the isolated skill
- Isolation: only the scenario fixture and bootstrap skill directory were copied; repository tests, plans, design, baselines, and expected results were absent
- Response SHA-256 (verbatim payload below, before this evidence wrapper): `103719ffefad359c8adc25f9754eef7f000953538fb256f9617430cc33c830e5`

## Full evaluator response

I inspected the repository and reached the required approval checkpoint. No files have been changed.

The repository is a small Parcel Desk scaffold:

- `README.md` describes an internal shipment-support product with API, web, and shared-type areas.
- Node 22 is confirmed by both `.nvmrc` and `package.json`.
- The three source entry points contain only two name constants and one type alias.
- The README’s command descriptions conflict with the current `package.json`: `dev`, `test`, and `lint` only echo markers.
- CI declares `npm test` and `npm run lint`, but `.github/workflows/ci.yml` contains no checkout or Node setup steps.
- Git status/history could not be inspected because this directory is not a Git repository.
- Safe baseline checks succeeded, but only as placeholders:
  - Local runtime: Node `v24.2.0`, which does not match the repository’s Node 22 requirement.
  - `npm test` printed `run-tests`.
  - `npm run lint` printed `run-lint`.
  - `npm run dev` printed `start-workspaces`.

The deterministic installer dry-run reported:

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

## Exact proposed write map

All paths are repository-relative.

- `CLAUDE.md`
  - Scope: repository-wide.
  - Evidence: `README.md`, `.nvmrc`, `package.json`.
  - Action: create from the scaffold, then minimally replace its boilerplate with the exact project-specific content below.
  - Conflict: README commands currently describe behavior the manifest does not implement.

- `.claude/context/codebase-map.md`
  - Scope: on-demand repository orientation.
  - Evidence: `README.md`, `package.json`, `.nvmrc`, `.github/workflows/ci.yml`, `apps/api/src/index.ts`, `apps/web/src/index.ts`, `packages/shared/src/index.ts`.
  - Action: create from the scaffold, then minimally replace its placeholder with the exact map below.
  - Unknowns are explicitly retained rather than inferred.

- `.claude/rules/shared-boundary.md`
  - Scope: `packages/shared/**`.
  - Evidence: `README.md`.
  - Action: additional project-specific create using the exact diff below.
  - Conflict: none.

- `.claude/context/learnings/.gitignore`
  - Scope: local learning artifacts.
  - Action: create exactly as follows:
    ```text
    receipts/
    *.tmp
    ```

- `.claude/settings.json`
  - Scope: Claude Code lifecycle hooks.
  - Action: create with this exact JSON:
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

- `.claude/hooks/session-start.py`
  - Action: create byte-for-byte from the deterministic scaffold.
  - SHA-256: `7d13512461dbc579b5818162188a818a52e0f256eeb8af80ed11273231ddf197`
  - Behavior: emits counts of local receipts and pending learning proposals; does not edit the repository.

- `.claude/hooks/session-end.py`
  - Action: create byte-for-byte from the deterministic scaffold.
  - SHA-256: `f7e3d6928686a32a14ed31389bd8bf5dc978b04103060c649e31f740b97e61ec`
  - Behavior: atomically records a local session receipt under the ignored `receipts/` directory without overwriting an existing receipt.

- `.claude/skills/start-codebase/SKILL.md`
  - Action: create byte-for-byte from the deterministic scaffold.
  - SHA-256: `e531ecb035c6d935468382396ca6cce14034d211f3bb10402439893fa01a4227`
  - Behavior: produces a current, evidence-cited briefing and safely evaluates unprocessed receipts.

- `.claude/skills/finish-session/SKILL.md`
  - Action: create byte-for-byte from the deterministic scaffold.
  - SHA-256: `69de10bfb3217a88fd40e678925877492ea11d83f8fd75be9b25c39ce3e168e1`
  - Behavior: creates reviewable learning proposals but never edits instructions.

- `.claude/skills/review-learnings/SKILL.md`
  - Action: create byte-for-byte from the deterministic scaffold.
  - SHA-256: `efc9e77a1e6e23a514d59896917a12c7bda978a2dd08e26c00b6d87c717f6116`
  - Behavior: requires proposal-specific approval before applying any learned instruction.

There are no merge or preserve actions. Parent directories would only be created as needed for these tracked files.

## Exact project-specific diffs

`CLAUDE.md`:

```diff
--- /dev/null
+++ b/CLAUDE.md
@@
+# Parcel Desk
+
+Parcel Desk is documented as an internal shipment-support application. Treat
+`README.md` as the source for product responsibilities; the current source
+entry points are only scaffolds. See `.claude/context/codebase-map.md` for the
+evidence-backed orientation and current gaps.
+
+## Repository-wide guidance
+
+- Use Node.js 22. Both `.nvmrc` and `package.json` select that major version.
+- Inspect `package.json` before relying on development commands. `README.md`
+  advertises `npm run dev`, `npm test`, and `npm run lint`, but the current
+  scripts only print markers.
+- Keep `packages/shared` independent of both applications; follow
+  `.claude/rules/shared-boundary.md` when changing that package.
+- Keep broad guidance here and put subsystem-specific rules in the narrowest
+  matching `.claude/rules/` file or nested `CLAUDE.md`.
+
+## Claude Code workflows
+
+- Run `/start-codebase` at the beginning of unfamiliar work for a current,
+  source-cited briefing.
+- Run `/finish-session` after durable discoveries or corrections; it only
+  proposes instruction changes.
+- Use `/review-learnings` to approve, revise, defer, or reject pending proposals.
```

`.claude/context/codebase-map.md`:

```diff
--- /dev/null
+++ b/.claude/context/codebase-map.md
@@
+# Codebase Map
+
+Use this as orientation, then verify each claim against the cited source before
+changing code. Update this map when those sources or entry points materially
+change.
+
+## Purpose and current maturity
+
+- `README.md` describes Parcel Desk as an internal shipment-support
+  application. It assigns parcel inspection and retry requests to the web app,
+  and shipment state plus carrier-adapter calls to the API. These are documented
+  responsibilities, not proof of implemented runtime behavior.
+- `apps/api/src/index.ts` currently exports only the `apiName` constant.
+- `apps/web/src/index.ts` currently exports only the `webName` constant.
+- `packages/shared/src/index.ts` currently exports only the `ParcelId` type.
+
+## Runtime and commands
+
+- Use Node.js 22; `.nvmrc` contains `22` and `package.json` requires `22.x`.
+- `README.md` documents `npm install` as setup. Re-check the manifest and any
+  future lockfile before choosing an install command.
+- `package.json` currently defines `npm run dev` as
+  `echo start-workspaces`; it does not start the applications.
+- `package.json` currently defines `npm test` as `echo run-tests`; it does not
+  execute a test runner.
+- `package.json` currently defines `npm run lint` as `echo run-lint`; it does
+  not execute a linter.
+- `.github/workflows/ci.yml` declares `npm test` and `npm run lint` for pull
+  requests. The workflow currently shows no checkout or Node setup steps, so
+  verify CI viability before relying on it.
+
+## Layout and likely change points
+
+- `apps/api`: API ownership is documented in `README.md`; begin with
+  `apps/api/src/index.ts`, then search for concrete routes, state, and adapter
+  code before assuming a framework or adding a parallel entry point.
+- `apps/web`: support-console ownership is documented in `README.md`; begin
+  with `apps/web/src/index.ts`, then confirm the UI framework and boot path
+  before adding components.
+- `packages/shared`: shared domain types live at
+  `packages/shared/src/index.ts`. Follow
+  `.claude/rules/shared-boundary.md` for its dependency direction.
+- Root tooling changes begin in `package.json`; pull-request automation begins
+  in `.github/workflows/ci.yml`.
+
+## Confirmed boundary
+
+- Code under `packages/shared/**` must not import from either application.
+  Evidence: `README.md`.
+
+## Unknowns to verify before implementation
+
+- The inspected evidence does not establish an HTTP framework, UI framework,
+  persistence layer, carrier-adapter implementation, test runner, linter, or
+  workspace wiring.
+- Treat the README's command descriptions as intended workflow and
+  `package.json` as current executable behavior until they are reconciled.
```

`.claude/rules/shared-boundary.md`:

```diff
--- /dev/null
+++ b/.claude/rules/shared-boundary.md
@@
+---
+paths:
+  - "packages/shared/**"
+---
+
+# Shared package boundary
+
+Do not import from `apps/api` or `apps/web` within `packages/shared`.
+`README.md` defines this directory as shared domain types and explicitly says
+it must not import from either application.
```

If approved, I will apply only this map, run the installer validation, inspect the resulting diff for scope and secrets, and report any warnings or unverified claims. Claude Code must then be restarted because lifecycle hooks load at session startup.

Do you approve these exact writes?

## Before manifest

```text
2e5ad0a47937b49cfa03d937405f2c4ad0cf82149c8e79c47791146ae132bf18  apps/web/src/index.ts
324ae4e84562c217e460cfa1d0c52bc0f77ad2edb9fbafb48953fc61a20a5bbf  apps/api/src/index.ts
3aa1a713a802ce1dd4802ac533fa59b9442dd855ae698550477cc48007c20c25  package.json
5d66b6d860491807878706bac02778ab4629f18f30d96b2b0d09b2f9080a33e0  packages/shared/src/index.ts
7a95e3ece717fe541c29bf2d533b2b6964333ddcc88123578acb08a918441bb3  README.md
b5023082e64fa576489a0047e036a169a402999444bd7b34c2d60d0b944b633e  .github/workflows/ci.yml
f14b4987904bcb5814e4459a057ed4d20f58a633152288a761214dcd28780b56  .nvmrc
```

## After manifest

The after manifest is byte-for-byte identical to the before manifest.

## Fixture diff

```text
(no differences; `diff -ruN` exited 0)
```
