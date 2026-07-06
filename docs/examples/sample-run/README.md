# Sample run (trimmed snapshot)

A trimmed, committed snapshot of a real completed SDLC run
(`20260706-0307-sdlc-toy-cli`: "add a hello CLI that greets a person by name",
classified new-feature/low). Full runs live under `runs/` and are gitignored;
this snapshot preserves the illustrative pieces:

- `task_state.json` — the completed resume anchor (all 6 stages `passed`;
  note `deliver.attempts: 2`).
- `workflow.lock.yaml` — the frozen manifest (low risk → no-op overlay).
- `events.jsonl` — the full audit trail, including the `orchestrator_reset`
  resume test after stage 3 and the deliver gate failure → repair → pass.
- `stages/intake/` — a passing first gate: summary, gate.json, and the
  completeness verdict.
- `stages/deliver/` — **the repair loop in action**: `gate.json` shows
  attempt 1 `completeness-check: fail` (the release-gate checklist item
  "Monitoring exists" was silently unaddressed) → `outcome: repair`, then
  attempt 2 `pass`. Both verdicts are included; compare the attempt-1
  failure findings with the attempt-2 confirmation.

The delivered change itself is committed at `examples/toy-cli/`.
