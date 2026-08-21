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
            SKILL / "LICENSE",
            SKILL / "SOURCE.md",
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
        missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
        self.assertEqual([], missing)

    def test_skill_frontmatter_and_local_links_are_valid(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        self.assertIsNotNone(match)
        keys = [
            line.split(":", 1)[0]
            for line in match.group(1).splitlines()
            if ":" in line
        ]
        self.assertEqual(["name", "description"], keys)
        self.assertIn("name: unlazy", match.group(1))
        self.assertIn("`CHECK` values execute as shell commands", text)
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
        installed_license = (SKILL / "LICENSE").read_text(encoding="utf-8")
        installed_source = (SKILL / "SOURCE.md").read_text(encoding="utf-8")
        self.assertEqual(license_text, installed_license)
        self.assertIn("https://github.com/Leonxlnx/unlazy", installed_source)
        self.assertIn(UPSTREAM_COMMIT, installed_source)

    def test_catalog_exposes_skill_without_default_workflow_attachment(self):
        root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
        catalog = (ROOT / "docs" / "skillpack-catalog.md").read_text(encoding="utf-8")
        standalone = (ROOT / "docs" / "using-skills-standalone.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("48 practice skills", root_readme)
        self.assertIn("`unlazy`", catalog)
        self.assertIn("`unlazy`", standalone)
        self.assertEqual(
            48,
            len(list((ROOT / "harness" / "skillpacks").glob("*/*/SKILL.md"))),
        )
        self.assertEqual(
            9,
            len(
                [
                    path
                    for path in (ROOT / "harness" / "skillpacks").iterdir()
                    if path.is_dir()
                ]
            ),
        )
        default_attachments = "\n".join(
            path.read_text(encoding="utf-8")
            for root in (ROOT / "harness" / "workflows", ROOT / "harness" / "stages")
            for path in root.rglob("*")
            if path.is_file()
        )
        self.assertNotIn("skillpacks/unlazy", default_attachments)

    @unittest.skipUnless(shutil.which("node"), "unlazy requires Node.js 16+")
    def test_gate_checker_rejects_malformed_ledgers_without_running_checks(self):
        fixtures = {
            "no-gates": "# Gates: empty\n",
            "duplicate-ids": (
                "- [ ] G1: first\n"
                "  EVIDENCE: pending\n"
                "- [ ] G1: second\n"
                "  EVIDENCE: pending\n"
                "ABANDON: G1 one line must not abandon duplicate gates\n"
            ),
            "missing-evidence": (
                "- [ ] G1: runnable but structurally incomplete\n"
                "  CHECK: node -e \"console.log('must-not-run')\"\n"
                "  EXPECT: must-not-run\n"
            ),
            "abandon-without-reason": (
                "- [ ] G1: unfinished\n"
                "  EVIDENCE: pending\n"
                "ABANDON: G1\n"
            ),
        }
        with tempfile.TemporaryDirectory() as tmp:
            for name, contents in fixtures.items():
                with self.subTest(name=name):
                    gate_file = Path(tmp) / f"{name}.md"
                    gate_file.write_text(contents, encoding="utf-8")
                    run = subprocess.run(
                        ["node", str(CHECKER), str(gate_file)],
                        text=True,
                        capture_output=True,
                        check=False,
                    )
                    self.assertEqual(2, run.returncode, run.stdout + run.stderr)
                    self.assertIn("parse error", run.stderr)
                    self.assertNotIn("must-not-run", run.stdout)

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

    @unittest.skipUnless(shutil.which("node"), "unlazy requires Node.js 16+")
    def test_gate_checker_records_the_output_that_satisfied_expect(self):
        with tempfile.TemporaryDirectory() as tmp:
            gate_file = Path(tmp) / "GATES.md"
            gate_file.write_text(
                "# Gates: evidence fixture\n\n"
                "- [ ] G1: preserve deciding evidence\n"
                "  CHECK: node -e \"console.log('deciding-match\\nunrelated-one\\nunrelated-two')\"\n"
                "  EXPECT: deciding-match\n"
                "  EVIDENCE: pending\n",
                encoding="utf-8",
            )
            run = subprocess.run(
                ["node", str(CHECKER), str(gate_file)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, run.returncode, run.stdout + run.stderr)
            updated = gate_file.read_text(encoding="utf-8")
            self.assertIn("EVIDENCE: deciding-match", updated)

    @unittest.skipUnless(shutil.which("node"), "unlazy requires Node.js 16+")
    def test_gate_checker_keeps_a_late_match_in_bounded_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            gate_file = Path(tmp) / "GATES.md"
            gate_file.write_text(
                "# Gates: long evidence fixture\n\n"
                "- [ ] G1: preserve a match after the evidence cap\n"
                "  CHECK: node -e \"console.log('x'.repeat(240) + 'deciding-match')\"\n"
                "  EXPECT: deciding-match\n"
                "  EVIDENCE: pending\n",
                encoding="utf-8",
            )
            run = subprocess.run(
                ["node", str(CHECKER), str(gate_file)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, run.returncode, run.stdout + run.stderr)
            updated = gate_file.read_text(encoding="utf-8")
            evidence = updated.split("EVIDENCE: ", 1)[1].strip()
            self.assertIn("deciding-match", evidence)
            self.assertLessEqual(len(evidence), 200)


if __name__ == "__main__":
    unittest.main()
