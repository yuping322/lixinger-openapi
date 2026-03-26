# Query Data Plugin 设计文档

## 1. 文档信息

- 状态：Proposal
- 日期：2026-03-25
- 作用范围：`/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/plugins/query_data`

---

## 2. 背景

`query_data` 当前承担的是一个混合职责：

1. 多个金融与搜索 provider 的本地文档仓。
2. 理杏仁查询工具的实际执行入口。
3. 其他 provider 的 smoke test 集合。
4. 面向 LLM 的参考说明与示例集合。

它已经具备明显价值，因为：

- provider 覆盖面广。
- 文档已经本地化，离线可读。
- 理杏仁查询链路可直接运行。
- 对后续 skill 和 agent 来说，这里已经天然像一个“数据源底座”。

但它也处在一个过渡状态：

- 目录从旧的 `skills/lixinger-data-query` 向 `.claude/plugins/query_data` 迁移尚未完成。
- “插件”“skill”“文档包”“测试脚本”几种形态叠加在一起，边界不清晰。
- 大部分 provider 只有文档，没有统一执行层。
- 仓库内外部引用存在路径漂移和命名漂移。

本设计文档的目标不是把它重写成重型统一数据平台，而是把它升级为一个可维护、可扩展、可被其他技能稳定复用的轻量查询插件。

---

## 3. 当前状态快照

基于当前仓库实物，`query_data` 具有以下特征：

- 位于 `.claude/plugins/query_data`，但当前目录下没有 `.claude-plugin/plugin.json`。
- 根目录下已有：
  - `README.md`
  - `LLM_USAGE_GUIDE.md`
  - `API_KEYWORD_INDEX.md`
  - `test_datasource.py`
  - `examples.py`
  - `.env.example`
- 当前共有 14 个 provider pack 目录：
  - `akshare`
  - `alltick-api-docs`
  - `alphavantage-api-docs`
  - `brave-search-api-docs`
  - `eodhd-api-docs`
  - `eulerpool-api-docs`
  - `financial-datasets-api-docs`
  - `financial-modeling-prep-api-docs`
  - `finnhub-api-docs`
  - `lixinger-api-docs`
  - `massive-api-docs`
  - `serpapi-ai-overview`
  - `tavily-api-docs`
  - `tiingo-api-docs`
- 上述 provider 合计约 4940 个 Markdown 文件。
- 真正包含执行脚本的 provider 只有 `lixinger-api-docs`。
- 根目录的 `test_datasource.py` 提供 13 个 provider 的最小 smoke test，但不是统一查询接口。

### 3.1 现状定位

可以把当前 `query_data` 理解为：

- 一个 provider docs registry 的雏形。
- 一个以理杏仁为主的 execution hub。
- 一个面向 LLM 的离线知识包。

它还不是：

- 一个完整的 Claude/Codex 插件包。
- 一个统一的 provider 适配层。
- 一个稳定的、可编排的多数据源查询运行时。

---

## 4. 关键问题总结

### 4.1 插件形态未闭环

其他插件目录如 `.claude/plugins/valuation` 和 `.claude/plugins/deep-research` 都具备 `.claude-plugin/plugin.json`，而 `query_data` 当前缺少该文件。

影响：

- 插件元信息缺失。
- 难以被统一注册、发现和管理。
- 当前更像“放在 plugins 目录里的资料包”，而不是一个正式插件。

### 4.2 目录与命名仍在迁移中

仓库仍同时存在以下几种表述：

- `.claude/plugins/query_data`
- `.claude/skills/lixinger-data-query`
- `skills/lixinger-data-query`

影响：

- README、架构文档、回归测试、skill 文档之间容易互相指向旧路径。
- 新接手的人很难判断哪一个才是当前事实来源。
- 后续自动化脚本和工具调用容易继续固化旧路径。

### 4.3 provider 文档丰富，但执行能力严重不对称

当前状态是“文档很多，统一可执行入口很少”：

- `lixinger-api-docs` 有 `query_tool.py` 和缓存逻辑。
- 其他 provider 大多只有 `SKILL.md + docs/`。
- 根目录的 `test_datasource.py` 只能验证“能否打通一个最小请求”，不能支持任务级查询工作流。

影响：

- provider 扩展快，但运行时复用弱。
- 上层技能仍需要知道每个 provider 的调用细节。
- 无法形成稳定的“发现 -> 选择 -> 执行 -> 溯源”闭环。

### 4.4 环境变量命名不一致

根目录文档和 `.env.example` 采用大写命名，例如：

- `EODHD_API_KEY`
- `FINANCIALDATASETS_API_KEY`
- `SERP_API_KEY`

但 `test_datasource.py` 中部分实现读取的是小写变量：

- `eodhd_api_key`
- `financialdatasets_api_key`
- `serp_api_key`

影响：

