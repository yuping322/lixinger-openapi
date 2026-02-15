# API 规范: hk/industry/fundamental (港股行业基本面数据)

获取港股行业基本面数据

## 接口地址
- **URL 后缀**: `hk/industry/fundamental`
- **支持格式**: `hk.industry.fundamental`

## 查询参数 (query_params)
大多数 API 遵循以下参数结构，根据具体需求选择：

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `stockCodes` | list | 是 | 股票代码列表，如 `["600519", "000001"]` |
| `date` | string | 否 | 指定日期 (YYYY-MM-DD) |
| `startDate` | string | 否 | 起始时间 (YYYY-MM-DD) |
| `endDate` | string | 否 | 结束时间 (YYYY-MM-DD) |
| `metricsList` | list | 否 | 指标列表，如 `["pe_ttm", "mc"]` |

## 调用示例
```bash
/opt/anaconda3/bin/python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "hk/industry/fundamental" --params '{"stockCodes": ["600519"], "date": "2024-12-30"}'
```
