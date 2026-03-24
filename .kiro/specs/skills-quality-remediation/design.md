# Skills Quality Remediation Bugfix Design

## Overview

本次修复针对 `.claude/skills` 下 Skills 文档体系中 5 类系统性质量问题：未验证/不存在的 API、参数定义冲突、跨市场模板污染、错误路径格式、TODO/Draft 内容残留。这些问题导致 AI 在执行金融分析任务时频繁遭遇 API 调用失败、参数错误、跨市场数据污染等运行时错误。

修复策略：以 `api_new/api-docs/` 和 `api_new/akshare_data/` 为真值来源，自底向上修复——先修路径格式和参数名（基础层），再修 Skill 文档引用（上层），最后补全 TODO 内容。同时为未来数据源扩展预留标准化接入路径。

## Glossary

- **Bug_Condition (C)**: 触发 bug 的条件——Skill 文档中存在不可执行的 API 引用、错误路径格式、参数冲突、跨市场污染或 TODO 占位符
- **Property (P)**: 修复后的期望行为——所有 API 引用均可验证，路径格式统一为斜杠，参数与真值文档一致，无跨市场污染，无 TODO 占位符
- **Preservation**: 已验证可用的 Skill 文档和 `query_tool.py` 行为不受影响
- **真值文档**: `api_new/api-docs/*.md` 和 `api_new/akshare_data/*.md`，是 API 路径、参数名、字段名的唯一权威来源
- **lixinger-data-query**: 数据查询统一收口目录 `.claude/skills/lixinger-data-query/`，当前包含理杏仁 API 和 AkShare 两个数据源
- **点号路径**: 错误格式，如 `cn.industry.fundamental.sw_2021`
- **斜杠路径**: 正确格式，如 `cn/industry/fundamental/sw_2021`

## Bug Details

### Bug Condition

5 类 bug 共享同一个 bug condition 函数：

**Formal Specification:**
```
FUNCTION isBugCondition(X)
  INPUT: X of type SkillDocument (SKILL.md 或 references/*.md)
  OUTPUT: boolean

  RETURN (
    // Bug 类型 1：不存在的 API
    X 包含未在 api_new/api-docs/ 中存在的 API 路径
    OR X 包含未在 api_new/akshare_data/ 中存在的接口名

    // Bug 类型 2：参数定义冲突
    OR X 中的参数名与 api_new/api-docs/ 真值文档不一致

    // Bug 类型 3：跨市场污染
    OR (X 属于 US-market_* 或 HK-market_* Skill
        AND X 包含 cn/ 前缀 API 路径或 A 股代码示例)

    // Bug 类型 4：错误路径格式
    OR X 包含点号格式路径（匹配正则 cn\.[a-z]|hk\.[a-z]|us\.[a-z]）

    // Bug 类型 5：TODO 残留
    OR (X 所属 Skill 状态为 stable/partial
        AND X 包含 "[TODO]" 占位符)
  )
END FUNCTION
```

### Examples

**Bug 类型 1 — 不存在的 API：**
- `China-market_esg-screener/references/data-queries.md` 引用 `cn/company/esg`、`cn/company/governance`、`cn/company/violation`，这三个路径在 `api_new/api-docs/` 中均不存在
- `China-market_sector-valuation-heat-map/references/data-queries.md` 包含 `Need to check for money flow specific API` 占位符

**Bug 类型 2 — 参数定义冲突：**
- `analysis-market/SKILL.md` 的 API 速查表中，`cn/index/constituents` 的必需参数写为 `indexCode`，但真值文档 `cn_index_constituents.md` 要求 `stockCodes`

**Bug 类型 3 — 跨市场污染：**
- `US-market_us-dividend-aristocrat-calculator/references/data-queries.md` 的查询示例使用 `cn/company/fundamental/non_financial`、`cn/company/dividend`，以及 A 股代码 `600519`、`000858`、`300750`

**Bug 类型 4 — 错误路径格式：**
- `China-market_sector-valuation-heat-map/references/data-queries.md` 中大量使用 `cn.industry.fundamental.sw_2021`、`cn.industry`、`cn.industry.candlestick` 等点号路径
- `lixinger-data-query/SKILL.md` 的示例命令中使用 `cn.company`、`cn.index.constituents` 等点号路径

**Bug 类型 5 — TODO 残留：**
- `China-market_macro-liquidity-monitor/references/methodology.md` 包含未定义的阈值和 `[TODO]` 占位符
- `China-market_limit-up-pool-analyzer/references/output-template.md` 包含空模板骨架

## Expected Behavior

### Preservation Requirements

