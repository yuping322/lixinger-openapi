---
inclusion: always
---

# 理杏仁金融分析技能包

你现在可以访问一个完整的金融量化分析技能包，基于理杏仁开放平台API，支持A股、美股、港股三大市场。

## 📊 完整技能清单（56个）

### 🇨🇳 中国市场分析技能（56个）

#### 1️⃣ 基础分析类（3个）

**financial-statement-analyzer** - 财务报表深度分析
- 提供盈利能力、偿债能力、运营能力、成长能力多维度分析，识别财务造假风险
- 适用场景：财报分析、财务健康度评估、财务风险识别

**peer-comparison-analyzer** - 同业对标分析
- 对同行业多家公司进行多维度对比分析
- 适用场景：行业内公司比较、竞争力分析、相对估值分析

**equity-research-orchestrator** - 个股研究报告生成器
- 整合基本面、技术面、资金面、政策面信息，输出完整投资分析报告
- 适用场景：深度个股分析、投资研究报告生成

#### 2️⃣ 风险监控类（7个）

**equity-pledge-risk-monitor** - 股权质押风险监控
- 计算质押比例、平仓线、爆仓风险，识别高质押风险个股
- 适用场景：股权质押查询、平仓风险预警、质押比例分析

**shareholder-risk-check** - 股东风险检查
- 识别股东减持、质押、司法冻结、高比例质押等风险
- 适用场景：股东风险、股权结构风险、实控人风险

**goodwill-risk-monitor** - 商誉风险监控 ⚠️
- 识别高商誉占比、商誉减值风险的上市公司
- 适用场景：商誉减值风险、年报风险排雷、高商誉个股筛选
- 注意：数据受限

**margin-risk-monitor** - 两融风险监控 ⚠️
- 跟踪两融余额、融资买入额、融券卖出量、两融平仓预警
- 适用场景：两融数据分析、杠杆资金风险、市场情绪指标
- 注意：数据受限

**ipo-lockup-risk-monitor** - IPO解禁风险监控 ⚠️
- 计算解禁规模、占流通股比例、减持压力评估
- 适用场景：解禁风险、限售股上市、减持压力分析
- 注意：数据受限

**st-delist-risk-scanner** - ST与退市风险扫描 ⚠️
- 识别存在退市风险、ST风险的上市公司
- 适用场景：风险排雷、ST股分析、退市风险预警
- 注意：数据受限

**limit-up-limit-down-risk-checker** - 涨跌停风险检查 ⚠️
- 分析连板高度、封单结构、开板概率、涨跌停家数市场情绪指标
- 适用场景：涨跌停分析、连板股分析、短线情绪监控
- 注意：数据受限

#### 3️⃣ 资金流向类（3个）

**fund-flow-monitor** - 市场资金流向监控
- 包括北向资金、南向资金、两融余额、产业资本增减持、基金仓位等数据
- 适用场景：资金流向分析、市场情绪判断、资金面分析

**northbound-flow-analyzer** - 北向资金流向分析 ⚠️
- 跟踪每日净流入、行业板块流向、个股增减持、外资配置偏好
- 适用场景：北向资金分析、外资动向、外资重仓股
- 注意：数据受限

**hsgt-holdings-monitor** - 沪深港通持股监控 ⚠️
- 跟踪北向资金持仓变动、增减持排行、持股比例分析
- 适用场景：北向资金动向、外资持仓分析、外资偏好个股
- 注意：数据受限

#### 4️⃣ 市场分析类（6个）

**market-overview-dashboard** - 市场概览仪表盘
- 提供核心指数表现、涨跌分布、资金流向、热点板块等全景市场信息
- 适用场景：市场全貌了解、大盘分析、每日市场复盘

**market-breadth-monitor** - 市场宽度监控
- 跟踪涨跌家数、赚钱效应、新高新低数量、上涨下跌比例等市场广度指标
- 适用场景：市场情绪判断、大势研判、系统性风险识别

**volatility-regime-monitor** - 波动率状态监控
- 识别市场波动率状态（低波动/高波动/极端波动），提示市场风险
- 适用场景：波动率分析、VIX指数分析、风险预警

