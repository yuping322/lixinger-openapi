# API 规范: us/index/hot/ifet_sni (美股指数热度数据-场内基金认购净流入)

获取与美股指数相关的场内基金净流入数据

## 接口地址
- **URL 后缀**: `us/index/hot/ifet_sni`
- **支持格式**: `us.index.hot.ifet_sni`

## 查询参数 (query_params)

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `stockCodes` | list | 是 | 指数代码列表，如 `[".INX"]` |

## 返回字段

**净流入数据**：
- `ifet_sni_ytd` - 年初至今净流入
- `ifet_sni_w1` - 近1周净流入
- `ifet_sni_m1` - 近1月净流入
- `ifet_sni_m3` - 近3月净流入
- `ifet_sni_fys` - 本财年以来净流入
- `ifet_as` - 资产规模

## 调用示例
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "us/index/hot/ifet_sni" --params '{"stockCodes": [".INX"]}'
```
