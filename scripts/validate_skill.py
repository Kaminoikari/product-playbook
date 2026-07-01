import re, pathlib

_FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
_NAME = re.compile(r"^name:\s*(.+?)\s*$", re.MULTILINE)
_DESC = re.compile(r"^description:\s*(.+?)\s*$", re.MULTILINE | re.DOTALL)
_WORKFLOW_LEAK = re.compile(r"\bstep\s*1\b|\bthen\b.*\bthen\b", re.IGNORECASE)

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
    elif _WORKFLOW_LEAK.search(desc_m.group(1)):
        out.append("description: appears to summarize workflow (found step/then sequence)")
    if "provenance" not in body.lower():
        out.append("body: missing provenance instruction")
    if "language" not in body.lower():
        out.append("body: missing runtime language-detection line")
    return out