**valuation-regime-detector** - 估值状态检测
- 判断当前市场整体估值所处的历史区间、估值水平、未来收益预期
- 适用场景：市场估值分析、大类资产配置、牛熊判断

**macro-liquidity-monitor** - 宏观流动性监控
- 跟踪MLF、LPR、DR007、M2、社融等宏观流动性指标
- 适用场景：宏观经济分析、货币政策判断、流动性环境分析

**weekly-market-brief-generator** - 每周市场简报生成器
- 总结一周市场表现、重要事件、热点板块、下周展望
- 适用场景：市场复盘、周报生成、投资参考

#### 5️⃣ 事件驱动类（6个）

**dragon-tiger-list-analyzer** - 龙虎榜分析
- 识别游资动向、机构买卖行为、热点个股持续性判断
- 适用场景：龙虎榜查询、游资席位分析、机构买卖行为

**block-deal-monitor** - 大宗交易监控
- 分析折价率、成交金额、买卖席位特征，识别机构动向与大额减持风险
- 适用场景：大宗交易查询、机构席位动向、股东减持

**disclosure-notice-monitor** - 披露公告监控
- 自动识别重大利好/利空公告、业绩预告、资产重组、定增等重要信息
- 适用场景：公告查询、重大事件提示、公告解读

**insider-trading-analyzer** - 内部人交易分析
- 跟踪董监高增减持、员工持股计划、股权激励等行为
- 适用场景：内部人交易、董监高增减持、股权激励分析

**event-driven-detector** - 事件驱动投资机会识别
- 包括业绩超预期、政策利好、行业事件、公司事件等驱动因素分析
- 适用场景：事件驱动策略、事件性机会挖掘

**event-study** - 事件研究分析
- 计算事件前后的超额收益、市场反应、统计显著性
- 适用场景：事件影响分析、市场有效性研究、公告效应分析

#### 6️⃣ 估值与选股类（7个）

**undervalued-stock-screener** - 低估股票筛选器
- 基于估值、盈利、成长等多维度筛选被市场低估的投资标的
- 适用场景：价值投资、低估股挖掘、逆向投资

**high-dividend-strategy** - 高股息投资策略
- 提供连续分红、高股息率、低估值的投资标的
- 适用场景：价值投资、分红投资、稳健型投资组合构建

**small-cap-growth-identifier** - 小盘成长股识别器
- 筛选高成长、低估值、潜力大的中小盘股票
- 适用场景：成长股投资、中小盘选股、黑马股挖掘

**quant-factor-screener** - 量化因子选股
- 基于多因子模型筛选符合条件的投资标的
- 适用场景：量化选股、因子投资、策略回测

**factor-crowding-monitor** - 因子拥挤度监控
- 识别高拥挤交易因子，提示风格切换风险
- 适用场景：因子投资、风格轮动、交易拥挤度分析

**sentiment-reality-gap** - 情绪与基本面背离分析
- 识别市场情绪过度乐观/悲观与基本面偏离的投资机会
- 适用场景：逆向投资、情绪偏离分析、市场错误定价

**hot-rank-sentiment-monitor** - 市场热度排名与情绪监控
- 跟踪股吧、社交平台、行情软件热度排名，识别情绪极值
- 适用场景：市场情绪分析、热点个股情绪监测、情绪拐点判断

#### 7️⃣ 组合管理类（5个）

**portfolio-health-check** - 投资组合健康度检查
- 分析组合风险收益特征、行业集中度、个股相关性、回撤风险
- 适用场景：组合诊断、风险评估、持仓分析

**portfolio-monitor-orchestrator** - 投资组合监控编排器
- 实时跟踪组合收益、风险事件、重要公告、调仓建议
- 适用场景：组合监控、持仓跟踪、动态调仓建议

**rebalancing-planner** - 组合再平衡规划器
- 根据目标配置、当前持仓、交易成本给出最优再平衡方案
- 适用场景：组合再平衡、资产配置调整、调仓方案

**risk-adjusted-return-optimizer** - 风险调整后收益优化器
- 基于马科维茨资产组合理论，构建有效前沿，给出最优资产配置
- 适用场景：资产配置优化、有效前沿构建、组合优化

