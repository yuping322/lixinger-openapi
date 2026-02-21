# 市场热度排名数据获取完整指南

## 📊 问题说明

理杏仁免费版**不提供**以下数据：
- 热度数据 (hot-data API)
- 资金流向 (fund-flow API)

这些数据需要付费订阅或使用其他数据源。

---

## ✅ 当前可用的替代方案

### 方案1: 使用现有数据进行情绪分析（已实现）

我们已经实现了基于可用数据的情绪分析系统，使用以下指标：

| 指标 | 数据源 | 说明 |
|------|--------|------|
| 成交量变化 | K线数据 | 反映市场活跃度和关注度 |
| 股东人数变化 | 股东人数接口 | 反映筹码集中度（散户vs机构） |
| 公告频率 | 公告接口 | 反映公司动作和市场关注度 |
| 价格波动率 | K线数据 | 反映情绪强度和市场分歧 |

**使用方法**:
```bash
python3 market_sentiment_analysis_600519.py
```

**优点**:
- ✅ 完全基于理杏仁免费数据
- ✅ 无需额外配置
- ✅ 提供综合情绪评分（0-100）
- ✅ 包含交叉验证和矛盾分析

**局限**:
- ❌ 无法获取真实的热度排名数据
- ❌ 无法获取资金流向详细数据
- ❌ 股东人数数据更新频率低（季度）

---

### 方案2: 使用AKShare获取热度数据（推荐）

AKShare是开源免费的金融数据接口库，提供丰富的市场热度数据。

#### 安装AKShare

```bash
pip install akshare
```

#### 可用的热度相关接口

##### 1. 东方财富人气榜

```python
import akshare as ak

# 个股人气榜
popularity = ak.stock_hot_rank_em()
print(popularity.head())

# 字段说明:
# - 序号: 排名
# - 股票代码: 代码
# - 股票名称: 名称
# - 最新价: 当前价格
# - 涨跌幅: 涨跌幅
# - 人气: 人气值
```

##### 2. 雪球热度榜

```python
# 雪球热股榜
xueqiu_hot = ak.stock_hot_rank_xq()
print(xueqiu_hot.head())

# 字段说明:
# - 股票代码
# - 股票名称
# - 当前价
# - 涨跌幅
# - 关注度
```

##### 3. 百度股市通热度

```python
# 百度股市通热度
baidu_hot = ak.stock_hot_rank_baidu()
print(baidu_hot.head())
```

##### 4. 同花顺热度

```python
# 同花顺热度榜
ths_hot = ak.stock_hot_rank_ths()
print(ths_hot.head())
```

##### 5. 资金流向数据

```python
# 个股资金流向
fund_flow = ak.stock_individual_fund_flow_rank(indicator="今日")
print(fund_flow.head())

# 字段说明:
# - 序号
# - 代码
# - 名称
# - 最新价
# - 今日涨跌幅
# - 今日主力净流入-净额
# - 今日主力净流入-净占比
# - 今日超大单净流入-净额
# - 今日超大单净流入-净占比
# - 今日大单净流入-净额
# - 今日大单净流入-净占比
# - 今日中单净流入-净额
# - 今日中单净流入-净占比
# - 今日小单净流入-净额
# - 今日小单净流入-净占比
```

##### 6. 龙虎榜数据

```python
# 龙虎榜每日统计
lhb_daily = ak.stock_lhb_detail_daily_sina(date="20260221")
print(lhb_daily.head())

# 个股龙虎榜明细
lhb_detail = ak.stock_lhb_detail_em(symbol="600519")
print(lhb_detail.head())
```

#### 完整示例脚本

```python
#!/usr/bin/env python3
"""
使用AKShare获取市场热度数据
"""
import akshare as ak
import pandas as pd
from datetime import datetime

def get_hot_rank_data():
    """获取多个平台的热度排名"""
    print("=" * 80)
    print("市场热度排名数据汇总")
    print(f"获取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()
    
    # 1. 东方财富人气榜
    print("📊 东方财富人气榜 Top 10")
    print("-" * 80)
    try:
        em_hot = ak.stock_hot_rank_em()
        print(em_hot.head(10).to_string(index=False))
    except Exception as e:
        print(f"❌ 获取失败: {e}")
    print()
    
    # 2. 资金流向排名
    print("💰 今日主力资金流向 Top 10")
    print("-" * 80)
    try:
        fund_flow = ak.stock_individual_fund_flow_rank(indicator="今日")
        print(fund_flow.head(10)[['序号', '代码', '名称', '最新价', 
                                   '今日涨跌幅', '今日主力净流入-净额', 
                                   '今日主力净流入-净占比']].to_string(index=False))
    except Exception as e:
        print(f"❌ 获取失败: {e}")
    print()
    
    # 3. 查询特定股票
    stock_code = "600519"
    print(f"🔍 查询 {stock_code} 在各榜单中的排名")
    print("-" * 80)
    
    # 在东方财富人气榜中查找
    try:
        em_hot = ak.stock_hot_rank_em()
        stock_rank = em_hot[em_hot['股票代码'] == stock_code]
        if not stock_rank.empty:
            print(f"东方财富人气榜排名: 第 {stock_rank.iloc[0]['序号']} 名")
            print(f"人气值: {stock_rank.iloc[0]['人气']}")
        else:
            print(f"未在东方财富人气榜 Top 100 中")
    except Exception as e:
        print(f"❌ 查询失败: {e}")
    
    # 在资金流向榜中查找
    try:
        fund_flow = ak.stock_individual_fund_flow_rank(indicator="今日")
        stock_flow = fund_flow[fund_flow['代码'] == stock_code]
        if not stock_flow.empty:
            print(f"资金流向排名: 第 {stock_flow.iloc[0]['序号']} 名")
            print(f"主力净流入: {stock_flow.iloc[0]['今日主力净流入-净额']} 万元")
            print(f"主力净流入占比: {stock_flow.iloc[0]['今日主力净流入-净占比']}%")
        else:
            print(f"未在资金流向榜 Top 100 中")
    except Exception as e:
        print(f"❌ 查询失败: {e}")
    
    print()
    print("=" * 80)

if __name__ == "__main__":
    get_hot_rank_data()
```

