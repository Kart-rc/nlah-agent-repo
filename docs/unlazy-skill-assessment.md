# Unlazy Skill Usefulness Assessment

## Decision

`unlazy` is sufficiently distinct to add as an additional practice skill. Its
value is narrow but concrete: it provides an executable, task-local completion
ledger for substantial standalone work. It should not be attached to NLAH's
shipped workflows by default because those workflows already provide stronger
orchestration and use different state, validation, and escalation semantics.

The integrated source is `unlazy` v2 from
<https://github.com/Leonxlnx/unlazy>, audited at commit
`ed9e8d2b5919698cf2c54bda270d507e10b69617`.

## Evaluation method

The assessment compared upstream `SKILL.md`, gate format, templates, and three
Node scripts against:

- the runtime charter and write boundaries in [`HARNESS.md`](../HARNESS.md);
- plan, implement, verify, and deliver stage contracts;
- the completeness, adversarial, and test-of-tests validators;
- planning, incremental implementation, testing, review, and shipping practice
  skills; and
- the guarantees explicitly absent from
  [standalone mode](using-skills-standalone.md#what-standalone-mode-does-not-provide).

Two fresh-context agents also received the same pressured completion scenario
(the prompt, rubric, and concise outcome record are preserved in
[`docs/evaluations/2026-08-21-unlazy-comparison.md`](evaluations/2026-08-21-unlazy-comparison.md)):
twelve promised outcomes, nine apparently complete, two only eyeballed, one
silently deferred, slow CI, remembered report counts, deadline pressure, and a
manager requesting immediate shipment. One agent used the current NLAH
skillset; one used upstream `unlazy`.

Both agents correctly refused to claim `12/12`. The meaningful difference was
mechanism: the NLAH-only agent could use full workflow artifacts and validators
but confirmed the practice library had no reusable per-outcome ledger/checker;
the `unlazy` agent created leaf and integration gates, executed them with the
bundled checker, remeasured report numbers, and made the deferred outcome
machine-visible. This supports addition for standalone work, not replacement of
the full harness.

## Capability comparison

| `unlazy` capability | Closest existing NLAH behavior | Overlap | Assessment |
|---|---|---|---|
| Task-local `GATES.md` / `gates/*.md` ledger | Stage acceptance criteria, `gate.json`, validator verdicts | Partial | NLAH tracks stages and attempts, not one evidence-bearing record per task outcome. |
| Executable `CHECK` / `EXPECT` evaluation | Plan `Verify:` lines and producer-run commands | None | Existing documents instruct agents to run checks; no reusable parser matches expected output and updates the criterion. |
| Automatic checkbox and evidence updates | Verbatim output written manually to change and verification reports | None | `gate-check.mjs` deterministically updates the ledger and returns non-zero while unmet work remains. |
| Fresh context per leaf | Fresh context per workflow stage and repair attempt | Partial | NLAH isolates stages; `unlazy` can isolate plan leaves inside a large standalone task. |
| Parent re-runs leaf checks | Independent verify stage and validator subagents | Partial | NLAH is stronger at independent judgment, but its orchestrator deliberately reads state/summaries rather than re-running producer checks itself. |
| Branch integration gates | Workflow dependencies plus verify/readiness stages | Partial | NLAH checks final integration; `unlazy` can add gates at every internal decomposition node. |
| Re-measure every final-report number | Delivery claims trace to prior artifacts | Partial | NLAH requires traceability but has no universal rule that each reported number is freshly measured. |
| Visible `ABANDON` entry | Bounded repair followed by abort/escalation | Partial, different | Useful for honest standalone handoff; it must not be interpreted as a passed NLAH acceptance gate. |
| Optional filesystem Stop hook | Protocol STOP at approvals or escalation | None | NLAH has no hook that blocks ending a standalone turn while a local ledger is unmet. |

## Why the skill is unique

Existing practice skills cover the right principles:

- `planning-and-task-breakdown` writes acceptance criteria and verification
  steps;
- `incremental-implementation` verifies each slice;
- `test-driven-development` proves changed behavior;
- `doubt-driven-development` challenges confident decisions; and
- `shipping-and-launch` checks release readiness.

`unlazy` does not replace those disciplines. It supplies the missing execution
primitive that binds their outcomes into one repeatable ledger. A shell command,
not an agent's memory, decides whether a runnable gate passes; evidence is
recorded at the decision point; an unchecked or evidence-free gate remains
visibly incomplete.

This is most useful precisely where
[`docs/using-skills-standalone.md`](using-skills-standalone.md) says the full
harness is absent: no automatic validators, repair loop, or externalized run
state. The skill gives that mode a lightweight completion floor without
pretending to recreate the whole harness.

## Compatibility limits

Attaching upstream `unlazy` unchanged to a full workflow would create conflicts:

1. **State location:** upstream writes root-level `GATES.md`, `PLAN.md`, and
   `gates/`; NLAH producers are constrained to their stage directories, with
   builder-only target-repository exceptions.
2. **Topology:** upstream orchestrated mode defines leaf subagents and branch
   gates; NLAH permits only the topology locked in `workflow.lock.yaml`.
3. **Completion semantics:** upstream treats a documented `ABANDON` as resolved
   for checker exit status; NLAH exhausts repair into explicit escalation or
   abort.
4. **Verification ownership:** upstream asks the parent to re-run leaf checks;
   NLAH separates producer, validator, and orchestrator responsibilities.
5. **Hook scope:** the optional hook scans process working-directory ledgers,
   not a specific NLAH run, and could block legitimate approval or escalation
   stops.
6. **Command execution:** `gate-check.mjs` runs ledger-authored commands through
   a shell. Those commands require the same permission and destructive-action
   review as direct shell execution.

Therefore the catalog marks the skill `ad hoc / standalone`; no workflow
manifest references it, and hook installation is never automatic.

## Source audit finding

The integration tests and independent review found three checker defects in
upstream commit `ed9e8d2`:
`gate-check.mjs GATES.md` discarded its first positional file when `--timeout`
was absent. `indexOf("--timeout")` returned `-1`, and the filter still excluded
index `tIdx + 1` (`0`). The parser also treated structurally invalid ledgers as
complete, and evidence capture could discard the output that actually matched
`EXPECT`. The vendored copy applies focused fixes: positional arguments are
retained, malformed ledgers return exit code 2 before checks execute, and the
deciding match is recorded, including matches late in long lines. Regression
tests cover each behavior. References, templates, and the other scripts remain
aligned with the pinned source; the pack README records every local adaptation.

## Conclusion

Add the skill. It is not a new full-harness control plane; it is a useful
standalone completion tool with an evidence-bearing ledger and deterministic
checker that the existing practice library does not otherwise contain.
