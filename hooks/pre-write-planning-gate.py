#!/usr/bin/env python3
"""PreToolUse hook: gate code-file writes during the planning phase.

The product-playbook plugin draws a hard line between PLANNING (produces
docs) and DEVELOPMENT (produces code). Until the user runs `/product-dev`
to enter the dev-handoff phase — which creates a `.product-dev-active`
marker file — Claude should not be writing source code.

This hook fires on Write / Edit / MultiEdit. If:
  • a planning session is in progress (progress file exists, not complete)
  • AND the dev-active marker is absent
  • AND the target path looks like source code

…it injects an advisory `systemMessage` reminding Claude to finish
planning first. The hook does NOT block the tool call (permissionDecision
remains unset / allowed) so the user retains an explicit override path.

Doc/text files (.md, .txt, .json, etc.) are always allowed — those are
expected planning artifacts.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

CODE_EXTENSIONS = {
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs",
    ".py", ".rb", ".php", ".go", ".rs", ".java", ".kt",
    ".swift", ".cs", ".cpp", ".cc", ".c", ".h", ".hpp",
    ".vue", ".svelte", ".scala", ".dart", ".m", ".mm",
}

WATCHED_TOOLS = {"Write", "Edit", "MultiEdit"}


def _planning_in_progress(progress_file: Path) -> bool:
    if not progress_file.is_file():
        return False
    try:
        body = progress_file.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False
    lowered = body.lower()
    if "status: complete" in lowered or "status：complete" in lowered:
        return False
    if re.search(r"status\s*[:：]\s*completed", lowered):
        return False
    return True


def _target_path(tool_name: str, tool_input: dict) -> str | None:
    if not isinstance(tool_input, dict):
        return None
    return tool_input.get("file_path") or tool_input.get("path")


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    tool_name = payload.get("tool_name")
    if tool_name not in WATCHED_TOOLS:
        return 0

    cwd = Path(payload.get("cwd") or os.getcwd())

    # Dev phase active → silent passthrough.
    if (cwd / ".product-dev-active").is_file():
        return 0

    if not _planning_in_progress(cwd / ".product-playbook-progress.md"):
        return 0

    target = _target_path(tool_name, payload.get("tool_input") or {})
    if not target:
        return 0

    suffix = Path(target).suffix.lower()
    if suffix not in CODE_EXTENSIONS:
        return 0

    message = (
        f"[product-playbook] Heads-up: '{target}' looks like source code, "
        "but this project is still in the PLANNING phase (no "
        "`.product-dev-active` marker). The plugin's contract is "
        "planning-produces-docs, dev-produces-code. Recommended: finish "
        "the current mode's remaining steps, then run `/product-dev` to "
        "enter the dev-handoff phase. If the user has explicitly asked "
        "for code now, acknowledge the override and proceed."
    )
    json.dump({"systemMessage": message}, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
