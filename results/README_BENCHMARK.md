# README 架构与视觉方案基准报告（6 个高星 skill 仓库）

> 调研日期：2026-09-06。方法：raw.githubusercontent.com 抓 README 全文 + api.github.com 抓根目录/assets 目录清单，全部 6 仓库抓取成功，无跳过。原始文件存于 `results/raw/`。
> 星数采用任务书给定值：humanizer 43.5k / oh-story 6.5k / lieflat-charts 4.7k / human-writing 3.5k / sepia 2.3k / writing-dna-skill 1.4k。

## 总览速查表

| 仓库 | 语言 | 行数 | 头图 | 徽章 | 表格 | GIF | 安装渠道数 | 安装位置 | 演示证明 | 语言策略 |
|---|---|---|---|---|---|---|---|---|---|---|
| blader/humanizer | EN | 209 | 无 | 1（skills.sh installs） | 5 张（45 行） | 0 | 4 | **末尾** | 35 模式 before/after 表 + 完整长例文 + Wikipedia 来源 | 单语 |
| zenstory-ai/oh-story-claudecode | CN | 415（EN 412） | 2 张 PNG 截图（工作台+封面样例） | 0 | 4 张（57 行） | 0 | 2 + 7 平台适配细节 | 前部（第 3 节） | mermaid 流程图 + demo/ 真实产出样例 + 版本 blockquote | 双语分文件 + 顶部切换 |
| larashero3-dotcom/lieflat-charts | CN | 308（EN 300） | PNG hero（可点击→moxt.ai） | 0 | 2 张 MD + 大量 HTML 表格图墙 | **11 个** | 2 | 中后部 | 图墙 + 动图 + 可交互 live 模板链接 | 双语分文件 + 顶部切换 |
| KKKKhazix/human-writing | CN | 116 | SVG 封面（100% 宽） | 3（version/MIT/release，配色统一 flat-square） | 2 张 | 0 | 1（自然语言）+fallback | **前部（第 2 节）** | 无 before/after 例文，靠方法论叙述 | 单语 |
| larashero3-dotcom/writing-dna-skill | CN | 223（EN 224） | PNG hero（中英双版，可点击→moxt.ai） | 0 | 2 张 | 0 | 1（MoxtHub）+ 自然语言 | 中部（约 55%） | 「300 AI vs 329 真实文章实测」数据声明（链接姊妹仓库） | 双语分文件 + 顶部切换 |
| Nanako0129/sepia | EN | 186 | 无（徽章带充当头部门面） | **5**（2 CI + release + license + Patreon） | 3 张 | 0 | 5（CLI×4 平台 + 项目级） | 中部（约 33%） | arXiv×13 引用 + evals/ + CI 徽章 + Star History | 三语分文件（EN/zh-CN/zh-TW） |

---

## 1. blader/humanizer（43.5k★，英文 humanizer）

**根目录**：`.claude-plugin/` `.github/` `AGENTS.md` `LICENSE` `README.md` `SKILL.md` `agents/` `scripts/`（无图片目录、无 CONTRIBUTING、无 evals）

**章节骨架**：H1 → 1 个 skills.sh 徽章 → 一句话定位 → How it works（含 Wikipedia 引文 blockquote + 事实边界声明）→ Usage（3 种调用方式 + ### Match your voice 子节）→ The 35 patterns（5 张 before/after 表，按 Content/Language/Style/Chatbot/Filler 分组）→ Full example（Lisbon 游记完整 before/after 长例）→ Sources → Version history（`<details>` 折叠，25 个版本条目，每条注明模式数）→ License → **Installation（最后一节）**

