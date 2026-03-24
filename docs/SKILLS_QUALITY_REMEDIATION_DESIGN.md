# Skills 质量整治设计文档

## 1. 文档目的

本文档用于指导 `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills` 下现有 Skills 的质量整治工作。

本轮整治目标不是继续扩张新 Skill，而是先解决现有 Skill 文档体系中的交付问题，尤其是以下三类高优问题：

1. 高频主入口 Skill 的方法论与输出补齐
2. Draft 方法论补齐
3. TODO 模板补齐

这三类问题直接决定：

- Skill 能否给出稳定、可复用、可解释的分析结果
- 用户首次使用 Skill 时是否能拿到完整输出
- 当前 108 个 Skill 是否只是“目录很多”，还是“真的能交付”

---

## 2. 当前现状与关键证据

### 2.1 Skills 总量与映射现状

`/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/analysis-market/SKILLS_MAP.md` 当前记录：

- 总计 108 个 Skill
- A 股 57 个
- 港股 14 个
- 美股 36 个
- 基础工具 1 个

问题在于：`SKILLS_MAP.md` 更偏向“覆盖面展示”和“新增缺口规划”，但没有真实反映每个 Skill 的交付成熟度。

### 2.2 当前最影响交付质量的不是“缺 Skill”，而是“文档未收口”

从当前文档可以明确看到三类直接影响交付的缺口：

#### 1）高频主入口 Skill 已有流程，但“方法论-模板-结论”闭环不完整

代表入口包括：

- `China-market_financial-statement-analyzer`
- `China-market_single-stock-health-check`
- `China-market_market-overview-dashboard`
- `China-market_industry-board-analyzer`
- `China-market_portfolio-health-check`
- `US-market_us-financial-statement-analyzer`
- `US-market_us-portfolio-health-check`
- `HK-market_hk-market-overview`
- `HK-market_hk-financial-statement`

这些 Skill 往往最容易成为主入口或协同入口。一旦方法论、阈值、输出模板不完整，整个体系的“首次体验”会直接变差。

#### 2）存在明确的 Draft 方法论文件

当前检出 4 份带核心 `[TODO]` 的方法论文档：

- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/China-market_macro-liquidity-monitor/references/methodology.md`
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/China-market_event-study/references/methodology.md`
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/US-market_us-peer-comparison-analyzer/references/methodology.md`
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/US-market_us-tax-aware-rebalancing-planner/references/methodology.md`

这类文件的问题不是“小瑕疵”，而是：

- 指标口径没定
- 阈值来源没定
- 边界条件没定
- 数据缺失降级没定

也就是说，Skill 即便能写出流程，也未形成稳定判断依据。

#### 3）存在大量 TODO 输出模板

当前检出 57 个包含 `[TODO]` 的 Markdown 文件，其中：

- 4 个为 `methodology.md`
- 53 个为 `output-template.md`

也就是说，大量 Skill 的最终输出层仍停留在 Draft 状态。

典型模板形态是：

- 结论摘要处仍为 `[TODO]`
- 风险与监控表格仅有空骨架
- 下一步建议仍为 `[TODO]`
- 没有置信度、缺失数据说明、补充核验项

这会导致 Skill 即使拿到了数据，也难以稳定产出一份结构完整的结果。

### 2.3 与这三类问题相比，参数/API/复制污染属于下一层问题

参数坑、未验证 API、AkShare 风险、跨市场复制污染仍然重要，但如果当前主入口 Skill 的方法论和输出层不完整，那么即便接口修通，最终交付仍然会显得“浅、散、空”。

因此，本轮优先顺序调整为：

1. 先补“结果层”
2. 再补“判断层”
3. 最后再系统修“查询层”和“状态层”

---

## 3. 根因判断

现有 Skills 的核心问题，不是“选题不够多”，而是“交付闭环没有完成”。

### 3.1 把流程文档当成了完成态 Skill

很多 Skill 已具备：

- 工作流程
- 指标清单
- 参考查询

但缺少：

