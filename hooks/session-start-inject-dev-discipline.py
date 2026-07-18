import json, os, sys, pathlib

DIGEST = """<PRODUCT-PLAYBOOK-DEV-DISCIPLINE>
These gates apply whenever the session moves into implementation: writing or modifying source code, building a feature, fixing a bug, or closing out a branch. They are dormant during planning, research, and conversation; product planning stays with the product-playbook meta-skill.

0. Right-size first: plan mode only for real architectural ambiguity; a single-purpose diff under ~30 lines with a green focused test skips reviewer subagents (inline review + launch check instead); large tasks write a plan contract (outcome-based acceptance criteria, Non-goals, verification plan) to docs/plans/ before implementing.
1. TDD first: write the failing test and watch it fail before writing production code; every bug fix starts from a failing reproduction test. No test theater: never hard-code expected values, start past the unit, re-implement it in the test, or skip the real entry path. Waivers (user said skip, or no testable runtime surface) are stated in one line, never silent.
2. Scope integrity: build exactly what was agreed; flag out-of-scope discoveries in one line without silently fixing or expanding.
3. Security hygiene: no hardcoded secrets, never touch .env files, validate inputs at system boundaries, and treat payments, auth, permissions, and migrations as high-risk surfaces.
4. Subagent economy: implement inline by default; use subagents only for parallel independent research or exploration that you synthesize afterwards. When dispatching: task instruction last, file paths instead of pasted content, I/O contract declared, cheap models for mechanical roles.
5. Independent review: save test output (and frontend screenshots) to scratch, then dispatch two fresh-context read-only reviewers in parallel: a code reviewer judging the diff, and a spec reviewer checking diff (plus plan-file diff) against the agreed requirements. Reviewers audit the saved evidence rather than rebuilding it, never invent requirements beyond the contract, hold the bar constant across rounds (prior gaps first), and end with VERDICT: PASS or VERDICT: FAIL (missing verdict = FAIL). Identical findings two rounds running, or three rounds total: stop and escalate to the user.
6. Finish the branch: full test suite green with real output, entry-point launch check (run the real CLI/server/page and assert the primary observable is correct; run it twice; screenshot frontend), resolve review findings, then offer the close-out choice: merge, open a PR, or keep the branch.

Full protocol: read {skill_path} once implementation starts.
</PRODUCT-PLAYBOOK-DEV-DISCIPLINE>"""


def main():
    sys.stdin.read()  # consume hook input; content unused
    root = pathlib.Path(os.environ.get("CLAUDE_PLUGIN_ROOT", "."))
    skill_path = root / "skills" / "dev-discipline" / "SKILL.md"
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": DIGEST.format(skill_path=skill_path),
    }}))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # never block session start
        print(f"session-start-inject-dev-discipline: {exc}", file=sys.stderr)
    sys.exit(0)
