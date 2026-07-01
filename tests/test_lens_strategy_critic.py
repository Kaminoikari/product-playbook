# tests/test_lens_strategy_critic.py
import unittest, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from validate_skill import validate_skill

SKILL = "skills/strategy-critic/SKILL.md"

class TestStrategyCriticLens(unittest.TestCase):
    def test_passes_validator(self):
        self.assertEqual(validate_skill(SKILL), [])

    def test_declares_tag_and_substance(self):
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertIn("Strategy Critique", body)
        self.assertIn("critic", body.lower())
        self.assertIn("diagnosis", body.lower())
        self.assertGreater(len(body), 6000)
        self.assertNotIn("summary_for_main_agent", body)

if __name__ == "__main__":
    unittest.main()