**要点**：
- 唯一没有头图的英文仓库，也是唯一把安装放在**文末**的——逻辑是"内容说服你，装不装最后再说"。
- 演示证明的范式是「**规则表内嵌 before/after 列**」：35 条模式每条都带 AI 味例句和改写句，5 张表构成页面主体。
- 完整例文（Lisport 700 词级 before/after）放在规则表之后，作为"综合演示"。
- 语气：极度克制平实，自称 "Plain Language"，零 emoji，零营销词；证据链指向 Wikipedia "Signs of AI writing" 与 WikiProject AI Cleanup。
- 社会证明仅 skills.sh 安装量徽章；无 star history、无用户引用。
- 安装 4 渠道：npx skills add / Claude plugin marketplace / Claude Desktop ZIP 上传 / 手动复制 SKILL.md。

## 2. zenstory-ai/oh-story-claudecode（6.5k★，中文网文 skill 包）

**根目录**：`CHANGELOG.md` `CONTRIBUTING.md` `README.md` `README_EN.md` `demo/` `marketplace.json` `package.json` `playwright.config.mjs` `reasonix-plugin.json` `.zcode-plugin/` `scripts/` `skills/` `tests/` 等（工程化程度最高的中文仓库）

**章节骨架**（CN 版）：顶部语言切换 → H1 → 一段定位（全流程覆盖清单）→ 核心思路（blockquote 金句「套路 = 确定性的情绪满足」+ 三步方法论）→ 流程总览（**mermaid flowchart**）→ 安装（方式一：一句话自然语言；方式二：npx；`<details>` 内 7 个平台逐一适配说明）→ Skills（13 行表格：skill 名/触发词/说明）→ Agent 体系 → 自动化 Hooks → 项目文件结构 → 知识体系（`<details>` 内 21 主题知识库表）→ 适用平台（起点/番茄/晋江/知乎盐言等 8 个平台名）→ demo 样例指引 → 贡献 → 交流（Telegram + Discussions + Issues）→ 致谢（LINUX DO 社区等 3 项）

**要点**：
- 头图是**产品截图而非 logo**：`demo/story-dashboard.png`（本地写作工作台）+ 封面样例图；无徽章。
- 唯一用 mermaid 流程图的仓库；唯一带 playwright 测试配置与 CHANGELOG 深度绑定的中文仓库。
- H1 下直接放 3 条版本 blockquote（v0.7.9/0.7.8/0.7.7），用 changelog 当"更新鲜度证明"。
- 安装以「**把这句话发给 Agent**」为主渠道，附 npx；7 平台差异全部折叠进 `<details>`。
- 社会证明走社区路线：Telegram 群、GitHub Discussions、LINUX DO 致谢、作者个人处境一句话（"能让我度过找工作的过渡期"）。
- 语气：工程师式详尽 + 网文行话（黄金三章、爽点、装逼打脸），信息密度极高，几乎无客套。

## 3. larashero3-dotcom/lieflat-charts（4.7k★，数据可视化 skill）

**根目录**：`catalog.md` `report-catalog.md` `mono-tokens.js` `color-presets.js` `templates/` `examples/` `docs/` `THIRD_PARTY_NOTICES.md` `README.en.md`

**assets 清单**（docs/assets/）：**11 个 GIF + 约 25 张 PNG**（readme-hero-zh/en、preview-*、color-*-motion.gif、reports/report-*.png、author-profile.jpg）——6 家中视觉投入最大。

**章节骨架**：H1 → 语言切换 → **hero 图（可点击，链接 moxt.ai hub）** → 定位段 + 3 种视觉风格 bullet → Preview（Lupi/Glance/Basics/Interactive 四小节，HTML `<table>` 图墙 + 动图）→ 增加了彩色模式（3 套色系各配 GIF + 图墙）→ 最新更新（报告模式 12 套模板 3×4 图墙）→ 零门槛快速使用（Moxt 优先 + 「普通问答 vs Moxt」对比表；npx + 自然语言安装；8 条示例 prompt）→ 关注躺在废墟里（作者社媒矩阵 + 头像图）→ Templates（数量统计表）→ Design（设计哲学 5 条）→ Structure（目录树）→ License（**PolyForm Noncommercial**，非商业许可）

