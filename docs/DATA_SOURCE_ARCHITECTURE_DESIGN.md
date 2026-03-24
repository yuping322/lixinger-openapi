# 数据源架构设计（多 Provider / 最小改动版）

## 1. 背景

当前 A 股估值主链已经形成了可工作的三段式结构：

1. `cn-data-source` 负责按估值场景组织取数步骤与字段映射。
2. `.claude/skills/lixinger-data-query` 负责实际查询执行，当前已同时覆盖理杏仁与部分 AkShare。
3. `company-valuation` 只消费标准化后的 canonical 输入，不直接关心上游 provider。

这条链路已经具备继续扩展的基础，但目前的扩展规则主要分散在多个 `SKILL.md` 中，缺少一份统一的数据源架构设计。为了后续接入更多数据源，同时避免大改 `auto_valuation.py` 和现有 skill，需要一份“最小代码改动”的统一方案。

---

## 2. 设计目标

### 2.1 目标

- 支持未来接入更多数据源，如更多行情、财务、宏观、行业、另类数据 provider。
- 保持下游估值输入稳定，避免 provider 增长导致估值脚本频繁修改。
- 允许字段级混用多个 provider。
- 保留字段来源、报告期、单位、转换方式，方便审计与回溯。
- 优先通过文档规范、目录约定、轻量 registry 解决问题，尽量少加执行层代码。

### 2.2 非目标

- 本阶段不建设统一的重型 SDK。
- 本阶段不重写 `query_tool.py`。
- 本阶段不让 `company-valuation/scripts/auto_valuation.py` 直接感知 provider。
- 本阶段不追求所有 provider 统一成一个复杂运行时框架。

---

## 3. 当前架构判断

### 3.1 当前事实

- `cn-data-source` 是**数据源编排层**，不是可执行适配器。
- `.claude/skills/lixinger-data-query` 是**当前实际执行层**；虽然名字叫 `lixinger-data-query`，但它已经承担“多数据源查询中枢”的角色。
- `data-source-docs` 是**provider 文档摘要/缓存层**，适合做可发现性与轻量 registry，不适合直接承担估值取数。
- `company-valuation` 已经是 **provider-agnostic** 的，只依赖 canonical 输入与 `source_map`。

### 3.2 关键判断

因此最小改动路线不是去改估值计算层，而是：

1. 继续把 `company-valuation` 当成稳定消费层。
2. 把 `cn-data-source` 定位成“按场景装配 canonical 输入”的编排层。
3. 把 `.claude/skills/lixinger-data-query` 继续当成默认执行层，并逐步容纳更多 provider 文档与调用方式。
4. 用 `source_map` / `source_notes` 承担字段级溯源。
5. 用一个轻量 `provider registry` 约定统一 provider 元数据与优先级。

---

## 4. 核心设计原则

### 原则 1：canonical 字段稳定优先

下游一律消费：
- `financials.*`
- `balance_sheet.*`
- `shares.*`
- `market.*`
- `adjustments.*`
- `assumptions.*`

新增 provider 时，优先改“字段映射与优先级”，不改估值公式与主脚本。

### 原则 2：字段级 provenance 必须保留

任一关键字段都应该可以回溯到：
- 来自哪个 provider
- 哪个 dataset / endpoint
- 原始字段名
- 报告期或交易日
- 单位
- 是否做过换算或公式桥接

### 原则 3：执行层允许异构，不强行统一 SDK

不同 provider 可以分别通过：
- HTTP API
- Python package
- 本地脚本
- 本地缓存

接入，但对 `cn-data-source` 和 `company-valuation` 暴露的组织形式要统一。

### 原则 4：按“数据域”管理优先级，而不是按 provider 全局一刀切

例如：
- `financials` 适合理杏仁优先
- `cashflow` 当前适合 AkShare 优先
- `macro` 可能 AkShare 或官方源优先
- `market` 可能理杏仁或交易所源优先

---

## 5. 推荐目标架构

```text
Provider Docs / Metadata
    ├─ data-source-docs
    └─ provider summaries / docs / cache

Execution Adapters
    ├─ lixinger-data-query/query_tool.py
    ├─ api_new/api-docs/
    ├─ api_new/akshare_data/
    └─ future: api_new/{provider}_data/

Domain Orchestration
    └─ cn-data-source
         ├─ 根据估值场景决定需要哪些数据域
         ├─ 根据优先级选择 provider
         ├─ 组装 canonical JSON
         └─ 写入 source_map/source_notes

Valuation Consumption
    └─ company-valuation
         ├─ input-schema.md
         └─ auto_valuation.py
```

