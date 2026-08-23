# Unlazy Skill Integration Design

## Context

The NLAH harness already prevents premature completion inside full workflows:
stage contracts require evidence, validators run in fresh contexts, failed gates
trigger repair or escalation, and run state is persisted under `runs/<run-id>/`.
Its standalone skill mode intentionally does not provide those enforcement
guarantees.

Upstream `unlazy` v2 adds a smaller task-local completion mechanism:

- an acceptance ledger (`GATES.md` or `gates/*.md`);
- executable `CHECK` / `EXPECT` gates;
- automatic evidence capture and a non-zero status while gates remain unmet;
- leaf and integration ledgers for deep decomposition;
- explicit, visible abandonment instead of silently narrowing scope;
- final-report number remeasurement; and
- an optional Claude Code Stop hook.

Source: <https://github.com/Leonxlnx/unlazy>, pinned for this integration at
commit `ed9e8d2b5919698cf2c54bda270d507e10b69617` (MIT).

## Decision

Add `unlazy` as a ninth practice-skill pack and the harness's 48th practice
skill. Treat it as an ad hoc standalone discipline rather than attaching it to
any shipped workflow by default.

This placement preserves the useful part of the skill without creating a
second orchestration protocol inside NLAH. Full NLAH workflows remain governed
only by `HARNESS.md`; `unlazy` fills the documented standalone-mode gap where a
user wants stronger completion evidence without starting a full harness run.

## Alternatives considered

### Reject it as redundant

Rejected. Existing skills provide planning, incremental implementation, and
verification advice, but the repository has no reusable per-outcome ledger or
bundled command that executes checks and records evidence.

### Attach upstream `unlazy` to shipped workflows

Rejected. The upstream skill creates its own `PLAN.md`, gate tree, subagent
topology, and abandonment semantics. Those overlap or conflict with NLAH's
locked workflow manifest, run-directory write boundaries, independent
validators, and bounded escalation policy.

### Rewrite it as a harness-native validator

Deferred. A native executable-criteria validator could eventually reuse the
gate format, but that is a separate harness behavior change. It would require
schema, permission, security, and workflow decisions beyond adding the
requested skill.

## Package layout

```text
harness/skillpacks/unlazy/
├── LICENSE
├── README.md
└── unlazy/
    ├── LICENSE
    ├── SOURCE.md
    ├── SKILL.md
    ├── USAGE.md
    ├── references/
    ├── scripts/
    └── templates/
```

The executable skill directory contains runtime material plus an install-local
license and source record. Pack-level `README.md` records provenance, the
pinned commit, adaptations, and NLAH attachment policy. `USAGE.md` explains
standalone invocation, ledger location, the Node 16+ requirement, and why the
optional Stop hook is never installed automatically.

The vendored `SKILL.md` retains the upstream method but normalizes frontmatter
to the harness/Codex discovery contract (`name` and `description`). Attribution,
version, source, and license are preserved both at pack level and, for personal
installation, inside the executable skill directory.

## Integration boundaries

- Do not modify `HARNESS.md` orchestration semantics.
- Do not attach `unlazy` to any existing workflow manifest or stage default.
- Do not install or configure the Stop hook.
- Do not make an upstream `ABANDON` entry equivalent to a passed NLAH gate.
- Document that full harness runs should use their existing stage artifacts,
  validators, repair loops, and escalation instead.
- Preserve upstream checker behavior except for regression-tested, disclosed
  correctness hardening. Commands in a user/agent-authored ledger are shell
  commands and must remain within the active agent's normal permission boundary.

## Documentation changes

- Add an evidence-backed overlap and usefulness assessment.
- Add the pack to the skill catalog as `ad hoc / standalone`.
- Update README and standalone-guide pack/skill counts.
- Explain that `unlazy` strengthens standalone completion discipline but does
  not recreate risk routing, independent validators, or resumable workflow
  state.

## Verification design

Add a focused Python test module before vendoring the package. It must fail
while the package is absent, then prove:

1. required package files and upstream resources exist;
2. `SKILL.md` has valid `name` / `description` frontmatter and local links
   resolve;
3. provenance pins the audited upstream commit and preserves the MIT license;
4. `gate-check.mjs --status` reports an unchecked fixture as unmet;
5. running the checker executes a deterministic gate, checks the box, records
   evidence, and subsequently reports all gates met; and
6. malformed ledgers fail closed and deciding evidence is recorded;
7. install-local provenance and license files survive personal installation;
8. actual pack/skill counts are nine and 48; and
9. documentation and catalog entries expose the new skill without a workflow
   or stage-default attachment.

Final verification runs the focused test, the full test suite, harness lint,
Node syntax checks for every vendored script, and a clean diff/status audit.
