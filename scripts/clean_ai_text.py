#!/usr/bin/env python3
"""Clean + quarantine AI-side outputs before measurement.

1. Normalize in place: strip <think> blocks, markdown bold section-label
   prefixes ("**Background:**" / "Background:"), collapse blank lines.
   (Human-side structured abstracts were saved WITHOUT labels; AI side must match.)
2. Quarantine files whose content is meta-commentary/refusal rather than the
   requested text (e.g. "no closing summary is provided", "Here is the abstract").
   Quarantined files move to data/ai_quarantine/<model>/<section>/.

Usage: python -X utf8 scripts/clean_ai_text.py
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AI = ROOT / "data" / "ai"
QUAR = ROOT / "data" / "ai_quarantine"

META = re.compile(
    r"no closing summary|as an AI|I cannot|I can't|unable to (?:fulfill|complete|generate)"
    r"|I'll (?:write|draft|create)|I will (?:write|draft|create)|here (?:is|are) (?:the|a) "
    r"|below is (?:the|a) |^(?:sure|certainly)[,!]|sorry,? but|word (?:count|limit)"
    r"|cannot assist|instead of (?:the|a) (?:abstract|introduction|discussion)",
    re.I)
THINK = re.compile(r"<think>.*?</think>", re.S | re.I)
LABEL = re.compile(
    r"^\s*\*{0,2}(?:background|methods?|results?|conclusions?|objective|objectives|aims?"
    r"|design|setting|patients|participants|interventions|main outcome measures"
    r"|purpose|introduction|discussion|findings|limitations?)\*{0,2}\s*[:：]\s*\*{0,2}\s*",
    re.I)


def clean_text(t):
    t = THINK.sub("", t)
    t = re.sub(r"\*{1,3}", "", t)          # bold/italic markers
    t = re.sub(r"^#{1,4}\s*", "", t, flags=re.M)  # markdown headings
    lines = [LABEL.sub("", ln) for ln in t.splitlines()]
    t = "\n".join(lines)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip() + "\n"


def main():
    n_clean = n_quar = 0
    for f in sorted(AI.glob("*/*/*.md")):
        raw = f.read_text(encoding="utf-8", errors="ignore")
        if META.search(raw):
            dest = QUAR / f.parts[-3] / f.parts[-2]
            dest.mkdir(parents=True, exist_ok=True)
            shutil.move(str(f), str(dest / f.name))
            n_quar += 1
            print(f"[quarantine] {'/'.join(f.parts[-3:])}")
            continue
        cleaned = clean_text(raw)
        if cleaned != raw:
            f.write_text(cleaned, encoding="utf-8")
            n_clean += 1
    print(f"DONE cleaned={n_clean} quarantined={n_quar}")


if __name__ == "__main__":
    main()
