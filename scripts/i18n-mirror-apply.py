#!/usr/bin/env python3
"""LLM-driven i18n mirror agent. v2 of closed-loop self-correction.

Reads `scripts/i18n-drift-report.py --json` output, identifies clusters with
non-info drift, and asks `claude -p` to translate the missing/under-mirrored
content into each i18n target file. Always dry-run unless --apply is passed.

Why semi-automated, not fully automated:
  The translation step is high-leverage but high-risk — bad output can pollute
  reference files that orchestrators load. This agent prints a unified diff
  for every cluster and exits before writing unless the caller passes --apply.
  The human gate sits exactly between "LLM proposes" and "files change".

Why whole-file reconciliation instead of section surgery:
  Earlier prototypes tried to extract changed source blocks and patch them
  into the target at heading anchors. Anchor resolution is the dominant
  failure mode (translated headers don't lexically match source). Whole-file
  reconciliation gives the LLM full context to reproduce structure faithfully
  at the cost of larger prompts. Per-call latency ~30-90s, ~5-15k tokens.

Safety:
  - Default dry-run. --apply required to write.
  - --max N cap (default 3) bounds blast radius per invocation.
  - Subprocess timeout 600s per file.
  - Token cap: skips files where source+target > MAX_INPUT_CHARS (~24KB)
    to avoid silently truncating long files.
  - Uses subscription token from active claude session (no API billing).
  - Never re-translates inside code fences (instructed via prompt + verified
    post-hoc by comparing fence count source vs output).
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

DRIFT_SCRIPT = Path(__file__).parent / "i18n-drift-report.py"

LANG_NAME = {
    "zh-TW": "Traditional Chinese (繁體中文, Taiwan)",
    "zh-CN": "Simplified Chinese (简体中文)",
    "ja": "Japanese (日本語)",
    "ko": "Korean (한국어)",
    "es": "Spanish (Español)",
}

CANONICAL_VOCAB = [
    "fear", "anxiety", "shame", "worry", "dread",
    "self-doubt", "sense of loss", "threat to identity",
    "embarrassment", "guilt",
]

MAX_INPUT_CHARS = 36_000
CLAUDE_TIMEOUT_SECONDS = 600

MISSING_PROMPT_TEMPLATE = """You are a faithful translator creating an i18n mirror of a product-playbook PM-skill reference file. The English source is the source of truth; no {lang_name} translation exists yet.

<SOURCE_FILE language="English" path="{source_path}">
{source_content}
</SOURCE_FILE>

Your task: produce a complete {lang_name} translation that mirrors the SOURCE file exactly in structure (every heading, every list, every code block, every table) while reading naturally in {lang_name}.