- 按文档配置后，测试仍会失败。
- 配置成功率降低，问题排查成本高。

### 4.5 文档结构和真实目录不一致

多处文档仍引用旧结构，例如 `api_new/api-docs/`，但 `lixinger-api-docs` 当前实际目录已经是 `docs/`。

影响：

- LLM 按文档操作时，容易打开不存在的路径。
- 维护者无法确认哪些说明已过期。

### 4.6 “无需依赖”表述不准确

`query_tool.py` 当前依赖：

- `pandas`
- `requests`
- `duckdb`

虽然当前机器上可以运行 `--help`，但它并不是严格意义上的“零依赖工具”。

影响：

- 文档承诺和真实运行条件不一致。
- 在新环境中容易出现“按文档操作但无法启动”的问题。

### 4.7 缺少统一的 provider 元数据层

现在每个 provider 基本都有自己的 `SKILL.md`，但缺少统一、结构化、可程序读取的 metadata。

结果是：

- provider 能力只能靠自然语言文档理解。
- 无法稳定做路由、筛选、能力比较和自动健康检查。

### 4.8 测试能力偏弱

当前测试主要是 smoke test，缺少：

- 配置合法性检查
- provider metadata 校验
- 文档路径一致性检查
- 统一命令级回归
- 失败分类和错误提示标准化

---

## 5. 设计目标

### 5.1 目标

1. 让 `query_data` 成为正式、可注册的插件。
2. 保留当前“轻量 Provider Pack”思路，不引入重型统一 SDK。
3. 为每个 provider 建立最小结构化元数据，便于发现和路由。
4. 在不破坏现有理杏仁工作流的前提下，补齐统一查询入口的骨架。
5. 把文档、执行、测试三层职责拆清楚。
6. 让其他 skill 能稳定引用它，而不依赖过时路径。
7. 建立低成本健康检查机制，避免“文档存在但不可用”。

### 5.2 非目标

本阶段不做以下事情：

1. 不为所有 provider 建全量 canonical schema。
2. 不为所有 provider 建完整 Python SDK。
3. 不强行把 AkShare、搜索 API、证券 API 统一成同一种返回结构。
4. 不重写现有估值技能的业务逻辑。
5. 不要求一次性迁移所有引用到新目录结构。

---

## 6. 设计原则

### 6.1 轻接入，强约束

provider 的接入成本必须继续保持低，但对最小元数据、目录规范、鉴权声明、示例命令要有统一约束。

### 6.2 文档先可用，再追求抽象

不是先设计重型接口，而是先确保：

- 文档能找到
- 命令能跑
- 鉴权清晰
- 结果可解释

### 6.3 保持理杏仁链路稳定

`lixinger-api-docs/scripts/query_tool.py` 已经被多处引用，应视为现阶段兼容锚点，升级方案要包裹它，而不是先破坏它。

### 6.4 结构化元数据优先于自由文本猜测

后续的 provider 发现、路由、健康检查、能力矩阵都应优先依赖结构化 metadata，而不是靠读取大段 Markdown 推断。

### 6.5 先做“统一入口骨架”，不做“统一语义平台”

统一的是：

- provider 声明
- 鉴权约定
- 入口命令
- 健康检查
- 结果溯源

不统一的是：

- 全部返回字段
- 全部查询参数
- 全部业务语义

---

## 7. 目标架构

### 7.1 推荐目录结构

```text
.claude/plugins/query_data/
├── .claude-plugin/
│   └── plugin.json
├── README.md
├── LLM_USAGE_GUIDE.md
├── docs/
│   ├── QUERY_DATA_PLUGIN_DESIGN.md
│   ├── PROVIDER_PACK_SPEC.md
│   └── MIGRATION_GUIDE.md
├── tools/
│   ├── provider_smoke_test.py
│   ├── provider_catalog.py
│   ├── doctor.py
│   └── compat_paths.py
├── generated/
│   ├── provider_index.json
│   ├── capability_matrix.json
│   └── keyword_index.md
├── providers/
│   ├── lixinger/
│   │   ├── provider.yaml
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── docs/
│   │   └── scripts/
│   ├── finnhub/
│   │   ├── provider.yaml
│   │   ├── SKILL.md
│   │   └── docs/
│   └── ...
├── README_COMPAT.md
└── legacy/
    └── ...
```

### 7.2 兼容策略

由于当前目录已经被实际使用，建议分两阶段处理：

#### Phase A：逻辑升级，不立即搬家

先保留现有目录名，例如：

- `lixinger-api-docs`
- `finnhub-api-docs`
- `tavily-api-docs`

在现有目录内新增 `provider.yaml`，并补齐根级插件元信息与统一工具。

#### Phase B：结构收拢

当所有引用都完成迁移后，再把 provider 收拢到 `providers/` 下，旧路径只保留兼容层或说明文档。

