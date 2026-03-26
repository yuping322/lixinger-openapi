---
description: 使用小盘成长策略筛选 A 股股票，先建候选池，再评估成长质量与经营韧性
argument-hint: "[股票池 / 市值范围 / 条件]"
---

Load the `small-cap-growth-identifier` skill.

默认流程：
1. 先用 `lixinger-screener` 生成小市值成长候选池。
2. 再评估收入增长、盈利能力、现金流、资产负债与股东结构等因素。
3. 如需更多财务或股东字段，再调用 `query_data` 或其他接口补数。

如果用户没有给出条件，先确认：
- 股票池范围
- 市值上限
- 增长要求
- 结果数量

Example:
`/small-cap-growth-identifier 创业板 小市值高增长`
