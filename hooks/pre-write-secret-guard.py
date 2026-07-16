#!/usr/bin/env python3
"""PreToolUse hook: pause writes that contain high-confidence credentials.

Dev discipline forbids hardcoded secrets and any agent-driven writes to
`.env` files. This hook scans the content a Write / Edit / MultiEdit is
about to land (new content only) against high-confidence credential
patterns (provider-specific key shapes and private-key blocks; no
generic `password = ...` heuristics, which drown in false positives).

On a match it returns `permissionDecision: "ask"` so the user makes the
call in one word. Lines that look like documentation placeholders
(example / dummy / redacted / <angle-bracket> values) are skipped. The
matched secret is never echoed back; the reason names only the pattern
and line number.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

WATCHED_TOOLS = {"Write", "Edit", "MultiEdit"}

SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("AWS access key id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("GitHub fine-grained PAT", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{22,}\b")),
    ("Anthropic API key", re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{20,}\b")),
    ("OpenAI API key", re.compile(r"\bsk-(?:proj|svcacct)-[A-Za-z0-9_\-]{20,}\b|\bsk-[A-Za-z0-9]{48}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9\-]{10,}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("Stripe live key", re.compile(r"\b[sr]k_live_[A-Za-z0-9]{24,}\b")),
    ("npm token", re.compile(r"\bnpm_[A-Za-z0-9]{36}\b")),
    ("private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
]

PLACEHOLDER = re.compile(
    r"example|placeholder|your[_\-]|x{4,}|dummy|fake|redacted|sample|<[^>]*>|\.\.\.",
    re.IGNORECASE,
)

ENV_TEMPLATE_NAMES = {".env.example", ".env.sample", ".env.template", ".env.dist"}


def _new_content(tool_name: str, tool_input: dict) -> str:
    if tool_name == "Write":
        return str(tool_input.get("content") or "")
    if tool_name == "Edit":
        return str(tool_input.get("new_string") or "")
    if tool_name == "MultiEdit":
        edits = tool_input.get("edits") or []
        return "\n".join(str(e.get("new_string") or "") for e in edits if isinstance(e, dict))
    return ""


def _is_env_file(target: str) -> bool:
    name = Path(target).name
    if name in ENV_TEMPLATE_NAMES:
        return False
    return name == ".env" or name.startswith(".env.")


def _find_secrets(content: str) -> list[str]:
    """Return human-readable hits like 'AWS access key id (line 12)'."""
    hits: list[str] = []
    for line_no, line in enumerate(content.splitlines(), start=1):
        if PLACEHOLDER.search(line):
            continue
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(line):
                hits.append(f"{label} (line {line_no})")
    return hits


def _ask(reason: str) -> None:
    json.dump({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": reason,
    }}, sys.stdout)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    tool_name = payload.get("tool_name")
    if tool_name not in WATCHED_TOOLS:
        return 0

    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        return 0
    target = tool_input.get("file_path") or tool_input.get("path") or ""

    if isinstance(target, str) and target and _is_env_file(target):
        _ask(
            f"[product-playbook] Secret guard: '{target}' is a .env file. Dev "
            "discipline is to never write .env files through the agent. "
            "Approve only if this is intentional."
        )
        return 0

    hits = _find_secrets(_new_content(tool_name, tool_input))
    if hits:
        _ask(
            "[product-playbook] Secret guard: content matches high-confidence "
            f"credential pattern(s): {'; '.join(hits)}. Hardcoded credentials "
            "belong in env vars or a secret manager. Approve only if this is "
            "intentional (for example a test fixture with a fabricated key)."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