- 指标口径定义
- 阈值与样本期说明
- 失效条件与边界条件
- 结构化输出模板
- 缺失数据和降级说明

### 3.2 方法论文档没有真正成为判断依据

部分 Skill 虽引用 `references/methodology.md` 或相近文件，但方法论文档要么仍为 Draft，要么没有形成：

- 计算公式
- 分位方法
- 信号阈值
- 结论分级
- 无效化条件

这样会导致不同人或不同轮次分析时，结论口径漂移。

### 3.3 输出模板没有产品化

大量 `output-template.md` 仍停留在“空模板”阶段。结果是：

- 输出内容不稳定
- Skill 之间风格不统一
- 很难形成可复用的标准产物
- 后续无法被编排型 Skill 稳定消费

### 3.4 高流量入口没有优先维护

从体系结构看，真正最应该优先稳定的是主入口型 Skill，而不是长尾专项 Skill。因为主入口型 Skill：

- 被引用概率更高
- 覆盖分析面更广
- 更容易成为后续 Skill 的上游
- 一旦质量提升，会立刻带动整体观感提升

---

## 4. 本轮整治目标

### 4.1 总体目标

建立一个“先能稳定交付，再逐步提高可执行精度”的 Skill 文档体系。

### 4.2 具体目标

1. 为高频主入口 Skill 补齐完整的方法论与输出结构。
2. 清空当前 Draft 方法论中的核心 `[TODO]`。
3. 清空当前输出模板中的核心 `[TODO]`。
4. 形成统一的模板家族，而不是 50+ 份空壳模板各自漂移。
5. 为后续参数/API/状态整治打下统一的结果层基线。

### 4.3 非目标

本轮暂不把以下事项作为最高优先级：

- 新增 Skill 扩张
- 全量 API 真值校验
- 全量 AkShare 依赖重构
- 全量筛选类 Skill 执行模型改造
- `SKILLS_MAP.md` 全面状态重标

这些事项保留，但后置到本轮“交付层补齐”之后。

---

## 5. 质量模型设计

### 5.1 Skill 文档的最小完成标准

一个 Skill 至少需要同时具备以下 4 层内容：

1. **工作流程层**：这个 Skill 做什么
2. **方法论层**：这个 Skill 如何判断
3. **查询说明层**：这个 Skill 如何取数
4. **输出模板层**：这个 Skill 如何稳定交付

本轮优先补的是第 2 层与第 4 层。

### 5.2 方法论文档最低要求

每个高频或正式可用 Skill 的方法论文档至少包含：

- 数据口径与字段映射
- 时间窗口与频率
- 核心指标与计算公式
- 标准化/分位/排名方法
- 信号定义与阈值
- 边界条件与无效化条件
- 缺失数据处理与降级策略
- 特定市场注意事项

### 5.3 输出模板最低要求

每个正式可用 Skill 的输出模板至少包含：

- 结论摘要
- 关键数据表
- 分析解释
- 风险清单
- 缺失数据说明
- 监控清单或下一步建议
- 免责声明

---

## 6. 优先级设计（按当前业务要求重排）

### 6.1 总原则

当前优先级遵循以下顺序：

1. 先补高频主入口 Skill 的方法论与输出
2. 再补所有 Draft 方法论
3. 再补 TODO 模板
4. 最后处理参数/API/状态等系统性问题

### 6.2 优先级规则

#### P0：立即执行

- 高频主入口 Skill 的方法论补齐
- 高频主入口 Skill 的输出模板补齐
- Draft 方法论补齐
- TODO 模板补齐
- 模板家族标准化

#### P1：次优先级

- 参数规则下沉至各 Skill
- 未验证 API 清理
- 文档参数冲突修复
- `SKILLS_MAP.md` 状态重标

#### P2：后续跟进

- 筛选类 Skill 执行模型重构
- AkShare 依赖 Skill 降级设计
- 跨市场复制污染清理
- 长尾 Skill 全量核验

#### P3：后置扩张

- 新 Skill 扩张
- 跨市场联动增强
- 另类数据扩展
- 高频量化与短线扩展

