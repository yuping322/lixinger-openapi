# Plugin Pack 分组策略

## Pack 定义原则

每个 Plugin Pack 必须：
1. 面向一个明确的业务目标
2. 包含 3~7 个 plugin
3. 每个 plugin 包含 3~10 个核心 skills
4. 有清晰的 Pack Owner
5. 有独立的交付节奏

---

## Pack A：选股前研究 (Pre-Selection Research)

**业务目标**：帮助分析师完成从行业筛选到个股估值的全流程研究

### 包含 Plugin（建议）
1. `industry-concept-research` - 行业/主题研究
2. `valuation` - 估值分析
3. `stock-screener` - 股票筛选
4. `financial-statement-analyzer` - 财务体检
5. `event-driven-detector` - 事件机会识别

### 目标 Skills 数量：15~30

### Pack Owner：待定

---

## Pack B：选股后排雷 (Post-Selection Risk)

**业务目标**：帮助风控团队识别已选个股的潜在风险

### 包含 Plugin（建议）
1. `risk-monitor` - 风险监控引擎
2. `equity-pledge-risk-monitor` - 股权质押风险
3. `st-delist-risk-scanner` - ST/退市风险
4. `goodwill-risk-monitor` - 商誉风险
5. `ipo-lockup-risk-monitor` - 解禁风险

### 目标 Skills 数量：10~20

### Pack Owner：待定

---

## Pack C：组合层管理 (Portfolio Management)

**业务目标**：帮助基金经理管理组合仓位、约束与再平衡

### 包含 Plugin（建议）
1. `portfolio-health-check` - 组合体检
2. `rebalancing-planner` - 再平衡规划
3. `etf-allocator` - ETF配置
4. `risk-adjusted-return-optimizer` - 风险收益优化

### 目标 Skills 数量：10~15

### Pack Owner：待定

---

## Pack D：数据基础设施 (Data Infrastructure)

**业务目标**：提供稳定、高效的数据获取与可用性管理

### 包含 Plugin（建议）
1. `query_data` - 数据查询
2. `stock-crawler` - 数据爬取（可选）
3. `lixinger-data-query` - 理杏仁数据接口

### 目标 Skills 数量：3~8

### Pack Owner：待定

---

## Pack 分组决策矩阵

对每个现有 skill/plugin 进行归类：

| 决策维度 | 权重 | 评分标准 |
|---------|------|---------|
| 业务域归属 | 40% | 明确属于哪个域 |
| 用户角色 | 30% | 主要服务谁 |
| 复用频次 | 20% | 被多少其他 pack 调用 |
| 数据依赖 | 10% | 是否依赖特定数据源 |

**总分计算**：
```
Pack_Score = 业务域(40%) + 用户角色(30%) + 复用频次(20%) + 数据依赖(10%)
```

归类到得分最高的 Pack。

---

## 跨 Pack 调用规则

1. Pack 内调用：自由调用
2. 跨 Pack 调用：必须通过标准化契约
3. 禁止：Pack 内 skill 直接调用其他 Pack 的数据源

**示例**：
- Pack A 的 `valuation` 可以调用 Pack D 的 `query_data`（通过契约）
- Pack A 的 `valuation` 不可以直接调用理杏仁 API

---

## Pack 发布节奏

每个 Pack 独立发布，节奏建议：
- Pack A：每月一次（研究需求高频变化）
- Pack B：每季度一次（风险规则相对稳定）
- Pack C：每季度一次（组合管理相对稳定）
- Pack D：每周一次（数据源高频变化）