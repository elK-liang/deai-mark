# BENCHMARK 示例（held-out AI 侧真实命中 → 规则改写）

## Case: 规则 1.2 ing_clause（源: PMC5998602）

**Before (AI 生成原文摘录):**
> Our findings identify a HULC/miR15a/PTEN regulatory network in which HULC overexpression is associated with reduced miR15a and PTEN levels, providing mechanistic insight into how HULC accelerates liver cancer through autophagy-mediated inhibition of PTEN.

**After (规则 1.2: 拆独立句):**
> Our findings identify a HULC/miR15a/PTEN regulatory network in which HULC overexpression is associated with reduced miR15a and PTEN levels. This provides mechanistic insight into how HULC accelerates liver cancer through autophagy-mediated inhibition of PTEN

---
*完整验收流程见 SKILL.md；before 均为语料库真实命中（held-out），非人工造例。*