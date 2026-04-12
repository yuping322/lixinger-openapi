# 业务域地图（Domain Map）

## 一级业务域定义（6组）

### 1. 数据获取域 (Data Acquisition)
**职责**：行情/财报/公告/新闻/另类数据获取与可用性管理
- 输入：外部数据源（理杏仁/东财/Wind等）
- 输出：标准化数据模型 + 可用性状态
- 关键能力：数据查询、缓存管理、缺口检测、时效标注
- 相关 skills: `lixinger-data-query`, `query_data`

### 2. 研究分析域 (Research & Attribution)
**职责**：行业、主题、因子、事件、归因分析
- 输入：标准化数据模型 + 用户意图
- 输出：研究结论 + 归因报告
- 关键能力：行业分析、财务分析、事件归因、因子研究
- 相关 skills: `financial-statement-analyzer`, `event-study`, `industry-concept-research`

### 3. 估值决策域 (Valuation & Decision)
**职责**：估值、情景、可比、投研结论生成
- 输入：研究结论 +可比公司数据
- 输出：估值区间 + 投资建议 + 置信度
- 关键能力：估值计算、可比分析、情景推演
- 相关 skills: `valuation-regime-detector`, `peer-comparison-analyzer`, `valuation`

### 4. 风险监控域 (Risk & Post-Trade Monitoring)
**职责**：排雷、事件触发、持仓后告警
- 输入：持仓数据 + 市场事件流
- 输出：风险标签 + 告警信号 + 复评建议
- 关键能力：风险扫描、事件预警、触发复评
- 相关 skills: `equity-pledge-risk-monitor`, `st-delist-risk-scanner`, `risk-monitor`

### 5. 组合执行域 (Portfolio & Allocation)
**职责**：仓位、约束、再平衡、风控联动
- 输入：投资建议 + 组合约束
- 输出：仓位方案 + 执行清单 + 约束检查报告
- 关键能力：仓位优化、约束检查、再平衡规划
- 相关 skills: `portfolio-health-check`, `rebalancing-planner`, `etf-allocator`

### 6. 投研交付域 (Delivery & Reporting)
**职责**：报告、结论卡片、监控清单、审计追踪
- 输入：各域输出结果
- 输出：交付物（报告/卡片/清单）
- 关键能力：报告生成、卡片组装、监控清单输出
- 相关 skills: `investment-memo-generator`, `weekly-market-brief-generator`, `suitability-report-generator`

---

## 跨域标准流程

```
数据获取域 → 研究分析域 → 估值决策域 → 风险监控域 → 组合执行域 → 投研交付域
```

**关键约束**：
- 每个域只负责单一环节
- 跨域调用必须通过标准化契约
- 禁止跳域直接调用数据源

---

## Plugin Pack 分组规则

### Pack A：选股前研究 (Pre-Selection Research)
- 覆盖域：研究分析域 + 估值决策域
- 目标用户：研究员/分析师
- Plugin 数量：3~7个

### Pack B：选股后排雷 (Post-Selection Risk)
- 覆盖域：风险监控域
- 目标用户：风控/合规
- Plugin 数量：3~5个

### Pack C：组合层管理 (Portfolio Management)
- 覆盖域：组合执行域 + 风险监控域
- 目标用户：基金经理/交易员
- Plugin 数量：3~5个

### Pack D：数据基础设施 (Data Infrastructure)
- 覆盖域：数据获取域
- 目标用户：技术团队
- Plugin 数量：2~3个

---

## 市场适配层

**原则**：业务域优先，市场作为参数
- 同一业务能力，多市场适配通过参数切换
- 避免按市场无限复制 plugin 目录
- Market 维度作为 adapter/parameter，不作为 primary 组织维度

**示例**：
- `valuation-regime-detector` 支持 China/US/HK 参数
- 不建议拆成：`valuation-regime-detector-cn`, `valuation-regime-detector-us`, `valuation-regime-detector-hk`