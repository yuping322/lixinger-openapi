---
name: stock-screener-strategy-design-doc
overview: 围绕现有 6 个选股策略做一次完整调研与设计文档产出，明确哪些方向应并入现有策略、哪些暂不新建、以及后续文档与策略文件的更新范围。
todos:
  - id: audit-mapping
    content: 用 [subagent:code-explorer] 核对6策略与新增方向映射
    status: completed
  - id: freeze-guidelines
    content: 更新 README 与设计清单，固化主线和优先级
    status: completed
    dependencies:
      - audit-mapping
  - id: refactor-high-dividend
    content: 用 [skill:skill-creator] 改 high-dividend 文档族，吸收股东回报与现金牛
    status: completed
    dependencies:
      - freeze-guidelines
  - id: refactor-undervalued-quant
    content: 用 [skill:skill-creator] 改 undervalued 与 quant 文档族
    status: completed
    dependencies:
      - freeze-guidelines
  - id: refactor-esg
    content: 用 [skill:skill-creator] 改 esg 文档族，补治理与监管验证
    status: completed
    dependencies:
      - freeze-guidelines
  - id: evaluate-new-strategy
    content: 评估是否新增 business-cycle-turnaround，仅无法吸收时再建
    status: completed
    dependencies:
      - refactor-high-dividend
      - refactor-undervalued-quant
      - refactor-esg
  - id: consistency-review
    content: 复核全部文档一致性、边界与输出模板
    status: completed
    dependencies:
      - evaluate-new-strategy
---

## User Requirements

- 基于已经完成的调研结论，产出一份“调研清楚、可直接执行”的设计与改造方案。
- 重点回答：应优先改造现有 6 个策略，还是继续新建策略；哪些方向值得继续研究，哪些不值得独立实现。
- 方案需要落到 `.claude/plugins/stock-screener` 现有文档体系中，尤其要衔接已存在的 `README.md`、`STRATEGY_DESIGN_CHECKLIST.md`、`commands/` 与 `skills/` 文档。

## Product Overview

- 当前插件应继续以“策略研究框架”而不是“单次选股结果”来组织内容。
- 文档需要明确两条主线：`低估值 + 盈利增长 + 质量约束`，以及 `高股息/低估白马 + 现金流 + 分红可持续`。
- 最终呈现应为结构化章节、映射表和优先级清单，方便后续持续补充新方向时直接复用。

## Core Features

- 明确现有 6 个策略与新增方向的承接关系，优先吸收进已有母策略。
- 给出“值得继续研究 / 低优先级 / 暂不独立实现”的判断标准和结论。
- 固化“底仓型策略”和“进攻型卫星策略”的分类方法。
- 说明若确实需要新增策略，最多先新增哪 1 个，以及触发新增的条件。
- 给出需要更新的具体文件、更新顺序和保持文档一致性的要求。

## Tech Stack Selection

- 当前项目是基于 Markdown 的 Claude 插件文档体系，已验证的结构为：
- 插件总览：`.claude/plugins/stock-screener/README.md`
- 命令入口：`.claude/plugins/stock-screener/commands/*.md`
- 策略技能：`.claude/plugins/stock-screener/skills/{strategy}/SKILL.md`
- 设计决策：`.claude/plugins/stock-screener/skills/{strategy}/DECISIONS.md`
- 参考文档：`.claude/plugins/stock-screener/skills/{strategy}/references/*.md`
- 已验证的统一工作流是：先复用 `.claude/skills/lixinger-screener` 建候选池，再对入围股做少量补查；现有 `undervalued-stock-screener`、`high-dividend-strategy`、`quant-factor-screener`、`esg-screener` 均遵循该模式。
- 本次方案不引入新框架、不改目录模式，优先复用现有 6 个策略的命令、技能、决策与模板体系。

## Implementation Approach

### 方法与总体策略

采用“先固化总纲，再收敛到现有母策略”的方案：

