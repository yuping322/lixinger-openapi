---
name: findata-toolkit-cn
description: A股金融数据工具包。提供脚本获取A股实时行情、财务指标、董监高增减持、北向资金、宏观经济数据（LPR、CPI/PPI、PMI、社融、M2）。用于需要实时A股市场数据支撑投资分析时。所有数据源免费，无需API密钥。
license: Apache-2.0
---

# 金融数据工具包 — A股市场

自包含的数据工具包，提供A股市场实时金融数据和定量计算。所有数据源**免费**，**无需API密钥**。

## 安装

安装依赖（一次性）：

```bash
pip install -r requirements.txt
```

## 可用工具

所有脚本位于 `scripts/` 目录。从技能根目录运行。

# 金融数据工具包 — A股市场 (Lixinger 版)

自包含的数据工具包，提供 A 股市场实时金融数据、定量计算与筛选。核心引擎已切换至 **理杏仁 (Lixinger)**，支持 DuckDB 缓存与单位自动换算。

## 安装

安装依赖（一次性）：

```bash
pip install -r requirements.txt
```

## 可用工具 (Entity-based)

统一入口脚本：`python scripts/toolkit.py`。该脚本采用“实体聚合”设计，通过极少数调用即可获得高密度数据。

### 1. 个股分析 (`--stock`)
聚合基本面、财务、估值、资金和异动数据。支持 `brief` (摘要) 和 `full` (详尽) 模式。

- `python scripts/toolkit.py --stock 600519` (默认 brief)
- `python scripts/toolkit.py --stock 600519 --mode full` (详细历史与高管变动)

### 2. 基金分析 (`--fund`)
支持公募基金与 ETF。聚合净值、持仓和评级。

- `python scripts/toolkit.py --fund 510300` (沪深 300 ETF)

### 3. 市场概览 (`--market`)
每日复盘必备。聚合指数表现、全市场资金流向。

- `python scripts/toolkit.py --market`

### 4. 板块分析 (`--sector`)
获取行业/概念板块的估值与成分股。

- `python scripts/toolkit.py --sector 申万行业代码`

### 5. 宏观脉搏 (`--macro`)
聚合利率 (LPR)、通胀 (CPI/PPI)、货币供应 (M2/社融) 和 GDP。

- `python scripts/toolkit.py --macro`

### 6. 数据筛选器 (`--screen` / `--sync`)
支持 SQL 风格的大规模选股筛选。

- 同步数据：`python scripts/toolkit.py --sync`
- 筛选：`python scripts/toolkit.py --screen 'pe_ttm < 20 AND industry="白酒"'`

## 输出格式

所有输出均为 **JSON**，包含 `identity` (标识), `valuation` (估值), `metrics` (指标) 等高密度字段，极大降低 LLM 的调用频次并提升理解效率。

## 缓存与数据源

- **数据源**：主要为理杏仁 (Lixinger)，辅以 DuckDB 缓存。
- **配置**：`config/data_sources.yaml` 中设置理杏仁 Token。
