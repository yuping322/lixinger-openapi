# API 规范: us/index/constituents (美股指数成分股)

获取美股指数成分股列表

## 接口地址
- **URL 后缀**: `us/index/constituents`
- **支持格式**: `us.index.constituents`

## 查询参数 (query_params)

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `stockCodes` | list | 否 | 指数代码列表，如 `[".INX"]` |
| `date` | string | 是 | `latest` 或指定日期 (YYYY-MM-DD) |

## 返回字段

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `constituents` | array | 成分股列表 |
| `constituents[].stockCode` | string | 股票代码 |
| `constituents[].areaCode` | string | 区域代码 |
| `constituents[].market` | string | 市场 |

## 调用示例
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "us/index/constituents" --params '{"stockCodes": [".INX"], "date": "latest"}'
```
