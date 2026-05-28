#!/usr/bin/env python3
"""UserPromptSubmit hook: enforce specialist sub-agent dispatch.

The product-playbook skill has three specialist sub-agents
(discovery-specialist, strategy-critic, pre-mortem-runner). When a
user message clearly matches one specialist's scope — e.g. pastes a
strategy and asks for review, or asks for Persona/JTBD analysis — the
main agent SHOULD dispatch via the Task tool with the matching
`subagent_type`. In single-shot `claude -p` mode, the main agent
strongly tends to inline-handle the request instead, because the
direct ask outranks the dispatch protocol prose in SKILL.md.

This hook closes that gap at the harness layer. On every user prompt,
it pattern-matches against trigger phrases for each specialist. If a
match fires, it emits a `systemMessage` reminding the agent that
dispatch is required (with the exact Task tool invocation shape).
The hook never blocks the user prompt; it just makes the dispatch
protocol unmissable.

Pattern strictness — these are intentional false-positive-tolerant.
A spurious dispatch reminder costs the agent one re-read of SKILL.md's
dispatch table (cheap). A missed dispatch costs an inline-simulated
specialist response that the eval (and the user) will not trust
(expensive).
"""

from __future__ import annotations

import json
import re
import sys


# Each entry: (specialist subagent_type, list of regex patterns).
# Patterns are case-insensitive. Match ANY pattern → fire that specialist.
SPECIALIST_TRIGGERS: list[tuple[str, list[str]]] = [
    (
        "strategy-critic",
        [
            # Direct ask to review/critique strategy-shaped artifact
            r"\breview\s+(this|our|the|my)\s+strategy\b",
            r"\bcritique\s+(this|our|the|my)\s+strategy\b",
            r"\bhow\s+strong\s+is\s+(this|our|the|my)\s+strategy\b",
            r"\btell\s+me\s+how\s+strong\s+this\s+strategy\s+is\b",
            # User pastes a strategy artifact (mission/vision/strategy triplet)
            r"\bour\s+mission\s+is\b.*\bour\s+(vision|strategy)\s+is\b",
            r"\bour\s+strategy\s+is\b",
            # Rumelt / DHM / Empowered Teams artifacts
            r"\b(diagnosis|guiding\s+policy|coherent\s+action)\b.*\b(diagnosis|guiding\s+policy|coherent\s+action)\b",
            r"\bdhm\s+(model|critique|analysis)\b",
            r"\bempowered\s+team(s)?\s+charter\b",
        ],
    ),
    (
        "discovery-specialist",
        [
            # Direct ask for Persona/JTBD/OST/Journey/Continuous Discovery
            r"\b(produce|generate|create|do|run)\s+(the\s+)?(persona|jtbd|journey\s+map|opportunity\s+solution\s+tree|ost)\b",
            r"\b(persona\s+and\s+jtbd|jtbd\s+and\s+persona)\b",
            r"\bjtbd\s+analysis\b",
            r"\bpersona\s+analysis\b",
            r"\b(continuous|ongoing)\s+discovery\b",
            r"\bjobs[\s\-]+to[\s\-]+be[\s\-]+done\b",
        ],
    ),
    (
        "pre-mortem-runner",
        [
            r"\bpre[\s\-]?mortem\b",
            r"\bwhat\s+could\s+go\s+wrong\b",
            r"\brisk\s+analysis\s+(for|on|of)\b",
            r"\bfailure\s+modes?\b",
        ],
    ),
]


REMINDER_TEMPLATE = (
    "[product-playbook] DISPATCH ENFORCEMENT — the user's prompt is in "
    "the operating scope of the `{specialist}` sub-agent. You MUST "
    "delegate via the Task tool. Inline-handling this request (answering "
    "the user's question yourself) is the failure mode this hook exists "
    "to prevent — the sub-agent's focused context produces materially "
    "higher-quality output than you can inline.\n\n"
    "Required response shape (in this order, no exceptions):\n\n"
    "1. Your first line of output, verbatim:\n\n"
    "   > Dispatching to `{specialist}` subagent via Task tool with "
    "`subagent_type={specialist}`.\n\n"
    "2. Immediately after, call the Task tool:\n\n"
    "   Task(\n"
    "     subagent_type=\"{specialist}\",\n"
    "     description=\"<short 2-3 word summary>\",\n"
    "     prompt=\"<paste the user's original prompt verbatim, then add a "
    "final line: 'Reply in [user's working language].'>\"\n"
    "   )\n\n"
    "3. After the sub-agent returns YAML, integrate its output into your "
    "reply to the user.\n\n"
    "Do NOT do any of the following before the Task call:\n"
    "- Produce a Persona / JTBD / strategy critique / pre-mortem yourself.\n"
    "- Add prose, mode menus, progress indicators, or any explanation.\n"
    "- Skip the Task call because you 'already know the answer.'\n\n"
    "Only false-positive exception: if the prompt genuinely has no "
    "connection to `{specialist}`'s scope, say so in one short sentence, "
    "then proceed without dispatch. When in doubt, dispatch — the "
    "sub-agent's `status: out_of_scope` reply cleanly bounces back."
)


def detect_specialists(prompt: str) -> list[str]:
    """Return list of specialist names whose patterns match the prompt."""
    matched: list[str] = []
    for specialist, patterns in SPECIALIST_TRIGGERS:
        for pattern in patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                matched.append(specialist)
                break  # one pattern is enough per specialist
    return matched


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    prompt = (payload.get("user_prompt") or "").strip()
    if not prompt:
        return 0

    matched = detect_specialists(prompt)
    if not matched:
        return 0

    messages = [REMINDER_TEMPLATE.format(specialist=s) for s in matched]
    output = {"systemMessage": "\n\n---\n\n".join(messages)}
    json.dump(output, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
