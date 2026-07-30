import json, os, pathlib, subprocess, unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
HOOK = ROOT / "hooks" / "pre-write-secret-guard.py"

# Well-known documentation placeholder (AWS docs) and a same-shape live-looking key.
AWS_DOC_EXAMPLE_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_LIVE_SHAPE_KEY = "AKIA" + "J7Q2ZKN4RP8W5TBH"


GUARD_ENV_VAR = "PRODUCT_PLAYBOOK_SECRET_GUARD"


def _run(payload: dict | str, guard: str | None = None) -> subprocess.CompletedProcess:
    stdin = payload if isinstance(payload, str) else json.dumps(payload)
    env = {**os.environ, "CLAUDE_PLUGIN_ROOT": str(ROOT)}
    # Pin the switch instead of inheriting it: an operator who turned the guard
    # off in their own shell would otherwise silently flip every default-mode
    # assertion below into a false pass.
    if guard is None:
        env.pop(GUARD_ENV_VAR, None)
    else:
        env[GUARD_ENV_VAR] = guard
    return subprocess.run(
        ["python3", str(HOOK)],
        input=stdin, capture_output=True, text=True,
        env=env, timeout=10,
    )


def _write_payload(file_path: str, content: str) -> dict:
    return {
        "tool_name": "Write",
        "tool_input": {"file_path": file_path, "content": content},
        "cwd": "/tmp",
        "session_id": "s1",
    }


def _decision(proc: subprocess.CompletedProcess) -> dict:
    return json.loads(proc.stdout)["hookSpecificOutput"]


class TestSecretGuard(unittest.TestCase):
    def test_live_shape_aws_key_asks_for_confirmation(self):
        proc = _run(_write_payload("config.py", f'AWS_KEY = "{AWS_LIVE_SHAPE_KEY}"\n'))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = _decision(proc)
        self.assertEqual(out["permissionDecision"], "ask")
        self.assertIn("AWS", out["permissionDecisionReason"])

    def test_reason_never_echoes_the_secret_itself(self):
        proc = _run(_write_payload("config.py", f'AWS_KEY = "{AWS_LIVE_SHAPE_KEY}"\n'))
        self.assertNotIn(AWS_LIVE_SHAPE_KEY, _decision(proc)["permissionDecisionReason"])

    def test_documented_placeholder_key_passes_silently(self):
        proc = _run(_write_payload("README.md", f"Use {AWS_DOC_EXAMPLE_KEY} as an example key.\n"))
        self.assertEqual(proc.stdout.strip(), "")

    def test_private_key_block_asks_for_confirmation(self):
        content = "-----BEGIN RSA PRIVATE KEY-----\nMIIEow...\n"
        out = _decision(_run(_write_payload("deploy/id_rsa", content)))
        self.assertEqual(out["permissionDecision"], "ask")

    def test_clean_content_passes_silently(self):
        proc = _run(_write_payload("src/app.py", "def handler(event):\n    return 200\n"))
        self.assertEqual(proc.stdout.strip(), "")

    def test_env_file_write_asks_for_confirmation(self):
        out = _decision(_run(_write_payload("/repo/.env", "DB_URL=postgres://x\n")))
        self.assertEqual(out["permissionDecision"], "ask")
        self.assertIn(".env", out["permissionDecisionReason"])

    def test_env_example_file_passes_silently(self):
        proc = _run(_write_payload("/repo/.env.example", "DB_URL=\n"))
        self.assertEqual(proc.stdout.strip(), "")

    def test_edit_new_string_is_scanned(self):
        payload = {
            "tool_name": "Edit",
            "tool_input": {
                "file_path": "src/client.ts",
                "old_string": "const token = process.env.GH_TOKEN",
                "new_string": 'const token = "ghp_' + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8" + '"',
            },
            "cwd": "/tmp",
            "session_id": "s1",
        }
        out = _decision(_run(payload))
        self.assertEqual(out["permissionDecision"], "ask")
        self.assertIn("GitHub", out["permissionDecisionReason"])

    def test_malformed_stdin_never_blocks(self):
        proc = _run("not json {{{")
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), "")


class TestSecretGuardTurnedOff(unittest.TestCase):
    """`PRODUCT_PLAYBOOK_SECRET_GUARD=off` — for unattended runs where a consent
    dialog has nobody to answer it. Detection must still happen and still be
    visible; only the blocking is dropped."""

    def test_live_shape_key_writes_without_a_prompt(self):
        proc = _run(_write_payload("config.py", f'AWS_KEY = "{AWS_LIVE_SHAPE_KEY}"\n'), guard="off")
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), "", "a decision was emitted, so the write still stalls")

    def test_env_file_write_goes_through_without_a_prompt(self):
        proc = _run(_write_payload(".env", "API_KEY=whatever\n"), guard="off")
        self.assertEqual(proc.stdout.strip(), "")

    def test_the_finding_is_still_reported_on_stderr(self):
        proc = _run(_write_payload("config.py", f'AWS_KEY = "{AWS_LIVE_SHAPE_KEY}"\n'), guard="off")
        self.assertIn("AWS", proc.stderr)

    def test_stderr_report_never_echoes_the_secret_itself(self):
        proc = _run(_write_payload("config.py", f'AWS_KEY = "{AWS_LIVE_SHAPE_KEY}"\n'), guard="off")
        self.assertNotIn(AWS_LIVE_SHAPE_KEY, proc.stderr)

    def test_clean_content_stays_silent_on_stderr_too(self):
        proc = _run(_write_payload("config.py", 'NAME = "charles"\n'), guard="off")
        self.assertEqual(proc.stdout.strip(), "")
        self.assertEqual(proc.stderr.strip(), "")

    def test_only_an_explicit_off_value_disables_the_guard(self):
        # A stray or misspelled value must fail SAFE — still ask.
        for value in ("", "on", "ask", "1", "true", "OFFF", "disabled"):
            with self.subTest(value=value):
                out = _decision(_run(_write_payload(".env", "A=1\n"), guard=value))
                self.assertEqual(out["permissionDecision"], "ask")

    def test_off_is_case_and_whitespace_insensitive(self):
        for value in ("off", "OFF", " Off ", "0", "false", "no"):
            with self.subTest(value=value):
                proc = _run(_write_payload(".env", "A=1\n"), guard=value)
                self.assertEqual(proc.stdout.strip(), "")


if __name__ == "__main__":
    unittest.main()
