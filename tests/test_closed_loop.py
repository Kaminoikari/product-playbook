"""N7: unittest suite covering the closed-loop guardrails.

Promotes the inline-bash smoke assertions into a structured test suite so:
  - failures point at a specific assertion (vs. opaque bash diff)
  - the suite can run in CI (pure Python, zero LLM/quota cost)
  - regressions show up as test failures, not silently broken markdown

Loads the scripts/ modules via importlib (their filenames contain hyphens,
so they can't be normal `import` targets). Each test class corresponds to
one optimisation pass A1-A4, B5, B6, D9, O1-O7, N1-N6.

Run via:
  python3 -m unittest tests/test_closed_loop.py
  npm test
"""

from __future__ import annotations

import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"


def _load(name: str, fname: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / fname)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestA1AttributionPaths(unittest.TestCase):
    """A1: EVAL_ATTRIBUTION primary/secondary paths must all exist."""

    def test_clean_state(self):
        m = _load("debt", "eval-debt-report.py")
        # clean state: every hardcoded path should resolve to a real file
        # (running from REPO_ROOT — the repo's current source tree)
        missing = m._check_attribution_paths(REPO_ROOT)
        self.assertEqual(missing, [], f"unexpected missing paths: {missing}")

    def test_synthetic_broken_path(self):
        m = _load("debt", "eval-debt-report.py")
        m.EVAL_ATTRIBUTION["_test_broken_eval"] = {
            "primary": ["references/this-does-not-exist.md"],
            "secondary": [],
        }
        try:
            missing = m._check_attribution_paths(REPO_ROOT)
            self.assertIn("_test_broken_eval.primary: references/this-does-not-exist.md",
                          missing)
        finally:
            del m.EVAL_ATTRIBUTION["_test_broken_eval"]


class TestA2HardGateStructure(unittest.TestCase):
    """A2: validate_hard_gate_structure rejects malformed additions."""

    def setUp(self):
        self.m = _load("pp", "patch-proposer.py")

    def test_no_new_gate(self):
        self.assertIsNone(self.m.validate_hard_gate_structure("foo", "bar"))

    def test_well_formed_gate(self):
        upd = "old\n\n**X (Hard Gate)**: do it\nFAIL: bad\n✅ PASS: good"
        self.assertIsNone(self.m.validate_hard_gate_structure("old", upd))

    def test_missing_fail(self):
        upd = "old\n\n**X (Hard Gate)**: do it\n✅ PASS: good"
        err = self.m.validate_hard_gate_structure("old", upd)
        self.assertIsNotNone(err)
        self.assertIn("FAIL", err)

    def test_missing_pass_marker(self):
        upd = "old\n\n**X (Hard Gate)**: do it\nFAIL: nope"
        err = self.m.validate_hard_gate_structure("old", upd)
        self.assertIsNotNone(err)
        self.assertIn("✅", err)


class TestA3MirrorValidation(unittest.TestCase):
    """A3: i18n mirror verify_no_fence_drift catches structural drift."""

    def setUp(self):
        self.m = _load("mm", "i18n-mirror-apply.py")

    def test_frontmatter_preserved(self):
        src = "---\nname: x\ndescription: y\n---\nbody"
        warns = self.m.verify_no_fence_drift(src, "", src)
        self.assertFalse(any("frontmatter" in w for w in warns))

    def test_frontmatter_key_dropped(self):
        src = "---\nname: x\ndescription: y\n---\nbody"
        upd = "---\nname: x\n---\nbody"
        warns = self.m.verify_no_fence_drift(src, "", upd)
        self.assertTrue(any("frontmatter" in w for w in warns))

    def test_heading_off_by_one_tolerated(self):
        warns = self.m.verify_no_fence_drift("## A\n## B\n## C\n", "", "## A\n## B\n")
        self.assertFalse(any("heading count" in w for w in warns))

    def test_heading_big_drop_flagged(self):
        warns = self.m.verify_no_fence_drift("## A\n## B\n## C\n## D\n", "", "## A\n")
        self.assertTrue(any("heading count" in w for w in warns))

    def test_table_row_mismatch(self):
        src = "| a | b |\n|--|--|\n| 1 | 2 |\n| 3 | 4 |\n"
        upd = "| a | b |\n|--|--|\n| 1 | 2 |\n"
        warns = self.m.verify_no_fence_drift(src, "", upd)
        self.assertTrue(any("table rows" in w for w in warns))


