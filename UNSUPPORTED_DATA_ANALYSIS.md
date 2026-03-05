# 不支持数据分析报告

**分析日期**: 2026-02-27  
**数据来源**: 理杏仁API + AKShare

---

## 执行摘要

根据对所有Skills的data-queries文档分析，不支持的数据可分为三类：

| 类别 | 数量 | 占比 | 可行性 |
|------|------|------|--------|
| **可通过二次计算获得** | ~15项 | 40% | ✅ 高 |
| **可通过AKShare获得** | ~12项 | 32% | ✅ 中 |
| **确实无法获得** | ~10项 | 27% | ❌ 低 |

---

## 一、可通过二次计算获得的数据

这些数据可以基于理杏仁API返回的原始数据进行计算得到。

### 1.1 估值衍生指标

#### PCF (市现率)
- **原始数据**: 市值(mc) + 经营现金流(q.cfs.ncf_oa.t)
- **计算公式**: `PCF = 市值 / 经营现金流`
- **AKShare对应**: 无直接接口，需计算
- **实现难度**: ⭐ 简单

```python
# 示例代码
mc = fundamental_data['mc']  # 市值
cash_flow = fs_data['q.cfs.ncf_oa.t']  # 经营现金流
pcf = mc / cash_flow
```

#### EV/EBITDA (企业价值倍数)
- **原始数据**: 市值(mc) + 总负债(q.bs.tl.t) + 现金(q.bs.c.t) + EBITDA
- **计算公式**: 
  - `EV = 市值 + 总负债 - 现金`
  - `EBITDA = 营业利润 + 折旧摊销`
  - `EV/EBITDA = EV / EBITDA`
- **AKShare对应**: 需要多个接口组合
- **实现难度**: ⭐⭐ 中等

```python
# 示例代码
ev = mc + total_debt - cash
ebitda = operating_profit + depreciation
ev_ebitda = ev / ebitda
```

### 1.2 风险指标

#### Beta (系统风险)
- **原始数据**: 个股历史价格 + 指数历史价格
- **计算公式**: `Beta = Cov(股票收益率, 市场收益率) / Var(市场收益率)`
- **AKShare对应**: `stock_zh_a_hist()` + `index_zh_a_hist()`
- **实现难度**: ⭐⭐ 中等

```python
# 示例代码
import numpy as np
stock_returns = stock_prices.pct_change()
market_returns = index_prices.pct_change()
beta = np.cov(stock_returns, market_returns)[0,1] / np.var(market_returns)
```

#### 波动率 (Volatility)
- **原始数据**: 历史价格数据
- **计算公式**: `σ = std(收益率) * √252`
- **AKShare对应**: `stock_zh_a_hist()`
- **实现难度**: ⭐ 简单

```python
# 示例代码
returns = prices.pct_change()
volatility = returns.std() * np.sqrt(252)  # 年化波动率
```

#### 相关性矩阵
- **原始数据**: 多只股票的历史价格
- **计算公式**: `Corr(股票A, 股票B)`
- **AKShare对应**: `stock_zh_a_hist()`
- **实现难度**: ⭐ 简单

```python
# 示例代码
returns = prices.pct_change()
correlation_matrix = returns.corr()
```

### 1.3 财务比率

#### 流动比率、速动比率
- **原始数据**: 资产负债表数据
- **计算公式**: 
  - `流动比率 = 流动资产 / 流动负债`
  - `速动比率 = (流动资产 - 存货) / 流动负债`
- **AKShare对应**: `stock_financial_analysis_indicator()`
- **实现难度**: ⭐ 简单

#### 资产负债率、权益乘数
- **原始数据**: 资产负债表数据
- **计算公式**: 
  - `资产负债率 = 总负债 / 总资产`
  - `权益乘数 = 总资产 / 股东权益`
- **AKShare对应**: `stock_financial_analysis_indicator()`
- **实现难度**: ⭐ 简单

### 1.4 集中度指标

#### HHI指数 (赫芬达尔指数)
- **原始数据**: 持仓权重列表
- **计算公式**: `HHI = Σ(权重²)`
- **AKShare对应**: 无需，本地计算
- **实现难度**: ⭐ 简单

