# 数据获取指南（港股）

使用 `query_tool.py` 获取 valuation-regime-detector 所需的数据。

---

## 查询示例

### 查询HK.Company.Fundamental.Non Financial

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "hk/company/fundamental/non_financial" \
  --params '{"date": "2025-12-31", "stockCodes": ["00700", "00005", "01299"], "metricsList": ["pe_ttm", "pb", "dyr", "mc"]}' \
  --columns "date,stockCode,pe_ttm,pb,dyr,mc" \
  --limit 20
```

### 查询HK.Index.Fundamental

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "hk/index/fundamental" \
  --params '{"date": "2026-02-24", "stockCodes": ["HSI"], "metricsList": ["pe_ttm.mcw", "pb.mcw", "dyr.mcw", "mc"]}' \
  --columns "date,stockCode,pe_ttm.mcw,pb.mcw,dyr.mcw,mc" \
  --limit 20
```

### 查询南向资金流向（港股通）

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "hk/southbound/flow" \
  --params '{"startDate": "2026-01-01", "endDate": "2026-02-24"}' \
  --columns "date,netInflow,buyAmount,sellAmount" \
  --limit 30
```

---

## 参数说明

- `--suffix`: API 路径（参考下方可用 API 列表）
- `--params`: JSON 格式参数
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件
- `--limit`: 限制返回行数

---

## 本 Skill 常用 API

- `hk/company/fundamental/non_financial`
- `hk/index/fundamental`
- `hk/southbound/flow`（南向资金流向）

---

## 港股代码规范

港股代码使用5位数字，例如：
- `00700`: 腾讯控股
- `00005`: 汇丰控股
- `01299`: 友邦保险
- `HSI`: 恒生指数

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../../plugins/query_data/lixinger-api-docs/SKILL.md`

---

## 数据缺失处理

如果某些港股数据缺失：
1. 检查股票代码格式（是否使用5位数字）
2. 使用中国市场的同类数据作为参考（如有AH股）
3. 使用成交量变化作为资金流向的代理指标