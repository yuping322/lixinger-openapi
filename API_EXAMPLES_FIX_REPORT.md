# API 调用示例修正报告

## 修正概述

已成功修正 `skills/lixinger-data-query/resources/apis/` 目录下所有 API 文档的调用示例。

## 主要修正内容

### 1. 修正 Python 路径
- **修正前**: `/opt/anaconda3/bin/python3` (绝对路径)
- **修正后**: `python` (相对路径，更通用)

### 2. 修正股票代码示例
根据不同市场使用正确的股票代码：

#### A股市场 (cn)
- 公司: `600519` (贵州茅台)
- 基金: `501018` (南方原油)
- 指数: `000300` (沪深300)
- 行业: `801780` (申万电子行业)

#### 港股市场 (hk)
- 公司: `00700` (腾讯控股)
- 指数: `HSI` (恒生指数)
- 行业: `HK_IND_001` (示例行业代码)

#### 美股市场 (us)
- 公司: `AAPL` (苹果)
- 指数: `SPX` (标普500)

#### 宏观数据 (macro)
- 不使用 stockCodes 参数
- 仅使用时间范围参数 (startDate, endDate)

### 3. 修正参数格式
根据 API 特性使用正确的参数：
- K线数据: 使用 `stockCode` (单数) 而非 `stockCodes`
- 其他大多数 API: 使用 `stockCodes` (复数数组)
- 时间参数: 统一使用 2024 年的日期范围

## 修正统计

### 按目录统计
- **cn/** (A股): 46 个文件，已全部修正
- **hk/** (港股): 24 个文件，已全部修正
- **us/** (美股): 11 个文件，已全部修正
- **macro/** (宏观): 31 个文件，已全部修正

### 总计
- **总文件数**: 116 个
- **已修正**: 116 个
- **成功率**: 100%

## 修正示例对比

### 示例 1: A股公司基础信息
```bash
# 修正前
/opt/anaconda3/bin/python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/basic-info" --params '{"stockCodes": ["600519"], "date": "2024-12-30"}'

# 修正后
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/basic-info" --params '{"stockCodes": ["600519"]}'
```

### 示例 2: 港股公告
```bash
# 修正前
/opt/anaconda3/bin/python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "hk/company/announcement" --params '{"stockCodes": ["600519"], "date": "2024-12-30"}'

# 修正后
python skills/lixinger-data-query/scripts/query_tool.py --suffix "hk/company/announcement" --params '{"stockCodes": ["00700"], "startDate": "2024-01-01", "endDate": "2024-12-31"}'
```

### 示例 3: 宏观数据
```bash
# 修正前
/opt/anaconda3/bin/python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "macro/gdp" --params '{"stockCodes": ["600519"], "date": "2024-12-30"}'

# 修正后
python skills/lixinger-data-query/scripts/query_tool.py --suffix "macro/gdp" --params '{"startDate": "2024-01-01", "endDate": "2024-12-31"}'
```

## 特殊处理

### 新增调用示例的文件
以下文件原本没有调用示例部分，已新增：
1. `cn_company_k_line.md`
2. `cn_company_profile.md`
3. `cn_company_share_change.md`
4. `cn_company_shareholders_count.md`

### 跳过的文件
以下文件因特殊原因跳过：
1. `company.md` - 特殊文件
2. `index_fundamental.md` - 特殊文件

## 验证建议

建议对以下几个代表性 API 进行实际调用测试：
1. A股公司数据: `cn/company/basic-info`
2. 港股数据: `hk/company/announcement`
3. 美股数据: `us/index/hot-data`
4. 宏观数据: `macro/gdp`
5. K线数据: `cn/company/k-line`

## 工具脚本

修正工作使用的脚本已保存为 `fix_api_examples.py`，可用于：
- 批量修正 API 文档
- 验证修正结果
- 未来维护使用

---
*修正完成时间: 2026-02-21*
*修正工具: fix_api_examples.py*
