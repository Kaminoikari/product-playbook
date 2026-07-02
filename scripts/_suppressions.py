"""Loop suppressions — manual mute list for known-in-progress pairs.

M7: when the human knows a particular (file, eval_name) pair is being handled
manually (e.g., a Hard Gate is being hand-tuned and patch-proposer's auto
attempts keep getting overridden), record it here. patch-proposer skips
suppressed pairs entirely; attribution-check filters them out of suspects;
loop-summary's stall detection ignores them when judging whether the loop
has stalled.

Format: docs/loop-suppressions.jsonl, one JSON object per line:
    {"file": "skills/jtbd/SKILL.md", "eval_name": "jtbd-depth",
     "reason": "hand-tuning the priority-rule wording in branch foo",
     "added": "2026-05-29"}

Lines without `file` and `eval_name` are skipped silently. Comments via
`# ...` lines are tolerated.
"""

from __future__ import annotations

import json
from pathlib import Path

DEFAULT_PATH = Path("docs") / "loop-suppressions.jsonl"


def load_suppressions(path: Path | None = None) -> set[tuple[str, str]]:
    """Return a set of (file, eval_name) pairs to mute."""
    p = path or DEFAULT_PATH
    if not p.is_file():
        return set()
    out: set[tuple[str, str]] = set()
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        f = rec.get("file")
        e = rec.get("eval_name")
        if f and e:
            out.add((f, e))
    return out
