# API 规范: cn/company/fundamental/non_financial (基本面数据)

获取非金融公司基本面数据

## 接口地址
- **URL 后缀**: `cn/company/fundamental/non_financial`
- **支持格式**: `cn.company.fundamental.non_financial`

## 查询参数 (query_params)
| 参数名 | 类型 | 必选 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户专属 Token |
| `stockCodes` | list | 是 | 股票代码列表 |

## 调用示例
```bash
/opt/anaconda3/bin/python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/fundamental/non_financial" --params '{"stockCodes": ["300750"]}'
```
