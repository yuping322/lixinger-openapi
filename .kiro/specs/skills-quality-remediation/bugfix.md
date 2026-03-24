# Bugfix Requirements Document

## Introduction

`.claude/skills` 下现有 108 个 Skills 存在系统性质量问题，导致 AI 在执行金融分析任务时频繁遭遇 API 调用失败、参数错误、跨市场数据污染等问题。这些问题的核心不是 Skill 数量不足，而是现有 Skill 的"可执行性"存在严重缺陷——文档描述的分析框架与实际可运行的 API 之间存在断裂。

**本轮修复范围**：未验证/不存在的 API（Section 1）、参数定义冲突（Section 2）、跨市场模板污染（Section 3）、错误路径格式（Section 4）、TODO/Draft 内容残留（Section 5）。

**不在本轮修复范围**：状态失真（SKILLS_MAP.md 重标）、AkShare 重依赖降级改造、筛选类 Skill 执行模型重构。这三类问题已记录至 `docs/SKILLS_ISSUES_ANALYSIS.md`，由用户后续手动处理。

---

## Bug Analysis

### Current Behavior (Defect)

**Section 1：未验证/不存在的 API**

1.1 WHEN AI 调用 `China-market_esg-screener` 执行 ESG 筛选时，THEN 系统尝试调用 `cn/company/esg`、`cn/company/governance`、`cn/company/violation` 等在 `api_new/api-docs` 中不存在的接口，导致 `Api was not found` 错误

1.2 WHEN AI 调用 `China-market_sector-valuation-heat-map` 执行行业估值分析时，THEN 系统使用点号路径格式（如 `cn.industry.fundamental.sw_2021`）和猜测型接口（如 `Need to check for money flow specific API`），导致调用失败

**Section 2：参数定义冲突**

1.3 WHEN AI 参照 `analysis-market/SKILL.md` 中的参数表调用 `cn/index/constituents` 时，THEN 系统使用 `indexCode` 作为参数名，但真实 API 要求 `stockCodes`，导致 `ValidationError: "stockCodes" is required`

**Section 3：跨市场模板污染**

1.4 WHEN AI 调用 `US-market_us-dividend-aristocrat-calculator` 执行美股股息贵族分析时，THEN 系统使用 `cn/company/fundamental/non_financial`、`cn/company/dividend` 等 A 股路径，以及 `600519`、`000858`、`300750` 等 A 股代码作为示例，导致美股分析产出 A 股数据

**Section 4：错误路径格式**

1.5 WHEN AI 参照部分 Skill 的 `references/data-queries.md` 构造查询命令时，THEN 系统使用点号路径（如 `cn.industry.fundamental.sw_2021`）而非斜杠路径，导致 `Api was not found` 错误

**Section 5：TODO/Draft 内容残留**

1.9 WHEN AI 参照 `China-market_macro-liquidity-monitor/references/methodology.md` 或 `China-market_limit-up-pool-analyzer/references/output-template.md` 执行分析时，THEN 系统输出包含 `[TODO]`、未定义阈值、空模板等草稿内容，导致分析结论不完整或无法使用

---

### Expected Behavior (Correct)

**Section 1：未验证/不存在的 API**

2.1 WHEN AI 调用 `China-market_esg-screener` 执行 ESG 筛选时，THEN 系统 SHALL 仅使用 `api_new/api-docs` 中已核验存在的 API，对于无对应 API 的数据维度，SHALL 明确标注"当前数据源不支持"并提供替代方案或降级输出

2.2 WHEN AI 调用 `China-market_sector-valuation-heat-map` 执行行业估值分析时，THEN 系统 SHALL 使用斜杠路径格式的已验证 API（如 `cn/industry/fundamental/sw_2021`），不得出现猜测型接口或 `Need to check` 占位符

**Section 2：参数定义冲突**

2.3 WHEN AI 参照 `analysis-market/SKILL.md` 中的参数表调用 `cn/index/constituents` 时，THEN 系统 SHALL 使用与 `api_new/api-docs/cn_index_constituents.md` 一致的参数名 `stockCodes`，文档中不得存在与真值文档冲突的参数定义

**Section 3：跨市场模板污染**

2.4 WHEN AI 调用 `US-market_us-dividend-aristocrat-calculator` 执行美股股息贵族分析时，THEN 系统 SHALL 仅使用 `us/` 前缀的 API 路径和美股代码示例（如 `AAPL`、`JNJ`），不得出现任何 `cn/` 路径或 A 股代码

**Section 4：错误路径格式**

