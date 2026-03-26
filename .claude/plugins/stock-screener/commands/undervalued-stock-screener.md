---
description: 使用低估值策略筛选 A 股股票，先建候选池，再做低估原因与风险分析
argument-hint: "[股票池 / 行业 / 条件]"
---

Load the `undervalued-stock-screener` skill.

默认流程：
1. 先用 `lixinger-screener` 构建候选股票池。
2. 再按低估值、盈利质量、现金流和风险条件筛选。
3. 如需额外数据，再调用 `query_data` 或其他接口补数。

如果用户没有给出条件，先确认：
- 股票池范围
- 行业或板块限制
- 数量
- 侧重点（深度价值 / 成长价值 / 红利价值）

Example:
`/undervalued-stock-screener 全A 低估值高股息`
