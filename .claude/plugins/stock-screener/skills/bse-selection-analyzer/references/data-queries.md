# 北交所选股数据获取指南

## 定位

本策略优先使用 `lixinger-screener` 生成北交所候选池，再对入围名单补充北证50、行情和财务数据。

## 推荐工作流

### 第一步：用 `lixinger-screener` 构建北交所候选池

```bash
cd /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/lixinger-screener

node request/fetch-lixinger-screener.js \
  --query "北交所，PE-TTM小于30，股息率大于1%，季度营收同比增长率大于10%，换手率大于1%" \
  --output csv
```

如果 request 版字段映射不稳定，可切到 browser 版验证页面字段：

```bash
cd /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/lixinger-screener

node run-skill.js --query "北交所，流动性较好，成长性较高" --headless false
```

## 第二步：对入围名单补充北交所专属数据

### 北证50成分股

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/constituents" \
  --params '{"date": "latest", "stockCodes": ["899050"]}' \
  --flatten "constituents" \
  --columns "stockCode"
```

### 基本面与流动性

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date": "latest", "stockCodes": ["920001", "920002"], "metricsList": ["pe_ttm", "pb", "dyr", "mc", "to_r", "ta"]}' \
  --columns "stockCode,pe_ttm,pb,dyr,mc,to_r,ta"
```

### 财务成长数据

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"date": "latest", "stockCodes": ["920001", "920002"], "metricsList": ["q.ps.toi.t_y2y", "q.ps.np.t_y2y", "q.ps.gp_m.t"]}' \
  --columns "stockCode,q.ps.toi.t_y2y,q.ps.np.t_y2y,q.ps.gp_m.t"
```

### 历史行情

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/quote/daily" \
  --params '{"date": "latest", "stockCodes": ["920001"], "metricsList": ["to", "ta", "high", "low", "volume"], "count": 20}' \
  --flatten "quote" \
  --columns "stockCode,date,to,ta,high,low,volume"
```

## 适用边界

- `lixinger-screener` 适合先筛出北交所候选池和基础流动性条件。
- 北证50、历史行情、公司基础信息等更适合通过 `query_data` 补充。
- 若需要更细的专精特新标签或政策属性，可继续接入其他数据源。

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../../../query_data/lixinger-api-docs/SKILL.md`
