# China-market Skills Data-Queries 匹配度分析报告

**分析日期**: 2026-02-27  
**分析范围**: `/Users/fengzhi/Downloads/git/lixinger-openapi/skills/China-market`  
**Skills 总数**: 57

---

## 执行摘要

### 整体状况

✅ **所有 57 个 skills 都具备完整的文档结构**
- 100% 的 skills 拥有 `SKILL.md`
- 100% 的 skills 拥有 `references/data-queries.md`
- 100% 的 data-queries.md 包含可执行的 API 示例

### 关键发现

1. **API 覆盖度**: 共使用 30 个不同的 API 端点
2. **示例质量**: 所有 data-queries.md 都提供了可执行的命令示例
3. **格式统一**: 所有示例都遵循统一的 `query_tool.py` 调用格式
4. **参数完整**: 大部分示例包含 `--params`、`--columns` 等关键参数

### 主要问题

⚠️ **数据需求覆盖不完整**
- 部分 skills 的 data-queries.md 未能完全覆盖 SKILL.md 中提到的所有数据需求
- 某些特定数据类型（如涨停数据、龙虎榜、质押等）缺少直接的 API 示例

---

## API 使用统计

### 高频 API（使用次数 ≥ 5）

| API 端点 | 使用次数 | 主要用途 |
|---------|---------|---------|
| `cn/company/fundamental/non_financial` | 25 | 公司基本面数据（估值、财务指标） |
| `cn/company/candlestick` | 11 | K线数据（价格、成交量） |
| `cn/company` | 11 | 公司基本信息 |
| `cn/index/fundamental` | 8 | 指数基本面数据 |
| `cn/index/candlestick` | 5 | 指数K线数据 |

### 中频 API（使用次数 2-4）

| API 端点 | 使用次数 | 主要用途 |
|---------|---------|---------|
| `macro/money-supply` | 4 | 货币供应量 |
| `us/index/fundamental` | 4 | 美股指数基本面 |
| `cn/company/shareholders-num` | 3 | 股东人数 |
| `cn/company/major-shareholders-shares-change` | 3 | 大股东持股变动 |
| `cn/industry` | 3 | 行业数据 |
| `cn/company/block-deal` | 2 | 大宗交易 |
| `cn/company/dividend` | 2 | 分红数据 |
| `cn/company/trading-abnormal` | 2 | 龙虎榜数据 |
| `cn/index/constituents` | 2 | 指数成分股 |
| `cn/company/fs/non_financial` | 2 | 财务报表 |
| `cn/company/operation-revenue-constitution` | 2 | 营收构成 |
| `macro/price-index` | 2 | 价格指数（CPI/PPI） |
| `macro/gdp` | 2 | GDP 数据 |

### 低频 API（使用次数 = 1）

共 15 个 API，包括：
- `cn/company/pledge` - 股权质押
- `cn/company/margin-trading-and-securities-lending` - 融资融券
- `cn/company/senior-executive-shares-change` - 高管持股变动
- `cn/company/inquiry` - 问询函
- `cn/company/measures` - 监管措施
- 等等

---

## 详细案例分析

### 案例 1: single-stock-health-check（个股健康检查）

**数据需求关键词**:
- ✅ fundamental（基本面）
- ✅ shareholder（股东）
- ⚠️ dividend（分红）- 未提供示例
- ⚠️ valuation（估值）- 未提供示例
- ⚠️ pledge（质押）- 未提供示例
- ⚠️ margin（融资融券）- 未提供示例
- ⚠️ industry（行业）- 未提供示例
- ⚠️ limit_up_down（涨跌停）- 未提供示例
- ⚠️ repurchase（回购）- 未提供示例
- ⚠️ trading_abnormal（龙虎榜）- 未提供示例

**提供的 API 示例**: 11 个
- `cn/company/profile` - 公司概况
- `cn/company/fundamental/non_financial` - 基本面
- `cn/company/fs/non_financial` - 财务报表
- `cn/company/customers` - 客户
- `cn/company/suppliers` - 供应商
- `cn/company/fund-shareholders` - 基金持股
- `cn/company/fund-collection-shareholders` - 基金集合持股
- `cn/company/inquiry` - 问询函
- `cn/company/measures` - 监管措施
- `cn/company/nolimit-shareholders` - 无限售股东
- `cn/company/equity-change` - 股本变动

**评估**:
- ✅ 示例数量丰富（11 个）
- ✅ 覆盖了核心的基本面和股东数据
- ⚠️ 缺少分红、质押、融资融券等风险指标的示例
- ⚠️ 缺少估值和行业对比的示例

**建议**: 补充以下 API 示例
```bash
# 分红数据
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/dividend"

# 质押数据
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/pledge"

# 融资融券
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/margin-trading-and-securities-lending"
```

