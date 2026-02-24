# 数据获取指南

本文档说明如何获取本技能所需的数据。

---

## 📊 推荐数据获取方式

### 1. 理杏仁数据查询工具 (query_tool.py) - 推荐

使用 `lixinger-data-query` skill 提供的查询工具，支持字段过滤、数据筛选和嵌套数组展开。

**工具路径**: `skills/lixinger-data-query/scripts/query_tool.py`

#### 核心优势
- ✅ 字段过滤 (`--columns`): 只返回需要的字段，节省 30-40% token
- ✅ 数据筛选 (`--row-filter`): 过滤符合条件的数据
- ✅ 数组展开 (`--flatten`): 处理嵌套结构（如指数成分股）
- ✅ CSV 格式输出: 默认格式，最节省 token
- ✅ 162 个 API 接口: 覆盖 A股、港股、美股、宏观数据

#### 使用示例

**查询股票基本信息**:
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company" \
  --params '{"stockCodes": ["600519"]}' \
  --columns "stockCode,name,ipoDate,exchange"
```

**查询 K 线数据**:
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.candlestick" \
  --params '{"stockCode": "600519", "startDate": "2024-01-01", "endDate": "2024-12-31"}' \
  --columns "date,open,close,high,low,volume"
```

**查询分红数据**:
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.dividend" \
  --params '{"stockCode": "600519"}' \
  --columns "date,dividendPerShare,dividendYield"
```

**查询股东人数**:
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.shareholders-num" \
  --params '{"stockCode": "600519"}' \
  --columns "date,num,shareholdersNumberChangeRate"
```

**查询公告信息**:
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.announcement" \
  --params '{"stockCode": "600519"}' \
  --columns "date,linkText,types" \
  --limit 20
```

**查询指数成分股（展开嵌套数组）**:
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.index.constituents" \
  --params '{"date": "2024-12-10", "stockCodes": ["000016"]}' \
  --flatten "constituents" \
  --columns "stockCode,weight"
```

**筛选低估值股票**:
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.fundamental.non_financial" \
  --params '{"date": "2024-12-10"}' \
  --row-filter '{"pe_ttm": {"<": 20}, "pb": {"<": 3}}' \
  --columns "stockCode,name,pe_ttm,pb" \
  --limit 50
```

#### 参数说明

**必需参数**:
- `--suffix`: API 路径（参考 [API 列表](../lixinger-data-query/SKILL.md#api-接口列表)）
- `--params`: JSON 格式参数（参考 `api_new/api-docs/` 中的 API 文档）

**增强参数（强烈推荐）**:
- `--columns`: 指定返回字段，逗号分隔
- `--row-filter`: JSON 格式过滤条件（支持 `>`, `<`, `==`, `!=`, `in`, `startswith`, `endswith`, `contains`）
- `--flatten`: 展开嵌套数组字段
- `--limit`: 限制返回行数（默认 100）

**可选参数**:
- `--format`: 输出格式 `csv`（默认）、`json`、`text`

#### 查找可用 API

**方法 1: 查看 API 列表**
```bash
# 查看完整 API 列表
cat skills/lixinger-data-query/SKILL.md
```

**方法 2: 搜索关键字**
```bash
# 搜索包含"分红"的 API
grep -r "分红" skills/lixinger-data-query/api_new/api-docs/

# 搜索包含"股东"的 API
grep -r "股东" skills/lixinger-data-query/api_new/api-docs/
```

**方法 3: 查看 API 文档**
```bash
# 查看具体 API 的参数说明
cat skills/lixinger-data-query/api_new/api-docs/cn_company_dividend.md
```

#### 最佳实践

1. **始终使用 `--columns`**: 只返回需要的字段，减少无用数据
2. **主动使用 `--row-filter`**: 过滤数据，提高数据质量
3. **处理嵌套数据时使用 `--flatten`**: 展开数组结构
4. **使用 `--limit` 控制数量**: 避免返回过多数据
5. **参考 API 文档**: 查看 `api_new/api-docs/` 了解参数格式

---

### 2. Findata Service API (备选)

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
curl "http://localhost:8000/api/cn/stock/600519/history?start_date=2024-01-01&end_date=2024-12-31"

# 获取分红数据
curl "http://localhost:8000/api/cn/dividend/600519"
```

---

### 3. 理杏仁 API 直接调用 (Python)

**前提**: 需要配置理杏仁 Token

```python
from lixinger_openapi.query import query_json
from lixinger_openapi.token import set_token

# 设置 token
set_token('your-token', write_token=False)

# 查询股票基本信息
result = query_json("cn/company", {"stockCodes": ["600519"]})

# 查询 K 线数据
result = query_json("cn/company/candlestick", {
    "stockCode": "600519",
    "startDate": "2024-01-01",
    "endDate": "2024-12-31"
})
```

---

## ⚠️ 数据限制说明

### 理杏仁免费版限制

以下数据在免费版中**不可用**或**数据有限**：

| 数据类型 | 状态 | 替代方案 |
|---------|------|---------|
| 股东详细信息 | ❌ 不可用 | 使用股东人数接口 |
| 高管增减持 | ❌ 不可用 | 考虑使用 AKShare |
| 大股东增减持 | ❌ 不可用 | 考虑使用 AKShare |
| 龙虎榜 | ⚠️ API 可用但通常无数据 | 考虑使用 AKShare |
| 大宗交易 | ❌ 不可用 | 考虑使用 AKShare |
| 股权质押 | ❌ 不可用 | 考虑使用 AKShare |
| 实时行情 | ⚠️ 使用最新日线代替 | 使用 K 线数据 |
| 估值指标 | ⚠️ 部分可用 | 使用 `cn/company/fundamental` |

---

## 🔄 替代数据源

### AKShare (开源免费)

对于理杏仁不提供的数据，可以使用 AKShare：

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

**安装 AKShare**:
```bash
pip install akshare
```

---

## 📚 相关文档

- **查询工具文档**: `skills/lixinger-data-query/SKILL.md`
- **LLM 使用指南**: `skills/lixinger-data-query/LLM_USAGE_GUIDE.md`
- **查询示例**: `skills/lixinger-data-query/EXAMPLES.md`
- **API 文档目录**: `skills/lixinger-data-query/api_new/api-docs/`

---

## 💡 技巧提示

1. **优先使用 query_tool.py**: 功能最强大，支持字段过滤和数据筛选
2. **使用 `--columns` 减少数据量**: 只返回需要的字段，节省 30-40% token
3. **使用 `--row-filter` 提高数据质量**: 只返回符合条件的数据
4. **查看 API 文档**: 参考 `api_new/api-docs/` 了解参数格式和可用字段
5. **注意日期格式**: 统一使用 YYYY-MM-DD 格式
6. **合理设置时间范围**: 避免查询过长时间范围的数据

---

**文档版本**: 2.0  
**更新时间**: 2026-02-23  
**维护者**: Kiro AI
