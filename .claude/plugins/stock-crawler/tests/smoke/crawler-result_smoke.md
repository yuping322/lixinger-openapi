---
test_case: analyze-crawl-results-basic
description: "验证分析爬取结果功能"
command: analyze-crawl-results
---

## 输入

```json
{
  "site": "eastmoney-crawler"
}
```

## 预期输出

```json
{
  "scan_summary": {
    "site": "eastmoney-crawler",
    "page_dir": "pages-<timestamp>",
    "total_files": 156,
    "total_chars": 1250000,
    "time_range": {
      "earliest": "2026-03-25T...",
      "latest": "2026-03-25T..."
    }
  },
  "content_analysis": {
    "titles": ["标题1", "标题2", ...],
    "entities": ["SH600000", "宁德时代", ...],
    "themes": ["财经新闻", "个股分析", ...]
  },
  "quality_issues": [],
  "recommendations": ["建议后续操作"]
}
```

## 验证点

1. **scan_summary 完整**: 包含 site, page_dir, total_files, total_chars
2. **total_files 准确**: 与 pages 目录下文件数量一致
3. **entities 识别正确**: 提取到股票代码或公司名称
4. **themes 有意义**: 主题聚类合理
5. **quality_issues 格式正确**: 数组格式，可包含空数组

## 执行命令

```bash
find output/eastmoney-crawler/pages-*/ -name "*.md" | wc -l
head -1 output/eastmoney-crawler/pages-*/*.md
```