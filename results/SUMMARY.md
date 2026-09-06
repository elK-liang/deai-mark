# AI 侧语料生成与测量总结（2026-09-06 收尾快照）

## 1. 参与面板与完成矩阵

最终进度快照（`progress.py` 原样输出见 `results/final_counts.txt`，快照时间 13:38:43，总 365/630）：

| 模型 | abstract | introduction | discussion | 状态 |
|---|---|---|---|---|
| minimax_minimax-m2.7-free | 78/70 | 101/70 | 82/70 | 三节完成（超额为历史遗留，cap 只挡新增） |
| minimax_minimax-m3-free | 97/70 | **0/70** | **0/70** | 摘要完成；引言/讨论因模型级日限额（429 limit_rpd）+ 账号级 free-models-per-day 耗尽未完成 |
| glm-5.3-flash-zcode-agent | **0/70** | **0/70** | 7/70 | **agent 通道采集进行中**，本次仅纳入 discussion 已有 7 篇 |

- 退役模型（本轮已整体移至 `data/ai_retired/`，不参与本次测量）：nvidia_nemotron-3-super-120b-a12b-free（abstract 12）、dots-studio_dots-3-note-preview-free（abstract 10）、z-ai_glm-5.2-free（abstract 3）。
- 替补模型探测：4 个候选（google/gemma-4-26b-a4b-it:free、inclusionai/ling-3.0-flash-sante:free、google/gemma-4-31b-it:free、nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free）全部返回 429「free-models-per-day」（账号级日 50 次免费额度耗尽，Remaining=0，重置约 UTC 零点 ≈18.6 小时后），按规则判不可用，**未加入替补**。`config.json` 现为 `["minimax/minimax-m3:free", "minimax/minimax-m2.7:free"]`。
- 收尾为 coordinator 指令的提前收尾（并发槽位让给 agent 生成通道），非 90 分钟时间盒自然到期。

## 2. 每节 top-10 特征（混合侧，直接抄自 *_pooled.txt）

### abstract（human 745 篇 / ai 175 篇 = m2.7 78 + m3 97）

| # | 特征 | R | CI95 | 判定 |
|---|---|---|---|---|
| 1 | em_dash | 6.81 | [3.34,16.19] | INCLUDE (CI-low>=2) |
| 2 | ing_clause | 6.11 | [4.80,7.92] | INCLUDE (CI-low>=2) |
| 3 | further_studies | 4.45 | [2.02,11.06] | INCLUDE (CI-low>=2) |
| 4 | landscape (ctl) | 3.94 | [2.07,7.84] | (ctl) INCLUDE (CI-low>=2) |
| 5 | highlight_v (ctl) | 2.90 | [1.99,4.37] | cond (CI-low>=1.5) |
| 6 | X_importance_of | 2.74 | [1.02,7.59] | - |
| 7 | robust (ctl) | 2.26 | [1.04,4.83] | - |
| 8 | semicolon (ctl) | 1.84 | [1.34,2.57] | - |
| 9 | underscore | 7.54 | (few hits) | - |
| 10 | passive_rough (ctl) | 1.47 | [1.33,1.61] | - |

INCLUDE 共 4 项；per-journal 稳定性：further_studies OK（spread 2.8x），em_dash / ing_clause / landscape / highlight_v 均 UNSTABLE（spread 5.7–12.7x）。

### introduction（human 716 篇 / ai 101 篇 = 仅 m2.7）

| # | 特征 | R | CI95 | 判定 |
|---|---|---|---|---|
| 1 | landscape (ctl) | 8.91 | [4.64,17.01] | (ctl) INCLUDE (CI-low>=2) |
| 2 | em_dash | 8.63 | [5.68,14.00] | INCLUDE (CI-low>=2) |
| 3 | notably | 7.19 | [2.55,21.23] | INCLUDE (CI-low>=2) |
| 4 | ing_clause | 6.72 | [5.32,8.58] | INCLUDE (CI-low>=2) |
| 5 | comprehensive (ctl) | 5.87 | [3.89,8.49] | (ctl) INCLUDE (CI-low>=2) |
| 6 | robust (ctl) | 5.14 | [3.15,7.98] | (ctl) INCLUDE (CI-low>=2) |
| 7 | X_importance_of | 4.89 | [2.11,9.88] | INCLUDE (CI-low>=2) |
| 8 | highlight_v (ctl) | 3.73 | [2.45,5.40] | (ctl) INCLUDE (CI-low>=2) |
| 9 | thereby | 3.40 | [2.22,5.16] | INCLUDE (CI-low>=2) |
| 10 | underscore | 30.83 | (few hits) | - |

