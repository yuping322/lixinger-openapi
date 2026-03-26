# Stock Screener Plugin

可扩展的股票策略筛选插件。

当前作用：
- 统一承载股票策略筛选类 skill
- 为每个策略提供独立 `/command` 入口
- 统一约定先用 `lixinger-screener` 建候选池，再按策略需要补充其他数据

## 当前已接入策略

| Strategy | Description |
|---|---|
| `undervalued-stock-screener` | 低估股票筛选器 |
| `high-dividend-strategy` | 高股息策略 |
| `quant-factor-screener` | 量化因子筛选器 |
| `small-cap-growth-identifier` | 小盘成长股识别器 |
| `bse-selection-analyzer` | 北交所选股分析器 |
| `esg-screener` | ESG 筛选器 |

## Commands

| Command | Description |
|---|---|
| `/undervalued-stock-screener [股票池/条件]` | 低估值筛选 |
| `/high-dividend-strategy [股票池/条件]` | 高股息筛选 |
| `/quant-factor-screener [股票池/条件]` | 多因子筛选 |
| `/small-cap-growth-identifier [股票池/条件]` | 小盘成长筛选 |
| `/bse-selection-analyzer [股票池/条件]` | 北交所标的筛选 |
| `/esg-screener [股票池/条件]` | ESG 候选池与补充评分 |

## Data Layer

### 1. 通用建池 / 筛选

统一优先复用：
- `.claude/skills/lixinger-screener`

定位：
- 通用股票筛选
- 条件表达
- 自然语言筛选
- request / browser 双入口
- 推荐顺序：`request` 默认，`browser` 仅用于字段映射验证、自然语言试错或 request 异常时兜底

约束：
- 不把具体策略逻辑塞进 `lixinger-screener`
- 它只负责候选池与基础筛选，不负责各策略的完整分析编排

### 2. 补充数据

当策略需要更多字段时，按需补充：
- `.claude/plugins/query_data`
- 其他外部接口（如 AkShare、监管/治理类接口）

## Directory Layout

```text
.claude/plugins/stock-screener/
├── README.md
├── .claude-plugin/plugin.json
├── commands/
│   ├── undervalued-stock-screener.md
│   ├── high-dividend-strategy.md
│   ├── quant-factor-screener.md
│   ├── small-cap-growth-identifier.md
│   ├── bse-selection-analyzer.md
│   └── esg-screener.md
└── skills/
    ├── undervalued-stock-screener/
    ├── high-dividend-strategy/
    ├── quant-factor-screener/
    ├── small-cap-growth-identifier/
    ├── bse-selection-analyzer/
    └── esg-screener/
```

## Expansion Rule

后续增加新策略时：
1. 在 `skills/` 下新增策略目录
2. 在 `commands/` 下新增同名命令文档
3. 更新本 README 的“当前已接入策略”列表
4. 如需被全局 skill 索引发现，同步更新 `.claude/plugins.json`

## Recommended Workflow

1. 先确定筛选范围、行业、板块、数量与排序逻辑
2. 使用 `lixinger-screener` 生成候选池
3. 对入围名单做策略专属打分或深度分析
4. 仅在需要时补充额外数据，避免全市场逐股深拉
