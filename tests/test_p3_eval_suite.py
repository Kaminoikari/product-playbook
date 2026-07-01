import json, pathlib, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "evals" / "evals.json").read_text(encoding="utf-8"))
CASES = DATA["evals"]
NAMES = {c["name"] for c in CASES}
VALID_SEV = {"critical", "warning", "info"}

class TestP3EvalSuite(unittest.TestCase):
    def test_case_count_focused(self):
        self.assertGreaterEqual(len(CASES), 8)
        self.assertLessEqual(len(CASES), 10)

    def test_every_case_has_required_fields(self):
        seen_ids = set()
        for c in CASES:
            self.assertIn("id", c); self.assertIn("name", c)
            self.assertIn("prompt", c); self.assertIn("expectations", c)
            self.assertNotIn(c["id"], seen_ids, f"dup id {c['id']}"); seen_ids.add(c["id"])
            self.assertTrue(c["expectations"], c["name"])
            for e in c["expectations"]:
                self.assertIn("text", e); self.assertIn(e["severity"], VALID_SEV, e)

    def test_new_outcome_first_cases_present(self):
        for required in ("lens-selection-single", "lens-blend", "provenance-format",
                         "guardrail-proportional"):
            self.assertIn(required, NAMES, required)

    def test_obsolete_mode_cases_gone(self):
        for gone in ("eval-mode-selection", "eval-quick-mode-jtbd", "eval-revision-mode",
                     "eval-quality-hardgate", "eval-subagent-discovery"):
            self.assertNotIn(gone, NAMES, gone)

    def test_no_mode_scoping_language_in_expectations(self):
        blob = json.dumps(DATA, ensure_ascii=False)
        # the obsolete Discovery/Develop/Deliver mode-scoping vocabulary must be gone
        for banned in ("Discovery mode", "Develop/Deliver", "Full Mode", "Quick Mode",
                       "Revision Mode", "Hard Gate"):
            self.assertNotIn(banned, blob, banned)

    def test_provenance_expectation_exists(self):
        blob = json.dumps(DATA, ensure_ascii=False)
        self.assertIn("Frameworks:", blob)  # at least one case scores the provenance line

    def test_attribution_covers_new_eval_names(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "edr", str(ROOT / "scripts" / "eval-debt-report.py"))
        edr = importlib.util.module_from_spec(spec); spec.loader.exec_module(edr)
        keys = set(edr.EVAL_ATTRIBUTION.keys())
        # every current evals.json case name has an attribution entry (patch coverage)
        for name in NAMES:
            self.assertIn(name, keys, f"{name} missing from EVAL_ATTRIBUTION")
        # retired names no longer linger as dead keys (trigger-eval is the one allowed non-case key)
        for retired in ("eval-mode-selection", "eval-subagent-discovery", "eval-revision-mode"):
            self.assertNotIn(retired, keys, retired)
