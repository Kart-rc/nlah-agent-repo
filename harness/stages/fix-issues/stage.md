---
id: fix-issues
summary: "For each issue: create an isolated git worktree and branch in the target repo, execute that issue's fix plan, verify, and commit to the issue branch."
producer: builder
inputs:
  - name: fix_plan
    description: "Per-issue fix plan (from fix-plan)."
    format: markdown
    required: true
  - name: issue_manifest
    description: "Machine-readable issue list with slugs, branches, and acceptance criteria (from issue-intake)."
    format: json
    required: true
  - name: target_repo
    description: "Path to the codebase to fix. Worktrees are created under <target_repo>/.worktrees/."
    format: path
    required: true
  - name: base_branch
    description: "Branch to base every issue branch on. Defaults to the repo's current HEAD when absent."
    format: text
    required: false
outputs:
  - name: fix_summary
    file: fix_summary.md
    format: markdown
    description: "Per-issue record: worktree, branch, steps executed with verbatim verification output, commits, status fixed|blocked with evidence."
  - name: fix_manifest
    file: fix_manifest.json
    format: json
    description: "Machine-readable results: [{id, slug, branch, worktree_path, base_ref, status: fixed|blocked, commits, files, blocker}]."
acceptance_criteria:
  - "Every issue in issue_manifest.json has a dedicated worktree at <target_repo>/.worktrees/<slug> on branch fix/<slug> created from the base ref, recorded in fix_manifest.json with its absolute worktree_path; .worktrees/ is listed in the repo's .git/info/exclude."
  - "Every issue ends with status fixed or blocked: fixed means every plan step for that issue executed with its verification command's verbatim output recorded and passing; blocked states precisely what blocks, what was attempted, and which acceptance criteria remain unmet."
  - "All changes for an issue are committed only to that issue's branch, in commits whose messages reference the issue id; nothing is committed to the base branch, and nothing is pushed to any remote."
  - "The primary working tree of target_repo is left untouched: fix_summary.md records fenced 'git -C <target_repo> status --porcelain' output showing it clean, and 'git worktree list' output showing every issue worktree."
  - "Every behavior change carries a new or updated test on its issue branch, or fix_summary.md explains per issue why testing was infeasible."
  - "No secrets, credentials, or sensitive data appear in code, commits, or logged output."
default_validators:
  - uses: validators/completeness-check
    with:
      extra_check: "fix_manifest.json and fix_summary.md agree on every issue's status, branch, and commit list; every issue id from issue_manifest.json appears in both."
  - uses: validators/red-team
    with:
      focus: "secrets in commits, changes leaking onto the wrong branch or into the primary working tree, worktrees created outside <target_repo>/.worktrees/"
knowledge_slots: [org-context]
skill_refs:
  - skillpacks/addyosmani/git-workflow-and-versioning
  - skillpacks/addyosmani/incremental-implementation
  - skillpacks/addyosmani/test-driven-development
permissions:
  writes: [own_artifact_dir, target_repo]
---

# Fix Issues

## Purpose

The batch counterpart of implement, and the only stage that changes the
target repo in a batch-fix run. Each issue gets its own worktree and branch
so fixes stay isolated from each other and from the primary working tree;
this contract explicitly directs the worktree creation and the per-branch
commits that make that isolation real. Nothing is ever pushed.

## Procedure

1. Read the fix plan, the issue manifest, and every attached practice skill
   before writing any code.
2. Add `.worktrees/` to `<target_repo>/.git/info/exclude` (a local-only
   ignore — never a tracked-file change) so the primary tree's `git status`
   stays clean.
3. Resolve the base ref: the `base_branch` input when provided, else the
   repo's current HEAD. Record it.
4. Per issue, in the fix plan's declared cross-issue order:
   a. `git -C <target_repo> worktree add .worktrees/<slug> -b fix/<slug>
      <base_ref>` — the slug and branch come from the issue manifest.
   b. Execute that issue's plan steps with the worktree as working
      directory. Per step: make the change, run the step's `Verify:`
      command inside the worktree, record its verbatim output.
   c. Write or update tests with each behavior change (test-driven where
      the attached skill directs).
   d. Commit to the issue branch as coherent steps land, with messages
      referencing `ISS-<n>`.
   e. A failing verification that cannot be fixed within the plan marks the
      issue `blocked` — record what blocks, what was attempted, and which
      acceptance criteria remain unmet, then move on to the next issue. One
      blocked issue never abandons the batch.
5. Maintain `fix_manifest.json` as you go.
6. Finish with the proof block: fenced `git -C <target_repo> status
   --porcelain` output (clean) and `git worktree list` output (every issue
   worktree present).

## Output format constraints

`fix_summary.md` sections in order: `# Fix Summary`, `## Base ref`,
`## Issues` (one `### ISS-<n>` subsection per issue: `Status:`, `Worktree:`,
`Branch:`, `Commits:`, `Steps:` with fenced verification command + verbatim
output per step, `Deviations:` — "none" if none), `## Main tree proof`
(the fenced `git status --porcelain` and `git worktree list` outputs),
`## Knowledge gaps`. `fix_manifest.json`: JSON array of `{"id", "slug",
"branch", "worktree_path", "base_ref", "status", "commits", "files",
"blocker"}` where `status` is `fixed` or `blocked` and `blocker` is null
for fixed issues.

## Knowledge consumption

- `org-context`: coding standards, commit-message conventions, or internal
  library docs if attached; otherwise follow the target repo's own
  conventions and note assumptions under `## Knowledge gaps`.

## Boundaries

- Do NOT push to any remote, ever.
- Do NOT commit to the base branch or modify the primary working tree.
- Do NOT merge issue branches into each other or into the base branch.
- Do NOT remove worktrees — verification and delivery need them in place.
- Do NOT redesign or expand an issue's scope — deviations from the plan are
  recorded under Deviations; a deviation that changes architecture means
  stop + summary (F4).
- Do NOT fix anything not in the issue manifest.

## Self-check before submitting

Per issue, re-run its full verification set inside its worktree and confirm
the recorded outputs are current. Confirm `git -C <target_repo> status
--porcelain` is empty, and per branch that `git log <base_ref>..fix/<slug>`
shows only that issue's commits. Scan every diff for secrets.

## Summary requirement

Write `summary.md` (≤200 words): fixed vs blocked counts, the riskiest diff
in the batch, and any cross-issue conflict encountered while executing.
