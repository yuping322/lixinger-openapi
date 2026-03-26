---
description: 使用高股息策略筛选 A 股股票，先建候选池，再评估分红可持续性与总回报
argument-hint: "[股票池 / 指数 / 条件]"
---

Load the `high-dividend-strategy` skill.

默认流程：
1. 先用 `lixinger-screener` 生成高股息候选池。
2. 再评估股息率、分红增长、自由现金流覆盖与资产负债率。
3. 如需更多历史分红或财务字段，再调用 `query_data` 或其他接口补数。

如果用户没有给出条件，先确认：
- 股票池范围
- 回溯期
- 结果数量
- 排名优先级

Example:
`/high-dividend-strategy 中证红利 高股息可持续`