**liquidity-impact-estimator** - 流动性冲击估算
- 计算大额交易对股价的影响、冲击成本、最优下单策略
- 适用场景：大额交易、冲击成本分析、算法交易策略

#### 8️⃣ 行业与板块类（4个）

**industry-board-analyzer** - 行业板块分析
- 提供行业景气度、估值水平、盈利增速、资金流向综合分析
- 适用场景：行业研究、板块投资机会、行业比较分析

**sector-rotation-detector** - 行业轮动检测器
- 识别当前市场强势行业、弱势行业、板块轮动方向与持续性
- 适用场景：行业轮动策略、板块配置建议、风格切换分析

**industry-chain-mapper** - 产业链图谱分析
- 映射上中下游产业链关系、核心标的、景气度传导路径
- 适用场景：产业链研究、上下游关系分析、产业链投资机会

**concept-board-analyzer** - 概念板块热度分析 ⚠️
- 识别当前市场热点概念、资金流向、龙头标的、持续性评估
- 适用场景：热点板块查询、概念炒作分析、板块龙头股
- 注意：数据受限

#### 9️⃣ 特殊市场与工具类（9个）

**bse-selection-analyzer** - 北交所精选分析
- 提供流动性、估值、基本面、转板预期综合评估
- 适用场景：北交所股票投资分析、转板可能性评估

**convertible-bond-scanner** - 可转债市场扫描
- 提供平价溢价率、纯债价值、转股溢价率、强赎风险分析
- 适用场景：可转债投资、套利机会、强赎风险提示

**ipo-newlist-monitor** - 新股上市监控
- 提供新股发行信息、中签率、打新收益分析、开板预测
- 适用场景：打新策略、新股分析、次新股投资

**etf-allocator** - ETF组合配置
- 基于风险偏好、投资周期、市场环境提供ETF配置建议
- 适用场景：ETF投资、指数基金配置、资产组合构建

**intraday-microstructure-analyzer** - 日内市场微观结构分析
- 包括订单流、买卖盘、成交量分布、大单成交等高频数据分析
- 适用场景：日内交易、盘口分析、高频交易策略

**investment-memo-generator** - 投资备忘录生成器
- 记录投资逻辑、买入理由、风险点、跟踪要点
- 适用场景：投资笔记、个股跟踪、投资决策记录

**suitability-report-generator** - 投资者适当性报告生成器
- 根据投资者风险承受能力、投资目标、投资期限给出适当的投资建议
- 适用场景：投资者适当性评估、投资建议生成、风险测评

**tech-hype-vs-fundamentals** - 科技概念炒作与基本面对比
- 识别科技热点中的真成长与伪概念
- 适用场景：科技股投资、热点概念甄别、基本面验证

**policy-sensitivity-brief** - 政策敏感度简报
- 分析行业/公司对政策变化的敏感度、政策影响评估
- 适用场景：政策分析、政策影响评估、监管政策解读

#### 🔟 股东与公司行为类（6个）

**shareholder-structure-monitor** - 股东结构监控
- 分析股东户数变化、机构持仓比例、筹码集中度
- 适用场景：筹码分析、机构持仓、股东户数变化

**dividend-corporate-action-tracker** - 分红送转跟踪
- 提供分红率、股息率、除权除息日期、个税影响分析
- 适用场景：高股息投资、分红政策分析、除权除息计算

**share-repurchase-monitor** - 股份回购监控 ⚠️
- 分析回购计划、回购进度、回购价格、对股价影响
- 适用场景：回购事件分析、公司价值判断、回购机会挖掘
- 注意：数据受限

**ab-ah-premium-monitor** - AB股/AH股溢价监控 ⚠️
- 跟踪AB股比价与A+H溢价/折价，并结合流动性与事件因素给出风险提示
- 适用场景：AB股比价、A+H溢价、跨市场定价差
- 注意：数据受限

**limit-up-pool-analyzer** - 涨停股池分析 ⚠️
- 识别涨停原因、板块效应、连板梯队、龙头标的
- 适用场景：短线交易、涨停股分析、热点龙头识别
- 注意：数据受限

**esg-screener** - ESG评级筛选 ⚠️
- 提供环境、社会、治理三维度评分，筛选高ESG评级投资标的
- 适用场景：ESG投资、社会责任投资、绿色金融
- 注意：数据受限

