# Data Queries 更新报告

## 任务概述

将所有 China-market skills 中的 `data-queries.md` 文件更新为新版本，强调使用 `lixinger-data-query` skill 的 `query_tool.py` 工具。

---

## 更新内容

### 主要变化

1. **推荐使用 query_tool.py**
   - 将 `query_tool.py` 作为首选数据获取方式
   - 强调增强参数的使用（`--columns`, `--row-filter`, `--flatten`）
   - 提供详细的使用示例和最佳实践

2. **核心优势说明**
   - ✅ 字段过滤：节省 30-40% token
   - ✅ 数据筛选：只返回符合条件的数据
   - ✅ 数组展开：处理嵌套结构
   - ✅ CSV 格式：默认格式，最节省 token
   - ✅ 162 个 API 接口：覆盖全市场数据

3. **丰富的使用示例**
   - 查询股票基本信息
   - 查询 K 线数据
   - 查询分红数据
   - 查询股东人数
   - 查询公告信息
   - 查询指数成分股（展开嵌套数组）
   - 筛选低估值股票

4. **保留备选方案**
   - Findata Service API（备选）
   - 理杏仁 API 直接调用（Python）
   - AKShare（替代数据源）

---

## 更新统计

### 文件更新

- **总文件数**: 56
- **成功更新**: 56
- **失败**: 0
- **成功率**: 100%

### 更新的 Skills

所有 `skills/China-market/*/references/data-queries.md` 文件已更新，包括：

1. ab-ah-premium-monitor_UNSUPPORTED
2. block-deal-monitor
3. bse-selection-analyzer
4. concept-board-analyzer_UNSUPPORTED
5. convertible-bond-scanner
6. disclosure-notice-monitor
7. dividend-corporate-action-tracker
8. dragon-tiger-list-analyzer
9. equity-pledge-risk-monitor
10. equity-research-orchestrator
11. esg-screener_UNSUPPORTED
12. etf-allocator
13. event-driven-detector
14. event-study
15. factor-crowding-monitor
16. financial-statement-analyzer
17. fund-flow-monitor
18. goodwill-risk-monitor_UNSUPPORTED
19. high-dividend-strategy
20. hot-rank-sentiment-monitor
21. hsgt-holdings-monitor_UNSUPPORTED
22. industry-board-analyzer
23. industry-chain-mapper
24. insider-trading-analyzer
25. intraday-microstructure-analyzer
26. investment-memo-generator
27. ipo-lockup-risk-monitor_UNSUPPORTED
28. ipo-newlist-monitor
29. limit-up-limit-down-risk-checker_UNSUPPORTED
30. limit-up-pool-analyzer_UNSUPPORTED
31. liquidity-impact-estimator
32. macro-liquidity-monitor
33. margin-risk-monitor_UNSUPPORTED
34. market-breadth-monitor
35. market-overview-dashboard
36. northbound-flow-analyzer_UNSUPPORTED
37. peer-comparison-analyzer
38. policy-sensitivity-brief
39. portfolio-health-check
40. portfolio-monitor-orchestrator
41. quant-factor-screener
42. rebalancing-planner
43. risk-adjusted-return-optimizer
44. sector-rotation-detector
45. sentiment-reality-gap
46. share-repurchase-monitor_UNSUPPORTED
47. shareholder-risk-check
48. shareholder-structure-monitor
49. small-cap-growth-identifier
50. st-delist-risk-scanner_UNSUPPORTED
51. suitability-report-generator
52. tech-hype-vs-fundamentals
53. undervalued-stock-screener
54. valuation-regime-detector
55. volatility-regime-monitor
56. weekly-market-brief-generator

---

## 备份说明

### 备份文件

所有原始文件已备份为 `.bak` 文件：
- 备份位置：与原文件相同目录
- 备份文件名：`data-queries.md.bak`

### 恢复方法

如需恢复原文件：
```bash
# 恢复单个文件
mv skills/China-market/bse-selection-analyzer/references/data-queries.md.bak \
   skills/China-market/bse-selection-analyzer/references/data-queries.md

# 批量恢复所有文件
find skills/China-market -name "data-queries.md.bak" -type f | while read file; do
  mv "$file" "${file%.bak}"
done
```

---

## 新模板特点

### 1. 强调 query_tool.py

新模板将 `query_tool.py` 作为首选方案，并详细说明其优势：
- 字段过滤（`--columns`）
- 数据筛选（`--row-filter`）
- 数组展开（`--flatten`）
- CSV 格式输出

### 2. 丰富的示例

提供 7 个常用场景的完整示例：
- 基本信息查询
- K 线数据查询
- 分红数据查询
- 股东人数查询
- 公告信息查询
- 指数成分股查询（展开嵌套数组）
- 低估值股票筛选

### 3. 参数说明

详细说明所有参数的用途和使用方法：
- 必需参数：`--suffix`, `--params`
- 增强参数：`--columns`, `--row-filter`, `--flatten`, `--limit`
- 可选参数：`--format`

### 4. 查找 API 的方法

