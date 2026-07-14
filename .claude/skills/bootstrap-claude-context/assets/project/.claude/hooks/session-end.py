#!/usr/bin/env python3
"""Record a minimal, reviewable receipt when a Claude Code session ends."""

import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RECEIPTS_PATH = Path(".claude/context/learnings/receipts")


def parse_input() -> dict[str, Any] | None:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError, RuntimeError, TypeError, ValueError):
        return None
    return payload if isinstance(payload, dict) else None


def text_value(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key, "")
    return value if isinstance(value, str) else ""


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def receipt_filename(session_id: str) -> str:
    safe_stem = re.sub(r"[^A-Za-z0-9_-]+", "-", session_id).strip("-_")
    safe_stem = (safe_stem or "session")[:48]
    digest = hashlib.sha256(session_id.encode("utf-8")).hexdigest()[:12]
    return f"{safe_stem}-{digest}.json"


def write_receipt(receipts: Path, filename: str, receipt: dict[str, str]) -> None:
    destination = receipts / filename
    if destination.exists() or destination.is_symlink():
        return

    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=receipts,
            prefix=".receipt-",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_name = temporary_file.name
            json.dump(receipt, temporary_file, indent=2, sort_keys=True)
            temporary_file.write("\n")
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        try:
            os.link(temporary_name, destination)
        except FileExistsError:
            pass
    finally:
        if temporary_name:
            Path(temporary_name).unlink(missing_ok=True)


def record_session(payload: dict[str, Any]) -> None:
    project_value = os.environ.get("CLAUDE_PROJECT_DIR")
    session_id = text_value(payload, "session_id")
    cwd_value = text_value(payload, "cwd")
    if not project_value or not session_id or not cwd_value:
        return

    project = Path(project_value).resolve()
    cwd = Path(cwd_value).resolve()
    if not project.is_dir() or not is_within(cwd, project):
        return

    receipts = project / RECEIPTS_PATH
    if not is_within(receipts.resolve(strict=False), project):
        return
    receipts.mkdir(parents=True, exist_ok=True)

    reason = text_value(payload, "reason") or text_value(payload, "end_reason")
    receipt = {
        "session_id": session_id,
        "transcript_path": text_value(payload, "transcript_path"),
        "cwd": cwd_value,
        "reason": reason,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    write_receipt(receipts, receipt_filename(session_id), receipt)


def main() -> int:
    payload = parse_input()
    if payload is None:
        return 0
    try:
        record_session(payload)
    except (OSError, RuntimeError, TypeError, ValueError):
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
