---
description: 查看 stock-crawler 离线抓取任务的进度
argument-hint: "[task_id or output_path]"
---

Check the progress of a `stock-crawler` task.

Prefer checking progress from:

1. returned `markdownPath`
2. output directory
3. `logs/`
4. `pages-*`
5. `links.txt`

When reporting progress, summarize:

- whether the task is still running or finished
- which artifacts already exist
- whether partial results are already analyzable
- whether a rerun is recommended

Example:
`/check-crawl-progress stock_crawler_20260325_101530_eastmoney_news_article`

