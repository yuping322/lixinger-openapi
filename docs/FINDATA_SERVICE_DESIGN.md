# Findata Service 统一设计文档

## 文档信息

- **版本**: v1.0
- **日期**: 2026-02-19
- **目标**: 将三个市场 (China/US/HK) 的 findata-toolkit 统一为一个微服务架构

---

## 1. 项目背景与目标

### 1.1 现状分析

#### 1.1.1 架构问题

**重复建设**：
```
skills/
├── China-market/findata-toolkit-cn/  (59个views)
├── US-market/findata-toolkit-us/     (复制代码)
└── HK-market/findata-toolkit-hk/     (复制代码)
    └── findata-toolkit-cn/           (嵌套重复)
```

**调用混乱**：
- ❌ `views_runner.py` (legacy，有依赖问题)
- ❌ `toolkit.py --skill` (新方式，但不完整)
- ❌ AKShare 直接调用 (分散在各处)
- ❌ 理杏仁 API 聚合 (没有统一封装)

**耦合严重**：
- 每个 skill 依赖复杂的 toolkit 内部结构
- 93 个 `data-queries.md` 引用过时的命令
- Skills 无法独立运行

#### 1.1.2 数据源现状

**中国市场**：
- 理杏仁 API (主要): 财务、估值、行情
- AKShare (补充): 资金流、龙虎榜、大宗交易等
- 新浪/东方财富/百度股市通 (补充)

**美国市场**：
- 目前主要是框架代码
- 需要集成 Yahoo Finance, Alpha Vantage 等

**香港市场**：
- 目前主要是框架代码
- 需要集成港股数据源

### 1.2 目标架构

#### 1.2.1 设计原则

1. **微服务化**: 数据服务与技能层解耦
2. **统一接口**: 一套 API 覆盖多市场多数据源
3. **故障切换**: 多数据源自动切换
4. **简单易用**: Skills 只需轻量级客户端

#### 1.2.2 架构图

```
┌─────────────────────────────────────────────────────────┐
│  Skills Layer (业务层)                                  │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │ dividend-tracker│  │ macro-monitor   │              │
│  │  ├─ skill.md    │  │  ├─ skill.md    │              │
│  │  ├─ data-queries│  │  ├─ data-queries│              │
│  │  └─ client.py   │  │  └─ client.py   │              │
│  └─────────────────┘  └─────────────────┘              │
└─────────────────────────────────────────────────────────┘
                        ↓ HTTP/REST API
┌─────────────────────────────────────────────────────────┐
│  Findata Service (统一数据服务)                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  FastAPI Server (Port 8000)                      │  │
│  ├──────────────────────────────────────────────────┤  │
│  │  Routes:                                         │  │
│  │  ├─ /api/cn/*   (中国市场)                       │  │
│  │  ├─ /api/us/*   (美国市场)                       │  │
│  │  └─ /api/hk/*   (香港市场)                       │  │
│  ├──────────────────────────────────────────────────┤  │
│  │  Providers (数据源抽象层):                        │  │
│  │  ├─ LixingerProvider                             │  │
│  │  ├─ AKShareProvider                              │  │
│  │  ├─ SinaProvider                                 │  │
│  │  ├─ EastmoneyProvider                            │  │
│  │  └─ CacheLayer (缓存层)                          │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  External Data Sources                                  │
│  ├─ Lixinger API (理杏仁)                              │
│  ├─ AKShare (开源金融数据库)                            │
│  ├─ Sina/EF/Eastmoney (财经网站)                       │
│  └─ Yahoo/Alpha Vantage (海外市场)                     │
└─────────────────────────────────────────────────────────┘
```

---

## 2. API 接口设计规范

### 2.1 统一响应格式

```json
{
  "code": 1,
  "message": "success",
  "data": [...],
  "meta": {
    "source": "lixinger",
    "cached": true,
    "timestamp": "2026-02-19T10:30:00Z",
    "count": 100
  },
  "warnings": [],
  "errors": []
}
```

