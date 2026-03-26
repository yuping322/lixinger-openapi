# ESG 筛选数据获取指南

## 定位

ESG 筛选同样采用两层数据结构：

1. **候选池与基础排除**：优先使用 `lixinger-screener`
2. **ESG 评分 / 争议 / 治理代理**：再使用 `query_data`、AkShare 或其他外部接口补数

`lixinger-screener` 不承担 ESG 全量评分职责，只负责通用股票池筛选。

## 推荐工作流

### 第一步：用 `lixinger-screener` 建候选池

```bash
cd /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/lixinger-screener

node request/fetch-lixinger-screener.js \
  --query "沪深300，排除ST，PE-TTM小于40，ROE大于8%，资产负债率小于70%" \
  --output csv
```

适合先在候选池阶段处理的条件：
- 股票池范围（沪深300 / 中证800 / 全A / 行业）
- ST / 退市 / 流动性排除
- 基础估值与财务健康过滤
- 行业、板块、上市时间等通用条件

## 第二步：补充 ESG 数据

### ESG 评级（外部）

> ⚠️ 理杏仁不提供独立 ESG 评分接口。
> 可使用 AkShare `stock_esg_rate_sina` 作为批量 ESG 评级补充源。

```python
import akshare as ak

esg_df = ak.stock_esg_rate_sina()
stock_esg = esg_df[esg_df['成分股代码'].str.contains('600519')]
print(stock_esg)
```

### 财务基本面

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"stockCodes": ["600519"], "date": "latest", "metricsList": ["pe_ttm", "pb", "roe_ttm"]}' \
  --columns "stockCode,pe_ttm,pb,roe_ttm"
```

### 治理代理数据

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/majority-shareholders" \
  --params '{"stockCode": "600519"}' \
  --columns "stockCode,shareholderName,holdingRatio"
```

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/nolimit-shareholders" \
  --params '{"stockCode": "600519"}' \
  --columns "stockCode,shareholderName,holdingRatio"
```

### 监管与争议代理

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/measures" \
  --params '{"stockCode": "600519"}' \
  --columns "stockCode,measureType,measureDate"
```

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/inquiry" \
  --params '{"stockCode": "600519"}' \
  --columns "stockCode,inquiryType,inquiryDate"
```

## 适用边界

- `lixinger-screener` 适合做 ESG 分析前的通用候选池和基础排除。
- ESG 评分、争议、治理质量、排放强度等核心维度仍需要外部数据或代理指标。
- 最佳实践是先批量拿 ESG 外部评级，再按股票代码过滤到 screener 候选池上。

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../../../query_data/lixinger-api-docs/SKILL.md`
