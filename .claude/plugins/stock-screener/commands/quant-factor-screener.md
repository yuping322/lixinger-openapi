---
description: 使用多因子策略筛选 A 股股票，先建候选池，再计算价值/质量/成长/动量等因子
argument-hint: "[股票池 / 风格 / 条件]"
---

Load the `quant-factor-screener` skill.

默认流程：
1. 先用 `lixinger-screener` 缩小候选池与基础过滤范围。
2. 再对入围名单计算价值、质量、成长、规模、动量、低波动等因子。
3. 如需行情、行业或宏观数据，再调用 `query_data` 或其他接口补数。

如果用户没有给出条件，先确认：
- 股票池范围
- 因子偏好
- 行业中性要求
- 结果数量

Example:
`/quant-factor-screener 全A 价值质量成长综合`
