# 小盘成长策略数据获取指南

## 定位

本策略把 `lixinger-screener` 作为小市值成长候选池入口，再对入围名单补充经营质量、现金流和股东结构数据。

## 推荐工作流

### 第一步：用 `lixinger-screener` 构建小盘成长候选池

```bash
cd /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/lixinger-screener

node request/fetch-lixinger-screener.js \
  --query "总市值小于150亿，营业收入增长率(3年复合)大于15%，净利润增长率(3年复合)大于15%，净资产收益率(TTM)大于10%，资产负债率小于60%" \
  --output csv
```

适合先放进候选池的条件：
- 总市值 / 流通市值
- 营收增长率 / 净利润增长率
- ROE / 毛利率 / 资产负债率
- ST 排除、上市年限、板块限制

## 第二步：对入围名单补充质量与股东数据

### 财务基本面

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date": "latest", "stockCodes": ["300750"], "metricsList": ["mc", "pe_ttm", "pb", "roe"]}' \
  --columns "date,stockCode,mc,pe_ttm,pb,roe"
```

### 营收、利润率与现金流

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"date": "latest", "stockCodes": ["300750"], "metricsList": ["operating_revenue", "gross_profit_margin", "net_profit_margin", "net_operate_cash_flow"]}' \
  --columns "date,stockCode,operating_revenue,gross_profit_margin,net_profit_margin,net_operate_cash_flow"
```

### 股东或资金侧补充

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/mutual-market" \
  --params '{"date": "latest"}' \
  --columns "date,stockCode,holder_name,hold_ratio,hold_type" \
  --limit 100
```

## 适用边界

- `lixinger-screener` 非常适合先做“小市值 + 增长 + 盈利能力”的批量初筛。
- 更细的经营质量、现金流、股东结构、机构持仓等信息，建议只对入围名单补查。
- 若要识别专精特新、产业链位置或管理层特征，可继续使用其他数据源补充。

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../../../query_data/lixinger-api-docs/SKILL.md`
