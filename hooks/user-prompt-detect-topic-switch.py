#!/usr/bin/env python3
"""UserPromptSubmit hook: detect change-propagation triggers.

Advisory reminder, active only when a planning session is in progress
(signalled by a `.product-playbook-progress.md` whose status is not
"complete"): if the prompt contains keywords that suggest revising an
earlier step (e.g. "改 step 2", "update persona", "重做 JTBD"), remind
Claude to apply `references/rules-change-propagation.md` so downstream
artifacts stay consistent.

The reminder is advisory: the hook never blocks the user prompt. It
emits a JSON `systemMessage` that surfaces in Claude's context.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

CHANGE_PROPAGATION_PATTERNS = [
    r"改\s*(step|步驟|S\d)",
    r"重做\s*(step|步驟|S\d|JTBD|Persona|MVP|North\s*Star)",
    r"重新\s*(做|寫|算).*(step|步驟|JTBD|Persona|MVP)",
    r"修改.*(step|步驟|JTBD|Persona|MVP|North\s*Star)",
    r"\bupdate\s+(step|persona|jtbd|mvp|north\s*star)",
    r"\brewrite\s+(step|persona|jtbd|mvp)",
    r"\bredo\s+(step|persona|jtbd|mvp)",
    r"\bchange\s+(step|persona|jtbd|mvp|north\s*star)",
]


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


def _matches_any(prompt: str, patterns: list[str]) -> bool:
    return any(re.search(p, prompt, re.IGNORECASE) for p in patterns)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    prompt = (payload.get("user_prompt") or "").strip()
    if not prompt:
        return 0

    cwd = payload.get("cwd") or os.getcwd()
    progress = Path(cwd) / ".product-playbook-progress.md"
    if not _planning_in_progress(progress):
        return 0

    if not _matches_any(prompt, CHANGE_PROPAGATION_PATTERNS):
        return 0

    message = (
        "[product-playbook] Change intent detected. Apply "
        "`references/rules-change-propagation.md`: identify which "
        "downstream tables depend on the modified step, update them in "
        "lock-step, and surface the propagation summary to the user."
    )
    json.dump({"systemMessage": message}, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
