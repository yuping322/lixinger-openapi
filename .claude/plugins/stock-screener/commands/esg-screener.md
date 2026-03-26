---
description: 使用 ESG 视角筛选 A 股股票，先建候选池，再补充 ESG 评分、争议与治理代理数据
argument-hint: "[股票池 / ESG策略 / 条件]"
---

Load the `esg-screener` skill.

默认流程：
1. 先用 `lixinger-screener` 建候选池，并完成基础排除筛选。
2. 再补充 ESG 评分、争议、治理与监管代理数据。
3. 如需外部评级或争议信息，可继续调用 `query_data`、AkShare 或其他接口。

如果用户没有给出条件，先确认：
- 股票池范围
- ESG 策略（同类最优 / 排除法 / 整合法 / 主题投资）
- 聚焦支柱（E / S / G / 全部）
- 结果数量

Example:
`/esg-screener 沪深300 排除高污染 治理优先`
