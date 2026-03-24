# Skills 问题分析文档

> 本文档记录不在本轮 `skills-quality-remediation` 修复范围内的三类问题，供用户后续手动处理参考。

---

## 1. SKILLS_MAP.md 状态失真问题

### 问题描述

`analysis-market/SKILLS_MAP.md` 将几乎所有 108 个 Skill 标记为 `✅`，无法区分以下真实状态：

- `stable`：API 已核验，方法论完整，输出模板完整
- `partial`：部分 API 已核验，方法论或模板存在 TODO
- `experimental`：API 未核验，依赖 AkShare 或猜测型接口
- `broken`：已知存在 API 不存在或参数冲突问题

### 被错误标为 ✅ 的典型 Skill

以下 Skill 存在已知问题，但在 SKILLS_MAP.md 中仍标记为 `✅`：

| Skill | 实际状态 | 问题类型 |
|-------|---------|---------|
| `China-market_esg-screener` | broken | 调用不存在的 API（`cn/company/esg` 等） |
| `China-market_sector-valuation-heat-map` | broken | 使用点号路径 + 猜测型接口 |
| `US-market_us-dividend-aristocrat-calculator` | broken | 跨市场污染，使用 A 股路径和代码 |
| `China-market_hsgt-holdings-monitor` | experimental | 强依赖 AkShare，无降级 |
| `China-market_northbound-flow-analyzer` | experimental | 强依赖 AkShare |
| `China-market_undervalued-stock-screener` | experimental | 全市场扫描模型，高成本高失败率 |
| `China-market_quant-factor-screener` | experimental | 全市场扫描模型 |
| `China-market_macro-liquidity-monitor` | partial | methodology.md 含大量 [TODO] |
| `China-market_event-study` | partial | methodology.md 含大量 [TODO] |
| `US-market_us-peer-comparison-analyzer` | partial | methodology.md 含大量 [TODO] |
| `US-market_us-tax-aware-rebalancing-planner` | partial | methodology.md 含大量 [TODO] |

### 建议重标维度

重标时建议为每个 Skill 增加以下字段：

```
状态: stable / partial / experimental / broken
数据依赖: lixinger-only / lixinger+akshare / manual
API 核验: yes / no / partial
```

---

## 2. AkShare 重依赖 Skill 清单

### 问题描述

以下 Skill 的核心数据强依赖 AkShare。当 AkShare 不可用（被封、超时、数据缺失）时，这些 Skill 直接报错退出即可——**不需要三层降级改造**，这是本轮范围外的决策。

用户可根据实际需要决定是否为这些 Skill 增加降级逻辑。

### AkShare 重依赖 Skill 清单

#### A 股市场

| Skill | AkShare 依赖内容 | 不可用时行为 |
|-------|----------------|------------|
| `China-market_hsgt-holdings-monitor` | 沪深港通持仓数据（`ak.stock_hsgt_hold_stock_em` 等） | 直接报错退出，提示 AkShare 不可用 |
| `China-market_northbound-flow-analyzer` | 北向资金流数据（`ak.stock_hsgt_north_net_flow_in` 等） | 直接报错退出 |
| `China-market_dragon-tiger-list-analyzer` | 龙虎榜数据（`ak.stock_lhb_detail_em` 等） | 直接报错退出 |
| `China-market_limit-up-pool-analyzer` | 涨停板池数据（`ak.stock_zt_pool_em` 等） | 直接报错退出 |
| `China-market_intraday-microstructure-analyzer` | 盘中分时数据（`ak.stock_intraday_em` 等） | 直接报错退出 |
| `China-market_hot-rank-sentiment-monitor` | 热度排名数据（`ak.stock_hot_rank_detail_realtime_em` 等） | 直接报错退出 |
| `China-market_fund-flow-monitor` | 资金流向数据（`ak.stock_individual_fund_flow` 等） | 直接报错退出 |
| `China-market_margin-risk-monitor` | 融资融券数据（`ak.stock_margin_detail_szse` 等） | 直接报错退出 |

#### 说明

- 上述 Skill 的核心功能依赖 AkShare 提供的实时/高频数据，Lixinger API 无法替代
- 当 AkShare 不可用时，Skill 应输出明确的错误信息，说明数据源不可用，而非静默返回空结果
- 建议在各 Skill 的 `SKILL.md` 中增加一行说明：`数据依赖: AkShare（核心数据不可用时直接报错退出）`

---

## 3. 筛选类 Skill 执行模型问题清单

### 问题描述

以下筛选类 Skill 的执行模型与 API 能力不匹配：

- **问题**：默认对全市场（5000+ 股票）执行历史数据扫描
- **API 限制**：Lixinger API 为单代码 + `startDate` 模式，不支持批量全市场拉取
- **后果**：极高调用成本（数千次 API 请求）或批量失败

### 受影响 Skill 清单

| Skill | 当前执行模型 | 问题 |
|-------|------------|------|
| `China-market_undervalued-stock-screener` | 全市场历史扫描（PE/PB/ROE 等） | 需逐一查询 5000+ 股票，成本极高 |
| `China-market_quant-factor-screener` | 全市场多因子扫描 | 同上，且因子越多成本越高 |
| `China-market_small-cap-growth-identifier` | 全市场小盘成长筛选 | 同上 |
| `China-market_esg-screener` | 全市场 ESG 评分扫描 | 同上，且 ESG API 本身不存在 |
| `China-market_st-delist-risk-scanner` | 全市场 ST/退市风险扫描 | 同上 |
| `US-market_us-undervalued-stock-screener` | 全美股历史扫描 | 美股数量更多，成本更高 |
| `US-market_us-quant-factor-screener` | 全美股多因子扫描 | 同上 |
| `US-market_us-small-cap-growth-identifier` | 全美股小盘成长筛选 | 同上 |

### 建议执行模型（供参考，不在本轮实施）

如用户后续决定修复，建议采用"候选池收缩"模型：

```
Step 1: 定义候选池（如指数成分股 Top N，而非全市场）
Step 2: 快照筛选（用指数基本面数据初步过滤）
Step 3: 对候选集取历史数据（仅对 50-200 只股票查询）
Step 4: 排序输出
```

这样可将 API 调用次数从 5000+ 降至 50-200 次。
