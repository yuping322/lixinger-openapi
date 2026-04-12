# Legacy Skills → Engine Rules Mapping

本文档定义 legacy skills 与新规则引擎之间的映射关系、降级策略与告警语义统一规则。

---

## 1. 映射总览

| Legacy Skill | 主规则 ID | 子规则数 | 降级策略 | 告警语义 |
|--------------|-----------|----------|----------|----------|
| `equity-pledge-risk-monitor` | `PLEDGE_001` | 2 | hybrid | 质押控制权风险 |
| `goodwill-risk-monitor` | `GOODWILL_001` | 2 | hybrid | 商誉减值风险 |
| `ipo-lockup-risk-monitor` | `IPO_001` | 2 | hybrid | 解禁供给冲击 |
| `limit-up-limit-down-risk-checker` | `BOARD_001` | 2 | legacy_only | 涨跌停可交易性 |
| `liquidity-impact-estimator` | `LIQUIDITY_001` | 2 | hybrid | 流动性冲击成本 |
| `margin-risk-monitor` | `MARGIN_001` | 2 | hybrid | 两融拥挤风险 |
| `shareholder-risk-check` | `SHAREHOLDER_RISK_001` | 2 | hybrid | 治理控制权风险 |
| `shareholder-structure-monitor` | `SHAREHOLDER_STRUCT_001` | 2 | hybrid | 筹码结构变化 |
| `st-delist-risk-scanner` | `ST_DELIST_001` | 2 | legacy_only | 退市制度风险 |

---

## 2. 详细映射规则

### 2.1 equity-pledge-risk-monitor（股权质押风险）

**降级策略：hybrid**

| Engine Rule | 触发条件 | Severity | Legacy 对应分析点 |
|-------------|----------|----------|-------------------|
| `equity-pledge-risk-monitor` (PLEDGE_001) | pledge_ratio_controller >= 0.75 && distance_to_margin_call <= 0.2 | high/critical | 控制股东质押比例 + 平仓距离 |
| `equity-pledge-risk-monitor-margin-call` | 距平仓线 < 10% | critical | 紧急平仓风险 |
| `equity-pledge-risk-monitor-concentration` | 质押集中度 > 80% | high | 质押结构脆弱性 |

**告警语义统一**：
- legacy 输出：`控制权与财务/流动性风险提示`
- engine 输出：`alert.thesis = "控股股东高质押且接近平仓线，存在被动减持与控制权扰动风险"`

### 2.2 goodwill-risk-monitor（商誉风险）

**降级策略：hybrid**

| Engine Rule | 触发条件 | Severity | Legacy 对应分析点 |
|-------------|----------|----------|-------------------|
| `goodwill-risk-monitor` (GOODWILL_001) | goodwill_ratio >= 0.3 && impairment_probability >= 0.5 | high | 商誉规模 + 减值概率 |
| `goodwill-risk-monitor-impairment-probability` | 减值概率 > 70% | critical | 减值冲击预警 |
| `goodwill-risk-monitor-auditor-change` | 审计师变更 + 商誉高 | medium | 审计风险信号 |

**告警语义统一**：
- legacy 输出：`潜在商誉减值风险与财报冲击`
- engine 输出：`alert.thesis = "商誉占净资产比例高且减值概率大，存在财报冲击风险"`

### 2.3 ipo-lockup-risk-monitor（解禁风险）

**降级策略：hybrid**

| Engine Rule | 触发条件 | Severity | Legacy 对应分析点 |
|-------------|----------|----------|-------------------|
| `ipo-lockup-risk-monitor` (IPO_001) | near_term_unlock_ratio >= 0.15 | medium | 近期解禁比例 |
| `ipo-lockup-risk-monitor-near-term-unlock` | 30天内解禁 > 20% | high | 近期解禁冲击 |
| `ipo-lockup-risk-monitor-vc-exit-pressure` | VC持股 + 解禁临近 | high | VC退出压力 |

