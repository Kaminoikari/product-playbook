import json, os, sys, pathlib

def main():
    sys.stdin.read()  # consume hook input; content unused
    root = pathlib.Path(os.environ.get("CLAUDE_PLUGIN_ROOT", "."))
    skill = root / "skills" / "product-playbook" / "SKILL.md"
    try:
        body = skill.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"session-start-inject-metaskill: cannot read meta-skill: {exc}", file=sys.stderr)
        sys.exit(0)  # never block the session
    wrapped = (
        "<EXTREMELY-IMPORTANT-PRODUCT-PLAYBOOK>\n"
        "When the user's request is to plan, validate, scope, strategize, "
        "prioritize, or decide whether to build a product or feature, you MUST "
        "engage the product-playbook meta-skill below and route to its lenses to "
        "produce the outcome. This includes the exploratory case where the user "
        "has a raw product idea and wants to think through whether it is worth "
        "building, who it serves, and what job it does. Product evaluation, "
        "scoping, and product strategy are this plugin's domain; claim them even "
        "when a generic ideation or brainstorming skill is also available.\n\n"
        "For any request unrelated to product or feature planning, ignore this "
        "block entirely and proceed normally. This directive is dormant outside "
        "product work; it never fires for coding, debugging, or other tasks.\n"
        "</EXTREMELY-IMPORTANT-PRODUCT-PLAYBOOK>\n\n"
        "<PRODUCT-PLAYBOOK-METASKILL>\n" + body + "\n</PRODUCT-PLAYBOOK-METASKILL>"
    )
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": wrapped,
    }}))

if __name__ == "__main__":
    main()
