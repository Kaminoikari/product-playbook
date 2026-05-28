#!/usr/bin/env python3
"""Behavioral eval runner for product-playbook.

For each eval item in evals.json:
  1. Run the prompt through `claude -p` headless and capture the response text.
  2. Hand the response + every expectation to a second `claude -p` judge call,
     which returns strict JSON {expectations: [{text, passed, reason}, ...]}.
  3. Repeat N times (default 3) and take per-expectation majority vote.
  4. Compute aggregate score via compute_eval_score.compute_score.
  5. Exit non-zero if --fail-on threshold is hit.

Designed to run both locally and in CI. CI typically uses --runs 1 for cost.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from compute_eval_score import (
    compute_score,
    format_summary_markdown,
    should_fail,
)


JUDGE_SYSTEM_PROMPT = """You are a strict evaluator. You will receive an AI assistant's response together with a list of expectations. For each expectation, decide whether the response satisfies it.

Return ONLY a single JSON object, no prose, no markdown fences:
{"expectations":[{"index":0,"passed":true,"reason":"..."},{"index":1,"passed":false,"reason":"..."}]}

- "passed" must be a boolean.
- "reason" must be a single sentence (<= 200 chars) explaining the judgement, quoting the response where useful.
- Output exactly one entry per expectation, in the same order, with the matching "index".
- Be strict: if an expectation has multiple requirements, all must be met to pass.
- Judge only what is in the response; do not assume hidden content."""


def _run_claude(prompt: str, timeout: int, system: str | None = None, output_format: str = "text") -> str:
    """Invoke `claude -p` and return stdout text."""
    cmd = ["claude", "-p", prompt, "--output-format", output_format]
    if system:
        cmd += ["--append-system-prompt", system]
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    proc = subprocess.run(
        cmd, capture_output=True, text=True, timeout=timeout, env=env
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"claude exited {proc.returncode}: {proc.stderr[:500]}"
        )
    return proc.stdout


def get_response(prompt: str, timeout: int = 180) -> str:
    """Run the user prompt through claude headless and return the assistant text."""
    return _run_claude(prompt, timeout=timeout).strip()


def _parse_judge_output(raw: str) -> dict | None:
    """Best-effort JSON extraction from judge stdout. Returns None on failure."""
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1:
        return None
    try:
        return json.loads(raw[start : end + 1])
    except json.JSONDecodeError:
        return None


def _judge_output_complete(parsed: object, expected_count: int) -> bool:
    """Verify parsed payload has exactly N expectations with indexes 0..N-1.

    Guards against the model emitting a structurally valid but fabricated
    JSON when the repair retry has no other anchor to reason from.
    """
    if not isinstance(parsed, dict):
        return False
    exps = parsed.get("expectations")
    if not isinstance(exps, list) or len(exps) != expected_count:
        return False
    indexes = {e.get("index") for e in exps if isinstance(e, dict)}
    return indexes == set(range(expected_count))


def judge(response_text: str, expectations: list[dict], timeout: int = 120) -> list[dict]:
    """Ask claude to judge the response against every expectation in one shot."""
    numbered = "\n".join(
        f"{i}. {exp['text']}" for i, exp in enumerate(expectations)
    )
    judge_prompt = (
        "Response under evaluation (between <response> tags):\n"
        f"<response>\n{response_text}\n</response>\n\n"
        "Expectations to evaluate (one judgement per line):\n"
        f"{numbered}\n\n"
        "Return the JSON object now."
    )
    expected_count = len(expectations)
    raw = _run_claude(judge_prompt, timeout=timeout, system=JUDGE_SYSTEM_PROMPT)
    parsed = _parse_judge_output(raw)
    if parsed is None or not _judge_output_complete(parsed, expected_count):
        # First attempt unusable — retry with the FULL original judge prompt
        # plus the malformed previous output. `claude -p` is stateless, so
        # without re-feeding response + expectations the repair model has
        # no anchor and may fabricate verdicts (Codex PR #9 P2-1).
        repair_prompt = (
            f"{judge_prompt}\n\n"
            "Your previous attempt did not produce a valid, complete JSON "
            "object. The raw previous output was:\n"
            f"<previous_output>\n{raw}\n</previous_output>\n\n"
            "Re-evaluate the response above against every expectation and "
            "re-emit ONLY the JSON object described in the system prompt — "
            "no prose, no fences, no second object. Start with `{` and end "
            "with `}`. Use escaped quotes inside reason strings. Output "
            f"exactly {expected_count} entries with indexes 0..{expected_count - 1}."
        )
        raw = _run_claude(repair_prompt, timeout=timeout, system=JUDGE_SYSTEM_PROMPT)
        parsed = _parse_judge_output(raw)
        if parsed is None or not _judge_output_complete(parsed, expected_count):
            raise RuntimeError(
                f"judge returned incomplete/non-JSON after retry "
                f"(expected {expected_count} indexed expectations): {raw[:200]}"
            )

    by_index = {item["index"]: item for item in parsed.get("expectations", [])}
    out = []
    for i, exp in enumerate(expectations):
        verdict = by_index.get(i, {})
        out.append({
            "text": exp["text"],
            "severity": exp["severity"],
            "passed": bool(verdict.get("passed", False)),
            "reason": str(verdict.get("reason", ""))[:400],
        })
    return out


def run_single(eval_item: dict, runs: int, response_timeout: int, judge_timeout: int) -> list[dict]:
    """Run one eval item N times and return per-expectation aggregated results."""
    n_exp = len(eval_item["expectations"])
    # tally[i] = list of (passed: bool, reason: str)
    tally: list[list[tuple[bool, str]]] = [[] for _ in range(n_exp)]

    for run_idx in range(runs):
        try:
            response = get_response(eval_item["prompt"], timeout=response_timeout)
        except (subprocess.TimeoutExpired, RuntimeError) as e:
            print(f"    run {run_idx + 1}/{runs}: response failed: {e}", file=sys.stderr)
            for i in range(n_exp):
                tally[i].append((False, f"response error: {e}"))
            continue
        try:
            verdicts = judge(response, eval_item["expectations"], timeout=judge_timeout)
        except (subprocess.TimeoutExpired, RuntimeError) as e:
            print(f"    run {run_idx + 1}/{runs}: judge failed: {e}", file=sys.stderr)
            for i in range(n_exp):
                tally[i].append((False, f"judge error: {e}"))
            continue
        for i, v in enumerate(verdicts):
            tally[i].append((v["passed"], v["reason"]))

    # Aggregate via majority vote per expectation
    results = []
    for i, exp in enumerate(eval_item["expectations"]):
        passes = sum(1 for p, _ in tally[i] if p)
        results.append({
            "eval_id": eval_item["id"],
            "eval_name": eval_item["name"],
            "expectation_text": exp["text"],
            "severity": exp["severity"],
            "passes": passes,
            "runs": runs,
            "passed": passes * 2 > runs,  # strict majority (> 50%)
            "reasons": [r for _, r in tally[i]],
        })
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval-file", default=str(Path(__file__).parent / "evals.json"))
    ap.add_argument("--runs", type=int, default=3, help="Runs per eval for majority vote (default 3)")
    ap.add_argument("--workers", type=int, default=2, help="Parallel evals")
    ap.add_argument("--response-timeout", type=int, default=180)
    ap.add_argument("--judge-timeout", type=int, default=120)
    ap.add_argument("--fail-on", choices=["critical", "any", "none"], default="none",
                    help="Exit non-zero if this severity threshold is hit")
    ap.add_argument("--json", dest="json_out", default=None,
                    help="Path to write machine-readable results")
    ap.add_argument("--markdown", dest="markdown_out", default=None,
                    help="Path to write GitHub-flavored Markdown summary")
    ap.add_argument("--only", default=None,
                    help="Comma-separated list of eval ids or names to run (default: all)")
    args = ap.parse_args()

    eval_path = Path(args.eval_file)
    data = json.loads(eval_path.read_text())
    items = data["evals"]

    if args.only:
        wanted = {s.strip() for s in args.only.split(",")}
        items = [
            it for it in items
            if str(it["id"]) in wanted or it["name"] in wanted
        ]
        if not items:
            print(f"No evals matched --only={args.only}", file=sys.stderr)
            return 2

    print(f"Running {len(items)} evals × {args.runs} runs (workers={args.workers}) from {eval_path.name}")
    print("=" * 72)

    all_results: list[dict] = []
    per_eval_status = []

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(run_single, it, args.runs, args.response_timeout, args.judge_timeout): it
            for it in items
        }
        for fut in as_completed(futures):
            it = futures[fut]
            try:
                results = fut.result()
            except Exception as e:
                print(f"  [ERROR] eval {it['id']} ({it['name']}): {e}")
                continue
            all_results.extend(results)
            pass_n = sum(1 for r in results if r["passed"])
            per_eval_status.append({"id": it["id"], "name": it["name"], "pass": pass_n, "total": len(results)})
            print(f"  [{it['id']:>2}] {it['name']:<40} {pass_n}/{len(results)} expectations passed")

    summary = compute_score(all_results)
    print("=" * 72)
    print(f"Score: {summary['score']}/100  band={summary['band']}")
    print(f"  critical_failures={summary['critical_failures']}  "
          f"warning_failures={summary['warning_failures']}  "
          f"info_failures={summary['info_failures']}")
    print(f"  passed {summary['passed_expectations']}/{summary['total_expectations']} expectations")

    if args.json_out:
        Path(args.json_out).write_text(json.dumps({
            "kind": "behavioral",
            "eval_file": eval_path.name,
            "runs_per_eval": args.runs,
            "per_eval": per_eval_status,
            "summary": {k: v for k, v in summary.items() if k != "breakdown"},
            "breakdown": summary["breakdown"],
        }, indent=2, ensure_ascii=False))
        print(f"  → wrote {args.json_out}")

    if args.markdown_out:
        Path(args.markdown_out).write_text(
            format_summary_markdown(summary, title="Behavioral Eval Results")
        )
        print(f"  → wrote {args.markdown_out}")

    return 1 if should_fail(summary, args.fail_on) else 0


if __name__ == "__main__":
    sys.exit(main())