---

## 7. 分阶段整治路线图

## Phase 0：建立补齐基线（P0）

### 目标

先把“要补什么、按什么标准补”统一下来。

### 工作项

1. 确认高频主入口 Skill 清单。
2. 确认当前 Draft 方法论清单。
3. 统计 TODO 模板并按模板类型分组。
4. 形成统一的 `methodology` 最小字段标准。
5. 形成统一的 `output-template` 最小字段标准。

### 交付物

- 主入口 Skill 清单
- Draft 方法论清单
- TODO 模板分类表
- 方法论标准骨架
- 输出模板标准骨架

### 验收标准

- 所有 P0 对象均有明确归属
- 不再“看到 TODO 再临时补”，而是先有统一基线

---

## Phase 1：补齐高频主入口 Skill 的方法论与输出（P0）

### 目标

优先修复最容易被调用、最能代表整个体系质量的主入口 Skill。

### 建议优先 Skill

#### A股主入口

1. `China-market_financial-statement-analyzer`
2. `China-market_single-stock-health-check`
3. `China-market_market-overview-dashboard`
4. `China-market_industry-board-analyzer`
5. `China-market_portfolio-health-check`
6. `China-market_peer-comparison-analyzer`
7. `China-market_weekly-market-brief-generator`

#### 美股主入口

8. `US-market_us-financial-statement-analyzer`
9. `US-market_us-portfolio-health-check`
10. `US-market_us-weekly-market-brief-generator`

#### 港股主入口

11. `HK-market_hk-market-overview`
12. `HK-market_hk-financial-statement`

### 补齐项

每个主入口 Skill 至少补齐以下内容：

- 指标口径
- 阈值来源
- 样本期说明
- 评分逻辑
- 失效场景
- 缺失数据降级
- 结论模板
- 风险与监控段
- 下一步建议段

### 交付要求

每个 Skill 必须形成以下闭环：

- `SKILL.md`：说明任务与流程
- `references/methodology.md` 或等价方法论文档：说明判断标准
- `references/output-template.md`：说明输出结构
- 三者之间口径一致

### 验收标准

- 不再出现“只有流程，没有判断依据”
- 不再出现“只能讲思路，无法稳定产出报告”
- 主入口 Skill 至少能输出一份完整、结构化、可复用结果

---

## Phase 2：补齐 Draft 方法论（P0）

### 目标

把当前仍为 Draft 的方法论文档全部补齐为可使用状态，或明确降级。

### 当前清单

1. `China-market_macro-liquidity-monitor/references/methodology.md`
2. `China-market_event-study/references/methodology.md`
3. `US-market_us-peer-comparison-analyzer/references/methodology.md`
4. `US-market_us-tax-aware-rebalancing-planner/references/methodology.md`

### 每份 Draft 方法论必须补齐的内容

#### A. 数据口径

- 数据源与字段映射
- 更新频率
- 默认时间窗口
- 样本期与比较基准

#### B. 核心指标

- 指标列表
- 计算公式
- 分位/排名/标准化逻辑

#### C. 信号与阈值

- 触发条件
- 解除条件
- 无效化条件
- 阈值来源说明

#### D. 边界条件与降级

- 数据缺失处理
- 异常值处理
- 接口不稳定时的替代判断
- 哪些结论只能降级为“观察”

#### E. 市场特殊说明

- A股 / 港股 / 美股制度差异
- 税制、交易制度、披露制度等背景差异

### 验收标准

- Draft 文件中的核心 `[TODO]` 清零
- 每份方法论文档都能独立支撑判断逻辑
- 不再依赖“口头默认规则”完成分析

---

## Phase 3：补齐 TODO 模板（P0）

### 目标

不再逐个补“空模板”，而是先建立模板家族，再批量收口。

### 当前现状

当前检出 53 份 `output-template.md` 含 `[TODO]`。如果逐个手工补，效率低且风格容易继续漂移。因此建议按模板类型归并。

### 模板家族建议

