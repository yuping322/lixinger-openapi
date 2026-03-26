# Plugin D：Fundamental Forensics（质量取证与治理风险引擎）技术设计文档

## 1. 文档目标

将 `Plugin D: Fundamental Forensics` 从“风险清单”升级为“脆弱性评分 + 触发链推断”的工程化方案，用于回答：

1. 公司业绩是否呈现“表面增长、质量恶化”的早期迹象。
2. 治理与财务信号是否已经形成会触发估值压缩（multiple de-rating）的风险链。
3. 如何把多技能输出统一为可审计、可追踪、可监控的取证产物。

---

## 2. 问题定义与设计边界

### 2.1 核心问题

> 对任一标的，在时点 T 给出可解释的 `fragility_score`（脆弱性评分），并输出从“异常信号 → 风险放大 → 估值杀伤”的触发链。

### 2.2 非目标（本阶段不做）

- 不做自动交易执行或自动调仓。
- 不做纯文本情绪舆情的大规模 NLP 建模（仅消费上游技能结构化结论）。
- 不替代会计审计结论，仅提供投资取证视角的风险预警。

---

## 3. 能力并入与角色分工

本插件作为“编排层 + 评分层 + 因果图层”，消费以下技能产物：

### 3.1 财务质量与基本面

- `China-market_financial-statement-analyzer` / `US-market_us-financial-statement-analyzer`
  - 提供营收、利润、现金流、应收/存货/费用率等质量因子。
- `China-market_tech-hype-vs-fundamentals` / `US-market_us-tech-hype-vs-fundamentals`
  - 提供“叙事热度 vs 基本面兑现”的背离程度。
- `China-market_sentiment-reality-gap` / `US-market_us-sentiment-reality-gap`
  - 提供市场情绪与盈利现实的偏差监控。

### 3.2 治理与股东风险

- `China-market_goodwill-risk-monitor`
- `China-market_equity-pledge-risk-monitor`
- `China-market_margin-risk-monitor`
- `China-market_shareholder-risk-check` / `China-market_shareholder-structure-monitor`
- `China-market_st-delist-risk-scanner`
- `US-market_us-insider-sentiment-aggregator`
- `US-market_us-esg-screener`

这些技能输出统一映射为三类证据：

1. `quality_deterioration_evidence`（质量退化证据）
2. `governance_stress_evidence`（治理压力证据）
3. `valuation_killchain_evidence`（估值杀伤链证据）

---

## 4. 总体架构

```text
[Skill Outputs / Raw Signals]
  ├─ Financial statement quality signals
  ├─ Governance / pledge / shareholder / ST risks
  ├─ Insider & ESG signals
  └─ Hype-vs-fundamentals / sentiment-reality gaps
        ↓
[Normalization & Evidence Layer]
  ├─ time alignment (quarterly + monthly + event-driven)
  ├─ cross-market metric harmonization (CN/HK/US schema)
  ├─ winsorize / z-score / percentile mapping
  └─ evidence confidence scoring
        ↓
[Forensics Engine]
  ├─ anomaly detector (single-point)
  ├─ combination detector (multi-signal co-movement)
  ├─ trigger-chain builder (causal DAG)
  └─ fragility score aggregator
        ↓
[Outputs]
  ├─ forensics/red_flag_graph.json
  ├─ forensics/fragility_scorecard.json
  └─ forensics/90d_monitor_plan.json
        ↓
[Consumers]
  ├─ risk-monitor plugin
  ├─ deep-research plugin
  ├─ valuation plugin
  └─ post-selection clearance workflow
```

---

## 5. 核心设计：从单点异常到“异常组合 + 触发链”

### 5.1 单点异常（Point Anomaly）

对每个风险因子计算异常强度：

- 绝对阈值（如：应收占比、商誉占净资产比、质押比例）
- 同业分位（行业内 percentile）
- 历史偏离（rolling z-score）
- 趋势加速度（二阶变化）

输出 `point_anomaly_score ∈ [0,100]`。

### 5.2 异常组合（Combination Pattern）

重点识别“组合触发器”，例如：

- `应收恶化 + 经营现金流背离 + 毛利率下行`
- `股权质押上升 + 融资盘拥挤 + 大股东减持`
- `商誉高位 + 资产减值计提加速 + ROIC 下滑`
- `高热度叙事 + 盈利兑现不足 + insider 偏负面`

组合风险使用加权协同项：

`combo_risk = Σ(w_i * anomaly_i) + λ * interaction_strength`

其中 `interaction_strength` 由近 4~8 个观测窗口的共振频率与同步方向给出。

### 5.3 触发链（Trigger Chain / Causal DAG）

将证据映射为有向图：

- 节点类型：
  - `EVIDENCE`（证据）
  - `RISK_STATE`（中间风险态）
  - `IMPACT`（结果，如估值压缩、融资能力恶化）
- 边含义：
  - `supports`（支持）
  - `amplifies`（放大）
  - `invalidates`（削弱）

触发链示例：

`应收周转恶化` → `盈利质量怀疑` → `分析师下修` → `估值中枢下移`

---

## 6. Fragility Score 评分体系

## 6.1 一级维度（建议默认权重）

- `FQ` 财务质量退化（30%）
- `GV` 治理与股东脆弱性（25%）
- `BL` 资产负债表压力（15%）
- `MF` 市场结构与交易脆弱性（10%）
- `NR` 叙事-现实背离（10%）
- `EX` 外部约束（监管/ESG/退市制度）（10%）