1. 先用 `README.md` 与 `STRATEGY_DESIGN_CHECKLIST.md` 固化两条主线、优先级和新增门槛。
2. 再改造现有母策略文档族，让新增方向被已有能力吸收，而不是立即裂变成大量新策略。
3. 仅当进攻型周期逻辑无法被现有结构清晰承接时，才新增 `business-cycle-turnaround`。

### 高层工作方式

- `high-dividend-strategy`：承接 `shareholder-yield-enhancer`、`cash-cow-compounder`，并吸收 `soe-rerating` 中“分红提升 / 市值管理 / 股东回报增强”的部分。
- `undervalued-stock-screener`：承接 `leader-oversold-recovery`，强化“低估值 + 增长/质量修复”的主线表达。
- `quant-factor-screener`：作为解释层，补强 `价值 + 质量 + 成长` 共振、风格冲突、待启动样本的说明能力。
- `esg-screener`：作为验证层，补强股东结构、治理改善、监管风险、资本配置等代理验证。
- `small-cap-growth-identifier` 与 `bse-selection-analyzer`：第一阶段保持不动，避免无证据扩散。
- `distress-turnaround-screener` 与 `post-regulatory-rerating`：当前不建议独立实现，只保留在清单中的低优先级结论。

### 关键技术决策与取舍

- **优先改已有 6 个策略，而不是新建多个策略**：因为现有文档结构已能承接用户当前验证出的两条主线，重复建新策略只会造成命名膨胀和维护分裂。
- **只保留 1 个条件性新增候选**：`business-cycle-turnaround` 可作为唯一待评估新增项，避免把 `景气反转 / 供需改善 / 订单驱动 / 资本开支周期` 过早拆成 4 个弱边界策略。
- **保持命令名向后兼容**：继续使用现有 `/high-dividend-strategy`、`/undervalued-stock-screener` 等入口，降低使用者认知切换成本。
- **把研究结论写成可验证边界，而非口号**：所有新增方向必须落回现有模板中的“异常发现、机会清单、跟踪信号、失效条件”。

### Performance 与 Reliability

- 继续沿用“候选池优先、入围股补查”的轻量模式，避免全市场重拉；核心复杂度保持在候选样本规模的线性处理。
- 潜在瓶颈仍是补查型数据拉取，因此只在高优先候选上补数，避免在命令与技能文档中鼓励全市场深拉。
- 不承诺仓库中未验证的字段、完整 ESG 评分或伪精确目标价，降低后续实现偏差和文档失真。

### Avoiding Technical Debt

- 复用现有命令 frontmatter、`SKILL.md` 章节、`DECISIONS.md` 结构、`references/output-template.md` 模板，不引入新文档范式。
- 不改动与当前研究主线无关的 `small-cap-growth-identifier` 和 `bse-selection-analyzer`，控制 blast radius。
- 把“是否新增策略”放到最后决策，先验证现有策略吸收能力，避免后续回收成本。

## Implementation Notes

- 命令文档继续保持当前格式：frontmatter、`Load the skill`、默认目标、默认流程、分类输出、示例。
- `SKILL.md` 继续沿用现有章节：`何时使用`、`执行步骤`、`输出要求`、`数据边界`。
- `DECISIONS.md` 需要显式写明“为什么吸收新增方向、为什么暂不新建、哪些结论只是低优先级保留”。
- `high-dividend-strategy` 的模板与方法论要补强自由现金流、回购、资本配置、现金牛特征；但命令名与主分类可尽量保持稳定。
- `undervalued-stock-screener` 要把“龙头补跌错杀”写成该策略的高质量分支，而不是独立命令。
- `quant-factor-screener` 只负责解释共振与冲突，不演变成另一个综合总分大全。
- `esg-screener` 继续坚持“治理与风险代理”边界，不扩大成仓库当前无法验证的完整 ESG 平台。

## Architecture Design

### 现有策略承接关系

