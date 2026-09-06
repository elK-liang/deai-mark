#!/usr/bin/env python3
"""Measure candidate AI-tone features in English academic text.

R = AI frequency / human frequency (R>1 = AI uses the feature more).
Frequency denominators: per-1000-words (w), per-100-sentences (s), per-100-paragraphs (p).
95% CI via bootstrap resampling over documents (1000 iterations).
Human groups (by journal, parsed from manifest.csv) give a stability check.

Usage:
  python -X utf8 scripts/measure_en.py --human data/human/abstracts --ai data/ai/gpt-5.6/abstract
  python -X utf8 scripts/measure_en.py --human data/human/introductions          # human-side only
Filenames must be <pmcid>.md on both sides for pairing metadata; group labels come
from data/manifest.csv (journal column).
"""
import re
import sys
import random
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# OPERATORS — each rule: name -> (regex, denominator unit, group, prereg role)
# role: "rule" = rule candidate | "ctl" = control, never becomes a rewrite rule
# Denominator: w = per-1000-words, s = per-100-sentences, p = per-100-paragraphs
# ---------------------------------------------------------------------------
SI = r"(?:^|\n)\s*"
RULES = {
    # A. lexical (per 1000 words)
    "delve":            (r"\bdelv(?:e|es|ed|ing)\b", "w", "rule"),
    "intricate":        (r"\bintricat(?:e|es)\b|\bintricacies\b", "w", "rule"),
    "pivotal":          (r"\bpivotal\b", "w", "rule"),
    "underscore":       (r"\bunderscore(?:s|d|ing)?\b", "w", "rule"),
    "showcase":         (r"\bshowcas(?:e|es|ed|ing)\b", "w", "rule"),
    "tapestry":         (r"\btapestr(?:y|ies)\b", "w", "rule"),
    "realm":            (r"\brealm\b", "w", "rule"),
    "testament":        (r"\btestament\b", "w", "rule"),
    "holistic":         (r"\bholistic\b", "w", "rule"),
    "seamless":         (r"\bseamless(?:ly)?\b", "w", "rule"),
    "foster":           (r"\bfoster(?:s|ed|ing)?\b", "w", "rule"),
    "garner":           (r"\bgarner(?:s|ed|ing)?\b", "w", "rule"),
    "leverage":         (r"\bleverag(?:e|es|ed|ing)\b", "w", "rule"),
    "meticulous":       (r"\bmeticulous(?:ly)?\b", "w", "rule"),
    "commendable_grp":  (r"\bcommendable\b|\bpraiseworthy\b|\blaudable\b", "w", "rule"),
    "groundbreaking":   (r"\bgroundbreaking\b|\bcutting-edge\b", "w", "rule"),
    "notably":          (r"\bnotably\b", "w", "rule"),
    "crucial":          (r"\bcrucial(?:ly)?\b", "w", "rule"),
    "comprehensive":    (r"\bcomprehensive(?:ly)?\b", "w", "ctl"),
    "robust":           (r"\brobust(?:ness)?\b", "w", "ctl"),
    "highlight_v":      (r"\bhighlight(?:s|ed|ing)?\b", "w", "ctl"),
    "landscape":        (r"\blandscapes?\b", "w", "ctl"),
    "thereby":          (r"\bthereby\b", "w", "rule"),
    "wherein":          (r"\bwherein\b", "w", "ctl"),
    "overallcomma":     (r"\b[Oo]verall,", "w", "rule"),
    "regarding":        (r"\b[Rr]egarding\b", "w", "rule"),
    # B. phrase templates (per 1000 words)
    "play_X_role":      (r"\bplays? a (?:crucial|vital|pivotal|key|significant) role\b", "w", "rule"),
    "pave_the_way":     (r"\bpaves? the way\b", "w", "rule"),
    "shed_light":       (r"\bsheds? light\b", "w", "rule"),
    "bridge_the_gap":   (r"\bbridg(?:e|es|ed|ing) the gap\b", "w", "rule"),
    "in_recent_years":  (r"\bin recent years\b", "w", "rule"),
    "further_studies":  (r"\bfurther (?:research|studies) (?:are|is) (?:needed|warranted|required)\b|\bfuture studies\b|\bfurther investigation\b", "w", "rule"),
    "our_knowledge":    (r"\bto (?:the best of )?our knowledge\b", "w", "rule"),
    "findings_suggest": (r"\bthese findings suggest\b|\bour findings (?:suggest|indicate|reveal)\b", "w", "rule"),
    "in_conclusion":    (r"\bin conclusion\b", "w", "rule"),
    "not_only_but":     (r"\bnot only\b.{0,80}?\bbut also\b", "w", "rule"),
    "worth_noting":     (r"\bworth noting\b|\bit should be noted\b|\bit is important to note\b", "w", "rule"),
    "X_importance_of":  (r"\b(?:highlight|underscore|emphasiz\w*|stress)(?:es|ed|ing)? the (?:importance|need|significance)\b", "w", "rule"),
    "vast_potential":   (r"\b(?:vast|enormous|immense|tremendous) potential\b", "w", "rule"),
    "promising_avenue": (r"\bpromising (?:avenue|approach|strategy)\b|\bopens? (?:up )?new (?:avenues|possibilities)\b", "w", "rule"),
    "in_this_study":    (r"\b[Ii]n this (?:study|work|paper|investigation)\b", "w", "rule"),
    "not_X_but_Y":      (r"\bnot (?:just|merely|simply) [^.,;]{1,40} but\b", "w", "rule"),
    # C. sentence-level (per 100 sentences)
    "si_signpost":      (SI + r"(?:Moreover|Furthermore|Additionally|In addition|Notably|Importantly|Specifically|Consequently|Subsequently)\b", "s", "rule"),
    "si_however":       (SI + r"However\b", "s", "ctl"),
    "si_thus":          (SI + r"(?:Thus|Therefore|Hence)\b", "s", "ctl"),
    "ing_clause":       (r",\s+(?:highlighting|underscoring|demonstrating|revealing|indicating|suggesting|emphasizing|reflecting|showcasing|providing|paving|contributing|ensuring|allowing|enabling|supporting)\b", "s", "rule"),
    "adverb_triad":     (r"\b\w+ly, \w+ly, and \w+ly\b", "s", "rule"),
    "passive_rough":    (r"\b(?:was|were|is|are|been|being)\s+\w+(?:ed|en)\b", "s", "ctl"),
    "collect_end":      (r"\b(?:Finally|In summary|Taken together|Collectively)\b", "s", "rule"),
    # controls per 1000 words
    "hedge":            (r"\b(?:may|might|could|suggests?|suggested|potential(?:ly)?|likely|presumably|possibly)\b", "w", "ctl"),
    "we":               (r"\bwe\b", "w", "ctl"),
    "semicolon":        (r";\s", "w", "ctl"),
    "em_dash":          (r"—|\s--\s", "w", "rule"),
    # D. paragraph-level (per 100 paragraphs)
    "p_open_this":      (r"^This\b", "p", "ctl"),
    "p_open_signpost":  (r"^(?:However|Moreover|Furthermore|Additionally|Notably|Overall)\b", "p", "rule"),
    "p_open_comment":   (r"^(?:Interestingly|Strikingly|Notably|Importantly|Remarkably)\b", "p", "rule"),
}

