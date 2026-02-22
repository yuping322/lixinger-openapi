# API 规范: cn/fund (基金基础信息)

获取基金基础信息数据

## 接口地址
- **URL 后缀**: `cn/fund`
- **支持格式**: `cn.fund`

## 查询参数 (query_params)
| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `stockCodes` | list | 是 | 基金代码列表，如 `["510300", "159915"]` |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/fund" --params '{"stockCodes": ["510300"]}'
```