### 分层职责

#### A. Provider Docs / Metadata 层
职责：
- 管理 provider 文档摘要
- 记录认证方式、主要 endpoint、数据域覆盖
- 为后续新增 provider 提供可发现性

建议继续复用：
- `.claude/plugins/valuation/skills/data-source-docs/`

#### B. Execution Adapter 层
职责：
- 真正执行请求或脚本调用
- 处理认证、缓存、参数格式、返回结果原样输出
- 不直接负责估值字段标准化

当前默认承载：
- `.claude/skills/lixinger-data-query/`

短期建议：
- 不改 skill 名称
- 继续在其目录下容纳更多 provider 文档与轻量调用说明

#### C. Domain Orchestration 层
职责：
- 面向估值任务选择所需数据域
- 按优先级从多个 provider 取数
- 做单位统一、报告期对齐、字段映射
- 输出 canonical JSON 和 `source_map`

当前承载：
- `.claude/plugins/valuation/skills/cn-data-source/SKILL.md`

#### D. Valuation Consumption 层
职责：
- 消费标准化输入
- 不感知上游 provider
- 只保留必要的 provenance 展示

当前承载：
- `.claude/plugins/valuation/skills/company-valuation/`

---

## 6. 轻量 Provider Registry 设计

本阶段建议先定义**规范**，不强制立即写执行代码消费它。

推荐 registry 逻辑位置：
- 说明文档：本文件
- 后续若要落地 machine-readable 文件，可放在：
  - `.claude/plugins/valuation/skills/data-source-docs/references/provider-registry.json`
  - 或 `.claude/plugins/valuation/skills/cn-data-source/references/provider-registry.json`

推荐结构：

```json
{
  "providers": {
    "lixinger": {
      "role": "primary",
      "type": "api",
      "domains": ["company", "financials", "market", "industry"],
      "executor": "python3 .claude/skills/lixinger-data-query/scripts/query_tool.py",
      "docs_dir": ".claude/skills/lixinger-data-query/api_new/api-docs",
      "auth": "token.cfg",
      "status": "active"
    },
    "akshare": {
      "role": "fallback",
      "type": "python_package",
      "domains": ["cashflow", "macro", "alt_data"],
      "executor": "python3 -c 'import akshare as ak; ...'",
      "docs_dir": ".claude/skills/lixinger-data-query/api_new/akshare_data",
      "auth": "none",
      "status": "active"
    }
  },
  "priority_by_domain": {
    "company": ["lixinger", "manual"],
    "financials": ["lixinger", "akshare", "manual"],
    "cashflow": ["akshare", "lixinger", "manual"],
    "market": ["lixinger", "manual"],
    "macro": ["akshare", "lixinger", "manual"],
    "peers": ["lixinger", "manual"]
  }
}
```

### 这个 registry 的价值

- 统一记录“哪个 provider 负责什么”
- 统一记录“不同数据域的优先级”
- 让 `cn-data-source` 的编排规则可维护，而不是散落在多处文字说明里
- 未来若要加自动路由脚本，可以直接消费这份 registry

---

## 7. canonical 输入与 source_map 约定

### 7.1 canonical 层保持不变

继续使用现有 `company-valuation` 输入 schema，不新增 provider-specific 字段。

### 7.2 `source_map` 标准

建议每个关键字段至少记录：

```json
{
  "financials.revenue": {
    "provider": "lixinger",
    "dataset": "cn.company.fs.non_financial",
    "field": "y.ps.toi.t",
    "period_end": "2024-12-31",
    "unit": "CNY",
    "transform": "/ 1000000"
  }
}
```

推荐扩展字段：
- `provider`
- `dataset`
- `field`
- `period_end`
- `currency`
- `unit`
- `transform`
- `quality_flag`：如 `reported` / `estimated` / `manual`
- `note`

### 7.3 `source_notes` 用法

适合记录：
- 为什么混用了多个 provider
- 是否统一到了合并口径
- 是否存在报告期错位
- 哪些字段为估算值

---

## 8. 数据域拆分建议

建议 `cn-data-source` 以后按数据域组织，而不是按 provider 组织：

1. `company_profile`
2. `financials`
3. `cashflow`
4. `balance_sheet`
5. `market`
6. `dividend`
7. `industry`
8. `peers`
9. `macro`
10. `qoe_support`

每个数据域维护：
- canonical 字段列表
- provider 优先级
- 主 provider 查询模板
- fallback 查询模板
- 单位与口径校验规则