**告警语义统一**：
- legacy 输出：`供给冲击风险提示`
- engine 输出：`alert.thesis = "近期限售解禁规模大，存在供给冲击风险"`

### 2.4 limit-up-limit-down-risk-checker（涨跌停风险）

**降级策略：legacy_only**

> 原因：涨跌停涉及实时交易制度约束，engine 规则尚未完全覆盖盘中动态。

| Engine Rule | 触发条件 | Severity | Legacy 对应分析点 |
|-------------|----------|----------|-------------------|
| `limit-up-limit-down-risk-checker` (BOARD_001) | 当前涨跌停状态 | high | 可交易性约束 |
| `limit-up-limit-down-risk-checker-liquidation-chain` | 连板跌停 | critical | 清算链风险 |
| `limit-up-limit-down-risk-checker-board-failure` | 涨停封板失败 | medium | 板块情绪转折 |

**降级行为**：
- mode=engine_only 时：仅执行 BOARD_001 主规则，输出警告提示 legacy_only 模式更完整
- mode=hybrid 时：legacy 输出为主，engine 输出作为补充

### 2.5 liquidity-impact-estimator（流动性风险）

**降级策略：hybrid**

| Engine Rule | 触发条件 | Severity | Legacy 对应分析点 |
|-------------|----------|----------|-------------------|
| `liquidity-impact-estimator` (LIQUIDITY_001) | turnover < 1% && volume < avg*0.5 | high | 低流动性预警 |
| `liquidity-impact-estimator-depth-slippage` | 滑点估算 > 3% | critical | 交易冲击成本 |
| `liquidity-impact-estimator-auction-gap` | 集合竞价缺口大 | medium | 日内流动性缺口 |

**告警语义统一**：
- legacy 输出：`流动性风险与交易冲击成本代理`
- engine 输出：`alert.thesis = "流动性不足，大额交易存在显著冲击成本风险"`

### 2.6 margin-risk-monitor（两融风险）

**降级策略：hybrid**

| Engine Rule | 触发条件 | Severity | Legacy 对应分析点 |
|-------------|----------|----------|-------------------|
| `margin-risk-monitor` (MARGIN_001) | margin_balance_ratio_change > 0.1 | medium | 两融余额变化 |
| `margin-risk-monitor-crowded-long` | 融资集中度高 | high | 拥挤做多风险 |
| `margin-risk-monitor-financing-broker-divergence` | 券商融资分歧 | medium | 杠杆预期分歧 |

**告警语义统一**：
- legacy 输出：`踩踏与波动放大风险`
- engine 输出：`alert.thesis = "融资余额快速上升且持仓集中，存在踩踏风险"`

### 2.7 shareholder-risk-check（股东风险检查）

**降级策略：hybrid**

| Engine Rule | 触发条件 | Severity | Legacy 对应分析点 |
|-------------|----------|----------|-------------------|
| `shareholder-risk-check` (SHAREHOLDER_RISK_001) | control_instability_signal | high | 控制权稳定性 |
| `shareholder-risk-check-reduction-plan` | 减持计划公告 | medium | 减持风险 |
| `shareholder-risk-check-equity-freeze` | 股权冻结 | critical | 司法风险 |

**告警语义统一**：
- legacy 输出：`治理风险标签`
- engine 输出：`alert.thesis = "股东结构或控制权存在不稳定信号"`

### 2.8 shareholder-structure-monitor（股东结构监控）

**降级策略：hybrid**

| Engine Rule | 触发条件 | Severity | Legacy 对应分析点 |
|-------------|----------|----------|-------------------|
| `shareholder-structure-monitor` (SHAREHOLDER_STRUCT_001) | holder_count_change > 20% | medium | 股东户数变化 |
| `shareholder-structure-monitor-ownership-instability` | 大股东变动 | high | 持股集中度变化 |
| `shareholder-structure-monitor-related-party-rise` | 关联方持股上升 | medium | 关联交易风险 |

