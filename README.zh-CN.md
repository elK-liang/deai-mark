# less-ai-tone-academic

[![License: MIT](https://img.shields.io/badge/License-MIT-58a6ff.svg)](LICENSE)
[![Validation: 3 rounds / 148 docs](https://img.shields.io/badge/validation-3%20rounds%20%C3%97%20148%20held--out-3fb950.svg)](results/VALIDATION.md)

![banner](assets/banner.svg)

中文 | [English](README.md)

基于对照语料测量的英文生物医学论文"去 AI 味"skill。
方法学参照 [lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone)，
三处改进：**逐篇配对设计**（同一篇文章人类节 vs AI 以相同事实生成的节）、
**语料可核验**（人类侧全部 CC-BY，manifest 公开 PMCID/DOI）、**R 值带 bootstrap CI**。

**✅ 已完成（2026-09-06）。规则集 [`SKILL.md`](SKILL.md)（v2）· 验证报告 [`results/VALIDATION.md`](results/VALIDATION.md) · benchmark 见 [`results/BENCHMARK.md`](results/BENCHMARK.md)。**

## 验证（66 篇 held-out 端到端 + 18.9 万词泛化性）

- **信号清除**：em-dash 30→0（100%）、句尾分词 79→1（99%）、underscore 83%、翻案腔 100%
- **信息守恒**：数字序列 59/59 文件零变化；hedge 零升级；最大词数变化 4.2%
- **反规则零误伤**：we/被动/分号/crucial/ctl 四项全部逐字保留
- **泛化性**：六条核心规则在人类 18.9 万词上的命中密度为 AI 侧的 1/3–1/10
- 验证翻出 11 类规则缺陷（封闭词表漏网、分节作用域保护伞等），v2 已全部修订，
  **v2 复测待做**（见 VALIDATION.md 第四节如实声明）
- 执行层事故 7 次全部被 diff 验证拦截，教训已固化为执行注意事项

## 结果速览

- 语料：人类侧 879 篇（89.7 万词，16 种 CC-BY 期刊，2018–2022.6）vs AI 侧 3 模型
  （MiniMax-M2.7 全三节 276 篇、M3 摘要 97 篇、GLM-agent 通道 210 篇），逐篇配对。
- 全节铁信号：**em-dash（5.1–8.6×）、句尾分词从句（2.4–6.3×）**
- 节特异信号：摘要 **we 回避 0.43×**（恢复第一人称）；引言 notably 6.5×、thereby 2.7×；
  讨论 **underscore 17×**、foster 6.8×、翻案腔 21.9×
- 反规则（人类更多，禁止改）：crucial、句首路标词、分号、hedge、被动语态、词表
  （delve/pivotal 等在 2026 模型已≈0——词表时代结束）
- 完整表：`results/`（3 节 pooled + 7 个分模型表，全部含 95% CI）

## 文件

- `SKILL.md` — 规则集（分节组织 + 反规则 + 学术豁免 + 验收清单）
- `PROTOCOL.md` — 预注册协议（阈值在测量 AI 侧前冻结）
- `features/CANDIDATES.md` — 57 项候选特征（12 项预注册对照组）
- `scripts/` — fetch_corpus.py（Europe PMC 抓取）/ generate_ai_side.py（受控生成）/
  measure_en.py（测量+CI）/ clean_ai_text.py（数据质检）/ progress.py（进度面板）
- `results/` — 终版测量全表 + SUMMARY.md + BENCHMARK.md
- `HANDOFF.md` — 完整过程记录与局限

## 定位

作者自有稿件的风格清理，供遵守期刊 AI 披露政策前提下改善表达；不用于规避学术诚信筛查。

