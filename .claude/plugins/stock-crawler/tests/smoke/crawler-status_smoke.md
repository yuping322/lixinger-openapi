---
test_case: check-crawl-progress-basic
description: "验证检查爬取进度功能"
command: check-crawl-progress
---

## 输入

```json
{
  "site": "eastmoney-crawler"
}
```

## 预期输出

```markdown
进度报告:
========
配置: eastmoney-plugin.json
输出目录: output/eastmoney-crawler/

状态: 运行中 ⏳
- 最新日志: logs/crawler-*.log
- 已抓取页面: N 个
- 已发现链接: N 个
- Markdown 文件: N 个

建议: ...
```

## 验证点

1. **报告格式正确**: 包含状态、日志、页面、链接、Markdown 文件统计
2. **目录检查正确**: 能够正确识别 `pages-*/` 和 `logs/` 目录
3. **计数准确**: 文件数量与实际目录内容一致
4. **建议合理**: 根据状态给出恰当建议

## 执行命令

```bash
ls -lah output/eastmoney-crawler/
tail -5 output/eastmoney-crawler/logs/crawler-*.log
wc -l output/eastmoney-crawler/links.txt
```