# 数据获取指南

资金流向监控使用**理杏仁API**获取融资融券、北向资金、成交流量等数据。

---

## 核心数据接口列表

### 1. 个股资金流向指标（核心）

**API**: `cn/company/fundamental/non_financial`

**用途**: 获取个股融资融券、北向资金、成交额等资金相关指标

**查询示例**:
```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"stockCodes": ["300750"], "startDate": "2026-03-17", "endDate": "2026-03-23", "metricsList": ["fnpa", "fb", "mm_nba", "ha_shm", "ta", "to_r", "spc"]}' \
  --columns "date,stockCode,fnpa,fb,mm_nba,ha_shm,ta,to_r,spc" \
  --limit 10
```

**核心指标说明**:

| 指标 | 字段名 | 说明 | 用途 |
|------|--------|------|------|
| 融资净买入 | `fnpa` | 当日融资买入额 - 融资偿还额 | 杠杆资金动向，正值为流入 |
| 融资余额 | `fb` | 累计融资余额 | 杠杆资金存量 |
| 融资买入额 | `fpa` | 当日融资买入金额 | 融资买入强度 |
| 融资偿还额 | `fra` | 当日融资偿还金额 | 融资还款压力 |
| 融券净卖出 | `snsa` | 当日融券卖出量 - 融券偿还量 | 做空力量 |
| 融券余额 | `sb` | 累计融券余额 | 做空存量 |
| 陆股通净买入 | `mm_nba` | 北向资金净买入金额 | 外资动向 |
| 陆股通持仓金额 | `ha_shm` | 北向资金持仓金额 | 外资存量 |
| 陆股通持仓股数 | `ha_sh` | 北向资金持仓股数 | 外资持股量 |
| 成交额 | `ta` | 当日成交金额 | 流动性 |
| 换手率 | `to_r` | 当日换手率 | 交易活跃度 |
| 涨跌幅 | `spc` | 当日涨跌幅 | 价格变动 |

**注意事项**:
- 使用 `startDate` 时只能传入**单个** `stockCodes`
- 批量查询需要循环调用
- 返回的是日频数据

---

### 2. 指数资金流向指标

**API**: `cn/index/fundamental`

**用途**: 获取指数的融资融券、北向资金、成交额等汇总数据

**查询示例**:
```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/fundamental" \
  --params '{"stockCodes": ["000300"], "startDate": "2026-03-17", "endDate": "2026-03-23", "metricsList": ["fnpa", "fb", "mm_nba", "ha_shm", "ta", "to_r", "cpc"]}' \
  --columns "date,fnpa,fb,mm_nba,ha_shm,ta,to_r,cpc" \
  --limit 10
```

**可用指标**:
- 融资相关：`fpa`, `fra`, `fnpa`, `fb`
- 融券相关：`ssa`, `sra`, `snsa`, `sb`
- 北向资金：`ha_shm`, `mm_nba`
- 成交流量：`ta`, `to_r`, `tv`
- 价格：`cp`, `cpc`

**常用指数代码**:
- `000300`: 沪深300
- `000016`: 上证50
- `000905`: 中证500
- `000852`: 中证1000
- `399001`: 深证成指
- `399006`: 创业板指

---

### 3. 指数融资融券汇总

**API**: `cn/index/margin-trading-and-securities-lending`

**用途**: 获取指数的融资融券汇总数据（更简洁）

**查询示例**:
```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/margin-trading-and-securities-lending" \
  --params '{"stockCode": "000300", "startDate": "2026-03-17", "endDate": "2026-03-23"}' \
  --columns "date,financingBalance,securitiesBalance,financingBalanceToMarketCap" \
  --limit 10
```

**返回字段**:
- `financingBalance`: 融资余额
- `securitiesBalance`: 融券余额
- `financingBalanceToMarketCap`: 融资余额占流通市值比例

---

### 4. 行业融资融券数据

**API**: `cn/industry/margin-trading-and-securities-lending/sw_2021`

**用途**: 获取申万行业的融资融券数据，用于行业资金流向分析

