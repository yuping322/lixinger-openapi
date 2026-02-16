# API 规范: us/index/hot/cp (美股指数热度数据-收盘点位)

获取美股指数价格表现和增长率汇总数据（CAGR）

## 接口地址
- **URL 后缀**: `us/index/hot/cp`
- **支持格式**: `us.index.hot.cp`

## 查询参数 (query_params)

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `stockCodes` | list | 是 | 指数代码列表，如 `[".INX"]` |

## 返回字段

**期间涨跌幅**：
- `cpc_w1` - 近1周涨跌幅
- `cpc_m1` - 近1月涨跌幅
- `cpc_m3` - 近3月涨跌幅
- `cpc_m6` - 近6月涨跌幅
- `cpc_y1` - 近1年涨跌幅
- `cpc_y2` - 近2年涨跌幅
- `cpc_y3` - 近3年涨跌幅
- `cpc_y5` - 近5年涨跌幅

**复合年化增长率 (CAGR)**：
- `cp_cac_y2` - 2年CAGR
- `cp_cac_y3` - 3年CAGR
- `cp_cac_y5` - 5年CAGR
- `cp_cac_y10` - 10年CAGR

## 调用示例
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "us/index/hot/cp" --params '{"stockCodes": [".INX", ".DJI"]}'
```