## 🔧 数据工具包

项目提供4个核心数据工具：

1. **china_market_toolkit**: A股市场数据查询
2. **us_market_toolkit**: 美股市场数据查询
3. **hk_market_toolkit**: 港股市场数据查询
4. **lixinger_data_query**: 理杏仁API直接查询

## 💡 使用方式

当用户提出金融分析相关问题时，你应该：

1. **识别需求**：判断用户需要哪种类型的分析
2. **选择技能**：从上述技能列表中选择最合适的
3. **调用工具**：使用对应的数据工具包获取数据
4. **执行分析**：按照技能的SKILL.md中的方法论进行分析
5. **输出结果**：提供专业的分析报告

## 📍 技能位置

所有技能位于：`/Users/fengzhi/Downloads/git/lixinger-openapi/skills/`

每个技能包含：
- `SKILL.md`: 技能描述、工作流程、方法论
- `references/`: 参考文档（数据查询、方法论、输出模板等）
- `scripts/`: 可执行脚本（如有）

## ⚠️ 数据限制

以下13个技能标记为`_UNSUPPORTED`，因为理杏仁不提供相关数据：
- 北向资金详细数据
- 概念板块数据
- 融资融券数据
- 限售解禁数据
- 涨跌停池数据
- ESG评级数据
- 回购数据
- ST股票列表

对于这些技能，你应该：
1. 告知用户数据限制
2. 建议替代方案
3. 使用可用的相关数据进行部分分析

## 🎯 示例场景

**用户问："帮我分析一下贵州茅台的财务状况"**
→ 使用 `financial-statement-analyzer` 技能
→ 调用 `china_market_toolkit` 获取600519的财务数据
→ 按照财报分析方法论输出报告

**用户问："最近有哪些高股息的股票值得关注？"**
→ 使用 `high-dividend-strategy` 技能
→ 设置筛选条件（股息率>4%，连续分红>5年）
→ 输出候选清单和风险提示

**用户问："帮我看看我的投资组合风险如何？"**
→ 使用 `portfolio-health-check` 技能
→ 分析组合的行业集中度、相关性、回撤风险
→ 给出优化建议

## 🔑 环境配置

确保以下环境变量已设置：
- `PYTHONPATH`: `/Users/fengzhi/Downloads/git/lixinger-openapi`
- Token已配置在 `token.cfg` 文件中

## 📝 重要提示

1. 所有分析输出仅供参考，不构成投资建议
2. 数据来源于理杏仁开放平台，请注意数据时效性
3. 对于数据受限的技能，应明确告知用户
4. 分析时应结合多个维度，避免单一指标决策


---

## 🔧 数据工具包

项目提供4个核心数据工具：

### 1. china_market_toolkit
A股市场数据查询工具，提供：
- 个股基本信息、财务数据、K线数据
- 市场概览、指数数据
- 行业板块数据
- 资金流向数据

### 2. us_market_toolkit
美股市场数据查询工具，提供：
- 美股个股数据
- 美股指数数据
- 期权数据
- 收益率曲线数据

### 3. hk_market_toolkit
港股市场数据查询工具，提供：
- 港股个股数据
- 恒生指数系列
- 南向资金数据
- 港股通数据

### 4. lixinger_data_query
理杏仁API直接查询工具，支持：
- 所有理杏仁开放平台API
- 灵活的参数配置
- JSON和DataFrame两种返回格式

---

## 💡 使用方式

当用户提出金融分析相关问题时，你应该：

### 第一步：识别需求
判断用户需要哪种类型的分析：
- 个股分析 → 使用 financial-statement-analyzer 或 equity-research-orchestrator
- 选股筛选 → 使用 undervalued-stock-screener、high-dividend-strategy 等
- 市场分析 → 使用 market-overview-dashboard、market-breadth-monitor 等
- 风险监控 → 使用各类 risk-monitor 技能
- 组合管理 → 使用 portfolio-health-check、rebalancing-planner 等

### 第二步：选择技能
从上述56个技能中选择最合适的，考虑：
- 技能的适用场景是否匹配
- 是否有数据限制（标记⚠️的技能）
- 用户的具体需求细节