### 2.2 中国市场 API (China Market)

#### 2.2.1 股票数据 `/api/cn/stock`

**基础信息**
```http
GET /api/cn/stock/{symbol}/basic
```

**历史行情**
```http
GET /api/cn/stock/{symbol}/history
  ?interval=day
  &start_date=2024-01-01
  &end_date=2024-12-31
  &adjust=hfq
```

**实时行情**
```http
GET /api/cn/stock/{symbol}/realtime
```

**财务报表**
```http
GET /api/cn/stock/{symbol}/financial
  ?statement_type=balance_sheet|income|cash_flow
  &limit=5
```

**估值指标**
```http
GET /api/cn/stock/{symbol}/valuation
  ?metrics=pe_ttm,pb,ps,pcf
```

#### 2.2.2 市场数据 `/api/cn/market`

**市场概览**
```http
GET /api/cn/market/overview
```

**行业板块**
```http
GET /api/cn/market/industry
GET /api/cn/market/industry/{industry_code}/stocks
```

**概念板块**
```http
GET /api/cn/market/concept
GET /api/cn/market/concept/{concept_code}/stocks
```

#### 2.2.3 资金流向 `/api/cn/flow`

**市场资金流**
```http
GET /api/cn/flow/market
```

**个股资金流**
```http
GET /api/cn/flow/stock/{symbol}
```

**主力资金排名**
```http
GET /api/cn/flow/rank
  ?indicator=today|3d|5d|10d
  &limit=50
```

#### 2.2.4 特殊数据 `/api/cn/special`

**龙虎榜**
```http
GET /api/cn/special/dragon-tiger
  ?date=2024-01-01
```

**大宗交易**
```http
GET /api/cn/special/block-deal
  ?start_date=2024-01-01
  &end_date=2024-01-31
```

**北向资金**
```http
GET /api/cn/special/northbound/flow
GET /api/cn/special/northbound/holdings/{symbol}
```

**涨停池**
```http
GET /api/cn/special/limit-up
  ?date=2024-01-01
```

#### 2.2.5 宏观经济 `/api/cn/macro`

**利率数据**
```http
GET /api/cn/macro/lpr
GET /api/cn/macro/shibor?tenor=overnight
```

**通胀数据**
```http
GET /api/cn/macro/cpi
GET /api/cn/macro/ppi
```

**货币供应**
```http
GET /api/cn/macro/m2
GET /api/cn/macro/social-financing
```

### 2.3 美国市场 API (US Market)

#### 2.3.1 股票数据 `/api/us/stock`

```http
GET /api/us/stock/{symbol}/basic
GET /api/us/stock/{symbol}/history
GET /api/us/stock/{symbol}/realtime
GET /api/us/stock/{symbol}/financial
```

#### 2.3.2 市场数据 `/api/us/market`

```http
GET /api/us/market/overview
GET /api/us/market/sectors
```

### 2.4 香港市场 API (HK Market)

#### 2.4.1 股票数据 `/api/hk/stock`

```http
GET /api/hk/stock/{symbol}/basic
GET /api/hk/stock/{symbol}/history
GET /api/hk/stock/{symbol}/realtime
```

#### 2.4.2 特殊数据 `/api/hk/special`

```http
GET /api/hk/special/southbound/flow
GET /api/hk/special/southbound/holdings
```

### 2.5 通用功能

#### 2.5.1 数据筛选 `/api/query`

```http
POST /api/query
Content-Type: application/json

{
  "market": "cn",
  "filters": [
    {"field": "pe_ttm", "op": "<", "value": 20},
    {"field": "industry", "op": "==", "value": "白酒"}
  ],
  "fields": ["symbol", "name", "pe_ttm", "pb", "market_cap"],
  "order_by": "market_cap",
  "limit": 50
}
```

#### 2.5.2 健康检查

```http
GET /health
```

---

## 3. 核心模块设计

