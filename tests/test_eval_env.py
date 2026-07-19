import json, os, sys, pathlib, unittest
from unittest import mock

EVALS = pathlib.Path(__file__).resolve().parents[1] / "evals"
sys.path.insert(0, str(EVALS))
from eval_env import plugin_isolation_args  # noqa: E402

SUPERPOWERS = "superpowers@claude-plugins-official"
SELF_PLUGIN = "product-playbook@skills-dir"


class TestPluginIsolationArgs(unittest.TestCase):
    @mock.patch.dict(os.environ, {}, clear=True)
    def test_default_disables_superpowers(self):
        args = plugin_isolation_args()
        self.assertEqual(args[0], "--settings")
        settings = json.loads(args[1])
        self.assertIs(settings["enabledPlugins"][SUPERPOWERS], False)

    @mock.patch.dict(os.environ, {"PRODUCT_PLAYBOOK_EVAL_ISOLATE": "0"}, clear=True)
    def test_isolation_can_be_turned_off(self):
        self.assertEqual(plugin_isolation_args(), [])

    @mock.patch.dict(os.environ, {"PRODUCT_PLAYBOOK_EVAL_DISABLE_PLUGINS": "a@x, b@y"}, clear=True)
    def test_override_list_is_honored(self):
        settings = json.loads(plugin_isolation_args()[1])
        self.assertIs(settings["enabledPlugins"]["a@x"], False)
        self.assertIs(settings["enabledPlugins"]["b@y"], False)

    # The user may scope product-playbook per-project (user-level false +
    # .claude/settings.local.json true). Evals run claude -p from $HOME, where
    # only the user-level false applies — without self-enablement every
    # should_trigger case is a structural zero regardless of model or content.
    @mock.patch.dict(os.environ, {}, clear=True)
    def test_self_plugin_is_force_enabled_by_default(self):
        settings = json.loads(plugin_isolation_args()[1])
        self.assertIs(settings["enabledPlugins"][SELF_PLUGIN], True)

    @mock.patch.dict(os.environ, {"PRODUCT_PLAYBOOK_EVAL_DISABLE_PLUGINS": "  ,  "}, clear=True)
    def test_empty_disable_list_still_enables_self(self):
        settings = json.loads(plugin_isolation_args()[1])
        self.assertEqual(settings["enabledPlugins"], {SELF_PLUGIN: True})

    @mock.patch.dict(os.environ, {"PRODUCT_PLAYBOOK_EVAL_ENSURE_SELF": "0"}, clear=True)
    def test_self_enablement_can_be_opted_out(self):
        settings = json.loads(plugin_isolation_args()[1])
        self.assertNotIn(SELF_PLUGIN, settings["enabledPlugins"])


if __name__ == "__main__":
    unittest.main()
