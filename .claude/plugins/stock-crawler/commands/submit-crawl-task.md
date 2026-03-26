---
description: 提交一个 stock-crawler 离线抓取任务
argument-hint: "[site] [target] [url-or-keyword]"
---

Use the `stock-crawler` plugin to submit an offline crawl task.

Prefer this workflow:

1. Identify the target site such as `eastmoney-plugin`, `cninfo-plugin`, `xueqiu-plugin`, or `lixinger-plugin`.
2. Choose a target such as `news_article`, `announcement_list`, or `search_results`.
3. Decide whether this is:
   - a page crawl via `crawl_site_data`
   - a link discovery run via `crawl_site_links`
   - a site search via `crawl_site_search`
4. Return a task-style response containing:
   - `task_id`
   - `status`
   - `site`
   - `target`
   - expected output directory
   - next step for checking progress

Example:
`/submit-crawl-task eastmoney-plugin news_article https://finance.eastmoney.com/a/202603252345678.html`

