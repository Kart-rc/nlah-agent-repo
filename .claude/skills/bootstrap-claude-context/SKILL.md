---
name: bootstrap-claude-context
description: Use when a repository needs Claude Code onboarding, layered project instructions, or installation of a self-improving context scaffold.
---

# Bootstrap Claude Context

Build a small, evidence-backed instruction system. Treat every existing
instruction as user-authored: never replace or rewrite it silently.

## Required workflow

1. Set the target repository explicitly. Read all existing `CLAUDE.md`,
   `AGENTS.md`, `.claude/rules/`, Claude settings, contributor guidance, build
   manifests, CI, tests, and relevant subsystem documentation. Record the path
   supporting every repository claim; label inferences and unknowns.
2. Read [references/layering.md](references/layering.md). Read
   [references/learning-admission.md](references/learning-admission.md) before
   proposing the learning loop or its rule content.
3. Run the deterministic installer in preview mode:

   ```sh
   python3 "${CLAUDE_SKILL_DIR}/scripts/install.py" --target "$TARGET" --dry-run
   ```

4. Present the dry-run result, conflicts, and an exact proposed map of every
   create/merge/preserve action plus every project-specific instruction diff.
   Explain each rule's evidence and narrowest layer.
5. **Stop and obtain explicit developer approval for those exact writes.** A
   request to inspect, bootstrap, or improve guidance is not approval to mutate
   it. If the plan changes, show the revised diff and ask again.
6. After approval, apply the stable scaffold:

   ```sh
   python3 "${CLAUDE_SKILL_DIR}/scripts/install.py" --target "$TARGET" --apply
   ```

   The installer preserves existing files. Reconcile preserved files only with
   the separately approved minimal diff; never replace handwritten guidance
   with a template.
7. Write only approved, evidence-cited codebase-map content and project rules.
   Use complete repository-relative evidence paths; never persist absolute home
   or transcript paths in tracked context. Keep detailed orientation in the
   map, not root guidance. Do not turn sparse entry points into invented
   architecture, or broaden a path-specific observation into a repository-wide
   rule. When evidence exists only in the developer's request, cite it as an
   unverified developer-provided note with the concrete path or command it
   names; never invent a receipt ID, source file, review, or other evidence
   artifact.
8. Validate the installation:

   ```sh
   python3 "${CLAUDE_SKILL_DIR}/scripts/install.py" --target "$TARGET" --validate
   ```

   Inspect the final diff for scope and secrets, then report preserved files,
   warnings, and unverified claims. Tell the developer to restart Claude Code
   because lifecycle hooks load at session startup.

## Acceptance checks

- Root guidance is lean and universal; scoped details stay scoped.
- Every repository-specific rule includes identifiable evidence.
- Temporary state, credentials, and unsettled hypotheses are absent.
- The installed finish workflow proposes changes but never edits instructions.
- No user-authored guidance changed outside the approved exact diff.

## Common mistakes

- Treating a README label as proof of runtime behavior.
- Citing a directory without citing the source of the rule.
- Generalizing one generated file into “never edit generated files.”
- Applying a “helpful” edit before approval.
