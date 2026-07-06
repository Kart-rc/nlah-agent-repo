# NLAH Magnetic Harness

- Read `HARNESS.md` first — it is the constitution. Its orchestration protocol is the only definition of how workflows run; never restate or improvise it.
- Any delivery request (feature, bug fix, proposal, ...) routes through the `agentic-delivery-router` skill. Creating or modifying workflows goes through `workflow-composer`.
- During a run, write only inside `runs/<run-id>/` — except `builder`-persona stages, which modify the target repo as their stage contract directs.
- After editing anything under `harness/`, run `python3 scripts/harness_lint.py` and fix findings before proceeding.
