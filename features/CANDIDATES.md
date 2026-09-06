# 候选特征清单（预注册版 v1）

约 45 项。来源标记：**P** = 已发表 LLM 学术用词漂移研究追踪的词/短语（Gray 2023;
Liang et al. 2024; Kobak et al. 2024; Sands et al. 2024；入库前逐条核验出处）；
**L** = lieflat 框架结构特征的英文对应物；**N** = 学术体裁新候选。
**ctl** = 对照项，预注册为不可入选改写规则（用于验证分母、暴露体裁差异、防止误伤学术规范）。

判定阈值见 PROTOCOL.md 第 4 节。全部项无条件全表报告。

## A. 词汇层（每千词）

| # | 特征 | 算子要点 | 来源 |
|---|---|---|---|
| 1 | delve | \bdelv(e\|es\|ed\|ing)\b | P |
| 2 | intricate | \bintricate\|intricacies\b | P |
| 3 | pivotal | \bpivotal\b | P |
| 4 | underscore | \bunderscore(s\|d\|ing)?\b | P |
| 5 | showcase | \bshowcas(e\|es\|ed\|ing)\b | P |
| 6 | tapestry | \btapestry\b | P |
| 7 | realm | \brealm\b | P |
| 8 | testament | \btestament\b | P |
| 9 | holistic | \bholistic\b | P |
| 10 | seamless | \bseamless(ly)?\b | P |
| 11 | foster | \bfoster(s\|ed\|ing)?\b | P |
| 12 | garner | \bgarner(s\|ed\|ing)?\b | P |
| 13 | leverage | \bleverag(e\|es\|ed\|ing)\b | P |
| 14 | meticulous | \bmeticulous(ly)?\b | P |
| 15 | commendable 组 | \bcommendable\|praiseworthy\|laudable\b | P |
| 16 | groundbreaking 组 | \bgroundbreaking\|cutting-edge\b | P |
| 17 | notably | \bnotably\b | P |
| 18 | crucial | \bcrucial(ly)?\b | P/ctl 双属性，按数据判 |
| 19 | comprehensive | \bcomprehensive(ly)?\b | ctl（人类学术常用） |
| 20 | robust | \brobust(ness)?\b | ctl |
| 21 | highlight(动词) | \bhighlight(s\|ed\|ing)?\b | ctl |
| 22 | landscape(抽象) | \blandscapes?\b（需人工抽检是否比喻用法） | P/ctl |
| 23 | thereby | \bthereby\b | N |
| 24 | wherein | \bwherein\b | ctl |
| 25 | overall 句首 | \b[Oo]verall,\b | N |
| 26 | regarding | \b[Rr]egarding\b | N |

## B. 短语模板（每千词）

| # | 特征 | 算子要点 | 来源 |
|---|---|---|---|
| 27 | play a X role | \bplays? a (crucial\|vital\|pivotal\|key\|significant) role\b | P |
| 28 | pave the way | \bpaves? the way\b | P |
| 29 | shed light | \bsheds? light\b | P |
| 30 | bridge the gap | \bbridg(e\|es\|ed\|ing) the gap\b | P |
| 31 | in recent years | \bin recent years\b | P |
| 32 | further research 组 | \bfurther (research\|studies) (are\|is) (needed\|warranted\|required)\|future studies\|further investigation\b | N |
| 33 | to our knowledge | \bto (the best of )?our knowledge\b | N |
| 34 | these findings suggest | \bthese findings suggest\|our findings (suggest\|indicate\|reveal)\b | N |
| 35 | in conclusion | \bin conclusion\b | N |
| 36 | not only…but also | \bnot only\b.{0,80}?\bbut also\b | L |
| 37 | worth noting 组 | \b(it is )?worth noting\|it should be noted\|it is important to note\b | P |
| 38 | X the importance of | \b(highlight\|underscore\|emphasiz\|stress)(es\|ed\|ing)? the (importance\|need\|significance)\b | P |
| 39 | vast potential | \b(vast\|enormous\|immense\|tremendous) potential\b | P |
| 40 | promising avenue | \bpromising (avenue\|approach\|strategy)\|opens? (up )?new (avenues\|possibilities)\b | P |
| 41 | in this study | \b[Ii]n this (study\|work\|paper\|investigation)\b | N |
| 42 | not X but Y | \bnot (just\|merely\|simply) [^.,;]{1,40} but\b | L |

## C. 句层结构（每百句）

| # | 特征 | 算子要点 | 来源 |
|---|---|---|---|
| 43 | 句首路标词组 | ^\s*(Moreover\|Furthermore\|Additionally\|In addition\|Notably\|Importantly\|Specifically\|Consequently\|Subsequently) | L |
| 44 | 句首 However | ^\s*However\b | ctl |
| 45 | 句首 Thus 组 | ^\s*(Thus\|Therefore\|Hence)\b | ctl |
| 46 | 逗号分词从句 | ,\s+(highlighting\|underscoring\|demonstrating\|revealing\|indicating\|suggesting\|emphasizing\|reflecting\|showcasing\|providing\|paving\|contributing\|ensuring\|allowing\|enabling\|supporting)\b | P/L |
| 47 | 副词三连 | \b\w+ly, \w+ly, and \w+ly\b | N |
| 48 | passive（粗算子） | \b(was\|were\|is\|are\|been\|being)\s+\w+(ed\|en)\b | ctl |
| 49 | hedge 密度 | \b(may\|might\|could\|suggest(s\|ed)?\|potential(ly)?\|likely\|presumably\|possibly)\b（每千词） | ctl |
| 50 | we 密度 | \bwe\b（每千词） | ctl |

## D. 段落/标点层

| # | 特征 | 分母 | 算子要点 | 来源 |
|---|---|---|---|---|
| 51 | 破折号 | 每千词 | —（em dash）与 ` -- ` | L |
| 52 | 段首 This 回指 | 每百段 | ^This | L/N |
| 53 | 段首路标词 | 每百段 | ^(However\|Moreover\|Furthermore\|Additionally\|Notably\|Overall) | L |
| 54 | 段首评论语 | 每百段 | ^(Interestingly\|Strikingly\|Notably\|Importantly\|Remarkably) | N |
| 55 | 句长变异系数 | — | 生成 vs 人类 CV（lieflat 对照项的英文版） | L |
| 56 | 分号密度 | 每千词 | \b;\s | ctl |
| 57 | collect 组收尾 | 每百句 | \b(Finally\|In summary\|Taken together\|Collectively)\b | N |

## 里程检查点

1. 每条算子在采信频率前抽检 20 条命中（lieflat 规程）
2. 人类侧先跑：ctl 项应呈期刊间一致性；否则先修分母
3. **AI 侧数据到位前冻结本清单**——新增候选只能进 v2，不回填本轮
