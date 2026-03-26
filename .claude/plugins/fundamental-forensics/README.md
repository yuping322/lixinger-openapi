# Plugin D · Fundamental Forensics

> 质量取证与治理风险引擎（从“风险项列表”升级为“脆弱性评分 + 触发链”）

## 1) 要解决的深问题

很多公司会出现“业绩看起来还行，但质量已经恶化”的阶段：

- 利润表仍在增长，但现金流、应收、存货已经背离；
- 治理问题（质押、股东结构、减持、ST 风险）在提前累积；
- 市场叙事很热，但基本面兑现弱，最终触发估值杀伤。

**Plugin D 的目标不是列风险点，而是给出：**

1. `fragility_score`（脆弱性评分）
2. 风险因果“触发链”（为什么会从异常走向估值压缩）
3. 未来 90 天监控与升级处置计划

---

## 2) 并入能力（Skills）

### 财务质量层

- `China-market_financial-statement-analyzer`
- `US-market_us-financial-statement-analyzer`

用于识别：利润质量、现金流质量、营运资本质量、会计估计压力。

### 治理/股东风险层

- `China-market_goodwill-risk-monitor`
- `China-market_equity-pledge-risk-monitor`
- `China-market_margin-risk-monitor`
- `China-market_shareholder-risk-check`
- `China-market_shareholder-structure-monitor`
- `China-market_st-delist-risk-scanner`
- `US-market_us-insider-sentiment-aggregator`
- `US-market_us-esg-screener`

用于识别：治理脆弱性、融资链条脆弱性、监管与退市脆弱性。

### 叙事偏差层

- `China-market_tech-hype-vs-fundamentals` / `US-market_us-tech-hype-vs-fundamentals`
- `China-market_sentiment-reality-gap` / `US-market_us-sentiment-reality-gap`

用于识别：情绪-基本面错位是否正在放大。

---

## 3) 引擎核心：三层取证模型

## Layer A：单点异常（Point Abnormality）

每个信号产出 `point_score(0~100)`：

- 绝对阈值异常（例如应收占比、质押比例、商誉占净资产）
- 同业分位异常（行业分位 > 80/90）
- 历史偏离异常（z-score）
- 恶化速度异常（斜率/二阶变化）

## Layer B：异常组合（Combination Abnormality）

不单看“有没有异常”，而看“异常是否组合共振”：

- `应收恶化 + OCF/NI 下行 + 存货上升`
- `质押上升 + 两融拥挤 + 大股东减持`
- `商誉偏高 + 减值加速 + ROIC 下滑`
- `叙事热度上升 + 盈利兑现走弱 + insider 偏负面`

定义：

`combo_score = Σ(w_i * point_score_i) + synergy_bonus - hedge_offset`

其中：

- `synergy_bonus`：同向恶化、同步发生、历史上高共振组合。
- `hedge_offset`：现金修复、治理修复、经营拐点等对冲证据。

## Layer C：触发链（Trigger Chain）

将证据连接为因果链：

`异常证据(EVIDENCE) -> 风险状态(RISK_STATE) -> 估值/融资冲击(IMPACT)`

示例：

`应收与收入背离` + `OCF/NI 持续走弱`
→ `盈利质量存疑`
→ `盈利预测下修`
→ `估值中枢下移`

---

## 4) Fragility Score 设计

## 4.1 六维评分

- `FQ` 财务质量脆弱性（30%）
- `GV` 治理脆弱性（25%）
- `BS` 资产负债表脆弱性（15%）
- `TR` 交易结构脆弱性（10%）
- `NG` 叙事-现实偏离（10%）
- `EX` 外部制度约束（10%）

总分：

`fragility_score = weighted_sum + chain_amplifier - mitigant_credit + uncertainty_penalty`

## 4.2 分档解释

- `0-24` 低脆弱（Low）
- `25-49` 中性（Moderate）
- `50-69` 提升（Elevated）
- `70-84` 高风险（High）
- `85-100` 临界（Critical）

## 4.3 动态指标

- `delta_30d`：近 30 日变化
- `delta_90d`：近 90 日变化
- `fragility_trend`：`improving / deteriorating / unstable`
- `shock_sensitivity`：对负面事件的脆弱放大系数

---

## 5) 必交付输出

## A. `forensics/red_flag_graph.json`

定位“为什么危险”：

- 节点：异常证据、风险状态、影响结果
- 边：supports / amplifies / invalidates
- 每条边附置信度和时间戳

## B. `forensics/fragility_scorecard.json`

定位“有多危险”：

- 总分 + 分项分
- top drivers（前三驱动）
- mitigants（对冲项）
- invalidators（反证条件）

## C. `forensics/90d_monitor_plan.json`

定位“接下来怎么盯”：

- 指标、频率、触发阈值
- yellow / orange / red 升级规则
- 对应动作（更新估值折价、触发治理专报、纳入组合限额）

---

## 6) 执行流程（生产化）

1. 聚合多技能结构化结果（季度 + 月度 + 事件驱动）。
2. 统一尺度（行业分位、历史偏离、市场映射）。
3. 计算单点异常与组合异常。
4. 生成触发链图并计算链路置信度。
5. 计算 fragility_score 与风险分档。
6. 生成 90 天监控计划。
7. 回写 risk-monitor / valuation / deep-research。

---

## 7) 关键治理原则

- **可追溯**：每个结论必须能回到源数据与规则版本。
- **可解释**：高风险必须给出驱动项和反证项。
- **可降级**：数据缺失时保守上调不确定性惩罚，并标注低置信度。
- **可迭代**：保留命中/漏报/误报案例，持续调阈值与权重。

---

## 8) 最小可行版本（MVP）

MVP 先解决你提出的核心场景：

- “业绩表面稳定，但质量在恶化”
- “治理/财务信号提前预警估值杀伤”

MVP 成果标准：

1. 能稳定输出三份 JSON。
2. 组合异常命中率显著高于单点异常。
3. 对高 fragility 标的可给出可执行的 90 天监控动作。
