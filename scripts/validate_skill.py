import re, pathlib

_FRONTMATTER = re.compile(r"---\n(.*?)\n---\n", re.DOTALL)
_NAME = re.compile(r"^name:\s*(.+?)\s*$", re.MULTILINE)
_DESC = re.compile(r"^description:\s*(.+?)\s*$", re.MULTILINE)
_BLOCK_SCALAR_INDICATORS = ("|", "|-", "|+", ">", ">-", ">+")
_WORKFLOW_LEAK = re.compile(r"\bstep\s*1\b|\bthen\b.*\bthen\b", re.IGNORECASE)


def _extract_description(frontmatter: str, desc_match: "re.Match[str]") -> str:
    """Return the logical description text.

    Handles both a plain scalar (``description: some text``) and a YAML
    block scalar (``description: |`` followed by indented continuation
    lines), joining the continuation lines into one string so the
    workflow-leak heuristic can see the real content instead of just the
    block-scalar indicator character.
    """
    value = desc_match.group(1)
    if value not in _BLOCK_SCALAR_INDICATORS:
        return value
    continuation_lines = []
    for line in frontmatter[desc_match.end():].splitlines():
        if line.strip() == "":
            continue
        if line[:1] not in (" ", "\t"):
            break
        continuation_lines.append(line.strip())
    return " ".join(continuation_lines)


def validate_skill(path: str) -> list[str]:
    text = pathlib.Path(path).read_text(encoding="utf-8")
    out = []
    m = _FRONTMATTER.match(text)
    if not m:
        return ["frontmatter: missing leading --- ... --- block"]
    fm, body = m.group(1), text[m.end():]
    if len(m.group(0)) > 1024:
        out.append("frontmatter: block exceeds 1024 characters")
    name_m = _NAME.search(fm)
    if not name_m:
        out.append("name: missing")
    elif not re.fullmatch(r"[a-z0-9-]+", name_m.group(1)):
        out.append(f"name: '{name_m.group(1)}' must match ^[a-z0-9-]+$")
    desc_m = _DESC.search(fm)
    if not desc_m:
        out.append("description: missing")
    else:
        description = _extract_description(fm, desc_m)
        if _WORKFLOW_LEAK.search(description):
            out.append("description: appears to summarize workflow (found step/then sequence)")
    if "provenance" not in body.lower():
        out.append("body: missing provenance instruction")
    if "language" not in body.lower():
        out.append("body: missing runtime language-detection line")
    return out
