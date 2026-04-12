---
name: risk-monitor-orchestrator
description: 风险监控编排器。用于在"旧能力迁移不整合"阶段控制执行模式（legacy_only / hybrid / engine_only），并管理选股后排雷与持仓后事件增量处理流程。
---

# Risk Monitor Orchestrator

编排 risk-monitor 插件的执行流程，支持 legacy/engine 双模式切换与事件驱动增量更新。

## 执行模式

- `legacy_only`：仅调用 `skills/legacy/*`（当前默认）
- `hybrid`：旧能力 + 新引擎并行输出对照
- `engine_only`：仅新引擎

## 输入契约

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `mode` | string | 是 | `legacy_only` / `hybrid` / `engine_only` |
| `watchlist` | array/string | 是 | 股票代码列表，至少 1 只 |
| `as_of_date` | string | 否 | YYYY-MM-DD，默认今日 |
| `event_sources` | array | 否 | `announcement` / `news` / `market_anomaly` |
| `event_window` | string | 否 | 如 `24h` / `3d` |

## 输出契约

```json
{
  "dispatch_timestamp": "ISO时间",
  "input": { "mode, watchlist, as_of_date, event_sources" },
  "status": "plan_generated | completed | completed_with_disagreement | rejected",
  "execution_plan": { "模式对应的执行计划" },
  "results": { "聚合风险结果" },
  "qa_status": "passed | failed_input_validation | failed_execution",
  "errors": [],
  "warnings": [],
  "next_steps": [ "下一步操作列表" ]
}
```

## 调用入口

### 方式一：Dispatcher 脚本

```bash
python3 skills/risk-monitor-orchestrator/dispatcher.py \
  --mode legacy_only \
  --watchlist '["600519","000858"]' \
  --as-of-date 2026-04-12
```

### 方式二：Skill 工具调用

使用 skill 工具加载本 skill 后，按流程执行：
1. 解析输入参数
2. 根据 mode 选择执行路径
3. 调用 legacy skills 或执行规则
4. 按 `templates/post-selection-risk-clearance-output-template.md` 生成输出

## 处理流程

### legacy_only 模式

```
1. 加载 skills/legacy/* 的 9 个 SKILL.md
2. 对每个 skill:
   - 读取 data-queries.md 获取数据
   - 按 methodology.md 执行分析
   - 按 output-template.md 生成结果
3. 聚合输出按主模板格式化
```

### engine_only 模式

```
1. 加载 skills/risk-signal-engine/rules/*.json
2. 过滤 active 状态规则
3. 按 event_sources 过滤相关规则（如有）
4. 对每个规则:
   - 获取 inputs_required 数据
   - 计算 logic.expression
   - 按 severity.mapping 分级
   - 生成标准化告警
```

### hybrid 模式

```
1. 并行启动 legacy_only 和 engine_only 分支
2. 等待两分支完成
3. 执行 comparison_strategy:
   - 检查 risk_type_match
   - 检查 severity_consistency
   - 检查 thesis_overlap
4. 输出对照矩阵，disagreement 标记人工复核
```

## 事件路由

| event_source | 触发规则类型 |
|--------------|-------------|
| announcement | pledge_update, unlock_notice, financial_report, major_event |
| news | negative_news, regulatory_action, industry_warning |
| market_anomaly | volume_spike, price_gap, limit_up_down_chain |

---

## QA Rules

### Rule 1: 输入完整性检查

```yaml
rule_id: QA_INPUT_001
description: 检查输入参数完整性
checks:
  - watchlist 非空且包含有效股票代码格式
  - mode 为 legacy_only / hybrid / engine_only 之一
  - as_of_date 格式为 YYYY-MM-DD（如提供）
failure_action: reject_execution
error_message: "输入参数校验失败：{具体错误}"
```

### Rule 2: 输出字段完整性检查