**告警语义统一**：
- legacy 输出：`筹码结构与供给冲击风险提示`
- engine 输出：`alert.thesis = "股东结构显著变化，存在筹码供给冲击风险"`

### 2.9 st-delist-risk-scanner（退市风险）

**降级策略：legacy_only**

> 原因：退市制度判定涉及多维度财务指标与监管公告，engine 规则尚未完全覆盖制度性触发逻辑。

| Engine Rule | 触发条件 | Severity | Legacy 对应分析点 |
|-------------|----------|----------|-------------------|
| `st-delist-risk-scanner` (ST_DELIST_001) | ST标签或退市风险警示 | critical | 制度性风险 |
| `st-delist-risk-scanner-financial-trigger` | 财务指标触发退市条件 | critical | 财务退市风险 |
| `st-delist-risk-scanner-compliance-trigger` | 合规问题触发退市 | critical | 合规退市风险 |

**降级行为**：
- mode=engine_only 时：仅执行 ST_DELIST_001 主规则，建议用户切换 legacy_only
- mode=hybrid 时：legacy 输出为主，engine 输出作为补充

---

## 3. 降级策略定义

### 3.1 策略类型

| 策略 | 定义 | 使用场景 |
|------|------|----------|
| `legacy_only` | 仅执行 legacy skill，engine 规则不触发 | 制度性风险、实时交易约束 |
| `hybrid` | legacy + engine 并行输出对照 | 大多数风险维度 |
| `engine_only` | 仅执行 engine 规则，legacy 不触发 | 规则已完全覆盖的维度 |

### 3.2 hybrid 模式输出对照规则

```
comparison_strategy:
  - risk_type_match: 检查 legacy 与 engine 输出风险类型一致性
  - severity_consistency: 检查等级差异（允许 ±1 级）
  - thesis_overlap: 检查 thesis 核心结论重叠度
  - disagreement_action: 标记人工复核
```

### 3.3 disagreement 处理流程

1. legacy 与 engine severity 差异 > 1 级 → 标记 `needs_review`
2. thesis 核心结论矛盾 → 标记 `needs_review`
3. 仅一方触发告警 → 标记 `partial_coverage`

---

## 4. 告警语义统一规则

### 4.1 thesis 模板

所有 engine 输出 thesis 必须遵循：
```
"{风险主体}{风险特征}，存在{风险后果}风险"
```

示例：
- `控股股东高质押且接近平仓线，存在被动减持与控制权扰动风险`
- `商誉占净资产比例高且减值概率大，存在财报冲击风险`
- `融资余额快速上升且持仓集中，存在踩踏风险`

### 4.2 severity 映射

| Legacy 输出级别 | Engine 输出级别 | 统一展示 |
|-----------------|-----------------|----------|
| 红色预警 | critical | 🔴 Critical |
| 黄色预警 | high | 🟠 High |
| 蓝色预警 | medium | 🟡 Medium |
| 绿色提示 | low | 🟢 Low |
- 无风险 | none | ⚪ None |

### 4.3 evidence_refs 要求

engine 输出必须包含：
- 数据源引用（lixinger / announcement / market）
- 指标值（如 `pledge_ratio_controller=0.82`）
- 阈值对比（如 `threshold=0.75`）

---

## 5. 跨维度规则映射

| Rule ID | 涉及维度 | 说明 |
|---------|----------|------|
| `cross-dimension-risk-liquidity-pledge` | liquidity + equity_pledge | 流动性恶化加剧质押平仓风险 |
| `cross-dimension-governance-financial-stress` | shareholder + margin | 治理风险叠加杠杆压力 |
| `cross-dimension-event-risk` | ipo_lockup + board | 解禁事件叠加涨跌停约束 |

---

## 6. 版本与变更记录

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| 1.0.0 | 2026-04-12 | 初始映射表建立 |