# Unlazy Skill Integration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add the audited upstream `unlazy` v2 package as a tested, documented, ad hoc standalone practice skill without changing NLAH workflow semantics.

**Architecture:** Vendor the upstream runtime files under a new `unlazy` skill pack, normalize only the discovery frontmatter, and put NLAH-specific provenance and routing guidance around the package. Keep all shipped workflow manifests unchanged; the new skill fills the documented standalone completion-enforcement gap.

**Tech Stack:** Markdown Agent Skills, zero-dependency Node.js 16+ scripts, Python `unittest`, NLAH natural-language harness documents.

---

### Task 1: Add failing skillpack integration tests

**Files:**
- Create: `tests/test_unlazy_skillpack.py`

**Step 1: Write the failing package and behavior tests**

Create a `unittest` module that checks the required layout, normalized
frontmatter, local resource links, pinned provenance, catalog exposure, lack of
default workflow attachment, and the checker's RED → GREEN behavior:

```python
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "harness" / "skillpacks" / "unlazy"
SKILL = PACK / "unlazy"
CHECKER = SKILL / "scripts" / "gate-check.mjs"
UPSTREAM_COMMIT = "ed9e8d2b5919698cf2c54bda270d507e10b69617"


class UnlazySkillpackTests(unittest.TestCase):
    def test_required_package_files_exist(self):
        required = (
            PACK / "README.md",
            PACK / "LICENSE",
            SKILL / "SKILL.md",
            SKILL / "USAGE.md",
            CHECKER,
            SKILL / "scripts" / "stop-hook.mjs",
            SKILL / "scripts" / "install-hooks.mjs",
            SKILL / "references" / "gates.md",
            SKILL / "references" / "method.md",
            SKILL / "references" / "orchestration.md",
            SKILL / "references" / "token-economy.md",
            SKILL / "templates" / "PLAN.md",
            SKILL / "templates" / "gates-leaf.md",
            SKILL / "templates" / "gates-node.md",
        )
        self.assertEqual([], [str(path.relative_to(ROOT)) for path in required if not path.is_file()])

    def test_skill_frontmatter_and_local_links_are_valid(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        self.assertIsNotNone(match)
        keys = [line.split(":", 1)[0] for line in match.group(1).splitlines() if ":" in line]
        self.assertEqual(["name", "description"], keys)
        self.assertIn("name: unlazy", match.group(1))
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if "://" not in target and not target.startswith("#"):
                self.assertTrue((SKILL / target).is_file(), target)

    def test_pack_records_source_license_and_audited_commit(self):
        readme = (PACK / "README.md").read_text(encoding="utf-8")
        license_text = (PACK / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("https://github.com/Leonxlnx/unlazy", readme)
        self.assertIn(UPSTREAM_COMMIT, readme)
        self.assertIn("MIT License", license_text)
        self.assertIn("Leonxlnx", license_text)

    def test_catalog_exposes_skill_without_default_workflow_attachment(self):
        root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
        catalog = (ROOT / "docs" / "skillpack-catalog.md").read_text(encoding="utf-8")
        standalone = (ROOT / "docs" / "using-skills-standalone.md").read_text(encoding="utf-8")
        self.assertIn("48 practice skills", root_readme)
        self.assertIn("`unlazy`", catalog)
        self.assertIn("`unlazy`", standalone)
        manifests = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "harness" / "workflows").glob("*/workflow.yaml"))
        self.assertNotIn("skillpacks/unlazy", manifests)

    @unittest.skipUnless(shutil.which("node"), "unlazy requires Node.js 16+")
    def test_gate_checker_turns_a_passing_check_into_recorded_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            gate_file = Path(tmp) / "GATES.md"
            gate_file.write_text(
                "# Gates: fixture\n\n"
                "- [ ] G1: deterministic fixture passes\n"
                "  CHECK: node -e \"console.log('gate-ok')\"\n"
                "  EXPECT: gate-ok\n"
                "  EVIDENCE: pending\n",
                encoding="utf-8",
            )
            before = subprocess.run(
                ["node", str(CHECKER), "--status", str(gate_file)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(1, before.returncode)
            self.assertIn("UNMET: 1", before.stdout)
            run = subprocess.run(
                ["node", str(CHECKER), str(gate_file)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, run.returncode, run.stdout + run.stderr)
            self.assertIn("ALL MET (1 met)", run.stdout)
            updated = gate_file.read_text(encoding="utf-8")
            self.assertIn("- [x] G1:", updated)
            self.assertIn("EVIDENCE: gate-ok", updated)
            after = subprocess.run(
                ["node", str(CHECKER), "--status", str(gate_file)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, after.returncode)
            self.assertIn("ALL MET (1 met)", after.stdout)


if __name__ == "__main__":
    unittest.main()
```