```yaml
rule_id: QA_OUTPUT_001
description: 检查输出契约必须字段
checks:
  - dispatch_timestamp 存在且为有效 ISO 时间
  - status 为 plan_generated / completed / completed_with_disagreement / rejected 之一
  - qa_status 为 passed / failed_* 之一
  - results.summary 中每只股票包含 overall_risk 和 action 字段
failure_action: mark_failed_execution
error_message: "输出契约校验失败：缺失字段 {具体字段}"
```

### Rule 3: severity 合规性检查

```yaml
rule_id: QA_SEVERITY_001
description: 检查 severity 级别合规
checks:
  - 所有 severity 值为 critical / high / medium / low / none 之一
  - hybrid 模式下 severity_gap 不超过 2 级（超过则 needs_review=true）
failure_action: mark_warning
warning_message: "severity 异常：{股票} gap={差距}"
```

### Rule 4: thesis 结构检查

```yaml
rule_id: QA_THESIS_001
description: 检查 thesis 语义结构
checks:
  - thesis 包含风险主体 + 风险特征 + 风险后果 三要素
  - thesis 长度 20-200 字符
failure_action: mark_warning
warning_message: "thesis 结构不完整：{股票}"
```

---

## Fallback Strategy

### 缺数降级

```yaml
strategy: partial_execution
conditions:
  - 单维度数据缺失：跳过该维度，标记 coverage_gap
  - 多维度数据缺失（>3）：降级为 partial_report，标记 needs_review
  - 核心维度（st_delist, equity_pledge）缺失：拒绝执行
fallback_output:
  - 输出 partial_coverage 字段，列出缺失维度
  - 生成降级报告，说明数据缺口
```

### 规则执行失败

```yaml
strategy: rule_skip_with_warning
conditions:
  - 单规则计算失败：跳过该规则，标记 rule_failure
  - 规则依赖数据缺失：标记 data_gap，跳过执行
fallback_output:
  - 输出 failed_rules 字段，列出失败规则
  - 生成 warning 提示用户复核
```

### hybrid 模式分歧处理

```yaml
strategy: mark_disagreement
conditions:
  - severity_gap > 1：标记 needs_review=true
  - thesis_overlap < 0.5：标记 needs_review=true
  - 仅一方触发：标记 partial_coverage=true
fallback_output:
  - 输出 comparison_result 字段，详细记录分歧点
  - 生成人工复核清单
```

---

## Confidence Aggregation

### 公式

**单股票综合置信度计算**：

```
confidence_stock = Σ(confidence_rule_i * weight_i) / Σ(weight_i)
```

其中：
- `confidence_rule_i`：规则引擎输出的 confidence.base_score
- `weight_i`：规则权重，按 severity 分级：
  - critical: weight = 4
  - high: weight = 3
  - medium: weight = 2
  - low: weight = 1
  - none: weight = 0.5

### hybrid 模式置信度融合

```
confidence_hybrid = α * confidence_legacy + β * confidence_engine

α = 0.6（legacy 权重）
β = 0.4（engine 权重）
```

> 注：当 needs_review=true 时，置信度衰减 20%。

### 置信度阈值

| 置信度范围 | 输出行为 |
|------------|----------|
| ≥ 0.8 | 正常输出，qa_status=passed |
| 0.6-0.8 | 输出 + warning，建议复核 |
| < 0.6 | 输出 + needs_review=true，强制人工复核 |

---

## 当前阶段策略

- 先确保 legacy 迁移可用。
- 新引擎在不影响 legacy 的前提下独立迭代。
- hybrid 模式仅用于对照验证，不作为主要交付模式。

## 示例调用

### 扫描股票池

```bash
# legacy_only 模式（默认）
python3 dispatcher.py --watchlist '["600519","000858","300750"]'

# hybrid 模式
python3 dispatcher.py --mode hybrid --watchlist '["600519","000858"]'
```

### 事件驱动增量

```bash
# 公告触发重算
python3 dispatcher.py \
  --mode engine_only \
  --watchlist '["600519"]' \
  --event-sources announcement
```