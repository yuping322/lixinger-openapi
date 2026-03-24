# Competitive Positioning Engine (CPE) — Manual-First MVP

description: 竞争格局引擎：定义比较空间、重构 peer clusters、沉淀 market map / claims / verdict 的结构化输出。当前为 manual-first MVP，以动力电池（宁德时代）为第一个真实样例，优先把对象模型与证据链结构跑通，后续再按 Phase 2 补齐自动化推断规则。触发词：竞争格局、护城河、peer 比较、市场地位、竞争优势、CPE。

## 目标与范围（Phase 2 预备）

- 先把输出契约与 case 目录结构跑通（manual-first）
- 允许研究员手工校正 peer list 与 claims 证据
- 不追求一步自动评分，先保证"证据链结构正确、主张可追溯"
- 第一个真实行业样例：动力电池（宁德时代 300750）

## 输出契约（对齐 references/cpe-output-contract.json）

四个文件构成一个完整 `competitive_positioning/` 目录：

### market_map.json
- 市场定义（scope、地理范围、价值链位置）
- 细分市场（id、规模、CAGR、集中度、关键玩家）
- 整体集中度（CR3/CR5/HHI）

### peer_clusters.json
- 按竞争层次分组的 peer 列表（中国一线 / 全球一线 / 细分专项）
- 每个 peer 的纳入理由、关键相似点、关键差异点
- 排除列表（含排除理由）

### claims.json
- 竞争主张列表，维度覆盖：scale / technology / cost / customer / brand / supply_chain / regulation / capital
- 每条主张：direction（advantage/disadvantage/neutral）、severity、supporting_evidence、counter_evidence、confidence、status
- status 取值：confirmed / tentative / disputed / stale

### verdict.json
- position（leader / challenger / niche / follower）
- moat_assessment（moat_type、moat_strength、moat_trend、rationale）
- premium_discount_view（direction、key_drivers、key_risks）
- confidence、key_uncertainties、summary

## 真实样例：宁德时代（300750）动力电池

路径：`examples/catl_300750/`

核心结论（截至 2025-12-31）：
- position: leader，moat_strength: wide，moat_trend: **narrowing**
- 三重护城河：规模（全球 37% 份额）+ 技术（专利 19000+）+ 客户（覆盖全球前 20 大整车厂中 16 家）
- 三重压力：比亚迪国内追赶 + 欧美贸易壁垒 + 储能价格战
- 核心不确定性：固态电池技术路线切换窗口（2028-2032）

claims 覆盖 8 条主张（5 个 advantage、3 个 disadvantage），confidence 范围 0.62-0.88。

## 使用方式

### 手工创建新 case

1. 在 `research_cases/case_YYYYMMDD_company/competitive_positioning/` 下创建四个文件
2. 参考 `examples/catl_300750/` 的结构和字段
3. 用 `deep-research-qa` 做 QA（后续版本将加入 CPE QA 检查项）

### 与 FQE 集成

CPE 的 `verdict.json` 中的 `premium_discount_view` 应与 FQE 的 `verdict.json` 中的 `grade` 和 `scores` 联合解读：
- FQE grade A/B + CPE position leader → 支持估值溢价
- FQE grade C/D + CPE moat_trend narrowing → 估值折价信号

## 下一步（Phase 2 自动化方向）

- 从理杏仁 API 拉取 peer 财务数据，自动生成定量 claims（毛利率对比、ROE 对比等）
- 基于 market_map 的集中度数据自动触发竞争格局红旗
- QA 脚本加入 CPE 检查项（claims 是否有 supporting_evidence、verdict 字段完整性）