WORD = re.compile(r"[A-Za-z][A-Za-z'\u2019-]*")
ABBR = r"(?:[A-Z]\.|e\.g|i\.e|et al|cf|vs|Fig|Figs|Eq|Ref|Refs|p\b|No|Dr|Prof|St|approx)"


def split_sentences(text):
    text = re.sub(r"\s+", " ", text)
    parts = re.split(r"(?<=[.!?])\s+(?=[\"'(\[]?[A-Z0-9])", text)
    out = []
    for s in parts:
        # merge fragments cut after an abbreviation (Fig. 3a / et al. / p < ...)
        if out and re.search(ABBR + r"\.$", out[-1]):
            out[-1] = out[-1] + " " + s
            continue
        if s.strip():
            out.append(s.strip())
    return out


def paragraphs(text):
    return [p for p in re.split(r"\n\s*\n", text) if len(p.split()) >= 8]


def measure_doc(text, compiled):
    w = max(len(WORD.findall(text)), 1)
    sents = split_sentences(text)
    paras = paragraphs(text)
    row = {"w": w, "s": len(sents), "p": len(paras), "n": {}}
    for name, (rx, unit, _) in compiled.items():
        row["n"][name] = len(rx.findall(text))
    return row


def freq(rows, name):
    den = {"w": 1000.0, "s": 100.0, "p": 100.0}
    tot_n = sum(r["n"][name] for r in rows)
    tot_d = sum(r[UNIT[name]] for r in rows) / den[UNIT[name]]
    return tot_n / tot_d if tot_d else 0.0, tot_n, tot_d


UNIT = {name: spec[1] for name, spec in RULES.items()}
COMPILED = {name: (re.compile(spec[0], re.M), spec[1], spec[2]) for name, spec in RULES.items()}
ROLE = {name: spec[2] for name, spec in RULES.items()}


def load_dir(d):
    files = sorted(Path(d).glob("*.md"))
    rows, ids = [], []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rows.append(measure_doc(text, COMPILED))
        ids.append(f.stem)
    return rows, ids


