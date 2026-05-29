"""Eval freshness check — shared helper.

Detects the silent-foot-gun where someone runs lift-report / patch-proposer /
attribution-check against an `eval-results.behavioral.json` that pre-dates the
last edit to a watched authored file (references/, agents/, i18n/, SKILL.md).
In that case the eval is stale: it does not reflect the current code, and any
report built on it draws wrong conclusions.

Usage:
    from _freshness import check_eval_freshness
    is_fresh, reason = check_eval_freshness(eval_path, repo_root)
    if not is_fresh and not args.force:
        print(f"❌ {reason}", file=sys.stderr)
        sys.exit(2)

Watched paths (any descendant .md file counts):
  references/   agents/   i18n/   SKILL.md
Plus the eval spec itself:
  evals/evals.json — if the eval spec changes, old eval-results no longer
                     match the current contract even if no .md file changed.
"""

from __future__ import annotations

from pathlib import Path

try:
    from _config import WATCHED  # M6: centralised
except ImportError:
    # fallback when imported via importlib without sys.path adjustment
    WATCHED = ["references", "agents", "i18n", "SKILL.md", "evals/evals.json"]


def _latest_authored_mtime(root: Path) -> tuple[float, Path | None]:
    latest = 0.0
    latest_path: Path | None = None
    for entry in WATCHED:
        p = root / entry
        if not p.exists():
            continue
        candidates = [p] if p.is_file() else list(p.rglob("*.md"))
        for f in candidates:
            try:
                m = f.stat().st_mtime
            except OSError:
                continue
            if m > latest:
                latest = m
                latest_path = f
    return latest, latest_path


def check_eval_freshness(eval_path: Path, root: Path) -> tuple[bool, str]:
    """Return (is_fresh, reason).

    is_fresh = True when eval_path mtime >= latest authored-file mtime.
    On False, reason describes which file is newer and by how much, with the
    suggested remediation.
    """
    try:
        eval_mtime = eval_path.stat().st_mtime
    except OSError as e:
        return False, f"cannot stat {eval_path}: {e}"

    latest, latest_path = _latest_authored_mtime(root)
    if latest_path is None:
        return True, ""  # nothing to compare against; trust the eval

    if eval_mtime >= latest:
        return True, ""

    delta_min = (latest - eval_mtime) / 60
    rel = latest_path.relative_to(root) if root in latest_path.parents else latest_path
    return False, (
        f"eval JSON `{eval_path}` is OLDER than authored file `{rel}` by "
        f"{delta_min:.1f} min — eval was run BEFORE the latest edit, so the "
        f"report would draw wrong conclusions. Re-run eval (npm run "
        f"eval:behavioral) and try again. Override with --force if you "
        f"genuinely want stale-eval behavior (e.g., debugging the harness)."
    )
