# API 规范: cn/industry (行业基础信息)

获取行业基础信息数据

## 接口地址
- **URL 后缀**: `cn/industry`
- **支持格式**: `cn.industry`

## 查询参数 (query_params)
| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `stockCodes` | list | 是 | 行业代码列表，如 `["industry_name"]` |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/industry" --params '{"stockCodes": ["申万2021一级"]}'
```
