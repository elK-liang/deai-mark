---
name: less-ai-tone-academic
description: 按明确清单清理英文学术论文（摘要/引言/讨论）中的 AI 生成痕迹。白名单改写：只处理列出的规则；未命中文字逐字保留；统计数字、引用、hedge、方法学表述一律不动。基于 89.7 万词人类语料与三模型 AI 语的配对测量（2026-09，CI 判定）。 De-AI-tone cleanup for English biomedical manuscripts, whitelist rules only, section-specific.
---

# 去AI味（英文学术版）

清理英文期刊稿件中的 AI 生成痕迹。规则来自 879 篇人类论文（2018–2022，CC-BY，16 刊）
与 3 个模型 583 篇生成文本的逐篇配对测量，每条规则都过了 bootstrap CI 判定。
**先认体裁与节，再动手。** 本 skill 只用于作者自有稿件的语言清理，不用于规避学术诚信筛查。

## 硬性边界（最高优先级）

**白名单改写。** 只处理下面列出的规则；未命中的句子逐字保留。没有把握时，保持原文。
**结构不动。** 标题层级、段落顺序、图表位置、公式、方法学结构一律不碰。
**信息守恒。** 不新增事实、数字、引用、因果；不删除任何限定词。改写后每个实词
必须能在原句或紧邻原文指出出处。**判断强度不得改变**：may → demonstrate 是篡改。

## 学术豁免（改写理由不成立的地方，即使"读着像 AI"）

- **Methods/实验部分的被动语态**是规范，不是 AI 味（测量：讨论节被动语态人类反而多 1.5 倍）
- **hedge**（may / might / suggest / likely / appear to）是认识规范：密度测量两侧无差异
  （引言 R=1.0），不许因为"含糊"而删除或升级
- **术语、缩写、统计标记**（p < 0.05、95% CI、Fig. 3a）一律不动
- **图表指代句**（"As shown in Table 2..."）是学术惯例，不动
- 字数、期刊格式要求优先于本规则集

---

## 规则一：跨节通用（摘要/引言/讨论全部适用）

### 1.1 揭晓式 em-dash（全节最强信号：5.1–8.6 倍）

两个 em-dash 夹一个插入语，或破折号前制造停顿揭晓。实测：AI 0.74–2.14/千字，
人类 0.15–0.39。CI 下界全部过 2.0。

改法：改为逗号或括号；揭晓式改直接陈述。

> ❌ Three miRNAs—miR-145-5p, miR-155-5p, and miR-23b-3p—were significantly overexpressed.
> ✅ Three miRNAs (miR-145-5p, miR-155-5p, and miR-23b-3p) were significantly overexpressed.

> ❌ The result was clear—combination therapy outperformed monotherapy.
> ✅ The result was clear: combination therapy outperformed monotherapy.

不改：数字区间（3–5）、复合词（pre-post comparison）、期刊要求用破折号处。

### 1.2 句尾分词从句（, suggesting/providing/indicating...；6.3 倍）

逗号后接**结论标签类分词**收尾，把结论挂在前句尾巴上。实测：摘要 AI 8.2 vs 人类 1.3/百句。

**触发分词为开放式家族**（验证实测的同族词，不限于此列举）：
suggesting / indicating / providing / highlighting / demonstrating / revealing /
underscoring / emphasizing / reflecting / showcasing / confirming / reinforcing /
leading to / making / linking / motivating / raising / leaving / offering /
promoting / driving / enabling / ensuring / allowing / supporting / paving /
resulting in / yielding / signifying / amplifying / eliciting。
同类新变体出现时同样适用（判定标准：分词内容是对前句的**结论标注或意义拔高**，
而非对前句的动作描述）。同形的形容词短语（", indicative of..."）按同一判定标准处理（v2.1）。

改法（**交替使用，防止单一句式堆积**——v2 修订，验证发现拆句 2/3 会产生 "This..." 开头）：
a) 拆成独立句，主语多样化：This / These data / These findings / This observation /
   The results / 该领域的具体主语，同一篇内不连续两次用同一开头；
b) 嵌回主句：", and this suggested that..."；
c) 从句内容若只是前句同义复述（删掉后读者不损失任何信息），整段删除。

判断：从句含新信息 → 拆句保留；纯复述 → 删；介于两者 → 拆句。

---

## 规则二：摘要专用

### 2.1 恢复第一人称主语（AI 回避 we：0.43 倍）

