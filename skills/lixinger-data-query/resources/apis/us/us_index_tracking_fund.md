# API 规范: us/index/tracking-fund (美股指数跟踪基金)

获取跟踪特定美股指数的基金信息

## 接口地址
- **URL 后缀**: `us/index/tracking-fund`
- **支持格式**: `us.index.tracking-fund`

## 查询参数 (query_params)

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `stockCode` | string | 是 | 指数代码，如 `".INX"` |

## 返回字段

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `stockCode` | string | 基金代码 |
| `shortName` | string | 基金简称 |
| `areaCode` | string | 区域代码 |
| `market` | string | 市场 |
| `exchange` | string | 交易所 |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "us/index/tracking-fund" --params '{"stockCodes": ["SPX"], "date": "2024-12-31"}'
```