这样新增 provider 时，只是给某些数据域补一套映射，而不是重写整个估值链。

---

## 9. 最小代码改动实施方案

### Phase 0：文档规范先行（现在就可以做）

改动范围：
- `cn-data-source/SKILL.md`
- `company-valuation/references/input-schema.md`
- 本设计文档

目标：
- 统一 `source_map` / `source_notes`
- 明确 provider priority by domain
- 明确新增 provider 的接入位置

### Phase 1：新增 provider 时只做三类改动

#### 1) 补 provider 文档
位置建议：
- `.claude/skills/lixinger-data-query/api_new/{provider}_data/`
- 或保留现有 `api-docs/` / `akshare_data/` 风格

#### 2) 补 `cn-data-source` 映射与优先级
包括：
- 字段映射表
- domain priority
- `source_map` 示例
- 该 provider 适用的数据域

#### 3) 必要时补一个很薄的执行脚本
只有在现有 `query_tool.py` 完全不适配时才新增。

原则：
- 先文档化
- 再轻量脚本化
- 最后才考虑统一路由

### Phase 2：可选的轻量统一路由（未来再做）

如果 provider 数量明显增加，再考虑新增一个很薄的：
- `provider_dispatch.py`

职责只做：
- 根据 provider key 调不同执行器
- 不做估值字段映射
- 不做复杂 business logic

这样不会破坏现有 `query_tool.py`，也不会影响 `auto_valuation.py`。

---

## 10. 新数据源接入 checklist

新增一个 provider 时，建议按以下顺序：

1. 明确它覆盖哪些数据域
2. 确定它是 primary 还是 fallback
3. 写 provider 文档摘要
4. 在执行层增加文档目录或轻量调用脚本
5. 在 `cn-data-source` 中补字段映射
6. 给 canonical JSON 增加 `source_map` 示例
7. 检查单位、币种、报告期、合并口径
8. 只在 canonical 字段不够时才改 `input-schema.md`
9. 只有在估值逻辑真的需要新字段时才改 `auto_valuation.py`

---

## 11. 对当前仓库的具体建议

### 11.1 立即保持不动的部分

为了最小改动，以下部分短期不要动：
- `.claude/plugins/valuation/skills/company-valuation/scripts/auto_valuation.py`
- 现有 canonical 字段名
- 现有 QoE / normalization 结构

### 11.2 建议优先维护的部分

- `.claude/plugins/valuation/skills/cn-data-source/SKILL.md`
- `.claude/plugins/valuation/skills/company-valuation/references/input-schema.md`
- `.claude/skills/lixinger-data-query/api_new/`
- `.claude/plugins/valuation/skills/data-source-docs/`

### 11.3 关于 `.claude/skills/lixinger-data-query` 的定位

虽然名称偏向理杏仁，但在最小改动方案里，建议将它视为：

> 当前统一的数据查询执行层（execution hub），而不是单一 provider 的专属实现。

短期不改名，避免：
- skill 路径大面积调整
- 命令文档失效
- 现有调用链断裂

如未来 provider 数量很多，再考虑通过 alias 或新 skill 名做软迁移。

---

## 12. 推荐的目录约定

### 12.1 当前保守方案

```text
.claude/plugins/valuation/skills/cn-data-source/
  SKILL.md

.claude/plugins/valuation/skills/data-source-docs/
  SKILL.md
  references/
  scripts/

.claude/skills/lixinger-data-query/
  SKILL.md
  scripts/
  api_new/
    api-docs/
    akshare_data/
    {future_provider}_data/
```

### 12.2 未来可演进但非必需

若 provider 持续增加，可逐步演进为：

```text
.claude/skills/market-data-query/
  scripts/
    provider_dispatch.py
  providers/
    lixinger/
    akshare/
    future_provider/
```

但这属于第二阶段，不是现在必须做的事。

---

## 13. 方案结论

这套方案的核心不是“新建一个大框架”，而是明确三件事：

1. **下游 canonical schema 固定**：估值层不因 provider 增长而频繁改动。
2. **上游按数据域扩展 provider**：通过 `cn-data-source` 做编排，通过 `source_map` 做溯源。
3. **执行层继续复用现有能力**：短期继续使用 `.claude/skills/lixinger-data-query` 作为 execution hub，只在必要时增加轻量适配脚本。

这样做的好处是：
- 对现有代码影响最小
- 接入新 provider 的成本可控
- 估值结果可追溯
- 后续若要自动化升级，也有清晰演进路径
