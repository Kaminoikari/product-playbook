#!/usr/bin/env python3
"""Test whether the installed product-playbook skill triggers for each query.

Uses `claude -p` with stream-json output and counts a trigger when either an
explicit Skill tool_use names a product-playbook skill or the response carries
product-playbook's provenance line (the meta-skill is often applied inline
without a formal Skill call). Tests the REAL installed skill, not a temp
command file.

Severity convention (since trigger items have no per-item severity):
  - false negative (should_trigger=true but skill did NOT fire) -> critical
  - false positive (should_trigger=false but skill DID fire)    -> warning
  - true positive / true negative                               -> pass

This matches portaly-sentry's CRITICAL/WARNING/INFO split: a missed trigger
silently breaks the user-facing skill (critical); a spurious trigger is
noisy but recoverable (warning).
"""

import argparse
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from compute_eval_score import (  # noqa: E402
    compute_score,
    format_summary_markdown,
    should_fail,
)
from eval_env import plugin_isolation_args  # noqa: E402


# product-playbook's provenance line ("— Frameworks: X · Y") is unique to its
# output, so finding it is a high-precision signal that the meta-skill drove the
# response even when the skill was applied inline without a formal Skill call.
_PROVENANCE_RE = re.compile(r"[-—–]{1,2}\s*Frameworks:")


def _detect_trigger(output: str) -> bool:
    """Whether stream-json `output` shows product-playbook engaged.

    Either signal suffices:
      1. an explicit Skill tool_use naming a product-playbook skill, or
      2. the product-playbook provenance line in the assistant text, which it
         emits inline even when it applies the meta-skill without a Skill call.
    """
    for line in output.split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        if event.get("type") == "assistant":
            for block in event.get("message", {}).get("content", []):
                btype = block.get("type")
                if btype == "tool_use" and block.get("name") == "Skill":
                    inp = json.dumps(block.get("input", {}))
                    if "product-playbook" in inp or "product-" in inp:
                        return True
                if btype == "text" and _PROVENANCE_RE.search(block.get("text", "")):
                    return True

        if event.get("type") == "stream_event":
            se = event.get("event", {})
            if se.get("type") == "content_block_start":
                cb = se.get("content_block", {})
                if cb.get("type") == "tool_use" and cb.get("name") == "Skill":
                    return True

    return False


def test_single_query(query: str, timeout: int = 60) -> bool:
    """Run a single query and return whether product-playbook skill was triggered."""
    cmd = [
        "claude", "-p", query,
        "--output-format", "stream-json",
        "--verbose",
        # 4 turns, not 1-2: the meta-skill often needs a couple of turns to
        # commit to a lens and start delivering, and its trigger signals (the
        # Skill call or the provenance line) do not appear until it does. Fewer
        # turns truncate real triggers into false negatives.
        "--max-turns", "4",
    ] + plugin_isolation_args()

    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True,
            timeout=timeout, env=env,
            cwd=str(Path.home())
        )
        output = result.stdout
    except subprocess.TimeoutExpired:
        return False

    return _detect_trigger(output)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval-file", default=str(Path(__file__).parent / "trigger-eval.json"))
    ap.add_argument("--runs", type=int, default=1, help="Runs per query (default 1)")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=60)
    ap.add_argument("--fail-on", choices=["critical", "any", "none"], default="none")
    ap.add_argument("--json", dest="json_out", default=None,
                    help="Path to write machine-readable results")
    ap.add_argument("--markdown", dest="markdown_out", default=None,
                    help="Path to write GitHub-flavored Markdown summary")
    args = ap.parse_args()

    eval_path = Path(args.eval_file)
    eval_set = json.loads(eval_path.read_text(encoding="utf-8"))

    print(f"Testing {len(eval_set)} queries × {args.runs} runs (workers={args.workers}) from {eval_path.name}")
    print("=" * 72)

    expectation_results = []
    per_query = []
    tp = fp = tn = fn = 0

    for i, item in enumerate(eval_set):
        query = item["query"]
        expected = item["should_trigger"]
        triggers = 0

        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            futures = [
                pool.submit(test_single_query, query, args.timeout)
                for _ in range(args.runs)
            ]
            for f in as_completed(futures):
                if f.result():
                    triggers += 1

        trigger_rate = triggers / args.runs
        fired = trigger_rate >= 0.5
        passed = (expected == fired)

        if passed:
            if expected:
                tp += 1
            else:
                tn += 1
            severity = "info"
        else:
            if expected and not fired:
                fn += 1
                severity = "critical"
            else:
                fp += 1
                severity = "warning"

        status = "PASS" if passed else "FAIL"
        label = "should_trigger" if expected else "should_NOT_trigger"
        print(f"  [{status}] rate={triggers}/{args.runs} ({label}): {query[:80]}")

        per_query.append({
            "query": query,
            "should_trigger": expected,
            "fired": fired,
            "triggers": triggers,
            "runs": args.runs,
            "trigger_rate": trigger_rate,
            "pass": passed,
            "severity_on_fail": severity,
        })

        expectation_results.append({
            "eval_id": i + 1,
            "eval_name": f"trigger-query-{i + 1}",
            "expectation_text": f"{'Should' if expected else 'Should NOT'} trigger product-playbook: {query[:120]}",
            "severity": severity,
            "passed": passed,
        })

    summary = compute_score(expectation_results)
    print("=" * 72)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    accuracy = (tp + tn) / len(eval_set) if eval_set else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    print(f"Confusion: TP={tp} FP={fp} TN={tn} FN={fn}")
    print(f"  Precision={precision:.0%} Recall={recall:.0%} Accuracy={accuracy:.0%} F1={f1:.0%}")
    print(f"Score: {summary['score']}/100  band={summary['band']}")
    print(f"  critical_failures={summary['critical_failures']} (false negatives)  "
          f"warning_failures={summary['warning_failures']} (false positives)")

    if args.json_out:
        Path(args.json_out).write_text(json.dumps({
            "kind": "trigger",
            "eval_file": eval_path.name,
            "runs_per_query": args.runs,
            "per_query": per_query,
            "confusion": {"tp": tp, "fp": fp, "tn": tn, "fn": fn,
                          "precision": precision, "recall": recall,
                          "accuracy": accuracy, "f1": f1},
            "summary": {k: v for k, v in summary.items() if k != "breakdown"},
            "breakdown": summary["breakdown"],
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  → wrote {args.json_out}")

    if args.markdown_out:
        Path(args.markdown_out).write_text(
            format_summary_markdown(summary, title="Trigger Eval Results"),
            encoding="utf-8",
        )
        print(f"  → wrote {args.markdown_out}")

    return 1 if should_fail(summary, args.fail_on) else 0


if __name__ == "__main__":
    sys.exit(main())
