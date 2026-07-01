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

    def test_slash_commands_deleted(self):
        self.assertFalse((ROOT / "commands").exists() and any((ROOT / "commands").glob("product-*.md")))

    def test_mode_spine_refs_deleted(self):
        gone = ["rules-full", "rules-quick", "rules-revision", "rules-custom", "rules-build",
                "rules-product-type", "rules-optional-trigger", "rules-progress",
                "rules-end-of-flow", "rules-subagent-dispatch", "rules-commands"]
        for name in gone:
            self.assertFalse((ROOT / "references" / f"{name}.md").exists(), name)

    def test_change_propagation_kept(self):
        self.assertTrue((ROOT / "references" / "rules-change-propagation.md").exists())

    def test_planning_gate_no_product_dev_command_ref(self):
        src = (ROOT / "hooks" / "pre-write-planning-gate.py").read_text(encoding="utf-8")
        self.assertNotIn("/product-dev", src)
        self.assertNotIn("permissionDecision", src)  # stays non-blocking

    def test_topic_switch_change_propagation_kept_offtopic_dropped(self):
        src = (ROOT / "hooks" / "user-prompt-detect-topic-switch.py").read_text(encoding="utf-8")
        self.assertIn("rules-change-propagation", src)   # consistency guardrail kept
        self.assertNotIn("rules-progress", src)          # deleted file no longer referenced
        self.assertNotIn("continue/pause/end", src)      # old mode menu removed
        self.assertNotIn("permissionDecision", src)      # stays non-blocking

    def test_recipe_docs_exist_with_sequences(self):
        rec = ROOT / "references" / "recipes"
        expected = {
            "full-product-plan.md": ["strategy-kernel", "jtbd", "mvp-scoping", "success-metrics"],
            "quick-validation.md": ["jtbd", "pr-faq", "success-metrics"],
            "product-revision.md": ["problem-framing", "mvp-scoping", "success-metrics"],
            "feature-extension.md": ["problem-framing", "solution-prioritization", "pre-mortem", "mvp-scoping"],
        }
        for fname, lenses in expected.items():
            body = (rec / fname).read_text(encoding="utf-8")
            for lens in lenses:
                self.assertIn(lens, body, f"{fname} missing {lens}")

    def test_metaskill_recipes_point_to_docs(self):
        body = (ROOT / "skills" / "product-playbook" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("references/recipes/", body)
        self.assertNotIn("Fallback during migration", body)

    def test_new_system_has_no_reference_to_deleted_orchestration(self):
        # The runtime new system (skills/) must not reference any deleted mode-spine file.
        # NOTE: grep skills/ ONLY — test files legitimately name the deleted files to assert
        # their absence, and hooks/ still references rules-progress until Task 4 adapts it.
        import subprocess
        pattern = r"rules-(full|quick|revision|custom|build|product-type|optional-trigger|progress|end-of-flow|subagent-dispatch|commands)\b"
        hits = subprocess.run(["grep", "-rlE", pattern, str(ROOT / "skills")],
                              capture_output=True, text=True).stdout.strip()
        self.assertEqual(hits, "", f"dangling ref in skills/: {hits}")