**要点**：
- 视觉方案的天花板：PNG hero + HTML 表格拼图墙 + 11 个动图 + live HTML 模板外链，README 本身就是产品 demo。
- 徽章 0 个——用图墙的"眼见为实"替代徽章的社会证明。
- 强平台绑定：hero 图和安装首推都指向 moxt.ai，且用对比表论证"为什么在 Moxt 里更好用"。
- 作者个人品牌（"躺在废墟里"）单独成节，小红书/抖音/B站/公众号/视频号/X 全平台导流。
- 语气：编辑设计语言（发丝线、留白、账本式导轨），把方法论写成审美主张。
- License 是 6 家中唯一的非标准商业限制（PolyForm Noncommercial）。

## 4. KKKKhazix/human-writing（3.5k★，中文写作 skill）

**根目录**：`.gitignore` `CHANGELOG.md` `LICENSE` `README.md` `assets/`（仅 1 个 `readme-cover.svg`）`human-writing/`

**章节骨架**：`<p align=center>` SVG 封面 → 居中徽章行（3 个）→ 居中导航锚链接（快速安装·写作流程·仓库结构·提交问题）→ blockquote 痛点 → 场景段落 → 它做什么（材料/推进/中文 三列表 + 初稿检查说明）→ 快速安装（**"把下面这句话发给你的 Agent"** + `<details>` fallback + 用法示例）→ 1.1.0 改了什么（设计演进叙述）→ 仓库结构（`<details>` 目录树 + 文件职责表）→ 反馈 → 居中 footer 署名

**要点**：
- 最短（116 行）、最"海报化"：居中排版 + SVG 封面 + 统一暖灰配色的 flat-square 徽章（C4473A/313131/6B6258），视觉最像产品官网的中文仓库。
- 3 个徽章是「版本 + License + Release」标准三件套，配色与封面统一——唯一做徽章色彩管理的仓库。
- **没有 before/after 例文**（6 家中唯一），演示证明完全靠"讲原理讲得足够透"：1.1.0 章节把「1.0 禁字面 → 1.1 禁动作」的演进写成设计故事，是说服力核心。
- 安装极简到一句话（发给 Agent 的自然语言），主推零门槛。
- 语气最锋利口语化："读完觉得挺流畅，但说不出是谁写的""读者认的是姿势，不是字""绝不拿车轱辘话凑字数"。

## 5. larashero3-dotcom/writing-dna-skill（1.4k★，写作蒸馏 skill）

**根目录**：`CONTRIBUTING.md` `SKILL.md` `README.en.md` `agents/` `assets/`（hero 中英双版 PNG）`docs/` `examples/` `references/` `skills/` `templates/`

**章节骨架**：H1 → 语言切换 → hero 图（→moxt.ai）→ 英文名 → 宗旨（"快乐写作"）→ 它解决什么问题 → 适合什么 → 中英文产物（对话语言与产物语言分离）→ 它能分析什么 → 蒸馏的六个层次（L1-L6 表：语言/结构/选题/素材/认知/视觉）→ 语料要求（≥20 篇完整文章）→ 蒸馏流程（6 步）→ 蒸馏产物（目录树）→ 快速上手（MoxtHub 优先 + 自然语言指令）→ 使用蒸馏好的风格（5 步硬性流程 + 优先级规则）→ 写完之后：去掉 AI 味（内置 `lieflat-less-ai-tone`，**300 篇 AI 输出 vs 329 篇真实文章对比实测**）→ 为什么有效 → **重要边界（伦理声明：不冒充作者、不开源语料）** → 文件结构 → License（MIT + MoxtHub CTA）

**要点**：
- 结构范式是「问题 → 分层模型表 → 流程 → 产物 → 上手」，用 L1-L6 层次表建立方法论权威。
- 演示证明靠**数据声明**而非例文图片：300 vs 329 的对比实测数字，链接姊妹仓库 lieflat-less-ai-tone 供查证。
- 唯一写「伦理边界」章节的仓库（学术/抄袭敏感场景的先行做法）。
- 与 lieflat 同厂牌（larashero3-dotcom），共享 moxt.ai 导流与 hero 图方案，但无徽章、无 GIF。
- 语气温和有宗旨感（"快乐写作""Make 写作 Happy Again！"），规则讲得细（冲突优先级、白名单改写）。