- `/high-dividend-strategy`
- 承接：`shareholder-yield-enhancer`
- 承接：`cash-cow-compounder` 的底仓型部分
- 承接：`soe-rerating` 中分红增强与市值管理部分

- `/undervalued-stock-screener`
- 承接：`leader-oversold-recovery`
- 强化：`低估值 + 盈利增长 + 质量约束`

- `/quant-factor-screener`
- 支撑：解释 `价值 + 质量 + 成长` 共振
- 支撑：区分待启动、风格受益、冲突高风险

- `/esg-screener`
- 支撑：股东结构、治理改善、监管风险验证
- 支撑：`soe-rerating` 的治理与监管侧证据

- 暂不扩张
- `small-cap-growth-identifier`
- `bse-selection-analyzer`

- 条件新增
- `business-cycle-turnaround` 仅在现有四个母策略无法清晰承接时新增

## Directory Structure

### Directory Structure Summary

本次方案以文档与技能结构改造为主，优先收敛到现有 6 个策略中的 4 个母策略，先统一总纲，再同步命令、技能、设计决策、方法论与输出模板。

### 总纲与决策文件

- `.claude/plugins/stock-screener/README.md`  [MODIFY]  
插件总览与策略索引。补充“优先改已有策略、最多条件性新增 1 个策略”的总原则，并把新增方向映射到现有母策略。
- `.claude/plugins/stock-screener/STRATEGY_DESIGN_CHECKLIST.md`  [NEW]  
当前设计总控文档。固化两条主线、优先级、值得研究与低优先级方向、以及新增门槛。

### 高股东回报主线

- `.claude/plugins/stock-screener/commands/high-dividend-strategy.md`  [MODIFY]  
用户入口文档。扩展默认目标与分类说明，使其覆盖股东回报增强、现金牛复利、央国企分红重估。
- `.claude/plugins/stock-screener/skills/high-dividend-strategy/SKILL.md`  [MODIFY]  
主技能说明。明确其作为底仓型母策略的定位与适用场景。
- `.claude/plugins/stock-screener/skills/high-dividend-strategy/DECISIONS.md`  [MODIFY]  
设计决策。写清为何吸收新增方向、哪些能力继续保留在该策略中。
- `.claude/plugins/stock-screener/skills/high-dividend-strategy/references/calculation-methodology.md`  [MODIFY]  
方法论文档。补强自由现金流、回购、资本配置、现金牛与总回报框架。
- `.claude/plugins/stock-screener/skills/high-dividend-strategy/references/output-template.md`  [MODIFY]  
输出模板。补足股东回报增强与现金牛证据位、失效条件与跟踪点。

### 低估修复主线

- `.claude/plugins/stock-screener/commands/undervalued-stock-screener.md`  [MODIFY]  
用户入口文档。把“行业龙头补跌错杀”纳入现有低估值策略叙述。
- `.claude/plugins/stock-screener/skills/undervalued-stock-screener/SKILL.md`  [MODIFY]  
主技能说明。强化“低估值 + 增长/质量修复”而非纯便宜名单。
- `.claude/plugins/stock-screener/skills/undervalued-stock-screener/DECISIONS.md`  [MODIFY]  
设计决策。说明为何优先吸收错杀龙头，而不是新建独立策略。
- `.claude/plugins/stock-screener/skills/undervalued-stock-screener/references/screening-methodology.md`  [MODIFY]  
方法论文档。补强龙头韧性、盈利质量、估值分位、错杀与陷阱识别。
- `.claude/plugins/stock-screener/skills/undervalued-stock-screener/references/output-template.md`  [MODIFY]  
输出模板。加入龙头错杀的证据位与失效条件表达。

### 因子解释层