def bootstrap_ci(rows_a, rows_h, name, iters=1000, seed=7):
    """Ratio CI by resampling documents on both sides (paired design ignored here)."""
    rng = random.Random(seed)
    na, nh = len(rows_a), len(rows_h)
    den = {"w": 1000.0, "s": 100.0, "p": 100.0}[UNIT[name]]
    ratios = []
    for _ in range(iters):
        sa = [rows_a[rng.randrange(na)] for _ in range(na)]
        sh = [rows_h[rng.randrange(nh)] for _ in range(nh)]
        fa = sum(r["n"][name] for r in sa) / max(sum(r[UNIT[name]] for r in sa) / den, 1e-9)
        fh = sum(r["n"][name] for r in sh) / max(sum(r[UNIT[name]] for r in sh) / den, 1e-9)
        ratios.append(fa / max(fh, 1e-9))
    ratios.sort()
    return ratios[int(0.025 * iters)], ratios[int(0.975 * iters)]


def journal_groups(ids):
    """pmcid -> journal, from manifest.csv"""
    m = {}
    mf = ROOT / "data" / "manifest.csv"
    if mf.exists():
        for row in csv.DictReader(open(mf, encoding="utf-8-sig")):
            m[row["pmcid"]] = row["journal"]
    return m


def main():
    argv = sys.argv[1:]
    human, ai, cur = [], [], None
    for a in argv:
        if a == "--human":
            cur = human
        elif a == "--ai":
            cur = ai
        elif cur is not None:
            cur.append(a)
    if not human:
        print(__doc__)
        return
    h_rows, h_ids = [], []
    for d in human:
        r, i = load_dir(d)
        h_rows += r
        h_ids += i
    jmap = journal_groups(h_ids)

    hw = sum(r["w"] for r in h_rows)
    print(f"human: {len(h_rows)} docs, {hw:,} words\n")
    if not ai:
        print(f"{'feature':<18}{'unit':<5}{'role':<5}{'freq':>9}  docs")
        for name in RULES:
            f, n, d = freq(h_rows, name)
            nd = sum(1 for r in h_rows if r["n"][name])
            print(f"{name:<18}{UNIT[name]:<5}{ROLE[name]:<5}{f:>9.3f}  {nd}")
        return

    a_rows, a_ids = [], []
    for d in ai:
        r, i = load_dir(d)
        a_rows += r
        a_ids += i
    aw = sum(r["w"] for r in a_rows)
    print(f"ai:    {len(a_rows)} docs, {aw:,} words\n")
    head = f"{'feature':<18}{'role':<5}{'human':>8}{'ai':>8}{'R':>7}{'CI95':>16}  judge"
    print(head)
    print("-" * len(head))
    out = []
    for name in RULES:
        fh, nh, _ = freq(h_rows, name)
        fa, na, _ = freq(a_rows, name)
        if fh < 1e-6 and fa < 1e-6:
            continue
        r = fa / fh if fh > 1e-9 else float("inf")
        if nh >= 5 and na >= 5:
            lo, hi = bootstrap_ci(a_rows, h_rows, name)
            ci = f"  [{lo:>5.2f},{hi:>5.2f}]"
            if lo >= 2.0:
                judge = "INCLUDE (CI-low>=2)"
            elif lo >= 1.5:
                judge = "cond (CI-low>=1.5)"
            else:
                judge = None
        else:
            lo = hi = None
            ci = "   (few hits)"
            judge = None
        if judge is None:
            judge = ("reverse -> anti-rule" if fh / max(fa, 1e-9) >= 2.0
                     else ("no signal" if 0.8 <= r <= 1.25 else "-"))
        if ROLE[name] == "ctl" and "INCLUDE" in judge:
            judge = "(ctl) " + judge
        out.append((r, name, fh, fa, lo, hi, judge))
    for r, name, fh, fa, lo, hi, judge in sorted(out, key=lambda t: t[0], reverse=True):
        cistr = f"  [{lo:>5.2f},{hi:>5.2f}]" if lo is not None else "      (few hits)"
        rstr = "    ∞" if r == float("inf") else f"{r:>7.2f}"
        print(f"{name:<18}{ROLE[name]:<5}{fh:>8.3f}{fa:>8.3f}{rstr}{cistr}  {judge}")

    # per-journal stability for any feature whose CI suggests inclusion
    print("\n-- per-journal spread (human side) for top candidates --")
    groups = {}
    for row, pid in zip(h_rows, h_ids):
        groups.setdefault(jmap.get(pid, "?"), []).append(row)
    for r, name, fh, fa, lo, hi, judge in sorted(out, reverse=True)[:12]:
        if not ((lo is not None and lo >= 1.5) or fh / max(fa, 1e-9) >= 2.0):
            continue
        vals = []
        for g, rows in groups.items():
            f, _, _ = freq(rows, name)
            vals.append(f)
        nz = [v for v in vals if v > 0]
        if len(nz) < max(3, len(vals) // 2):
            print(f"{name:<18} groups={len(vals)}  sparse（仅 {len(nz)} 组出现，离散度不定义）")
            continue
        spread = max(nz) / min(nz)
        print(f"{name:<18} groups={len(vals)}  spread={spread:>6.1f}x "
              f"{'OK' if spread <= 5 else 'UNSTABLE'}")


if __name__ == "__main__":
    main()