#### 模板家族 A：一页诊断 / 体检类

适用代表：

- `single-stock-health-check`
- `portfolio-health-check`
- `shareholder-risk-check`
- `goodwill-risk-monitor`
- `equity-pledge-risk-monitor`

标准结构：

1. 综合结论
2. 核心评分或风险等级
3. 关键指标表
4. 红灯项 / 黄灯项
5. 监控建议
6. 需补充数据
7. 免责声明

#### 模板家族 B：市场概览 / 仪表板类

适用代表：

- `market-overview-dashboard`
- `market-breadth-monitor`
- `volatility-regime-monitor`
- `fund-flow-monitor`
- `valuation-regime-detector`

标准结构：

1. 市场结论摘要
2. 核心市场指标面板
3. 主要驱动项
4. 风险与拐点观察
5. 未来 1–4 周监控点
6. 缺失数据说明
7. 免责声明

#### 模板家族 C：事件 / 公告 / 监控类

适用代表：

- `disclosure-notice-monitor`
- `dragon-tiger-list-analyzer`
- `ipo-newlist-monitor`
- `dividend-corporate-action-tracker`
- `event-study`

标准结构：

1. 事件摘要
2. 关键事实表
3. 事件影响分析
4. 风险提示
5. 后续验证项
6. 数据缺失说明
7. 免责声明

#### 模板家族 D：组合 / 调仓 / 配置类

适用代表：

- `rebalancing-planner`
- `portfolio-monitor-orchestrator`
- `etf-allocator`
- `risk-adjusted-return-optimizer`
- `us-tax-aware-rebalancing-planner`

标准结构：

1. 当前状态诊断
2. 组合暴露与约束
3. 建议动作
4. 预期改善点
5. 风险与交易摩擦
6. 执行优先级
7. 免责声明

#### 模板家族 E：研究 / 备忘录 / 周报类

适用代表：

- `equity-research-orchestrator`
- `investment-memo-generator`
- `weekly-market-brief-generator`
- `us-investment-memo-generator`
- `us-weekly-market-brief-generator`

标准结构：

1. 核心观点
2. 支撑证据
3. 正反论据
4. 风险清单
5. 需进一步验证的假设
6. 附录或数据摘要
7. 免责声明

### 执行策略

1. 先定义 5 套模板家族的标准结构。
2. 再把 53 份 TODO 模板按家族归类。
3. 最后按家族批量替换，而不是逐份临时编写。

### 验收标准

- TODO 模板的核心 `[TODO]` 清零
- 同类 Skill 输出结构一致
- 后续编排型 Skill 可以稳定消费这些结果

---

## Phase 4：参数 / API / 状态层整治（P1）

### 目标

在结果层和判断层补齐后，再系统处理接口层问题。

### 工作项

1. 参数规则下沉至各 Skill
2. 未验证 API 清理
3. 文档参数冲突修复
4. `SKILLS_MAP.md` 状态重标

### 原因

这些问题仍重要，但当前不再作为最高优先级。因为在主入口 Skill 和模板未成型之前，先修接口并不能立刻改善最终交付质量。

---

## Phase 5：筛选类 / AkShare 风险类整治（P2）

### 目标

在主入口体系稳定后，处理高成本、高失败率的专项 Skill。

### 工作项

1. 筛选类 Skill 改为分阶段候选收缩
2. AkShare Skill 增加三层降级模式
3. 长尾专项 Skill 的输出模板逐步替换为标准模板家族

---

## 8. P0 立即执行清单（按当前优先级排序）