**查询示例**:
```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry/margin-trading-and-securities-lending/sw_2021" \
  --params '{"stockCode": "490000", "startDate": "2026-03-17"}' \
  --columns "date,financingBalance,securitiesBalance,financingBalanceToMarketCap" \
  --limit 10
```

**常用行业代码（申万一级）**:
- `490000`: 非银金融
- `480000`: 银行
- `340000`: 食品饮料
- `630000`: 电气设备（新能源）
- `270000`: 电子
- `640000`: 计算机
- `230000`: 钢铁
- `330000`: 房地产
- `350000`: 家用电器
- `420000`: 医药生物
- `450000`: 公用事业
- `710000`: 传媒
- `280000`: 汽车
- `240000`: 有色金属
- `220000`: 基础化工

---

### 5. 行业成分股列表

**API**: `cn/industry/constituents/sw_2021`

**用途**: 获取行业板块的成分股，用于板块内资金流向分析

**查询示例**:
```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry/constituents/sw_2021" \
  --params '{"stockCode": "490000", "date": "2026-03-21"}' \
  --columns "stockCode,stockName,weight" \
  --limit 50
```

**用途**: 
- 获取板块龙头个股
- 分析板块内资金集中程度

---

### 6. K线数据（价格验证）

**API**: `cn/index/candlestick` 或 `cn/company/candlestick`

**用途**: 获取K线数据，用于验证资金流向与价格的背离

**查询示例**:
```bash
# 指数K线
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/candlestick" \
  --params '{"stockCode": "000300", "startDate": "2026-03-17", "endDate": "2026-03-23", "type": "normal"}' \
  --columns "date,close,change,volume,amount" \
  --limit 10

# 个股K线
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCode": "300750", "startDate": "2026-03-17", "endDate": "2026-03-23"}' \
  --columns "date,close,change,volume,amount,to_r" \
  --limit 10
```

**返回字段**:
- `date`: 日期
- `open`: 开盘价
- `close`: 收盘价
- `high`: 最高价
- `low`: 最低价
- `change`: 涨跌幅
- `volume`: 成交量
- `amount`: 成交额
- `to_r`: 换手率（个股）

---

### 7. 市场宽度数据

**API**: `cn/market/breadth`

**用途**: 获取市场宽度数据，辅助判断资金分布

**查询示例**:
```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/market/breadth" \
  --params '{"date": "2026-03-21"}' \
  --columns "date,upCount,downCount,limitUpCount,limitDownCount" \
  --limit 10
```

**返回字段**:
- `upCount`: 上涨家数
- `downCount`: 下跌家数
- `limitUpCount`: 涨停家数
- `limitDownCount`: 跌停家数
- `advancesToDeclinesRatio`: 涨跌比

---

### 8. 大盘资金流向（交易所汇总）

**API**: `cn/market/overview`

**用途**: 获取上交所/深交所的整体市场数据

**查询示例**:
```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/market/overview" \
  --params '{"exchange": "sh", "startDate": "2026-03-17", "endDate": "2026-03-23"}' \
  --columns "date,totalAmount,totalVolume,turnover" \
  --limit 10
```

**返回字段**:
- `totalAmount`: 总成交额
- `totalVolume`: 总成交量
- `turnover`: 换手率

---

## 核心指标计算

### 资金流向指标

| 指标 | 公式 | 说明 |
|------|------|------|
| 融资净买入 | fnpa = fpa - fra | 杠杆资金日度动向 |
| N日累计融资净买入 | Σ(fnpa) over N days | 趋势性资金流向 |
| 融资强度 | fnpa / ta × 100% | 融资资金参与度 |
| 融资余额占比 | fb / 流通市值 × 100% | 杠杆水平 |
| 北向资金强度 | mm_nba / ta × 100% | 外资参与度 |
| 成交活跃度 | ta / 流通市值 × 100% | 换手情况 |

### 背离检测

| 指标 | 公式 | 说明 |
|------|------|------|
| 资金-价格背离 | sign(fnpa) != sign(spc) | 融资资金与价格不同向 |
| 持续背离天数 | 连续背离的交易日数 | 背离持续性 |
| 北向-指数背离 | sign(mm_nba) != sign(cpc) | 外资与大盘不同向 |

### 阈值参考