Rules:
1. Mirror SOURCE's section structure, headers, code blocks, table layouts, and content depth. Same number of `##`/`###` headings, same number of code fences.
2. Preserve these canonical English vocabulary tokens VERBATIM, with a parenthetical {lang_name} gloss on first introduction in each section: {canonical_vocab}
3. Preserve these English KEYWORDS VERBATIM (do NOT translate them — they function as enforcement markers that downstream tooling greps for): `FAIL`, `Hard Gate`, `Bootstrap`.
4. Preserve ALL code-fenced (```) block contents VERBATIM — no translation inside fences.
5. Preserve markdown table structure (same number of rows and columns as source).
6. Preserve any YAML frontmatter at the top of the file VERBATIM — those keys (`name:`, `description:`, etc.) are machine-read.
7. Output ONLY the full {lang_name} target file content, wrapped in <UPDATED_TARGET> ... </UPDATED_TARGET> tags. No preamble, no diff, no explanation outside the tags.

Begin output now."""

PROMPT_TEMPLATE = """You are a faithful translator updating an i18n mirror of a product-playbook PM-skill reference file. The English source is the source of truth; the {lang_name} target has drifted out of sync.

<SOURCE_FILE language="English" path="{source_path}">
{source_content}
</SOURCE_FILE>

<TARGET_FILE language="{lang_name}" path="{target_path}">
{target_content}
</TARGET_FILE>

<DRIFT_SIGNALS>
{drift_summary}
</DRIFT_SIGNALS>

Your task: produce an updated {lang_name} target file that mirrors the SOURCE's structure and content depth while preserving the TARGET's existing translation style for passages already faithful.

Rules:
1. Mirror SOURCE's section structure, headers, code blocks, table layouts, and content depth.
2. Where TARGET already faithfully translates a passage, keep that translation — do not re-translate for cosmetic differences.
3. Where TARGET is missing content the SOURCE has, translate it into {lang_name} and insert at the structurally equivalent position.
4. Preserve these canonical English vocabulary tokens VERBATIM, with a parenthetical {lang_name} gloss on first introduction in each section: {canonical_vocab}
5. Preserve these English KEYWORDS VERBATIM (do NOT translate them — they function as enforcement markers that downstream tooling greps for): `FAIL`, `Hard Gate`, `Bootstrap`. Example: "Responses ending with ... FAIL the contract" must stay "FAIL" in the target language, not be translated to "失敗"/"불합격"/"falla"/etc.
6. Preserve ALL code-fenced (```) block contents VERBATIM — no translation inside fences.
7. Preserve markdown table structure (same number of rows and columns as source).
8. Do not add or remove top-level (## or #) sections that exist in source.
9. Output ONLY the full rewritten target file content, wrapped in <UPDATED_TARGET> ... </UPDATED_TARGET> tags. No preamble, no diff, no explanation outside the tags.

Begin output now."""


def load_drift_report(root: Path, file_filter: str | None, lang_filter: str | None) -> dict:
    cmd = ["python3", str(DRIFT_SCRIPT), "--root", str(root), "--json"]
    if file_filter:
        cmd += ["--file", file_filter]
    if lang_filter:
        cmd += ["--lang", lang_filter]
    # drift report exits 0 (clean), 1 (critical), or 2 (warning/info) — all
    # are valid "report produced" states; only fail on other codes
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode not in (0, 1, 2):
        raise RuntimeError(
            f"drift report exited {result.returncode}\nstderr: {result.stderr[:500]}"
        )
    return json.loads(result.stdout)


def build_drift_summary(drifts: list[dict]) -> str:
    if not drifts:
        return "No specific signals — full structural reconciliation requested."
    lines = []
    for d in drifts:
        delta = d["target"] - d["source"]
        sign = "+" if delta > 0 else ""
        lines.append(
            f"- [{d['severity']}] {d['signal']}: source has {d['source']}, "
            f"target has {d['target']} ({sign}{delta})"
        )
    return "\n".join(lines)


def call_claude(prompt: str) -> str:
    """Invoke claude -p, return raw output. Raises on timeout or non-zero exit."""
    result = subprocess.run(
        ["claude", "-p", "--output-format", "text"],
        input=prompt,
        capture_output=True,
        text=True,
        timeout=CLAUDE_TIMEOUT_SECONDS,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"claude -p exited {result.returncode}\nstderr: {result.stderr[:500]}"
        )
    return result.stdout


def extract_updated(raw: str) -> str:
    m = re.search(r"<UPDATED_TARGET>\s*\n(.*?)\n\s*</UPDATED_TARGET>", raw, re.DOTALL)
    if not m:
        raise ValueError(
            "Could not find <UPDATED_TARGET> tags in output. First 500 chars:\n"
            + raw[:500]
        )
    return m.group(1)


def verify_no_fence_drift(source: str, target: str, updated: str) -> list[str]:
    """Catch obvious LLM mistakes before showing the diff to a human."""
    warnings = []
    src_fences = source.count("```")
    out_fences = updated.count("```")
    if out_fences != src_fences:
        warnings.append(
            f"code fence count mismatch: source={src_fences}, updated={out_fences} "
            f"(LLM may have translated inside fences or dropped a block)"
        )
    for vocab in CANONICAL_VOCAB:
        # match same boundary semantics as drift detector
        pat = r"(?<![A-Za-z])" + re.escape(vocab) + r"s?(?![A-Za-z])"
        src_n = len(re.findall(pat, source, re.I))
        if src_n > 0:
            out_n = len(re.findall(pat, updated, re.I))
            if out_n == 0:
                warnings.append(
                    f"canonical token {vocab!r} present in source but absent in updated"
                )
    return warnings


def render_diff(target_path: str, current: str, updated: str) -> str:
    return "".join(difflib.unified_diff(
        current.splitlines(keepends=True),
        updated.splitlines(keepends=True),
        fromfile=f"a/{target_path}",
        tofile=f"b/{target_path}",
        n=3,
    ))


def process_cluster(cluster: dict, root: Path, apply: bool, log_lines: list[str]) -> dict:
    source_path = root / cluster["source"]
    target_path = root / cluster["target"]
    source = source_path.read_text(encoding="utf-8")
    is_missing = not target_path.is_file()
    target = "" if is_missing else target_path.read_text(encoding="utf-8")

    total_chars = len(source) + len(target)
    if total_chars > MAX_INPUT_CHARS:
        return {
            "cluster": cluster,
            "status": "skipped",
            "reason": f"source+target too large ({total_chars} > {MAX_INPUT_CHARS} chars); manual edit recommended",
        }

    if is_missing:
        prompt = MISSING_PROMPT_TEMPLATE.format(
            lang_name=LANG_NAME[cluster["lang"]],
            source_path=cluster["source"],
            source_content=source,
            canonical_vocab=", ".join(CANONICAL_VOCAB),
        )
    else:
        prompt = PROMPT_TEMPLATE.format(
            lang_name=LANG_NAME[cluster["lang"]],
            source_path=cluster["source"],
            target_path=cluster["target"],
            source_content=source,
            target_content=target,
            drift_summary=build_drift_summary(cluster["drifts"]),
            canonical_vocab=", ".join(CANONICAL_VOCAB),
        )

    log_lines.append(f"\n=== {cluster['target']} (lang={cluster['lang']}) ===")
    log_lines.append(f"  invoking claude -p (input ~{len(prompt)} chars)...")
    try:
        raw = call_claude(prompt)
    except subprocess.TimeoutExpired:
        return {"cluster": cluster, "status": "timeout", "reason": "claude -p exceeded 600s"}
    except RuntimeError as e:
        return {"cluster": cluster, "status": "error", "reason": str(e)}

    try:
        updated = extract_updated(raw)
    except ValueError as e:
        return {"cluster": cluster, "status": "parse-error", "reason": str(e)}

    warnings = verify_no_fence_drift(source, target, updated)
    diff = render_diff(cluster["target"], target, updated)

    if not diff.strip():
        return {"cluster": cluster, "status": "no-change", "diff": ""}

    if apply:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(updated, encoding="utf-8")
        status = "applied"
    else:
        status = "dry-run"

    return {
        "cluster": cluster,
        "status": status,
        "diff": diff,
        "warnings": warnings,
        "diff_lines": diff.count("\n"),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=Path.cwd())
    ap.add_argument("--file", type=str, default=None,
                    help="Filter to reference files containing this substring")
    ap.add_argument("--lang", type=str, default=None,
                    help=f"Filter to one lang ({list(LANG_NAME)})")
    ap.add_argument("--apply", action="store_true",
                    help="Write changes to target files (default: dry-run, diff only)")
    ap.add_argument("--max", type=int, default=3,
                    help="Cap on number of clusters to process per invocation (default 3)")
    ap.add_argument("--include-warnings", action="store_true",
                    help="Process warning-level clusters too (default: critical only)")
    args = ap.parse_args()

    root = args.root.resolve()
    print(f"loading drift report...", file=sys.stderr)
    report = load_drift_report(root, args.file, args.lang)

    # Missing-file mirrors are conceptually critical drift (whole file absent)
    # — synthesize cluster-shaped entries so they flow through the same
    # eligibility + processing pipeline. The drift_summary will be empty;
    # process_cluster() detects the missing target and switches prompts.
    missing_clusters = []
    for m in report.get("missing", []):
        lang_seg = m["target"].split("/")[1]  # i18n/<lang>/...
        missing_clusters.append({
            "source": m["source"],
            "target": m["target"],
            "lang": lang_seg,
            "drifts": [{"signal": "missing-file", "severity": "critical",
                        "source": 1, "target": 0}],
        })

    eligible = []
    for c in list(missing_clusters) + list(report["clusters"]):
        worst = max((d["severity"] for d in c["drifts"]),
                    key=lambda s: {"info": 0, "warning": 1, "critical": 2}[s])
        if worst == "critical" or (args.include_warnings and worst == "warning"):
            eligible.append(c)

    print(f"eligible clusters: {len(eligible)} (cap: {args.max})", file=sys.stderr)
    if not eligible:
        print("nothing to do — no drift meets severity threshold", file=sys.stderr)
        return 0

    selected = eligible[: args.max]
    if len(eligible) > args.max:
        print(f"  (deferring {len(eligible) - args.max} cluster(s) — increase --max if intended)", file=sys.stderr)

    log_lines = [f"# i18n-mirror-apply run {date.today().isoformat()}",
                 f"# mode: {'APPLY' if args.apply else 'DRY-RUN'}",
                 f"# clusters: {len(selected)}"]
    results = []
    for i, cluster in enumerate(selected, 1):
        print(f"\n[{i}/{len(selected)}] {cluster['target']} ({cluster['lang']})", file=sys.stderr)
        r = process_cluster(cluster, root, args.apply, log_lines)
        results.append(r)
        print(f"  status: {r['status']}", file=sys.stderr)
        if r.get("warnings"):
            for w in r["warnings"]:
                print(f"  ⚠️  {w}", file=sys.stderr)
        if r.get("diff"):
            print(f"\n--- diff for {cluster['target']} ---")
            print(r["diff"])
        elif r.get("reason"):
            print(f"  reason: {r['reason']}", file=sys.stderr)

    log_path = root / "logs" / f"i18n-mirror-{date.today().isoformat()}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    print(f"\nlog: {log_path}", file=sys.stderr)

    summary = {
        s: sum(1 for r in results if r["status"] == s)
        for s in ["dry-run", "applied", "no-change", "skipped", "timeout", "error", "parse-error"]
    }
    print(f"\nsummary: {summary}", file=sys.stderr)

    if not args.apply and any(r["status"] == "dry-run" for r in results):
        print("\nto write these changes: re-run with --apply", file=sys.stderr)

    has_failures = any(r["status"] in ("timeout", "error", "parse-error") for r in results)
    return 1 if has_failures else 0


if __name__ == "__main__":
    sys.exit(main())