```python
# 示例代码
weights = [0.3, 0.25, 0.2, 0.15, 0.1]
hhi = sum([w**2 for w in weights])
effective_holdings = 1 / hhi
```

#### 有效持仓数
- **原始数据**: HHI指数
- **计算公式**: `有效持仓数 = 1 / HHI`
- **AKShare对应**: 无需，本地计算
- **实现难度**: ⭐ 简单

### 1.5 VaR (风险价值)

#### 历史模拟法VaR
- **原始数据**: 历史收益率数据
- **计算公式**: `VaR = Percentile(收益率, 5%)`
- **AKShare对应**: `stock_zh_a_hist()`
- **实现难度**: ⭐⭐ 中等

```python
# 示例代码
portfolio_returns = ...  # 组合历史收益率
var_95 = np.percentile(portfolio_returns, 5)  # 95% VaR
cvar_95 = portfolio_returns[portfolio_returns <= var_95].mean()  # CVaR
```

---

## 二、可通过AKShare获得的数据

这些数据理杏仁API不提供，但AKShare有对应接口。

### 2.1 市场行情数据

#### 实时行情
- **理杏仁**: 不支持实时数据
- **AKShare**: ✅ `stock_zh_a_spot_em()` - 实时行情
- **实现难度**: ⭐ 简单

```python
import akshare as ak
spot_data = ak.stock_zh_a_spot_em()
```

#### 分钟级K线
- **理杏仁**: 不支持分钟数据
- **AKShare**: ✅ `stock_zh_a_hist_min_em()` - 分钟K线
- **实现难度**: ⭐ 简单

```python
minute_data = ak.stock_zh_a_hist_min_em(
    symbol="600519",
    period="1",  # 1分钟
    adjust="qfq"
)
```

### 2.2 资金流向数据

#### 个股资金流向
- **理杏仁**: 不支持
- **AKShare**: ✅ `stock_individual_fund_flow()` - 个股资金流
- **实现难度**: ⭐ 简单

```python
fund_flow = ak.stock_individual_fund_flow(stock="600519", market="sh")
```

#### 行业资金流向
- **理杏仁**: 不支持
- **AKShare**: ✅ `stock_sector_fund_flow_rank()` - 行业资金流
- **实现难度**: ⭐ 简单

```python
sector_flow = ak.stock_sector_fund_flow_rank(indicator="今日")
```

### 2.3 龙虎榜数据

#### 龙虎榜明细
- **理杏仁**: 不支持
- **AKShare**: ✅ `stock_lhb_detail_em()` - 龙虎榜明细
- **实现难度**: ⭐ 简单

```python
lhb_data = ak.stock_lhb_detail_em(date="20260227")
```

#### 营业部统计
- **理杏仁**: 不支持
- **AKShare**: ✅ `stock_lhb_yybph_em()` - 营业部排行
- **实现难度**: ⭐ 简单

### 2.4 热度数据

#### 股票热度排名
- **理杏仁**: 有 `cn/company/hot/tr_dri` 但需要提供stockCodes
- **AKShare**: ✅ `stock_hot_rank_em()` - 全市场热度排名
- **实现难度**: ⭐ 简单

```python
hot_rank = ak.stock_hot_rank_em()
```

#### 概念板块热度
- **理杏仁**: 不支持
- **AKShare**: ✅ `stock_board_concept_name_em()` - 概念板块
- **实现难度**: ⭐ 简单

### 2.5 新闻舆情数据

#### 个股新闻
- **理杏仁**: 不支持
- **AKShare**: ✅ `stock_news_em()` - 个股新闻
- **实现难度**: ⭐ 简单

```python
news = ak.stock_news_em(symbol="600519")
```

#### 公告数据
- **理杏仁**: 不支持
- **AKShare**: ✅ `stock_notice_report()` - 公告查询
- **实现难度**: ⭐ 简单

### 2.6 转债数据

#### 可转债行情
- **理杏仁**: 不支持
- **AKShare**: ✅ `bond_zh_hs_cov_spot()` - 可转债实时
- **实现难度**: ⭐ 简单

```python
convertible_bonds = ak.bond_zh_hs_cov_spot()
```

