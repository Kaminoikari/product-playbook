#!/usr/bin/env python3
"""Shared environment helpers for the eval runners.

Isolates product-playbook from other installed plugins during a `claude -p`
eval run, so a trigger or behavioral score reflects product-playbook alone.
"""
from __future__ import annotations

import json
import os

# Plugins whose skills or SessionStart directives confound product-playbook
# measurement. superpowers injects a SessionStart "brainstorm first" directive
# that out-competes the meta-skill on ambiguous product prompts, so a trigger
# run in an env that also has superpowers under-reports triggering. Disabling a
# plugin that is not installed is a harmless no-op (e.g. a clean CI env), so
# this default is safe to leave on.
_DEFAULT_INTERFERING = "superpowers@claude-plugins-official"


def plugin_isolation_args() -> list[str]:
    """`claude` CLI args that disable known-interfering plugins for an eval run.

    Off when PRODUCT_PLAYBOOK_EVAL_ISOLATE=0. The disabled set defaults to
    superpowers and is overridable (comma-separated) via
    PRODUCT_PLAYBOOK_EVAL_DISABLE_PLUGINS; an empty set returns []. `--settings`
    merges over the user's settings, so only the named plugins flip to false
    while product-playbook, login, and everything else stay intact.
    """
    if os.environ.get("PRODUCT_PLAYBOOK_EVAL_ISOLATE", "1") == "0":
        return []
    raw = os.environ.get("PRODUCT_PLAYBOOK_EVAL_DISABLE_PLUGINS", _DEFAULT_INTERFERING)
    names = [n.strip() for n in raw.split(",") if n.strip()]
    enabled: dict[str, bool] = {name: False for name in names}
    # Force-enable the plugin under test. The user may scope product-playbook
    # per-project (user-level enabledPlugins false + a repo-local true), and
    # evals run `claude -p` from $HOME where only the user-level false applies:
    # without this line the plugin never loads headless and every
    # should_trigger case is a structural zero regardless of model or content.
    if os.environ.get("PRODUCT_PLAYBOOK_EVAL_ENSURE_SELF", "1") != "0":
        enabled["product-playbook@skills-dir"] = True
    if not enabled:
        return []
    return ["--settings", json.dumps({"enabledPlugins": enabled})]
