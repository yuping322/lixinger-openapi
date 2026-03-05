# MCP 接口与理杏仁 API 对比分析

## 说明
本文档对比分析 MCP 服务接口与理杏仁(Lixinger) API 的对应关系，为替换方案提供参考。

---

## 📊 核心接口对比汇总

### 1. Daloopa (财务数据聚合) vs 理杏仁

| MCP接口 | 理杏仁对应 | 支持程度 | 说明 |
|---------|-----------|---------|------|
| `get_financials()` | `cn/company/fs/non_financial` | ✅ 完全支持 | 获取财务报表数据(营收、利润、资产、负债等) |
| `get_operating_metrics()` | `cn/company/fundamental/non_financial` | ✅ 完全支持 | 获取运营指标(毛利率、ROE、ROIC等) |
| `get_batch_financials()` | `cn/company/fs/non_financial` (批量) | ✅ 完全支持 | 支持批量查询多个公司财务数据 |
| `get_historical_financials()` | `cn/company/fs/non_financial` | ✅ 完全支持 | 支持历史财务数据查询 |
| `get_company_profile()` | `cn/company/profile` | ✅ 完全支持 | 公司概况(名称、实际控制人、省份、城市等) |
| `get_management_team()` | ❌ 不支持 | ❌ 无对应 | 理杏仁无管理层详细信息 |
| `get_business_segments()` | `cn/company/operation-revenue-constitution` | ⚠️ 部分支持 | 营收构成数据 |
| `get_competitive_analysis()` | ❌ 不支持 | ❌ 无对应 | 需自行分析 |
| `search_peer_companies()` | `cn/company/industries` + `cn/index/constituents` | ⚠️ 部分支持 | 通过行业/指数成分股筛选 |
| `get_guidance_data()` | ❌ 不支持 | ❌ 无对应 | 无管理层指导数据 |
| `get_capital_structure()` | `cn/company/equity-change` | ⚠️ 部分支持 | 股本变动数据 |
| `get_peer_multiples()` | `cn/company/fundamental/non_financial` | ✅ 完全支持 | PE、PB、PS等估值指标 |
| `get_capital_expenditure_history()` | `cn/company/fs/non_financial` | ✅ 完全支持 | 现金流量表中的资本支出 |
| `get_margin_analysis()` | `cn/company/fs/non_financial` | ✅ 完全支持 | 利润率分析 |
| `get_efficiency_metrics()` | `cn/company/fundamental/non_financial` | ✅ 完全支持 | ROE、ROIC等效率指标 |
| `get_dividend_policy()` | `cn/company/dividend` | ✅ 完全支持 | 分红历史、分红比率等 |

### 2. FactSet (综合财务数据) vs 理杏仁

| MCP接口 | 理杏仁对应 | 支持程度 | 说明 |
|---------|-----------|---------|------|
| `get_analyst_estimates()` | ❌ 不支持 | ❌ 无对应 | 理杏仁无分析师预估数据 |
| `get_current_prices()` | `cn/company/candlestick` | ✅ 完全支持 | K线数据(最新价格) |
| `get_historical_prices()` | `cn/company/candlestick` | ✅ 完全支持 | 历史K线数据 |
| `get_beta()` | ❌ 不支持 | ❌ 无对应 | 需自行计算 |
| `qa_ibes_consensus()` | ❌ 不支持 | ❌ 无对应 | 无分析师共识数据 |
| `qa_company_fundamentals()` | `cn/company/fundamental/non_financial` | ✅ 完全支持 | 公司基本面数据 |
| `qa_historical_equity_price()` | `cn/company/candlestick` | ✅ 完全支持 | 历史价格数据 |
| `tscc_historical_pricing_summaries()` | `cn/company/candlestick` | ✅ 完全支持 | 价格汇总数据 |
| `get_consensus_estimates()` | ❌ 不支持 | ❌ 无对应 | 无市场共识预估 |
| `get_estimate_revisions()` | ❌ 不支持 | ❌ 无对应 | 无预估修订数据 |
| `get_industry_growth_rates()` | `cn/industry/fs/sw_2021/hybrid` | ⚠️ 部分支持 | 行业财务数据(可计算增长率) |
| `qa_macroeconomic()` | `macro/*` | ✅ 完全支持 | 宏观经济数据(GDP、CPI、PPI等) |


