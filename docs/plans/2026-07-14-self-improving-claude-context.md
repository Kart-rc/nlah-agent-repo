# Self-Improving Claude Context Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a reusable Claude Code skill that installs a developer start walkthrough, lean layered instructions, and a review-gated session learning loop into any repository.

**Architecture:** A project-local bootstrap skill performs repository analysis and installs stable assets. Python standard-library scripts make installation and lifecycle hooks deterministic; Claude Code skills perform codebase understanding, learning admission, and developer-approved rule updates.

**Tech Stack:** Claude Code skills and hooks, Markdown, Python 3 standard library, `unittest`, JSON.

---

### Task 1: Establish skill-behavior baselines

**Files:**
- Create: `tests/skill-evals/scenarios.md`
- Create: `tests/skill-evals/baseline-results.md`

**Step 1: Write pressure scenarios**

Define at least three independent prompts that ask an agent without the new
skill to:

1. onboard a developer to an unfamiliar fixture repository;
2. create a layered `CLAUDE.md` setup from mixed project evidence; and
3. learn from a session where one durable correction is mixed with temporary
   task state and a secret-like value.

Each scenario must record observable success criteria, especially concise root
instructions, evidence citations, narrow rule scope, and approval before rule
mutation.

**Step 2: Run the scenarios without the skill**

Run each scenario in a fresh agent context with only the fixture and prompt.
Do not mention the intended architecture or expected failure.

Expected: at least one baseline omits an important behavior or edits rules
without a review gate.

**Step 3: Record the baseline verbatim**

Write the prompt, output summary, exact failure, and any rationalization to
`tests/skill-evals/baseline-results.md`.

**Step 4: Commit**

```bash
git add tests/skill-evals/scenarios.md tests/skill-evals/baseline-results.md
git commit -m "test: capture Claude context skill baselines"
```

### Task 2: Specify and test the bootstrap installer

**Files:**
- Create: `tests/test_bootstrap_claude_context.py`
- Create: `.claude/skills/bootstrap-claude-context/scripts/install.py`
- Create: `.claude/skills/bootstrap-claude-context/assets/project/CLAUDE.md`
- Create: `.claude/skills/bootstrap-claude-context/assets/project/.claude/settings.fragment.json`
- Create: `.claude/skills/bootstrap-claude-context/assets/project/.claude/context/codebase-map.md`
- Create: `.claude/skills/bootstrap-claude-context/assets/project/.claude/context/learnings/.gitignore`

**Step 1: Write failing installer tests**

Use `tempfile.TemporaryDirectory` and `subprocess.run` to specify:

```python
def test_dry_run_lists_writes_without_mutating_target(): ...
def test_install_creates_expected_project_scaffold(): ...
def test_install_merges_existing_settings_without_losing_keys(): ...
def test_reinstall_is_idempotent_and_preserves_user_files(): ...
def test_install_rejects_non_directory_and_unsafe_targets(): ...
```

The scaffold assertion must include the three installed skills, two hook
scripts, context directories, `CLAUDE.md`, and merged lifecycle hooks.

**Step 2: Run tests to verify RED**

Run:

```bash
python3 -m unittest -v tests.test_bootstrap_claude_context
```

Expected: FAIL because `install.py` and assets do not exist.

**Step 3: Initialize the bootstrap skill**

Run the available skill initializer for `bootstrap-claude-context` at
`.claude/skills/`, requesting `scripts,references,assets`. Remove placeholder
examples and keep only resources used by this capability.

**Step 4: Implement the minimal installer**

Implement these commands:

```text
install.py --target PATH --dry-run
install.py --target PATH --apply
install.py --target PATH --validate
```

Use `pathlib`, `json`, `shutil`, and atomic temporary-file replacement. Copy
missing stable assets, never overwrite existing instruction or skill files,
and merge only this capability's hook entries into `.claude/settings.json`.
Return a machine-readable summary of `create`, `merge`, `preserve`, and
`warning` actions.

**Step 5: Run tests to verify GREEN**

Run:

```bash
python3 -m unittest -v tests.test_bootstrap_claude_context
```

Expected: all installer tests PASS.

### Task 3: Implement lifecycle hooks test-first

**Files:**
- Modify: `tests/test_bootstrap_claude_context.py`
- Create: `.claude/skills/bootstrap-claude-context/assets/project/.claude/hooks/session-start.py`
- Create: `.claude/skills/bootstrap-claude-context/assets/project/.claude/hooks/session-end.py`

**Step 1: Write failing hook-contract tests**

Add tests specifying:

```python
def test_session_start_emits_concise_context_with_pending_counts(): ...
def test_session_start_tolerates_malformed_input(): ...
def test_session_end_writes_atomic_receipt_inside_project(): ...
def test_session_end_deduplicates_same_session(): ...
def test_session_end_rejects_cwd_outside_project(): ...
def test_session_end_never_writes_transcript_content(): ...
```

Pass hook JSON over stdin and set `CLAUDE_PROJECT_DIR` explicitly. Assert exit
code zero for malformed or unavailable optional state so lifecycle failures do
not block the developer.

**Step 2: Run tests to verify RED**

Run:

```bash
python3 -m unittest -v tests.test_bootstrap_claude_context
```

Expected: new hook tests FAIL because the hook assets do not exist.

**Step 3: Implement `SessionStart`**

Parse stdin defensively, count receipt and pending-proposal files under the
project, and emit JSON with `hookSpecificOutput.hookEventName` set to
`SessionStart` and concise `additionalContext`. Do not read transcript content
or modify the repository.