### 3.1 数据源抽象层 (Provider Layer)

#### 3.1.1 设计模式

借鉴 akshare-one-enhanced 的工厂模式：

```python
# providers/base.py
from abc import ABC, abstractmethod
from typing import Any, Dict
import pandas as pd

class BaseProvider(ABC):
    """数据源基类"""

    @abstractmethod
    def get_hist_data(self, symbol: str, **kwargs) -> pd.DataFrame:
        """获取历史数据"""
        pass

    @abstractmethod
    def get_realtime_data(self, symbol: str) -> pd.DataFrame:
        """获取实时数据"""
        pass

    @abstractmethod
    def get_financial_data(self, symbol: str, statement_type: str) -> pd.DataFrame:
        """获取财务数据"""
        pass
```

#### 3.1.2 理杏仁 Provider

```python
# providers/lixinger.py
from .base import BaseProvider
from lixinger_openapi.query import query_json

class LixingerProvider(BaseProvider):
    """理杏仁数据源"""

    def __init__(self, token: str):
        self.token = token

    def get_hist_data(self, symbol: str, **kwargs) -> pd.DataFrame:
        result = query_json("cn/company/candlestick", {
            "stockCode": symbol,
            "type": kwargs.get("adjust", "ex_rights"),
            "startDate": kwargs.get("start_date"),
            "endDate": kwargs.get("end_date"),
            "period": kwargs.get("interval", "daily")
        })
        return pd.DataFrame(result.get('data', []))

    # ... 其他方法实现
```

#### 3.1.3 AKShare Provider

```python
# providers/akshare.py
import akshare as ak
from .base import BaseProvider

class AKShareProvider(BaseProvider):
    """AKShare 数据源"""

    def get_hist_data(self, symbol: str, **kwargs) -> pd.DataFrame:
        df = ak.stock_zh_a_hist(
            symbol=symbol,
            period=kwargs.get("interval", "daily"),
            start_date=kwargs.get("start_date"),
            end_date=kwargs.get("end_date"),
            adjust=kwargs.get("adjust", "")
        )
        return self._normalize_columns(df)

    # ... 其他方法实现
```

### 3.2 多数据源路由 (Multi-Source Router)

#### 3.2.1 自动故障切换

```python
# providers/router.py
from typing import List, Tuple
import logging

class MultiSourceRouter:
    """多数据源路由器"""

    def __init__(self, providers: List[Tuple[str, BaseProvider]]):
        self.providers = providers

    def execute(self, method_name: str, **kwargs):
        """按优先级尝试多个数据源"""
        for source_name, provider in self.providers:
            try:
                method = getattr(provider, method_name)
                result = method(**kwargs)
                logging.info(f"Successfully fetched data from {source_name}")
                return result
            except Exception as e:
                logging.warning(f"Failed to fetch from {source_name}: {e}")
                continue

        raise RuntimeError(f"All providers failed for {method_name}")
```

### 3.3 缓存层 (Cache Layer)

#### 3.3.1 智能缓存策略

```python
# providers/cache.py
from cachetools import TTLCache
from datetime import datetime

class CacheManager:
    """智能缓存管理"""

    def __init__(self):
        # 实时数据: 1小时
        self.realtime_cache = TTLCache(maxsize=1000, ttl=3600)
        # 日线数据: 24小时
        self.daily_cache = TTLCache(maxsize=5000, ttl=86400)
        # 历史数据: 7天
        self.historical_cache = TTLCache(maxsize=10000, ttl=604800)
        # 财务数据: 30天
        self.financial_cache = TTLCache(maxsize=2000, ttl=2592000)

    def get_cache(self, data_type: str):
        """根据数据类型选择缓存"""
        cache_map = {
            "realtime": self.realtime_cache,
            "daily": self.daily_cache,
            "historical": self.historical_cache,
            "financial": self.financial_cache,
        }
        return cache_map.get(data_type, self.daily_cache)
```