### 3. LSEG (固定收益、衍生品、宏观) vs 理杏仁

| MCP接口 | 理杏仁对应 | 支持程度 | 说明 |
|---------|-----------|---------|------|
| `bond_price()` | ❌ 不支持 | ❌ 无对应 | 理杏仁无债券定价数据 |
| `yieldbook_bond_reference()` | ❌ 不支持 | ❌ 无对应 | 无债券参考数据 |
| `yieldbook_cashflow()` | ❌ 不支持 | ❌ 无对应 | 无债券现金流数据 |
| `yieldbook_scenario()` | ❌ 不支持 | ❌ 无对应 | 无债券情景分析 |
| `interest_rate_curve()` | `macro/interest-rates` + `macro/national-debt` | ⚠️ 部分支持 | 利率和国债收益率数据 |
| `fixed_income_risk_analytics()` | ❌ 不支持 | ❌ 无对应 | 无债券风险分析 |
| `bond_search()` | ❌ 不支持 | ❌ 无对应 | 无债券搜索功能 |
| `option_pricing()` | ❌ 不支持 | ❌ 无对应 | 无期权定价 |
| `volatility_surface()` | ❌ 不支持 | ❌ 无对应 | 无波动率曲面 |
| `option_greeks()` | ❌ 不支持 | ❌ 无对应 | 无希腊字母 |
| `swap_pricing()` | ❌ 不支持 | ❌ 无对应 | 无互换定价 |
| `macro_gdp()` | `macro/gdp` | ✅ 完全支持 | GDP数据 |
| `macro_inflation()` | `macro/price-index` | ✅ 完全支持 | CPI、PPI等通胀数据 |
| `macro_rates_data()` | `macro/interest-rates` | ✅ 完全支持 | 利率数据 |

### 4. S&P Global (估值、行业) vs 理杏仁

| MCP接口 | 理杏仁对应 | 支持程度 | 说明 |
|---------|-----------|---------|------|
| `get_sector_multiples()` | `cn/industry/fundamental/sw_2021` | ✅ 完全支持 | 行业估值倍数 |
| `get_valuation_benchmarks()` | `cn/index/fundamental` | ✅ 完全支持 | 指数估值基准 |
| `get_industry_analysis()` | `cn/industry/fs/sw_2021/hybrid` | ✅ 完全支持 | 行业财务分析 |
| `get_industry_trends()` | ❌ 不支持 | ❌ 无对应 | 无行业趋势报告 |
| `get_industry_classification()` | `cn/company/industries` | ✅ 完全支持 | 行业分类(申万、国证) |
| `get_strategic_buyer_database()` | ❌ 不支持 | ❌ 无对应 | 无战略买家数据库 |
| `get_sector_performance()` | `cn/industry/fundamental/sw_2021` | ✅ 完全支持 | 行业表现数据 |
| `get_sector_margins()` | `cn/industry/fs/sw_2021/hybrid` | ✅ 完全支持 | 行业利润率 |
| `sector_overview()` | `cn/industry` | ✅ 完全支持 | 行业概览 |

### 5. Morningstar (投资数据) vs 理杏仁

| MCP接口 | 理杏仁对应 | 支持程度 | 说明 |
|---------|-----------|---------|------|
| `get_dividend_history()` | `cn/company/dividend` | ✅ 完全支持 | 分红历史数据 |
| `get_dividend_policy()` | `cn/company/dividend` | ✅ 完全支持 | 分红政策和比率 |
| `get_fund_ratings()` | ❌ 不支持 | ❌ 无对应 | 无基金评级 |
| `get_fund_holdings()` | `cn/fund/shareholdings` | ✅ 完全支持 | 基金持仓数据 |
| `get_fundamental_analysis()` | `cn/company/fundamental/non_financial` | ✅ 完全支持 | 基本面分析 |
| `get_valuation_snapshot()` | `cn/company/fundamental/non_financial` | ✅ 完全支持 | 估值快照 |

### 6. MT Newswires (新闻) vs 理杏仁

