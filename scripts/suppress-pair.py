#!/usr/bin/env python3
"""Append a (file, eval_name) pair to docs/loop-suppressions.jsonl.

K3: M7 added the suppression reader but not a writer. Without this, the
human has to hand-edit JSONL with the right shape every time they want to
mute a pair — annoying enough to skip, which defeats the feature.

Usage:
  python3 scripts/suppress-pair.py \\
    --file references/02b-jtbd.md \\
    --eval eval-jtbd-depth \\
    --reason "hand-tuning the priority-rule wording in branch foo"

Idempotent: if the (file, eval_name) pair is already present, prints "exists"
and exits 0 without re-appending. Validates --eval against EVAL_ATTRIBUTION
keys (warns if unknown; doesn't block — eval names sometimes precede their
attribution entry).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import date
from pathlib import Path

DEFAULT_PATH = Path("docs") / "loop-suppressions.jsonl"
SCRIPTS = Path(__file__).parent


def _existing_pairs(path: Path) -> set[tuple[str, str]]:
    spec = importlib.util.spec_from_file_location("_suppressions",
                                                    SCRIPTS / "_suppressions.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.load_suppressions(path)


def _known_evals() -> set[str]:
    try:
        spec = importlib.util.spec_from_file_location("debt", SCRIPTS / "eval-debt-report.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return set(mod.EVAL_ATTRIBUTION.keys())
    except (ImportError, OSError, AttributeError):
        return set()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", required=True,
                    help="Repo-relative path being patched (e.g. references/02b-jtbd.md)")
    ap.add_argument("--eval", dest="eval_name", required=True,
                    help="Eval name (e.g. eval-jtbd-depth)")
    ap.add_argument("--reason", default="",
                    help="One-line note for future-you about why this pair is muted")
    ap.add_argument("--path", type=Path, default=DEFAULT_PATH,
                    help="Override suppressions file path (default: docs/loop-suppressions.jsonl)")
    ap.add_argument("--allow-unknown-eval", action="store_true",
                    help="Don't warn if --eval isn't in EVAL_ATTRIBUTION")
    args = ap.parse_args()

    key = (args.file, args.eval_name)
    existing = _existing_pairs(args.path)
    if key in existing:
        print(f"exists: ({args.file}, {args.eval_name}) already suppressed", file=sys.stderr)
        return 0

    known = _known_evals()
    if known and args.eval_name not in known and not args.allow_unknown_eval:
        print(f"⚠️  {args.eval_name!r} is not in EVAL_ATTRIBUTION. Either it's "
              f"a typo, or the eval predates its attribution entry. Pass "
              f"--allow-unknown-eval to suppress anyway.", file=sys.stderr)
        print(f"   known evals: {sorted(known)[:5]}...", file=sys.stderr)
        return 2

    record = {
        "file": args.file,
        "eval_name": args.eval_name,
        "reason": args.reason or "(no reason given)",
        "added": date.today().isoformat(),
    }
    args.path.parent.mkdir(parents=True, exist_ok=True)
    with args.path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"appended to {args.path}: {record}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
