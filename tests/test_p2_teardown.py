import json, pathlib, unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class TestP2Teardown(unittest.TestCase):
    def test_dispatch_hook_deleted(self):
        self.assertFalse((ROOT / "hooks" / "user-prompt-detect-specialist-dispatch.py").exists())

    def test_discovery_specialist_deleted(self):
        self.assertFalse((ROOT / "agents" / "discovery-specialist.md").exists())

    def test_hooks_json_valid_and_no_dispatch(self):
        cfg = json.loads((ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8"))
        blob = json.dumps(cfg)
        self.assertNotIn("specialist-dispatch", blob)
        # topic-switch and the two session-start hooks + planning-gate remain
        self.assertIn("user-prompt-detect-topic-switch.py", blob)
        self.assertIn("session-start-inject-metaskill.py", blob)
