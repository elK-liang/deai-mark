# less-ai-tone-academic

[![License: MIT](https://img.shields.io/badge/License-MIT-58a6ff.svg)](LICENSE)
[![Validation: 3 rounds / 148 docs](https://img.shields.io/badge/validation-3%20rounds%20%C3%97%20148%20held--out-3fb950.svg)](results/VALIDATION.md)
[![Corpus: 89.7k words human vs AI](https://img.shields.io/badge/corpus-paired%20%7C%20verifiable%20DOIs-d29922.svg)](data/manifest.csv)

![banner](assets/banner.svg)

**An evidence-based ruleset that removes AI writing tells from English biomedical manuscripts — built the way lieflat-less-ai-tone did it for Chinese, with three methodological upgrades.**

English | [中文](README.zh-CN.md)

- [`SKILL.md`](SKILL.md) — the ruleset (v2.2): whitelist rewrite rules, anti-rules, academic exemptions, acceptance checklist. Drop it into any agent skill slot or use as a system prompt.
- [`results/VALIDATION.md`](results/VALIDATION.md) — three validation rounds, before/after numbers, every defect found and how it was fixed.
- [`PROTOCOL.md`](PROTOCOL.md) — preregistered thresholds, frozen **before** the AI side was measured.
- [`data/manifest.csv`](data/manifest.csv) — 879 human papers with PMCID / DOI / license. Every number in this repo is independently checkable.

## Why another "humanizer"

Every popular humanizer for English (blader/humanizer and its translations) is a curated checklist. This project instead **measured** what actually separates AI-generated from human biomedical prose, then kept only the features that survived:

1. **Paired corpus.** 879 human CC-BY papers (16 journals, 2018–2022.6 — pre-LLM) vs. text generated from *the same articles' facts* (title + keywords + Results only, no style instructions, 3 model families). Same facts, two origins — topic confounds eliminated.
2. **Preregistered thresholds.** R = AI/human frequency with bootstrap 95% CI; a feature enters only if CI-low ≥ 2.0 (12 control features were preregistered as never-rules to catch misclassifications — four of them flipped, and we report that honestly).
3. **Section-aware rules.** The strongest tells are *section-specific*: what marks an AI abstract ("we"-avoidance, 0.43×) is the opposite of what marks an AI introduction. One flat rule list would be wrong three ways.

## Headline findings

| Finding | Evidence |
|---|---|
| **The famous word lists are dead.** delve / showcase / meticulous ≈ 0 in 2026 models; humans use *crucial* and *play a crucial role* 3–6× more than AI | → anti-rules: do NOT rewrite by internet word lists |
| **Structural tells dominate**: reveal-style em-dashes (5.1–8.6×), trailing "-ing" result clauses (2.4–6.3×) | → rules 1.1 / 1.2, validated 100% / 81–99% clearance |
| **Discussion-section fingerprints**: underscore (17×), foster/pave-the-way family (6.8×), not-X-but-Y self-heralding (21.9×) | → rules 4.1–4.4 |
| **Abstract**: AI avoids "we" (0.43×) — restore first person for analytic verbs only, capped at human density (~4/k words) | → rule 2.1 |
| **No single "AI style" exists**: semicolon use differs 17× between model families; em-dash concentration is model-specific | → per-model tables in `results/` |

## Validation (three independent rounds, 148 held-out documents)

| Metric | Round 1 (v1) | Round 2 (v2) | Round 3 (v2.1) |
|---|---|---|---|
| Signal clearance (em-dash / -ing / underscore / rhetoric) | 83–100% | 67–100% | 81–100% |
| Every residual manually adjudicated | ✅ correct non-edits | ✅ | ✅ |
| Number sequences unchanged | 59/59 | 52/54* | 26/26 |
| Hedges upgraded (must be zero) | 0 | 0 | 0 |
| Anti-rule violations | 0 | 0 | 0 |

\* both diffs were legitimate edits (gene-name token, deleted clause).

Each round's defects (11 + 10 + 6 found) are logged with example sentences in [`results/VALIDATION.md`](results/VALIDATION.md) — the rule revisions they triggered are marked v2 / v2.1 / v2.2 in SKILL.md.

## Use

```bash
npx skills add elK-liang/less-ai-tone-academic
```

Or copy `SKILL.md` as a system prompt in any tool. Feed it a **finished draft**; it touches only whitelisted patterns, preserves every number/citation/hedge/figure callout byte-for-byte, and leaves unmatched sentences untouched.

> **Scope & ethics**: for authors cleaning their **own** drafts, consistent with journal AI-disclosure policies. Not for evading academic-integrity screening.

## Reproduce

```bash
# human side: refetch full texts via manifest (CC-BY, Europe PMC)
python scripts/fetch_corpus.py

# AI side: controlled generation (facts-only prompts)
python scripts/generate_ai_side.py

# measure all 57 operators, R with bootstrap CI, per-journal stability
python scripts/measure_en.py --human data/human/introductions --ai "data/ai/*/introduction"
```

The AI-side corpus (583 generated sections) ships with the repo; the human side is refetchable from the manifest (CC-BY texts kept out of the repo by default — rerun the fetcher to rebuild).

## Methodology lineage

Inspired by [larashero3-dotcom/lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone) (Chinese, 2.83M characters). Upgrades here: paired-by-article design (their acknowledged limitation: unpaired topics), fully verifiable human corpus (theirs is unpublished), CI-based inclusion thresholds (theirs are point estimates), and three published validation rounds (theirs has none).

**Limitations** (also in PROTOCOL.md §6): free-tier model panel (MiniMax ×2 + GLM-agent channel — no GPT/Claude/Gemini fingerprints); one agent channel differs from bare-API conditions (documented); findings are time-stamped — models converge toward human style over time (GPT's em-dash fell from ~1/sentence to 0.11 in under a year, per lieflat's Chinese data); 2018–2022 human corpus cannot fully exclude early-adopter LLM polishing.

## License

MIT. Generated corpus included under MIT; human-side metadata (DOIs) for refetching.
