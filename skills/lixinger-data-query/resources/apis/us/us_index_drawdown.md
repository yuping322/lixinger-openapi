# API 规范: us/index/drawdown (美股指数回撤)

获取美股指数历史回撤数据

## 接口地址
- **URL 后缀**: `us/index/drawdown`
- **支持格式**: `us.index.drawdown`

## 查询参数 (query_params)

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `stockCode` | string | 是 | 指数代码，如 `".INX"` |
| `startDate` | string | 否 | 起始时间 (YYYY-MM-DD) |
| `endDate` | string | 否 | 结束时间 (YYYY-MM-DD) |
| `granularity` | string | 否 | `y` (年), `q` (季), 默认为日度 |

## 返回字段

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `date` | string | 日期 |
| `drawdown` | number | 回撤率 |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "us/index/drawdown" --params '{"stockCodes": ["SPX"], "date": "2024-12-31"}'
```
