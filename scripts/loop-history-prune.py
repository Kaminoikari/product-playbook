#!/usr/bin/env python3
"""Prune docs/loop-history.jsonl to keep recent ticks only.

N3 of the closed-loop initiative. loop-history.jsonl grows unbounded — one
record per tick, with daily ticks that's 365 records/year, and loop-summary
re-reads the whole file every invocation. Most of the analytic logic only
looks at the last 2-3 records anyway.

This script keeps the most recent --keep-last N records and either:
  - discards the rest (default), OR
  - moves them into docs/loop-history-archive-<year>.jsonl with --archive

Both flows are deterministic and idempotent. Safe to run as a cron or as
part of a release checklist.

Exit codes:
  0  pruned successfully (or already within limit)
  1  history file not found / not readable
  2  --dry-run requested; nothing written
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_HISTORY = Path("docs") / "loop-history.jsonl"


def _read(history_path: Path) -> list[str]:
    """Return the raw lines (preserving JSON text), skipping blank lines."""
    if not history_path.is_file():
        return []
    lines = []
    for line in history_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            lines.append(line)
    return lines


def _archive_path(record_line: str, base_dir: Path) -> Path:
    """Group archived records by year, derived from the record's timestamp."""
    year = "unknown"
    try:
        rec = json.loads(record_line)
        ts = rec.get("timestamp") or ""
        if ts:
            year = ts[:4]
    except json.JSONDecodeError:
        pass
    return base_dir / f"loop-history-archive-{year}.jsonl"


def prune(history_path: Path, keep_last: int, archive: bool, dry_run: bool) -> dict:
    lines = _read(history_path)
    if not lines:
        return {"action": "noop", "reason": "no records found", "kept": 0, "archived": 0}

    if len(lines) <= keep_last:
        return {"action": "noop", "reason": f"only {len(lines)} record(s) — within "
                f"keep-last={keep_last}", "kept": len(lines), "archived": 0}

    to_archive = lines[:-keep_last]
    to_keep = lines[-keep_last:]
    if dry_run:
        return {"action": "dry-run", "reason": "no files written (--dry-run)",
                "kept": len(to_keep), "would_archive": len(to_archive)}

    archived_count = 0
    if archive:
        archives_by_path: dict[Path, list[str]] = {}
        for line in to_archive:
            archives_by_path.setdefault(_archive_path(line, history_path.parent),
                                        []).append(line)
        for path, recs in archives_by_path.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8") as f:
                for r in recs:
                    f.write(r + "\n")
            archived_count += len(recs)

    history_path.write_text("\n".join(to_keep) + "\n", encoding="utf-8")
    return {"action": "pruned", "kept": len(to_keep),
            "archived": archived_count if archive else 0,
            "discarded": (len(to_archive) - archived_count) if archive else len(to_archive)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--history", type=Path, default=DEFAULT_HISTORY)
    ap.add_argument("--keep-last", type=int, default=30,
                    help="Number of most-recent records to retain (default 30)")
    ap.add_argument("--archive", action="store_true",
                    help="Move pruned records into docs/loop-history-archive-<year>.jsonl "
                         "instead of discarding")
    ap.add_argument("--dry-run", action="store_true",
                    help="Report what would change, don't write")
    args = ap.parse_args()

    if not args.history.is_file():
        print(f"❌ history file not found: {args.history}", file=sys.stderr)
        return 1

    result = prune(args.history, args.keep_last, args.archive, args.dry_run)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if result["action"] == "dry-run" else 0


if __name__ == "__main__":
    sys.exit(main())
