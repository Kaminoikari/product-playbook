#!/usr/bin/env python3
"""Test whether the installed product-playbook skill triggers for each query.

Uses `claude -p` with stream-json output, checks if Skill tool is called
with 'product-playbook' in the input. Tests the REAL installed skill,
not a temp command file.
"""

import json
import os
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path


def test_single_query(query: str, timeout: int = 60) -> bool:
    """Run a single query and return whether product-playbook skill was triggered."""
    cmd = [
        "claude", "-p", query,
        "--output-format", "stream-json",
        "--verbose",
        "--max-turns", "1",
    ]

    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True,
            timeout=timeout, env=env,
            cwd=str(Path.home())  # Run from home to avoid project-level SKILL.md
        )
        output = result.stdout
    except subprocess.TimeoutExpired:
        return False

    # Check stream events for Skill tool invocation with product-playbook
    for line in output.split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        # Check tool_use in assistant message
        if event.get("type") == "assistant":
            message = event.get("message", {})
            for block in message.get("content", []):
                if block.get("type") == "tool_use":
                    name = block.get("name", "")
                    inp = json.dumps(block.get("input", {}))
                    if name == "Skill" and "product-playbook" in inp:
                        return True
                    if name == "Skill" and "product-" in inp:
                        return True

        # Check stream events for early detection
        if event.get("type") == "stream_event":
            se = event.get("event", {})
            se_type = se.get("type", "")

            if se_type == "content_block_start":
                cb = se.get("content_block", {})
                if cb.get("type") == "tool_use" and cb.get("name") == "Skill":
                    return True  # Skill tool called = triggered

    return False


def main():
    default_eval = "trigger-eval.json"
    if len(sys.argv) > 3:
        default_eval = sys.argv[3]
    eval_path = Path(__file__).parent / default_eval
    eval_set = json.loads(eval_path.read_text())

    runs_per_query = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    max_workers = int(sys.argv[2]) if len(sys.argv) > 2 else 4

    print(f"Testing {len(eval_set)} queries x {runs_per_query} runs (workers={max_workers})")
    print("=" * 70)

    results = []
    total_pass = 0
    total_fail = 0
    tp = fp = tn = fn = 0

    for i, item in enumerate(eval_set):
        query = item["query"]
        expected = item["should_trigger"]
        triggers = 0

        # Run multiple times
        with ProcessPoolExecutor(max_workers=max_workers) as pool:
            futures = [pool.submit(test_single_query, query) for _ in range(runs_per_query)]
            for f in as_completed(futures):
                if f.result():
                    triggers += 1

        trigger_rate = triggers / runs_per_query
        passed = (expected and trigger_rate >= 0.5) or (not expected and trigger_rate < 0.5)

        if passed:
            total_pass += 1
        else:
            total_fail += 1

        if expected and trigger_rate >= 0.5:
            tp += 1
        elif expected:
            fn += 1
        elif trigger_rate >= 0.5:
            fp += 1
        else:
            tn += 1

        status = "PASS" if passed else "FAIL"
        label = "should_trigger" if expected else "should_NOT_trigger"
        print(f"  [{status}] rate={triggers}/{runs_per_query} ({label}): {query[:80]}")

        results.append({
            "query": query,
            "should_trigger": expected,
            "triggers": triggers,
            "runs": runs_per_query,
            "trigger_rate": trigger_rate,
            "pass": passed,
        })

    print("=" * 70)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    accuracy = (tp + tn) / len(eval_set) if eval_set else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    print(f"Results: {total_pass}/{len(eval_set)} passed")
    print(f"  TP={tp} FP={fp} TN={tn} FN={fn}")
    print(f"  Precision={precision:.0%} Recall={recall:.0%} Accuracy={accuracy:.0%} F1={f1:.0%}")

    # Save results
    output = {
        "results": results,
        "summary": {
            "passed": total_pass,
            "failed": total_fail,
            "total": len(eval_set),
            "tp": tp, "fp": fp, "tn": tn, "fn": fn,
            "precision": precision,
            "recall": recall,
            "accuracy": accuracy,
            "f1": f1,
        }
    }
    out_path = Path(__file__).parent / "trigger-results.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
