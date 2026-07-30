from __future__ import annotations

import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).parents[1] / "scripts" / "build_skill_shards.py"
SPEC = importlib.util.spec_from_file_location("build_skill_shards", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot load scanner module from {SCRIPT}")
scanner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(scanner)


def skill_text(
    name: str,
    description: str = "Use when a test task needs this skill.",
    body: str = "# Skill\n\nInstructions.\n",
) -> str:
    return (
        "---\n"
        f"name: {name}\n"
        f"description: {description}\n"
        "---\n\n"
        f"{body}"
    )


class SkillShardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.base = Path(self.tempdir.name)
        self.root = self.base / "catalog"
        self.output = self.base / "output"
        self.root.mkdir()

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def write_skill(
        self,
        relative_dir: str,
        name: str,
        *,
        description: str = "Use when a test task needs this skill.",
        body: str = "# Skill\n\nInstructions.\n",
    ) -> Path:
        directory = self.root / relative_dir
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / "SKILL.md"
        path.write_text(skill_text(name, description, body), encoding="utf-8")
        return path

    def test_extracts_only_bounded_frontmatter(self) -> None:
        path = self.write_skill(
            "safe",
            "safe-skill",
            body=(
                "# Safe\n\n"
                "```yaml\n"
                "name: body-impostor\n"
                "description: Use when this body value must be ignored.\n"
                "```\n"
            ),
        )

        entry, error = scanner.read_skill(path, self.root.resolve())

        self.assertIsNone(error)
        self.assertEqual(entry["name"], "safe-skill")
        self.assertNotIn("body-impostor", entry["frontmatter"])

    def test_supports_folded_multiline_description(self) -> None:
        directory = self.root / "folded"
        directory.mkdir()
        path = directory / "SKILL.md"
        path.write_text(
            "---\n"
            "name: folded-skill\n"
            "description: >-\n"
            "  Use when a task spans\n"
            "  multiple lines.\n"
            "---\n\n"
            "# Folded\n",
            encoding="utf-8",
        )

        entry, error = scanner.read_skill(path, self.root.resolve())

        self.assertIsNone(error)
        self.assertEqual(
            entry["description"], "Use when a task spans multiple lines."
        )

    def test_reports_malformed_and_missing_frontmatter(self) -> None:
        malformed_dir = self.root / "malformed"
        missing_dir = self.root / "missing"
        malformed_dir.mkdir()
        missing_dir.mkdir()
        (malformed_dir / "SKILL.md").write_text(
            "---\nname: malformed\n# no closing fence\n", encoding="utf-8"
        )
        (missing_dir / "SKILL.md").write_text("# Missing\n", encoding="utf-8")

        result = scanner.build_catalog(self.root, self.output)

        self.assertEqual(result["included_count"], 0)
        self.assertEqual(result["skipped_count"], 2)
        reasons = {item["reason"] for item in result["skipped"]}
        self.assertIn("unterminated_frontmatter", reasons)
        self.assertIn("missing_frontmatter", reasons)

    def test_reports_unreadable_skill(self) -> None:
        path = self.write_skill("private", "private-skill")
        original = Path.read_text

        def guarded_read(candidate: Path, *args: object, **kwargs: object) -> str:
            if candidate == path:
                raise PermissionError("denied")
            return original(candidate, *args, **kwargs)

        with mock.patch.object(Path, "read_text", guarded_read):
            entry, error = scanner.read_skill(path, self.root.resolve())

        self.assertIsNone(entry)
        self.assertEqual(error["reason"], "unreadable")

    def test_rejects_unreadable_catalog_root(self) -> None:
        self.root.chmod(0)
        try:
            with self.assertRaisesRegex(ValueError, "readable"):
                scanner.build_catalog(self.root, self.output)
        finally:
            self.root.chmod(0o700)

    def test_discovers_unicode_paths_and_ignores_other_filenames(self) -> None:
        expected = self.write_skill("équipe/分析", "unicode-skill")
        (self.root / "équipe" / "NOT_A_SKILL.md").write_text(
            skill_text("ignored"), encoding="utf-8"
        )

        result = scanner.build_catalog(self.root, self.output)

        self.assertEqual(result["included_count"], 1)
        self.assertEqual(result["entries"][0]["path"], str(expected.resolve()))

    def test_skips_external_symlink_and_deduplicates_internal_file_symlink(
        self,
    ) -> None:
        source = self.write_skill("source", "source-skill")
        alias_dir = self.root / "alias"
        escape_dir = self.root / "escape"
        alias_dir.mkdir()
        escape_dir.mkdir()
        try:
            (alias_dir / "SKILL.md").symlink_to(source)
            external = self.base / "external-SKILL.md"
            external.write_text(skill_text("external-skill"), encoding="utf-8")
            (escape_dir / "SKILL.md").symlink_to(external)
        except OSError as exc:
            self.skipTest(f"symlinks unavailable: {exc}")

        result = scanner.build_catalog(self.root, self.output)

        self.assertEqual(result["included_count"], 1)
        reasons = [item["reason"] for item in result["skipped"]]
        self.assertIn("duplicate_canonical_path", reasons)
        self.assertIn("symlink_escape", reasons)

    def test_does_not_follow_symlink_directory_cycles(self) -> None:
        self.write_skill("real", "real-skill")
        loop = self.root / "real" / "loop"
        try:
            loop.symlink_to(self.root / "real", target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"symlinks unavailable: {exc}")

        result = scanner.build_catalog(self.root, self.output)

        self.assertEqual(result["included_count"], 1)
        self.assertIn(
            "symlink_directory_not_followed",
            {item["reason"] for item in result["skipped"]},
        )

    def test_shards_are_deterministic_and_respect_limits(self) -> None:
        for index in range(7):
            self.write_skill(
                f"group-{index}",
                f"skill-{index}",
                body="# Skill\n\n" + ("x" * 160),
            )

        first = scanner.build_catalog(
            self.root, self.output / "first", max_files=3, max_bytes=700
        )
        second = scanner.build_catalog(
            self.root, self.output / "second", max_files=3, max_bytes=700
        )

        first_shape = [
            [entry["relative_path"] for entry in shard["entries"]]
            for shard in first["shards"]
        ]
        second_shape = [
            [entry["relative_path"] for entry in shard["entries"]]
            for shard in second["shards"]
        ]
        self.assertEqual(first_shape, second_shape)
        assigned = [path for shard in first_shape for path in shard]
        self.assertEqual(len(assigned), len(set(assigned)))
        self.assertEqual(len(assigned), 7)
        for shard in first["shards"]:
            self.assertLessEqual(shard["entry_count"], 3)
            self.assertLessEqual(shard["total_bytes"], 700)

    def test_oversized_skill_gets_singleton_shard(self) -> None:
        self.write_skill(
            "large", "large-skill", body="# Large\n\n" + ("x" * 2_000)
        )
        self.write_skill("small", "small-skill")

        result = scanner.build_catalog(
            self.root, self.output, max_files=20, max_bytes=500
        )

        oversized = [
            shard for shard in result["shards"] if shard["oversized_singleton"]
        ]
        self.assertEqual(len(oversized), 1)
        self.assertEqual(oversized[0]["entry_count"], 1)
        self.assertEqual(oversized[0]["entries"][0]["name"], "large-skill")

    def test_empty_catalog_creates_inventory_without_shards(self) -> None:
        result = scanner.build_catalog(self.root, self.output)

        self.assertEqual(result["discovered_count"], 0)
        self.assertEqual(result["included_count"], 0)
        self.assertEqual(result["shards"], [])
        self.assertTrue((self.output / "inventory.json").is_file())

    def test_scales_to_500_skills_without_duplicate_assignment(self) -> None:
        for index in range(500):
            self.write_skill(f"pack/skill-{index:03d}", f"skill-{index:03d}")

        result = scanner.build_catalog(
            self.root, self.output, max_files=20, max_bytes=100 * 1024
        )

        assigned = [
            entry["path"]
            for shard in result["shards"]
            for entry in shard["entries"]
        ]
        self.assertEqual(result["included_count"], 500)
        self.assertEqual(len(assigned), 500)
        self.assertEqual(len(set(assigned)), 500)
        self.assertTrue(
            all(shard["entry_count"] <= 20 for shard in result["shards"])
        )

    def test_reports_duplicate_names_without_dropping_versions(self) -> None:
        first = self.write_skill("pack-a/shared", "shared-skill")
        second = self.write_skill("pack-b/shared", "shared-skill")

        result = scanner.build_catalog(self.root, self.output)

        self.assertEqual(result["included_count"], 2)
        self.assertEqual(
            result["name_collisions"],
            [
                {
                    "name": "shared-skill",
                    "paths": sorted([str(first.resolve()), str(second.resolve())]),
                }
            ],
        )

    def test_rejects_output_directory_inside_catalog(self) -> None:
        with self.assertRaisesRegex(ValueError, "outside the skills directory"):
            scanner.build_catalog(self.root, self.root / "generated")

    def test_validates_recommendation_paths_and_rejects_escape(self) -> None:
        valid = self.write_skill("valid", "valid-skill")
        external_dir = self.base / "outside"
        external_dir.mkdir()
        external = external_dir / "SKILL.md"
        external.write_text(skill_text("outside-skill"), encoding="utf-8")
        result_path = self.base / "recommendation.json"
        result_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "status": "recommended",
                    "catalog": {"root": str(self.root.resolve())},
                    "recommendations": [
                        {
                            "path": str(valid.resolve()),
                            "classification": "required",
                        }
                    ],
                    "conditional_skills": [
                        {
                            "path": str(external),
                            "classification": "conditional",
                        }
                    ],
                    "rejected_alternatives": [],
                }
            ),
            encoding="utf-8",
        )

        validation = scanner.validate_result(self.root, result_path)

        self.assertFalse(validation["valid"])
        self.assertEqual(validation["checked_count"], 2)
        self.assertEqual(validation["errors"][0]["reason"], "path_outside_catalog")

    def test_validation_enforces_status_classification_and_rejected_paths(
        self,
    ) -> None:
        valid = self.write_skill("valid", "valid-skill")
        external_dir = self.base / "outside"
        external_dir.mkdir()
        external = external_dir / "SKILL.md"
        external.write_text(skill_text("outside-skill"), encoding="utf-8")
        result_path = self.base / "recommendation.json"
        result_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "status": "invented",
                    "recommendations": [
                        {
                            "path": str(valid),
                            "classification": "conditional",
                        }
                    ],
                    "conditional_skills": [],
                    "rejected_alternatives": [
                        {
                            "path": str(external),
                            "classification": "excluded",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )

        validation = scanner.validate_result(self.root, result_path)

        self.assertFalse(validation["valid"])
        reasons = {error["reason"] for error in validation["errors"]}
        self.assertIn("invalid_status", reasons)
        self.assertIn("invalid_classification", reasons)
        self.assertIn("path_outside_catalog", reasons)
        self.assertEqual(validation["checked_count"], 2)

    def test_validation_requires_exact_canonical_paths_and_status_consistency(
        self,
    ) -> None:
        valid = self.write_skill("valid", "valid-skill")
        noncanonical = valid.parent / ".." / "valid" / "SKILL.md"
        result_path = self.base / "recommendation.json"
        result_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "status": "no_match",
                    "clarifying_question": None,
                    "recommendations": [
                        {
                            "path": str(noncanonical),
                            "classification": "required",
                        }
                    ],
                    "conditional_skills": [],
                    "rejected_alternatives": [],
                }
            ),
            encoding="utf-8",
        )

        validation = scanner.validate_result(self.root, result_path)

        self.assertFalse(validation["valid"])
        reasons = {error["reason"] for error in validation["errors"]}
        self.assertIn("path_not_canonical", reasons)
        self.assertIn("status_collection_mismatch", reasons)


if __name__ == "__main__":
    unittest.main()
