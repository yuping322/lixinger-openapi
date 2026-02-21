# Findata Service 改造文档

## 执行摘要

**分析范围**：93 个 Skills (China-market: 59个, US-market: 33个, HK-market: 1个)
**数据依赖**：76 个 Views，120+ 个 Tools
**当前实现**：11 个 API 接口
**覆盖率**：约 15%

---

## 1. 当前实现 vs 需求对比

### 1.1 已实现的接口（11个）

| 分类 | 接口 | 对应 Skills | 状态 |
|------|------|-----------|------|
| **股票** | `/api/cn/stock/{symbol}/basic` | 所有股票相关 | ✅ 已实现 |
| **股票** | `/api/cn/stock/{symbol}/history` | 所有股票相关 | ✅ 已实现 |
| **股票** | `/api/cn/stock/{symbol}/realtime` | 所有股票相关 | ✅ 已实现 |
| **股票** | `/api/cn/stock/{symbol}/financial` | financial-statement-analyzer | ✅ 已实现 |
| **股票** | `/api/cn/stock/{symbol}/valuation` | valuation-regime-detector | ✅ 已实现 |
| **市场** | `/api/cn/market/overview` | market-overview-dashboard | ✅ 已实现 |
| **宏观** | `/api/cn/macro/lpr` | 3个宏观相关 | ✅ 已实现 |
| **宏观** | `/api/cn/macro/cpi` | 3个宏观相关 | ✅ 已实现 |
| **宏观** | `/api/cn/macro/ppi` | 3个宏观相关 | ✅ 已实现 |
| **宏观** | `/api/cn/macro/pmi` | 3个宏观相关 | ✅ 已实现 |
| **宏观** | `/api/cn/macro/m2` | 3个宏观相关 | ✅ 已实现 |

### 1.2 缺失的高优先级接口（按使用频率排序）

#### 第一优先级：核心数据接口（影响 50+ skills）

| 接口分类 | Tools 需求 | 影响技能数 | 优先级 |
|---------|-----------|----------|--------|
| **资金流向** | stock_market_fund_flow, stock_main_fund_flow 等 | 8 | P0 |
| **北向资金** | stock_hsgt_* 系列 | 8 | P0 |
| **行业板块** | stock_board_industry_* 系列 | 10 | P0 |
| **龙虎榜** | stock_lhb_* 系列 | 6 | P1 |
| **大宗交易** | stock_dzjy_* 系列 | 6 | P1 |
| **涨跌停池** | stock_zt_pool_*, stock_dt_pool_* | 6 | P1 |

#### 第二优先级：专项数据接口（影响 20+ skills）

| 接口分类 | Tools 需求 | 影响技能数 | 优先级 |
|---------|-----------|----------|--------|
| **融资融券** | stock_margin_* 系列 | 10 | P1 |
| **分红配股** | stock_fhps_em 等 | 4 | P2 |
| **股权质押** | stock_pledge_* | 2 | P2 |
| **限售解禁** | stock_restricted_* | 2 | P2 |
| **商誉风险** | stock_sy_* | 1 | P2 |
| **回购** | stock_repurchase_* | 1 | P2 |

#### 第三优先级：特色数据接口

| 接口分类 | Tools 需求 | 影响技能数 | 优先级 |
|---------|-----------|----------|--------|
| **概念板块** | stock_board_concept_* | 1 | P3 |
| **热点排行** | stock_hot_rank_em | 2 | P3 |
| **ESG评级** | stock_esg_* | 1 | P3 |
| **IPO新股** | stock_ipo_* | 3 | P3 |

---

## 2. 详细需求分析

### 2.1 资金流向接口（P0 - 最优先）

**影响 Skills**：
- fund-flow-monitor
- industry-board-analyzer（部分）
- market-overview-dashboard（部分）

**需要实现的接口**：

```python
# 1. 大盘资金流
GET /api/cn/flow/market
返回: 日期, 主力净流入, 超大单净流入, 大单净流入等

# 2. 个股资金流
GET /api/cn/flow/stock/{symbol}
返回: 主力净流入, 散户净流入等

# 3. 主力资金排名
GET /api/cn/flow/rank
参数: indicator=today|3d|5d|10d
返回: 排名列表

# 4. 板块资金流
GET /api/cn/flow/sector
参数: sector_type=industry|concept, indicator=today|5d|10d
返回: 板块资金流排名

# 5. 大单追踪
GET /api/cn/flow/big-deal
返回: 大单交易明细
```

