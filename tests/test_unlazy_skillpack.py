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
        standalone = (ROOT / "docs" / "using-skills-standalone.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("48 practice skills", root_readme)
        self.assertIn("`unlazy`", catalog)
        self.assertIn("`unlazy`", standalone)
        manifests = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (ROOT / "harness" / "workflows").glob("*/workflow.yaml")
        )
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