## 6. Nanako0129/sepia（2.3k★，de-AI writing skill）

**根目录**：`CONTRIBUTING.md` `evals/` `research/` `scripts/` `tests/` `plugin.json` `README.zh-CN.md` `README.zh-TW.md` `.claude-plugin/` `.codex-plugin/` `.agents/`（唯一带 evals + research + tests 三件套的仓库）

**章节骨架**：H1 → 语言切换（EN/繁/简）→ **4 徽章行（2 个 live CI：behavioral eval、version consistency + release + license）** → blockquote 定位 → 标准与操作概述 → Why another humanizer（**arXiv 引用论证**：StoryScope 93.2% macro-F1，LAMP 编辑后检测率仅降 1.6%）→ 三层通行表 → 30 特征诊断 + 各模型指纹说明 → 专业文档域规则表（release notes/PR/postmortem/tickets/技术文章 5 行）→ 操作入口矩阵表（4 操作 × 4 平台）→ Experimental: composing with voice skills → Sentence rhythm and Chinese calibration（句长离散度是唯一共识信号；中文 HC3 语料校准）→ Install（5 小节：Skills CLI 77+ agents、Claude Code、Codex、Grok Build、Antigravity、项目级安装）→ Uninstall → Layout（目录树）→ **Star History 图** → Sources（**13 篇 arXiv/PNAS/ACL 论文**）→ Support（Patreon + 成本透明说明）→ License

**要点**：
- 唯一把「**证据链**」做成门面的仓库：2 个 live CI 徽章 + arXiv 密集引用 + research/ 目录 + evals/ 目录，学术范即卖点。
- 唯一有 Star History 图、Patreon 赞助徽章、独立 Uninstall 章节的仓库。
- 认识论诚实是其独特语气："Verified means the install completes... Whether the entries then behave as documented has not been checked"；"Vendors that publish no such guidance are recorded as consulted, not guessed"。
- 无头图无例文图，靠徽章带 + 表格矩阵撑起视觉结构。
- 操作粒度最细：write/review/refactor/recreate 四操作 × 每平台命令，install/uninstall 成对出现。

---

## 共性模式清单（频次标注）

1. **标题后紧跟一句话定位/blockquote 金句**（6/6）：humanizer "reads like a person wrote it"；human-writing "说不出是谁写的"；sepia "at the layer that actually gives AI away"；zenstory "套路=确定性的情绪满足"。一句话讲清"病→药"。
2. **用 Markdown 表格枚举能力/规则**（6/6）：所有仓库至少 1 张表，且表是"能力清单"而非装饰——模式表（humanizer）、skill 表（zenstory）、层次表（writing-dna）、操作矩阵（sepia）、风格统计（lieflat）、三列方法论（human-writing）。
3. **目录树/文件结构章节**（5/6，humanizer 除外）：说明 skill 的"黑盒里有什么"，普遍放在尾部。
4. **双语分文件 + 顶部语言切换**（4/6）：zenstory(EN)、lieflat(EN)、writing-dna(EN)、sepia(zh-CN+zh-TW)；两家单语（humanizer 纯英、human-writing 纯中）。中文主仓库标配「中文 | English」首行。
5. **License 收尾章节**（6/6）：MIT 占 5/6，lieflat 用 PolyForm Noncommercial。
6. **「把这句话发给你的 Agent」自然语言安装**（4/6）：human-writing、zenstory、lieflat、writing-dna 均主推一句话安装；npx skills add 出现在 4/6（humanizer/zenstory/lieflat/sepia）。安装位置普遍在**概念展示之后的中部**（5/6），humanizer 反向放在末尾——"安装置顶"并不成立，"安装紧跟卖点"才成立。
7. **头图**（4/6）：human-writing 用 SVG 封面、lieflat/writing-dna 用可点击 PNG hero、zenstory 用产品截图；humanizer 和 sepia 无头图（用徽章/文字开门面）。GIF 仅 lieflat 一家（11 个）。
8. **版本/变更叙事**（4/6 显式章节）：humanizer 的 `<details>` 版本史、zenstory 顶部版本 blockquote + CHANGELOG、human-writing "1.1.0 改了什么"、lieflat "最新更新"。高星仓库倾向把 changelog 当内容营销（讲设计演进而非罗列 commit）。
9. **社区/反馈渠道**（5/6）：从 Issues（human-writing）到 Telegram+Discussions（zenstory）、社媒矩阵（lieflat）、Patreon（sepia）。中文仓库偏私域社群，英文仓库偏平台原生。
10. **`<details>` 折叠长内容**（4/6）：版本史、平台适配、目录树、知识清单——控制首屏长度是共识手段。
11. **外部证据引用**（3/6）：humanizer→Wikipedia，sepia→13 篇 arXiv，writing-dna→300v329 实测声明。中文仓库（human-writing、zenstory）基本不引外部研究。
12. **页长中位数约 220 行**（116–415）：写作类偏短（116–223），工具包/平台适配类偏长（308–415）。