**理杏仁对应 API**：
- 无直接对应，需要使用 AKShare 或其他数据源

### 2.2 北向资金接口（P0）

**影响 Skills**：
- northbound-flow-analyzer
- hsgt-holdings-monitor
- ab-ah-premium-monitor

**需要实现的接口**：

```python
# 1. 北向资金流向
GET /api/cn/special/northbound/flow
参数: start_date, end_date, market=all|sh|sz
返回: 日期, 沪股通净买入, 深股通净买入

# 2. 北向持股明细
GET /api/cn/special/northbound/holdings/{symbol}
返回: 持股数量, 持股比例, 变动

# 3. 北向持股排名
GET /api/cn/special/northbound/rank
参数: indicator=today|5d|10d
返回: 持股排名列表

# 4. 板块北向资金
GET /api/cn/special/northbound/sector
返回: 板块北向资金分布
```

**理杏仁对应 API**：
- 无直接对应，需要使用 AKShare

### 2.3 行业板块接口（P0）

**影响 Skills**：
- industry-board-analyzer
- sector-rotation-detector
- industry-chain-mapper

**需要实现的接口**：

```python
# 1. 行业列表
GET /api/cn/board/industry/list
返回: 行业代码, 行业名称

# 2. 行业实时行情
GET /api/cn/board/industry/spot
返回: 行业涨跌幅, 领涨股等

# 3. 行业历史行情
GET /api/cn/board/industry/{industry_code}/history
参数: start_date, end_date
返回: K线数据

# 4. 行业成分股
GET /api/cn/board/industry/{industry_code}/stocks
返回: 成分股列表
```

**理杏仁对应 API**：
- `cn/index/` - 部分支持
- 需要补充 AKShare 数据

### 2.4 龙虎榜接口（P1）

**影响 Skills**：
- dragon-tiger-list-analyzer

**需要实现的接口**：

```python
# 1. 龙虎榜每日明细
GET /api/cn/special/dragon-tiger/daily
参数: date
返回: 股票代码, 营业部买入/卖出, 净买入等

# 2. 个股龙虎榜
GET /api/cn/special/dragon-tiger/stock/{symbol}
返回: 该股的龙虎榜历史记录

# 3. 营业部统计
GET /api/cn/special/dragon-tiger/broker/stats
参数: window=3d|5d|10d
返回: 营业部上榜次数, 净买入统计

# 4. 机构买卖统计
GET /api/cn/special/dragon-tiger/institution/stats
返回: 机构买卖统计
```

### 2.5 大宗交易接口（P1）

**影响 Skills**：
- block-deal-monitor

**需要实现的接口**：

```python
# 1. 市场统计
GET /api/cn/special/block-deal/market-stats
返回: 大宗交易总额, 溢价/折价比例

# 2. 每日明细
GET /api/cn/special/block-deal/daily
参数: start_date, end_date
返回: 每日大宗交易明细

# 3. 活跃个股
GET /api/cn/special/block-deal/active-stocks
参数: window=1m|3m|6m
返回: 活跃大宗交易个股

# 4. 活跃营业部
GET /api/cn/special/block-deal/active-brokers
参数: window=1m|3m
返回: 活跃营业部排名
```

### 2.6 涨跌停池接口（P1）

**影响 Skills**：
- limit-up-pool-analyzer
- limit-up-limit-down-risk-checker

**需要实现的接口**：

```python
# 1. 涨停池
GET /api/cn/special/limit-up
参数: date
返回: 涨停股列表, 涨停原因

# 2. 跌停池
GET /api/cn/special/limit-down
参数: date
返回: 跌停股列表

# 3. 涨停统计
GET /api/cn/special/limit-up/stats
返回: 连板统计, 封板率等
```

### 2.7 融资融券接口（P1）

**影响 Skills**：
- margin-risk-monitor

**需要实现的接口**：

```python
# 1. 融资融券余额
GET /api/cn/margin/balance
参数: symbol (可选)
返回: 融资余额, 融券余额

# 2. 融资融券明细
GET /api/cn/margin/detail/{symbol}
返回: 融资买入额, 融券卖出量等

# 3. 融资融券标的
GET /api/cn/margin/targets
返回: 融资融券标的列表
```