AI 在摘要里用被动和名词化躲开 "we"。人类摘要 4.0 次 we/千字，AI 只有 1.7。

**判据（v2 修订：验证发现全转会反向超标）**：只转**分析性动作**（examined /
analyzed / investigated / identified / observed / evaluated / compared / found），
不转**程序性动作**（enrolled / treated / measured / stored / stained / performed——
这些被动是试验惯例，转了会破坏方法学表述）。同一篇 we 密度控制在人类水平
（约 4/千词以内），**密度条款优先于正例句型**：文本已含足量 we 时即使命中典型句型
也不转（v2.1 明文）。

改法：被动句若无理由隐藏施动者，改回主动："We investigated / We found / Our data show"。

> ❌ A total of 120 patients were retrospectively analyzed to evaluate...
> ✅ We retrospectively analyzed 120 patients to evaluate...

不改：真正无需施动者的表述（"The samples were stored at −80°C"）；期刊明确要求
第三人称摘要时以期刊为准。

### 2.2 空转的 future-work 收尾（3.6 倍）

**语义触发，不限字面（v2 修订：验证发现字面式命中数为零，AI 已改用变体）**。
摘要结尾出现的"无新信息的展望句"，涵盖：
"further research/studies are needed/warranted"（字面式）、
"foundation(s) for future studies/validation"、"warranting further clinical validation"、
"offer a foundation for future translational studies"、"may open new avenues"。
人类摘要 0.06/千字（几乎不写），AI 0.22。

改法：摘要空间宝贵，若只是套话，删；若点名了具体后续对象（"to validate in a
prospective cohort of X patients"），保留具体部分、删空泛框架。整句删除时不受
"不删限定词"约束（该句本身零信息量），但**删后必须检查上下文衔接**。

---

## 规则三：引言专用

### 3.1 notably / Importantly 开头（6.5 倍）

实测引言层 notably：AI 0.14 vs 人类 0.02/千字。
**作用域（v2 修订：任何节命中即处理——验证发现该标记在摘要/讨论同样高频出现）**。

改法：删掉副词直接陈述，或把强调降级为句序安排。

> ❌ Notably, EGFR mutations were detected in 45% of the cohort.
> ✅ EGFR mutations were detected in 45% of the cohort.

### 3.2 thereby + 分词（2.7 倍）

"thereby confirming/enabling/providing..." 与 1.2 同构，引言层尤其密。
**作用域同 3.1：任何节命中即处理（讨论节实测 7 处漏网）。**

改法：拆句或改 "and thus confirmed..."（嵌回句子中间）。与 1.2 共用时优先嵌回式
（验证发现拆句式会产生弱主语链）。

### 3.3 强调模板 X the importance of（3.4 倍）

"highlight/underscore/emphasize/stress/reinforce + the importance/need/significance/
value/relevance/necessity/critical role of..."（v2 修订：动词与名词表扩容——
验证实测 "highlight the biological relevance of"、"reinforce the necessity for"
等同族模板漏网）。

改法：直接说那个重要的事是什么。

> ❌ These results underscore the importance of early screening.
> ✅ These results support early screening for high-risk groups.

**作用域**：同 3.1——任何节命中即处理（v2.1 补：验证实测讨论节漏网）。
**动词身份说明**：highlight/underscore 家族动词无论出现在哪个模板里都可触发本条；
独立的 highlight 动词用法（"These data highlight the context-dependent nature of..."）
因 ctl 项保护不主动处理——同一动词在不同句式里命运不同是设计使然，不是疏漏。

---

## 规则四：讨论专用

### 4.1 underscore 作动词（17 倍，全场最大信号）

讨论节underscore：AI 0.44 vs 人类 0.026/千字，CI [10.2, 38.2]。

改法：同 3.3。这是讨论节的头号指纹。

### 4.2 宣传腔动词与 pave-the-way 家族（foster 6.8× / leverage 5.8× / pave 29×）

foster / leverage / pave the way / open (up) avenues for / unlock / offer a pathway
toward / set the stage for / opens the door to（v2.1 名词侧：avenues/pathways for
future X 作宾语时同样按本条处理；v2.2 作用域：**任何节命中即处理**——验证实测
"we leveraged..." 在引言漏网，且本条指纹 5.8× 为全语料测量值，非讨论节专属）。
不改：cross-fostering（动物饲养技术术语）。

> ❌ This finding paves the way for novel therapeutic strategies.
> ✅ This finding suggests that targeting X may improve outcomes in patients with Y.

