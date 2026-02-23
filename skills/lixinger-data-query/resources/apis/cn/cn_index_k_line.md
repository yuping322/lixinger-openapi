# API 规范: cn/index/candlestick (A股指数K线数据)

获取A股指数历史价格数据（K线）

## 接口地址
- **URL 后缀**: `cn/index/candlestick`
- **支持格式**: `cn.index.candlestick`

## 查询参数 (query_params)

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `stockCode` | string | 是 | 指数代码，如 `"000300"` (沪深300) |
| `type` | string | 是 | K线类型，枚举值：`normal`（价格指数）或 `total_return`（全收益指数） |
| `date` | string | 否 | 指定日期 (YYYY-MM-DD) |
| `startDate` | string | 否 | 起始时间 (YYYY-MM-DD) |
| `endDate` | string | 否 | 结束时间 (YYYY-MM-DD)，时间跨度不超过10年 |
| `limit` | number | 否 | 返回最近数据的数量 |

## 返回字段 (data)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `date` | date | 数据时间 |
| `stockCode` | string | 指数代码 |
| `open` | number | 开盘价 |
| `close` | number | 收盘价 |
| `high` | number | 最高价 |
| `low` | number | 最低价 |
| `volume` | number | 成交量 |
| `amount` | number | 成交额 |
| `change` | number | 涨跌幅 |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/index/candlestick" --params '{"stockCode": "000300", "startDate": "2024-01-01", "endDate": "2024-12-31", "type": "normal"}'
```
