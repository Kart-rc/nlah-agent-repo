"""Regression checks for the Claude context structural validator."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


VALIDATOR_PATH = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "validate_claude_context_skill.py"
)


def load_validator():
    spec = importlib.util.spec_from_file_location(
        "validate_claude_context_skill", VALIDATOR_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("validator module could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SourceMachinePathTests(unittest.TestCase):
    def test_rejects_source_machine_absolute_paths(self):
        validator = load_validator()

        rejected = (
            "/root/project/skill.md",
            "/tmp/alice/project/skill.md",
            "/private/tmp/evaluation/project/skill.md",
            "/opt/workspace/project/skill.md",
            "/Volumes/dev/repo/skill.md",
            "/Users/alice/project/skill.md",
            "/home/alice/project/skill.md",
            r"C:\Users\alice\project\skill.md",
            "C:/Users/alice/project/skill.md",
        )
        for value in rejected:
            with self.subTest(value=value):
                self.assertTrue(validator.contains_source_machine_absolute_path(value))
        self.assertFalse(
            validator.contains_source_machine_absolute_path(
                "Use repository-relative .claude/rules paths."
            )
        )


class PlaceholderTests(unittest.TestCase):
    def test_rejects_actual_markers_but_allows_instructional_prose(self):
        validator = load_validator()

        for value in (
            "TODO: replace this section",
            "  - FIXME: finish the workflow",
            "TBD: choose a scope",
            "INSERT_HERE",
            "REPLACE ME",
        ):
            with self.subTest(value=value):
                self.assertTrue(validator.contains_placeholder_marker(value))
        self.assertFalse(
            validator.contains_placeholder_marker("Do not leave TODO comments.")
        )

    def test_source_debris_reports_marker_and_allows_todo_prose(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "bad.md").write_text("TODO: fill this in\n", encoding="utf-8")
            (root / "good.md").write_text(
                "Do not leave TODO comments.\n", encoding="utf-8"
            )
            violations = []
            with mock.patch.object(validator, "SKILL_ROOT", root):
                validator.validate_no_source_debris(violations)

        self.assertEqual(1, len(violations))
        self.assertIn("placeholder marker", violations[0])


class SettingsSchemaTests(unittest.TestCase):
    def setUp(self):
        self.validator = load_validator()
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.settings_path = self.root / "settings.fragment.json"
        self.hooks = {
            "SessionStart": self.root / "session-start.py",
            "SessionEnd": self.root / "session-end.py",
        }

    def tearDown(self):
        self.temporary.cleanup()

    @staticmethod
    def command(event):
        filename = "session-start.py" if event == "SessionStart" else "session-end.py"
        return f'python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/{filename}"'

    def valid_settings(self):
        return {
            "hooks": {
                event: [
                    {
                        "hooks": [
                            {"type": "command", "command": self.command(event)}
                        ]
                    }
                ]
                for event in self.hooks
            }
        }

    def validate(self, settings):
        self.settings_path.write_text(json.dumps(settings), encoding="utf-8")
        violations = []
        with (
            mock.patch.object(
                self.validator, "SETTINGS_FRAGMENT", self.settings_path
            ),
            mock.patch.object(self.validator, "HOOKS", self.hooks),
        ):
            self.validator.validate_settings(violations)
        return violations

    def test_accepts_exact_lifecycle_schema(self):
        self.assertEqual([], self.validate(self.valid_settings()))

    def test_rejects_malformed_lifecycle_entries(self):
        cases = {}

        missing_event = self.valid_settings()
        del missing_event["hooks"]["SessionEnd"]
        cases["missing event"] = missing_event

        wrong_event_shape = self.valid_settings()
        wrong_event_shape["hooks"]["SessionStart"] = {}
        cases["wrong event shape"] = wrong_event_shape

        missing_hooks = self.valid_settings()
        missing_hooks["hooks"]["SessionStart"] = [
            {
                "not_a_hook": {
                    "type": "command",
                    "command": self.command("SessionStart"),
                }
            }
        ]
        cases["arbitrary nested command"] = missing_hooks

        empty_hooks = self.valid_settings()
        empty_hooks["hooks"]["SessionStart"] = [{"hooks": []}]
        cases["empty hooks"] = empty_hooks

        extra_entry_key = self.valid_settings()
        extra_entry_key["hooks"]["SessionStart"][0]["arbitrary"] = True
        cases["extra entry key"] = extra_entry_key

        extra_hook_key = self.valid_settings()
        extra_hook_key["hooks"]["SessionStart"][0]["hooks"][0]["timeout"] = 1
        cases["extra hook key"] = extra_hook_key

        wrong_command = self.valid_settings()
        wrong_command["hooks"]["SessionStart"][0]["hooks"][0]["command"] = (
            "python3 other.py"
        )
        cases["wrong command"] = wrong_command

        for label, settings in cases.items():
            with self.subTest(label=label):
                self.assertTrue(self.validate(settings), label)


class StructuralValidationTests(unittest.TestCase):
    def setUp(self):
        self.validator = load_validator()
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def test_rejects_bad_frontmatter(self):
        skill = self.root / "SKILL.md"
        skill.write_text(
            "---\nname: Bad_Name\ndescription: test\nmetadata: extra\n---\n",
            encoding="utf-8",
        )
        violations = []
        with mock.patch.object(self.validator, "SKILLS", (skill,)):
            self.validator.validate_skills(violations)
        self.assertGreaterEqual(len(violations), 2)

    def test_rejects_root_template_at_200_lines(self):
        root_template = self.root / "CLAUDE.md"
        root_template.write_text("line\n" * 200, encoding="utf-8")
        violations = []
        with mock.patch.object(self.validator, "ROOT_TEMPLATE", root_template):
            self.validator.validate_root_template(violations)
        self.assertEqual(1, len(violations))

    def test_rejects_hook_syntax_error(self):
        hook = self.root / "session-start.py"
        hook.write_text("def broken(:\n", encoding="utf-8")
        violations = []
        with mock.patch.object(
            self.validator, "HOOKS", {"SessionStart": hook}
        ):
            self.validator.validate_hooks(violations)
        self.assertEqual(1, len(violations))

    def test_rejects_missing_required_workflow_phrase(self):
        workflow = self.root / "workflow.md"
        workflow.write_text("Evidence only.\n", encoding="utf-8")
        violations = []
        self.validator.require_language(
            workflow,
            {"approval": ("explicit developer approval",)},
            violations,
        )
        self.assertEqual(1, len(violations))


if __name__ == "__main__":
    unittest.main()
