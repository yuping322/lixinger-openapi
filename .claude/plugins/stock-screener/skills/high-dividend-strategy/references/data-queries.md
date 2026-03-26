# 高股息策略数据获取指南

## 定位

本策略的数据获取分两层：

1. **候选池构建**：优先使用 `.claude/skills/lixinger-screener`
2. **补充数据**：对入围名单再按需调用 `.claude/plugins/query_data` 或其他接口

这样可以先批量筛出高股息候选股，再对少量入围公司检查分红可持续性，避免全市场逐股深拉。

## 推荐工作流

### 第一步：用 `lixinger-screener` 建候选池

```bash
cd /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/lixinger-screener

node request/fetch-lixinger-screener.js \
  --query "股息率大于3%，PE-TTM小于20，PB小于2，上市日期早于2018-01-01" \
  --output markdown
```

更稳定的方式是使用参数文件：

```bash
cd /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/lixinger-screener

node request/fetch-lixinger-screener.js \
  --input-file high-dividend-screen.json \
  --output csv
```

建议的候选池条件：
- `股息率`：先做初筛
- `PE-TTM` / `PB`：过滤极端高估值标的
- `上市日期`：过滤上市时间过短的公司
- `excludeSpecialTreatment`：排除 ST
- 行业、板块、指数范围：按策略需要限定

## 第二步：对入围名单补充分红与财务数据

候选池确定后，再对少量股票补充分红、自由现金流和资产负债率等字段。

### 历史分红

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/dividend" \
  --params '{"stockCode": "600519", "startDate": "2021-01-01"}' \
  --columns "date,dividend,dividendAmount,annualNetProfitDividendRatio,exDate"
```

### 财务与估值补数

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"stockCodes":["600519"],"date":"latest","metricsList":["dyr","pe_ttm","pb","mc"]}' \
  --columns "stockCode,dyr,pe_ttm,pb,mc"
```

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"stockCodes":["600519"],"startDate":"2021-01-01","endDate":"latest","metricsList":["q.ps.np.t","q.cfs.fcf.t","q.bs.tl.t","q.bs.ta.t"]}' \
  --columns "date,stockCode,q.ps.np.t,q.cfs.fcf.t,q.bs.tl.t,q.bs.ta.t"
```

### 总回报所需价格

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCode": "600519", "startDate": "2021-01-01", "endDate": "latest", "type": "bc_rights"}' \
  --columns "date,close"
```

## 适用边界

- `lixinger-screener` 适合构建高股息候选池，不负责完整分红历史与现金流覆盖计算。
- `cn/company/dividend` 只支持单个 `stockCode`，因此更适合对入围股补查，而不是全市场直接循环。
- 若需要更复杂的红利指数成分、行业暴露或外部收益率对比，可继续使用其他接口补数。

## 相关文件

- 技能文档：`.claude/plugins/stock-screener/skills/high-dividend-strategy/`
- 计算方法：`.claude/plugins/stock-screener/skills/high-dividend-strategy/references/calculation-methodology.md`
- 输出模板：`.claude/plugins/stock-screener/skills/high-dividend-strategy/references/output-template.md`
- 理杏仁筛选底座：`.claude/skills/lixinger-screener/`
- 补充数据接口：`.claude/plugins/query_data/lixinger-api-docs/`
