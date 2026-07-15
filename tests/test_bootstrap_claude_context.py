import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPOSITORY_ROOT / ".claude" / "skills" / "bootstrap-claude-context"
INSTALLER = SKILL_ROOT / "scripts" / "install.py"
ASSET_PROJECT = SKILL_ROOT / "assets" / "project"
SESSION_START_HOOK = ASSET_PROJECT / ".claude" / "hooks" / "session-start.py"
SESSION_END_HOOK = ASSET_PROJECT / ".claude" / "hooks" / "session-end.py"

EXPECTED_FILES = {
    "CLAUDE.md",
    ".claude/settings.json",
    ".claude/context/codebase-map.md",
    ".claude/context/learnings/.gitignore",
    ".claude/hooks/session-start.py",
    ".claude/hooks/session-end.py",
    ".claude/skills/start-codebase/SKILL.md",
    ".claude/skills/finish-session/SKILL.md",
    ".claude/skills/review-learnings/SKILL.md",
}


class BootstrapClaudeContextTests(unittest.TestCase):
    def run_installer(self, target, mode):
        return subprocess.run(
            [sys.executable, str(INSTALLER), "--target", str(target), mode],
            cwd=REPOSITORY_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def parse_summary(self, result):
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        summary = json.loads(result.stdout)
        self.assertEqual(
            set(summary), {"create", "merge", "preserve", "warning"}
        )
        for actions in summary.values():
            self.assertIsInstance(actions, list)
        return summary

    def run_hook(self, script, project, payload=None, raw_stdin=None):
        environment = os.environ.copy()
        environment["CLAUDE_PROJECT_DIR"] = str(project)
        stdin = raw_stdin if raw_stdin is not None else json.dumps(payload or {})
        return subprocess.run(
            [sys.executable, str(script)],
            cwd=REPOSITORY_ROOT,
            env=environment,
            input=stdin,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_dry_run_lists_writes_without_mutating_target(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory)

            result = self.run_installer(target, "--dry-run")

            summary = self.parse_summary(result)
            self.assertTrue(EXPECTED_FILES.issubset(set(summary["create"])))
            self.assertEqual(list(target.iterdir()), [])

    def test_install_creates_expected_project_scaffold(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory)

            apply_result = self.run_installer(target, "--apply")

            summary = self.parse_summary(apply_result)
            self.assertTrue(EXPECTED_FILES.issubset(set(summary["create"])))
            for relative_path in EXPECTED_FILES:
                self.assertTrue((target / relative_path).is_file(), relative_path)

            settings = json.loads((target / ".claude/settings.json").read_text())
            self.assertEqual(set(settings["hooks"]), {"SessionStart", "SessionEnd"})
            for event in ("SessionStart", "SessionEnd"):
                self.assertEqual(len(settings["hooks"][event]), 1)

            validate_result = self.run_installer(target, "--validate")
            self.parse_summary(validate_result)

    def test_install_merges_existing_settings_without_losing_keys(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory)
            claude_directory = target / ".claude"
            claude_directory.mkdir()
            existing_start_hook = {
                "matcher": "startup",
                "hooks": [{"type": "command", "command": "existing-start"}],
            }
            original = {
                "permissions": {"allow": ["Bash(git status:*)"]},
                "customSetting": {"nested": True},
                "hooks": {
                    "SessionStart": [existing_start_hook],
                    "PreToolUse": [
                        {
                            "matcher": "Bash",
                            "hooks": [
                                {"type": "command", "command": "existing-check"}
                            ],
                        }
                    ],
                },
            }
            settings_path = claude_directory / "settings.json"
            settings_path.write_text(json.dumps(original), encoding="utf-8")

            result = self.run_installer(target, "--apply")

            summary = self.parse_summary(result)
            self.assertIn(".claude/settings.json", summary["merge"])
            merged = json.loads(settings_path.read_text(encoding="utf-8"))
            self.assertEqual(merged["permissions"], original["permissions"])
            self.assertEqual(merged["customSetting"], original["customSetting"])
            self.assertEqual(merged["hooks"]["PreToolUse"], original["hooks"]["PreToolUse"])
            self.assertEqual(merged["hooks"]["SessionStart"][0], existing_start_hook)
            self.assertEqual(len(merged["hooks"]["SessionStart"]), 2)
            self.assertEqual(len(merged["hooks"]["SessionEnd"]), 1)

    def test_reinstall_is_idempotent_and_preserves_user_files(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory)
            first_result = self.run_installer(target, "--apply")
            self.parse_summary(first_result)

            root_instructions = target / "CLAUDE.md"
            start_skill = target / ".claude/skills/start-codebase/SKILL.md"
            root_instructions.write_text("# User instructions\n", encoding="utf-8")
            start_skill.write_text("# User start workflow\n", encoding="utf-8")
            settings_before = json.loads(
                (target / ".claude/settings.json").read_text(encoding="utf-8")
            )

            second_result = self.run_installer(target, "--apply")

            summary = self.parse_summary(second_result)
            self.assertEqual(root_instructions.read_text(encoding="utf-8"), "# User instructions\n")
            self.assertEqual(start_skill.read_text(encoding="utf-8"), "# User start workflow\n")
            self.assertIn("CLAUDE.md", summary["preserve"])
            self.assertIn(
                ".claude/skills/start-codebase/SKILL.md", summary["preserve"]
            )
            settings_after = json.loads(
                (target / ".claude/settings.json").read_text(encoding="utf-8")
            )
            self.assertEqual(settings_after, settings_before)
            self.assertIn(".claude/settings.json", summary["preserve"])

    def test_install_rejects_non_directory_and_unsafe_targets(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            file_target = temporary_path / "not-a-directory"
            file_target.write_text("content", encoding="utf-8")
            missing_target = temporary_path / "missing"

            for target in (file_target, missing_target, Path("/")):
                with self.subTest(target=target):
                    result = self.run_installer(target, "--apply")
                    self.assertNotEqual(result.returncode, 0)
                    self.assertTrue(result.stdout, result.stderr)
                    summary = json.loads(result.stdout)
                    self.assertEqual(summary["create"], [])
                    self.assertEqual(summary["merge"], [])
                    self.assertEqual(summary["preserve"], [])
                    self.assertTrue(summary["warning"])

    def test_install_rejects_scaffold_type_collision_before_mutating_target(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory)
            (target / "CLAUDE.md").mkdir()

            result = self.run_installer(target, "--apply")

            self.assertNotEqual(result.returncode, 0)
            summary = json.loads(result.stdout)
            self.assertTrue(
                any("CLAUDE.md" in warning for warning in summary["warning"])
            )
            self.assertFalse(target.joinpath(".claude").exists())
            self.assertTrue(target.joinpath("CLAUDE.md").is_dir())

    def test_install_rejects_settings_symlink_without_changing_it_or_its_target(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory)
            claude_directory = target / ".claude"
            claude_directory.mkdir()
            symlink_target = claude_directory / "shared-settings.json"
            original_content = '{"customSetting": true}\n'
            symlink_target.write_text(original_content, encoding="utf-8")
            settings_path = claude_directory / "settings.json"
            settings_path.symlink_to(symlink_target.name)

            result = self.run_installer(target, "--apply")

            self.assertNotEqual(result.returncode, 0)
            summary = json.loads(result.stdout)
            self.assertTrue(
                any("symbolic link" in warning for warning in summary["warning"])
            )
            self.assertTrue(settings_path.is_symlink())
            self.assertEqual(symlink_target.read_text(encoding="utf-8"), original_content)
            self.assertEqual(
                set(claude_directory.iterdir()), {symlink_target, settings_path}
            )

    def test_install_rejects_different_existing_hook_before_mutating_target(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory)
            hooks_directory = target / ".claude" / "hooks"
            hooks_directory.mkdir(parents=True)
            existing_hook = hooks_directory / "session-end.py"
            existing_content = "raise SystemExit(7)\n"
            existing_hook.write_text(existing_content, encoding="utf-8")

            result = self.run_installer(target, "--apply")

            self.assertNotEqual(result.returncode, 0)
            summary = json.loads(result.stdout)
            self.assertTrue(
                any(
                    "different existing managed hook" in warning
                    and "session-end.py" in warning
                    for warning in summary["warning"]
                )
            )
            self.assertEqual(
                existing_hook.read_text(encoding="utf-8"), existing_content
            )
            self.assertFalse((target / ".claude/settings.json").exists())
            self.assertFalse((target / "CLAUDE.md").exists())

    def test_validate_rejects_modified_managed_hook(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory)
            self.parse_summary(self.run_installer(target, "--apply"))
            installed_hook = target / ".claude/hooks/session-end.py"
            installed_hook.write_text("raise SystemExit(7)\n", encoding="utf-8")

            result = self.run_installer(target, "--validate")

            self.assertNotEqual(result.returncode, 0)
            summary = json.loads(result.stdout)
            self.assertTrue(
                any(
                    "installed managed hook differs" in warning
                    and "session-end.py" in warning
                    for warning in summary["warning"]
                )
            )

    def test_atomic_replacements_preserve_asset_and_existing_settings_modes(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory)
            claude_directory = target / ".claude"
            claude_directory.mkdir()
            settings_path = claude_directory / "settings.json"
            settings_path.write_text('{"customSetting": true}\n', encoding="utf-8")
            settings_path.chmod(0o644)

            result = self.run_installer(target, "--apply")

            self.parse_summary(result)
            source_instructions = (
                SKILL_ROOT / "assets" / "project" / "CLAUDE.md"
            )
            installed_instructions = target / "CLAUDE.md"
            actual_modes = [
                stat.S_IMODE(installed_instructions.stat().st_mode),
                stat.S_IMODE(settings_path.stat().st_mode),
            ]
            expected_modes = [
                stat.S_IMODE(source_instructions.stat().st_mode),
                0o644,
            ]
            self.assertEqual(actual_modes, expected_modes)

    def test_session_start_emits_concise_context_with_pending_counts(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            project = Path(temporary_directory)
            learnings = project / ".claude/context/learnings"
            receipts = learnings / "receipts"
            pending = learnings / "pending"
            receipts.mkdir(parents=True)
            pending.mkdir()
            (receipts / "first.json").write_text("{}\n", encoding="utf-8")
            (receipts / "second.json").write_text("{}\n", encoding="utf-8")
            (pending / "proposal.md").write_text("proposal\n", encoding="utf-8")

            result = self.run_hook(
                SESSION_START_HOOK,
                project,
                {"hook_event_name": "SessionStart", "session_id": "session-1"},
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(result.stdout)
            output = json.loads(result.stdout)
            hook_output = output["hookSpecificOutput"]
            self.assertEqual(hook_output["hookEventName"], "SessionStart")
            context = hook_output["additionalContext"]
            self.assertIn("2 session receipt", context)
            self.assertIn("1 pending learning proposal", context)
            self.assertLess(len(context), 500)
            self.assertEqual(len(list(receipts.iterdir())), 2)
            self.assertEqual(len(list(pending.iterdir())), 1)

    def test_session_start_tolerates_malformed_input(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            project = Path(temporary_directory)
            secret = "malformed-secret-value"

            result = self.run_hook(
                SESSION_START_HOOK,
                project,
                raw_stdin=f'{{"unexpected":"{secret}"',
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(result.stdout)
            output = json.loads(result.stdout)
            self.assertEqual(
                output["hookSpecificOutput"]["hookEventName"], "SessionStart"
            )
            self.assertNotIn(secret, result.stdout + result.stderr)

    def test_session_end_writes_atomic_receipt_inside_project(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            project = Path(temporary_directory)
            transcript = project / "transcript.jsonl"
            transcript.write_text("transcript content\n", encoding="utf-8")
            payload = {
                "session_id": "session/../../unsafe identifier",
                "transcript_path": str(transcript),
                "cwd": str(project),
                "reason": "user_exit",
            }

            result = self.run_hook(SESSION_END_HOOK, project, payload)

            self.assertEqual(result.returncode, 0, result.stderr)
            receipts = project / ".claude/context/learnings/receipts"
            receipt_files = list(receipts.glob("*.json"))
            self.assertEqual(len(receipt_files), 1)
            self.assertEqual(list(receipts.iterdir()), receipt_files)
            receipt = json.loads(receipt_files[0].read_text(encoding="utf-8"))
            self.assertEqual(
                set(receipt),
                {"session_id", "transcript_path", "cwd", "reason", "timestamp"},
            )
            self.assertEqual(receipt["session_id"], payload["session_id"])
            self.assertEqual(receipt["transcript_path"], str(transcript))
            self.assertEqual(receipt["cwd"], str(project))
            self.assertEqual(receipt["reason"], "user_exit")
            self.assertTrue(receipt["timestamp"])

    def test_session_end_deduplicates_same_session(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            project = Path(temporary_directory)
            payload = {
                "session_id": "same-session",
                "transcript_path": str(project / "transcript.jsonl"),
                "cwd": str(project),
                "reason": "first",
            }

            first_result = self.run_hook(SESSION_END_HOOK, project, payload)
            receipts = project / ".claude/context/learnings/receipts"
            receipt_files = list(receipts.glob("*.json"))
            self.assertEqual(first_result.returncode, 0, first_result.stderr)
            self.assertEqual(len(receipt_files), 1)
            original_receipt = receipt_files[0].read_text(encoding="utf-8")

            payload["reason"] = "duplicate"
            second_result = self.run_hook(SESSION_END_HOOK, project, payload)

            self.assertEqual(second_result.returncode, 0, second_result.stderr)
            self.assertEqual(list(receipts.glob("*.json")), receipt_files)
            self.assertEqual(
                receipt_files[0].read_text(encoding="utf-8"), original_receipt
            )

    def test_session_end_rejects_cwd_outside_project(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            project = temporary_path / "project"
            outside = temporary_path / "outside"
            project.mkdir()
            outside.mkdir()
            outside_payload = {
                "session_id": "outside-session",
                "transcript_path": str(outside / "transcript.jsonl"),
                "cwd": str(outside),
                "reason": "user_exit",
            }
            valid_payload = {
                "session_id": "inside-session",
                "transcript_path": str(project / "transcript.jsonl"),
                "cwd": str(project),
                "reason": "user_exit",
            }

            outside_result = self.run_hook(SESSION_END_HOOK, project, outside_payload)
            valid_result = self.run_hook(SESSION_END_HOOK, project, valid_payload)

            self.assertEqual(outside_result.returncode, 0, outside_result.stderr)
            self.assertEqual(valid_result.returncode, 0, valid_result.stderr)
            receipts = project / ".claude/context/learnings/receipts"
            receipt_files = list(receipts.glob("*.json"))
            self.assertEqual(len(receipt_files), 1)
            receipt = json.loads(receipt_files[0].read_text(encoding="utf-8"))
            self.assertEqual(receipt["session_id"], "inside-session")
            self.assertNotIn("outside-session", receipt_files[0].read_text())

    def test_session_end_never_writes_transcript_content(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            project = Path(temporary_directory)
            transcript_secret = "TOP-SECRET-TRANSCRIPT-CONTENT"
            transcript = project / "transcript.jsonl"
            transcript.write_text(transcript_secret, encoding="utf-8")
            payload = {
                "session_id": "content-safety-session",
                "transcript_path": str(transcript),
                "cwd": str(project),
                "reason": "user_exit",
            }

            result = self.run_hook(SESSION_END_HOOK, project, payload)

            self.assertEqual(result.returncode, 0, result.stderr)
            receipt_files = list(
                project.glob(".claude/context/learnings/receipts/*.json")
            )
            self.assertEqual(len(receipt_files), 1)
            receipt_text = receipt_files[0].read_text(encoding="utf-8")
            self.assertNotIn(transcript_secret, receipt_text)
            self.assertEqual(
                json.loads(receipt_text)["transcript_path"], str(transcript)
            )

    def test_hooks_tolerate_deeply_nested_json_without_tracebacks_or_writes(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            project = Path(temporary_directory)
            adversarial_json = "[" * 10_000 + "0" + "]" * 10_000

            for hook in (SESSION_START_HOOK, SESSION_END_HOOK):
                with self.subTest(hook=hook.name):
                    result = self.run_hook(
                        hook, project, raw_stdin=adversarial_json
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertNotIn("Traceback", result.stderr)
            self.assertEqual(list(project.iterdir()), [])

    def test_session_start_does_not_follow_learning_directories_outside_project(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            project = temporary_path / "project"
            external_receipts = temporary_path / "external-receipts"
            external_pending = temporary_path / "external-pending"
            learnings = project / ".claude/context/learnings"
            learnings.mkdir(parents=True)
            external_receipts.mkdir()
            external_pending.mkdir()
            for index in range(3):
                (external_receipts / f"receipt-{index}.json").write_text("{}\n")
            for index in range(4):
                (external_pending / f"proposal-{index}.md").write_text("proposal\n")
            (learnings / "receipts").symlink_to(
                external_receipts, target_is_directory=True
            )
            (learnings / "pending").symlink_to(
                external_pending, target_is_directory=True
            )

            result = self.run_hook(SESSION_START_HOOK, project, {})

            self.assertEqual(result.returncode, 0, result.stderr)
            context = json.loads(result.stdout)["hookSpecificOutput"][
                "additionalContext"
            ]
            self.assertIn("0 session receipt", context)
            self.assertIn("0 pending learning proposal", context)
            self.assertNotIn("3 session receipt", context)
            self.assertNotIn("4 pending learning proposal", context)
            self.assertTrue((learnings / "receipts").is_symlink())
            self.assertTrue((learnings / "pending").is_symlink())

    def test_session_start_excludes_symlink_file_entries_from_counts(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            project = temporary_path / "project"
            receipts = project / ".claude/context/learnings/receipts"
            pending = project / ".claude/context/learnings/pending"
            receipts.mkdir(parents=True)
            pending.mkdir()
            (receipts / "real.json").write_text("{}\n", encoding="utf-8")
            (pending / "real.md").write_text("proposal\n", encoding="utf-8")
            external_receipt = temporary_path / "external-receipt.json"
            external_proposal = temporary_path / "external-proposal.md"
            external_receipt.write_text("external receipt metadata\n")
            external_proposal.write_text("external proposal metadata\n")
            (receipts / "linked.json").symlink_to(external_receipt)
            (pending / "linked.md").symlink_to(external_proposal)

            result = self.run_hook(SESSION_START_HOOK, project, {})

            self.assertEqual(result.returncode, 0, result.stderr)
            context = json.loads(result.stdout)["hookSpecificOutput"][
                "additionalContext"
            ]
            self.assertIn("1 session receipt", context)
            self.assertIn("1 pending learning proposal", context)
            self.assertNotIn("external", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