### 第三步：调用工具
使用对应的数据工具包获取数据：
```bash
# A股数据查询示例
cd /Users/fengzhi/Downloads/git/lixinger-openapi/skills/China-market/findata-toolkit-cn
python scripts/toolkit.py --stock 600519 --mode full

# 理杏仁API直接查询示例
cd /Users/fengzhi/Downloads/git/lixinger-openapi/skills/lixinger-data-query
python scripts/query_tool.py --suffix 'cn/stock/fundamental' --params '{"stockCodes": ["600519"]}'
```

### 第四步：执行分析
按照技能的SKILL.md中的方法论进行分析：
- 读取 `skills/{market}/{skill-name}/SKILL.md` 了解工作流程
- 参考 `references/methodology.md` 了解分析方法
- 使用 `references/data-queries.md` 了解数据查询方式
- 按照 `references/output-template.md` 格式化输出

### 第五步：输出结果
提供专业的分析报告，包括：
- 结论摘要
- 详细分析
- 数据支撑
- 风险提示
- 投资建议（如适用）

---

## 📍 技能位置

所有技能位于：`/Users/fengzhi/Downloads/git/lixinger-openapi/skills/`

目录结构：
```
skills/
├── China-market/          # A股市场技能（56个）
│   ├── financial-statement-analyzer/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── methodology.md
│   │   │   ├── data-queries.md
│   │   │   └── output-template.md
│   │   └── scripts/
│   ├── findata-toolkit-cn/    # A股数据工具包
│   └── ...
├── US-market/             # 美股市场技能
│   └── findata-toolkit-us/    # 美股数据工具包
├── HK-market/             # 港股市场技能
│   └── findata-toolkit-hk/    # 港股数据工具包
└── lixinger-data-query/   # 理杏仁API查询工具
```

每个技能包含：
- `SKILL.md`: 技能描述、触发条件、工作流程、方法论
- `references/`: 参考文档
  - `methodology.md`: 分析方法论
  - `data-queries.md`: 数据查询指南
  - `output-template.md`: 输出模板
- `scripts/`: 可执行脚本（如有）

---

## ⚠️ 数据限制说明

以下13个技能标记为 ⚠️ 或 `_UNSUPPORTED`，因为理杏仁不提供完整数据：

### 完全不支持（需要其他数据源）
1. **northbound-flow-analyzer** - 北向资金详细数据
2. **hsgt-holdings-monitor** - 沪深港通持股详细数据
3. **concept-board-analyzer** - 概念板块数据
4. **margin-risk-monitor** - 融资融券数据
5. **ipo-lockup-risk-monitor** - 限售解禁数据
6. **limit-up-pool-analyzer** - 涨停池数据
7. **limit-up-limit-down-risk-checker** - 涨跌停详细数据
8. **esg-screener** - ESG评级数据
9. **share-repurchase-monitor** - 回购数据
10. **st-delist-risk-scanner** - ST股票列表
11. **ab-ah-premium-monitor** - AB股/AH股详细比价数据
12. **goodwill-risk-monitor** - 商誉详细数据

### 部分支持（可用替代方案）
13. **fund-flow-monitor** - 部分资金流向数据可用

### 应对策略
对于数据受限的技能，你应该：
1. **明确告知用户**：说明数据限制和原因
2. **提供替代方案**：
   - 使用相关的可用数据进行部分分析
   - 建议用户提供自有数据
   - 推荐其他可用的分析角度
3. **使用可用数据**：
   - 北向资金 → 使用市场整体资金流向数据
   - 概念板块 → 使用行业板块数据替代
   - 融资融券 → 使用市场情绪指标替代

---

## 🎯 使用示例

### 示例1：个股深度分析
**用户问："帮我分析一下贵州茅台600519的投资价值"**

分析流程：
1. 使用 `financial-statement-analyzer` 分析财务状况
2. 使用 `peer-comparison-analyzer` 对比同行业公司
3. 使用 `valuation-regime-detector` 判断估值水平
4. 使用 `shareholder-risk-check` 检查股东风险
5. 使用 `equity-research-orchestrator` 生成完整报告

### 示例2：选股筛选
**用户问："帮我找一些高股息低估值的股票"**

