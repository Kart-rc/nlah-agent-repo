---
id: test-of-tests
summary: "Mutation-style test-quality gate: deliberately broken code must make the suite fail; a test suite that cannot fail cannot verify."
agent: test-auditor
parameters:
  - name: target_repo
    description: "Root of the repository whose tests are audited — bind `workflow:target_repo`. The stage's artifacts list changed paths relative to this root; without it there is nothing to copy, mutate, or run."
    required: true
  - name: focus
    description: "Optional narrowing of the mutation target (e.g. 'the auth module only')."
    required: false
  - name: min_mutations
    description: "Minimum semantic mutations to attempt on changed behavior. Default 3."
    required: false
verdict_file: verdict.json
---

# Test of Tests

## Mission

Gate the verification tooling itself. Every other validator trusts that a
green test run means something; this one checks that trust. It seeds
deliberate faults into the changed code and demands that the test suite
notices. A suite that stays green over broken code is rejected — before its
false signal can certify anything downstream.

## Method

1. From the stage's artifacts (`diff_manifest.json`, `change_summary.md`),
   enumerate the changed behavior and the tests that claim to cover it,
   resolving every listed path against the `target_repo` parameter.
   Honor the `focus` parameter if given.
2. Run those tests once, unmutated, as a baseline. A failing or erroring
   baseline is itself a `fail` — mutations on top of a red baseline prove
   nothing.
3. Select at least `min_mutations` (default 3) small semantic mutations on
   the changed code: invert a conditional, off-by-one a boundary, delete a
   guard or validation, swap a return value. Prefer mutations on the
   behavior the acceptance criteria name.
4. For each mutation: apply it in a throwaway copy of the repo at
   `target_repo` (or a git-revertible edit that is fully restored — see the
   persona's hard rules), run the relevant tests, and record kill (tests
   fail) or survive (tests pass) with verbatim output.
5. Restore everything and prove the tree is clean before returning.
   If fewer than `min_mutations` mutations were feasible, say why in the
   verdict — an unexplained shortfall is a `fail`.

## Verdict format

Return, as your final message, verdict JSON matching
`harness/schema/task-state.schema.json` → `$defs/verdict`. `fail` if any
mutation on changed behavior survives (`major`; `blocker` when the surviving
mutation sits on a security or data-integrity path) or if the mutation quota
was missed without a stated reason. Each finding's `evidence` carries the
exact mutation diff and the passing test output; its `suggested_fix` names
the missing or weak test case. The summary quotes the restoration proof
(`git status --porcelain` output).

## Independence rules

You receive artifact paths, acceptance criteria, and parameters — nothing
else. Never read `summary.md`, other stages' directories, or anything
describing how the code was produced. Judge the suite by what it catches,
not by what its authors intended. Never leave a persisted change in the
target repo.
