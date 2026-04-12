# 市场参数化适配指南

## 背景

当前技能库中存在大量重复的市场特定技能，例如：
- `China-market_xxx`
- `US-market_us-xxx`
- `HK-market_hk-xxx`

这些技能功能相同，只是市场不同。为提高维护效率、减少重复代码、便于跨市场分析，建议将这些技能合并为参数化技能。

## 参数化策略

### 何时使用参数化

**适合参数化的场景**：
- 技能核心逻辑相同（分析方法、输出结构）
- 仅数据源不同（API 调用、字段映射）
- 仅市场特性不同（交易规则、特殊注意点）

**不适合参数化的场景**：
- 技能逻辑差异很大（计算方法、模型框架）
- 输出格式完全不同（语言、结构）
- 市场特性无法简单适配

### 参数化方案选择

#### 方案1：简单参数化

适用于逻辑高度相似的场景。

**示例**：`valuation-regime-detector`

```yaml
parameters:
  market:
    type: string
    enum: [china, us, hk]
    default: china
```

在 SKILL.md 中：
- 工作流程统一
- 数据获取部分根据 market 调用不同 API
- 注意事项部分列出市场特性

#### 方案2：参数化 + 适配层

适用于逻辑相似但有市场差异的场景。

**示例**：`valuation-regime-detector`（已实施）

```
references/
  methodology-china.md
  methodology-us.md
  methodology-hk.md
  data-queries-china.md
  data-queries-us.md
  data-queries-hk.md
  output-template-china.md
  output-template-us.md
  output-template-hk.md
```

SKILL.md 根据 `market` 参数：
- Step 2: 使用对应的 `data-queries-{market}.md`
- Step 3: 使用对应的 `methodology-{market}.md`
- Step 4: 使用对应的 `output-template-{market}.md`

#### 方案3：保留独立技能 + 标记 deprecated

适用于差异很大的场景，不建议合并。

保留原有技能，但在顶部标记 `deprecated: true`，引导用户使用参数化技能。

## 迁移步骤

### Step 1: 差异分析

对比现有技能：
- SKILL.md 层面：描述、工作流程
- methodology 层面：计算逻辑、规则、阈值
- data-queries 层面：数据源、API、字段
- output-template 层面：输出格式、语言

判断是否适合合并。

### Step 2: 设计统一 schema

设计输入 schema：
```json
{
  "market": "china|us|hk",
  "target": "...",
  "codes": "...",
  "time_window": "...",
  "output_format": "..."
}
```

设计输出 schema（跨市场统一）：
```json
{
  "regime": "...",
  "valuation_percentile": "...",
  "key_metrics": "...",
  "drivers": "...",
  "risks": "...",
  "monitoring_points": "...",
  "confidence": "...",
  "next_steps": "..."
}
```

### Step 3: 创建统一 SKILL.md

创建新的统一技能目录：
```
.claude/skills/{skill-name}/
  SKILL.md
  references/
    methodology-{market}.md
    data-queries-{market}.md
    output-template-{market}.md
```

在 SKILL.md 中：
- 定义 `market` 参数
- 工作流程中根据 market 分支
- 列出市场特定注意事项
- 提供跨市场示例

### Step 4: 复制现有文件

将现有技能的 methodology、data-queries、output-template 复制到新目录，按市场重命名。

### Step 5: 标记原有技能 deprecated

在原有技能 SKILL.md 顶部添加：
```yaml
deprecated: true
```

添加迁移说明：
```markdown
**已废弃：请使用统一技能 {skill-name}，传入 market={market} 参数。**

迁移说明：
- 旧调用方式：使用本技能
- 新调用方式：使用 `.claude/skills/{skill-name}/SKILL.md`，传入 `{market: "{market}"}`
- 输出格式保持一致，向后兼容
```

### Step 6: 创建迁移指南

在 `.claude/FRAMEWORK/` 创建迁移指南文档。

### Step 7: 创建测试对比

在统一技能目录下创建 `tests/migration-validation.md`：
- 对比原技能与新技能的输出（至少3个 case）
- 确保合并后输出一致
- 记录差异（如果有）及原因

### Step 8: 更新相关 commands

查找哪些 commands 调用了原技能：
```bash
grep -r "us-valuation-regime-detector" .claude/commands/
```

更新为调用统一技能：
```yaml
skill: valuation-regime-detector
parameters:
  market: us
```

## 迁移 Checklist

- [ ] 差异分析完成
- [ ] 参数化方案确定（简单参数化 / 参数化+适配层）
- [ ] 统一 SKILL.md 创建
- [ ] 输入 schema 设计完成
- [ ] 输出 schema 设计完成（跨市场统一）
- [ ] 市场特定 methodology 文件创建
- [ ] 市场特定 data-queries 文件创建
- [ ] 市场特定 output-template 文件创建
- [ ] 原有技能标记 deprecated
- [ ] 迁移指南创建
- [ ] 测试对比文档创建
- [ ] 相关 commands 更新
- [ ] 向后兼容验证完成

## 优先迁移候选技能列表

### 高优先级（逻辑相似度高）

1. **market-breadth-monitor**
   - `China-market_market-breadth-monitor`
   - `US-market_us-market-breadth-monitor`
   - `HK-market_hk-market-breadth`
   - 逻辑相似：涨跌家数、新高新低、宽度动量

