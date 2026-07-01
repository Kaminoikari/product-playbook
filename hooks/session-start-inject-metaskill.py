import json, os, sys, pathlib

def main():
    sys.stdin.read()  # consume hook input; content unused
    root = pathlib.Path(os.environ.get("CLAUDE_PLUGIN_ROOT", "."))
    skill = root / "skills" / "product-playbook" / "SKILL.md"
    try:
        body = skill.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"session-start-inject-metaskill: cannot read meta-skill: {exc}", file=sys.stderr)
        sys.exit(0)  # never block the session
    wrapped = (
        "<PRODUCT-PLAYBOOK-METASKILL>\n"
        "The product-playbook meta-skill is active this session. Follow it for any "
        "product/feature planning request.\n\n" + body + "\n</PRODUCT-PLAYBOOK-METASKILL>"
    )
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": wrapped,
    }}))

if __name__ == "__main__":
    main()
