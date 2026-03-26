---
description: 分析 stock-crawler 已产出的 Markdown 或中间抓取结果
argument-hint: "[markdown_path or output_dir]"
---

Analyze existing `stock-crawler` outputs instead of waiting for a full end-to-end rerun.

Preferred workflow:

1. Read existing Markdown files first.
2. If multiple files exist, summarize by:
   - titles
   - dates
   - entities
   - repeated themes
   - anomalies
3. Identify whether another crawl should be submitted:
   - broader list crawl
   - deeper article crawl
   - keyword search
   - retry after failure

Example:
`/analyze-crawl-results .claude/stock-crawler/output/eastmoney-search/`