### 2.8 分红配股接口（P2）

**影响 Skills**：
- dividend-corporate-action-tracker
- high-dividend-strategy

**需要实现的接口**：

```python
# 1. 分红配送
GET /api/cn/dividend/distribution
参数: date (报告期)
返回: 分红方案列表

# 2. 分红提醒
GET /api/cn/dividend/calendar
参数: start_date, end_date
返回: 除权除息日历

# 3. 个股分红历史
GET /api/cn/dividend/history/{symbol}
返回: 分红历史记录
```

---

## 3. 数据源对比分析

### 3.1 理杏仁 API 支持情况

| 数据类型 | 理杏仁支持 | AKShare支持 | 建议 |
|---------|-----------|------------|------|
| 股票基础信息 | ✅ 完整 | ✅ 完整 | 使用理杏仁 |
| 历史行情 | ✅ 完整 | ✅ 完整 | 使用理杏仁 |
| 财务数据 | ✅ 完整 | ✅ 完整 | 使用理杏仁 |
| 估值数据 | ✅ 完整 | ⚠️ 部分 | 使用理杏仁 |
| 宏观数据 | ✅ 完整 | ✅ 完整 | 使用理杏仁 |
| 资金流向 | ❌ 无 | ✅ 完整 | 使用 AKShare |
| 北向资金 | ❌ 无 | ✅ 完整 | 使用 AKShare |
| 龙虎榜 | ❌ 无 | ✅ 完整 | 使用 AKShare |
| 大宗交易 | ❌ 无 | ✅ 完整 | 使用 AKShare |
| 涨跌停 | ❌ 无 | ✅ 完整 | 使用 AKShare |
| 行业板块 | ⚠️ 部分 | ✅ 完整 | 理杏仁+AKShare |
| 融资融券 | ❌ 无 | ✅ 完整 | 使用 AKShare |
| 分红配股 | ⚠️ 部分 | ✅ 完整 | 理杏仁+AKShare |

### 3.2 数据源集成方案

**方案一：双数据源并存**
- 理杏仁：核心财务数据、估值数据、宏观数据
- AKShare：特色数据（资金流、龙虎榜、大宗交易等）
- 优点：数据完整
- 缺点：需要维护两套 Provider

**方案二：单一数据源 + 补充**
- 主数据源：理杏仁
- 补充数据源：AKShare（仅理杏仁不支持的）
- 优点：代码简洁
- 缺点：需要映射和转换

**建议**：采用方案二，优先使用理杏仁，AKShare 作为补充。

---

## 4. 实施计划

### 4.1 阶段一：核心接口补充（Week 1-2）

**目标**：实现 P0 优先级接口

**任务清单**：
1. ✅ 添加 AKShare Provider
2. ⬜ 实现资金流向 API（5个接口）
3. ⬜ 实现北向资金 API（4个接口）
4. ⬜ 实现行业板块 API（4个接口）
5. ⬜ 编写测试用例
6. ⬜ 更新客户端

**预期成果**：
- 新增 13 个 API 接口
- 覆盖率提升至 40%

### 4.2 阶段二：特色数据接口（Week 3-4）

**目标**：实现 P1 优先级接口

**任务清单**：
1. ⬜ 实现龙虎榜 API（4个接口）
2. ⬜ 实现大宗交易 API（4个接口）
3. ⬜ 实现涨跌停池 API（3个接口）
4. ⬜ 实现融资融券 API（3个接口）
5. ⬜ 优化缓存策略
6. ⬜ 性能测试

**预期成果**：
- 新增 14 个 API 接口
- 覆盖率提升至 70%

### 4.3 阶段三：完善与优化（Week 5-6）

**目标**：实现剩余接口 + 优化

**任务清单**：
1. ⬜ 实现分红配股 API
2. ⬜ 实现股权质押 API
3. ⬜ 实现限售解禁 API
4. ⬜ 实现其他特色数据 API
5. ⬜ 添加数据校验
6. ⬜ 文档完善
7. ⬜ 部署上线

**预期成果**：
- 新增 10+ 个 API 接口
- 覆盖率达到 90%+

---

## 5. 技术方案

### 5.1 AKShare Provider 实现