INCLUDE 共 9 项（含 4 个控制特征）；cond 1 项：we (ctl) 1.96 [1.69,2.26]。per-journal：ing_clause OK（4.2x）、X_importance_of OK（4.8x），landscape / em_dash / comprehensive / robust UNSTABLE，notably sparse（仅 7 组出现）。

### discussion（human 681 篇 / ai 89 篇 = m2.7 82 + agent 通道 7）

| # | 特征 | R | CI95 | 判定 |
|---|---|---|---|---|
| 1 | underscore | 26.42 | [15.72,51.80] | INCLUDE (CI-low>=2) |
| 2 | landscape (ctl) | 12.65 | [6.71,26.88] | (ctl) INCLUDE (CI-low>=2) |
| 3 | foster | 10.15 | [2.61,34.70] | INCLUDE (CI-low>=2) |
| 4 | leverage | 5.80 | [2.33,13.56] | INCLUDE (CI-low>=2) |
| 5 | em_dash | 5.30 | [3.63,7.89] | INCLUDE (CI-low>=2) |
| 6 | thereby | 4.89 | [3.42,6.86] | INCLUDE (CI-low>=2) |
| 7 | comprehensive (ctl) | 4.64 | [3.14,6.76] | (ctl) INCLUDE (CI-low>=2) |
| 8 | robust (ctl) | 3.27 | [2.23,4.66] | (ctl) INCLUDE (CI-low>=2) |
| 9 | ing_clause | 2.54 | [1.97,3.16] | cond (CI-low>=1.5) |
| 10 | highlight_v (ctl) | 2.48 | [1.78,3.36] | cond (CI-low>=1.5) |

INCLUDE 共 8 项（含 4 个控制特征）；cond 2 项。per-journal：全部 UNSTABLE 或 sparse（underscore / foster 仅 7 组出现）。

## 3. 反向（反规则）候选（AI 显著低于人类，judge=reverse -> anti-rule）

- **abstract（混合）**：we (ctl) R=0.38 [0.29,0.47]（唯一有 CI 的强反向）；few-hits 反向：findings_suggest 0.47、play_X_role 0.34、not_only_but 0.22、regarding 0.19、overallcomma 0.13、crucial 0.09，以及 AI 侧 0 命中组（intricate、showcase、holistic、meticulous、wherein、pave_the_way、shed_light、in_recent_years、our_knowledge、not_X_but_Y、si_signpost、si_however、si_thus、p_open_signpost）。
- **introduction（混合）**：semicolon (ctl) R=0.33 [0.09,0.66]（有 CI）；few-hits 反向：play_X_role 0.41、regarding 0.37、crucial 0.30、si_signpost 0.27、p_open_signpost 0.20、p_open_this 0.20，及 AI 侧 0 命中组（delve、showcase、holistic、meticulous、groundbreaking、pave_the_way、bridge_the_gap、in_recent_years、our_knowledge、findings_suggest、worth_noting、vast_potential、promising_avenue、si_however、si_thus）。
- **discussion（混合）**：we (ctl) R=0.27 [0.21,0.34]、semicolon (ctl) R=0.37 [0.25,0.53]、in_this_study R=0.46 [0.24,0.73]（三者均有 CI）；few-hits 反向：overallcomma 0.31、si_signpost 0.25、p_open_comment 0.19，及 AI 侧 0 命中组（delve、intricate、showcase、realm、meticulous、wherein、play_X_role、shed_light、in_recent_years、our_knowledge、worth_noting、vast_potential、si_however、si_thus、p_open_this、p_open_signpost）。
- 注意方向不一致项：we 在 abstract/discussion 为反向、在 introduction 为 cond 正向；passive_rough 在 abstract/introduction 略高、在 discussion 反向（0.68）。作为反规则采纳时需逐节区分。

