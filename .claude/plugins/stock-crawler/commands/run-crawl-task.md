---
description: "直接运行 stock-crawler 抓取任务（本地执行 npm run crawl）"
argument-hint: "--config=<config-name>"
target-skill: "无（直接调用外部脚本）"
output-format: "json"
risk-level: "low"
---

直接运行本地 stock-crawler 抓取任务，执行 `npm run crawl config/<config-name>.json`。

## 工作流程

1. 检查配置文件是否存在 `config/<config-name>.json`
2. 在 stock-crawler 目录下执行 `npm run crawl config/<config-name>.json`
3. 监控执行输出并返回结果

## 支持的配置文件

- `lixinger` - 理杏仁数据抓取
- `eastmoney-plugin` - 东方财富数据抓取
- `cninfo-plugin` - 巨潮资讯数据抓取
- `xueqiu-plugin` - 雪球数据抓取
- 其他 config/ 目录下的配置文件

## 使用示例

```bash
/run-crawl-task --config=lixinger
```

或直接运行:
```bash
cd ${CRAWLER_HOME:-.claude/stock-crawler}
npm run crawl config/lixinger.json
```

## 输出格式

```json
{
  "task_id": "crawl_lixinger_<timestamp>",
  "status": "running",
  "config": "config/lixinger.json",
  "message": "Crawler started"
}
```