> ❌ We leveraged the multi-omics dataset to...
> ✅ We used the multi-omics dataset to...

### 4.3 收尾路标降密（2.0 倍）

**路标家族（v2 修订：封闭三件套改为开放式——验证实测字面式仅 3/20 文件命中，
"In conclusion / Overall / Together / With these caveats / Within these considerations"
等变体占绝大多数）**：Taken together / In summary / Collectively / In conclusion /
Overall / Together / To summarize / With these caveats / Within these considerations
及同族总结性开头。

改法：全篇保留**一处**收尾路标；其余把"路标句 + 复述"压成一句真结论，
或直接删路标词保留结论句。

### 4.4 not X but Y 翻案腔（讨论节 21.9 倍）

"Our findings reveal not just X but also Y" 类。**作用域同 3.1：任何节命中即处理。**
验证实测：讨论节 7 处全清，改法为正面先行陈述。
**边界（v2.1）**：只处理"自身发现宣言式"翻案腔；领域共识背景句（"Tumors are not
merely collections of malignant cells but complex tissues"）不动——它陈述的是领域
认知，不是作者在立靶自翻。

---

## 反规则（测量证明"人类更多"或无差异——**禁止**据此改写）

| 特征 | 实测 | 结论 |
|---|---|---|
| crucial | 人类多 3.3–6.7 倍 | 学术常规词，不许删 |
| 句首 However/Moreover 路标 | 人类多 3–4 倍 | 学术规范，不按"机械"处理 |
| 分号 | 引言/讨论人类多 3 倍 | 学术标点习惯，不动 |
| play a (crucial) role | 人类多 2–4 倍 | 不许按模板清除 |
| hedge（may/might/suggest） | 两侧无差异 | 认识规范，不许删或升级 |
| 被动语态 | 讨论节人类多 1.5 倍 | 学术语态，只按 2.1 在摘要层处理 |
| in this study | 人类多 2 倍 | 不动 |
| delve/pivotal/crucial 词表 | 2026 模型≈0 | **词表已死**：不许按网上 AI 词单改词 |

**ctl 项诚实条款**：comprehensive/robust/highlight/landscape 实测 AI 高 2.3–8.9 倍
（引言最密），但因预注册为对照组、且可能伤及正当用法（robust statistics、
comprehensive review），本轮不列为规则。作者可自行酌情替换，skill 不主动处理。

---

## 验收清单（输出前逐项过）

- 每处改动对应上文明确的规则编号；指不出的撤销
- 数字、统计量、引用、图表指代、限定词：零改动
- 未命中句逐字保留；结构、段落、图表位置未动
- 摘要：we/主动语态是否在期刊格式允许内恢复；we 密度是否在人类水平（≤4/千词）
- 讨论：underscore/foster/pave the way 家族是否清零
- 没有按"网上 AI 词表"改词（delve/crucial/pivotal 不在处理范围）
- 没有删除或升级任何 hedge
- 拆句后检查：同一篇内 "This/These + 动词" 开头是否连续两次出现；是则换嵌回式或换主语
- 改写后每个实词可在原文指出出处

## 执行注意事项（v2 新增，来自 66 篇验证的执行层教训）

- **特殊字符保真**：不改写 U+2011 不换行连字符、U+202F 窄空格、弯引号、CRLF——
  整文件重写会静默破坏它们；只做局部句内编辑
- **节标签 ≠ 节功能**：段落的实际功能（讨论腔/方法腔）优先于所在节标签判断适用规则；
  引言末段实为讨论腔时按讨论规则处理
- **非规则瑕疵不顺手修**：拼写错误、中英混杂等源文本问题按逐字保留处理，
  可在输出后单独提示作者
- **diff 验证**：每处编辑后核对落点，防止拼接事故（三轮验证共 9 次编辑事故
  全部由 diff 捕获）
- **U+202F 窄空格警告**：部分编辑工具会把 U+202F 静默归一化为普通空格导致
  匹配失败或丢字符——含 U+202F 的句子用显式   转义或脚本编辑，编辑后
  复核该字符计数（第三轮验证实测）

---

规则集方法学参照 [larashero3-dotcom/lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone)（配对语料测量框架）；候选词来源 Kobak et al. 2024 (arXiv:2406.07016)、Liang et al. 2024 (arXiv:2403.07183)。测量与验证细节见仓库 results/。