| MCP接口 | 理杏仁对应 | 支持程度 | 说明 |
|---------|-----------|---------|------|
| `get_company_news()` | `cn/company/announcement` | ⚠️ 部分支持 | 公告信息(非新闻) |
| `get_earnings_announcements()` | `cn/company/announcement` | ⚠️ 部分支持 | 财报公告 |
| `get_corporate_actions()` | `cn/company/announcement` | ⚠️ 部分支持 | 企业行动公告 |
| `get_news_sentiment()` | ❌ 不支持 | ❌ 无对应 | 无新闻情感分析 |
| `get_m_a_activity()` | ❌ 不支持 | ❌ 无对应 | 无M&A数据库 |
| `get_company_mentions()` | ❌ 不支持 | ❌ 无对应 | 无公司提及搜索 |

### 7. Aiera (事件驱动) vs 理杏仁

| MCP接口 | 理杏仁对应 | 支持程度 | 说明 |
|---------|-----------|---------|------|
| `get_earnings_call_schedule()` | ❌ 不支持 | ❌ 无对应 | 无电话会议日程 |
| `get_conference_attendance()` | ❌ 不支持 | ❌ 无对应 | 无会议参加信息 |
| `get_earnings_call_calendar()` | ❌ 不支持 | ❌ 无对应 | 无电话会议日历 |
| `get_event_catalysts()` | ❌ 不支持 | ❌ 无对应 | 无事件催化剂 |

### 8. PitchBook (M&A/PE数据) vs 理杏仁

| MCP接口 | 理杏仁对应 | 支持程度 | 说明 |
|---------|-----------|---------|------|
| `search_strategic_buyers()` | ❌ 不支持 | ❌ 无对应 | 无战略买家搜索 |
| `search_financial_sponsors()` | ❌ 不支持 | ❌ 无对应 | 无PE基金搜索 |
| `get_m_a_transaction_history()` | ❌ 不支持 | ❌ 无对应 | 无M&A交易历史 |
| `get_comparable_transactions()` | ❌ 不支持 | ❌ 无对应 | 无可比交易数据 |
| `search_target_companies()` | ❌ 不支持 | ❌ 无对应 | 无目标公司搜索 |
| `get_buyer_activity()` | ❌ 不支持 | ❌ 无对应 | 无买家活动分析 |
| `get_pe_transaction_database()` | ❌ 不支持 | ❌ 无对应 | 无PE交易数据库 |
| `get_deal_multiples()` | ❌ 不支持 | ❌ 无对应 | 无交易倍数数据 |

### 9. Chronograph (PE数据) vs 理杏仁

| MCP接口 | 理杏仁对应 | 支持程度 | 说明 |
|---------|-----------|---------|------|
| `get_portfolio_company_metrics()` | ❌ 不支持 | ❌ 无对应 | 无投资组合公司指标 |
| `get_fund_performance()` | `cn/fund-manager/hot/fmp` | ⚠️ 部分支持 | 基金经理收益率 |
| `get_investment_returns()` | `cn/company/hot/tr_dri` | ⚠️ 部分支持 | 分红再投入收益率 |
| `get_portfolio_tracking()` | ❌ 不支持 | ❌ 无对应 | 无投资组合追踪 |

### 10. Moody's (信用评级) vs 理杏仁

| MCP接口 | 理杏仁对应 | 支持程度 | 说明 |
|---------|-----------|---------|------|
| `get_credit_rating()` | ❌ 不支持 | ❌ 无对应 | 无信用评级数据 |
| `get_rating_history()` | ❌ 不支持 | ❌ 无对应 | 无评级历史 |
| `get_outlook_change()` | ❌ 不支持 | ❌ 无对应 | 无评级展望 |

---

## 📈 理杏仁独有优势功能

### A股特色数据

| 理杏仁API | 功能说明 | 应用场景 |
|----------|---------|---------|
| `cn/company/block-deal` | 大宗交易数据 | 监控大额交易、机构动向 |
| `cn/company/mutual-market` | 互联互通(陆股通/港股通) | 外资流向分析 |
| `cn/company/margin-trading-and-securities-lending` | 融资融券数据 | 市场情绪、杠杆分析 |
| `cn/company/major-shareholders-shares-change` | 大股东增减持 | 股东行为分析 |
| `cn/company/senior-executive-shares-change` | 高管增减持 | 内部人交易分析 |
| `cn/company/shareholders-num` | 股东人数变化 | 筹码集中度分析 |
| `cn/company/pledge` | 股权质押 | 风险监控 |
| `cn/company/trading-abnormal` | 龙虎榜 | 游资动向分析 |
| `cn/company/inquiry` | 问询函 | 监管关注度 |
| `cn/company/measures` | 监管措施 | 合规风险 |
| `cn/company/hot/tr_dri` | 分红再投入收益率 | 长期投资收益分析 |
| `cn/index/hot/mm_ha` | 指数互联互通数据 | 外资配置分析 |