提供 3 种查找可用 API 的方法：
1. 查看 API 列表（`SKILL.md`）
2. 搜索关键字（`grep`）
3. 查看 API 文档（`api_new/api-docs/`）

### 5. 最佳实践

强调 5 个最佳实践：
1. 始终使用 `--columns`
2. 主动使用 `--row-filter`
3. 处理嵌套数据时使用 `--flatten`
4. 使用 `--limit` 控制数量
5. 参考 API 文档

---

## 相关文件

### 新创建的文件

1. **DATA_QUERIES_TEMPLATE_NEW.md**
   - 新版数据查询模板
   - 位置：`skills/China-market/DATA_QUERIES_TEMPLATE_NEW.md`

2. **update_data_queries_files.py**
   - 批量更新脚本
   - 位置：`update_data_queries_files.py`

3. **DATA_QUERIES_UPDATE_REPORT.md**
   - 本报告文件
   - 位置：`DATA_QUERIES_UPDATE_REPORT.md`

### 参考文档

1. **lixinger-data-query/SKILL.md**
   - 查询工具主文档
   - 包含 API 列表和使用说明

2. **lixinger-data-query/LLM_USAGE_GUIDE.md**
   - LLM 使用指南
   - 详细的调用流程和示例

3. **lixinger-data-query/EXAMPLES.md**
   - 查询示例集合
   - 各种场景的完整示例

---

## 对比分析

### 旧版本特点

- 主要推荐 Findata Service API
- 理杏仁 API 作为备选
- 缺少字段过滤和数据筛选的说明
- 示例较少

### 新版本特点

- 主要推荐 query_tool.py
- 强调增强参数的使用
- 提供丰富的使用示例
- 详细的参数说明和最佳实践
- 保留 Findata Service API 作为备选

### 优势对比

| 特性 | 旧版本 | 新版本 |
|------|--------|--------|
| 推荐工具 | Findata Service API | query_tool.py |
| 字段过滤 | ❌ 无 | ✅ `--columns` |
| 数据筛选 | ❌ 无 | ✅ `--row-filter` |
| 数组展开 | ❌ 无 | ✅ `--flatten` |
| 使用示例 | ⚠️ 较少 | ✅ 丰富 |
| 最佳实践 | ❌ 无 | ✅ 详细 |
| Token 优化 | ❌ 无说明 | ✅ 节省 30-40% |

---

## 影响分析

### 对 LLM 的影响

1. **更高效的数据获取**
   - 使用 `--columns` 只返回需要的字段
   - 使用 `--row-filter` 过滤数据
   - 节省 30-40% token

2. **更清晰的指导**
   - 详细的参数说明
   - 丰富的使用示例
   - 明确的最佳实践

3. **更好的数据质量**
   - 主动过滤无用数据
   - 只返回符合条件的数据
   - 处理嵌套结构

### 对用户的影响

1. **更快的响应速度**
   - 减少数据传输量
   - 降低 token 消耗
   - 提高查询效率

2. **更准确的结果**
   - 数据筛选更精确
   - 字段过滤更灵活
   - 结果更符合需求

3. **更好的可维护性**
   - 统一的数据获取方式
   - 清晰的文档结构
   - 易于理解和使用

---

## 后续建议

### 1. 测试验证

建议测试几个 skills，验证新的数据获取方式是否正常工作：
```bash
# 测试 dividend-corporate-action-tracker
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.dividend" \
  --params '{"stockCode": "600519"}' \
  --columns "date,dividendPerShare,dividendYield"

# 测试 shareholder-risk-check
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.shareholders-num" \
  --params '{"stockCode": "600519"}' \
  --columns "date,num,shareholdersNumberChangeRate"
```

### 2. 文档同步

确保以下文档保持同步：
- `lixinger-data-query/SKILL.md`
- `lixinger-data-query/LLM_USAGE_GUIDE.md`
- `lixinger-data-query/EXAMPLES.md`
- `China-market/DATA_QUERIES_TEMPLATE_NEW.md`

### 3. 用户反馈

收集用户反馈，了解：
- 新的数据获取方式是否更高效
- 文档是否清晰易懂
- 是否需要补充更多示例

### 4. 持续优化

根据使用情况持续优化：
- 补充更多常用场景的示例
- 优化参数说明
- 改进最佳实践指导

---

## 总结

本次更新成功将所有 56 个 China-market skills 的 `data-queries.md` 文件更新为新版本，主要变化包括：

1. ✅ 推荐使用 `query_tool.py` 作为首选数据获取方式
2. ✅ 强调增强参数的使用（`--columns`, `--row-filter`, `--flatten`）
3. ✅ 提供丰富的使用示例和最佳实践
4. ✅ 保留备选方案（Findata Service API、理杏仁 API、AKShare）
5. ✅ 所有原始文件已备份为 `.bak` 文件

新版本的文档更加强调数据获取的效率和质量，通过字段过滤和数据筛选，可以节省 30-40% 的 token，同时提高数据的准确性和相关性。

---

**更新时间**: 2026-02-23  
**更新者**: Kiro AI  
**文档版本**: 1.0
