#!/usr/bin/env python3
"""PreToolUse hook: advisory TDD gate for production-code writes.

Dev discipline is test-first: production code lands after a failing test
exists for it. This hook fires on Write / Edit / MultiEdit targeting a
code file, then looks for any test file whose name references the
target's stem (via `git ls-files` including untracked files, falling
back to a bounded directory walk). When no such test exists it injects a
one-line advisory `systemMessage`.

Advisory only, in the plugin's relative-guardrail style: it never denies
the call, fires at most once per file per session, and a
`.product-tdd-waived` marker in the working directory silences it
project-wide.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

CODE_EXTENSIONS = {
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs",
    ".py", ".rb", ".php", ".go", ".rs", ".java", ".kt",
    ".swift", ".cs", ".cpp", ".cc", ".c", ".h", ".hpp",
    ".vue", ".svelte", ".scala", ".dart", ".m", ".mm",
}

WATCHED_TOOLS = {"Write", "Edit", "MultiEdit"}

# Stems too generic to name a test after; for these, any test file in the
# repo counts as evidence that the project practices testing.
GENERIC_STEMS = {
    "index", "main", "app", "mod", "init", "__init__", "cli",
    "utils", "types", "constants", "config", "setup", "helpers",
}

_TEST_SEGMENT = re.compile(r"(^|[/_.\-])(test|spec)s?([/_.\-]|$)")

SKIP_DIRS = {
    ".git", "node_modules", "venv", ".venv", "__pycache__",
    "dist", "build", ".next", "target", "vendor", ".tox",
}
WALK_FILE_CAP = 5000


def _is_test_path(path: str) -> bool:
    return bool(_TEST_SEGMENT.search(Path(path).as_posix().lower()))


def _repo_files(base: Path) -> list[str]:
    """All file paths in the project, preferring git (tracked + untracked)."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(base), "ls-files", "--cached", "--others", "--exclude-standard"],
            capture_output=True, text=True, timeout=5,
        )
        if proc.returncode == 0:
            return proc.stdout.splitlines()
    except (OSError, subprocess.SubprocessError):
        pass
    found: list[str] = []
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            found.append(str(Path(dirpath, name).relative_to(base)))
            if len(found) >= WALK_FILE_CAP:
                return found
    return found


def _has_test_evidence(base: Path, stem: str) -> bool:
    test_files = [f for f in _repo_files(base) if _is_test_path(f)]
    if stem in GENERIC_STEMS:
        return bool(test_files)
    return any(stem in Path(f).name.lower() for f in test_files)


def _already_advised(session_id: str, target: str) -> bool:
    """Record `target` in the per-session state file; True if it was there."""
    state_file = Path(tempfile.gettempdir()) / f"pp-tdd-gate-{session_id}.json"
    advised: list[str] = []
    try:
        advised = json.loads(state_file.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        pass
    if target in advised:
        return True
    try:
        state_file.write_text(json.dumps(advised + [target]), encoding="utf-8")
    except OSError:
        pass
    return False


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    if payload.get("tool_name") not in WATCHED_TOOLS:
        return 0

    tool_input = payload.get("tool_input") or {}
    target = tool_input.get("file_path") or tool_input.get("path")
    if not isinstance(target, str) or not target:
        return 0

    suffix = Path(target).suffix.lower()
    if suffix not in CODE_EXTENSIONS or _is_test_path(target):
        return 0

    cwd = Path(payload.get("cwd") or os.getcwd())
    if (cwd / ".product-tdd-waived").is_file():
        return 0

    stem = Path(target).stem.lower()
    if _has_test_evidence(cwd, stem):
        return 0

    session_id = re.sub(r"[^A-Za-z0-9_-]", "", str(payload.get("session_id") or "default"))
    if _already_advised(session_id, target):
        return 0

    message = (
        f"[product-playbook] TDD gate: '{target}' looks like production code, "
        f"and no test referencing '{stem}' exists in this repo yet. Dev "
        "discipline is test-first: write the failing test, watch it fail, and "
        "only after that implement. If the user explicitly waived TDD or this "
        "change has no testable runtime surface, state the waiver in one line "
        "and proceed. A `.product-tdd-waived` file in the working directory "
        "silences this gate project-wide."
    )
    json.dump({"systemMessage": message}, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