---

### 案例 2: high-dividend-strategy（高股息策略）

**数据需求关键词**:
- ✅ dividend（分红）
- ✅ index（指数）
- ⚠️ valuation（估值）- 未提供示例
- ⚠️ financial_statement（财务报表）- 未提供示例
- ⚠️ industry（行业）- 未提供示例
- ⚠️ macro（宏观）- 未提供示例

**提供的 API 示例**: 2 个
- `cn/index/constituents` - 指数成分股
- `cn/company/dividend` - 分红数据

**评估**:
- ✅ 核心的分红数据已覆盖
- ✅ 提供了指数成分股筛选
- ⚠️ 缺少估值筛选（PE、PB、股息率）
- ⚠️ 缺少财务质量评估（ROE、负债率等）
- ⚠️ 缺少行业分布分析

**建议**: 补充以下 API 示例
```bash
# 估值数据（含股息率）
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/fundamental/non_financial" --columns "stockCode,name,dyr,pe_ttm,pb,roe"

# 财务报表
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/fs/non_financial" --columns "date,stockCode,totalAssets,totalLiabilities,netProfit"
```

---

### 案例 3: policy-sensitivity-brief（政策敏感度简报）

**数据需求关键词**:
- ⚠️ industry（行业）- 未提供示例
- ⚠️ limit_up_down（涨跌停）- 未提供示例
- ⚠️ macro（宏观）- 未提供示例

**提供的 API 示例**: 3 个
- `cn/company/fundamental/non_financial` - 公司基本面
- `cn/index/fundamental` - 指数基本面（2个示例）

**评估**:
- ⚠️ 示例与需求匹配度较低
- ⚠️ 缺少行业数据
- ⚠️ 缺少宏观经济数据
- ⚠️ 缺少市场情绪数据（涨停板、成交量等）

**建议**: 补充以下 API 示例
```bash
# 行业数据
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/industry"

# 宏观数据
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "macro/money-supply"
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "macro/gdp"

# K线数据（用于计算涨跌停）
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/candlestick" --columns "date,stockCode,close,pctChg"
```

---

### 案例 4: limit-up-pool-analyzer（涨停板分析）

**数据需求关键词**:
- ⚠️ limit_up_down（涨跌停）- 未提供直接示例

**提供的 API 示例**: 2 个
- `cn/company/candlestick` - K线数据
- `cn/company` - 公司基本信息

**评估**:
- ⚠️ 仅提供了 K线数据，需要自行计算涨停
- ⚠️ 缺少涨停原因分析的数据源
- ⚠️ 缺少龙虎榜数据

**建议**: 补充以下 API 示例
```bash
# 龙虎榜数据（涨停股常上榜）
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/trading-abnormal"

# 基本面数据（分析涨停原因）
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/fundamental/non_financial"
```

---

### 案例 5: financial-statement-analyzer（财务报表分析）

**数据需求关键词**:
- ✅ financial_statement（财务报表）
- ⚠️ valuation（估值）- 未提供示例
- ⚠️ shareholder（股东）- 未提供示例
- ⚠️ pledge（质押）- 未提供示例
- ⚠️ goodwill（商誉）- 未提供示例

**提供的 API 示例**: 2 个
- `us/index/fundamental` - 美股指数基本面
- `cn/company/fs/non_financial` - 财务报表

**评估**:
- ✅ 核心的财务报表 API 已提供
- ⚠️ 美股 API 示例与 China-market skill 不匹配
- ⚠️ 缺少估值、股东、质押等配套数据

**建议**: 
1. 移除或替换美股 API 示例
2. 补充以下 API 示例
```bash
# 估值数据
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/fundamental/non_financial" --columns "stockCode,pe_ttm,pb,roe,roa"

# 股东数据
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/major-shareholders-shares-change"

# 质押数据
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/pledge"
```

---

### 案例 6: block-deal-monitor（大宗交易监控）

**数据需求关键词**:
- ✅ block_deal（大宗交易）
- ✅ shareholder（股东）
- ⚠️ lockup（解禁）- 未提供示例
- ⚠️ industry（行业）- 未提供示例

**提供的 API 示例**: 4 个
- `cn/company/block-deal` - 大宗交易
- `cn/company/major-shareholders-shares-change` - 大股东持股变动
- `cn/company/shareholders-num` - 股东人数
- `macro/money-supply` - 货币供应量

**评估**:
- ✅ 核心的大宗交易和股东数据已覆盖
- ⚠️ 宏观数据（货币供应量）与大宗交易的关联性不明确
- ⚠️ 缺少解禁数据
- ⚠️ 缺少行业对比

