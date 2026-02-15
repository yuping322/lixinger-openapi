---
name: lixinger-data-query
description: 从理杏仁开放平台获取金融数据，包括股票、指数、基本面和市场信息。
---

# 理杏仁数据查询 Skill

本 Skill 为大语言模型（LLM）提供了一个程序化接口，用于从 [理杏仁开放平台](https://www.lixinger.com/open/api) 获取金融数据。

## 核心功能
- **查询基本面数据**: 获取股票和指数的 PE、PB、市值等财务指标。
- **查询指数数据**: 获取指数成分股、行业权重和指数点位。
- **市场覆盖**: 支持 A 股 (CN)、港股 (HK) 和美股 (US) 市场。
- **数据格式化**: 结果以 JSON 或结构化文本格式返回，便于分析。

## 使用指南

### 1. 发现 API (API Discovery)
本 Skill 采用模块化文档。你可以通过以下两种方式找到需要的接口：

- **快速搜索**: 使用 `grep` 在 **[API 目录 (CSV)](file:///Users/fengzhi/Downloads/git/lixinger-openapi/skills/lixinger-data-query/resources/api_catalog.csv)** 中搜索关键字。
  - 例如: `grep "基本面" skills/lixinger-data-query/resources/api_catalog.csv`
- **目录浏览**: 查阅 **[API 索引 (Markdown)](file:///Users/fengzhi/Downloads/git/lixinger-openapi/skills/lixinger-data-query/resources/api_index.md)** 了解完整分类。

确认接口后，**务必阅读**对应的详细规范文件（如 `cn/company.md`），以确认参数要求。

### 2. 运行查询工具
找到参数规范后，使用 `query_tool.py` 脚本获取数据。

```bash
# 通用查询（例如：查询所有银行股）
/opt/anaconda3/bin/python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn.company" --params '{"fsTableType": "bank"}'

# 查询上证 50 指数基本面数据
/opt/anaconda3/bin/python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn.index.fundamental" --params '{"date": "2024-12-10", "stockCodes": ["000016"], "metricsList": ["pe_ttm.mcw", "mc"]}'
```

### 3. 参数说明
- `--suffix`: API 接口后缀（例如 `cn.company`）。支持使用 `.` 或 `/` 作为分隔符。
- `--params`: JSON 格式的查询参数字符串。`token` 会由工具自动处理。
- `--format`: 输出格式，支持 `text` (默认), `json`, `csv`。

## 常用 API 接口
| 分类 | URL 后缀 | 描述 |
| :--- | :--- | :--- |
| **公司信息** | `cn/company` | 获取 A 股上市公司列表（可用 `fsTableType` 过滤） |
| **指数成分股** | `cn/index/constituents` | 获取特定日期的指数成分股 |
| **指数基本面** | `cn/index/fundamental` | 获取指数的估值指标，如 PE、PB |
| **市场基本面** | `cn/market/fundamental` | 获取整体市场的估值统计数据 |

## 最佳实践与典型工作流

当面临复杂任务时，建议遵循以下“多步工作流”以获得最准的数据：

### 示例：分析特定行业的平均估值
1. **发现代码**：调用 `cn/company` 并使用 `fsTableType` 过滤（如 `bank`）获取相关股票代码。
2. **获取指标**：将获取的代码填入 `cn/index/fundamental` 或 `cn/company/fundamental/bank` 的 `stockCodes` 中。
3. **计算汇总**：拿到数据后，在本地进行平均值运算或其他统计分析。

### LLM 调用建议 (Chain-of-Thought)
- **发现 -> 确认 -> 执行**：先查 `api_catalog.csv` 发现接口，再读具体的 `.md` 确认参数，最后执行。
- **防止溢出**：默认工具会截断前 100 行。如果需要全量数据进行复杂分析，请考虑分批查询或调大 `--limit`。
- **逐步验证**：复杂任务应拆解为多个步骤，每一步验证返回结果后再继续。

## 注意事项
- **通用参数**: 大多数接口支持 `date`, `startDate`, `endDate`, `metricsList` 等参数。详情请查看具体的接口规范。
- **输出截断**: `query_tool.py` 默认 `--limit 100` 以防止 Token 溢出。
- **Token 管理**: 本 Skill 依赖于项目根目录下的 `token.cfg` 文件。
- **成功状态码**: 理杏仁 API 成功请求返回的 `code` 为 `1`。
- **访问限制**:
  - 所有 API 都需要有效的 token。
  - 每个用户有每日访问次数限制（取决于账号等级）。
  - 部分高级数据需额外付费或特定权限。