## 4. few-hits 待足量项（R 高但双侧命中 <5，补数后可能升级）

- abstract：underscore R=7.54。
- introduction：not_X_but_Y R=∞、underscore R=30.83、garner 5.14、foster 3.85、realm 3.43、intricate 2.57。
- discussion：pave_the_way R=23.20、not_X_but_Y R=23.20、bridge_the_gap 5.80、holistic 2.90。
- 上述多数集中在 m2.7 一家（introduction 仅 m2.7 有数据），足量后需重验是否跨模型稳定。

## 5. 异常与数据质量备注（忠实记录）

1. **agent 通道（glm-5.3-flash-zcode-agent）**：采集通道为 ZCode 子代理直接撰写（带 harness 系统提示词），与 OpenRouter 裸 API 调用条件略有差异，属条件不一致的已知局限；目前采集**进行中**，本次仅 discussion 纳入 7 篇（abstract/introduction 为 0），其分模型测量（`results/discussion_glm-5.3-flash-zcode-agent.txt`）n=7、4,082 词，几乎全部特征 few-hits，仅供观察，不能下结论。其 em_dash=0（7 篇无破折号）与两个 API 模型的高 em_dash 形成鲜明对比，待足量后值得复核。
2. **m3 引言/讨论未完成**：OpenRouter 对 minimax-m3 的模型级日限额（429 `limit_rpd/minimax/minimax-m3-20260531`）+ 账号级 free-models-per-day（50/天）耗尽，重置约在 UTC 零点；断点续跑数据不丢，恢复后重跑 `scripts/generate_ai_side.py` 即可续填。
3. **m2.7 超额**：78/101/82 超出 cap 70，为早期运行遗留；生成脚本按 `>=cap` 跳过新增，未删数据。
4. **清洗**：本轮 `clean_ai_text.py` 规范化 29 个文件、新增隔离 0；历史隔离 `data/ai_quarantine/` 共 5 篇（m2.7/introduction 2 篇、m3/abstract 3 篇），未参与测量。
5. **measure_en.py bug 修复**：per-journal 稳定性段对 few-hits 特征（lo=None）做 `lo >= 1.5` 引发 TypeError，导致输出尾部截断并混入 traceback；已修复（加 `lo is not None` 判断）并全部重跑，8 个测量输出 rc=0，无 traceback。
6. **introduction 分模型与混合重合**：introduction 只有 m2.7 有数据，`introduction_minimax_minimax-m2.7-free.txt` 与 `introduction_pooled.txt` 数值完全相同（ai=101 篇）。
7. **生成提前终止**：按 coordinator 指令提前收尾（并发槽位让给 agent 通道），收尾时已验证 generate_ai_side 进程归零；progress.py 面板进程（--serve, 8768 端口）未受影响。
8. 跨模型方向核验（分模型输出）：abstract 的 ing_clause（m2.7 6.93 / m3 5.52）、em_dash（8.76 / 5.44）在两家 API 模型上方向一致，混合结论较稳；underscore 在 m3 摘要 R=10.71、m2.7 摘要仅 3.04（均 few-hits），跨模型不稳。

## 6. 产出文件

- `results/final_counts.txt` — progress.py 最终快照
- `results/abstract_pooled.txt` / `results/introduction_pooled.txt` / `results/discussion_pooled.txt` — 混合侧测量
- `results/abstract_minimax_minimax-m2.7-free.txt`、`results/introduction_minimax_minimax-m2.7-free.txt`、`results/discussion_minimax_minimax-m2.7-free.txt` — m2.7 分模型
- `results/abstract_minimax_minimax-m3-free.txt` — m3 摘要分模型
- `results/discussion_glm-5.3-flash-zcode-agent.txt` — agent 通道 discussion（n=7）
- 数据目录：`data/ai/`（活跃三目录）、`data/ai_retired/`（三个退役模型）、`data/ai_quarantine/`（隔离 5 篇）
