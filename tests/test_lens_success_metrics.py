# tests/test_lens_success_metrics.py
import unittest, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from validate_skill import validate_skill

SKILL = "skills/success-metrics/SKILL.md"

class TestSuccessMetricsLens(unittest.TestCase):
    def test_passes_validator(self):
        self.assertEqual(validate_skill(SKILL), [])

    def test_declares_tags_and_substance(self):
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertIn("`North Star`", body)
        self.assertIn("aha moment", body.lower())
        self.assertIn("sean ellis", body.lower())
        self.assertGreater(len(body), 2500)

    def test_excludes_empowered_teams_section(self):
        # §4.1 Empowered Teams belongs to the strategy-kernel lens, not this one.
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertNotIn("Empowered Teams", body)

if __name__ == "__main__":
    unittest.main()
