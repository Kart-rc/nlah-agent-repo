# runs/ — externalized run state

Every workflow run lives in its own directory here. Nothing in this directory
is committed (see `.gitignore`) — a trimmed example is committed at
`docs/examples/sample-run/` instead.

Layout (authoritative definition: `HARNESS.md` §4):

```
runs/<YYYYMMDD-HHMM-workflowid-slug>/
├── task_state.json          # resume anchor (schema: harness/schema/task-state.schema.json)
├── events.jsonl             # append-only audit trail: {ts, stage, event, detail}
├── request.md               # user request, verbatim
├── inputs.json              # resolved workflow-level inputs
├── workflow.lock.yaml       # frozen manifest incl. risk overlay
├── stages/<stage-id>/
│   ├── inputs.json          # input name → file path
│   ├── artifacts/           # producer outputs — validators read ONLY this
│   ├── summary.md           # ≤200 words — orchestrator reads ONLY this
│   ├── gate.json            # gate outcome per attempt
│   └── validation/attempt-<n>/<validator-id>.verdict.json
└── escalations/<stage-id>.md
```

To resume an interrupted run: tell Claude Code `resume run <run-id>`.
The orchestration loop is a pure function of `task_state.json` — passed stages
are never re-executed.