#### 转债转股价
- **理杏仁**: 不支持
- **AKShare**: ✅ `bond_cov_comparison()` - 转债对比
- **实现难度**: ⭐ 简单

### 2.7 期权数据

#### 期权行情
- **理杏仁**: 不支持
- **AKShare**: ✅ `option_finance_board()` - 期权行情
- **实现难度**: ⭐⭐ 中等

### 2.8 宏观数据补充

#### 更多宏观指标
- **理杏仁**: 有限的宏观数据
- **AKShare**: ✅ 丰富的宏观数据接口
  - `macro_china_cpi()` - CPI
  - `macro_china_ppi()` - PPI
  - `macro_china_pmi()` - PMI
  - `macro_china_gdp()` - GDP
  - `macro_china_money_supply()` - 货币供应
- **实现难度**: ⭐ 简单

---

## 三、确实无法获得的数据

这些数据既无法从理杏仁获得，也无法从AKShare获得，需要付费数据源或专业系统。

### 3.1 分析师数据

#### 分析师目标价
- **理杏仁**: ❌ 不支持
- **AKShare**: ❌ 不支持
- **替代方案**: 
  - 付费数据源：Wind、Bloomberg、FactSet
  - 券商研报爬虫（合规性问题）
- **实现难度**: ⭐⭐⭐⭐ 困难

#### 分析师盈利预测
- **理杏仁**: ❌ 不支持
- **AKShare**: ❌ 不支持
- **替代方案**: 同上
- **实现难度**: ⭐⭐⭐⭐ 困难

#### 分析师评级
- **理杏仁**: ❌ 不支持
- **AKShare**: ⚠️ 部分支持 `stock_analyst_rank_em()`
- **实现难度**: ⭐⭐⭐ 中等

### 3.2 机构持仓数据

#### 外资持仓明细（非港股通）
- **理杏仁**: ❌ 不支持
- **AKShare**: ❌ 不支持
- **替代方案**: 
  - QFII/RQFII季报披露
  - 付费数据源
- **实现难度**: ⭐⭐⭐⭐ 困难

#### 私募持仓数据
- **理杏仁**: ❌ 不支持
- **AKShare**: ❌ 不支持
- **替代方案**: 
  - 季报披露（滞后）
  - 付费数据源
- **实现难度**: ⭐⭐⭐⭐⭐ 非常困难

### 3.3 高频数据

#### 逐笔成交数据
- **理杏仁**: ❌ 不支持
- **AKShare**: ⚠️ 部分支持 `stock_zh_a_tick_tx()`（腾讯源，不稳定）
- **替代方案**: 
  - 券商Level-2数据
  - 交易所数据
- **实现难度**: ⭐⭐⭐⭐ 困难

#### 盘口数据（买卖五档）
- **理杏仁**: ❌ 不支持
- **AKShare**: ⚠️ 实时接口不稳定
- **替代方案**: 
  - 券商Level-2数据
  - 付费行情源
- **实现难度**: ⭐⭐⭐⭐ 困难

### 3.4 另类数据

#### 卫星图像数据
- **理杏仁**: ❌ 不支持
- **AKShare**: ❌ 不支持
- **替代方案**: 
  - 专业卫星数据提供商
  - 遥感数据平台
- **实现难度**: ⭐⭐⭐⭐⭐ 非常困难

#### 信用卡消费数据
- **理杏仁**: ❌ 不支持
- **AKShare**: ❌ 不支持
- **替代方案**: 
  - 银联数据（需授权）
  - 第三方支付数据
- **实现难度**: ⭐⭐⭐⭐⭐ 非常困难

### 3.5 风险模型数据

#### Barra风险因子
- **理杏仁**: ❌ 不支持
- **AKShare**: ❌ 不支持
- **替代方案**: 
  - MSCI Barra订阅
  - 自建风险模型（简化版）
- **实现难度**: ⭐⭐⭐⭐ 困难

#### 行业风险因子
- **理杏仁**: ❌ 不支持
- **AKShare**: ❌ 不支持
- **替代方案**: 
  - 自建风险模型
  - 学术研究数据
- **实现难度**: ⭐⭐⭐ 中等

### 3.6 衍生品数据

