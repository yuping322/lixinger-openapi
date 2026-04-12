---
description: 对已选股票池做排雷扫描，聚合9个风险维度并给出处置建议
argument-hint: "[watchlist] [--mode legacy_only|hybrid|engine_only] [--as-of-date YYYY-MM-DD]"
target-skill: "risk-monitor-orchestrator"
output-format: "post-selection-risk-clearance-output-template"
risk-level: "high"
---

# /risk-monitor-scan

对已选股票池做排雷扫描，聚合 legacy skills 与规则引擎输出，给出处置建议。

## 路由行为

加载 `risk-monitor-orchestrator` skill 后执行：
1. 解析 watchlist 与 mode 参数
2. 根据 mode 选择执行路径（legacy_only / hybrid / engine_only）
3. 调用各维度 risk skill/rule
4. 按 `templates/post-selection-risk-clearance-output-template.md` 生成标准化报告

## 参数

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `watchlist` | array/string | 是 | 股票代码列表，JSON数组或逗号分隔 |
| `as_of_date` | string | 否 | YYYY-MM-DD，默认今日 |
| `mode` | string | 否 | `legacy_only` / `hybrid` / `engine_only`（默认 `legacy_only`） |

## 输出契约

必须包含：
- 各维度风险等级（critical/high/medium/low/none）
- 处置建议（剔除/降权/观察/保留）
- 机制性风险解释与证伪条件
- 下一步监控要点

## 示例

```bash
/risk-monitor-scan '["600519","000858","300750"]'
/risk-monitor-scan '600519,000858' --mode hybrid --as-of-date 2026-04-12
```