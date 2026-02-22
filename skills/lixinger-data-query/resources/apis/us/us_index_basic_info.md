# API 规范: us/index (美股指数信息)

获取美股指数基本信息

## 接口地址
- **URL 后缀**: `us/index`
- **支持格式**: `us.index`

## 查询参数 (query_params)

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `stockCodes` | list | 否 | 指数代码列表，如 `[".INX", ".DJI"]` |

## 返回字段

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `name` | string | 指数名称 |
| `stockCode` | string | 指数代码 |
| `areaCode` | string | 区域代码 |
| `market` | string | 市场 |
| `fsTableType` | string | 财务报表类型 |
| `source` | string | 数据来源 |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "us/index/basic-info" --params '{"stockCodes": ["SPX"]}'
```