2.5 WHEN AI 参照任意 Skill 的 `references/data-queries.md` 构造查询命令时，THEN 系统 SHALL 使用斜杠路径格式（如 `cn/industry/fundamental/sw_2021`），所有文档中不得出现点号路径格式

**Section 5：TODO/Draft 内容残留**

2.9 WHEN AI 参照已标记为 `stable` 或 `partial` 的 Skill 执行分析时，THEN 系统 SHALL 输出完整的结构化结论，方法论文档 SHALL 包含指标计算公式、阈值来源和边界条件，输出模板 SHALL 包含结论摘要、关键数据表、风险说明和下一步建议，不得出现 `[TODO]` 占位符

---

### Unchanged Behavior (Regression Prevention)

3.1 WHEN AI 调用已验证可用的 Skill（如 `China-market_financial-statement-analyzer`、`China-market_single-stock-health-check`）执行分析时，THEN 系统 SHALL CONTINUE TO 按原有方法论和数据查询路径正常执行，整治工作不得破坏现有可用 Skill 的执行逻辑

3.2 WHEN AI 使用 `lixinger-data-query` 工具通过 `query_tool.py` 直接查询 API 时，THEN 系统 SHALL CONTINUE TO 支持所有现有已验证的 API 路径和参数格式，整治工作不得修改底层查询工具的行为

3.3 WHEN AI 调用 `analysis-market/analysis-best-practices.md` 中已记录的正确参数规则（如 `metricsList` 必填、`.mcw` 后缀、`source` 参数等）时，THEN 系统 SHALL CONTINUE TO 按这些规则正确执行，整治工作应将这些规则下沉至各 Skill，而非替换或删除全局规则

3.4 WHEN AI 调用港股或美股 Skill 执行对应市场分析时，THEN 系统 SHALL CONTINUE TO 使用对应市场的 API 前缀（`hk/` 或 `us/`）和市场代码格式，整治工作不得引入新的跨市场污染

3.5 WHEN AI 参照 `analysis-market/SKILL.md` 中的项目文件夹管理规范（`analysis_YYYYMMDD_HHMMSS_主题`）和三级优先级规则（Skills → 数据 API → AkShare）时，THEN 系统 SHALL CONTINUE TO 遵循这些工作流规范，整治工作不得改变这些核心工作流约定

---

## 超出本轮修复范围的问题

以下三类问题已分析记录至 `docs/SKILLS_ISSUES_ANALYSIS.md`，**不在本轮修复范围内**，由用户后续手动处理：

1. **SKILLS_MAP.md 状态失真**：`analysis-market/SKILLS_MAP.md` 将几乎所有 Skill 标记为 `✅`，无法区分真实可用状态。问题清单和重标建议见分析文档。

2. **AkShare 重依赖 Skill 清单**：`China-market_hsgt-holdings-monitor` 等强依赖 AkShare 的 Skill，在 AkShare 不可用时直接报错退出即可，不需要三层降级改造。受影响 Skill 清单见分析文档。

3. **筛选类 Skill 执行模型问题**：`China-market_undervalued-stock-screener` 等筛选类 Skill 默认全市场扫描，与 API 单代码限制不匹配。问题清单见分析文档。

---

## Bug Condition 形式化描述

### Bug Condition 函数

```pascal
FUNCTION isBugCondition(X)
  INPUT: X of type SkillDocument
  OUTPUT: boolean

  RETURN (
    X 包含未在 api_new/api-docs 中存在的 API 路径
    OR X 包含点号格式路径（如 cn.xxx.yyy）
    OR X 包含与 api_new/api-docs 真值文档冲突的参数定义
    OR X 包含其他市场的 API 路径或代码示例（跨市场污染）
    OR X 包含 [TODO] 占位符且状态标记为 stable/partial
  )
END FUNCTION
```

### Fix Checking Property

```pascal
// Property: Fix Checking - Skill 文档质量修复验证
FOR ALL X WHERE isBugCondition(X) DO
  result ← remediate'(X)
  ASSERT (
    result 中所有 API 路径均在 api_new/api-docs 中存在
    AND result 中所有路径使用斜杠格式
    AND result 中参数定义与 api_new/api-docs 真值一致
    AND result 中不含其他市场的 API 路径或代码
    AND result 中 stable/partial Skill 不含 [TODO] 占位符
  )
END FOR
```

### Preservation Checking Property

```pascal
// Property: Preservation Checking - 已验证可用 Skill 不受影响
FOR ALL X WHERE NOT isBugCondition(X) DO
  ASSERT remediate(X) = remediate'(X)
  // 即：整治操作对已正确的 Skill 文档不产生破坏性变更
END FOR
```