**Step 4: Implement `SessionEnd`**

Validate that the event working directory is within `CLAUDE_PROJECT_DIR`.
Atomically write one receipt per sanitized session identifier containing only
the session id, transcript path, cwd, end reason, and timestamp. Never include
transcript content. Treat duplicate events as success.

**Step 5: Run tests to verify GREEN**

Run:

```bash
python3 -m unittest -v tests.test_bootstrap_claude_context
```

Expected: all hook and installer tests PASS.

**Step 6: Commit**

```bash
git add .claude/skills/bootstrap-claude-context tests/test_bootstrap_claude_context.py
git commit -m "feat: add deterministic Claude context bootstrap"
```

### Task 4: Author the layered-context skills

**Files:**
- Create: `.claude/skills/bootstrap-claude-context/SKILL.md`
- Create: `.claude/skills/bootstrap-claude-context/references/layering.md`
- Create: `.claude/skills/bootstrap-claude-context/references/learning-admission.md`
- Create: `.claude/skills/bootstrap-claude-context/assets/project/.claude/skills/start-codebase/SKILL.md`
- Create: `.claude/skills/bootstrap-claude-context/assets/project/.claude/skills/finish-session/SKILL.md`
- Create: `.claude/skills/bootstrap-claude-context/assets/project/.claude/skills/review-learnings/SKILL.md`

**Step 1: Convert baseline failures into assertions**

For each baseline failure, add a direct instruction or acceptance check to the
smallest relevant skill. Do not add speculative rules that no baseline or
approved design requirement supports.

**Step 2: Write the bootstrap skill**

Require this sequence:

1. inspect existing agent instructions and repository evidence;
2. run installer dry-run;
3. propose the layered instruction map and exact writes;
4. obtain approval before applying;
5. apply the stable scaffold;
6. write only evidence-backed project rules; and
7. run installer validation and report restart requirements.

Keep detailed layer selection and learning admission criteria in the two
reference files.

**Step 3: Write `start-codebase`**

Require repository status, relevant instruction discovery, tooling and entry
point detection, architecture walkthrough with file evidence, safe baseline
checks, likely change points, and pending-proposal visibility. The output must
be a concise developer briefing rather than a repository dump.

**Step 4: Write `finish-session`**

Require evidence extraction from the session, rejection of temporary or secret
material, contradiction checks, narrow layer selection, and creation of a
pending proposal. Forbid direct instruction edits.

**Step 5: Write `review-learnings`**

Require per-proposal evidence validation, exact diff display, explicit developer
approval, minimal application, validation, and archival with disposition.

### Task 5: Validate and forward-test the skills

**Files:**
- Modify: `tests/skill-evals/baseline-results.md`
- Create: `tests/skill-evals/forward-results.md`
- Create: `scripts/validate_claude_context_skill.py`

**Step 1: Write failing structural validation tests**

Specify checks for:

- required skill frontmatter and valid lower-case names;
- root template below 200 lines;
- valid JSON settings fragment;
- hook asset existence and syntax;
- required proposal admission and approval language; and
- no placeholder markers or absolute source-machine paths.

Run:

```bash
python3 scripts/validate_claude_context_skill.py
```

Expected: FAIL until the validator and all authored resources are complete.

**Step 2: Implement the validator and reach GREEN**

Use only the Python standard library. Print every violation and exit nonzero
when any check fails.

Run:

```bash
python3 scripts/validate_claude_context_skill.py
```

Expected: PASS with a concise artifact count.

**Step 3: Repeat the original scenarios with the skill**

Run each scenario in a fresh agent context and give it only the skill path,
fixture, and user-like task. Record outputs in
`tests/skill-evals/forward-results.md`.

Expected: the agent produces an evidence-backed walkthrough, chooses narrow
instruction layers, and creates a proposal rather than directly mutating rules.

**Step 4: Close observed loopholes and re-run**

Update only instructions needed to address observed forward-test failures. Run
the scenarios again until all stated success criteria pass.

**Step 5: Run the full verification suite**

Run:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_claude_context_skill.py
python3 -m compileall -q .claude/skills/bootstrap-claude-context scripts tests
git diff --check
```

Expected: all commands exit zero.

**Step 6: Commit**

```bash
git add .claude/skills/bootstrap-claude-context scripts/validate_claude_context_skill.py tests/skill-evals
git commit -m "feat: add layered Claude context workflows"
```

### Task 6: Verify an installed fixture end to end

**Files:**
- Create during test only: temporary fixture repository
- Modify if required by evidence: `.claude/skills/bootstrap-claude-context/**`

**Step 1: Install into a fresh fixture**

Run the installer with `--apply`, then `--validate`. Inspect the generated tree
and confirm settings contain both lifecycle hooks.

**Step 2: Simulate lifecycle events**

Pipe representative `SessionEnd` JSON into the installed hook, then pipe
`SessionStart` JSON into its hook. Confirm exactly one receipt is created and
startup context reports it without exposing transcript content.

**Step 3: Verify repeat installation**

Add a handwritten instruction and custom settings key, re-run installation,
and prove both remain unchanged.

**Step 4: Re-run full verification**

Run:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_claude_context_skill.py
python3 -m compileall -q .claude/skills/bootstrap-claude-context scripts tests
git diff --check
```

Expected: all commands exit zero with no warnings.

**Step 5: Commit any evidence-driven fixes**

```bash
git add .claude/skills/bootstrap-claude-context scripts tests
git commit -m "test: verify Claude context lifecycle end to end"
```
