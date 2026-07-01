import json, os, sys, pathlib, unittest
from unittest import mock

EVALS = pathlib.Path(__file__).resolve().parents[1] / "evals"
sys.path.insert(0, str(EVALS))
from eval_env import plugin_isolation_args  # noqa: E402

SUPERPOWERS = "superpowers@claude-plugins-official"


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
        self.assertEqual(settings["enabledPlugins"], {"a@x": False, "b@y": False})

    @mock.patch.dict(os.environ, {"PRODUCT_PLAYBOOK_EVAL_DISABLE_PLUGINS": "  ,  "}, clear=True)
    def test_empty_override_is_noop(self):
        self.assertEqual(plugin_isolation_args(), [])


if __name__ == "__main__":
    unittest.main()
