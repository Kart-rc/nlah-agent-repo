# Adding a Stage

A stage is the unit of producer work. It is self-contained and
workflow-agnostic: any workflow may attach it, parameterizing per-attachment
via manifest `with`/bindings — never by editing the stage for one workflow.

## Checklist

1. **Create `harness/stages/<id>/stage.md`** — frontmatter must validate
   against `harness/schema/stage-contract.schema.json`:
   - `id` — slug, must equal the directory name
   - `summary` — one line
   - `producer` — an existing persona in `.claude/agents/` (planner, builder,
     or analyst; add a new persona only for a genuinely new tool profile)
   - `inputs` / `outputs` — names, formats, descriptions; outputs also declare
     their `file` inside `artifacts/`
   - `acceptance_criteria` — **the centerpiece.** Concrete, checkable
     statements a hostile reviewer can verify. If a criterion needs taste to
     evaluate, sharpen it until it doesn't, or split it
   - `default_validators` — the validators the composer will copy into
     manifests (completeness-check first; add adversarial/persona/red-team as
     the work warrants)
   - `knowledge_slots` — adapter capabilities the stage can consume
     (org-context, prior-art, personal-notes)
   - `skill_refs` — suggested practice skills from `harness/skillpacks/`
   - `permissions.writes` — `[own_artifact_dir]`, plus `target_repo` only for
     builder stages

2. **Write the body** with exactly these section headings (linted):
   - `Purpose` — why the stage exists, one paragraph
   - `Procedure` — numbered steps the producer follows
   - `Output format constraints` — exact structure of each artifact (the
     completeness-check verifies these mechanically)
   - `Knowledge consumption` — per slot: when/how to query an attached
     adapter, the citation rule, and the no-adapter fallback (proceed +
     record under `## Knowledge gaps`)
   - `Boundaries` — what the stage MUST NOT do (the scope-drift anchor, F4)
   - `Self-check before submitting` — the producer's pre-flight against the
     acceptance criteria
   - `Summary requirement` — what goes in the ≤200-word `summary.md`

3. **Lint**: `python3 scripts/harness_lint.py` — fix everything.

4. **Attach it** to a workflow via the workflow-composer skill (or edit the
   manifest directly): add the stage block with `uses`, `needs`, input
   bindings, and materialized validators/skills. Lint again.

5. **Prove it**: run the workflow on a toy request and confirm the stage's
   gate fires and its artifacts satisfy a fresh reader.

## Design guidance

- **One stage = one kind of judgment.** If your Procedure alternates between
  producing and evaluating, the evaluating half is probably a validator
  attachment, not stage content.
- **Artifacts over prose.** Downstream stages consume declared outputs by
  path; anything important must live in an output file, not in the summary.
- **Criteria drive repairs.** Repair prompts quote failed criteria verbatim —
  vague criteria produce vague repairs.
- **Don't fork stages per workflow.** If two workflows need different
  behavior, parameterize via manifest `with` on validators or different
  attached skills. Fork only when the *contract* (inputs/outputs/criteria)
  genuinely differs — see `docs/architecture.md` on why proposal has
  `research`/`draft` instead of reusing `design`.