**中英文语气差异**：英文两家（humanizer/sepia）克制、平实、可证伪表述多（"has not been checked""must come from the source"），证据链外置（Wikipedia/arXiv/CI）；中文四家痛点口语化、金句化（"姿势不是字"）、个人品牌与平台生态强绑定（moxt.ai、起点/番茄、小红书/Telegram），方法论叙述代替文献引用。中文 README 敢于展示作者人格，英文 README 致力于隐藏作者人格——与产品主张（去 AI 味）形成有趣的互文。

## 差异化机会（我们是「学术英文去 AI 味规则集」）

1. **学术场景的 before/after 例文完全空白**：humanizer 的招牌例文是游记，sepia 的专业域只有 release notes/PR/postmortem，没有一家覆盖 Abstract / Introduction / Related Work / Discussion 这些学术部件。我们可以做「按论文部件分组的 before/after 对照表 + 一篇完整学术段落改写长例」——直接复用被验证最有效的两种演示形态（humanizer 的规则表内嵌例句 + 完整长例），换到无人占据的语料域。
2. **可复现的量化评测 + 徽章化**：sepia 走了 arXiv 引用 + CI 徽章路线但没贴自己的前后检测数字；writing-dna 给了 300v329 但无脚本无徽章。我们可以做「学术段落上 AI 检测器（GPTZero/Originality/Turnitin AI）改写前后分数对照表」+ evals/ 可复现脚本 + live CI 徽章——把 sepia 的证据门面和 writing-dna 的实测数字合成，且只在学术语料上做。同时补一句立场声明（writing-dna 的伦理边界章节先例）：目标是"写得像人"，不是帮助规避学术诚信审查。
3. **非母语作者（Chinglish × AI 味双重污染）定位**：6 家全部默认用户是"英语母语者写英文"或"中文者写中文"；「中国研究者写英文学术论文」这一双重夹击场景无人认领。中文主 README + 学术英文 EN 变体的双语结构（4/6 已验证）天然适配，且可在规则集中独有「中式学术腔（如过度 hedging、名词化堆叠）× AI 味」的交叉规则层——这是 zenstory 的中文校准（HC3）和 sepia 的 per-model 指纹都没做的组合。

---

### 附：原始数据位置

- README 原文与根目录/assets JSON：`C:\Users\13552\.zcode\workspace\default\less-ai-tone-academic\results\raw\`（文件名 = owner_repo.md / .root.json）
- 本报告：`C:\Users\13552\.zcode\workspace\default\less-ai-tone-academic\results\README_BENCHMARK.md`
