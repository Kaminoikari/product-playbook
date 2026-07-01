"""Centralised tunables for the closed-loop harness scripts.

M6: each LLM-using script previously defined its own MAX_INPUT_CHARS and
CLAUDE_TIMEOUT_SECONDS constants. They drifted over time (mirror agent
used 600s, lift report didn't have one, etc.). This module is the single
import-once source.

All values are overridable by environment variable. Convention:
    PRODUCT_PLAYBOOK_<UPPERCASE_KEY>

Example:
    PRODUCT_PLAYBOOK_CLAUDE_TIMEOUT_SECONDS=900 python3 scripts/patch-proposer.py ...

Why env-driven instead of CLI flags: most callers are scripts invoking each
other via subprocess, and threading a flag through every layer is noise.
Env vars cross the subprocess boundary automatically.
"""

from __future__ import annotations

import os


def _getenv_int(key: str, default: int) -> int:
    raw = os.environ.get(f"PRODUCT_PLAYBOOK_{key}")
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


# LLM subprocess tunables
CLAUDE_TIMEOUT_SECONDS = _getenv_int("CLAUDE_TIMEOUT_SECONDS", 600)
MAX_INPUT_CHARS = _getenv_int("MAX_INPUT_CHARS", 36_000)
MAX_RETRIES = _getenv_int("MAX_RETRIES", 2)

# loop-tick wraps each Stage in subprocess.run(timeout=...). Must be >=
# CLAUDE_TIMEOUT_SECONDS × expected concurrent LLM calls. With --max 3 +
# --multi-file fan-out to ~2 primaries each, worst-case patch-proposer is
# 6 × CLAUDE_TIMEOUT_SECONDS. Default 1800s covers typical --max 3 runs;
# bump via PRODUCT_PLAYBOOK_LOOP_SUBPROCESS_TIMEOUT when running --multi-file.
LOOP_SUBPROCESS_TIMEOUT = _getenv_int("LOOP_SUBPROCESS_TIMEOUT", 1800)

# Severity weights (used by eval-debt-report scoring and lift computation)
SEVERITY_WEIGHTS = {"critical": 15, "warning": 5, "info": 1}

# Score → band thresholds
BAND_HEALTHY = _getenv_int("BAND_HEALTHY", 90)
BAND_NEEDS_ATTENTION = _getenv_int("BAND_NEEDS_ATTENTION", 70)

# Loop convergence rules
STALL_SCORE_TOLERANCE = _getenv_int("STALL_SCORE_TOLERANCE", 5)
REGRESSION_SCORE_DROP = _getenv_int("REGRESSION_SCORE_DROP", 5)

# Canonical vocabulary tokens — must remain English across all i18n
CANONICAL_VOCAB = [
    "fear", "anxiety", "shame", "worry", "dread",
    "self-doubt", "sense of loss", "threat to identity",
    "embarrassment", "guilt",
]

# Watched authored-file roots for eval freshness comparison
WATCHED = ["references", "agents", "SKILL.md", "evals/evals.json"]
