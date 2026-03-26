# /fundamental-forensics-scan

基于结构化输入构建 Plugin D 的三份标准输出：

- `forensics/red_flag_graph.json`
- `forensics/fragility_scorecard.json`
- `forensics/90d_monitor_plan.json`

## 用法

```bash
python3 .claude/plugins/fundamental-forensics/tools/build_forensics_outputs.py \
  --input .claude/plugins/fundamental-forensics/examples/sample_input.json \
  --output-dir /tmp/fundamental-forensics-output
```

## 输入要求

输入 JSON 建议至少包含：

- `symbol`, `market`, `as_of_date`
- `signals`（应收、OCF/NI、存货、商誉、质押、insider、hype-gap、ST 风险）
- `trend`（`delta_30d`, `delta_90d`, `fragility_trend`）
- `mitigants`
- `data_quality`
- `invalidators`

## 输出说明

1. `red_flag_graph.json`：证据→风险态→影响的触发链图
2. `fragility_scorecard.json`：总分、分项分、触发组合、驱动项
3. `90d_monitor_plan.json`：90 天监控频率、阈值、升级动作
