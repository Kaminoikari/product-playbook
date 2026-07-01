import json, os, subprocess, pathlib, unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class TestInjectHook(unittest.TestCase):
    def test_hook_emits_metaskill_in_additional_context(self):
        env = {**os.environ, "CLAUDE_PLUGIN_ROOT": str(ROOT)}
        proc = subprocess.run(
            ["python3", str(ROOT / "hooks" / "session-start-inject-metaskill.py")],
            input="{}", capture_output=True, text=True, env=env, timeout=10,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        ctx = payload["hookSpecificOutput"]["additionalContext"]
        self.assertIn("PRODUCT-PLAYBOOK-METASKILL", ctx)
        self.assertIn("Read the outcome", ctx)

    def test_hook_never_blocks_when_metaskill_unreadable(self):
        # Safety property: on read failure the hook must exit 0, not crash the session.
        env = {**os.environ, "CLAUDE_PLUGIN_ROOT": str(ROOT / "no_such_dir")}
        proc = subprocess.run(
            ["python3", str(ROOT / "hooks" / "session-start-inject-metaskill.py")],
            input="{}", capture_output=True, text=True, env=env, timeout=10,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertIn("cannot read meta-skill", proc.stderr)