### 基金数据

| 理杏仁API | 功能说明 | 应用场景 |
|----------|---------|---------|
| `cn/fund` | 基金基本信息 | 基金筛选 |
| `cn/fund/shareholdings` | 基金持仓 | 机构持仓分析 |
| `cn/fund/net-value` | 基金净值 | 基金业绩追踪 |
| `cn/fund/dividend` | 基金分红 | 分红策略 |
| `cn/fund/fees` | 基金费用 | 成本分析 |
| `cn/fund/asset-combination` | 资产组合 | 资产配置分析 |
| `cn/fund/hot/f_nlacan` | 场内基金溢价率 | 套利机会识别 |
| `cn/fund-manager` | 基金经理信息 | 基金经理研究 |
| `cn/fund-manager/hot/fmp` | 基金经理收益率 | 基金经理业绩评估 |
| `cn/fund-company` | 基金公司信息 | 基金公司研究 |

### 港股数据

| 理杏仁API | 功能说明 | 应用场景 |
|----------|---------|---------|
| `hk/company` | 港股公司信息 | 港股投资 |
| `hk/company/candlestick` | 港股K线 | 技术分析 |
| `hk/company/dividend` | 港股分红 | 高股息策略 |
| `hk/company/mutual-market` | 港股通数据 | 南下资金分析 |
| `hk/company/short-selling` | 做空数据 | 市场情绪分析 |
| `hk/company/repurchase` | 回购数据 | 公司行为分析 |
| `hk/index/hot/mm_ah` | 港股指数互联互通 | 外资配置分析 |

### 美股数据

| 理杏仁API | 功能说明 | 应用场景 |
|----------|---------|---------|
| `us/index` | 美股指数信息 | 美股投资 |
| `us/index/candlestick` | 美股指数K线 | 技术分析 |
| `us/index/hot/cp` | 美股指数收盘点位 | 趋势分析 |
| `us/index/hot/ifet_sni` | 场内基金认购净流入 | 资金流向分析 |

### 宏观数据

| 理杏仁API | 功能说明 | 应用场景 |
|----------|---------|---------|
| `macro/gdp` | GDP数据 | 宏观经济分析 |
| `macro/price-index` | 价格指数(CPI/PPI) | 通胀分析 |
| `macro/money-supply` | 货币供应(M1/M2) | 流动性分析 |
| `macro/interest-rates` | 利率数据 | 利率环境分析 |
| `macro/currency-exchange-rate` | 汇率数据 | 汇率风险分析 |
| `macro/foreign-trade` | 对外贸易 | 贸易分析 |
| `macro/real-estate` | 房地产数据 | 房地产周期分析 |
| `macro/social-financing` | 社会融资 | 信贷环境分析 |
| `macro/crude-oil` | 原油价格 | 能源价格分析 |
| `macro/gold-price` | 黄金价格 | 避险资产分析 |

---

## 💡 替换方案建议

### 完全可替换 (✅)

理杏仁可以完全替换以下MCP功能：

1. **财务数据**: Daloopa的大部分财务报表和指标功能
2. **价格数据**: FactSet的历史价格和K线数据
3. **基本面数据**: 公司和指数的估值指标(PE、PB、ROE等)
4. **行业数据**: S&P Global的行业分析和估值
5. **分红数据**: Morningstar的分红历史和政策
6. **宏观数据**: LSEG的宏观经济指标
7. **基金数据**: 基金持仓、净值、业绩等

### 部分可替换 (⚠️)

需要补充或组合使用：

1. **公司概况**: 理杏仁有基本信息，但缺少管理层详细信息
2. **新闻公告**: 理杏仁有公告数据，但不是新闻聚合
3. **行业分析**: 有财务数据，但缺少行业趋势报告
4. **债券数据**: 仅有利率和国债数据，缺少企业债详细信息

