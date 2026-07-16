import json, os, subprocess, pathlib, unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
HOOK = ROOT / "hooks" / "session-start-inject-dev-discipline.py"


def _run(stdin: str = "{}", env_overrides: dict | None = None) -> subprocess.CompletedProcess:
    env = {**os.environ, "CLAUDE_PLUGIN_ROOT": str(ROOT), **(env_overrides or {})}
    return subprocess.run(
        ["python3", str(HOOK)],
        input=stdin, capture_output=True, text=True, env=env, timeout=10,
    )


class TestInjectDevDiscipline(unittest.TestCase):
    def test_hook_emits_discipline_digest_in_additional_context(self):
        proc = _run()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        ctx = payload["hookSpecificOutput"]["additionalContext"]
        self.assertEqual(payload["hookSpecificOutput"]["hookEventName"], "SessionStart")
        self.assertIn("PRODUCT-PLAYBOOK-DEV-DISCIPLINE", ctx)

    def test_digest_names_all_six_gates(self):
        ctx = json.loads(_run().stdout)["hookSpecificOutput"]["additionalContext"]
        for gate_marker in ("failing test", "Scope integrity", "Security hygiene",
                            "Subagent economy", "Independent review", "Finish the branch"):
            self.assertIn(gate_marker, ctx)

    def test_digest_review_gate_names_both_reviewers(self):
        ctx = json.loads(_run().stdout)["hookSpecificOutput"]["additionalContext"]
        self.assertIn("code reviewer", ctx)
        self.assertIn("spec reviewer", ctx)

    def test_digest_offers_finish_branch_choices(self):
        ctx = json.loads(_run().stdout)["hookSpecificOutput"]["additionalContext"]
        self.assertIn("merge", ctx)
        self.assertIn("PR", ctx)

    def test_digest_points_to_full_skill(self):
        ctx = json.loads(_run().stdout)["hookSpecificOutput"]["additionalContext"]
        self.assertIn("skills/dev-discipline/SKILL.md", ctx)

    def test_digest_declares_dormant_scope(self):
        # The block must stand down outside implementation work, the same
        # scoping contract the metaskill injection makes for planning.
        ctx = json.loads(_run().stdout)["hookSpecificOutput"]["additionalContext"]
        self.assertIn("dormant", ctx)

    def test_hook_survives_malformed_stdin(self):
        proc = _run(stdin="not json {{{")
        self.assertEqual(proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()
