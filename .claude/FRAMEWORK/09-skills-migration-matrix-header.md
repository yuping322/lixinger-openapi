# Skills 迁移矩阵（Skills Migration Matrix）

> 目的：追踪所有现有 skills 的归类、合并、淘汰决策
> 状态：todo / in-progress / done / blocked
> 最后更新：2026-04-12

---

## 迁移决策分类

### A 类：直接纳入（Keep & Wrap）
- 条件：主题清晰、输入输出明确、内容可复用
- 动作：补 frontmatter / I-O 契约 / QA 字段，挂到对应 plugin pack

### B 类：合并重构（Merge & Refactor）
- 条件：能力重复、边界重叠、命名分散
- 动作：合并为一个 plugin 下的多个子 skill，统一术语与输出

### C 类：淘汰或重写（Sunset & Rewrite）
- 条件：数据源失效、业务价值低、长期无人使用
- 动作：下线归档，必要时按新契约重写最小版本

---

## China-market Skills（55个）

### 研究分析域相关

| skill_name | business_domain | target_plugin_pack | migration_type | owner | status |
|-----------|----------------|-------------------|----------------|-------|--------|
| `financial-statement-analyzer` | Research & Attribution | Pack A | A | TBD | todo |
| `event-study` | Research & Attribution | Pack A | A | TBD | todo |
| `peer-comparison-analyzer` | Valuation & Decision | Pack A | A | TBD | todo |
| `event-driven-detector` | Research & Attribution | Pack A | A | TBD | todo |
| `institutional-research-heat-validator` | Research & Attribution | Pack A | B | TBD | todo |
| `dragon-tiger-list-analyzer` | Research & Attribution | Pack A | A | TBD | todo |
| `insider-trading-analyzer` | Research & Attribution | Pack A | A | TBD | todo |

### 估值决策域相关

| skill_name | business_domain | target_plugin_pack | migration_type | owner | status |
|-----------|----------------|-------------------|----------------|-------|--------|
| `valuation-regime-detector` | Valuation & Decision | Pack A | A | TBD | todo |
| `stock-bond-yield-gap-monitor` | Valuation & Decision | Pack A | A | TBD | todo |
| `tech-hype-vs-fundamentals` | Valuation & Decision | Pack A | A | TBD | todo |
| `sentiment-reality-gap` | Valuation & Decision | Pack A | A | TBD | todo |

### 风险监控域相关

| skill_name | business_domain | target_plugin_pack | migration_type | owner | status |
|-----------|----------------|-------------------|----------------|-------|--------|
| `equity-pledge-risk-monitor` | Risk & Post-Trade Monitoring | Pack B | A | TBD | todo |
| `st-delist-risk-scanner` | Risk & Post-Trade Monitoring | Pack B | A | TBD | todo |
| `goodwill-risk-monitor` | Risk & Post-Trade Monitoring | Pack B | A | TBD | todo |
| `ipo-lockup-risk-monitor` | Risk & Post-Trade Monitoring | Pack B | A | TBD | todo |
| `unlock-shock-overshoot-detector` | Risk & Post-Trade Monitoring | Pack B | A | TBD | todo |
| `unlock-shock-overreaction-finder` | Risk & Post-Trade Monitoring | Pack B | B | TBD | todo |
| `share-repurchase-monitor` | Risk & Post-Trade Monitoring | Pack B | A | TBD | todo |
| `margin-risk-monitor` | Risk & Post-Trade Monitoring | Pack B | A | TBD | todo |
| `factor-crowding-monitor` | Risk & Post-Trade Monitoring | Pack B | A | TBD | todo |
| `volatility-regime-monitor` | Risk & Post-Trade Monitoring | Pack B | A | TBD | todo |
| `liquidity-impact-estimator` | Risk & Post-Trade Monitoring | Pack B | A | TBD | todo |
| `limit-up-limit-down-risk-checker` | Risk & Post-Trade Monitoring | Pack B | A | TBD | todo |
| `ab-ah-premium-monitor` | Risk & Post-Trade Monitoring | Pack B | A | TBD | todo |
| `block-deal-monitor` | Risk & Post-Trade Monitoring | Pack B | A | TBD | todo |