```python
# providers/akshare.py
import akshare as ak
from typing import List, Dict
import pandas as pd

class AKShareProvider:
    """AKShare 数据源提供者"""

    def get_fund_flow_market(self) -> List[dict]:
        """获取大盘资金流"""
        df = ak.stock_market_fund_flow()
        return df.to_dict(orient='records')

    def get_fund_flow_stock(self, symbol: str) -> List[dict]:
        """获取个股资金流"""
        df = ak.stock_individual_fund_flow(stock=symbol, market="sh")
        return df.to_dict(orient='records')

    def get_dragon_tiger_daily(self, date: str) -> List[dict]:
        """获取龙虎榜每日明细"""
        df = ak.stock_lhb_detail_em(date=date)
        return df.to_dict(orient='records')

    # ... 更多方法
```

### 5.2 多数据源路由

```python
# providers/router.py
from typing import List
from .lixinger import LixingerProvider
from .akshare import AKShareProvider

class DataRouter:
    """数据源路由器"""

    def __init__(self, lixinger: LixingerProvider, akshare: AKShareProvider):
        self.lixinger = lixinger
        self.akshare = akshare

    def get_stock_history(self, symbol: str, **kwargs):
        """优先使用理杏仁"""
        return self.lixinger.get_stock_history(symbol, **kwargs)

    def get_fund_flow_market(self):
        """使用 AKShare"""
        return self.akshare.get_fund_flow_market()

    # ... 智能路由逻辑
```

### 5.3 缓存策略优化

```python
# 根据数据类型设置不同的缓存时间
CACHE_STRATEGY = {
    "realtime": 3600,      # 实时数据: 1小时
    "daily": 86400,        # 日线数据: 24小时
    "financial": 604800,   # 财务数据: 7天
    "macro": 86400,        # 宏观数据: 24小时
    "fund_flow": 3600,     # 资金流: 1小时
    "dragon_tiger": 86400, # 龙虎榜: 24小时
    "block_deal": 86400,   # 大宗交易: 24小时
}
```

---

## 6. 风险与挑战

### 6.1 技术风险

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|----------|
| AKShare API 不稳定 | 高 | 中 | 缓存 + 降级 + 多数据源 |
| 数据格式不一致 | 中 | 高 | 标准化层 + 字段映射 |
| 性能瓶颈 | 中 | 中 | 缓存 + 异步 + 分页 |
| Token 限制 | 低 | 低 | 配额管理 |

### 6.2 数据质量

| 问题 | 影响 | 解决方案 |
|------|------|----------|
| 数据源延迟 | 中 | 标注数据时间戳 |
| 数据缺失 | 中 | 多数据源互补 |
| 数据错误 | 高 | 数据校验 + 监控告警 |

---

## 7. 成功指标

### 7.1 量化指标

| 指标 | 当前 | 目标 |
|------|------|------|
| API 接口数量 | 11 | 38+ |
| Skills 覆盖率 | 15% | 90%+ |
| 平均响应时间 | <200ms | <300ms |
| 缓存命中率 | 80% | 85%+ |
| 测试覆盖率 | 0% | 80%+ |

### 7.2 质量指标

- ✅ 所有接口有完整的 API 文档
- ✅ 所有接口有测试用例
- ✅ 错误处理完善
- ✅ 性能满足要求
- ✅ 文档完整

---

## 8. 下一步行动

### 8.1 立即行动（本周）

1. **添加 AKShare Provider**
   - 实现 `providers/akshare.py`
   - 添加基础方法

2. **实现资金流向 API**
   - 5个接口
   - 测试验证

3. **实现北向资金 API**
   - 4个接口
   - 测试验证

### 8.2 短期计划（2周内）

1. 实现行业板块 API
2. 实现龙虎榜 API
3. 实现大宗交易 API
4. 完善文档

### 8.3 中期计划（1个月内）

1. 实现所有 P1/P2 优先级接口
2. 性能优化
3. 全面测试
4. 部署上线

---

## 9. 附录

### 9.1 Skills 详细依赖列表

见 `skills_analysis.json`

### 9.2 API 接口完整列表

见 `/docs/FINDATA_SERVICE_DESIGN.md`

### 9.3 数据源对比表

见第3节

---

**文档版本**: v1.0
**更新时间**: 2026-02-19
**维护者**: 开发团队
