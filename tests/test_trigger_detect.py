import json, sys, pathlib, unittest

EVALS = pathlib.Path(__file__).resolve().parents[1] / "evals"
sys.path.insert(0, str(EVALS))
from run_trigger_test import _detect_trigger  # noqa: E402


def _stream(*events):
    return "\n".join(json.dumps(e) for e in events)


def _tool(skill_name):
    return {"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": "Skill", "input": {"skill": skill_name}}]}}


def _text(text):
    return {"type": "assistant", "message": {"content": [{"type": "text", "text": text}]}}


class TestDetectTrigger(unittest.TestCase):
    def test_explicit_product_playbook_skill_call(self):
        self.assertTrue(_detect_trigger(_stream(_tool("product-playbook:jtbd"))))

    def test_provenance_line_counts_as_trigger(self):
        # The inline-application case: no Skill call, but the signature provenance line.
        out = _stream(_text("Here is the go/no-go.\n— Frameworks: JTBD · Pre-mortem"))
        self.assertTrue(_detect_trigger(out))

    def test_endash_and_double_dash_provenance_variants(self):
        self.assertTrue(_detect_trigger(_stream(_text("—— Frameworks: RICE"))))
        self.assertTrue(_detect_trigger(_stream(_text("– Frameworks: MVP"))))

    def test_competing_skill_is_not_a_trigger(self):
        self.assertFalse(_detect_trigger(_stream(_tool("superpowers:brainstorming"))))

    def test_generic_text_without_provenance_is_not_a_trigger(self):
        self.assertFalse(_detect_trigger(_stream(_text("Let me brainstorm ideas about frameworks."))))


if __name__ == "__main__":
    unittest.main()
