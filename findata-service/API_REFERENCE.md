# Findata Service API 参考文档

## 服务信息

- **服务地址**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 接口统计

- **总计**: 35 个 API 接口
- **数据源**: 理杏仁
- **缓存**: 智能缓存（实时1小时，日线24小时，财务7天）

---

## 1. 股票接口 `/api/cn/stock`

### 1.1 获取股票基础信息
```
GET /api/cn/stock/{symbol}/basic
```

**参数**:
- `symbol`: 股票代码（如 600519）

**返回**:
```json
{
  "code": 1,
  "message": "success",
  "data": [{"name": "贵州茅台", "stockCode": "600519", ...}],
  "meta": {"source": "lixinger", "count": 1}
}
```

### 1.2 获取历史行情
```
GET /api/cn/stock/{symbol}/history
```

**参数**:
- `symbol`: 股票代码
- `start_date`: 开始日期 (YYYY-MM-DD)
- `end_date`: 结束日期 (YYYY-MM-DD)
- `period`: 周期 (daily/weekly/monthly)
- `adjust`: 复权类型 (ex_rights/no_adjust)

### 1.3 获取实时行情
```
GET /api/cn/stock/{symbol}/realtime
```

### 1.4 获取财务数据
```
GET /api/cn/stock/{symbol}/financial
```

**参数**:
- `statement_type`: 报表类型 (balance_sheet/income_statement/cash_flow)
- `limit`: 返回记录数 (1-20)

### 1.5 获取估值指标
```
GET /api/cn/stock/{symbol}/valuation
```

---

## 2. 市场接口 `/api/cn/market`

### 2.1 获取市场概览
```
GET /api/cn/market/overview
```

**返回**: 主要指数行情数据

---

## 3. 宏观接口 `/api/cn/macro`

### 3.1 LPR利率
```
GET /api/cn/macro/lpr
```

### 3.2 CPI数据
```
GET /api/cn/macro/cpi
```

### 3.3 PPI数据
```
GET /api/cn/macro/ppi
```

### 3.4 PMI数据
```
GET /api/cn/macro/pmi
```

### 3.5 M2货币供应
```
GET /api/cn/macro/m2
```

---

## 4. 资金流向接口 `/api/cn/flow`

### 4.1 个股资金流
```
GET /api/cn/flow/stock/{symbol}
```

### 4.2 指数资金流
```
GET /api/cn/flow/index/{index_code}
```

### 4.3 行业资金流
```
GET /api/cn/flow/industry?industry_code={code}
```

**参数**:
- `industry_code`: 行业代码（可选，不填返回所有）

---

## 5. 行业板块接口 `/api/cn/board`

### 5.1 行业列表
```
GET /api/cn/board/industry/list
```

### 5.2 行业K线
```
GET /api/cn/board/industry/{industry_code}/kline?start_date={start}&end_date={end}
```

### 5.3 行业成分股
```
GET /api/cn/board/industry/{industry_code}/stocks
```

### 5.4 行业估值
```
GET /api/cn/board/industry/{industry_code}/valuation
```

### 5.5 指数列表
```
GET /api/cn/board/index/list
```

### 5.6 指数K线
```
GET /api/cn/board/index/{index_code}/kline?start_date={start}&end_date={end}
```

### 5.7 指数成分股
```
GET /api/cn/board/index/{index_code}/constituents
```

---

## 6. 特殊数据接口 `/api/cn/special`

### 6.1 龙虎榜
```
GET /api/cn/special/dragon-tiger/{symbol}?start_date={start}&end_date={end}
```

**参数**:
- `symbol`: 股票代码
- `start_date`: 开始日期（可选）
- `end_date`: 结束日期（可选）

### 6.2 大宗交易
```
GET /api/cn/special/block-deal/{symbol}
```

### 6.3 股权质押
```
GET /api/cn/special/equity-pledge/{symbol}
```

---

## 7. 股东信息接口 `/api/cn/shareholder`

### 7.1 股东信息
```
GET /api/cn/shareholder/{symbol}
```

### 7.2 股东人数
```
GET /api/cn/shareholder/{symbol}/count
```

### 7.3 高管增减持
```
GET /api/cn/shareholder/{symbol}/executive
```

### 7.4 大股东增减持
```
GET /api/cn/shareholder/{symbol}/major
```

---

## 8. 分红配股接口 `/api/cn/dividend`

### 8.1 分红送配
```
GET /api/cn/dividend/{symbol}
```

---

## 统一响应格式

所有接口返回统一格式：

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

**字段说明**:
- `code`: 1表示成功，0表示失败
- `message`: 响应消息
- `data`: 数据数组
- `meta`: 元数据
  - `source`: 数据源
  - `cached`: 是否来自缓存
  - `timestamp`: 时间戳
  - `count`: 数据数量
- `warnings`: 警告信息
- `errors`: 错误信息

---

## 使用示例

### Python
```python
import requests

# 股票基础信息
response = requests.get("http://localhost:8000/api/cn/stock/600519/basic")
data = response.json()
print(data)

# 历史行情
response = requests.get(
    "http://localhost:8000/api/cn/stock/600519/history",
    params={"start_date": "2024-01-01", "end_date": "2024-12-31"}
)
data = response.json()
print(data)
```

### curl
```bash
# 股票基础信息
curl "http://localhost:8000/api/cn/stock/600519/basic"

# 历史行情
curl "http://localhost:8000/api/cn/stock/600519/history?start_date=2024-01-01&end_date=2024-12-31"

# 龙虎榜
curl "http://localhost:8000/api/cn/special/dragon-tiger/600519"
```

---

## 缓存策略

| 数据类型 | 缓存时间 | 说明 |
|---------|---------|------|
| 实时数据 | 1小时 | 资金流向、热度数据 |
| 日线数据 | 24小时 | K线、估值数据 |
| 财务数据 | 7天 | 财务报表、分红数据 |
| 宏观数据 | 24小时 | CPI、PPI、PMI等 |

---

## 错误处理

所有错误返回格式：

```json
{
  "detail": "错误描述"
}
```

HTTP状态码：
- `200`: 成功
- `404`: 数据未找到
- `500`: 服务器错误