**Unchanged Behaviors:**
- 已验证可用的 Skill（如 `China-market_financial-statement-analyzer`、`China-market_single-stock-health-check`）的执行逻辑不受影响
- `query_tool.py` 的所有现有已验证 API 路径和参数格式继续有效
- `analysis-market/analysis-best-practices.md` 中已记录的正确参数规则（`metricsList` 必填、`.mcw` 后缀、`source` 参数等）继续有效
- `analysis-market/SKILL.md` 中的项目文件夹管理规范和三级优先级规则不变
- 港股和美股 Skill 的 `hk/`、`us/` 前缀 API 路径不受影响

**Scope:**
所有不满足 `isBugCondition(X)` 的 Skill 文档不应被修改。修复操作仅针对满足 bug condition 的文档，且修改范围最小化。

## Hypothesized Root Cause

1. **自动生成文档未经验证**: 部分 Skill 的 `references/data-queries.md` 由模板自动生成，生成时未对照 `api_new/api-docs/` 验证 API 路径是否存在，导致幻觉 API（如 `cn/company/esg`）被写入文档

2. **跨市场模板复制**: `US-market_us-dividend-aristocrat-calculator` 的 `data-queries.md` 直接从 A 股 Skill 模板复制，未替换市场前缀和代码示例，导致美股 Skill 引用 A 股 API

3. **路径格式不统一**: 早期文档使用点号路径（Python 对象访问风格），后来规范改为斜杠路径，但旧文档未同步更新

4. **参数名记忆错误**: `analysis-market/SKILL.md` 的速查表中 `cn/index/constituents` 参数名 `indexCode` 是错误记忆，真值文档要求 `stockCodes`（与其他指数 API 保持一致）

5. **Draft 文档未完成即发布**: 部分 Skill 的 `methodology.md` 和 `output-template.md` 在 Draft 状态下被纳入 Skill 体系，`[TODO]` 占位符未被替换为实际内容

## Correctness Properties

Property 1: Bug Condition - Skill 文档可执行性修复

_For any_ Skill 文档 X 满足 `isBugCondition(X)`，修复后的文档 `remediate'(X)` SHALL 满足：
- 所有 API 路径均可在 `api_new/api-docs/` 或 `api_new/akshare_data/` 中找到对应文档
- 所有路径使用斜杠格式（`cn/xxx/yyy`），不含点号格式
- 所有参数名与对应真值文档一致
- US-market_* 和 HK-market_* Skill 不含 `cn/` 前缀路径或 A 股代码
- stable/partial 状态 Skill 的文档不含 `[TODO]` 占位符

**Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 2.9**

Property 2: Preservation - 已验证 Skill 不受影响

_For any_ Skill 文档 X 不满足 `isBugCondition(X)`（即已正确的文档），修复操作 SHALL 对其不产生任何修改，保持 `remediate(X) = remediate'(X)`，确保现有可用 Skill 的执行逻辑完全不变。

**Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5**

## Data Source Extension Architecture

### 设计目标

`lixinger-data-query/` 是所有数据源的统一收口。当前有两个数据源（理杏仁 API、AkShare），未来引入第三、第四个数据源时，应遵循以下约定。

### 目录约定

```
.claude/skills/lixinger-data-query/
├── api_new/
│   ├── api-docs/              # 理杏仁 API 文档（每个 API 一个 .md 文件）
│   ├── akshare_data/          # AkShare 接口文档（每个接口一个 .md 文件）
│   ├── {datasource}_data/     # 新数据源文档目录（命名规范：{datasource}_data/）
│   └── API_KEYWORD_INDEX.md   # 统一关键词索引（覆盖所有数据源）
├── scripts/
│   └── query_tool.py          # 理杏仁 API 查询工具（仅理杏仁）
├── SKILL.md                   # 主文档（描述所有数据源的使用方式）
├── LLM_USAGE_GUIDE.md         # LLM 使用指南
└── EXAMPLES.md                # 查询示例
```

### 新增数据源的标准步骤

1. **创建文档目录**: 在 `api_new/` 下创建 `{datasource}_data/` 目录，每个接口一个 `.md` 文件，格式与 `akshare_data/` 保持一致（包含：接口名、输入参数、返回字段、调用示例）

2. **更新 API_KEYWORD_INDEX.md**: 在索引文件中为新数据源添加独立章节，格式与现有章节一致，支持中文关键词 grep 搜索

3. **更新 SKILL.md**: 在"数据源选择优先级"和"API 接口列表"章节中添加新数据源的说明，包括：适用场景、查找方式、调用示例

4. **更新 analysis-market/SKILL.md**: 在三级优先级规则中说明新数据源的位置（通常作为第三或第四优先级）

### 优先级规则扩展

当前三级优先级：理杏仁 API > AkShare > 其他

未来扩展时，新数据源插入位置由以下原则决定：
- 数据质量高、覆盖面广 → 插入理杏仁 API 之后
- 补充性数据源 → 插入 AkShare 之后
- 优先级顺序在 `analysis-market/SKILL.md` 的"使用优先级"章节中维护

