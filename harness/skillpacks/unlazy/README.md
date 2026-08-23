# Skill Pack: unlazy (vendored)

Vendored anti-premature-completion discipline for substantial standalone work.
The pack contributes one skill, `unlazy`, whose task-local gate ledger and
executable checks make incomplete outcomes and unsupported completion claims
visible.

- **Contents:** 1 skill, `unlazy`
- **Harness reference:** `skillpacks/unlazy/unlazy`
- **Default attachment:** none — ad hoc / standalone only
- **Runtime:** Node.js 16+ for the bundled scripts

## Source and version

- **Upstream:** <https://github.com/Leonxlnx/unlazy>
- **Vendored commit:** `ed9e8d2b5919698cf2c54bda270d507e10b69617`
- **Upstream release:** v2.0.0
- **License:** MIT; preserved in [`LICENSE`](LICENSE)

The executable package includes upstream `SKILL.md`, `references/`, `scripts/`,
and `templates/`. The NLAH copy has four audited adaptations:

1. `SKILL.md` keeps the required `name` and rewrites `description` as a concise
   trigger-only field. The upstream `license` and `metadata` values are
   recorded here instead.
2. `gate-check.mjs` preserves the first positional file argument when
   `--timeout` is absent. Upstream commit `ed9e8d2` computes the missing timeout
   value's index as `0` when `indexOf("--timeout")` returns `-1`, accidentally
   filtering out that file and reporting “no gate files found.”
3. `gate-check.mjs` fails closed on empty ledgers, duplicate gate IDs, missing
   evidence fields, and invalid abandonment lines, and records the output that
   actually satisfied `EXPECT` rather than unrelated trailing output. Its
   bounded evidence window retains matches that occur late in a long line.
4. The automatically loaded `SKILL.md` warns that ledger checks execute through
   a shell. `LICENSE` and `SOURCE.md` are duplicated inside the installable
   skill directory so personal-install mode retains license and provenance.

The references, templates, and other scripts remain identical to the pinned
source. `tests/test_unlazy_skillpack.py` covers the local checker changes,
installation layout, and documented `gate-check.mjs GATES.md` invocation.

## Why this is additional rather than redundant

NLAH's full workflows already provide stronger stage-level controls: persisted
run state, fresh producer and validator contexts, independent blocking gates,
bounded repair, and escalation. Existing practice skills also cover planning,
incremental implementation, testing, and review.

The current library does not otherwise provide a reusable per-outcome ledger
with a bundled command that executes `CHECK` lines, evaluates `EXPECT`, records
evidence, and returns a failing status while work remains incomplete. That
mechanism is useful specifically in standalone mode, where the repository
documents that full harness guarantees are absent. See the detailed
[assessment](../../../docs/unlazy-skill-assessment.md).

## NLAH usage boundary

Do not attach this skill to a shipped workflow by default. Upstream orchestrated
mode defines its own plan tree, subagent dispatch, integration gates, and
abandonment semantics; those must not override the locked topology, write
boundaries, validators, repair loops, or escalation rules in `HARNESS.md`.

Use `unlazy` directly for substantial standalone work when task-local evidence
is valuable but a full NLAH run is unnecessary. If the work needs risk routing,
independent validation, approval gates, resumability, or bounded escalation,
use the NLAH workflow instead.

The optional Stop hook is included for source completeness but is never
installed by this pack. Installing it changes Claude Code behavior and requires
the user's explicit permission.

## Updating the vendored copy

1. Fetch upstream and select an explicit commit.
2. Review its license, skill body, references, templates, and every script.
3. Replace only the runtime files listed above.
4. Reapply the trigger-only two-field frontmatter adaptation.
5. Update the pinned commit and release in this README.
6. Run `tests/test_unlazy_skillpack.py`, Node syntax checks, the full test
   suite, and `python3 scripts/harness_lint.py`.
