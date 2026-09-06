# PROTOCOL — 去AI味（生物医学英文论文版）对照研究

参照 larashero3-dotcom/lieflat-less-ai-tone 的方法学框架（对照语料 → 算子测量 → 规则蒸馏），
针对**英文生物医学论文写作**重建，并在三处方法学上超越原版：
配对设计、语料可核验、比值带置信区间。

## 1. 研究设计

**配对对照**。每篇入选论文同时贡献：
- **人类侧**：该文作者撰写的 abstract / introduction / discussion（2018–2022.6，LLM 时代前）
- **AI 侧**：仅向生成模型提供 title + keywords + Results 节文本（不提供人类写的目标节），
  要求其撰写同一篇文章的 abstract / introduction / discussion

同一篇文章、同一组事实、两种来源——话题完全配对，修复 lieflat 自报的"话题未严格配对"局限。
人类 Results 文本仅作为事实输入（Results 节公式化、风格负载低），不进入测量。

**受控生成条件**：提示词不含任何风格指令（无"简洁/口语/像人写"等要求），不联网，
仅给定事实。任何模型、任何温度按各自默认。

## 2. 语料

### 人类侧（主基线）
- 来源：Europe PMC 全文 XML，`OPEN_ACCESS:Y`，`SRC:MED`
- 授权：仅 `creativecommons.org/licenses/by`（含 by-sa），正则从 XML 提取，manifest 记录
- 时间窗：`FIRST_PDATE:[2018-01-01 TO 2022-06-30]`（ChatGPT 发布前 5 个月截断）
- 体裁：`research article`，排除 review；客户端再排除标题含 systematic review / meta-analysis 者
- 期刊分层（CC-BY 生物医学，17 种，每种 ≤45 篇）：J Transl Med, Mol Cancer, BMC Cancer,
  Cancers, Front Oncol, Cell Death Dis, BMC Med, Sci Rep, Nat Commun, eLife, PLOS Biol,
  Breast Cancer Res, J Exp Clin Cancer Res, Cancer Commun, Cell Death Discov, Genome Med,
  Cancer Cell Int
- 节提取（JATS）：
  - abstract：仅非结构化（无 `<title>/<label>` 子元素），80–400 词
  - introduction：`sec-type∈{intro,introduction}` 或标题 ^introduction|^background，≥120 词
  - discussion：`sec-type∈{discussion,conclusion}` 或标题 ^discussion|^conclusion，≥120 词
  - 段落提取剔除 fig/table-wrap/caption 内的 p，剔除 math/graphic 元素
- **可核验**：manifest.csv 公开每篇 PMCID/DOI/license/词数；全文可由 PMCID 免费复核

### AI 侧
- 模型清单待定（以可用 API key 为准，目标 5 家，覆盖 Claude / GPT / Gemini / DeepSeek / Kimi）
- 每模型 × 全部种子篇目 × 3 节；篇目数 ≈ 人类侧入选数（同批文章配对）
- 输出保存 `data/ai/{model}/{section}/{pmcid}.md`，manifest_ai.csv 记录模型/温度/时间/token

## 3. 特征与算子

候选清单见 `features/CANDIDATES.md`（~45 项）。来源三类：
- **P**：已发表计量研究追踪的漂移词（Gray 2023；Liang et al. 2024；Kobak et al. 2024；
  Sands et al. 2024 等；入库前逐条核验出处）
- **L**：lieflat 框架的结构类特征在英文的对应物（句首路标词、对举、破折号、段首评论）
- **N**：学术体裁新候选 + 对照项（标 ctl，用于验证分母与体裁豁免，预注册为**不可**入选规则）

算子 = 正则，定义置于 `scripts/measure_en.py` 首部，可修改可复核。
**算子质检规程（照抄 lieflat 2.6）**：任何算子的频率结果被采信前，先抽样检视 20 条命中实例；
算子覆盖范围与规则名不符即修正重测。

## 4. 判定标准（预注册，AI 侧测量前锁定）

R = AI 侧频率 ÷ 人类侧频率。频率 = 命中数 / 分母，分母按特征依附单位：
每千词（词汇/标点）、每百句（句层结构）、每百段（段落层）。

| 判定 | 条件 |
|---|---|
| 纳入规则 | R 的 bootstrap 95% CI 下界 ≥ 2.0（1000 次重抽，按文档重采样），且组间（期刊间）极差 ≤ 5 倍 |
| 条件纳入 | CI 下界 ≥ 1.5，且文档覆盖率 ≥ 25% 且组间一致 |
| 反向候选 | 人类/AI ≥ 2.0 → 写入反规则清单（"不许改"） |
| 排除 | 其余；R ∈ [0.8, 1.25] 视为无区分力 |

**多重比较诚实条款**：约 45 项检验不做事后挑拣；阈值与清单在测量 AI 侧之前冻结于本文件与
CANDIDATES.md，结果无论如何呈现均全表报告（含未通过项）。

## 5. 规则蒸馏约束（Phase 3，照抄 lieflat 第 4 节）

- 白名单原则：仅处理清单内特征，未命中句子逐字保留；标题层级/段落/图表/公式/引用/统计量不动
- 信息守恒：不新增事实，不删限定词；改写后每个实词可在原文指出出处
- **学术体裁豁免**（新增，学术版核心差异）：
  - Methods 的被动语态、Results 的数字与统计表述一律不按"翻译腔/名词化"处理
  - hedge（may/might/suggest）是认识规范，不按"含糊"处理，除非密度极端
  - 缩写、术语、图表指代（Fig. 3a）、统计标记（p < 0.05）不动
  - 期刊惯例优先：若目标期刊风格指南与规则冲突，以期刊为准
- 句长/段长均匀度、被动句、hedge 密度等"流输名词"是否成立，以测量结果为准，不预设

## 6. 局限（预注册）

- 时效性：模型迭代向人类文风收敛，所有频率为特定时点观测（写明测量日期与模型版本）
- 人类侧 2018–2022 亦有少量 early-adopter 润色文本，无法完全排除污染
- CC-BY 期刊非全域代表（CNS 正刊多数非 CC-BY），结论外推到非 OA 顶刊需谨慎
- Results 节作为生成素材会轻微收窄 AI 侧的话题发散度；配对收益大于此代价
- 正则不解析语义，算子覆盖落差是残余风险，以抽检规程缓解

## 7. 阶段与状态

- [x] Phase 0：协议 + 候选清单
- [ ] Phase 1：语料抓取（脚本 `scripts/fetch_corpus.py`）→ 人类侧 + seeds
- [ ] Phase 1b：AI 侧生成（`scripts/generate_ai_side.py`，待 API key）
- [ ] Phase 2：测量（`scripts/measure_en.py`）→ 全表 + CI
- [ ] Phase 3：SKILL.md 蒸馏（规则 + 反规则 + 验收清单 + 体裁豁免）
- [ ] Phase 4：benchmark（30–50 个 before/after）+ 复算入口

## 8. 定位声明

本工具用于**作者自有稿件**的风格清理，供遵守期刊 AI 使用披露政策的前提下改善表达；
不用于规避学术诚信筛查。
