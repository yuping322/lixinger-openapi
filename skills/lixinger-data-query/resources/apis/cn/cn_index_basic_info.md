# API 规范: cn/index (指数基础信息)

获取指数基础信息数据

## 接口地址
- **URL 后缀**: `cn/index`
- **支持格式**: `cn.index`

## 查询参数 (query_params)
| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `stockCodes` | list | 是 | 指数代码列表，如 `["000300", "000001"]` |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/index" --params '{"stockCodes": ["000300"]}'
```
