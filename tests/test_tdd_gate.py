import json, os, pathlib, subprocess, tempfile, unittest, uuid

ROOT = pathlib.Path(__file__).resolve().parents[1]
HOOK = ROOT / "hooks" / "pre-write-tdd-gate.py"


def _run(payload: dict | str) -> subprocess.CompletedProcess:
    stdin = payload if isinstance(payload, str) else json.dumps(payload)
    return subprocess.run(
        ["python3", str(HOOK)],
        input=stdin, capture_output=True, text=True,
        env={**os.environ, "CLAUDE_PLUGIN_ROOT": str(ROOT)}, timeout=15,
    )


def _payload(cwd: pathlib.Path, file_path: pathlib.Path, tool_name: str = "Write") -> dict:
    return {
        "tool_name": tool_name,
        "tool_input": {"file_path": str(file_path), "content": "x = 1\n"},
        "cwd": str(cwd),
        "session_id": uuid.uuid4().hex,
    }


class TestTddGate(unittest.TestCase):
    def setUp(self):
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        self.project = pathlib.Path(tmpdir.name)

    def test_source_write_without_any_test_gets_advisory(self):
        proc = _run(_payload(self.project, self.project / "src" / "invoice.py"))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        message = json.loads(proc.stdout)["systemMessage"]
        self.assertIn("TDD", message)
        self.assertIn("invoice", message)

    def test_matching_test_file_silences_gate(self):
        tests_dir = self.project / "tests"
        tests_dir.mkdir()
        (tests_dir / "test_invoice.py").write_text("def test_total(): ...\n")
        proc = _run(_payload(self.project, self.project / "src" / "invoice.py"))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout.strip(), "")

    def test_untracked_test_file_in_git_repo_silences_gate(self):
        # TDD order means the test is usually brand new and uncommitted when
        # the production file gets written; git discovery must still see it.
        subprocess.run(["git", "init", "-q", str(self.project)], check=True, capture_output=True)
        tests_dir = self.project / "tests"
        tests_dir.mkdir()
        (tests_dir / "invoice.test.ts").write_text("test('total', () => {})\n")
        proc = _run(_payload(self.project, self.project / "src" / "invoice.ts"))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout.strip(), "")

    def test_writing_a_test_file_is_always_silent(self):
        proc = _run(_payload(self.project, self.project / "tests" / "test_invoice.py"))
        self.assertEqual(proc.stdout.strip(), "")

    def test_non_code_file_is_silent(self):
        proc = _run(_payload(self.project, self.project / "PLAN.md"))
        self.assertEqual(proc.stdout.strip(), "")

    def test_generic_stem_accepts_any_test_file_as_evidence(self):
        (self.project / "app.spec.ts").write_text("it('boots', () => {})\n")
        proc = _run(_payload(self.project, self.project / "src" / "index.ts"))
        self.assertEqual(proc.stdout.strip(), "")

    def test_advisory_fires_at_most_once_per_file_per_session(self):
        payload = _payload(self.project, self.project / "src" / "invoice.py")
        first = _run(payload)
        second = _run(payload)
        self.assertIn("TDD", json.loads(first.stdout)["systemMessage"])
        self.assertEqual(second.stdout.strip(), "")

    def test_waiver_marker_silences_gate_project_wide(self):
        (self.project / ".product-tdd-waived").write_text("")
        proc = _run(_payload(self.project, self.project / "src" / "invoice.py"))
        self.assertEqual(proc.stdout.strip(), "")

    def test_malformed_stdin_never_blocks(self):
        proc = _run("not json {{{")
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), "")


if __name__ == "__main__":
    unittest.main()