| 排名 | 对象 | 类型 | 主要问题 | 当前动作 |
|---|---|---|---|---|
| 1 | `China-market_single-stock-health-check` | 主入口 Skill | 诊断型入口，需完整评分逻辑与输出卡片 | 补方法论、补一页诊断模板 |
| 2 | `China-market_financial-statement-analyzer` | 主入口 Skill | 财务分析深，但需统一结论结构与阈值解释 | 补方法论口径与完整报告模板 |
| 3 | `China-market_market-overview-dashboard` | 主入口 Skill | 概览型入口，需稳定面板与结论结构 | 补市场面板模板与结论层 |
| 4 | `China-market_industry-board-analyzer` | 主入口 Skill | 板块分析高频使用，需统一对比与风险段 | 补方法论与板块模板 |
| 5 | `China-market_portfolio-health-check` | 主入口 Skill | 组合诊断需评分、风险、建议标准化 | 补诊断框架与组合模板 |
| 6 | `China-market_peer-comparison-analyzer` | 主入口 Skill | 对比分析需明确口径、打分、结论框架 | 补同业对比方法论与模板 |
| 7 | `China-market_weekly-market-brief-generator` | 主入口 Skill | 周报类是高频消费结果，模板必须成熟 | 补周报模板与观察清单 |
| 8 | `US-market_us-financial-statement-analyzer` | 主入口 Skill | 美股主入口需同步成熟，避免中美两套标准脱节 | 补美股财报方法论与模板 |
| 9 | `US-market_us-portfolio-health-check` | 主入口 Skill | 组合体检类需和 A 股保持结构一致 | 补组合模板与差异化口径 |
| 10 | `US-market_us-weekly-market-brief-generator` | 主入口 Skill | 周报模板需标准化 | 补结论、面板、风险结构 |
| 11 | `HK-market_hk-market-overview` | 主入口 Skill | 港股入口型 Skill 需先有稳定输出骨架 | 补市场概览模板 |
| 12 | `HK-market_hk-financial-statement` | 主入口 Skill | 港股财报分析需建立本地口径说明 | 补财报方法论与模板 |
| 13 | `China-market_macro-liquidity-monitor/references/methodology.md` | Draft 方法论 | 核心方法论仍为 Draft | 清空 TODO，补流动性框架 |
| 14 | `China-market_event-study/references/methodology.md` | Draft 方法论 | 事件研究缺口径与阈值 | 清空 TODO，补事件研究框架 |
| 15 | `US-market_us-peer-comparison-analyzer/references/methodology.md` | Draft 方法论 | 同业对比缺指标标准 | 清空 TODO，补比较框架 |
| 16 | `US-market_us-tax-aware-rebalancing-planner/references/methodology.md` | Draft 方法论 | 调仓方法论缺税务逻辑细化 | 清空 TODO，补税务调仓框架 |
| 17 | 一页诊断 / 体检类模板家族 | 模板家族 | 多个风险/体检 Skill 仍是空模板 | 先出统一模板骨架 |
| 18 | 市场概览 / 仪表板类模板家族 | 模板家族 | 市场类输出缺统一结构 | 先出统一模板骨架 |
| 19 | 事件 / 公告 / 监控类模板家族 | 模板家族 | 事件类结论结构不稳定 | 先出统一模板骨架 |
| 20 | 组合 / 调仓 / 配置类模板家族 | 模板家族 | 组合类模板可复用性不足 | 先出统一模板骨架 |
| 21 | 研究 / 备忘录 / 周报类模板家族 | 模板家族 | 研究型结果风格容易漂移 | 先出统一模板骨架 |

---

## 9. 单个 Skill 的标准补齐模板

后续每次补一个 Skill，统一按以下模板推进。

### Step 1：明确 Skill 角色

- 它是不是主入口 Skill
- 它的结果给谁看
- 它是一页诊断、仪表板、监控报告还是研究报告

### Step 2：补方法论

至少补齐：

- 数据口径
- 核心指标
- 计算公式
- 阈值来源
- 边界条件
- 降级策略

### Step 3：补输出模板

至少补齐：

- 结论摘要
- 关键数据表
- 分析解释
- 风险清单
- 缺失数据说明
- 下一步建议

### Step 4：校对 `SKILL.md`

确保：

- `SKILL.md` 中引用的方法论文件存在
- `SKILL.md` 中引用的输出模板存在
- 工作流程与方法论、模板之间没有冲突

### Step 5：标记完成状态

完成后应能明确判断：

