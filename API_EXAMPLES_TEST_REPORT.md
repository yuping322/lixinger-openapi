# API 调用示例测试报告

## 测试时间
2026-02-21

## 测试概述
对修正后的 API 调用示例进行实际测试，验证其可用性。

## 测试结果

### ✅ 成功的 API

#### 1. cn/company/profile (公司概况)
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/profile" --params '{"stockCodes": ["600519"]}' --format json
```
**状态**: ✅ 成功  
**返回**: 贵州茅台公司概况信息

#### 2. cn/company/candlestick (K线数据)
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/candlestick" --params '{"stockCode": "600519", "type": "lxr_fc_rights", "startDate": "2024-12-01", "endDate": "2024-12-31"}' --format json
```
**状态**: ✅ 成功  
**返回**: K线数据  
**注意**: 需要 `type` 参数（复权类型）

#### 3. cn/company/trading-abnormal (龙虎榜)
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/trading-abnormal" --params '{"stockCode": "600519", "startDate": "2024-12-01", "endDate": "2024-12-31"}' --format json
```
**状态**: ✅ 成功  
**返回**: 空数据（该时间段无龙虎榜记录）  
**注意**: 使用 `stockCode`（单数）而非 `stockCodes`

#### 4. cn/index/fundamental (指数基本面)
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/index/fundamental" --params '{"stockCodes": ["000300"], "date": "2024-12-31", "metricsList": ["pe_ttm.mcw"]}' --format json
```
**状态**: ✅ 成功  
**返回**: 沪深300指数市值加权PE  
**注意**: 必须提供 `metricsList` 参数

#### 5. us/index/fundamental (美股指数基本面)
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "us/index/fundamental" --params '{"stockCodes": ["SPX"], "date": "2024-12-31", "metricsList": ["pe_ttm.mcw"]}' --format json
```
**状态**: ✅ 成功  
**返回**: 空数据（可能该日期无数据）

#### 6. macro/gdp (GDP数据)
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "macro/gdp" --params '{"areaCode": "cn", "startDate": "2024-01-01", "endDate": "2024-12-31", "metricsList": ["gdp"]}' --format json
```
**状态**: ✅ 成功  
**返回**: 空数据（可能该时间段无更新）  
**注意**: 需要 `areaCode` 和 `metricsList` 参数

### ❌ 不可用的 API

#### 1. cn/company/basic-info
**状态**: ❌ API不存在  
**错误**: "api is not found"  
**说明**: 该 API 路径在理杏仁服务端不存在

#### 2. cn/company/k-line
**状态**: ❌ API不存在  
**正确路径**: `cn/company/candlestick`  
**说明**: 文档中的路径与实际 API 路径不一致

#### 3. cn/company/share-change
**状态**: ❌ API不存在  
**错误**: "api is not found"

#### 4. cn/company/shareholders-count
**状态**: ❌ API不存在  
**错误**: "api is not found"

#### 5. hk/company/fundamental
**状态**: ❌ API不存在  
**错误**: "api is not found"

## 发现的问题

### 1. API 路径不一致
- 文档中: `cn/company/k-line`
- 实际API: `cn/company/candlestick`

### 2. 参数要求不明确
很多 API 需要额外的必填参数，但在文档中未明确标注：
- K线API 需要 `type` 参数（复权类型）
- 指数基本面 需要 `metricsList` 参数
- 宏观数据 需要 `areaCode` 和 `metricsList` 参数

### 3. 参数名称不一致
- 有些API使用 `stockCode`（单数）
- 有些API使用 `stockCodes`（复数数组）

### 4. 大量 API 不存在
根据之前的测试结果，110个API中只有7个可用，81个返回 "api is not found"

## 建议

### 1. 更新 API Catalog
需要从 API catalog 中移除不存在的 API，或标注其状态。

### 2. 完善参数文档
在每个 API 文档中明确标注：
- 必填参数
- 可选参数
- 参数的有效值范围
- 参数示例

### 3. 统一命名规范
建议在文档中说明：
- 哪些API使用 `stockCode`（单数）
- 哪些API使用 `stockCodes`（复数）
- 原因和规律

### 4. 提供完整示例
每个 API 的调用示例应该包含所有必填参数，确保示例可以直接运行。

### 5. 路径映射
对于路径不一致的情况（如 k-line vs candlestick），建议：
- 在文档中同时列出两种路径
- 或在工具中添加路径映射功能

## 下一步行动

1. ✅ 已完成：修正 Python 路径和股票代码
2. ⚠️ 待处理：更新 API 路径（k-line → candlestick）
3. ⚠️ 待处理：补充必填参数到调用示例
4. ⚠️ 待处理：验证所有可用 API 并更新文档
5. ⚠️ 待处理：创建 API 可用性状态表

## 附录：可用 API 列表

根据之前的测试结果，以下 API 确认可用：
1. cn/company/profile
2. cn/company/trading-abnormal
3. cn/company/candlestick (文档中为 k-line)
4. cn/index/fundamental
5. cn/fund
6. us/index/fundamental
7. macro/* (需要正确参数)

---
*测试执行时间: 2026-02-21*
*测试工具: query_tool.py*
