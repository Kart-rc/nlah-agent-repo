# Failure Taxonomy

Named failure classes with detection and recovery policy, per the NLAH model:
recovery is automated where safe, escalated where judgment is needed, and
always auditable (every transition lands in `events.jsonl`).

| Class | Name | Definition | Detected by | Recovery policy |
|---|---|---|---|---|
| **F1** | Contract violation | Required output missing, malformed, or an input binding unresolvable | completeness-check (first gate); the orchestrator at resolve time | Producer-side: counts against the repair budget; the repair prompt is the mechanical checklist of missing items. Orchestrator-side (unresolvable binding): halt the run and report — that is a harness bug, not a repair case |
| **F2** | Validation rejection | Artifact exists and conforms, but fails substantive acceptance criteria | adversarial-reviewer, red-team, persona-reviewer verdicts | Bounded repair loop: fresh producer context + prior artifacts + failure verdicts, up to `max_repair_attempts` (default 2), then F5 |
| **F3** | Tool/environment failure | MCP server down, command errors, network denial — not the producer's fault | Producer notes in summary; validator emits verdict `error` | Retry once. Persistent → escalate as an *environment* issue. Does NOT consume the repair budget |
| **F4** | Scope drift | Artifact does more or other than its contract (design contains code; implement redesigns) | Validators treat the stage's `Boundaries` section as implicit criteria | Repair prompt re-anchors to the contract and boundaries; second occurrence in the same stage → escalate with a drift note |
| **F5** | Budget exhaustion | Repair attempts exhausted without a passing gate | Gate loop counter | Apply the gate's `on_exhaustion`: `escalate` (default) writes `escalations/<stage>.md` and halts resumable; `abort` ends the run |
| **F6** | Knowledge adapter failure | Attached adapter unreachable, unqueryable, or empty | Producer records under `## Knowledge gaps` | Adapter `failure_mode: degrade` → proceed; gaps stay visible to validators and readers. `failure_mode: block` or attachment `required: true` → escalate |
| **F7** | Routing failure | No workflow matches the request, or multiple match ambiguously | Router confidence rubric (Step 4) | Ambiguous → ask the user to choose among the plausible matches. No match → offer workflow-composer with a suggested composition. Never guess-and-run |

## Notes

- **F1 vs F2** is the reason completeness-check always runs first: F1 failures
  are cheap to detect and produce mechanical repair instructions; F2 failures
  deserve the full attention of expensive validators only on artifacts that
  actually conform.
- **F3 must never masquerade as F2.** A validator that cannot run its checks
  (missing tool, unreachable path) emits verdict `error`, not `fail`; the
  orchestrator retries once and then escalates as an environment issue without
  burning the producer's repair budget.
- **F4 is contained by architecture** as well as by gates: producers only
  write to their own artifact directory (builder additionally to the target
  repo), so drift is visible in exactly one place.
- **Approval checkpoints are not failures.** `awaiting_approval` is a normal
  run status produced by the risk policy; declining approval typically leads
  to composer edits or an aborted run by human choice.
