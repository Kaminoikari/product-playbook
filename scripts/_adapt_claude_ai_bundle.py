"""Pure adaptation functions for the Claude.ai custom skill bundle.

Claude.ai Custom Skills caps the frontmatter description at 200 chars and
resolves file references relative to the skill folder. The plugin sources
use ``${CLAUDE_PLUGIN_ROOT}`` paths and per-lens SKILL.md frontmatter, so
the bundle build adapts them:

  adapt_meta(text)        meta-skill SKILL.md for the bundle root
  adapt_lens(name, text)  body-only lens doc for lenses/<name>.md

scripts/build-claude-ai-bundle.sh drives these functions; unit tests in
tests/test_claude_ai_bundle.py import them directly.
"""

from __future__ import annotations

import re

DESCRIPTION_MAX_CHARS = 200

SHORT_DESCRIPTION = (
    "MUST use when the user wants to plan, validate, scope, or strategize "
    "a product or feature. Composable product-thinking lenses (JTBD, "
    "PR-FAQ, pre-mortem, RICE, MVP) that blend to fit the outcome."
)

LENS_MAPPING_NOTE = (
    " Each lens body lives in lenses/<name>.md next to this file; "
    "read the one(s) you select before producing."
)

RECIPES_PLUGIN_PATH = "${CLAUDE_PLUGIN_ROOT}/references/recipes/"
RECIPES_BUNDLE_PATH = "recipes/"

ASSETS_PLUGIN_PATH = "${CLAUDE_PLUGIN_ROOT}/skills/document-export/assets/"
ASSETS_BUNDLE_PATH = "assets/"

# Matches a `description:` line plus any indented continuation lines, so
# both single-line and block-scalar YAML descriptions are covered.
_DESCRIPTION_RE = re.compile(
    r"^description:(?:[ \t].*)?(?:\n[ \t]+\S.*)*", re.MULTILINE
)

_AVAILABLE_LENSES_RE = re.compile(r"^Available lenses:.*$", re.MULTILINE)

_FRONTMATTER_RE = re.compile(r"\A---\n.*?\n---[ \t]*\n", re.DOTALL)


def adapt_meta(text: str) -> str:
    """Adapt the meta-skill SKILL.md content for the bundle root.

    Swaps in a description that fits the Claude.ai cap, appends the
    lenses/ mapping note to the "Available lenses:" line, and points the
    recipe references at the bundled recipes/ folder.
    """
    if len(SHORT_DESCRIPTION) > DESCRIPTION_MAX_CHARS:
        raise ValueError(
            f"SHORT_DESCRIPTION is {len(SHORT_DESCRIPTION)} chars; "
            f"Claude.ai caps descriptions at {DESCRIPTION_MAX_CHARS}"
        )

    adapted, replaced = _DESCRIPTION_RE.subn(
        "description: " + SHORT_DESCRIPTION, text, count=1
    )
    if replaced != 1:
        raise ValueError(
            "meta-skill frontmatter has no description line to replace"
        )

    adapted, replaced = _AVAILABLE_LENSES_RE.subn(
        lambda match: match.group(0).rstrip() + LENS_MAPPING_NOTE,
        adapted,
        count=1,
    )
    if replaced != 1:
        raise ValueError("meta-skill body has no 'Available lenses:' line")

    return adapted.replace(RECIPES_PLUGIN_PATH, RECIPES_BUNDLE_PATH)


def adapt_lens(name: str, text: str) -> str:
    """Return the body of a lens SKILL.md for lenses/<name>.md.

    Strips the YAML frontmatter block; lens bodies already open with a
    ``#`` heading. For document-export the bundled asset references are
    pointed at the assets/ folder next to the bundle-root SKILL.md.
    """
    match = _FRONTMATTER_RE.match(text)
    if match is None:
        raise ValueError(f"lens '{name}' has no YAML frontmatter to strip")
    body = text[match.end():].lstrip("\n")
    if name == "document-export":
        body = body.replace(ASSETS_PLUGIN_PATH, ASSETS_BUNDLE_PATH)
    return body