**保存为**: `get_hot_rank_akshare.py`

**运行**:
```bash
python3 get_hot_rank_akshare.py
```

---

### 方案3: 使用Tushare（需要积分）

Tushare是另一个流行的金融数据接口，提供更专业的数据。

#### 注册与配置

1. 访问 https://tushare.pro/register
2. 注册账号并获取token
3. 配置token:

```python
import tushare as ts
ts.set_token('your-token-here')
pro = ts.pro_api()
```

#### 可用接口

```python
# 龙虎榜数据
lhb = pro.top_list(trade_date='20260221')

# 每日指标（包含换手率、成交额等）
daily = pro.daily(ts_code='600519.SH', start_date='20260101', end_date='20260221')

# 资金流向
money_flow = pro.moneyflow(ts_code='600519.SH', start_date='20260101', end_date='20260221')
```

**注意**: Tushare需要积分才能访问某些接口，新用户有120积分。

---

### 方案4: 升级理杏仁订阅

如果需要完整的理杏仁数据，可以考虑升级订阅。

#### 理杏仁订阅计划

访问: https://www.lixinger.com/pricing

**个人版**:
- 价格: ¥199/月 或 ¥1,999/年
- 包含: 所有API接口，包括热度数据、资金流向等

**专业版**:
- 价格: ¥499/月 或 ¥4,999/年
- 包含: 更高的API调用频率和更多高级功能

#### 升级后可用的接口

```python
# 热度数据
hot_data = query_json('cn/company/hot-data', {
    'stockCodes': ['600519']
})

# 资金流向
fund_flow = query_json('cn/company/fund-flow', {
    'stockCodes': ['600519']
})

# 估值指标
valuation = query_json('cn/company/valuation', {
    'stockCodes': ['600519']
})
```

---

## 🎯 推荐方案对比

| 方案 | 成本 | 数据质量 | 易用性 | 推荐度 |
|------|------|---------|--------|--------|
| 方案1: 现有数据分析 | 免费 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 方案2: AKShare | 免费 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 方案3: Tushare | 免费/付费 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 方案4: 理杏仁付费 | ¥199+/月 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

### 推荐策略

**个人投资者/学习用途**:
- 使用 **方案1 + 方案2** 组合
- 免费且数据充足
- AKShare提供多平台热度数据

**专业投资者/机构**:
- 使用 **方案3 (Tushare)** 或 **方案4 (理杏仁付费)**
- 数据质量更高，更新更及时
- API稳定性更好

**开发者/量化研究**:
- 使用 **方案2 (AKShare)** 进行原型开发
- 生产环境切换到 **方案3** 或 **方案4**

---

## 🔧 集成AKShare到现有系统

### 步骤1: 安装依赖

```bash
pip install akshare
```

### 步骤2: 创建AKShare数据提供者

创建文件: `findata-service/providers/akshare_provider.py`

```python
"""
AKShare数据提供者
提供热度、资金流向等理杏仁免费版不支持的数据
"""
import akshare as ak
from typing import Dict, List, Optional
import pandas as pd

class AKShareProvider:
    """AKShare数据提供者"""
    
    def get_hot_rank(self, source: str = "em") -> pd.DataFrame:
        """
        获取热度排名
        
        Args:
            source: 数据源 (em=东方财富, xq=雪球, baidu=百度, ths=同花顺)
        """
        if source == "em":
            return ak.stock_hot_rank_em()
        elif source == "xq":
            return ak.stock_hot_rank_xq()
        elif source == "baidu":
            return ak.stock_hot_rank_baidu()
        elif source == "ths":
            return ak.stock_hot_rank_ths()
        else:
            raise ValueError(f"Unsupported source: {source}")
    
    def get_fund_flow(self, indicator: str = "今日") -> pd.DataFrame:
        """
        获取资金流向排名
        
        Args:
            indicator: 时间范围 (今日, 3日, 5日, 10日)
        """
        return ak.stock_individual_fund_flow_rank(indicator=indicator)
    
    def get_stock_fund_flow(self, symbol: str) -> pd.DataFrame:
        """
        获取个股资金流向历史
        
        Args:
            symbol: 股票代码 (如 600519)
        """
        return ak.stock_individual_fund_flow(stock=symbol, market="sh")
    
    def get_lhb_daily(self, date: str) -> pd.DataFrame:
        """
        获取龙虎榜每日统计
        
        Args:
            date: 日期 (格式: YYYYMMDD)
        """
        return ak.stock_lhb_detail_daily_sina(date=date)
    
    def get_lhb_detail(self, symbol: str) -> pd.DataFrame:
        """
        获取个股龙虎榜明细
        
        Args:
            symbol: 股票代码 (如 600519)
        """
        return ak.stock_lhb_detail_em(symbol=symbol)
```

