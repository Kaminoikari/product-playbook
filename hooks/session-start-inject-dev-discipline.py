import json, os, sys, pathlib

DIGEST = """<PRODUCT-PLAYBOOK-DEV-DISCIPLINE>
These gates apply whenever the session moves into implementation: writing or modifying source code, building a feature, fixing a bug, or closing out a branch. They are dormant during planning, research, and conversation; product planning stays with the product-playbook meta-skill.

1. TDD first: write the failing test and watch it fail before writing production code; every bug fix starts from a failing reproduction test. Waivers (user said skip, or the change has no testable runtime surface) are stated in one line, never silent.
2. Scope integrity: build exactly what was agreed; flag out-of-scope discoveries in one line without silently fixing or expanding.
3. Security hygiene: no hardcoded secrets, never touch .env files, validate inputs at system boundaries, and treat payments, auth, permissions, and migrations as high-risk surfaces.
4. Subagent economy: implement inline by default; use subagents only for parallel independent research or exploration that you synthesize afterwards.
5. Independent review: after an implementation milestone, dispatch two fresh-context reviewers in parallel: a code reviewer judging the diff on correctness and quality, and a spec reviewer checking the diff against the agreed requirements (nothing missing, nothing extra). Address confirmed findings from both.
6. Finish the branch: run the full test suite and report real output, resolve review findings, and offer the user the close-out choice: merge, open a PR, or keep the branch.

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