- 方法论是否完成
- 模板是否完成
- 是否可进入下一轮参数/API 整治

---

## 10. 建议的实际执行顺序

### 第一批：先补 5 个 A股主入口

1. `single-stock-health-check`
2. `financial-statement-analyzer`
3. `market-overview-dashboard`
4. `industry-board-analyzer`
5. `portfolio-health-check`

### 第二批：清空 4 个 Draft 方法论

6. `macro-liquidity-monitor`
7. `event-study`
8. `us-peer-comparison-analyzer`
9. `us-tax-aware-rebalancing-planner`

### 第三批：建立 5 套模板家族

10. 一页诊断 / 体检
11. 市场概览 / 仪表板
12. 事件 / 公告 / 监控
13. 组合 / 调仓 / 配置
14. 研究 / 备忘录 / 周报

### 第四批：回补其余主入口

15. `peer-comparison-analyzer`
16. `weekly-market-brief-generator`
17. `us-financial-statement-analyzer`
18. `us-portfolio-health-check`
19. `hk-market-overview`
20. `hk-financial-statement`

### 第五批：再进入参数/API/状态整治

21. 参数规则下沉
22. API 真值核对
23. 状态地图重标
24. 筛选类与 AkShare 风险类治理

---

## 11. 里程碑与验收口径

### 里程碑 M1：主入口结果层成型

完成标志：

- A股前 5 个主入口 Skill 完成方法论与输出模板补齐
- 可以稳定产出完整结构化结果

### 里程碑 M2：Draft 方法论清零

完成标志：

- 当前 4 份 Draft 方法论中的核心 `[TODO]` 清零
- 每份方法论文档都具备独立判断能力

### 里程碑 M3：模板家族成型

完成标志：

- 5 套模板家族标准结构完成
- 53 份 TODO 模板可按家族批量替换

### 里程碑 M4：主入口 Skill 体系闭环

完成标志：

- 主入口 Skill 的 `SKILL.md`、`methodology.md`、`output-template.md` 三层一致
- 后续参数/API 整治有统一结果层作为承接

---

## 12. 风险与控制措施

### 风险 1：逐个补模板，导致风格继续发散

**控制措施**：先做模板家族，再批量回填。

### 风险 2：先修接口，结果层仍然空心

**控制措施**：严格按本轮优先级执行，先补方法论与模板，再处理接口问题。

### 风险 3：高频主入口与长尾 Skill 混在一起做，投入被摊薄

**控制措施**：先锁定主入口 Skill，不在 P0 阶段处理长尾专项 Skill。

### 风险 4：方法论补齐后，模板仍无法承接复杂结论

**控制措施**：方法论补齐与模板补齐配套推进，不单做一侧。

---

## 13. 最终建议

当前最应该优先修的，不是“哪个接口先修”，而是：

> 先把最常被看到的 Skill，补成真正能交付的 Skill。

因此本轮建议执行顺序明确为：

1. 先补主入口 Skill 的方法论与输出
2. 再清空 Draft 方法论
3. 再清空 TODO 模板
4. 之后再做参数/API/状态层整治

这个顺序更符合当前业务目标：

- 先提升整体观感
- 先提升实际交付质量
- 先补“结果层”和“判断层”
- 再回头修“查询层”和“状态层”

---

## 14. 本文引用的关键文件

- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/analysis-market/SKILLS_MAP.md`
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/analysis-market/SKILL.md`
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/analysis-market/analysis-best-practices.md`
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/China-market_financial-statement-analyzer/SKILL.md`
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/China-market_single-stock-health-check/SKILL.md`
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/China-market_portfolio-health-check/SKILL.md`
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/China-market_market-overview-dashboard/references/output-template.md`
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/China-market_industry-board-analyzer/references/output-template.md`
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/China-market_macro-liquidity-monitor/references/methodology.md`
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/China-market_event-study/references/methodology.md`
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/US-market_us-peer-comparison-analyzer/references/methodology.md`
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/US-market_us-tax-aware-rebalancing-planner/references/methodology.md`
