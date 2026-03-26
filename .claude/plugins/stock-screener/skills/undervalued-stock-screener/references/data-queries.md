# 数据查询指南（低估值股票筛选）

## 概述

本文档记录 `China-market_undervalued-stock-screener` 当前实际可运行的数据获取方式。

当前不再优先使用旧版 `query_tool.py` 逐个接口拼接数据，而是直接复用：

- 目录：`/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/lixinger-screener`
- 已验证脚本：`request/fetch-lixinger-screener.js`
- 数据来源：理杏仁公司筛选器页面接口（非 open api 逐只拉取）
- 认证方式：`.env` 或 shell 环境变量中的 `LIXINGER_USERNAME` / `LIXINGER_PASSWORD`

这种方式更适合本 skill，因为它能直接按筛选条件批量拉取结果，并自动分页汇总。

## 推荐工作流

### 1. 进入筛选器目录

```bash
cd /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/lixinger-screener
```

### 2. 使用 request 版批量获取结果

支持两种入口：

- `--input-file`：适合稳定复现、固定排序、导出结果
- `--query`：适合快速试错

输出格式支持：`table-json`（默认）、`markdown`、`csv`、`raw`

## 已验证命令

以下命令已在当前仓库中实际运行通过。

### A. 主模板：低估值高股息

```bash
cd /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/lixinger-screener
node request/fetch-lixinger-screener.js \
  --input-file low-valuation-high-dividend.json \
  --output markdown
```

**本次实测结果**：

- 结果数量：`93`
- 最新行情时间：`2026-03-25`
- 最新财报季度：`2025-09-30`
- 条件来源：`low-valuation-high-dividend.json`
- 排序方式：按 `PE-TTM(扣非)统计值(10年)·分位点%` 升序

该模板最适合作为第一轮候选池，条件包括：

- `PE-TTM(扣非)统计值` 10 年分位点 ≤ `30`
- `PB(不含商誉)统计值` 10 年分位点 ≤ `30`
- `股息率` ≥ `2.5%`
- `上市日期` ≤ `2015-01-01`
- 排除 ST、退市、黑名单

### B. 自然语言快速试错

```bash
cd /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/lixinger-screener
node request/fetch-lixinger-screener.js \
  --query "PE-TTM(扣非)统计值10年分位点小于30%，PB(不含商誉)统计值10年分位点小于30%，股息率大于2.5%，上市日期早于2015-01-01" \
  --output markdown
```

**本次实测结果**：

- 结果数量：`93`
- 最新行情时间：`2026-03-25`
- 最新财报季度：`2025-09-30`

说明：

- 与主模板命中的股票集合一致
- 展示顺序与 `--input-file` 版本不同
- 如果要复现固定排序、写入报告或导出 CSV，优先用 `--input-file`

### C. 收窄模板：横盘后大跌

```bash
cd /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/lixinger-screener
node request/fetch-lixinger-screener.js \
  --input-file low-val-dividend-dip.json \
  --output markdown
```

**本次实测结果**：

- 结果数量：`11`
- 最新行情时间：`2026-03-25`
- 最新财报季度：`2025-09-30`

在主模板基础上额外加入：

- `过去250个交易日涨跌幅` 介于 `-20%` 和 `20%`
- `过去20个交易日涨跌幅` ≤ `-10%`

适合从“便宜”进一步缩到“近期明显回撤”的候选股。

### D. 收窄模板：横盘后大跌 + 现金流质量

```bash
cd /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/lixinger-screener
node request/fetch-lixinger-screener.js \
  --input-file low-val-dividend-dip-cashflow.json \
  --output markdown
```

**本次实测结果**：

- 结果数量：`9`
- 最新行情时间：`2026-03-25`
- 最新财报季度：`2025-09-30`

该模板在上一版基础上增加：

- `PCF-TTM` ≤ `15`

**实测注意**：仅设置 `max: 15` 会让负值 `PCF-TTM` 也通过筛选。
如果你的目标是“现金流为正且估值不高”，应把条件改成同时满足：

- `PCF-TTM >= 0`
- `PCF-TTM <= 15`

## 推荐参数文件

| 文件 | 用途 | 当前实测结果数 |
|------|------|----------------|
| `low-valuation-high-dividend.json` | 第一轮低估值候选池 | `93` |
| `low-val-dividend-dip.json` | 从候选池中找近期大跌标的 | `11` |
| `low-val-dividend-dip-cashflow.json` | 再加一层现金流估值约束 | `9` |
| `unified-input.example.json` | 最小可运行示例 | 未单独复跑 |

## 导出建议

### 导出 CSV

```bash
cd /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/lixinger-screener
node request/fetch-lixinger-screener.js \
  --input-file low-valuation-high-dividend.json \
  --output csv
```

### 保存成最终请求体，便于排查

```bash
cd /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/lixinger-screener
node request/fetch-lixinger-screener.js \
  --input-file low-valuation-high-dividend.json \
  --save-request-body ./data/undervalued-request-body.json \
  --output table-json
```

## 与旧版查询方式的差异

旧版文档中的这些描述已经不再准确：

- 不再默认限定 `沪深300` 成分股
- 不再依赖 `query_tool.py` 手工拆分 `index / fundamental / fs` 三类接口
- 数据时间不再手工填写固定日期，而是由筛选器接口返回最新可用日期
- request 版会自动翻页并汇总全部结果，不需要手工处理“每次 100 只”的分页问题

## 给本 skill 的使用建议

对于 `undervalued-stock-screener`，建议按下面顺序使用数据：

1. 先跑 `low-valuation-high-dividend.json` 拿第一轮候选池
2. 如果结果太多，再切到 `low-val-dividend-dip.json`
3. 如果想加强现金流约束，再用 `low-val-dividend-dip-cashflow.json`，并补上 `PCF-TTM >= 0`
4. 最终在报告中补充行业比较、低估原因和风险分析