**建议**: 补充以下 API 示例
```bash
# 行业数据
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/industry"

# 基本面数据（用于分析大宗交易折价率）
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/fundamental/non_financial"
```

---

### 案例 7: etf-allocator（ETF 配置器）

**数据需求关键词**:
- ⚠️ industry（行业）- 未提供示例
- ⚠️ limit_up_down（涨跌停）- 未提供示例

**提供的 API 示例**: 5 个
- `cn/index/fundamental` - 指数基本面（3个重复示例）
- `cn/index/constituents` - 指数成分股
- `cn/index/candlestick` - 指数K线

**评估**:
- ✅ 指数相关数据覆盖完整
- ⚠️ 存在重复示例（3个相同的 fundamental 调用）
- ⚠️ 缺少行业分布数据
- ⚠️ 缺少市场情绪数据

**建议**: 
1. 去除重复的 API 示例
2. 补充以下 API 示例
```bash
# 行业数据
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/industry"

# 成分股基本面
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/fundamental/non_financial"
```

---

### 案例 8: sector-rotation-detector（板块轮动检测）

**数据需求关键词**:
- ✅ macro（宏观）
- ✅ industry（行业）
- ✅ index（指数）
- ⚠️ candlestick（K线）- 未提供示例
- ⚠️ northbound（北向资金）- 未提供示例

**提供的 API 示例**: 5 个
- `macro/money-supply` - 货币供应量
- `macro/price-index` - 价格指数
- `cn/industry` - 行业数据
- `macro/gdp` - GDP
- `cn/index/fundamental` - 指数基本面

**评估**:
- ✅ 宏观和行业数据覆盖完整
- ✅ 示例与需求匹配度高
- ⚠️ 缺少 K线数据（用于计算板块涨跌幅）
- ⚠️ 缺少北向资金流向数据

**建议**: 补充以下 API 示例
```bash
# 指数K线（板块涨跌幅）
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/index/candlestick"

# 公司K线（个股表现）
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/candlestick"
```

---

## 问题分类与统计

### 问题 1: 数据需求覆盖不完整

**影响的 skills**: 约 40 个（70%）

**常见缺失的数据类型**:
1. **涨跌停数据** - 10+ skills 需要但未提供示例
2. **估值数据** - 8+ skills 需要但未提供示例
3. **行业数据** - 8+ skills 需要但未提供示例
4. **宏观数据** - 5+ skills 需要但未提供示例
5. **质押数据** - 4+ skills 需要但未提供示例
6. **龙虎榜数据** - 3+ skills 需要但未提供示例

**根本原因**:
- data-queries.md 主要提供了"如何使用 query_tool.py"的通用示例
- 未针对每个 skill 的具体需求定制示例
- 部分数据需求可能需要组合多个 API 或二次计算

---

### 问题 2: 示例重复或冗余

**影响的 skills**: 约 5 个（9%）

**典型案例**:
- `etf-allocator` 中有 3 个相同的 `cn/index/fundamental` 示例
- 部分 skills 的示例过于通用，缺少针对性

**建议**: 
- 去除重复示例
- 每个示例应展示不同的使用场景或参数组合

---

### 问题 3: API 选择不当

**影响的 skills**: 约 3 个（5%）

**典型案例**:
- `financial-statement-analyzer`（China-market skill）使用了 `us/index/fundamental`（美股 API）
- 部分 skills 使用了与主题关联性不强的 API

**建议**: 
- 审查每个 skill 的 API 选择
- 确保 API 与 skill 的市场范围（中国/美国/香港）一致

---

### 问题 4: 缺少参数说明

**影响的 skills**: 少数（约 10%）

**问题描述**:
- 部分示例缺少 `--columns` 参数，导致返回数据过多
- 部分示例缺少 `--row-filter` 参数，无法展示数据筛选能力

**建议**: 
- 所有示例都应包含 `--columns` 参数
- 复杂查询应展示 `--row-filter` 的使用

---

## 优秀实践

### 示例 1: single-stock-health-check

✅ **优点**:
- 提供了 11 个不同的 API 示例
- 覆盖了公司的多个维度（基本面、财务、股东、监管等）
- 每个示例都包含了 `--columns` 参数

### 示例 2: sector-rotation-detector

✅ **优点**:
- API 选择与需求高度匹配
- 覆盖了宏观、行业、指数三个层面
- 示例数量适中（5个）

### 示例 3: block-deal-monitor

✅ **优点**:
- 核心数据（大宗交易、股东变动）覆盖完整
- 提供了多维度的分析视角

---

## 改进建议

### 短期改进（1-2周）

1. **补充缺失的 API 示例**
   - 优先补充高频缺失的数据类型（涨跌停、估值、行业）
   - 重点关注使用频率高的 skills

