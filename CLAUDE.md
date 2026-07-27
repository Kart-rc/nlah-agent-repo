# NLAH Magnetic Harness

- Read `HARNESS.md` first — it is the constitution. Its orchestration protocol is the only definition of how workflows run; never restate or improvise it.
- Any delivery request (feature, bug fix, proposal, ...) routes through the `agentic-delivery-router` skill. Creating or modifying workflows goes through `workflow-composer`.
- When the ask is *which* path to take rather than delivery work itself ("which skills should I use", "I don't want a full workflow", "what's here"), `harness-navigator` answers with one concrete command; it executes nothing and never overrides the two rules above.
- During a run, write only inside `runs/<run-id>/` — except `builder`-persona stages, which modify the target repo as their stage contract directs.
- After editing anything under `harness/`, run `python3 scripts/harness_lint.py` and fix findings before proceeding.