### 3.4 数据标准化 (Data Normalization)

#### 3.4.1 字段映射

```python
# models/field_mapping.py
FIELD_MAPPINGS = {
    "cn": {
        "timestamp": ["日期", "date", "交易日期"],
        "open": ["开盘", "open"],
        "high": ["最高", "high"],
        "low": ["最低", "low"],
        "close": ["收盘", "close"],
        "volume": ["成交量", "volume"],
        "amount": ["成交额", "amount"],
    },
    "us": {
        "timestamp": ["Date", "date"],
        "open": ["Open", "open"],
        # ...
    }
}

def normalize_columns(df: pd.DataFrame, market: str = "cn") -> pd.DataFrame:
    """标准化列名"""
    mapping = FIELD_MAPPINGS.get(market, {})
    reverse_mapping = {v: k for k, vals in mapping.items() for v in vals}

    df.columns = [reverse_mapping.get(col, col) for col in df.columns]
    return df
```

---

## 4. 项目目录结构

### 4.1 推荐结构

```
findata-service/
├── server.py                    # FastAPI 服务入口
├── config/
│   ├── __init__.py
│   ├── settings.py             # 配置管理
│   └── logging.py              # 日志配置
├── routes/
│   ├── __init__.py
│   ├── cn/                     # 中国市场路由
│   │   ├── __init__.py
│   │   ├── stock.py
│   │   ├── market.py
│   │   ├── flow.py
│   │   ├── special.py
│   │   └── macro.py
│   ├── us/                     # 美国市场路由
│   │   ├── __init__.py
│   │   ├── stock.py
│   │   └── market.py
│   └── hk/                     # 香港市场路由
│       ├── __init__.py
│       ├── stock.py
│       ├── market.py
│       └── special.py
├── providers/
│   ├── __init__.py
│   ├── base.py                 # 数据源基类
│   ├── lixinger.py             # 理杏仁
│   ├── akshare.py              # AKShare
│   ├── sina.py                 # 新浪
│   ├── eastmoney.py            # 东方财富
│   ├── yahoo.py                # Yahoo Finance (US)
│   ├── router.py               # 多源路由
│   └── cache.py                # 缓存层
├── models/
│   ├── __init__.py
│   ├── requests.py             # 请求模型
│   ├── responses.py            # 响应模型
│   └── field_mapping.py        # 字段映射
├── services/
│   ├── __init__.py
│   ├── stock_service.py
│   ├── market_service.py
│   └── macro_service.py
├── utils/
│   ├── __init__.py
│   ├── date_utils.py
│   └── validators.py
├── tests/
│   ├── __init__.py
│   ├── test_cn_stock.py
│   ├── test_us_stock.py
│   └── test_providers.py
├── requirements.txt
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── README.md
```

### 4.2 Skills 客户端结构

```
skills/
├── China-market/
│   ├── dividend-corporate-action-tracker/
│   │   ├── skill.md
│   │   ├── data-queries.md      # 使用文档
│   │   └── client.py            # 轻量级客户端
│   ├── macro-liquidity-monitor/
│   │   ├── skill.md
│   │   ├── data-queries.md
│   │   └── client.py
│   └── ...
├── US-market/
│   └── ...
└── HK-market/
    └── ...
```

---

## 5. 实现示例

### 5.1 FastAPI 服务端

```python
# server.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routes.cn import stock as cn_stock
from routes.us import stock as us_stock
from routes.hk import stock as hk_stock

app = FastAPI(
    title="Findata Service",
    description="统一金融数据服务 API",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(cn_stock.router, prefix="/api/cn/stock", tags=["CN-Stock"])
app.include_router(us_stock.router, prefix="/api/us/stock", tags=["US-Stock"])
app.include_router(hk_stock.router, prefix="/api/hk/stock", tags=["HK-Stock"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 5.2 路由实现

```python
# routes/cn/stock.py
from fastapi import APIRouter, Query, HTTPException
from providers.router import MultiSourceRouter
from providers.lixinger import LixingerProvider
from providers.akshare import AKShareProvider
from models.responses import StandardResponse

