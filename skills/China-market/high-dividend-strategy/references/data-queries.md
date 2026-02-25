# 数据获取指南

使用 `query_tool.py` 获取 high-dividend-strategy 所需的数据。

---

## 查询示例

### 查询 Cn.Company.Dividend

**API 路径**: `cn/company/dividend`

**必需参数**: 
- `stockCode`: 股票代码（单个）
- `startDate` 或 `date`: 日期

**参数限制**:
- ⚠️ 此 API 只接受单个 `stockCode`（不是数组）
- 建议使用 `startDate` 查询历史分红记录

**查询示例**:

```bash
# 示例 1: 查询单个股票的历史分红（推荐）
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/dividend" \
  --params '{"stockCode": "600519", "startDate": "2020-01-01", "endDate": "2024-12-31"}' \
  --columns "date,dividend,dividendAmount,annualNetProfitDividendRatio,exDate" \
  --limit 20

# 示例 2: 查询多个股票的分红数据（需要循环）
for code in 600519 000858 601398; do
  python3 skills/lixinger-data-query/scripts/query_tool.py \
    --suffix "cn/company/dividend" \
    --params "{\"stockCode\": \"${code}\", \"startDate\": \"2020-01-01\"}" \
    --columns "date,stockCode,dividend,dividendAmount" \
    > dividend_${code}.csv
done
```

**常用字段**:
- `date`: 分红日期
- `dividend`: 每股分红（元）
- `dividendAmount`: 分红总额（万元）
- `annualNetProfitDividendRatio`: 分红率（%）
- `exDate`: 除权除息日
- `dividendYield`: 股息率（%）

**常见错误**:

❌ **错误**: 使用 stockCodes 数组
```bash
--params '{"stockCodes": ["600519", "000858"], "startDate": "2020-01-01"}'
```
✅ **正确**: 使用单个 stockCode
```bash
--params '{"stockCode": "600519", "startDate": "2020-01-01"}'
```

---

## 参数说明

- `--suffix`: API 路径（使用斜杠格式，如 `cn/company/dividend`）
- `--params`: JSON 格式参数（注意内层使用双引号）
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件（如 `"dividend > 1"`）
- `--limit`: 限制返回行数

---

## 本 Skill 常用 API

- `cn/company/dividend`: 分红数据
- `cn/company/fundamental/non_financial`: 基本面数据（需要 metricsList）

---

## 查找更多 API

```bash
# 查看完整 API 列表
cat skills/lixinger-data-query/SKILL.md

# 搜索关键字
grep -r "关键字" skills/lixinger-data-query/api_new/api-docs/

# 查看具体 API 文档
cat skills/lixinger-data-query/api_new/api-docs/{api_name}.md
```

**相关文档**: `skills/lixinger-data-query/SKILL.md`
