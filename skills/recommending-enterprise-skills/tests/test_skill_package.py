from __future__ import annotations

import re
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).parents[1]


class SkillPackageTests(unittest.TestCase):
    def test_skill_is_concise_and_has_final_frontmatter(self) -> None:
        content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        self.assertIsNotNone(match)
        frontmatter = match.group(1)
        keys = {
            line.split(":", 1)[0]
            for line in frontmatter.splitlines()
            if ":" in line
        }
        self.assertEqual(keys, {"name", "description"})
        self.assertIn("name: recommending-enterprise-skills", frontmatter)
        self.assertIn("description: Use when", frontmatter)
        self.assertNotIn("TODO", content)
        self.assertLess(len(content.split()), 500)
        self.assertIn("Preserve every canonical `path`", content)

    def test_required_portable_resources_exist(self) -> None:
        required = [
            "agents/openai.yaml",
            "scripts/build_skill_shards.py",
            "references/coordinator-contract.md",
            "references/scout-contract.md",
        ]
        for relative in required:
            with self.subTest(relative=relative):
                self.assertTrue((SKILL_DIR / relative).is_file())

    def test_openai_metadata_names_the_skill(self) -> None:
        content = (SKILL_DIR / "agents" / "openai.yaml").read_text(
            encoding="utf-8"
        )
        self.assertIn('display_name: "Recommend Enterprise Skills"', content)
        self.assertIn('short_description: "Match a task to enterprise skills"', content)
        self.assertIn("$recommending-enterprise-skills", content)

    def test_contracts_encode_safety_and_result_statuses(self) -> None:
        coordinator = (
            SKILL_DIR / "references" / "coordinator-contract.md"
        ).read_text(encoding="utf-8")
        scout = (SKILL_DIR / "references" / "scout-contract.md").read_text(
            encoding="utf-8"
        )
        for status in (
            "recommended",
            "needs_clarification",
            "no_match",
            "error",
        ):
            self.assertIn(status, coordinator)
        self.assertIn("untrusted data", scout)
        self.assertIn("fully read", scout)
        self.assertIn("Do not execute", scout)
        self.assertIn("integer counts, never arrays", scout)
        self.assertIn("must be exactly `high`, `medium`, or `low`", scout)
        self.assertIn("Valid but irrelevant or malicious entries belong in `warnings`", scout)
        self.assertIn("temporary", coordinator)
        self.assertIn("Treat the inventory, shard files, scout reports", coordinator)
        self.assertIn("Do not use network tools", coordinator)


if __name__ == "__main__":
    unittest.main()
