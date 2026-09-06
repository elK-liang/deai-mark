# less-ai-tone-academic

[![License: MIT](https://img.shields.io/badge/License-MIT-a42a25.svg)](LICENSE)
[![Validation: 3 rounds / 148 docs](https://img.shields.io/badge/validation-3%20rounds%20%C3%97%20148%20held--out-3a7d44.svg)](results/VALIDATION.md)
[![Corpus: paired, verifiable](https://img.shields.io/badge/corpus-paired%20%7C%20verifiable%20DOIs-8a857c.svg)](data/manifest.csv)

![What this project does to an AI-written sentence](assets/banner.svg)

English | [中文](README.zh-CN.md)

> The internet's AI-word lists died in 2025. This is what actually separates AI-drafted from human biomedical prose, measured on a paired corpus, and what to leave alone.

A rewrite ruleset for researchers who draft manuscripts with AI and edit by hand, especially when English is a second language. Every rule survived a measurement; every claim about what "AI writing" is comes with a frequency ratio and a confidence interval, not vibes.

- [`SKILL.md`](SKILL.md) carries the rules (v2.2): section-aware whitelists, anti-rules, academic exemptions.
- [`results/VALIDATION.md`](results/VALIDATION.md) documents three validation rounds on 148 held-out documents, including every defect found and what fixed it.
- [`PROTOCOL.md`](PROTOCOL.md) froze the thresholds before the AI side was measured.
- [`data/manifest.csv`](data/manifest.csv) lists all 879 human papers with PMCID, DOI and license, so every number here can be checked independently.

## What it does to a paragraph

A real discussion paragraph from the validation corpus (AI-generated, held out). Two rules fire; everything else stays byte-for-byte.

**Before**

> The reproducibility of the wrinkle formation process across more than twenty experiments **underscores** the robustness of this phenomenon, although the number of wrinkles exhibited some biological variability**, likely reflecting minor differences** in initial bacterial distribution, local growth rates, or subtle variations in substrate properties.

**After**

> The reproducibility of the wrinkle formation process across more than twenty experiments **indicates** the robustness of this phenomenon, although the number of wrinkles exhibited some biological variability. **This likely reflects minor differences** in initial bacterial distribution, local growth rates, or subtle variations in substrate properties.

Rule 4.1 replaced the template verb "underscores"; rule 1.2 split the trailing "-ing" result clause into a sentence with a real subject. The hedges ("may", "could", "likely") survive untouched, the numbers survive untouched, and no sentence without a rule match was edited. That restraint is the product.

## How the corpus was built

The human side is 879 CC-BY papers from 16 journals, published 2018 to mid-2022, before LLM assistance was common. The AI side was generated from the same articles: each model received only the title, keywords and Results section, with no style instructions, and wrote its own abstract, introduction and discussion. Same facts, two origins, so topic confounds drop out.

Three model families contributed: MiniMax M2.7 and M3, and a GLM-5.3 agent channel. All 583 generated sections ship in this repo under `data/ai/`.

A feature became a rule only if its AI-to-human frequency ratio had a bootstrap 95% CI with lower bound at or above 2.0. Twelve control features were preregistered as never-rules to catch misclassifications; four of them flipped (AI uses them more), and the validation report says so rather than quietly promoting them.

## What the corpus shows

| Tell | AI vs human | Rule |
|---|---|---|
| Reveal-style em-dashes | 5.1 to 8.6x | 1.1 |
| Trailing result clauses (", suggesting...") | 2.4 to 6.3x | 1.2 |
| "underscore" in conclusions | 17x | 4.1 |
| "foster / pave the way / leverage" family | 5.8 to 29x | 4.2 |
| not-X-but-Y self-heralding | 21.9x in discussions | 4.4 |
| First person "we" in abstracts | 0.43x (AI avoids it) | 2.1 restores it, capped at human density |

The anti-rules matter as much. Delve, showcase, meticulous and the rest of the famous word lists occur at roughly zero in 2026 models, and human authors use "crucial" and "play a crucial role" several times more than AI does. Rewriting by internet word lists makes a manuscript more detectable, not less. So the ruleset protects hedges, passive voice in methods, semicolons, and the ordinary vocabulary of academic prose.

Section awareness is load-bearing: what marks an AI abstract (avoiding "we") is the opposite of what marks an AI introduction. The rules are organized by section for that reason.

## Validation

Three independent rounds on fresh, non-overlapping samples (66, 54 and 28 documents; the paired pool is now spent):

| Metric | Round 1 | Round 2 | Round 3 |
|---|---|---|---|
| Signal clearance, main tells | 83 to 100% | 67 to 100% | 81 to 100% |
| Residuals adjudicated as correct non-edits | all | all | all |
| Number sequences unchanged | 59/59 | 52/54 | 26/26 |
| Hedges upgraded | 0 | 0 | 0 |
| Anti-rule violations | 0 | 0 | 0 |

Each round found rule defects (11, then 10, then 6, with example sentences in the report). Each revision was re-validated on new documents in the next round. Nine editing accidents across rounds were all caught by mandatory diff checks, which is why the diff check is itself a rule.

## Install

Paste this to your agent:

```text
帮我安装这个skill：https://github.com/elK-liang/less-ai-tone-academic
```

Or install directly:

```bash
npx skills add elK-liang/less-ai-tone-academic
```

Or copy [`SKILL.md`](SKILL.md) into any tool that accepts custom instructions. Feed it a finished draft. It touches only whitelisted patterns, keeps every number, citation, hedge and figure callout byte-for-byte, and leaves unmatched sentences alone.

This tool is for authors cleaning their own drafts, consistent with journal AI-disclosure policies. It is not for evading academic-integrity screening.

## Reproduce

```bash
python scripts/fetch_corpus.py        # human side, from Europe PMC via the manifest
python scripts/generate_ai_side.py   # AI side, facts-only prompts
python scripts/measure_en.py --human data/human/introductions --ai "data/ai/*/introduction"
```

## Repository layout

```text
SKILL.md              the ruleset (v2.2)
PROTOCOL.md           preregistered thresholds and design
features/CANDIDATES.md  57 candidate operators, 12 controls
scripts/
  fetch_corpus.py     Europe PMC fetcher (human side)
  generate_ai_side.py facts-only generation harness (AI side)
  measure_en.py       57 operators, ratios, bootstrap CI
  clean_ai_text.py    corpus quality gate
data/
  ai/                 583 generated sections (shipped)
  manifest.csv        879 human papers: PMCID, DOI, license
results/
  VALIDATION.md       three rounds, defect log, final numbers
  README_BENCHMARK.md how 6 high-star repos present themselves
  *_pooled.txt        full measurement tables
validation*/          before/after pairs from all three rounds
```

## Lineage and limits

The method follows [lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone), which did this for Chinese on a 2.83M-character corpus. This repo upgrades three things it acknowledged as weaknesses: topics are paired article by article, the human corpus is public and verifiable rather than withheld, and inclusion thresholds carry confidence intervals.

Limits, stated plainly: the model panel is free-tier (no GPT, Claude or Gemini fingerprints yet); one generation channel is an agent harness rather than a bare API, and is documented as such; findings are dated, since models keep converging toward human style; and a 2018-2022 human corpus cannot fully exclude early-adopter LLM polishing. Details in PROTOCOL.md.

## Credits

This project stands on prior work, listed in the order it influenced us:

- **[larashero3-dotcom/lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone)** (MIT). The methodological foundation: the paired-corpus measurement framework, operator design and sampling QA discipline, the anti-rule concept, and the practice of publishing failure logs. Our three upgrades (pairing, public corpus, CI thresholds) are deliberate responses to its own stated limitations.
- **Excess-vocabulary studies**, which seeded the P-marked candidate words in `features/CANDIDATES.md`: Kobak et al. (2024), *Delving into ChatGPT usage in academic writing through excess vocabulary* (arXiv:2406.07016); Liang et al. (2024), *Monitoring AI-modified content at scale* (arXiv:2403.07183); and related analyses of LLM word-frequency drift in scholarly text.
- **[blader/humanizer](https://github.com/blader/humanizer)** and Wikipedia's ["Signs of AI writing"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), the checklist tradition for English; several of their patterns entered our candidate list and were measured rather than assumed.
- **Presentation design**: the README structure follows patterns distilled from six high-star repos (blader/humanizer, zenstory-ai/oh-story-claudecode, larashero3-dotcom/lieflat-charts, KKKKhazix/human-writing, larashero3-dotcom/writing-dna-skill, Nanako0129/sepia); the full analysis ships at [`results/README_BENCHMARK.md`](results/README_BENCHMARK.md).

## License

MIT. The generated corpus ships under MIT; human-side metadata (DOIs) lets anyone refetch the original CC-BY texts.