### 组合执行域相关

| skill_name | business_domain | target_plugin_pack | migration_type | owner | status |
|-----------|----------------|-------------------|----------------|-------|--------|
| `portfolio-health-check` | Portfolio & Allocation | Pack C | A | TBD | todo |
| `rebalancing-planner` | Portfolio & Allocation | Pack C | A | TBD | todo |
| `etf-allocator` | Portfolio & Allocation | Pack C | A | TBD | todo |
| `risk-adjusted-return-optimizer` | Portfolio & Allocation | Pack C | A | TBD | todo |
| `portfolio-stress-test` | Portfolio & Allocation | Pack C | A | TBD | todo |
| `portfolio-monitor-orchestrator` | Portfolio & Allocation | Pack C | A | TBD | todo |

### 投研交付域相关

| skill_name | business_domain | target_plugin_pack | migration_type | owner | status |
|-----------|----------------|-------------------|----------------|-------|--------|
| `investment-memo-generator` | Delivery & Reporting | Pack E (新增) | A | TBD | todo |
| `weekly-market-brief-generator` | Delivery & Reporting | Pack E | A | TBD | todo |
| `suitability-report-generator` | Delivery & Reporting | Pack E | A | TBD | todo |
| `equity-research-orchestrator` | Delivery & Reporting | Pack E | A | TBD | todo |

### 数据获取域相关

| skill_name | business_domain | target_plugin_pack | migration_type | owner | status |
|-----------|----------------|-------------------|----------------|-------|--------|
| `lixinger-data-query` | Data Acquisition | Pack D | A | TBD | todo |

### 其他待归类

| skill_name | business_domain | target_plugin_pack | migration_type | owner | status |
|-----------|----------------|-------------------|----------------|-------|--------|
| `northbound-flow-analyzer` | Research & Attribution | Pack A | A | TBD | todo |
| `hsgt-holdings-monitor` | Research & Attribution | Pack A | A | TBD | todo |
| `fund-flow-monitor` | Research & Attribution | Pack A | A | TBD | todo |
| `market-breadth-monitor` | Research & Attribution | Pack A | A | TBD | todo |
| `market-overview-dashboard` | Delivery & Reporting | Pack E | A | TBD | todo |
| `macro-liquidity-monitor` | Research & Attribution | Pack A | A | TBD | todo |
| `sector-valuation-heat-map` | Valuation & Decision | Pack A | A | TBD | todo |
| `limit-up-pool-analyzer` | Research & Attribution | Pack A | A | TBD | todo |
| `hot-rank-sentiment-monitor` | Research & Attribution | Pack A | A | TBD | todo |
| `intraday-microstructure-analyzer` | Research & Attribution | Pack A | A | TBD | todo |
| `opposing-pair-detector` | Research & Attribution | Pack A | A | TBD | todo |
| `single-stock-health-check` | Research & Attribution | Pack A | A | TBD | todo |
| `dividend-corporate-action-tracker` | Research & Attribution | Pack A | A | TBD | todo |
| `convertible-bond-scanner` | Research & Attribution | Pack A | A | TBD | todo |
| `ipo-newlist-monitor` | Research & Attribution | Pack A | A | TBD | todo |
| `ipo-ecosystem-research` | Research & Attribution | Pack A | A | TBD | todo |
| `disclosure-notice-monitor` | Risk & Post-Trade Monitoring | Pack B | A | TBD | todo |
| `shareholder-structure-monitor` | Research & Attribution | Pack A | A | TBD | todo |
| `shareholder-risk-check` | Risk & Post-Trade Monitoring | Pack B | A | TBD | todo |
| `ah-premium-sector-flow-linkage` | Valuation & Decision | Pack A | A | TBD | todo |
| `mna-buyback-insider-resonance-alpha` | Event-driven | Pack A | A | TBD | todo |