## Fix Implementation

### 修复执行顺序

按依赖关系从基础层到上层：

```
Layer 0（基础层）: 真值文档确认（api_new/api-docs/ 和 api_new/akshare_data/）
    ↓
Layer 1（路径格式）: 修复所有点号路径 → 斜杠路径
    ↓
Layer 2（参数名）: 修复参数定义冲突
    ↓
Layer 3（API 存在性）: 替换不存在的 API 引用
    ↓
Layer 4（跨市场污染）: 清理跨市场 API 路径和代码示例
    ↓
Layer 5（TODO 内容）: 补全 TODO 占位符
```

### Changes Required

#### Fix 1: 修复 `lixinger-data-query/SKILL.md` 中的点号路径示例

**文件**: `.claude/skills/lixinger-data-query/SKILL.md`

**问题**: "基础示例"代码块中使用 `cn.company`、`cn.index.constituents` 等点号路径

**修改**:
- `--suffix "cn.company"` → `--suffix "cn/company"`
- `--suffix "cn.index.constituents"` → `--suffix "cn/index/constituents"`

#### Fix 2: 修复 `analysis-market/SKILL.md` 中的参数定义冲突

**文件**: `.claude/skills/analysis-market/SKILL.md`

**问题**: "A股常用 API" 速查表中 `cn/index/constituents` 的必需参数列为 `indexCode`

**修改**: 将 `indexCode` 改为 `stockCodes`，与 `api_new/api-docs/cn_index_constituents.md` 真值一致

#### Fix 3: 修复 `China-market_sector-valuation-heat-map/references/data-queries.md`

**文件**: `.claude/skills/China-market_sector-valuation-heat-map/references/data-queries.md`

**问题**:
1. 所有 API 路径使用点号格式（`cn.industry.fundamental.sw_2021`、`cn.industry`、`cn.industry.candlestick`）
2. 包含 `Need to check for money flow specific API` 猜测型占位符

**修改**:
1. 将所有点号路径替换为斜杠路径：
   - `cn.industry.fundamental.sw_2021` → `cn/industry/fundamental/sw_2021`
   - `cn.industry` → `cn/industry`
   - `cn.industry.candlestick` → `cn/industry/candlestick`
   - `cn/industry.candlestick` → `cn/industry/candlestick`（混合格式也需修复）
   - `cn/industry.fundamental.sw_2021` → `cn/industry/fundamental/sw_2021`
2. 将 `Need to check for money flow specific API` 替换为明确说明：理杏仁 API 当前不提供行业资金流向数据，可使用 AkShare 的 `stock_board_industry_fund_flow_rank_em` 接口作为替代，或通过成分股成交量/价格变化推算

#### Fix 4: 修复 `China-market_esg-screener/references/data-queries.md`

**文件**: `.claude/skills/China-market_esg-screener/references/data-queries.md`

**问题**: 引用了 3 个不存在的 API：`cn/company/esg`、`cn/company/finance`、`cn/company/governance`、`cn/company/violation`

**修改**: 将不存在的 API 替换为可用的替代方案：
- `cn/company/esg` → 理杏仁 API 不提供 ESG 评分，标注"当前数据源不支持，可使用 AkShare `stock_esg_rate_sina` 接口获取新浪 ESG 评级"
- `cn/company/finance` → 替换为 `cn/company/fundamental/non_financial`（PE、PB、ROE 等）
- `cn/company/governance` → 替换为 `cn/company/majority-shareholders`（前十大股东）和 `cn/company/nolimit-shareholders`（前十大流通股东）
- `cn/company/violation` → 替换为 `cn/company/measures`（监管措施）和 `cn/company/inquiry`（问询函）

#### Fix 5: 修复 `US-market_us-dividend-aristocrat-calculator/references/data-queries.md`

**文件**: `.claude/skills/US-market_us-dividend-aristocrat-calculator/references/data-queries.md`

**问题**: 美股 Skill 中混入了 A 股 API 路径和 A 股代码示例

**修改**:
1. 删除以下 A 股查询示例（整个代码块）：
   - `cn/company/fundamental/non_financial`（含 `600519`、`000858`、`300750`）
   - `cn/company/dividend`（含 `600519`）
   - `cn/index/candlestick`（含 `000001`）
   - `cn/industry`
2. 保留并补充美股相关查询：
   - `us/company/fundamental/non_financial`（美股基本面，含 `AAPL`、`JNJ`、`KO` 等示例）
   - `us/company/dividend`（美股分红，含 `AAPL` 示例）
   - `us/index/fundamental`（已存在，保留）
3. 更新"本 Skill 常用 API"列表，移除所有 `cn/` 前缀条目，替换为 `us/` 前缀

#### Fix 6: 补全 TODO 内容（按需执行）

