# API 规范: us/index/candlestick (美股指数K线数据)

获取美股指数历史价格数据（K线）

## 接口地址
- **URL 后缀**: `us/index/candlestick`
- **支持格式**: `us.index.candlestick`

## 查询参数 (query_params)

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `stockCode` | string | 是 | 指数代码，如 `".INX"` |
| `type` | string | 是 | `normal` (价格) 或 `total_return` (总回报) |
| `date` | string | 否 | 指定日期 (YYYY-MM-DD) |
| `startDate` | string | 否 | 起始时间 (YYYY-MM-DD) |
| `endDate` | string | 否 | 结束时间 (YYYY-MM-DD) |
| `limit` | number | 否 | 最新数据点数量 |

## 返回字段

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `date` | string | 日期 |
| `open` | number | 开盘价 |
| `close` | number | 收盘价 |
| `high` | number | 最高价 |
| `low` | number | 最低价 |
| `volume` | number | 成交量 |

## 调用示例
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "us/index/candlestick" --params '{"stockCode": ".INX", "type": "normal", "startDate": "2024-01-01", "endDate": "2024-01-31"}'
```