2. **去除重复和不当的示例**
   - 清理重复的 API 调用
   - 替换市场范围不匹配的 API

3. **统一示例格式**
   - 所有示例都应包含 `--columns` 参数
   - 添加简短的注释说明每个示例的用途

### 中期改进（1个月）

4. **创建 API 映射表**
   - 建立"数据需求 → API 端点"的映射关系
   - 帮助快速找到合适的 API

5. **增加复杂查询示例**
   - 展示 `--row-filter` 的使用
   - 展示多步骤数据获取流程

6. **添加数据处理示例**
   - 某些需求（如涨停板）需要计算，应提供处理逻辑
   - 可以在 data-queries.md 中添加简单的 Python 代码片段

### 长期改进（2-3个月）

7. **自动化验证**
   - 创建脚本自动检查 data-queries.md 与 SKILL.md 的匹配度
   - 定期运行验证，确保文档同步更新

8. **创建最佳实践指南**
   - 总结优秀的 data-queries.md 案例
   - 为新 skill 的创建提供模板

9. **用户反馈机制**
   - 收集 skills 使用者的反馈
   - 根据实际使用情况优化示例

---

## 结论

### 总体评价

**优点**:
- ✅ 文档结构完整，所有 skills 都有配套的 data-queries.md
- ✅ 示例格式统一，易于理解和使用
- ✅ 核心 API（fundamental、candlestick）覆盖广泛

**不足**:
- ⚠️ 约 70% 的 skills 存在数据需求覆盖不完整的问题
- ⚠️ 部分示例与 skill 需求匹配度较低
- ⚠️ 缺少复杂查询和数据处理的示例

### 优先级建议

**P0（立即处理）**:
1. 补充高频缺失的数据类型示例（涨跌停、估值、行业）
2. 修正市场范围不匹配的 API（如 China-market 中的美股 API）

**P1（1-2周内）**:
3. 去除重复示例
4. 为所有示例添加 `--columns` 参数

**P2（1个月内）**:
5. 创建 API 映射表
6. 增加复杂查询示例

**P3（长期）**:
7. 建立自动化验证机制
8. 创建最佳实践指南

---

## 附录

### 附录 A: 完整的 API 使用统计

详见前文"API 使用统计"部分。

### 附录 B: 建议补充的 API 示例模板

```bash
# 涨停板数据（通过K线计算）
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCodes": ["600519"], "startDate": "2026-02-01", "endDate": "2026-02-27"}' \
  --columns "date,stockCode,close,pctChg" \
  --row-filter "pctChg >= 9.9"

# 估值筛选
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date": "2026-02-27"}' \
  --columns "stockCode,name,pe_ttm,pb,dyr,roe" \
  --row-filter "pe_ttm < 20 and pb < 3 and dyr > 3"

# 行业数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/industry" \
  --params '{"date": "2026-02-27"}' \
  --columns "industryCode,industryName,pe_ttm,pb"

# 质押风险
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/pledge" \
  --params '{"stockCode": "600519"}' \
  --columns "date,pledgeRatio,pledgor"

# 龙虎榜
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/trading-abnormal" \
  --params '{"stockCode": "600519", "startDate": "2026-02-01"}' \
  --columns "date,reason,buyAmount,sellAmount"
```

### 附录 C: 数据需求 → API 映射表

| 数据需求 | 推荐 API | 备注 |
|---------|---------|------|
| 基本面 | `cn/company/fundamental/non_financial` | 包含估值、财务指标 |
| K线数据 | `cn/company/candlestick` | 价格、成交量 |
| 涨跌停 | `cn/company/candlestick` + 计算 | 通过 pctChg 筛选 |
| 财务报表 | `cn/company/fs/non_financial` | 三大报表 |
| 分红 | `cn/company/dividend` | 分红历史 |
| 股东 | `cn/company/major-shareholders-shares-change` | 大股东变动 |
| 质押 | `cn/company/pledge` | 质押比例 |
| 大宗交易 | `cn/company/block-deal` | 大宗交易记录 |
| 龙虎榜 | `cn/company/trading-abnormal` | 异常交易 |
| 融资融券 | `cn/company/margin-trading-and-securities-lending` | 融资融券余额 |
| 行业 | `cn/industry` | 行业估值 |
| 指数 | `cn/index/fundamental` | 指数估值 |
| 宏观 | `macro/money-supply`, `macro/gdp`, `macro/price-index` | 宏观经济指标 |

---

**报告生成**: 自动化分析脚本  
**数据来源**: `/Users/fengzhi/Downloads/git/lixinger-openapi/skills/China-market`  
**分析工具**: Python 3 + 正则表达式
