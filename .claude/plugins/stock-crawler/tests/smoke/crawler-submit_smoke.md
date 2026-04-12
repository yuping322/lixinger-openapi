---
test_case: submit-crawl-task-basic
description: "验证提交爬取任务的基本功能"
command: submit-crawl-task
---

## 输入

```json
{
  "config": "eastmoney-plugin"
}
```

## 预期输出

```json
{
  "task_id": "crawl_eastmoney_<timestamp>",
  "status": "running",
  "config": "config/eastmoney-plugin.json",
  "artifacts_dir": "output/eastmoney-crawler/",
  "message": "Crawler started. Check logs for progress."
}
```

## 验证点

1. **返回结构完整**: 输出包含 `task_id`, `status`, `config`, `message` 字段
2. **task_id 格式正确**: 符合 `crawl_<site>_<timestamp>` 格式
3. **status 合法**: 为 `pending` 或 `running`
4. **config 路径正确**: 指向 `.claude/stock-crawler/config/eastmoney-plugin.json`
5. **artifacts_dir 存在**: 输出目录路径正确

## 执行命令

```bash
cd ${CRAWLER_HOME:-.claude/stock-crawler}
node src/index.js config/eastmoney-plugin.json
```

## 验证步骤

1. 检查 `output/eastmoney-crawler/logs/` 目录是否创建
2. 等待 5 秒后检查日志文件是否开始写入
3. 检查 `output/eastmoney-crawler/links.txt` 是否生成