这能避免一次性大规模移动文件，降低回归风险。

---

## 8. Provider Pack 最小规范

每个 provider 必须具备以下最小资产。

### 8.1 必填文件

1. `SKILL.md`
2. `provider.yaml`
3. `docs/` 或等价文档目录

### 8.2 可选文件

1. `README.md`
2. `scripts/`
3. `examples/`
4. `tests/`

### 8.3 `provider.yaml` 推荐字段

```yaml
provider_key: lixinger
display_name: Lixinger OpenAPI
kind: market_data
status: active
auth:
  type: env_or_file
  env_vars:
    - LIXINGER_TOKEN
  file_hints:
    - token.cfg
capabilities:
  - cn_equity_fundamental
  - cn_equity_financials
  - hk_equity_market_data
  - us_equity_market_data
entrypoints:
  smoke_test:
    command: python3 test_datasource.py --source lixinger
  query:
    command: python3 lixinger-api-docs/scripts/query_tool.py --suffix "cn/company" --params '{"stockCodes":["600519"]}'
docs:
  primary_index: lixinger-api-docs/README.md
  keyword_index: API_KEYWORD_INDEX.md
limits:
  rate_limit_notes: account-tier-based
  known_gaps:
    - no_unified_schema
provenance:
  api_base_url: https://open.lixinger.com/api/
```

### 8.4 必须满足的约束

每个 provider 至少应声明：

1. 如何鉴权
2. 用来验证联通性的最小命令
3. 能覆盖什么类型的数据
4. 已知限制
5. 主文档入口

---

## 9. 统一能力分层

### 9.1 文档层

职责：

- 承载原始或整理后的 provider 文档。
- 供 LLM、本地检索、人工排查使用。

约束：

- 不承担运行时状态。
- 不承担结构化路由规则。

### 9.2 元数据层

职责：

- 声明 provider 能力、鉴权方式、命令入口、已知限制。
- 供 catalog、doctor、routing 使用。

产物：

- `provider.yaml`
- `generated/provider_index.json`

### 9.3 执行层

职责：

- 提供最小可运行命令。
- 管理 smoke test、query 命令、缓存、结果格式。

说明：

- 理杏仁保留现有 `query_tool.py`。
- 其他 provider 先允许只有 `smoke_test`。
- 后续按需求逐步增加 `query` 入口，不要求一步到位。

### 9.4 路由与溯源层

职责：

- 根据任务筛选 provider。
- 记录本次使用的是哪个 provider、哪个接口、哪种鉴权。

这层可以很轻，不要求在 `query_data` 内完成复杂业务编排，但应提供可复用的 provider catalog 输出。

---

## 10. 推荐工具面

### 10.1 `provider_catalog.py`

目标：

- 输出所有 provider 的结构化索引。
- 支持按 capability、status、auth、has_query_entrypoint 筛选。

示例：

```bash
python3 tools/provider_catalog.py --capability cn_equity_fundamental
```

### 10.2 `provider_smoke_test.py`

目标：

- 统一触发所有 provider 或单个 provider 的 smoke test。
- 结果标准化为 `ok / fail / skipped`。

示例：

```bash
python3 tools/provider_smoke_test.py --provider lixinger
python3 tools/provider_smoke_test.py --all
```

### 10.3 `doctor.py`

目标：

- 检查插件完整性。
- 检查 manifest、metadata、路径引用、环境变量规范。
- 用于 CI 和本地自检。

检查项至少包括：

1. 是否存在 `.claude-plugin/plugin.json`
2. 每个 provider 是否存在 `SKILL.md`
3. 每个 provider 是否存在 `provider.yaml`
4. `provider.yaml` 中声明的 env var 是否符合统一命名规范
5. 根 README 和 skill 文档中是否残留废弃路径

---

## 11. 配置与密钥规范

### 11.1 环境变量命名规范

统一采用大写 snake case，例如：

- `LIXINGER_TOKEN`
- `FINNHUB_API_KEY`
- `EODHD_API_KEY`
- `SERP_API_KEY`

不再新增小写变量名。

### 11.2 兼容策略

短期内可以在代码中兼容读取旧变量名，但：

- 文档只保留新规范。
- `doctor.py` 应提示旧变量名已废弃。

### 11.3 文件密钥规范

仅允许少数必须依赖文件的 provider 使用文件型鉴权，并在 metadata 中显式声明：

- 文件名
- 搜索顺序
- 是否可被环境变量覆盖

---

## 12. 文档治理方案

### 12.1 单一事实来源

以下内容应各自只有一个主入口：

- 插件入口说明：根 `README.md`
- 设计原则：`docs/QUERY_DATA_PLUGIN_DESIGN.md`
- Provider 接入规范：`docs/PROVIDER_PACK_SPEC.md`
- LLM 使用策略：`LLM_USAGE_GUIDE.md`
- 自动生成索引：`generated/keyword_index.md`

