---
description: 使用北交所策略筛选标的，先建候选池，再评估流动性、成长性与行业景气
argument-hint: "[股票池 / 条件]"
---

Load the `bse-selection-analyzer` skill.

默认流程：
1. 先用 `lixinger-screener` 生成北交所候选池。
2. 再评估估值、成长、流动性、波动与专精特新特征。
3. 如需指数成分、历史行情或补充公司信息，再调用 `query_data` 或其他接口补数。

如果用户没有给出条件，先确认：
- 是否限定北证50或全北交所
- 流动性门槛
- 结果数量
- 是否强调专精特新属性

Example:
`/bse-selection-analyzer 北交所 流动性较好 成长优先`