class TestFreshness(unittest.TestCase):
    """Eval freshness gate — both the original watched dirs and N2 evals.json."""

    def setUp(self):
        self.m = _load("fr", "_freshness.py")

    def test_watched_includes_eval_spec(self):
        self.assertIn("evals/evals.json", self.m.WATCHED,
                      "N2: evals/evals.json must be a watched path")

    def test_just_touched_eval_is_fresh(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            tf.write(b"{}")
            tmp = Path(tf.name)
        try:
            ok, reason = self.m.check_eval_freshness(tmp, REPO_ROOT)
            self.assertTrue(ok, f"expected fresh, got: {reason}")
        finally:
            tmp.unlink()


class TestLoopSummaryJudge(unittest.TestCase):
    """L5 verdict logic across all 5 paths."""

    def setUp(self):
        self.m = _load("ls", "loop-summary.py")

    def _hist(self, *scores_crits):
        return [
            {"before_summary": {"score": s, "band": "needs", "critical_failures": c}}
            for s, c in scores_crits
        ]

    def test_insufficient_data(self):
        self.assertEqual(self.m.judge([])["status"], "insufficient-data")

    def test_converged_when_zero_crit_and_healthy(self):
        h = [{"before_summary": {"score": 80, "band": "needs", "critical_failures": 2}},
             {"before_summary": {"score": 90, "band": "healthy", "critical_failures": 0}}]
        self.assertEqual(self.m.judge(h)["status"], "converged")

    def test_regressing_on_score_drop(self):
        self.assertEqual(self.m.judge(self._hist((80, 2), (65, 5)))["status"], "regressing")

    def test_stalled_after_3_flat_ticks(self):
        h = self._hist((65, 3), (67, 3), (68, 3))
        self.assertEqual(self.m.judge(h)["status"], "stalled")

    def test_improving(self):
        self.assertEqual(self.m.judge(self._hist((65, 3), (75, 1)))["status"], "improving")


class TestN6Sparkline(unittest.TestCase):
    """N6: sparkline rendering."""

    def setUp(self):
        self.m = _load("ls", "loop-summary.py")

    def test_empty_returns_empty(self):
        self.assertEqual(self.m._sparkline([]), "")
        self.assertEqual(self.m._sparkline([42]), "")

    def test_flat_returns_constant(self):
        out = self.m._sparkline([5, 5, 5, 5])
        self.assertEqual(len(out), 4)
        self.assertEqual(len(set(out)), 1)  # all same char

    def test_monotonic_climb(self):
        out = self.m._sparkline([10, 20, 30, 40, 50])
        # first char should be the lowest sparkline glyph
        self.assertEqual(out[0], self.m.SPARK_CHARS[0])
        self.assertEqual(out[-1], self.m.SPARK_CHARS[-1])


class TestD9PriorSuspects(unittest.TestCase):
    """D9: parser extracts (file, eval) pairs from attribution-check reports."""

    def setUp(self):
        self.m = _load("pp", "patch-proposer.py")

    def test_no_docs_returns_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = os.getcwd()
            os.chdir(tmp)
            try:
                self.assertEqual(self.m._load_prior_suspects(), {})
            finally:
                os.chdir(cwd)

    def test_extracts_only_attribution_RIGHT_pairs(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            docs.mkdir()
            (docs / "attribution-check-2026-05-29.md").write_text(
                "### 1. `references/x.md` → eval `eval-a`\n"
                "**Patched file in primary?** ✅ yes\n\n"
                "### 2. `agents/y.md` → eval `eval-b`\n"
                "**Patched file in primary?** ❌ NO\n",
                encoding="utf-8",
            )
            cwd = os.getcwd()
            os.chdir(tmp)
            try:
                sus = self.m._load_prior_suspects()
                self.assertIn(("references/x.md", "eval-a"), sus)
                self.assertNotIn(("agents/y.md", "eval-b"), sus,
                                  "attribution-WRONG pairs should be skipped — D9 only "
                                  "feeds back wording-insufficient suspects")
            finally:
                os.chdir(cwd)


class TestO3AttributionPatch(unittest.TestCase):
    """O3: render_attribution_patch emits copy-pasteable EVAL_ATTRIBUTION edits."""

    def setUp(self):
        self.m = _load("ac", "attribution-check.py")

    def test_no_gap_returns_empty(self):
        report = {"suspects": [], "flipped": [], "untrackable": []}
        self.assertEqual(self.m.render_attribution_patch(report), [])

    def test_gap_renders_block(self):
        report = {"suspects": [{
            "patched_file": "agents/foo.md", "eval_name": "eval-x",
            "patched_file_in_primary": False,
            "current_primary_attribution": ["references/a.md"],
        }], "flipped": [], "untrackable": []}
        out = "\n".join(self.m.render_attribution_patch(report))
        self.assertIn("eval-x", out)
        self.assertIn("agents/foo.md", out)
        self.assertIn("references/a.md", out)  # original kept in merged primary

    def test_wording_insufficient_skipped(self):
        report = {"suspects": [{
            "patched_file": "X", "eval_name": "Y",
            "patched_file_in_primary": True,  # not a gap
            "current_primary_attribution": ["X"],
        }], "flipped": [], "untrackable": []}
        self.assertEqual(self.m.render_attribution_patch(report), [])


class TestO7RegressionRescueTrigger(unittest.TestCase):
    """O7: rescue triggers only on before=critical (set evolution immune)."""

    def setUp(self):
        self.m = _load("lift", "eval-lift-report.py")
        # render_regression_rescue uses subprocess.check_output for git log;
        # mock it once at the module level
        import subprocess as sp
        self._real = sp.check_output
        sp.check_output = lambda *a, **k: "abc123 fake commit"
        self._sp = sp

    def tearDown(self):
        self._sp.check_output = self._real

    def test_before_critical_triggers(self):
        report = {
            "summary": {"net_lift": 5, "score_delta": 5},
            "regressed": [{"before": {"severity": "critical"},
                           "after": {"severity": "warning"}}],
        }
        out = self.m.render_regression_rescue(report)
        self.assertTrue(out, "expected rescue (before=critical)")

    def test_before_warning_does_not_trigger(self):
        # set evolution case: warn→critical rename
        report = {
            "summary": {"net_lift": 5, "score_delta": 5},
            "regressed": [{"before": {"severity": "warning"},
                           "after": {"severity": "critical"}}],
        }
        out = self.m.render_regression_rescue(report)
        self.assertEqual(out, "")


class TestN3HistoryPrune(unittest.TestCase):
    """N3: prune keeps last-N records, optional archive."""

    def setUp(self):
        self.m = _load("pr", "loop-history-prune.py")

    def _write_history(self, n: int) -> Path:
        tmp = Path(tempfile.mkdtemp())
        hist = tmp / "loop-history.jsonl"
        with hist.open("w") as f:
            for i in range(n):
                f.write(json.dumps({
                    "timestamp": f"2026-05-{(i % 28) + 1:02d}T10:00:00",
                    "before_summary": {"score": 80 + i},
                }) + "\n")
        return hist

    def test_under_keep_last_noop(self):
        hist = self._write_history(5)
        try:
            result = self.m.prune(hist, keep_last=10, archive=False, dry_run=False)
            self.assertEqual(result["action"], "noop")
            self.assertEqual(result["kept"], 5)
        finally:
            hist.parent.rmdir() if False else None  # leave for OS cleanup

    def test_prune_discards_oldest(self):
        hist = self._write_history(50)
        result = self.m.prune(hist, keep_last=10, archive=False, dry_run=False)
        self.assertEqual(result["action"], "pruned")
        self.assertEqual(result["kept"], 10)
        self.assertEqual(result["discarded"], 40)
        # confirm the file now has 10 lines
        self.assertEqual(len(hist.read_text().strip().splitlines()), 10)

    def test_archive_writes_separate_file(self):
        hist = self._write_history(50)
        result = self.m.prune(hist, keep_last=10, archive=True, dry_run=False)
        self.assertEqual(result["archived"], 40)
        archive = hist.parent / "loop-history-archive-2026.jsonl"
        self.assertTrue(archive.is_file())
        self.assertEqual(len(archive.read_text().strip().splitlines()), 40)


class TestN5NoOpPatchDetection(unittest.TestCase):
    """N5: cosmetic-only diffs flagged as applied-cosmetic (logic check)."""

    def test_module_imports_re(self):
        # smoke test that the patch-proposer module loads with N5 inline
        # since the no-op check uses re module — ensure module-level imports OK
        m = _load("pp", "patch-proposer.py")
        self.assertTrue(hasattr(m, "process_cluster"))
        # confirm the new status code string is present in the source
        import inspect
        src = inspect.getsource(m.process_cluster)
        self.assertIn("applied-cosmetic", src)
        self.assertIn("delta_hg", src)


class TestJudgeNoneGuard(unittest.TestCase):
    """Post-K9 fix: judge() must not crash on records missing before_summary.score.

    Previously the regression branch had a None guard (line 110) but the
    "improving" fallback dereferenced score_now/score_prev unconditionally —
    `(None - None)` TypeError on the format string. Real loop-tick.py always
    writes before_summary, but hand-edited or pre-L5 history records can hit
    this path. The fix returns insufficient-data instead of crashing.
    """

    def setUp(self):
        self.m = _load("ls", "loop-summary.py")

    def test_two_records_without_score_returns_insufficient_data(self):
        h = [{"timestamp": "2026-05-28", "patch_log": "x"},
             {"timestamp": "2026-05-29", "patch_log": "y"}]
        v = self.m.judge(h)
        self.assertEqual(v["status"], "insufficient-data")
        self.assertIn("score", v["reason"].lower())

    def test_mixed_missing_score_returns_insufficient_data(self):
        # one record has score, the other doesn't — also must not crash
        h = [{"before_summary": {"score": 70, "band": "needs",
                                  "critical_failures": 2}},
             {"timestamp": "2026-05-29"}]
        v = self.m.judge(h)
        self.assertEqual(v["status"], "insufficient-data")


class TestSinceDateValidation(unittest.TestCase):
    """Post-K9 fix: --since must reject malformed ISO dates with exit 2.

    Previously --since used lexicographic string compare, so any non-ISO
    input (e.g. typo `5-29-2026`) silently filtered to 0 ticks. Users would
    see 'insufficient-data' and assume the loop hadn't ticked. Now the
    invalid date is rejected up-front.
    """

    def test_main_rejects_malformed_since(self):
        import subprocess
        result = subprocess.run(
            ["python3", str(SCRIPTS / "loop-summary.py"),
             "--since", "notadate", "--history", "/dev/null"],
            capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("not a valid ISO date", result.stderr)

    def test_main_accepts_valid_since(self):
        import subprocess
        with tempfile.TemporaryDirectory() as td:
            empty = Path(td) / "h.jsonl"
            empty.write_text("")
            out = Path(td) / "summary.md"
            result = subprocess.run(
                ["python3", str(SCRIPTS / "loop-summary.py"),
                 "--since", "2026-01-01", "--history", str(empty),
                 "--output", str(out)],
                capture_output=True, text=True)
            self.assertEqual(result.returncode, 2,
                              "empty history → insufficient-data → exit 2")
            self.assertNotIn("not a valid ISO date", result.stderr)


class TestPruneKeepLastValidation(unittest.TestCase):
    """Post-K9 fix: loop-history-prune --keep-last must reject 0 and negatives.

    Python negative-slice quirk: lines[-0:] == lines[0:] (all records), and
    lines[-(-3):] == lines[3:] (first-half drop). Both are footguns. The
    fix rejects --keep-last < 1 with a clear message.
    """

    def test_keep_last_zero_rejected(self):
        import subprocess
        with tempfile.NamedTemporaryFile(suffix=".jsonl", mode="w", delete=False) as f:
            f.write('{"timestamp":"2026-05-29","score":70}\n')
            hpath = f.name
        try:
            result = subprocess.run(
                ["python3", str(SCRIPTS / "loop-history-prune.py"),
                 "--history", hpath, "--keep-last", "0"],
                capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn("--keep-last", result.stderr)
        finally:
            os.unlink(hpath)

    def test_keep_last_negative_rejected(self):
        import subprocess
        with tempfile.NamedTemporaryFile(suffix=".jsonl", mode="w", delete=False) as f:
            f.write('{"timestamp":"2026-05-29","score":70}\n')
            hpath = f.name
        try:
            result = subprocess.run(
                ["python3", str(SCRIPTS / "loop-history-prune.py"),
                 "--history", hpath, "--keep-last", "-3"],
                capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn("footgun", result.stderr.lower())
        finally:
            os.unlink(hpath)

    def test_keep_last_one_accepted(self):
        import subprocess
        with tempfile.NamedTemporaryFile(suffix=".jsonl", mode="w", delete=False) as f:
            for i in range(5):
                f.write(f'{{"timestamp":"2026-05-2{i}","score":{60+i}}}\n')
            hpath = f.name
        try:
            result = subprocess.run(
                ["python3", str(SCRIPTS / "loop-history-prune.py"),
                 "--history", hpath, "--keep-last", "1"],
                capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            # only the last record should survive
            kept = Path(hpath).read_text().strip().splitlines()
            self.assertEqual(len(kept), 1)
            rec = json.loads(kept[0])
            self.assertEqual(rec["score"], 64)
        finally:
            os.unlink(hpath)


class TestNegativeMaxRejection(unittest.TestCase):
    """Post-K9 fix: --max / --max-patches must reject negatives.

    patch-proposer --max -1 produced 'deferring N+1' arithmetic in the
    user-facing message; i18n-mirror-apply and loop-tick had the same shape.
    All three now reject negatives up-front.
    """

    def test_patch_proposer_rejects_negative_max(self):
        import subprocess
        r = subprocess.run(["python3", str(SCRIPTS / "patch-proposer.py"),
                            "--results", "/dev/null", "--max", "-1"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("--max must be >= 0", r.stderr)

    def test_i18n_mirror_rejects_negative_max(self):
        import subprocess
        r = subprocess.run(["python3", str(SCRIPTS / "i18n-mirror-apply.py"),
                            "--max", "-1"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("--max must be >= 0", r.stderr)

    def test_loop_tick_rejects_negative_max_patches(self):
        import subprocess
        r = subprocess.run(["python3", str(SCRIPTS / "loop-tick.py"),
                            "--eval-results", "/dev/null",
                            "--max-patches", "-1"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn("--max-patches must be >= 0", r.stderr)


class TestPairedOnlyBadge(unittest.TestCase):
    """Post-K9 fix: --paired-only must surface a visible badge in markdown.

    Previously only summary.paired_only=True was set in JSON; markdown
    readers couldn't tell paired-only net_lift apart from default net_lift.
    """

    def setUp(self):
        self.m = _load("lift", "eval-lift-report.py")

    def test_badge_present_when_paired_only(self):
        report = {
            "generated": "2026-05-30",
            "summary": {
                "before_score": 70, "after_score": 75, "score_delta": 5,
                "before_band": "needs", "after_band": "needs",
                "paired": 1, "added": 0, "removed": 0,
                "improved": 1, "regressed": 0, "unchanged_pass": 0,
                "unchanged_fail": 0, "soft_moves": 0,
                "lift_gain": 15, "lift_loss": 0, "net_lift": 15,
                "soft_pass_gain": 0, "soft_pass_loss": 0,
                "paired_only": True,
            },
            "improved": [], "regressed": [], "soft_moves": [],
            "added": [], "removed": [],
        }
        md = self.m.render_markdown(report, "before.json", "after.json")
        self.assertIn("--paired-only", md)
        self.assertIn("set-evolution", md.lower())

    def test_no_badge_when_default(self):
        report = {
            "generated": "2026-05-30",
            "summary": {
                "before_score": 70, "after_score": 75, "score_delta": 5,
                "before_band": "needs", "after_band": "needs",
                "paired": 1, "added": 0, "removed": 0,
                "improved": 1, "regressed": 0, "unchanged_pass": 0,
                "unchanged_fail": 0, "soft_moves": 0,
                "lift_gain": 15, "lift_loss": 0, "net_lift": 15,
                "soft_pass_gain": 0, "soft_pass_loss": 0,
            },
            "improved": [], "regressed": [], "soft_moves": [],
            "added": [], "removed": [],
        }
        md = self.m.render_markdown(report, "before.json", "after.json")
        self.assertNotIn("--paired-only", md)


if __name__ == "__main__":
    unittest.main()
