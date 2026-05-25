#!/usr/bin/env python3
"""Rewrite SKILL.md inside the Claude.ai bundle.

Claude.ai's skill upload caps description at 200 chars and the bundle
strips i18n/ to stay under the 200-file zip limit. The original
SKILL.md description is verbose (Claude Code has no such limit) and
its Language Detection block points at i18n/*/SKILL.md — both need
local rewrites for the Claude.ai bundle only.
"""

import pathlib
import re
import sys

SHORT_DESCRIPTION = (
    "MUST use when user wants to plan, design, or strategize a product "
    "or feature. 22 PM frameworks (JTBD, Persona, PR-FAQ, OST, North "
    "Star, MVP). Multilingual. Not for code or implementation."
)

LANGUAGE_BLOCK_REPLACEMENT = (
    "## 🌐 Language Detection\n"
    "\n"
    "Detect the language of the user's first message and respond in that "
    "language (English, 繁體中文, 日本語, 简体中文, Español, 한국어 all "
    "supported). Do not ask for confirmation; switch silently.\n"
)


def main(skill_path: str) -> int:
    if len(SHORT_DESCRIPTION) > 200:
        print(
            f"ERROR: SHORT_DESCRIPTION is {len(SHORT_DESCRIPTION)} chars "
            "(Claude.ai max is 200)",
            file=sys.stderr,
        )
        return 1

    path = pathlib.Path(skill_path)
    text = path.read_text(encoding="utf-8")

    # Replace the multi-line `description: |` block in YAML frontmatter
    # with a single-line description that fits Claude.ai's 200-char cap.
    new_text, n = re.subn(
        r"^description:\s*\|\n(?:[ \t]+.*\n)+",
        f"description: {SHORT_DESCRIPTION}\n",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if n != 1:
        print("ERROR: failed to rewrite description in SKILL.md", file=sys.stderr)
        return 1

    # Replace the Language Detection block (it points at i18n/ paths
    # that don't exist in the trimmed bundle).
    new_text, n = re.subn(
        r"## 🌐 Language Detection\n.*?(?=\n---\n)",
        LANGUAGE_BLOCK_REPLACEMENT.rstrip() + "\n",
        new_text,
        count=1,
        flags=re.DOTALL,
    )
    if n != 1:
        print(
            "WARN: Language Detection block not found — bundle may "
            "still reference i18n/ paths",
            file=sys.stderr,
        )

    path.write_text(new_text, encoding="utf-8")
    print(f"Rewrote {path} for Claude.ai upload "
          f"(description: {len(SHORT_DESCRIPTION)} chars)")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: _trim-skill-for-claude-ai.py <path-to-SKILL.md>",
              file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
