import textwrap, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from validate_skill import validate_skill

def _write(tmp_path, body):
    p = tmp_path / "SKILL.md"
    p.write_text(body, encoding="utf-8")
    return str(p)

def test_valid_skill_has_no_violations(tmp_path):
    body = textwrap.dedent("""\
        ---
        name: jtbd
        description: Use when you need to understand the job a user hires the product to do, before designing a solution.
        ---
        # JTBD
        Detect the user's language and reply in it.
        Append the framework tag `JTBD` to the provenance line.
        """)
    assert validate_skill(_write(tmp_path, body)) == []

def test_missing_provenance_flagged(tmp_path):
    body = "---\nname: jtbd\ndescription: Use when ...\n---\n# JTBD\nDetect the user's language.\n"
    assert any("provenance" in v.lower() for v in validate_skill(_write(tmp_path, body)))

def test_bad_name_flagged(tmp_path):
    body = "---\nname: JTBD_Skill\ndescription: Use when ...\n---\n# x\nprovenance tag\nlanguage\n"
    assert any("name" in v.lower() for v in validate_skill(_write(tmp_path, body)))

def test_workflow_leak_in_description_flagged(tmp_path):
    body = "---\nname: jtbd\ndescription: Step 1 gather interviews, then write the job statement, then rank.\n---\n# x\nprovenance\nlanguage\n"
    assert any("workflow" in v.lower() for v in validate_skill(_write(tmp_path, body)))