- `.claude/plugins/stock-screener/commands/quant-factor-screener.md`  [MODIFY]  
用户入口文档。明确其作为解释层而非新母策略，用于支撑共振与冲突分析。
- `.claude/plugins/stock-screener/skills/quant-factor-screener/SKILL.md`  [MODIFY]  
主技能说明。把 `价值 + 质量 + 成长` 共振与高共识主线显式对齐。
- `.claude/plugins/stock-screener/skills/quant-factor-screener/DECISIONS.md`  [MODIFY]  
设计决策。补充其与 `high-dividend-strategy`、`undervalued-stock-screener` 的协同边界。
- `.claude/plugins/stock-screener/skills/quant-factor-screener/references/factor-methodology.md`  [MODIFY]  
方法论文档。突出因子共振、待启动样本、风格受益与冲突风险。
- `.claude/plugins/stock-screener/skills/quant-factor-screener/references/output-template.md`  [MODIFY]  
输出模板。补足解释型字段，避免只剩综合排序。

### 治理验证层

- `.claude/plugins/stock-screener/commands/esg-screener.md`  [MODIFY]  
用户入口文档。明确其服务于治理改善、监管风险、股东结构验证。
- `.claude/plugins/stock-screener/skills/esg-screener/SKILL.md`  [MODIFY]  
主技能说明。补强 `soe-rerating` 与高收益治理风险验证。
- `.claude/plugins/stock-screener/skills/esg-screener/DECISIONS.md`  [MODIFY]  
设计决策。明确不扩展成全量 ESG 评分，仅强化治理代理与监管验证。
- `.claude/plugins/stock-screener/skills/esg-screener/references/esg-framework.md`  [MODIFY]  
方法论文档。补充股东结构、资本配置、监管措施、问询函等验证框架。
- `.claude/plugins/stock-screener/skills/esg-screener/references/output-template.md`  [MODIFY]  
输出模板。强化治理改善与高收益高治理风险两类输出。

### 条件性新增文件

仅在第 6 步评估确认“现有四个母策略无法清晰承接进攻型周期逻辑”时新增：

- `.claude/plugins/stock-screener/commands/business-cycle-turnaround.md`  [NEW]  
景气反转命令入口，聚合景气修复、供需改善、订单兑现、资本开支周期。
- `.claude/plugins/stock-screener/skills/business-cycle-turnaround/SKILL.md`  [NEW]  
主技能说明，限定为进攻型卫星策略。
- `.claude/plugins/stock-screener/skills/business-cycle-turnaround/DECISIONS.md`  [NEW]  
设计决策，说明为何现有策略无法吸收。
- `.claude/plugins/stock-screener/skills/business-cycle-turnaround/INSTALLATION.md`  [NEW]  
参照现有 skill 目录模板补齐安装说明。
- `.claude/plugins/stock-screener/skills/business-cycle-turnaround/LICENSE.txt`  [NEW]  
参照现有 skill 目录模板补齐许可文件。
- `.claude/plugins/stock-screener/skills/business-cycle-turnaround/VERSION`  [NEW]  
参照现有 skill 目录模板补齐版本文件。
- `.claude/plugins/stock-screener/skills/business-cycle-turnaround/references/methodology.md`  [NEW]  
方法论文档，覆盖景气、供需、订单、资本开支的最小统一框架。
- `.claude/plugins/stock-screener/skills/business-cycle-turnaround/references/data-queries.md`  [NEW]  
数据查询指南，限定候选池与补查边界。
- `.claude/plugins/stock-screener/skills/business-cycle-turnaround/references/output-template.md`  [NEW]  
输出模板，保持与现有策略同构。

## Agent Extensions

### SubAgent

- **code-explorer**
- Purpose: 核对现有 6 个策略、命令与参考文档的真实边界，确认哪些文件必须同步更新
- Expected outcome: 产出准确的文件级映射与改造范围，避免遗漏某个 `command`、`SKILL`、`DECISIONS` 或 `references` 文件

### Skill

- **skill-creator**
- Purpose: 按现有仓库的 skill 结构重写或扩展策略文档族，保持新旧策略文档格式一致
- Expected outcome: 形成结构统一、边界清楚、便于后续继续扩展的策略文档体系