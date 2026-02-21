# 数据获取指南

本文档说明如何获取本技能所需的数据。

---

## 📊 可用数据源

### 1. Findata Service API (推荐)

**服务地址**: http://localhost:8000  
**API文档**: http://localhost:8000/docs

#### 可用接口

| 接口 | 端点 | 说明 | 状态 |
|------|------|------|------|
| 公司基本信息 | `GET /api/cn/stock/{symbol}/basic` | 股票代码、交易所、上市日期等 | ✅ 可用 |
| 公司概况 | `GET /api/cn/stock/{symbol}/profile` | 公司名称、地址、实控人等 | ✅ 可用 |
| K线数据 | `GET /api/cn/stock/{symbol}/history` | 历史行情数据 | ✅ 可用 |
| 公告 | `GET /api/cn/stock/{symbol}/announcement` | 公司公告 | ✅ 可用 |
| 股东人数 | `GET /api/cn/shareholder/{symbol}/count` | 股东人数变化 | ✅ 可用 |
| 股本变动 | `GET /api/cn/shareholder/{symbol}/equity-change` | 股本结构变化 | ✅ 可用 |
| 分红送配 | `GET /api/cn/dividend/{symbol}` | 分红历史 | ✅ 可用 |

#### 使用示例

```bash
# 获取公司基本信息
curl "http://localhost:8000/api/cn/stock/600519/basic"

# 获取K线数据
curl "http://localhost:8000/api/cn/stock/600519/history?start_date=2023-01-01&end_date=2026-02-21"

# 获取分红数据
curl "http://localhost:8000/api/cn/dividend/600519"

# 获取股东人数
curl "http://localhost:8000/api/cn/shareholder/600519/count"

# 获取公告
curl "http://localhost:8000/api/cn/stock/600519/announcement"
```

---

### 2. 理杏仁API直接调用

**前提**: 需要配置理杏仁Token

#### Python示例

```python
from lixinger_openapi.query import query_json
from lixinger_openapi.token import set_token
from datetime import datetime, timedelta

# 设置token
set_token('your-token', write_token=False)

# 获取公司基本信息
result = query_json("cn/company", {
    "stockCodes": ["600519"]
})

# 获取K线数据
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

result = query_json("cn/company/candlestick", {
    "stockCode": "600519",
    "type": "ex_rights",
    "startDate": start_date,
    "endDate": end_date
})

# 获取分红数据
result = query_json("cn/company/dividend", {
    "stockCode": "600519",
    "startDate": start_date,
    "endDate": end_date
})

# 获取股东人数
result = query_json("cn/company/shareholders-num", {
    "stockCode": "600519",
    "startDate": start_date,
    "endDate": end_date
})

# 获取股本变动
result = query_json("cn/company/equity-change", {
    "stockCode": "600519",
    "startDate": start_date,
    "endDate": end_date
})

# 获取公告
result = query_json("cn/company/announcement", {
    "stockCode": "600519",
    "limit": 20
})
```

---

## ⚠️ 数据限制说明

### 理杏仁免费版限制

以下数据在免费版中**不可用**：

| 数据类型 | 状态 | 替代方案 |
|---------|------|---------|
| 股东详细信息 | ❌ 不可用 | 使用股东人数接口 |
| 高管增减持 | ❌ 不可用 | 考虑使用AKShare |
| 大股东增减持 | ❌ 不可用 | 考虑使用AKShare |
| 龙虎榜 | ⚠️ API可用但通常无数据 | 考虑使用AKShare |
| 大宗交易 | ❌ 不可用 | 考虑使用AKShare |
| 股权质押 | ❌ 不可用 | 考虑使用AKShare |
| 实时行情 | ⚠️ 使用最新日线代替 | 使用K线数据 |
| 估值指标 | ❌ 不可用 | 考虑升级订阅 |

---

## 🔄 替代数据源

### AKShare (开源免费)

对于理杏仁不提供的数据，可以使用AKShare：

```python
import akshare as ak

# 股权质押
pledge_data = ak.stock_pledge_stat(symbol="600519")

# 龙虎榜
lhb_data = ak.stock_lhb_detail_em(symbol="600519")

# 大宗交易
block_trade = ak.stock_dzjy_mrmx(symbol="600519")

# 高管增减持
executive = ak.stock_ggcg_em(symbol="600519")
```

**安装AKShare**:
```bash
pip install akshare
```

---

## 📝 数据字段说明

### 公司基本信息
```json
{
  "stockCode": "600519",
  "exchange": "sh",
  "market": "a",
  "ipoDate": "2001-08-27T00:00:00+08:00",
  "name": "贵州茅台"
}
```

### K线数据
```json
{
  "date": "2026-02-13T00:00:00+08:00",
  "open": 1486.6,
  "close": 1485.3,
  "high": 1507.8,
  "low": 1470.58,
  "volume": 4167900,
  "amount": 6216379203
}
```

### 分红数据
```json
{
  "date": "2025-11-06T00:00:00+08:00",
  "fsEndDate": "2025-09-30T00:00:00+08:00",
  "dividendPerShare": 30.0,
  "dividendRatio": 0.5,
  "dividendYield": 0.02
}
```

### 股东人数
```json
{
  "date": "2025-09-30T00:00:00+08:00",
  "num": 238512,
  "total": 238512,
  "shareholdersNumberChangeRate": 0.0809
}
```

### 股本变动
```json
{
  "date": "2025-09-01T00:00:00+08:00",
  "declarationDate": "2025-08-30T00:00:00+08:00",
  "changeReason": "股份回购",
  "capitalization": 1252000000,
  "outstandingSharesA": 1252000000
}
```

### 公告数据
```json
{
  "date": "2026-02-04T00:00:00+08:00",
  "linkText": "贵州茅台关于回购股份实施进展的公告",
  "linkUrl": "https://...",
  "types": ["srp"]
}
```

---

## 🎯 最佳实践

### 1. 数据缓存
- findata-service已实现多级缓存
- 避免频繁请求相同数据
- 合理设置数据更新频率

### 2. 错误处理
```python
result = query_json(endpoint, params)
if result.get('code') == 1:
    data = result.get('data', [])
    # 处理数据
else:
    # 处理错误
    print(f"Error: {result.get('message')}")
```

### 3. 批量查询
```python
# 查询多只股票
symbols = ["600519", "000858", "600036"]
for symbol in symbols:
    result = query_json("cn/company", {"stockCodes": [symbol]})
    # 处理结果
```

---

## 📚 相关文档

- **API参考**: `findata-service/API_REFERENCE.md`
- **服务实现**: `findata-service/IMPLEMENTATION_COMPLETE.md`
- **Skills就绪**: `SKILLS_READINESS_REPORT.md`
- **使用演示**: `SKILLS_USAGE_DEMO.md`

---

## 💡 技巧提示

1. **优先使用findata-service**: 已封装好的API，使用更方便
2. **注意日期格式**: 统一使用 YYYY-MM-DD 格式
3. **检查数据可用性**: 使用前先确认数据是否可用
4. **合理设置时间范围**: 避免查询过长时间范围的数据
5. **关注数据更新频率**: 
   - K线数据: 每日更新
   - 财务数据: 季度更新
   - 公告数据: 实时更新

---

**文档版本**: 1.0  
**更新时间**: 2026-02-21  
**维护者**: Kiro AI