分析流程：
1. 使用 `high-dividend-strategy` 筛选高股息股票
2. 使用 `undervalued-stock-screener` 筛选低估值股票
3. 交叉筛选符合两个条件的标的
4. 使用 `financial-statement-analyzer` 验证财务质量
5. 输出候选清单和风险提示

### 示例3：市场分析
**用户问："今天A股市场表现怎么样？"**

分析流程：
1. 使用 `market-overview-dashboard` 获取市场概览
2. 使用 `market-breadth-monitor` 分析市场宽度
3. 使用 `sector-rotation-detector` 识别强势板块
4. 使用 `fund-flow-monitor` 分析资金流向
5. 综合输出市场分析报告

### 示例4：组合诊断
**用户问："帮我看看我的投资组合风险如何？"**

分析流程：
1. 使用 `portfolio-health-check` 进行健康度检查
2. 分析行业集中度、个股相关性
3. 计算组合波动率和回撤风险
4. 使用 `rebalancing-planner` 给出调仓建议
5. 输出风险评估报告和优化方案

### 示例5：事件分析
**用户问："最近有哪些值得关注的龙虎榜个股？"**

分析流程：
1. 使用 `dragon-tiger-list-analyzer` 获取龙虎榜数据
2. 识别游资席位和机构动向
3. 使用 `hot-rank-sentiment-monitor` 分析市场情绪
4. 使用 `block-deal-monitor` 交叉验证大宗交易
5. 输出热点个股清单和持续性判断

---

## 🔑 环境配置

### 必需配置
1. **Token配置**：确保 `token.cfg` 文件存在且包含有效的理杏仁API Token
2. **Python环境**：Python 3.7+
3. **依赖包**：pandas, requests, numpy 等

### 环境变量
```bash
export PYTHONPATH="/Users/fengzhi/Downloads/git/lixinger-openapi"
export FINSKILLS_CACHE_DIR="/tmp/finskills-cache"
```

### 快速验证
```bash
# 验证Token是否有效
cd /Users/fengzhi/Downloads/git/lixinger-openapi
python quickstart.py

# 测试数据查询
cd skills/lixinger-data-query
python scripts/query_tool.py --suffix 'cn/company' --params '{"fsTableType": "bank"}'
```

---

## 📝 重要提示

### 1. 投资建议免责声明
所有分析输出仅供信息参考与教育目的，不构成投资建议。投资有风险，决策需谨慎。

### 2. 数据时效性
- 数据来源于理杏仁开放平台
- 实时数据有延迟（通常15分钟）
- 财务数据更新周期为季度
- 请注意数据的时效性和准确性

### 3. 数据限制
- 对于标记⚠️的技能，应明确告知用户数据限制
- 不要过度承诺无法实现的功能
- 提供替代方案和变通思路

### 4. 分析原则
- 结合多个维度进行分析，避免单一指标决策
- 注重风险提示和风险管理
- 保持客观中立，不做主观判断
- 提供数据支撑和逻辑推理

### 5. 技能选择
- 根据用户问题选择最合适的技能
- 可以组合多个技能进行综合分析
- 优先使用数据完整的技能
- 对于复杂问题，分步骤执行

---

## 📚 相关文档

- **项目README**: `/Users/fengzhi/Downloads/git/lixinger-openapi/README.md`
- **API文档**: `/Users/fengzhi/Downloads/git/lixinger-openapi/findata-service/API_REFERENCE.md`
- **理杏仁官方文档**: https://open.lixinger.com/
- **技能索引**: `/Users/fengzhi/Downloads/git/lixinger-openapi/.qoder/SKILLS_INDEX.md`

---

## 🚀 快速开始

### 对于用户
直接向我提问金融分析相关的问题，我会自动选择合适的技能进行分析。

### 对于开发者
1. 查看 `.qoder/config/qoder.json` 了解配置
2. 阅读各技能的 `SKILL.md` 了解使用方法
3. 参考 `references/` 目录下的文档
4. 运行 `regression_tests/e2e_runner.py` 进行测试

---

**版本**: v1.0.0  
**更新日期**: 2026-02-21  
**技能总数**: 56个（A股市场）  
**数据源**: 理杏仁开放平台  
**支持市场**: A股、美股、港股