2. **volatility-regime-monitor**
   - `China-market_volatility-regime-monitor`
   - `US-market_us-volatility-regime-monitor`
   - 逻辑相似：波动率状态、风险开关、监控触发

3. **financial-statement-analyzer**
   - `China-market_financial-statement-analyzer`
   - `US-market_us-financial-statement-analyzer`
   - `HK-market_hk-financial-statement`
   - 逻辑相似：财务报表分析、盈利质量、财务健康

4. **liquidity-impact-estimator**
   - `China-market_liquidity-impact-estimator`
   - `US-market_us-liquidity-impact-estimator`
   - `HK-market_hk-liquidity-risk`
   - 逻辑相似：流动性评估、冲击成本、交易可行性

5. **peer-comparison-analyzer**
   - `China-market_peer-comparison-analyzer`
   - `US-market_us-peer-comparison-analyzer`
   - 逻辑相似：同业对比、估值、成长、盈利能力

### 中优先级（有一定差异）

1. **event-study**
   - `China-market_event-study`
   - `US-market_us-event-study`
   - 差异：事件类型可能不同，但框架相同

2. **portfolio-health-check**
   - `China-market_portfolio-health-check`
   - `US-market_us-portfolio-health-check`
   - 差异：风险指标可能不同，但诊断框架相同

3. **rebalancing-planner**
   - `China-market_rebalancing-planner`
   - `US-market_us-rebalancing-planner`
   - `US-market_us-tax-aware-rebalancing-planner`
   - 差异：税务考虑不同，但再平衡规则相同

4. **investment-memo-generator**
   - `China-market_investment-memo-generator`
   - `US-market_us-investment-memo-generator`
   - 差异：语言不同，但结构相同

### 低优先级（差异较大）

1. **etf-allocator**
   - `China-market_etf-allocator`
   - `US-market_us-etf-allocator`
   - 差异：ETF市场、品种差异大

2. **risk-adjusted-return-optimizer**
   - `China-market_risk-adjusted-return-optimizer`
   - `US-market_us-risk-adjusted-return-optimizer`
   - 差异：市场约束、风险偏好差异大

3. **sector-rotation-detector**
   - 不存在 China 版本（但有类似技能）
   - `US-market_us-sector-rotation-detector`
   - 差异：行业分类、轮动逻辑可能不同

## 数据源适配注意事项

### 中国市场（China）

- 数据源：理杏仁 API
- 市场特性：T+1、涨跌停、停牌、公告滞后
- 指标：A股特定指标（如北向资金、南向资金）
- 语言：中文

### 美国市场（US）

- 数据源：理杏仁 API + FRED
- 市场特性：无涨跌停、做空机制、美元流动性
- 指标：美股特定指标（如信用利差、实际利率）
- 语言：英文

### 港股市场（HK）

- 数据源：理杏仁 API + 港股通数据
- 市场特性：无涨跌停、南向资金、AH溢价、汇率影响
- 指标：港股特定指标（如南向资金流向、AH溢价率）
- 语言：中文（可考虑英文选项）

## 向后兼容性

### 确保向后兼容

1. **输出格式一致**：统一技能输出 schema 与原技能一致
2. **调用方式兼容**：原技能仍可调用（deprecated 但不删除）
3. **数据源相同**：使用相同的数据源和 API
4. **置信度一致**：保持相同的置信度计算逻辑

### 废弃策略

1. **标记 deprecated**：在原有技能顶部标记
2. **保留文件**：不删除原有技能文件（向后兼容）
3. **迁移说明**：明确新调用方式和参数
4. **过渡期**：给予用户过渡时间（建议至少 1-2 个月）
5. **最终删除**：过渡期后可考虑删除（需评估影响）

## 测试验证

### 迁移验证测试

每个迁移的技能需完成以下测试：

1. **输出一致性测试**：对比原技能与新技能输出（至少3个 case）
2. **跨市场测试**：测试不同 market 参数的输出
3. **向后兼容测试**：测试原有技能调用是否仍有效
4. **边界测试**：测试极端输入、缺失数据的处理

### 测试文档

在 `tests/migration-validation.md` 中记录：
- 测试 case（输入、预期输出、实际输出）
- 差异分析（如果有）
- 置信度对比
- 向后兼容性验证

## 维护建议

### 统一技能维护

1. **定期更新**：定期更新各市场的 methodology
2. **市场特性更新**：市场规则变化时更新注意事项
3. **跨市场一致性**：保持输出 schema 跨市场一致
4. **文档同步**：各市场文档需同步更新

### 废弃技能维护

1. **标记状态**：定期检查 deprecated 标记
2. **迁移进度**：监控用户迁移进度
3. **删除评估**：评估删除时机和影响

## 成功案例：valuation-regime-detector

已成功合并：
- `China-market_valuation-regime-detector`
- `US-market_us-valuation-regime-detector`
- 新增 `HK` 市场支持

合并方案：**参数化 + 适配层**

差异分析：
- 数据源不同（理杏仁 vs FRED）
- 计算逻辑部分不同（A股特性 vs 美股特性）
- 输出语言不同（中文 vs 英文）

统一 schema：
- 输入：`{market: "china|us|hk", ...}`
- 输出：跨市场统一的结构化输出

适配层：
- `methodology-{market}.md`
- `data-queries-{market}.md`
- `output-template-{market}.md`

向后兼容：原有技能标记 deprecated，但仍可调用。

---

**更新日期**：2026-04-12
**版本**：v1.0