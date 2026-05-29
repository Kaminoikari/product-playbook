#!/usr/bin/env python3
"""Detect structural drift between English references/*.md and i18n/*/references/*.md.

This is v1 of the i18n mirror agent — deterministic, no LLM. After an English-side
edit to references/ (e.g. adding a new Hard Gate block), this report tells the
writer exactly which i18n files need to be re-mirrored and which signals diverged.

Signals compared per (source, target) pair:
  - Count signals: "Hard Gate" mentions, ## / ### headings, code fences, FAIL markers
  - Vocab signals: canonical JTBD vocabulary tokens (fear, anxiety, shame, ...)
    must appear in i18n in English with local-language gloss in parentheses
  - Size signal: i18n line count below 85% of source => warn

Severity:
  - critical: vocab token missing or under-represented (behavioral risk)
  - warning:  structural count divergence (Hard Gate, headings, fences)
  - info:     line-count ratio drift only

Input:  references/*.md and i18n/<lang>/references/*.md
Output: docs/i18n-drift-<YYYY-MM-DD>.md (default; --output overrides)
        or JSON to stdout with --json (for v2 mirror agent to consume)
Exit:   0 if no drift, 1 if any critical drift, 2 if only warning/info drift
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

LANGS = ["zh-TW", "zh-CN", "ja", "ko", "es"]

VOCAB = [
    "fear", "anxiety", "shame", "worry", "dread",
    "self-doubt", "sense of loss", "threat to identity",
    "embarrassment", "guilt",
]

COUNT_SIGNALS = {
    "Hard Gate mentions": lambda s: len(re.findall(r"Hard Gate", s)),
    "## headings":        lambda s: len(re.findall(r"^## ", s, re.M)),
    "### headings":       lambda s: len(re.findall(r"^### ", s, re.M)),
    "code fences":        lambda s: s.count("```"),
    "FAIL markers":       lambda s: len(re.findall(r"\bFAIL\b", s)),
}

LINE_RATIO_WARN = 0.85

SEVERITY_EMOJI = {"critical": "🔴", "warning": "🟡", "info": "🔵"}
SEVERITY_WEIGHT = {"critical": 15, "warning": 5, "info": 1}


def analyze(text: str) -> tuple[dict[str, int], dict[str, int], int]:
    counts = {name: fn(text) for name, fn in COUNT_SIGNALS.items()}
    vocab = {
        v: len(re.findall(r"\b" + re.escape(v) + r"\b", text, re.I))
        for v in VOCAB
    }
    lines = text.count("\n")
    return counts, vocab, lines


def compare(src_text: str, tgt_text: str) -> list[dict]:
    """Return list of drift entries. Each entry: {kind, signal, source, target, severity}."""
    s_counts, s_vocab, s_lines = analyze(src_text)
    t_counts, t_vocab, t_lines = analyze(tgt_text)
    drifts = []
    for name in COUNT_SIGNALS:
        if t_counts[name] < s_counts[name]:
            drifts.append({
                "kind": "structural-under",
                "signal": name,
                "source": s_counts[name],
                "target": t_counts[name],
                "severity": "warning",
            })
        elif t_counts[name] > s_counts[name] + 2:
            # tolerate +1/+2 (inline `Hard Gate` backticks in CJK)
            drifts.append({
                "kind": "structural-over",
                "signal": name,
                "source": s_counts[name],
                "target": t_counts[name],
                "severity": "info",
            })
    for v in VOCAB:
        if s_vocab[v] > 0 and t_vocab[v] < s_vocab[v]:
            drifts.append({
                "kind": "vocab-under",
                "signal": f"vocab `{v}`",
                "source": s_vocab[v],
                "target": t_vocab[v],
                "severity": "critical",
            })
    if s_lines > 0 and (t_lines / s_lines) < LINE_RATIO_WARN:
        drifts.append({
            "kind": "size",
            "signal": "line count ratio",
            "source": s_lines,
            "target": t_lines,
            "severity": "info",
        })
    return drifts


def scan(repo_root: Path, file_filter: str | None, lang_filter: str | None) -> dict:
    """Walk references/ and emit per-file drift report data."""
    refs_dir = repo_root / "references"
    if not refs_dir.is_dir():
        raise SystemExit(f"references/ not found under {repo_root}")

    source_files = sorted(p for p in refs_dir.glob("*.md") if p.is_file())
    if file_filter:
        source_files = [p for p in source_files if file_filter in p.name]

    langs = [lang_filter] if lang_filter else LANGS
    for lang in langs:
        if lang not in LANGS:
            raise SystemExit(f"unknown lang {lang!r}; must be one of {LANGS}")

    clusters = []
    clean = 0
    missing = []
    for src in source_files:
        src_text = src.read_text(encoding="utf-8")
        for lang in langs:
            tgt = repo_root / "i18n" / lang / "references" / src.name
            if not tgt.is_file():
                missing.append({"source": str(src.relative_to(repo_root)),
                                "target": str(tgt.relative_to(repo_root)),
                                "lang": lang})
                continue
            tgt_text = tgt.read_text(encoding="utf-8")
            drifts = compare(src_text, tgt_text)
            if not drifts:
                clean += 1
                continue
            weight = sum(SEVERITY_WEIGHT[d["severity"]] for d in drifts)
            clusters.append({
                "source": str(src.relative_to(repo_root)),
                "target": str(tgt.relative_to(repo_root)),
                "lang": lang,
                "drifts": drifts,
                "weight": weight,
            })
    clusters.sort(key=lambda c: c["weight"], reverse=True)
    return {
        "generated": date.today().isoformat(),
        "summary": {
            "total_pairs": clean + len(clusters),
            "clean": clean,
            "drifted": len(clusters),
            "missing_files": len(missing),
        },
        "missing": missing,
        "clusters": clusters,
    }


def render_markdown(report: dict) -> str:
    lines = [
        f"# i18n Mirror Drift — {report['generated']}",
        "",
        "Source-of-truth: `references/*.md` (English)",
        f"Targets: {', '.join(LANGS)}",
        "",
        "## Summary",
        "",
        f"- Pairs scanned: **{report['summary']['total_pairs']}**",
        f"- Clean: **{report['summary']['clean']}**",
        f"- Drifted: **{report['summary']['drifted']}**",
        f"- Missing i18n files: **{report['summary']['missing_files']}**",
        "",
    ]
    if report["missing"]:
        lines += ["## Missing i18n Files", ""]
        for m in report["missing"]:
            lines.append(f"- 🚫 `{m['source']}` has no mirror at `{m['target']}`")
        lines.append("")
    if not report["clusters"]:
        lines += ["## Drift Clusters", "", "_None — all i18n files are in sync._", ""]
        return "\n".join(lines)

    lines += ["## Drift Clusters (highest debt first)", ""]
    for c in report["clusters"]:
        worst = max(d["severity"] for d in c["drifts"]) if c["drifts"] else "info"
        # need explicit severity ordering since 'max' on strings is lex
        order = {"info": 0, "warning": 1, "critical": 2}
        worst = max((d["severity"] for d in c["drifts"]), key=lambda s: order[s])
        lines += [
            f"### {SEVERITY_EMOJI[worst]} `{c['source']}` → `{c['target']}`",
            "",
            f"Lang: **{c['lang']}**  ·  Debt weight: **{c['weight']}**",
            "",
            "| Signal | Source | Target | Δ | Severity |",
            "|--------|-------:|-------:|--:|----------|",
        ]
        for d in c["drifts"]:
            delta = d["target"] - d["source"]
            sign = "+" if delta > 0 else ""
            lines.append(
                f"| {d['signal']} | {d['source']} | {d['target']} | "
                f"{sign}{delta} | {SEVERITY_EMOJI[d['severity']]} {d['severity']} |"
            )
        lines.append("")
        lines.append(
            "**How to fix**: open both files side-by-side, locate the section in the "
            "source that introduces the missing signal, and add the equivalent "
            "translated block to the target. Preserve canonical English vocabulary "
            "tokens (`fear`, `anxiety`, ...) verbatim with a local-language gloss in "
            "parentheses."
        )
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=Path.cwd(),
                    help="Repo root (default: cwd)")
    ap.add_argument("--file", type=str, default=None,
                    help="Filter to reference filenames containing this substring (e.g. '02b-jtbd')")
    ap.add_argument("--lang", type=str, default=None,
                    help=f"Filter to one language (one of {LANGS})")
    ap.add_argument("--output", type=Path, default=None,
                    help="Markdown report path (default: docs/i18n-drift-<date>.md)")
    ap.add_argument("--json", action="store_true",
                    help="Emit JSON to stdout instead of markdown to file")
    args = ap.parse_args()

    report = scan(args.root.resolve(), args.file, args.lang)

    if args.json:
        json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
        print()
    else:
        out = args.output or args.root / "docs" / f"i18n-drift-{report['generated']}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_markdown(report), encoding="utf-8")
        print(f"wrote {out}", file=sys.stderr)

    has_critical = any(
        d["severity"] == "critical"
        for c in report["clusters"]
        for d in c["drifts"]
    )
    if has_critical:
        return 1
    if report["clusters"] or report["missing"]:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