router = APIRouter()

# 初始化数据源路由器
lixinger = LixingerProvider(token=settings.LIXINGER_TOKEN)
akshare = AKShareProvider()
stock_router = MultiSourceRouter([
    ("lixinger", lixinger),
    ("akshare", akshare)
])

@router.get("/{symbol}/history", response_model=StandardResponse)
async def get_stock_history(
    symbol: str,
    interval: str = Query("day", regex="^(minute|hour|day|week|month)$"),
    start_date: str = Query(..., regex="^\d{4}-\d{2}-\d{2}$"),
    end_date: str = Query(..., regex="^\d{4}-\d{2}-\d{2}$"),
    adjust: str = Query("none", regex="^(none|qfq|hfq)$")
):
    """获取股票历史行情"""
    try:
        df = stock_router.execute(
            "get_hist_data",
            symbol=symbol,
            interval=interval,
            start_date=start_date,
            end_date=end_date,
            adjust=adjust
        )

        return StandardResponse(
            code=1,
            message="success",
            data=df.to_dict(orient="records"),
            meta={
                "source": "multi",
                "count": len(df),
                "timestamp": datetime.now().isoformat()
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 5.3 Skills 客户端

```python
# skills/China-market/dividend-corporate-action-tracker/client.py
import requests
from typing import Dict, List, Optional

FIN_DATA_SERVICE = "http://localhost:8000"  # 或从环境变量读取

class DividendClient:
    """分红配股数据客户端"""

    def __init__(self, base_url: str = FIN_DATA_SERVICE):
        self.base_url = base_url

    def get_dividend_actions(
        self,
        symbol: Optional[str] = None,
        date: Optional[str] = None
    ) -> Dict:
        """获取分红配股数据"""
        params = {}
        if symbol:
            params["symbol"] = symbol
        if date:
            params["date"] = date

        resp = requests.get(
            f"{self.base_url}/api/cn/special/dividend",
            params=params
        )
        return resp.json()

    def get_dividend_calendar(self, start_date: str, end_date: str) -> List[Dict]:
        """获取分红日历"""
        resp = requests.get(
            f"{self.base_url}/api/cn/special/dividend/calendar",
            params={"start_date": start_date, "end_date": end_date}
        )
        return resp.json()["data"]

# 使用示例
if __name__ == "__main__":
    client = DividendClient()
    result = client.get_dividend_actions(symbol="600519")
    print(result)
```

---

## 6. 数据模型定义

### 6.1 请求模型

```python
# models/requests.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

class StockHistoryRequest(BaseModel):
    symbol: str = Field(..., description="股票代码")
    interval: str = Field("day", description="时间间隔")
    start_date: date = Field(..., description="开始日期")
    end_date: date = Field(..., description="结束日期")
    adjust: str = Field("none", description="复权类型")
    source: Optional[str] = Field(None, description="指定数据源")

class StockFinancialRequest(BaseModel):
    symbol: str
    statement_type: str = Field(..., regex="^(balance_sheet|income|cash_flow)$")
    limit: int = Field(5, ge=1, le=20)
```

### 6.2 响应模型

```python
# models/responses.py
from pydantic import BaseModel
from typing import Any, List, Dict, Optional
from datetime import datetime

class ResponseMeta(BaseModel):
    source: str
    cached: bool = False
    timestamp: datetime
    count: int

class StandardResponse(BaseModel):
    code: int = 1
    message: str = "success"
    data: List[Dict[str, Any]]
    meta: ResponseMeta
    warnings: Optional[List[str]] = []
    errors: Optional[List[str]] = []
```

---

## 7. 迁移计划

### 7.1 阶段一：核心服务搭建 (Week 1-2)

**目标**：基于 akshare-one-enhanced 搭建基础服务

**任务**：
1. Fork akshare-one-enhanced → findata-service
2. 添加 FastAPI 服务层
3. 实现中国市场核心接口
   - 股票基础数据
   - 历史行情
   - 实时行情
   - 财务数据
4. 集成理杏仁 Provider
5. 实现缓存层

**交付物**：
- 可运行的 FastAPI 服务
- 中国市场核心 API
- 基础测试用例

### 7.2 阶段二：扩展功能 (Week 3-4)

**目标**：完善中国市场功能，支持特殊数据

**任务**：
1. 实现资金流向 API
2. 实现龙虎榜/大宗交易 API
3. 实现北向资金 API
4. 实现宏观数据 API
5. 多数据源自动切换测试

**交付物**：
- 完整的中国市场 API
- 数据源切换测试报告

### 7.3 阶段三：多市场支持 (Week 5-6)

**目标**：添加美国和香港市场支持

**任务**：
1. 集成 Yahoo Finance Provider (US)
2. 实现美国市场 API
3. 实现香港市场 API
4. 实现港股通数据

**交付物**：
- 三市场统一 API
- 多市场测试用例

### 7.4 阶段四：Skills 迁移 (Week 7-8)

**目标**：迁移现有 Skills 到新架构

**任务**：
1. 设计 Skills 客户端规范
2. 实现示范客户端 (dividend-tracker, macro-monitor)
3. 批量迁移 China-market Skills (59个)
4. 更新所有 data-queries.md
5. 废弃旧 findata-toolkit

**交付物**：
- 所有 Skills 迁移完成
- 更新的文档
- 废弃的旧代码

### 7.5 阶段五：优化与部署 (Week 9-10)

**目标**：性能优化和生产部署

**任务**：
1. 性能测试与优化
2. Docker 容器化
3. 部署文档
4. 监控与告警
5. 用户文档

**交付物**：
- 生产就绪的服务
- 完整文档
- 监控面板

---

## 8. 技术栈

### 8.1 核心技术

**服务端**：
- Python 3.10+
- FastAPI (Web框架)
- Pydantic (数据验证)
- Pandas (数据处理)

**数据源**：
- lixinger-openapi (理杏仁 SDK)
- akshare (开源金融数据库)
- requests (HTTP客户端)

**缓存**：
- cachetools (内存缓存)
- Redis (可选，分布式缓存)

**部署**：
- Docker
- Docker Compose
- Nginx (反向代理)

### 8.2 依赖管理

```toml
# pyproject.toml
[project]
name = "findata-service"
version = "1.0.0"
requires-python = ">=3.10"

dependencies = [
    "fastapi>=0.115.0",
    "uvicorn>=0.35.0",
    "pydantic>=2.0.0",
    "pandas>=2.0.0",
    "akshare>=1.17.80",
    "lixinger-openapi>=0.1.0",
    "cachetools>=5.5.0",
    "requests>=2.32.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.24.0",
    "httpx>=0.27.0",
    "black>=24.0.0",
    "ruff>=0.12.0",
]
```

---

## 9. 测试策略

### 9.1 单元测试

```python
# tests/test_cn_stock.py
import pytest
from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

def test_get_stock_history():
    """测试获取股票历史数据"""
    response = client.get(
        "/api/cn/stock/600519/history",
        params={
            "start_date": "2024-01-01",
            "end_date": "2024-01-31",
            "interval": "day"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 1
    assert len(data["data"]) > 0

def test_multi_source_fallback():
    """测试多数据源切换"""
    # 模拟理杏仁失败，切换到 AKShare
    pass
```

### 9.2 集成测试

```python
# tests/test_integration.py
def test_end_to_end_flow():
    """端到端测试：从客户端到服务端"""
    from skills.China-market.dividend-tracker.client import DividendClient

    client = DividendClient(base_url="http://localhost:8000")
    result = client.get_dividend_actions(symbol="600519")

    assert result["code"] == 1
    assert "data" in result
```

---

## 10. 配置管理

### 10.1 环境变量

```bash
# .env
LIXINGER_TOKEN=your_token_here
AKSHARE_CACHE_DIR=/tmp/akshare-cache
REDIS_URL=redis://localhost:6379
LOG_LEVEL=INFO
CACHE_ENABLED=true
CACHE_TTL_DEFAULT=86400
```

### 10.2 配置类

```python
# config/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 数据源配置
    lixinger_token: str
    akshare_cache_dir: str = "/tmp/akshare-cache"

    # 缓存配置
    cache_enabled: bool = True
    cache_ttl_default: int = 86400
    redis_url: str = "redis://localhost:6379"

    # 服务配置
    service_host: str = "0.0.0.0"
    service_port: int = 8000
    log_level: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
```

---

## 11. 监控与日志

### 11.1 日志配置

```python
# config/logging.py
import logging
from logging.config import dictConfig

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "findata-service.log",
            "maxBytes": 10485760,
            "backupCount": 5,
            "formatter": "default",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"],
    },
}

dictConfig(LOGGING_CONFIG)
```

### 11.2 性能监控

```python
# middleware/monitoring.py
from fastapi import Request
import time

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    # 记录慢请求
    if process_time > 1.0:
        logging.warning(f"Slow request: {request.url} took {process_time:.2f}s")

    return response
```

---

## 12. 部署方案

### 12.1 Docker 部署

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 12.2 Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  findata-service:
    build: .
    ports:
      - "8000:8000"
    environment:
      - LIXINGER_TOKEN=${LIXINGER_TOKEN}
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
    volumes:
      - ./logs:/app/logs

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data

volumes:
  redis-data:
```

### 12.3 启动命令

```bash
# 开发环境
uvicorn server:app --reload

# 生产环境
uvicorn server:app --host 0.0.0.0 --port 8000 --workers 4

# Docker
docker-compose up -d
```

---

## 13. 文档与培训

### 13.1 API 文档

FastAPI 自动生成文档：
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

### 13.2 用户文档

需要编写：
- 快速开始指南
- API 使用示例
- 错误代码说明
- 最佳实践

### 13.3 开发者文档

需要编写：
- 架构设计文档
- 贡献指南
- 测试指南
- 部署指南

---

## 14. 风险与挑战

### 14.1 技术风险

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 数据源不稳定 | 高 | 多数据源备份、缓存策略 |
| 性能瓶颈 | 中 | 缓存优化、异步处理 |
| API 限流 | 中 | 请求队列、Token 池 |

### 14.2 迁移风险

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 现有 Skills 依赖 | 高 | 渐进式迁移、兼容层 |
| 数据格式变化 | 中 | 标准化层、版本控制 |
| 用户习惯改变 | 低 | 文档培训、示例代码 |

---

## 15. 成功指标

### 15.1 技术指标

- ✅ API 响应时间 < 200ms (P95)
- ✅ 数据源可用性 > 99%
- ✅ 缓存命中率 > 80%
- ✅ 测试覆盖率 > 80%

### 15.2 业务指标

- ✅ 93 个 data-queries.md 迁移完成
- ✅ 59 个 China-market Skills 迁移完成
- ✅ 用户文档完整
- ✅ 部署文档完整

---

## 16. 附录

### 16.1 参考资料

- [akshare-one-enhanced 项目](https://github.com/zwldarren/akshare-one)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [理杏仁 API 文档](https://www.lixinger.com/analytics/api/doc)
- [AKShare 文档](https://akshare.akfamily.xyz/)

### 16.2 术语表

| 术语 | 说明 |
|------|------|
| Provider | 数据源提供者 |
| Router | 多数据源路由器 |
| Skills | 技能层，业务逻辑单元 |
| View | 数据视图，聚合多个工具 |

### 16.3 联系方式

- 项目负责人: [待填写]
- 技术支持: [待填写]
- 文档维护: [待填写]

---

**文档结束**

*本文档将随着项目进展持续更新*
