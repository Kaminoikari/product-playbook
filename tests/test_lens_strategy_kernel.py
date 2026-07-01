# tests/test_lens_strategy_kernel.py
import unittest, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from validate_skill import validate_skill

SKILL = "skills/strategy-kernel/SKILL.md"

class TestStrategyKernelLens(unittest.TestCase):
    def test_passes_validator(self):
        self.assertEqual(validate_skill(SKILL), [])

    def test_declares_tags_and_substance(self):
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertIn("`Rumelt Kernel`", body)
        self.assertIn("`DHM`", body)
        self.assertIn("strategy", body.lower())
        self.assertIn("empowered", body.lower())
        self.assertGreater(len(body), 5000)

    def test_excludes_north_star_scope(self):
        # §4.2+ (North Star, Sean Ellis) belongs to the success-metrics lens, not this one.
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertNotIn("North Star", body)

if __name__ == "__main__":
    unittest.main()
