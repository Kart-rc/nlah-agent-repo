# Intake summary

Produced `artifacts/requirements.md` for the request: add a hello CLI script under `examples/toy-cli/` that greets a person by name. Verified the repo has no `examples/` directory today, so the deliverable is wholly new.

Most consequential requirements: (1) invoking the CLI with a name argument prints `Hello, <name>!` to stdout and exits 0, with the name interpolated; (2) all files live strictly under `examples/toy-cli/`; (3) a bare invocation must be deterministic and non-crashing (usage error or documented default — either passes).

Assumptions most likely to be challenged: the name arrives as a command-line argument rather than an interactive prompt, and the exact wording `Hello, <name>!` is pinned purely for testability (the request only says "greet by name"). Both are surfaced with rejected alternatives.

Open questions for downstream: preferred missing-name behavior (usage error vs default greeting); whether runtime prerequisites may be documented or must already exist in a fresh checkout; whether an automated test should ship with the example. None block design, since requirement 3 admits both missing-name behaviors. No knowledge adapters were attached; what I would have asked org-context and personal-notes is recorded under Knowledge gaps.