---

## US-market Skills（36个）

> 结构与 China 类似，建议合并同类能力，保留市场参数适配层

### 建议合并组（B类）

| 合并目标 | 源 skills | migration_type |
|---------|----------|----------------|
| `valuation-regime-detector` | `us-valuation-regime-detector` + `valuation-regime-detector` | B |
| `market-breadth-monitor` | `us-market-breadth-monitor` + `market-breadth-monitor` | B |
| `volatility-regime-monitor` | `us-volatility-regime-monitor` + `volatility-regime-monitor` | B |
| `financial-statement-analyzer` | `us-financial-statement-analyzer` + `financial-statement-analyzer` | B |

### 独立保留（A类）

| skill_name | business_domain | target_plugin_pack | migration_type | owner | status |
|-----------|----------------|-------------------|----------------|-------|--------|
| `us-insider-trading-analyzer` | Research & Attribution | Pack A | A | TBD | todo |
| `us-insider-sentiment-aggregator` | Research & Attribution | Pack A | A | TBD | todo |
| `us-dividend-aristocrat-calculator` | Valuation & Decision | Pack A | A | TBD | todo |
| `us-small-cap-growth-identifier` | Research & Attribution | Pack A | A | TBD | todo |
| `us-quant-factor-screener` | Research & Attribution | Pack A | A | TBD | todo |
| `us-earnings-reaction-analyzer` | Research & Attribution | Pack A | A | TBD | todo |
| `us-options-strategy-analyzer` | Portfolio & Allocation | Pack C | A | TBD | todo |
| `us-sector-rotation-detector` | Research & Attribution | Pack A | A | TBD | todo |
| `us-yield-curve-regime-detector` | Valuation & Decision | Pack A | A | TBD | todo |
| `us-policy-sensitivity-brief` | Research & Attribution | Pack A | A | TBD | todo |

---

## HK-market Skills（12个）

| skill_name | business_domain | target_plugin_pack | migration_type | owner | status |
|-----------|----------------|-------------------|----------------|-------|--------|
| `hk-market-overview` | Delivery & Reporting | Pack E | A | TBD | todo |
| `hk-southbound-flow` | Research & Attribution | Pack A | A | TBD | todo |
| `hk-foreign-flow` | Research & Attribution | Pack A | A | TBD | todo |
| `hk-etf-flow` | Research & Attribution | Pack A | A | TBD | todo |
| `hk-sector-rotation` | Research & Attribution | Pack A | A | TBD | todo |
| `hk-valuation-analyzer` | Valuation & Decision | Pack A | A | TBD | todo |
| `hk-financial-statement` | Research & Attribution | Pack A | A | TBD | todo |
| `hk-dividend-tracker` | Valuation & Decision | Pack A | A | TBD | todo |
| `hk-concentration-risk` | Risk & Post-Trade Monitoring | Pack B | A | TBD | todo |
| `hk-liquidity-risk` | Risk & Post-Trade Monitoring | Pack B | A | TBD | todo |
| `hk-currency-risk` | Risk & Post-Trade Monitoring | Pack B | A | TBD | todo |
| `hk-market-breadth` | Research & Attribution | Pack A | A | TBD | todo |

---

## 统计汇总

| 分类 | 数量 | 占比 |
|-----|------|-----|
| A类（直接纳入） | ~95 | ~85% |
| B类（合并重构） | ~15 | ~13% |
| C类（淘汰重写） | ~3 | ~2% |

---

## 下一步动作

1. 为所有 A类 skill 补齐 I/O 契约与 frontmatter
2. 执行 B类合并（先合并 valuation-regime-detector 系列）
3. 评估 C类候选（低频使用、数据源失效）
4. 为每个 Pack 指定 Owner
5. 建立 Pack 内 smoke test case

---

## 注意事项

- 本矩阵仅用于迁移决策追踪，不涉及具体代码改造
- 实际改造需按 Plugin Spec v1 执行
- 市场前缀（China/US/HK）应逐步改为参数，而非组织维度