总分：

`fragility_score = Σ(weight_k * subscore_k) - mitigants + data_conf_penalty`

其中：

- `mitigants`：现金储备充足、自由现金流改善、治理动作修复等。
- `data_conf_penalty`：关键数据缺失或置信度不足时上调保守惩罚。

### 6.2 评分分档

- `0-24`：稳健（Low Fragility）
- `25-49`：可控（Moderate）
- `50-69`：脆弱（Elevated）
- `70-84`：高脆弱（High）
- `85-100`：临界（Critical）

### 6.3 动态行为指标

除静态分数外，额外输出：

- `delta_30d`：30 日变化
- `acceleration_90d`：90 日加速度
- `regime_flag`：`improving | deteriorating | unstable`

---

## 7. 输出契约（JSON）

## 7.1 `forensics/red_flag_graph.json`

```json
{
  "as_of_date": "2026-03-26",
  "symbol": "600XXX.SH",
  "market": "CN",
  "nodes": [
    {"id": "n1", "type": "EVIDENCE", "label": "应收账款占比上升", "score": 78},
    {"id": "n2", "type": "EVIDENCE", "label": "经营现金流/净利润背离", "score": 82},
    {"id": "n3", "type": "RISK_STATE", "label": "盈利质量恶化", "score": 80},
    {"id": "n4", "type": "IMPACT", "label": "估值压缩风险", "score": 74}
  ],
  "edges": [
    {"from": "n1", "to": "n3", "relation": "supports", "weight": 0.71},
    {"from": "n2", "to": "n3", "relation": "supports", "weight": 0.79},
    {"from": "n3", "to": "n4", "relation": "amplifies", "weight": 0.66}
  ],
  "chain_confidence": 0.77,
  "invalidators": [
    "未来两个季度经营现金流显著修复",
    "应收周转天数回落至行业中位数以下"
  ]
}
```

## 7.2 `forensics/fragility_scorecard.json`

```json
{
  "as_of_date": "2026-03-26",
  "symbol": "600XXX.SH",
  "market": "CN",
  "fragility_score": 72,
  "band": "High",
  "subscores": {
    "FQ": 78,
    "GV": 69,
    "BL": 63,
    "MF": 55,
    "NR": 74,
    "EX": 58
  },
  "delta_30d": 11,
  "acceleration_90d": 6,
  "top_drivers": [
    "应收与现金流背离",
    "股权质押比例上升",
    "叙事热度与盈利兑现落差扩大"
  ],
  "confidence": 0.81
}
```

## 7.3 `forensics/90d_monitor_plan.json`

```json
{
  "as_of_date": "2026-03-26",
  "symbol": "600XXX.SH",
  "monitor_horizon_days": 90,
  "watch_items": [
    {
      "name": "应收周转天数",
      "frequency": "monthly",
      "trigger": "连续两期恶化且行业分位>80%",
      "action": "上调FQ维度权重并触发二级预警"
    },
    {
      "name": "经营现金流/净利润比",
      "frequency": "quarterly",
      "trigger": "<0.8 且同比下滑",
      "action": "提升触发链置信度并重算估值折价情景"
    },
    {
      "name": "股权质押比例",
      "frequency": "event-driven",
      "trigger": "新增质押导致比例上升>3pct",
      "action": "触发治理风险专报"
    }
  ],
  "escalation_rules": {
    "yellow": "fragility_score >= 60",
    "orange": "fragility_score >= 70 or delta_30d >= 10",
    "red": "fragility_score >= 85 or ST/delist risk triggered"
  }
}
```

---

## 8. 取证引擎流程（执行时序）

1. 拉取目标公司最新结构化信号（财务、治理、交易、情绪、外部约束）。
2. 标准化后产出单点异常分数。
3. 执行组合异常检测，计算协同风险项。
4. 建立并裁剪触发链 DAG（去除低置信边）。
5. 汇总 fragility score 与分项卡。
6. 生成 90 天监控计划（含频率、触发阈值、动作）。
7. 将结果推送给 risk-monitor 与 deep-research 作为下游输入。

---

## 9. 风险治理与可解释性要求

- 每个风险结论必须可回溯到原始证据（source + timestamp + transform）。
- 每个高风险评级必须包含 `top_drivers` 与 `invalidators`。
- 当数据缺失超过阈值（如核心字段缺失 >30%）时，结论必须附 `low_confidence` 标记。
- 关键规则参数（阈值、权重、置信度门槛）要求版本化管理。

---

## 10. 迭代路线图

### Phase 1（MVP）

- 完成 CN/US 双市场 schema 对齐。
- 落地三份核心输出文件。
- 提供 rule-based 触发链 + 线性 fragility 聚合。

### Phase 2（增强）

- 引入图模型/贝叶斯网络估计链路权重。
- 加入同行对照与行业热区基线（peer-relative fragility）。
- 接入 valuation plugin，实现“风险→估值折价”联动。

### Phase 3（运营化）

- 形成日更/周更任务编排。
- 维护风险案例库（命中、误报、漏报）做阈值再训练。
- 增加跨市场传染链（ADR/H股/A股）映射能力。

---

## 11. 交付清单

- 技术设计文档（本文）。
- 输出契约定义：
  - `forensics/red_flag_graph.json`
  - `forensics/fragility_scorecard.json`
  - `forensics/90d_monitor_plan.json`
- 后续实施建议：优先在 `risk-monitor` 插件中增加 `forensics` 子命令，实现单标的与组合级扫描。