| 指标 | 阈值 | 说明 |
|------|------|------|
| 融资净流入 | > 0 | 杠杆资金流入 |
| 融资强度 | > 3% | 融资参与度较高 |
| 融资余额占比 | > 10% | 杠杆水平较高，注意强平风险 |
| 北向净流入 | > 50亿 | 外资大幅流入（沪深合计） |
| 成交额变化 | > 20% | 成交显著放量 |

---

## 批量查询脚本

### 批量查询多只股票的资金流向
```bash
#!/bin/bash
stocks=("300750" "600519" "000858" "601398" "600036")
start_date="2026-03-17"
end_date="2026-03-23"

for stock in "${stocks[@]}"; do
  echo "=== 查询 ${stock} ==="
  python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
    --suffix "cn/company/fundamental/non_financial" \
    --params "{\"stockCodes\": [\"${stock}\"], \"startDate\": \"${start_date}\", \"endDate\": \"${end_date}\", \"metricsList\": [\"fnpa\", \"fb\", \"mm_nba\", \"ha_shm\", \"ta\", \"to_r\", \"spc\"]}" \
    --columns "date,stockCode,fnpa,fb,mm_nba,ha_shm,ta,to_r,spc" \
    --limit 10
  echo ""
done
```

### 批量查询多个行业的融资融券
```bash
#!/bin/bash
industries=("490000" "480000" "340000" "630000" "270000")
date="2026-03-21"

for industry in "${industries[@]}"; do
  echo "=== 查询行业 ${industry} ==="
  python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
    --suffix "cn/industry/margin-trading-and-securities-lending/sw_2021" \
    --params "{\"stockCode\": \"${industry}\", \"startDate\": \"${date}\"}" \
    --columns "date,financingBalance,securitiesBalance,financingBalanceToMarketCap" \
    --limit 5
  echo ""
done
```

---

## 数据限制与替代

### 理杏仁没有的数据

| 数据 | 说明 | 替代方案 |
|------|------|----------|
| 主力资金流向 | 超大单/大单/中单/小单净流入 | 使用融资净买入+北向资金 |
| 板块资金流向排名 | 行业/概念板块资金排名 | 使用行业融资融券数据 |
| 实时资金流向 | 盘中实时资金动向 | 使用日频数据，T日晚间更新 |
| 概念板块数据 | 同花顺/东方财富概念板块 | 使用申万行业替代 |

### 替代指标映射

| 原始需求 | 替代指标 | 数据源 |
|----------|----------|--------|
| 主力净流入 | 融资净买入 (fnpa) | 理杏仁 |
| 散户净流入 | 无法直接获取 | 用成交额-融资净买入估算 |
| 北向资金净流入 | 陆股通净买入 (mm_nba) | 理杏仁 |
| 板块资金流入 | 行业融资余额变化 | 理杏仁 |

---

## 数据更新时间

- **融资融券数据**: T+1日更新（通常在T日晚间20:00后）
- **北向资金数据**: T日盘后更新
- **K线数据**: 实时更新
- **市场宽度数据**: T日盘后更新

---

## 完整分析所需数据清单

执行完整的资金流向分析，需要获取以下数据：

### 1. 大盘层面
- [ ] 沪深300资金流向（`cn/index/fundamental`）
- [ ] 市场宽度数据（`cn/market/breadth`）
- [ ] 交易所成交概况（`cn/market/overview`）

### 2. 行业层面
- [ ] 申万行业融资融券数据（`cn/industry/margin-trading-and-securities-lending/sw_2021`）
- [ ] 行业成分股列表（`cn/industry/constituents/sw_2021`）

### 3. 个股层面
- [ ] 龙头个股资金流向（`cn/company/fundamental/non_financial`）
- [ ] 个股K线数据（`cn/company/candlestick`）

### 4. 时间窗口建议
- 短期：1日、5日
- 中期：10日、20日
- 趋势：60日

---

## 参考文档

- 理杏仁API文档: `plugins/query_data/lixinger-api-docs/api-docs/`
- 查询工具: `plugins/query_data/lixinger-api-docs/scripts/query_tool.py`
- 方法论文档: `references/methodology.md`
- 输出模板: `references/output-template.md`