### 步骤3: 添加API端点

在 `findata-service/routes/cn/` 下创建 `hot_rank.py`:

```python
"""
热度排名相关API端点
"""
from fastapi import APIRouter, Query
from providers.akshare_provider import AKShareProvider

router = APIRouter()
akshare = AKShareProvider()

@router.get("/hot-rank")
async def get_hot_rank(
    source: str = Query("em", description="数据源: em, xq, baidu, ths")
):
    """获取热度排名"""
    try:
        df = akshare.get_hot_rank(source)
        return {
            "code": 1,
            "message": "success",
            "data": df.to_dict(orient="records")
        }
    except Exception as e:
        return {
            "code": 0,
            "message": str(e),
            "data": []
        }

@router.get("/fund-flow/rank")
async def get_fund_flow_rank(
    indicator: str = Query("今日", description="时间范围: 今日, 3日, 5日, 10日")
):
    """获取资金流向排名"""
    try:
        df = akshare.get_fund_flow(indicator)
        return {
            "code": 1,
            "message": "success",
            "data": df.to_dict(orient="records")
        }
    except Exception as e:
        return {
            "code": 0,
            "message": str(e),
            "data": []
        }

@router.get("/stock/{symbol}/fund-flow")
async def get_stock_fund_flow(symbol: str):
    """获取个股资金流向历史"""
    try:
        df = akshare.get_stock_fund_flow(symbol)
        return {
            "code": 1,
            "message": "success",
            "data": df.to_dict(orient="records")
        }
    except Exception as e:
        return {
            "code": 0,
            "message": str(e),
            "data": []
        }
```

### 步骤4: 注册路由

在 `findata-service/server.py` 中添加:

```python
from routes.cn import hot_rank

app.include_router(hot_rank.router, prefix="/api/cn", tags=["热度排名"])
```

### 步骤5: 测试

```bash
# 启动服务
python findata-service/server.py

# 测试热度排名
curl "http://localhost:8000/api/cn/hot-rank?source=em"

# 测试资金流向
curl "http://localhost:8000/api/cn/fund-flow/rank?indicator=今日"

# 测试个股资金流向
curl "http://localhost:8000/api/cn/stock/600519/fund-flow"
```

---

## 📚 相关文档

- **AKShare官方文档**: https://akshare.akfamily.xyz/
- **Tushare官方文档**: https://tushare.pro/document/2
- **理杏仁定价**: https://www.lixinger.com/pricing
- **当前情绪分析脚本**: `market_sentiment_analysis_600519.py`

---

## 💡 最佳实践

### 1. 数据源选择

- **实时性要求高**: 使用AKShare（免费）或理杏仁付费版
- **历史数据分析**: 使用Tushare或理杏仁
- **成本敏感**: 使用AKShare + 现有理杏仁免费数据

### 2. 数据缓存

```python
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=128)
def get_hot_rank_cached(date: str):
    """带缓存的热度排名获取"""
    return ak.stock_hot_rank_em()

# 每小时更新一次
cache_time = datetime.now().replace(minute=0, second=0, microsecond=0)
hot_rank = get_hot_rank_cached(cache_time.isoformat())
```

### 3. 错误处理

```python
def safe_get_hot_rank(source="em", retry=3):
    """带重试的热度排名获取"""
    for i in range(retry):
        try:
            return ak.stock_hot_rank_em()
        except Exception as e:
            if i == retry - 1:
                raise
            time.sleep(1)
```

### 4. 数据验证

```python
def validate_hot_rank_data(df):
    """验证热度排名数据完整性"""
    required_columns = ['股票代码', '股票名称', '人气']
    if not all(col in df.columns for col in required_columns):
        raise ValueError("数据格式不正确")
    
    if df.empty:
        raise ValueError("数据为空")
    
    return True
```

---

## 🎯 总结

1. **理杏仁免费版不提供热度和资金流向数据**
2. **推荐使用AKShare作为免费替代方案**
3. **已实现基于可用数据的情绪分析系统**
4. **可以集成AKShare到findata-service获取完整数据**
5. **专业用户可考虑升级理杏仁订阅或使用Tushare**

---

**文档版本**: 1.0  
**更新时间**: 2026-02-21  
**维护者**: Kiro AI
