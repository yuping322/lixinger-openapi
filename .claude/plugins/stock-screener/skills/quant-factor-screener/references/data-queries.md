# 量化因子筛选数据获取指南

## 定位

本策略优先把 `lixinger-screener` 作为 **候选池构建器**，再对入围名单补充因子计算所需数据。

- **第一层**：`lixinger-screener` 负责 universe 筛选、基础条件过滤和导出候选池
- **第二层**：`query_data` 负责价格、行业、宏观、补充基本面等因子输入

## 推荐工作流

### 第一步：用 `lixinger-screener` 缩小候选池

```bash
cd /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/lixinger-screener

node request/fetch-lixinger-screener.js \
  --query "PE-TTM小于30，PB小于4，ROE大于8%，资产负债率小于60%，上市日期早于2020-01-01" \
  --output csv
```

适合先放进候选池的条件：
- 估值：`PE-TTM`、`PB`、`EV/EBITDA`
- 质量：`ROE`、资产负债率、毛利率
- 成长：营收增长率、净利润增长率
- 流动性：市值、成交额、换手率
- 基础排除：ST、退市、过新上市公司

## 第二步：对入围名单补充因子计算数据

### 基本面与行业数据

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date": "latest", "stockCodes": ["000001", "600519"], "metricsList": ["pe_ttm", "pb", "pcf_ttm", "ev_ebitda_r", "roe", "debt_to_assets", "ocf_to_net_profit", "mc", "to_r"]}' \
  --columns "date,stockCode,pe_ttm,pb,pcf_ttm,ev_ebitda_r,roe,debt_to_assets,ocf_to_net_profit,mc,to_r"
```

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/industries" \
  --params '{"date": "latest", "stockCodes": ["000001", "600519"]}' \
  --columns "date,stockCode,industry_name,industry_code"
```

### 价格、动量、低波动

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"date": "latest", "stockCodes": ["000001", "600519"], "limit": 250}' \
  --columns "date,stockCode,open,high,low,close,volume,turnover_rate"
```

### 基准与宏观环境

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/candlestick" \
  --params '{"date": "latest", "stockCodes": ["000300", "000905"], "limit": 250}' \
  --columns "date,stockCode,open,high,low,close,volume"
```

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "macro/interest-rates" \
  --params '{"startDate": "2025-01-01", "endDate": "latest"}' \
  --columns "date,rate_type,rate_value"
```

## 适用边界

- `lixinger-screener` 适合先完成 universe builder，不适合直接代替完整因子计算引擎。
- 动量、波动率、Beta、行业中性化等计算仍需要价格、指数和行业数据补充。
- 如果策略要做宏观择时或风格轮动，需要继续调用宏观与指数接口。

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../../../query_data/lixinger-api-docs/SKILL.md`