### 12.2 禁止继续扩散旧路径

所有新文档都应以 `.claude/plugins/query_data` 为主路径。

旧路径：

- `.claude/skills/lixinger-data-query`
- `skills/lixinger-data-query`

只允许出现在迁移说明中，不应继续作为推荐路径。

### 12.3 自动生成索引

`API_KEYWORD_INDEX.md` 这类文件不应完全手工维护，建议改为生成产物，并保留生成脚本。

---

## 13. 测试策略

### 13.1 测试分层

1. 结构测试
   - 目录、manifest、metadata 是否存在
2. 配置测试
   - env var 名称是否规范
   - provider metadata 是否可解析
3. smoke test
   - 最小 API 请求是否能成功
4. 命令级回归
   - 关键入口命令参数是否仍可解析

### 13.2 最低验收标准

每次新增或修改 provider，至少需要：

1. 通过 metadata 校验
2. 通过路径一致性检查
3. 至少一个 smoke test 可运行

### 13.3 理杏仁专项回归

因为理杏仁是当前主执行链路，应额外覆盖：

1. `query_tool.py --help`
2. token 加载顺序
3. 缓存读写
4. `--columns / --row-filter / --flatten / --limit`

---

## 14. 分阶段升级计划

### Phase 0：立即修复

目标：先把“容易踩坑”的问题降下来。

任务：

1. 为 `.claude/plugins/query_data` 增加 `.claude-plugin/plugin.json`
2. 统一 `.env.example`、README、测试脚本中的环境变量命名
3. 扫描并修复仓库内对旧路径的高频引用
4. 修正文档中 `api_new/api-docs` 等过期路径
5. 在 README 中明确 `query_tool.py` 的真实依赖

### Phase 1：元数据化

目标：让 provider 可被程序发现和检查。

任务：

1. 为每个 provider 新增 `provider.yaml`
2. 增加 `tools/provider_catalog.py`
3. 增加 `tools/doctor.py`
4. 生成 `generated/provider_index.json`

### Phase 2：统一测试入口

目标：把散落的 smoke test 收拢。

任务：

1. 用 `provider_smoke_test.py` 统一调度 provider 测试
2. 保留 `test_datasource.py` 作为兼容层
3. 标准化错误码和输出格式

### Phase 3：逐步补齐查询入口

目标：让非理杏仁 provider 也具备最小 query 能力。

任务：

1. 优先为常用 provider 增加 `query` 入口
2. 从最常见的行情、基础信息、新闻、搜索场景开始
3. 不追求全量覆盖，只做高价值最小集合

### Phase 4：目录收拢

目标：把迁移做完整。

任务：

1. 统一 provider 目录命名
2. 视情况收拢到 `providers/`
3. 清理旧路径兼容说明

---

## 15. 推荐优先级

### P0

1. 插件 manifest
2. 环境变量命名修复
3. 文档路径修复
4. 依赖说明修复

### P1

1. `provider.yaml`
2. `doctor.py`
3. `provider_catalog.py`

### P2

1. 统一 smoke test 入口
2. 常用 provider query 入口
3. 自动生成 capability/keyword 索引

### P3

1. 目录重构
2. 旧路径清理
3. 更细的 provenance 输出

---

## 16. 风险与权衡

### 16.1 不立即重构目录的好处

- 风险低。
- 不会一次性打断现有 skill 和测试引用。
- 便于逐步迁移。

代价：

- 短期内目录看起来仍不够整洁。

### 16.2 不做统一 schema 的好处

- 接入成本低。
- provider 扩张速度快。
- 不会因为 canonical 治理拖慢整个插件演进。

代价：

- 上层任务仍需要做 task-local extraction。

这个代价当前是可接受的，因为它明显小于“为所有 provider 预建统一大表”的维护成本。

---

## 17. 成功标准

当以下条件同时满足时，可认为 `query_data` 完成了本轮升级：

1. 它拥有正式插件 manifest。
2. 所有 provider 都具备最小 metadata。
3. 文档不再默认引用旧路径。
4. 环境变量命名完全统一。
5. 能用单一命令完成插件健康检查。
6. 理杏仁链路保持兼容。
7. 至少 3 到 5 个高频 provider 拥有最小 query 入口，而不仅是 smoke test。

---

## 18. 结论

`query_data` 最值得保留的，不是它已经“统一了所有数据源”，而是它已经形成了一个非常有价值的轻量基础设施雏形：

- 文档集中
- provider 多
- 主链路可跑
- 易于继续扩展

下一步最合理的方向，不是把它做成重型平台，而是把它补齐为一个正式插件，并通过最小元数据、统一健康检查和渐进式执行入口，把“文档仓 + 脚本集合”升级成“可维护的多数据源查询底座”。
