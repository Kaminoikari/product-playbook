# tests/test_lens_persona_journey.py
import unittest, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from validate_skill import validate_skill

SKILL = "skills/persona-journey/SKILL.md"

class TestPersonaJourneyLens(unittest.TestCase):
    def test_passes_validator(self):
        self.assertEqual(validate_skill(SKILL), [])

    def test_declares_tags_and_substance(self):
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertIn("`Persona`", body)
        self.assertIn("`Journey Map`", body)
        self.assertIn("buyer", body.lower())
        self.assertIn("journey", body.lower())
        self.assertGreater(len(body), 6000)

    def test_soften_pass_removed_hard_gate_framing(self):
        body = pathlib.Path(SKILL).read_text(encoding="utf-8")
        self.assertNotIn("Hard Gate", body)


if __name__ == "__main__":
    unittest.main()