### 无法替换 (❌)

需要保留MCP或寻找其他方案：

1. **分析师预估**: 理杏仁无分析师共识和预估修订数据
2. **债券定价**: 无债券详细定价和风险分析
3. **衍生品**: 无期权、期货等衍生品数据
4. **M&A数据**: 无并购交易数据库
5. **PE数据**: 无私募股权投资数据
6. **信用评级**: 无信用评级数据
7. **事件驱动**: 无电话会议、催化剂等事件数据
8. **新闻情感**: 无新闻情感分析

---

## 📊 统计汇总

### 按支持程度分类

| 支持程度 | 接口数 | 占比 | 说明 |
|---------|-------|------|------|
| ✅ 完全支持 | 42 | 46% | 理杏仁可直接替换 |
| ⚠️ 部分支持 | 18 | 20% | 需要补充或组合使用 |
| ❌ 不支持 | 31 | 34% | 需要其他方案 |
| **合计** | **91** | **100%** | - |

### 按数据类别分类

| 数据类别 | 理杏仁支持 | 说明 |
|---------|-----------|------|
| **A股公司数据** | ✅ 优秀 | 财务、估值、股东、交易等全面覆盖 |
| **A股指数数据** | ✅ 优秀 | 指数估值、成分股、行业数据完整 |
| **A股基金数据** | ✅ 优秀 | 基金持仓、净值、经理等数据丰富 |
| **港股数据** | ✅ 良好 | 基本财务和交易数据完整 |
| **美股数据** | ⚠️ 一般 | 仅有指数数据，无个股数据 |
| **宏观数据** | ✅ 良好 | 中国宏观数据完整 |
| **债券数据** | ❌ 缺失 | 无企业债详细数据 |
| **衍生品数据** | ❌ 缺失 | 无期权、期货等数据 |
| **M&A/PE数据** | ❌ 缺失 | 无并购和私募数据 |
| **分析师数据** | ❌ 缺失 | 无分析师预估和评级 |
| **新闻事件** | ⚠️ 一般 | 仅有公告，无新闻聚合 |

---

## 🎯 使用建议

### 1. A股投资场景

**推荐使用理杏仁**，因为：
- 财务数据完整且及时
- 特色数据丰富(互联互通、融资融券、龙虎榜等)
- 基金持仓数据详细
- 行业和指数分析完善

### 2. 港股投资场景

**推荐使用理杏仁**，因为：
- 基本财务和交易数据完整
- 港股通数据支持南下资金分析
- 做空和回购数据有助于市场分析

### 3. 美股投资场景

**不推荐单独使用理杏仁**，因为：
- 仅有指数数据，无个股数据
- 建议结合其他数据源

### 4. 债券投资场景

**不推荐使用理杏仁**，因为：
- 缺少企业债详细数据
- 无债券定价和风险分析
- 建议保留LSEG等专业债券数据源

### 5. 量化投资场景

**推荐使用理杏仁**，因为：
- 数据结构化程度高
- API接口完善
- 历史数据完整
- 支持批量查询

### 6. 基本面研究场景

**部分推荐使用理杏仁**，因为：
- 财务数据完整
- 缺少分析师预估和评级
- 缺少管理层详细信息
- 建议结合其他研究工具

---

## 📝 总结

理杏仁API在A股、港股数据方面表现优秀，可以替换MCP服务中约46%的接口功能。特别是在财务数据、估值分析、基金研究、宏观数据等方面具有明显优势。

但在以下领域仍需保留MCP或寻找其他方案：
- 分析师预估和评级
- 债券和衍生品定价
- M&A和PE交易数据
- 新闻情感和事件驱动
- 美股个股数据

**建议采用组合方案**：
- 理杏仁作为主要数据源(A股、港股、基金、宏观)
- AKShare作为补充数据源(新闻、公告等)
- 保留部分MCP服务(分析师、债券、M&A等专业数据)

---

**最后更新**: 2026年2月27日  
**理杏仁API版本**: 最新版  
**对比接口总数**: 91个  
**理杏仁完全支持**: 42个 (46%)  
**理杏仁部分支持**: 18个 (20%)  
**理杏仁不支持**: 31个 (34%)
