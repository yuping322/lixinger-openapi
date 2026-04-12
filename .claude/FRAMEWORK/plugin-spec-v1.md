# Plugin 统一规范 v1

> 适用范围：所有 `.claude/plugins/*` 及后续新增 plugin
> 强制生效：2026-04-12 起
> 违规处理：不接受进入 Plugin Pack

---

## 三层职责模型

### 1. Command（只做路由）
**职责**：解析参数 → 选择 skill → 声明输出模板
**禁止**：业务逻辑、数据获取、分析计算

**标准 frontmatter（必填）**：
```yaml
---
description: "一句话描述该命令的功能（不超过50字）"
argument-hint: "参数说明（格式：--key=value）"
target-skill: "调用的 skill 名称"
output-format: "markdown | json | table"
risk-level: "low | medium | high"
---
```

**示例**：
```markdown
---
description: "查询指定股票的估值分位"
argument-hint: "--stock=SH600000 --metric=pe_ttm"
target-skill: "valuation-regime-detector"
output-format: "markdown"
risk-level: "low"
---

# 执行估值分位查询

## 参数解析
- stock: {{args.stock}}
- metric: {{args.metric}}

## 调用 Skill
调用 `valuation-regime-detector`，传入参数...

## 输出模板
按 valuation-output-template.md 格式输出结果。
```

---

### 2. Skill（只做单一分析任务）
**职责**：一个 skill 对应一个明确能力
**禁止**：跨域调用、混合职责、直接数据抓取

**标准 SKILL.md 结构（必填）**：

```markdown
# [Skill Name]

## 能力定义
一句话描述该 skill 的核心能力。

## 输入字段（Input Schema）
| 字段名 | 类型 | 必填 | 说明 | 示例值 |
|-------|------|-----|------|--------|
| stock | string | 是 | 股票代码 | SH600000 |
| metric | string | 否 | 估值指标 | pe_ttm |
| date | string | 否 | 查询日期 | 2026-04-12 |

## 输出字段（Output Schema）
| 字段名 | 类型 | 必填 | 说明 | 示例值 |
|-------|------|-----|------|--------|
| percentile | float | 是 | 分位值 | 0.45 |
| confidence | float | 是 | 置信度 | 0.85 |
| data_gap | string | 否 | 数据缺口说明 | null |

## 失败模式（Failure Modes）
| 失败类型 | 触发条件 | 降级行为 | 用户提示 |
|---------|---------|---------|---------|
| DATA_NOT_AVAILABLE | 数据源无响应 | REFUSE | "数据源暂时不可用，请稍后重试" |
| INVALID_STOCK | 股票代码不存在 | REFUSE | "股票代码无效" |
| PARTIAL_DATA | 部分数据缺失 | DOWNGRADE | "部分数据缺失，置信度已降低" |

## 置信度来源（Confidence Source）
- 数据完整性：权重 40%
- 计算稳定性：权重 30%
- 同业可比性：权重 30%

## 最小示例（Minimal Example）
**输入**：
```json
{
  "stock": "SH600000",
  "metric": "pe_ttm"
}
```

**输出**：
```json
{
  "percentile": 0.45,
  "confidence": 0.85,
  "data_gap": null
}
```

## QA 规则（QA Rules）
- 分位值必须在 [0, 1] 区间
- 置信度必须在 [0, 1] 区间
- data_gap 必须为 null 或有效字符串
```

---

### 3. Orchestrator（只做编排与 QA）
**职责**：调度多个 skills → 执行一致性校验 → 降级 → 置信度汇总
**禁止**：业务逻辑、直接数据获取

**标准结构**：

```markdown
# [Orchestrator Name]

## 调度流程（Workflow）
1. 调用 skill-A 获取数据
2. 调用 skill-B 进行分析
3. 调用 skill-C 生成结论
4. 执行 QA 校验
5. 汇总置信度

## QA 规则（QA Rules）
| 规则名 | 校验内容 | 失败动作 |
|-------|---------|---------|
| cross_skill_consistency | skills A/B/C 输出一致性 | DOWNGRADE |
| data_freshness | 数据时效性 | REFUSE |
| confidence_threshold | 总置信度 > 0.7 | WARNING |

## 降级策略（Fallback）
- 主 skill 失败 → 尝试备用 skill
- 所有 skill 失败 → REFUSE
- 置信度 < 0.5 → WARNING + 降级输出

## 置信度汇总（Confidence Aggregation）
```
total_confidence = skill_A.confidence * 0.4 + skill_B.confidence * 0.3 + skill_C.confidence * 0.3
```
```

---

## 标准目录结构

每个 plugin 必须包含以下结构：

```text
plugins/<plugin>/
  README.md                    # 插件说明（必填）
  plugin.yaml                  # 插件元信息（必填）
  commands/
    <command>.md               # 必须有 frontmatter
  skills/
    <skill>/
      SKILL.md                 # 单一职责定义
      references/              # 可选：参考资料
      scripts/                 # 可选：执行脚本
      examples/                # 可选：示例文件
  contracts/
    input.schema.json          # 输入契约
    output.schema.json         # 输出契约
    qa-rules.schema.json       # QA 规则契约
  templates/
    output-template.md         # 输出模板
  tests/
    smoke/                     # 每个 command 至少一个 smoke case
      <command>_smoke.md
```

---

## plugin.yaml 标准模板

```yaml
name: "valuation"
version: "1.0.0"
owner: "TBD"
pack: "Pack A"
business_domain: "Valuation & Decision"
dependencies:
  - "query_data (Pack D)"
  - "stock-screener (Pack A)"
default_command: "valuation-query"
status: "active | beta | deprecated"
created_at: "2026-04-12"
updated_at: "2026-04-12"
```

---

## 质量红线（Quality Gates）

### 必须满足：
1. 每个 command 必须有完整 frontmatter
2. 每个 skill 必须声明 I/O schema + 失败模式 + 置信度来源
3. 每个 orchestrator 必须有 QA 规则 + 降级策略
4. 每个 plugin 必须有至少一个 smoke test

### 禁止：
1. Command 包含业务逻辑
2. Skill 直接调用数据源（必须通过 Pack D）
3. 跨域调用（必须通过契约）
4. 硬编码绝对路径（如 `/Users/fengzhi/...`）
5. 混合职责（一个 skill 做多件事）

---

## 发布流程

1. 提交 PR → 触发 smoke test
2. QA Owner 审核 → 检查契约合规
3. Pack Owner 批准 → 进入灰度
4. 灰度验证 → 7天无重大问题
5. 正式发布 → 更新 plugin.yaml 状态

---

## 现有 plugin 合规性评估

| plugin | frontmatter 完整度 | skill I/O 契约 | QA 规则 | 综合评分 |
|--------|------------------|--------------|--------|---------|
| valuation | 80% | 70% | 60% | 70% |
| industry-concept-research | 90% | 85% | 80% | 85% |
| risk-monitor | 40% | 50% | 30% | 40% |
| stock-crawler | 20% | 0% | 0% | 10% |
| stock-screener | 70% | 60% | 50% | 60% |

---

## 强制改造截止日期

- **Phase 1（高收益）**：risk-monitor, stock-crawler → 2026-04-15
- **Phase 2（全量）**：所有 plugin → 2026-04-30

---

## 附录：Command/Skill 模板文件

见 `templates/command-template.md` 和 `templates/skill-template.md`。