**范围**: `stable` 或 `partial` 状态 Skill 中包含 `[TODO]` 的 `methodology.md` 和 `output-template.md`

**策略**: 按 `docs/SKILLS_QUALITY_REMEDIATION_DESIGN.md` 中定义的模板家族批量补全，不在本设计文档中逐一列举具体内容

## Testing Strategy

### Validation Approach

测试策略分两阶段：先在未修复代码上运行探索性测试，确认 bug 存在并理解根因；再在修复后运行验证测试，确认修复正确且无回归。

### Exploratory Bug Condition Checking

**Goal**: 在修复前确认 bug 存在，验证根因分析。

**Test Plan**: 对每类 bug，构造会触发错误的查询命令，在未修复文档指导下执行，观察失败模式。

**Test Cases**:
1. **不存在 API 测试**: 按 `esg-screener/data-queries.md` 执行 `cn/company/esg` 查询（预期：`Api was not found`）
2. **参数冲突测试**: 按 `analysis-market/SKILL.md` 速查表使用 `indexCode` 参数调用 `cn/index/constituents`（预期：`ValidationError: "stockCodes" is required`）
3. **点号路径测试**: 按 `sector-valuation-heat-map/data-queries.md` 使用 `cn.industry.fundamental.sw_2021` 路径（预期：`Api was not found`）
4. **跨市场污染测试**: 按 `us-dividend-aristocrat-calculator/data-queries.md` 使用 `cn/company/dividend` 查询美股分红（预期：返回 A 股数据，与美股分析目标不符）

**Expected Counterexamples**:
- `Api was not found` 错误，确认不存在 API 和点号路径问题
- `ValidationError` 错误，确认参数名冲突问题
- 数据市场错误，确认跨市场污染问题

### Fix Checking

**Goal**: 验证修复后，所有满足 bug condition 的文档均产出正确行为。

**Pseudocode:**
```
FOR ALL X WHERE isBugCondition(X) DO
  result := remediate'(X)
  ASSERT (
    result 中所有 API 路径在 api_new/api-docs/ 或 api_new/akshare_data/ 中存在
    AND result 中所有路径使用斜杠格式
    AND result 中参数名与真值文档一致
    AND result 中不含其他市场的 API 路径或代码
    AND result 中不含 [TODO] 占位符（stable/partial Skill）
  )
END FOR
```

### Preservation Checking

**Goal**: 验证修复操作对未受影响文档无副作用。

**Pseudocode:**
```
FOR ALL X WHERE NOT isBugCondition(X) DO
  ASSERT remediate(X) = remediate'(X)
  // 即：修复操作对已正确的文档不产生任何变更
END FOR
```

**Testing Approach**: 对已验证可用的 Skill（如 `China-market_single-stock-health-check`、`China-market_financial-statement-analyzer`）执行完整分析流程，确认输出与修复前一致。

**Test Cases**:
1. **已验证 Skill 保持不变**: 检查 `single-stock-health-check/references/data-queries.md` 在修复前后内容相同
2. **query_tool.py 行为不变**: 修复前后执行相同的 `cn/company/dividend` 查询，结果一致
3. **analysis-best-practices.md 规则不变**: 确认 `metricsList` 必填、`.mcw` 后缀等规则在修复后仍然有效
4. **美股/港股 Skill 不受影响**: 确认 `US-market_us-financial-statement-analyzer` 等未受污染的 Skill 文档未被修改

### Unit Tests

- 对每个修复文件，逐行检查是否还存在点号路径（`grep "cn\." file.md`）
- 对每个修复文件，检查所有 API 路径是否在 `api_new/api-docs/` 中有对应文档
- 对 `analysis-market/SKILL.md`，验证 `cn/index/constituents` 参数名为 `stockCodes`
- 对 `us-dividend-aristocrat-calculator/data-queries.md`，验证不含任何 `cn/` 前缀路径

### Property-Based Tests

- 对所有 `references/data-queries.md` 文件，验证所有 `--suffix` 参数值均使用斜杠格式（正则：`--suffix "[a-z]+/[a-z]`）
- 对所有 `US-market_*/references/data-queries.md` 文件，验证不含 `cn/` 前缀路径
- 对所有 `HK-market_*/references/data-queries.md` 文件，验证不含 `cn/` 或 `us/` 前缀路径
- 对所有 `stable`/`partial` 状态 Skill 的文档，验证不含 `[TODO]` 字符串

### Integration Tests

- 执行完整的 `sector-valuation-heat-map` 分析流程，验证行业估值数据可正常获取
- 执行完整的 `us-dividend-aristocrat-calculator` 分析流程，验证使用美股 API 返回美股数据
- 执行 `cn/index/constituents` 查询（使用 `stockCodes` 参数），验证成分股数据正常返回
- 执行 `esg-screener` 分析流程，验证降级方案（AkShare ESG 接口）可正常工作