**Step 2: Run the test to verify RED**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_unlazy_skillpack.py' -v
```

Expected: FAIL because `harness/skillpacks/unlazy/` and its catalog entries do
not exist.

**Step 3: Commit the failing test**

```bash
git add -- tests/test_unlazy_skillpack.py
git commit -m "test: specify unlazy skillpack integration"
```

### Task 2: Vendor the pinned upstream runtime package

**Files:**
- Create: `harness/skillpacks/unlazy/LICENSE`
- Create: `harness/skillpacks/unlazy/unlazy/SKILL.md`
- Create: `harness/skillpacks/unlazy/unlazy/references/gates.md`
- Create: `harness/skillpacks/unlazy/unlazy/references/method.md`
- Create: `harness/skillpacks/unlazy/unlazy/references/orchestration.md`
- Create: `harness/skillpacks/unlazy/unlazy/references/token-economy.md`
- Create: `harness/skillpacks/unlazy/unlazy/scripts/gate-check.mjs`
- Create: `harness/skillpacks/unlazy/unlazy/scripts/install-hooks.mjs`
- Create: `harness/skillpacks/unlazy/unlazy/scripts/stop-hook.mjs`
- Create: `harness/skillpacks/unlazy/unlazy/templates/PLAN.md`
- Create: `harness/skillpacks/unlazy/unlazy/templates/gates-leaf.md`
- Create: `harness/skillpacks/unlazy/unlazy/templates/gates-node.md`

**Step 1: Copy the audited runtime files**

Copy only the runtime skill material from the temporary clone at
`/private/tmp/nlah-unlazy-source-20260821`; do not vendor its `.git`, README,
changelog, or contribution files into the executable skill directory.

**Step 2: Normalize discovery frontmatter**

Keep only `name` and `description` in `SKILL.md` frontmatter. Leave the
instruction body and all scripts/references/templates behaviorally identical
to upstream commit `ed9e8d2b5919698cf2c54bda270d507e10b69617`.

**Step 3: Run the package tests**

Run the focused test. Expected: layout/frontmatter/checker tests pass;
documentation/provenance assertions may still fail until Tasks 3–4.

### Task 3: Add provenance and NLAH usage boundaries

**Files:**
- Create: `harness/skillpacks/unlazy/README.md`
- Create: `harness/skillpacks/unlazy/unlazy/USAGE.md`

**Step 1: Write pack provenance**

Document the source URL, full audited commit, MIT license, vendored file set,
frontmatter-only adaptation, Node 16+ runtime, and update procedure.

**Step 2: Write the usage contract**

Explain:

- use for substantial standalone tasks with premature-completion risk;
- use `GATES.md` for solo tasks and `PLAN.md` + `gates/` for deep builds;
- run `gate-check.mjs` rather than self-certifying;
- do not attach by default to shipped NLAH workflows;
- full workflows use `HARNESS.md` state, validators, repair, and escalation;
- `ABANDON` is visible incomplete scope, not success;
- the Stop hook is optional and must never be installed without explicit user
  permission; and
- `CHECK` commands execute through a shell and remain subject to ordinary
  permission/safety review.

**Step 3: Run the focused test**

Expected: package/provenance/checker tests pass; catalog test still fails.

### Task 4: Publish the usefulness decision in harness documentation

**Files:**
- Create: `docs/unlazy-skill-assessment.md`
- Modify: `README.md`
- Modify: `docs/skillpack-catalog.md`
- Modify: `docs/using-skills-standalone.md`

**Step 1: Add the evidence-backed assessment**

Record a capability matrix comparing `unlazy` with stage contracts,
completeness checks, planning, incremental implementation, verification,
repair loops, report traceability, and standalone limitations. Conclude that
the skill is unique for its executable task-local ledger but redundant and
potentially conflicting as a default full-workflow attachment.

**Step 2: Update counts and catalog**

Change 47 → 48 skills and eight → nine packs where applicable. Add an
`unlazy` catalog section marked `ad hoc / standalone` and update the repository
layout/design-lineage summaries.

**Step 3: Explain the standalone fit**

Add the pack to the standalone guide and state that it improves completion
discipline but does not recreate risk routing, independent validators, bounded
repair/escalation, or resumable run state.

**Step 4: Run the focused test to verify GREEN**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_unlazy_skillpack.py' -v
```

Expected: all tests pass.

### Task 5: Verify the complete repository integration

**Files:**
- Verify all files changed by Tasks 1–4.

**Step 1: Validate every vendored script**

```bash
for script in harness/skillpacks/unlazy/unlazy/scripts/*.mjs; do node --check "$script"; done
```

Expected: exit 0 with no syntax errors.

**Step 2: Run harness lint**

```bash
python3 scripts/harness_lint.py
```

Expected: exit 0.

**Step 3: Run the full test suite**

```bash
python3 -m unittest discover -s tests -v
```

Expected: all tests pass.

**Step 4: Audit source fidelity**

Diff each vendored runtime file against the pinned clone. All references,
scripts, and templates must be byte-identical. `SKILL.md` may differ only in
its YAML frontmatter. Confirm no workflow manifest references
`skillpacks/unlazy`.

**Step 5: Audit the diff**

```bash
git diff --check
git status --short
git diff --stat
```

Expected: no whitespace errors; only the planned skillpack, tests, design,
assessment, and catalog documentation are changed.

### Task 6: Review and commit the integration

**Files:**
- Review all changed files.

**Step 1: Run a code/skill review**

Check source attribution, license preservation, script safety disclosures,
NLAH boundary clarity, catalog discoverability, and test coverage. Address any
findings and rerun Task 5.

**Step 2: Commit confirmed paths only**

```bash
git add -- README.md docs/skillpack-catalog.md docs/using-skills-standalone.md docs/unlazy-skill-assessment.md harness/skillpacks/unlazy tests/test_unlazy_skillpack.py docs/plans/2026-08-21-unlazy-skill-integration.md
git commit -m "feat: add unlazy completion skillpack"
```

**Step 3: Confirm final branch state**

```bash
git status --short --branch
git log -3 --oneline --decorate
```

Expected: clean `codex/add-unlazy-skill` branch with design, test, and feature
commits above `origin/main`.