#### 期权隐含波动率
- **理杏仁**: ❌ 不支持
- **AKShare**: ⚠️ 部分支持（需计算）
- **替代方案**: 
  - 期权行情 + Black-Scholes计算
  - 付费数据源
- **实现难度**: ⭐⭐⭐ 中等

#### 期权希腊字母
- **理杏仁**: ❌ 不支持
- **AKShare**: ❌ 不支持
- **替代方案**: 
  - 自行计算（需要期权定价模型）
  - 付费数据源
- **实现难度**: ⭐⭐⭐ 中等

---

## 四、实施建议

### 4.1 短期方案（1-2周）

**优先实现可计算的指标**:
1. ✅ Beta、波动率、相关性矩阵
2. ✅ 财务比率（流动比率、资产负债率等）
3. ✅ 集中度指标（HHI、有效持仓数）
4. ✅ VaR计算

**实施步骤**:
```python
# 创建计算工具库
# skills/lixinger-data-query/utils/calculations.py

def calculate_beta(stock_returns, market_returns):
    """计算Beta"""
    pass

def calculate_volatility(returns, window=252):
    """计算波动率"""
    pass

def calculate_correlation_matrix(returns_df):
    """计算相关性矩阵"""
    pass

def calculate_hhi(weights):
    """计算HHI指数"""
    pass

def calculate_var(returns, confidence=0.95):
    """计算VaR"""
    pass
```

### 4.2 中期方案（1个月）

**集成AKShare补充数据**:
1. ✅ 实时行情、分钟K线
2. ✅ 资金流向数据
3. ✅ 龙虎榜数据
4. ✅ 热度排名
5. ✅ 新闻公告

**实施步骤**:
```python
# 创建AKShare数据适配器
# skills/lixinger-data-query/adapters/akshare_adapter.py

class AKShareAdapter:
    def get_realtime_quotes(self, stock_codes):
        """获取实时行情"""
        pass
    
    def get_fund_flow(self, stock_code):
        """获取资金流向"""
        pass
    
    def get_hot_rank(self):
        """获取热度排名"""
        pass
```

### 4.3 长期方案（3个月）

**构建数据增强系统**:
1. ⚠️ 简化风险模型（自建）
2. ⚠️ 新闻情感分析（NLP）
3. ⚠️ 期权定价模型
4. ❌ 付费数据源接入（可选）

---

## 五、成本效益分析

### 5.1 免费方案（理杏仁 + AKShare + 计算）

**覆盖率**: ~85%  
**成本**: 0元  
**优点**:
- 无额外成本
- 数据质量可靠
- 满足大部分分析需求

**缺点**:
- 缺少分析师数据
- 缺少高频数据
- 缺少另类数据

### 5.2 混合方案（免费 + 部分付费）

**覆盖率**: ~95%  
**成本**: 5,000-20,000元/年  
**建议付费项**:
- Wind/Bloomberg终端（分析师数据）
- Level-2行情（高频数据）

### 5.3 完整方案（全付费）

**覆盖率**: ~99%  
**成本**: 50,000-200,000元/年  
**适用场景**: 专业机构、量化团队

---

## 六、总结

### 可行性评估

| 数据类别 | 可行性 | 推荐方案 |
|---------|-------|---------|
| 估值衍生指标 | ✅ 高 | 二次计算 |
| 风险指标 | ✅ 高 | 二次计算 |
| 财务比率 | ✅ 高 | 二次计算 |
| 市场行情 | ✅ 高 | AKShare |
| 资金流向 | ✅ 高 | AKShare |
| 龙虎榜 | ✅ 高 | AKShare |
| 新闻舆情 | ✅ 中 | AKShare |
| 分析师数据 | ❌ 低 | 付费数据源 |
| 高频数据 | ❌ 低 | 付费数据源 |
| 另类数据 | ❌ 低 | 专业提供商 |

### 推荐实施路径

**阶段1（立即）**: 实现所有可计算指标  
**阶段2（1周内）**: 集成AKShare补充数据  
**阶段3（1个月内）**: 构建简化风险模型  
**阶段4（按需）**: 接入付费数据源

---

**更新日期**: 2026-02-27  
**版本**: v1.0.0  
**作者**: Kiro AI Assistant
