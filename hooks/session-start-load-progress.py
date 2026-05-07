#!/usr/bin/env python3
"""SessionStart hook: auto-load product-playbook progress / context.

Detects `.product-playbook-progress.md` and `.product-context.md` in the
session's working directory. If either exists, their contents are injected
as additional context so Claude can resume the planning flow without
re-reading them manually.

Hook contract:
- Reads JSON payload from stdin (Claude Code provides session metadata).
- On exit code 0, stdout is fed back to Claude as session context.
- Silent (no output) when no playbook state is found, so non-PM projects
  are unaffected.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

MAX_BYTES_PER_FILE = 16 * 1024  # cap each file to keep injected context small


def _read_capped(path: Path) -> str | None:
    try:
        data = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if len(data) > MAX_BYTES_PER_FILE:
        data = data[:MAX_BYTES_PER_FILE] + "\n... (truncated by hook)\n"
    return data


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        payload = {}

    cwd = payload.get("cwd") or os.getcwd()
    cwd_path = Path(cwd)

    targets = [
        ("Planning progress", cwd_path / ".product-playbook-progress.md"),
        ("Product context", cwd_path / ".product-context.md"),
    ]

    sections: list[str] = []
    for label, path in targets:
        if not path.is_file():
            continue
        body = _read_capped(path)
        if body is None:
            continue
        sections.append(f"### {label} ({path.name})\n\n{body}")

    if not sections:
        return 0

    header = (
        "[product-playbook] Existing planning state was detected in this "
        "project. Resume from where the user left off — do NOT restart from "
        "step 1. Reference the snapshot below before responding."
    )
    additional_context = header + "\n\n" + "\n\n---\n\n".join(sections)

    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": additional_context,
        }
    }
    json.dump(output, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
