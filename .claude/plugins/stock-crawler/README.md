# Stock Crawler Plugin

Website-first research crawling plugin for non-API, high-timeliness, and unstructured investment data.

## Quickstart

1. Use `/submit-crawl-task` to submit a crawl as an offline-style task.
2. Use `/check-crawl-progress` to inspect output directories, logs, and partial artifacts.
3. Use `/analyze-crawl-results` to read Markdown outputs before the whole crawl lifecycle is fully complete.

Recommended priority:

1. Try `query_data` first for structured API-accessible data.
2. Use `stock-crawler` when the data is page-only, more timely on the website, or mainly unstructured.

## Scope and Fit

Best fit:

- website data that updates before APIs
- page-visible data that APIs do not provide
- paid API substitutes where the webpage still exposes useful information
- announcements, news, reports, and community content

Not ideal:

- standardized time series already covered by `query_data`
- workflows that require a full task scheduler inside the crawler core
- cases where you need one unified normalized schema before any analysis

## Execution Layer

Current execution entry:

- `.claude/stock-crawler/src/plugin-entry.js`

Current callable functions:

- `get_available_sites()`
- `crawl_site_data(site, target, url, options)`
- `crawl_site_links(site, url, limit)`
- `crawl_site_search(site, keyword, target, limit)`
- `cleanup()`

The plugin is currently best used in an offline-task style:

1. submit a crawl request
2. let the crawler fetch data
3. inspect logs and output artifacts
4. analyze generated Markdown
5. resubmit refined tasks if needed

## Commands

| Command | Description |
|---------|-------------|
| `/submit-crawl-task [site] [target] [url-or-keyword]` | Submit a stock-crawler offline crawl task |
| `/check-crawl-progress [task_id or output_path]` | Check logs, pages, links, and Markdown progress |
| `/analyze-crawl-results [markdown_path or output_dir]` | Analyze generated Markdown or partial crawl outputs |

## Task Model

Recommended external task fields:

- `task_id`
- `task_type`
- `site`
- `target`
- `status`
- `submitted_at`
- `artifacts_dir`
- `markdown_path`

Recommended statuses:

- `submitted`
- `running`
- `succeeded`
- `failed`

This task model is a plugin-layer convention. It does not require the crawler core itself to become a full queue system.

## Progress Checking

Preferred progress sources:

- returned `markdownPath`
- `.claude/stock-crawler/output/<site>-plugin/`
- `.claude/stock-crawler/output/<site>-search/`
- `output/<config-name>/logs/`
- `output/<config-name>/pages-<timestamp>/`
- `output/<config-name>/links.txt`

Practical interpretation:

- new Markdown file means a result is already analyzable
- growing `logs/` means the crawl is still active
- growing `pages-*` means partial outputs are already available
- changing `links.txt` indicates URL-level progress

## Analyze While Running

Do not wait for a full perfect end state before analysis.

Good pattern:

1. search or discover candidate links
2. crawl high-value pages
3. analyze Markdown immediately
4. submit narrower follow-up tasks

Typical examples:

- crawl `announcement_list`, then select a few `announcement_article` pages
- search for a theme, then deep-crawl the strongest hits
- rerun the same task later and compare the newest output set

## Output Convention

Suggested task submission response:

```json
{
  "task_id": "stock_crawler_20260325_101530_eastmoney_news_article",
  "status": "running",
  "site": "eastmoney-plugin",
  "target": "news_article",
  "submitted_at": "2026-03-25T10:15:30+08:00",
  "artifacts_dir": ".claude/stock-crawler/output/eastmoney-plugin/",
  "markdown_path": null,
  "message": "Task submitted. Check progress later."
}
```

Suggested finished response:

```json
{
  "task_id": "stock_crawler_20260325_101530_eastmoney_news_article",
  "status": "succeeded",
  "site": "eastmoney-plugin",
  "target": "news_article",
  "markdown_path": ".claude/stock-crawler/output/eastmoney-plugin/eastmoney-plugin_news_article_2026-03-25T10-16-02-123Z.md",
  "summary": {
    "title": "Example Title",
    "statistics": {
      "paragraphs": 18,
      "tables": 1,
      "lists": 0,
      "codeBlocks": 0
    }
  }
}
```

## Relationship to Current Implementation

Already supported:

- site-based crawling
- target-based invocation
- link discovery
- site search
- Markdown output

Not yet a full built-in scheduler:

- no full queue system inside the crawler core
- no complete task state store in the crawler core
- offline task semantics are mainly an outer plugin workflow convention
