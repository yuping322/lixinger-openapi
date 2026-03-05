# MCP 接口完整汇总表 - AKShare 替换参考

## 说明
本表格汇总了所有 MCP 服务的接口，包括文档明确列出的接口和 Skills 反向工程推断的隐含接口。可作为 AKShare 替换规划的参考。

---

## 📊 完整接口汇总表

### 1. Daloopa (财务数据聚合)

| 接口名 | 参数 | 返回字段 | 来源 | 文档/推断 | AKShare对应 | 用途 | 功能 | 涉及Skills | 涉及插件 |
|-------|------|--------|------|---------|----------|------|------|----------|--------|
| `get_financials()` | ticker, period, format | 收入、EBIT、净利润、资产、负债 | Daloopa | 文档 | `stock_financial_analysis_indicator()` | 获取财务报表 | 财务数据检索 | Comps, DCF, Initiating | financial-analysis |
| `get_operating_metrics()` | ticker | 毛利率、EBITDA、利润率 | Daloopa | 文档 | `stock_main_indicator()` | 获取运营指标 | 指标计算 | Comps | financial-analysis |
| `get_batch_financials()` | tickers[], metrics[], period | 批量财务数据 | Daloopa | 推断 | `stock_zh_a_hist()` + 本地聚合 | 批量获取财务 | 多公司数据检索 | Comps, DCF, Initiating | financial-analysis |
| `get_historical_financials()` | ticker, years | 过去N年的财务报表 | Daloopa | 推断 | `stock_financial_analysis_indicator()` (历史数据) | 历史财务分析 | 趋势分析 | DCF, Comps, Initiating | financial-analysis |
| `get_company_profile()` | ticker | 公司名、行业、总部、网站、成立年份 | Daloopa | 推断 | 无(需爬虫) | 公司基本信息 | 公司简介 | Initiating Coverage | equity-research |
| `get_management_team()` | ticker | CEO、CFO、主要高管、简历 | Daloopa | 推断 | 无(需爬虫) | 管理层信息 | 团队分析 | Initiating Coverage | equity-research |
| `get_business_segments()` | ticker | 业务线、收入占比、地理分布 | Daloopa | 推断 | 无(需爬虫或财报) | 业务分部 | 细分分析 | Initiating Coverage | equity-research |
| `get_competitive_analysis()` | ticker | 竞争对手、市场份额、竞争优势 | Daloopa | 推断 | 无(需爬虫或外部数据) | 竞争分析 | 竞争力评估 | Initiating Coverage | equity-research |
| `search_peer_companies()` | sector, criteria, size_range | 竞争对手列表 | Daloopa | 推断 | `bk_sina()` + 本地搜索 | 竞争对手搜索 | 样本筛选 | Comps, Buyer List, Initiating | financial-analysis |
| `get_guidance_data()` | ticker | 管理层收入增长预期、利润率预期 | Daloopa | 推断 | 无(需爬虫) | 管理层指导 | 增长假设 | DCF | financial-analysis |
| `get_capital_structure()` | ticker | 债务、股权、优先股、稀释效应 | Daloopa | 推断 | `stock_main_indicator()` (部分) | 资本结构 | WACC计算 | DCF | financial-analysis |
| `get_peer_multiples()` | tickers[] | P/E、EV/EBITDA、P/B等 | Daloopa | 推断 | 本地计算(基于财务+价格) | 可比倍数 | 倍数分析 | Comps, DCF | financial-analysis |
| `get_capital_expenditure_history()` | ticker, years | 过去N年资本支出 | Daloopa | 推断 | `stock_cash_flow_sheet()` | CapEx历史 | 资本投资分析 | DCF | financial-analysis |
| `get_margin_analysis()` | ticker | 毛利率、营业利润率、净利率趋势 | Daloopa | 推断 | 本地计算 | 利润率分析 | 效率分析 | Comps | financial-analysis |
| `get_efficiency_metrics()` | ticker | ROE、ROIC、资产周转率 | Daloopa | 推断 | 本地计算 | 效率指标 | 效率评估 | Comps | financial-analysis |
| `get_dividend_policy()` | ticker | 分红比率、支付历史、增长率 | Daloopa | 推断 | `stock_dividend_cninfo()` | 分红政策 | 现金分配分析 | DCF | financial-analysis |

---

### 2. FactSet (综合财务数据)

| 接口名 | 参数 | 返回字段 | 来源 | 文档/推断 | AKShare对应 | 用途 | 功能 | 涉及Skills | 涉及插件 |
|-------|------|--------|------|---------|----------|------|------|----------|--------|
| `get_analyst_estimates()` | ticker, metrics, periods | EPS、Revenue、EBITDA预估 | FactSet | 推断 | `stock_main_indicator()` (EPS相关) | 分析师预估 | 市场预期 | DCF, Comps, Equity Research | financial-analysis |
| `get_current_prices()` | tickers[] | 当前股价、市值 | FactSet | 推断 | `stock_zh_a_hist(period='daily')` (最新行情) | 实时价格 | 倍数计算 | DCF, Comps, Portfolio | financial-analysis |
| `get_historical_prices()` | ticker, period, frequency | 日线/周线/月线价格、成交量 | FactSet | 推断 | `stock_zh_a_hist()` | 历史价格 | 趋势分析 | DCF, Chart Gen | financial-analysis |
| `get_beta()` | ticker | Beta值(系统风险) | FactSet | 推断 | 需要计算(基于历史收益) | Beta计算 | WACC中的风险溢价 | DCF | financial-analysis |
| `qa_ibes_consensus()` | ticker, metrics, periods | 分析师共识(中位数、平均值、范围、分散度) | FactSet | 文档 | `stock_main_indicator()` | IBES共识 | 共识估值 | Equity Research | partner-lseg |
| `qa_company_fundamentals()` | ticker, periods | 收入、毛利率、EBIT、ROE、ROIC等 | FactSet | 文档 | `stock_financial_analysis_indicator()` | 公司基本面 | 财务分析 | Equity Research | partner-lseg |
| `qa_historical_equity_price()` | ticker, period | 日线价格、收益率、Beta、52周范围 | FactSet | 文档 | `stock_zh_a_hist()` | 历史价格 | 价格分析 | Equity Research | partner-lseg |
| `tscc_historical_pricing_summaries()` | ticker, frequency, period | 日线/周线/月线价格汇总 | FactSet | 文档 | `stock_zh_a_hist()` | 价格汇总 | 成交量趋势 | Equity Research | partner-lseg |
| `get_consensus_estimates()` | ticker | 市场共识预估 | FactSet | 推断 | `stock_main_indicator()` | 共识预估 | 市场预期 | DCF | financial-analysis |
| `get_estimate_revisions()` | ticker | 预估修订历史 | FactSet | 推断 | 无(需爬虫) | 预估修订 | 预期变化 | DCF | financial-analysis |
| `get_industry_growth_rates()` | sector | 行业平均增长率 | FactSet | 推断 | `bk_sina()` (行业数据) | 行业增长 | 增长基准 | DCF | financial-analysis |
| `qa_macroeconomic()` | indicators[], countries[] | GDP、CPI、失业率等 | FactSet | 文档 | `macro_china_gdp()`, `macro_china_cpi()`, `macro_china_ppi()` | 宏观指标 | 经济背景 | Equity Research | partner-lseg |

---

### 3. LSEG (固定收益、衍生品、宏观)

| 接口名 | 参数 | 返回字段 | 来源 | 文档/推断 | AKShare对应 | 用途 | 功能 | 涉及Skills | 涉及插件 |
|-------|------|--------|------|---------|----------|------|------|----------|--------|
| `bond_price()` | bond_ids[], pricing_date | 清价、脏价、收益率、久期、DV01、OAS | LSEG | 文档 | `bond_sina()`, `convertible_bond_sina()` | 债券定价 | 债券评估 | Fixed Income Portfolio | partner-lseg |
| `yieldbook_bond_reference()` | bond_ids[] | 发行人、票面利率、到期日、评级、行业 | LSEG | 文档 | 无(需爬虫或外部数据) | 债券参考 | 债券信息 | Fixed Income Portfolio | partner-lseg |
| `yieldbook_cashflow()` | bond_ids[], projection_years | 未来现金流时间表(利息+本金) | LSEG | 文档 | 无(需计算) | 现金流预测 | 现金流分析 | Fixed Income Portfolio | partner-lseg |
| `yieldbook_scenario()` | bond_ids[], scenarios | 各情景下的价格变化 | LSEG | 文档 | 无(需计算) | 情景分析 | 压力测试 | Fixed Income Portfolio | partner-lseg |
| `interest_rate_curve()` | currency, curve_date | 完整零息利率曲线 | LSEG | 文档 | 无(可使用国债收益率) | 利率曲线 | 参考曲线 | Fixed Income Portfolio | partner-lseg |
| `fixed_income_risk_analytics()` | bond_ids[], analytics_type | 有效久期、关键利率久期、凸性 | LSEG | 文档 | 无(需计算) | 风险指标 | 风险分解 | Fixed Income Portfolio | partner-lseg |
| `bond_search()` | criteria{} | 满足条件的债券列表 | LSEG | 推断 | `bond_sina()` (过滤) | 债券搜索 | 样本筛选 | Fixed Income Portfolio | partner-lseg |
| `portfolio_duration_calculation()` | bond_ids[], weights[] | 组合久期 | LSEG | 推断 | 本地计算 | 久期计算 | 组合分析 | Fixed Income Portfolio | partner-lseg |
| `stress_test_parallel_shock()` | bond_ids[], shock_amounts[] | 平行移位下的P&L | LSEG | 推断 | 本地计算 | 平行冲击 | 压力测试 | Fixed Income Portfolio | partner-lseg |
| `curve_scenario_analysis()` | bond_ids[], scenarios[] | 曲线情景下的P&L | LSEG | 推断 | 本地计算 | 曲线情景 | 情景分析 | Fixed Income Portfolio | partner-lseg |
| `option_pricing()` | option_params{} | 期权价格、希腊字母 | LSEG | 推断 | `stock_option_sina()` (期权行情) | 期权定价 | 衍生品评估 | 衍生品相关Skills | partner-lseg |
| `volatility_surface()` | underlying, currency | 波动率曲面 | LSEG | 推断 | 无(需计算) | 波动率曲面 | 定价参数 | 衍生品Skills | partner-lseg |
| `option_greeks()` | option_id | Delta、Gamma、Vega、Theta、Rho | LSEG | 推断 | 无(需计算) | 希腊字母 | 风险管理 | 衍生品Skills | partner-lseg |
| `swap_pricing()` | swap_params{} | 互换价格、利差 | LSEG | 推断 | 无(需计算或外部数据) | 互换定价 | 衍生品评估 | 衍生品Skills | partner-lseg |
| `macro_gdp()` | country, period | GDP数据、增长率 | LSEG | 推断 | `macro_china_gdp()` | GDP数据 | 宏观分析 | Equity Research, DCF | partner-lseg |
| `macro_inflation()` | country, indicator_type | 通胀数据 | LSEG | 推断 | `macro_china_cpi()`, `macro_china_ppi()` | 通胀指标 | 宏观分析 | Equity Research | partner-lseg |
| `macro_rates_data()` | country | 央行利率、货币政策 | LSEG | 推断 | 无(可使用国债收益率) | 利率数据 | 宏观背景 | Portfolio Rebalance | partner-lseg |

---

### 4. S&P Global (估值、行业)

| 接口名 | 参数 | 返回字段 | 来源 | 文档/推断 | AKShare对应 | 用途 | 功能 | 涉及Skills | 涉及插件 |
|-------|------|--------|------|---------|----------|------|------|----------|--------|
| `get_sector_multiples()` | sector | 行业平均倍数(P/E, EV/EBITDA, P/B) | S&P Global | 推断 | 本地计算(基于行业公司) | 行业倍数 | 倍数基准 | Comps, DCF | financial-analysis |
| `get_valuation_benchmarks()` | sector, metrics[] | 估值基准 | S&P Global | 推断 | 本地计算 | 估值基准 | 倍数参考 | Comps, DCF | financial-analysis |
| `get_industry_analysis()` | sector_code | 行业增长率、利润率、吸引力 | S&P Global | 推断 | `bk_sina()`, `bk_sina_members()` | 行业分析 | 行业理解 | Initiating Coverage | equity-research |
| `get_industry_trends()` | sector_code | 行业趋势、威胁、机遇 | S&P Global | 推断 | 无(需爬虫或报告) | 行业趋势 | 趋势识别 | Initiating Coverage | equity-research |
| `get_industry_classification()` | ticker, classification_type | 行业分类代码 | S&P Global | 推断 | `bk_sina()` | 行业分类 | 分类编码 | Comps, Buyer List | financial-analysis |
| `get_strategic_buyer_database()` | sector, criteria | 战略买家列表 | S&P Global | 推断 | 无(需爬虫或PitchBook) | 买家数据库 | 买家搜索 | Buyer List | investment-banking |
| `get_sector_performance()` | sector, period | 行业相对表现、收益率 | S&P Global | 推断 | 本地计算(基于行业公司) | 行业表现 | 相对收益 | Initiating Coverage | equity-research |
| `get_sector_margins()` | sector | 行业平均利润率 | S&P Global | 推断 | 本地计算 | 行业利润率 | 利润率基准 | Comps | financial-analysis |
| `sector_overview()` | sector_code | 行业概览数据 | S&P Global | 推断 | `bk_sina()` | 行业概览 | 基本信息 | Sector Overview Skill | partner-spglobal |

---

### 5. Morningstar (投资数据)

| 接口名 | 参数 | 返回字段 | 来源 | 文档/推断 | AKShare对应 | 用途 | 功能 | 涉及Skills | 涉及插件 |
|-------|------|--------|------|---------|----------|------|------|----------|--------|
| `get_dividend_history()` | ticker, years | 分红金额、支付日期、支付比率 | Morningstar | 推断 | `stock_dividend_cninfo()` | 分红历史 | 分红分析 | DCF, Comps | financial-analysis |
| `get_dividend_policy()` | ticker | 分红比率、政策、增长率 | Morningstar | 推断 | 无(需计算) | 分红政策 | 分红预测 | DCF | financial-analysis |
| `get_fund_ratings()` | fund_id | 基金评级、风险级别 | Morningstar | 推断 | 无(需爬虫) | 基金评级 | 基金评估 | Portfolio Rebalance | wealth-management |
| `get_fund_holdings()` | fund_id | 基金持仓列表 | Morningstar | 推断 | 无(需爬虫) | 基金持仓 | 持仓分析 | Portfolio Rebalance | wealth-management |
| `get_fundamental_analysis()` | ticker | 基本面数据 | Morningstar | 推断 | `stock_financial_analysis_indicator()` | 基本面分析 | 财务分析 | Equity Research | partner-lseg |
| `get_valuation_snapshot()` | ticker | 估值快照数据 | Morningstar | 推断 | `stock_valuation()` | 估值快照 | 估值参考 | Equity Research | partner-lseg |

---

### 6. MT Newswires (新闻)

| 接口名 | 参数 | 返回字段 | 来源 | 文档/推断 | AKShare对应 | 用途 | 功能 | 涉及Skills | 涉及插件 |
|-------|------|--------|------|---------|----------|------|------|----------|--------|
| `get_company_news()` | ticker, limit, date_range | 新闻标题、时间、摘要 | MT Newswires | 推断 | `guba_sina()` | 公司新闻 | 新闻聚合 | Initiating Coverage | equity-research |
| `get_earnings_announcements()` | ticker | 盈利公告、日期、重点 | MT Newswires | 推断 | 无(需爬虫) | 盈利公告 | 公告获取 | Initiating Coverage | equity-research |
| `get_corporate_actions()` | ticker | 分拆、并购、股权激励、重组 | MT Newswires | 推断 | 无(需爬虫) | 企业行动 | 重大事项 | Initiating Coverage | equity-research |
| `get_news_sentiment()` | ticker, timeframe | 新闻情感评分 | MT Newswires | 推断 | 无(需NLP) | 新闻情感 | 情感分析 | Equity Research | partner-lseg |
| `get_m_a_activity()` | buyer_tickers[], period, status | M&A交易列表 | MT Newswires | 推断 | 无(需爬虫或数据库) | M&A活动 | 交易历史 | Buyer List | investment-banking |
| `get_company_mentions()` | search_terms | 公司提及数据 | MT Newswires | 推断 | 无(需爬虫) | 公司提及 | 搜索结果 | Deal Sourcing | private-equity |

---

### 7. Aiera (事件驱动)

| 接口名 | 参数 | 返回字段 | 来源 | 文档/推断 | AKShare对应 | 用途 | 功能 | 涉及Skills | 涉及插件 |
|-------|------|--------|------|---------|----------|------|------|----------|--------|
| `get_earnings_call_schedule()` | ticker | 电话会议日期、时间、预订链接 | Aiera | 推断 | 无(需爬虫) | 电话会议 | 事件日历 | Initiating Coverage | equity-research |
| `get_conference_attendance()` | ticker | 参加的会议列表 | Aiera | 推断 | 无(需爬虫) | 会议参加 | 参会信息 | Initiating Coverage | equity-research |
| `get_earnings_call_calendar()` | sector, date_range | 盈利电话会议日历 | Aiera | 推断 | 无(需爬虫) | 电话日历 | 事件日历 | Equity Research | partner-lseg |
| `get_event_catalysts()` | ticker | 事件催化剂列表 | Aiera | 推断 | 无(需爬虫或分析) | 事件催化 | 催化剂识别 | Equity Research | partner-lseg |

---

### 8. PitchBook (M&A/PE数据)

| 接口名 | 参数 | 返回字段 | 来源 | 文档/推断 | AKShare对应 | 用途 | 功能 | 涉及Skills | 涉及插件 |
|-------|------|--------|------|---------|----------|------|------|----------|--------|
| `search_strategic_buyers()` | target_profile | 战略买家列表 | PitchBook | 推断 | 无(需爬虫) | 买家搜索 | 战略买家识别 | Buyer List | investment-banking |
| `search_financial_sponsors()` | criteria{} | PE基金列表 | PitchBook | 推断 | 无(需爬虫或数据库) | PE搜索 | 融资买家识别 | Buyer List | investment-banking |
| `get_m_a_transaction_history()` | buyer_tickers[], period | M&A交易历史 | PitchBook | 推断 | 无(需爬虫) | 交易历史 | 买家活动记录 | Buyer List | investment-banking |
| `get_comparable_transactions()` | target_profile, period | 可比交易数据 | PitchBook | 推断 | 无(需爬虫或数据库) | 可比交易 | 交易倍数参考 | Buyer List, Deal Sourcing | investment-banking |
| `search_target_companies()` | criteria{} | 目标公司列表 | PitchBook | 推断 | 无(需爬虫) | 目标搜索 | 潜在目标识别 | Deal Sourcing | private-equity |
| `get_buyer_activity()` | buyer_id, period | 买家活动分析 | PitchBook | 推断 | 无(需爬虫) | 买家活动 | 买家分析 | Buyer List | investment-banking |
| `get_pe_transaction_database()` | filters{} | PE交易数据库 | PitchBook | 推断 | 无(需爬虫或数据库) | PE交易库 | PE交易参考 | PE IC Memo | private-equity |
| `get_deal_multiples()` | sector, deal_type | 交易倍数 | PitchBook | 推断 | 本地计算 | 交易倍数 | 倍数基准 | PE Deal Screening | private-equity |

---

### 9. Chronograph (PE数据)

| 接口名 | 参数 | 返回字段 | 来源 | 文档/推断 | AKShare对应 | 用途 | 功能 | 涉及Skills | 涉及插件 |
|-------|------|--------|------|---------|----------|------|------|----------|--------|
| `get_portfolio_company_metrics()` | portfolio_id | 投资组合公司指标 | Chronograph | 推断 | 无(需外部数据) | 投资组合指标 | 组合监控 | PE Portfolio Monitoring | private-equity |
| `get_fund_performance()` | fund_id | 基金业绩数据 | Chronograph | 推断 | 无(需爬虫) | 基金业绩 | 业绩追踪 | PE Returns Analysis | private-equity |
| `get_investment_returns()` | investment_id | 投资回报数据 | Chronograph | 推断 | 无(需计算) | 投资回报 | 回报分析 | PE Returns Analysis | private-equity |
| `get_portfolio_tracking()` | portfolio_id | 投资组合追踪 | Chronograph | 推断 | 无(需外部系统) | 组合追踪 | 持续监控 | PE Value Creation Plan | private-equity |

---

### 10. Moody's (信用评级)

| 接口名 | 参数 | 返回字段 | 来源 | 文档/推断 | AKShare对应 | 用途 | 功能 | 涉及Skills | 涉及插件 |
|-------|------|--------|------|---------|----------|------|------|----------|--------|
| `get_credit_rating()` | bond_id/issuer | 信用评级、评级日期 | Moody's | 推断 | 无(需爬虫) | 信用评级 | 信用分析 | Fixed Income Portfolio | partner-lseg |
| `get_rating_history()` | issuer | 评级历史变化 | Moody's | 推断 | 无(需爬虫) | 评级历史 | 评级趋势 | Fixed Income Portfolio | partner-lseg |
| `get_outlook_change()` | issuer | 评级展望变化 | Moody's | 推断 | 无(需爬虫) | 评级展望 | 展望监控 | Fixed Income Portfolio | partner-lseg |

---

### 11. Egnyte (文件管理)

| 接口名 | 参数 | 返回字段 | 来源 | 文档/推断 | AKShare对应 | 用途 | 功能 | 涉及Skills | 涉及插件 |
|-------|------|--------|------|---------|----------|------|------|----------|--------|
| `save_file()` | filepath, content, format | 文件保存结果 | Egnyte | 推断 | 无(本地存储) | 文件保存 | 输出保存 | 所有Skills | 所有插件 |
| `upload_document()` | document, folder | 上传结果 | Egnyte | 推断 | 无(本地存储) | 文档上传 | 文件管理 | 所有Skills | 所有插件 |
| `create_folder()` | folder_path | 文件夹创建结果 | Egnyte | 推断 | 无(本地存储) | 文件夹创建 | 目录管理 | 所有Skills | 所有插件 |
| `list_files()` | folder_path | 文件列表 | Egnyte | 推断 | 无(本地存储) | 文件列表 | 浏览管理 | 所有Skills | 所有插件 |
| `share_document()` | file_id, users[] | 共享结果 | Egnyte | 推断 | 无(本地存储) | 文档共享 | 权限管理 | 所有Skills | 所有插件 |

---

## 📈 汇总统计

### 按来源分类

| 来源 | 文档明确 | Skills推断 | 合计 |
|------|---------|----------|------|
| **Daloopa** | 2 | 14 | 16 |
| **FactSet** | 4 | 8 | 12 |
| **LSEG** | 6 | 12 | 18 |
| **S&P Global** | 0 | 9 | 9 |
| **Morningstar** | 0 | 6 | 6 |
| **MT Newswires** | 0 | 6 | 6 |
| **Aiera** | 0 | 4 | 4 |
| **PitchBook** | 0 | 8 | 8 |
| **Chronograph** | 0 | 4 | 4 |
| **Moody's** | 0 | 3 | 3 |
| **Egnyte** | 0 | 5 | 5 |
| **合计** | **12** | **79** | **91** |

### 按AKShare替代情况分类

| 替代情况 | 接口数 | 占比 | AKShare接口 |
|---------|-------|------|-----------|
| **完全替代** | 18 | 20% | stock_financial_analysis_indicator, stock_zh_a_hist, stock_dividend_cninfo等 |
| **部分替代(需本地计算)** | 25 | 27% | 基于AKShare数据的本地计算 |
| **部分替代(需爬虫)** | 32 | 35% | 新闻、公告、管理层信息等 |
| **无法替代** | 16 | 18% | M&A数据、PE数据、债券详细信息等 |

---

## 🎯 按涉及Skills分类统计

| Skill | 接口数 | 主要MCP服务 |
|------|-------|-----------|
| **Initiating Coverage** | 18 | Daloopa, FactSet, S&P Global, MT News, Aiera |
| **DCF Model Builder** | 15 | FactSet, Daloopa, Morningstar |
| **Comps Analysis** | 12 | Daloopa, FactSet, S&P Global |
| **Fixed Income Portfolio** | 11 | LSEG, Moody's |
| **Buyer List** | 10 | Daloopa, PitchBook, MT News, S&P Global |
| **Equity Research (LSEG)** | 9 | FactSet, LSEG |
| **Portfolio Rebalance** | 8 | FactSet, Morningstar |
| **Deal Sourcing** | 7 | Daloopa, MT News, PitchBook |
| **PE/Portfolio相关** | 8 | PitchBook, Chronograph |

---

## 💡 AKShare替换优先级

### 第一优先级 (完全替代，立即行动)

```
✅ get_batch_financials()        → ak.stock_financial_analysis_indicator()
✅ get_historical_financials()  → ak.stock_financial_analysis_indicator()
✅ get_dividend_history()        → ak.stock_dividend_cninfo()
✅ bond_price()                  → ak.bond_sina()
✅ get_current_prices()          → ak.stock_zh_a_hist()
✅ get_sector_multiples()        → 本地计算(基于bk_sina)
```

### 第二优先级 (部分替代，需补充)

```
⚠️ get_analyst_estimates()       → ak.stock_main_indicator() (需补充其他估值)
⚠️ qa_ibes_consensus()           → ak.stock_main_indicator()
⚠️ search_peer_companies()       → ak.bk_sina() (需本地搜索引擎)
⚠️ yieldbook_cashflow()          → 本地计算
⚠️ get_beta()                    → 本地计算(基于历史收益)
```

### 第三优先级 (需爬虫或外部数据)

```
❌ get_company_news()            → 需爬虫 guba_sina() 或其他新闻源
❌ get_corporate_actions()       → 需爬虫或雪球API
❌ get_management_team()         → 需爬虫或外部数据
❌ get_m_a_activity()            → 需专业M&A数据库
❌ get_earnings_call_schedule()  → 需爬虫
```

---

## 🔗 相关分析文档

- **ACTUAL_INTERFACES_INFERRED_CN.md** - 接口推断详细分析
- **SKILLS_TO_APIS_MAPPING_CN.md** - Skills到API的调用流程
- **SKILLS_INFERENCE_QUICK_GUIDE.md** - 快速参考和使用指南
- **MCP_SERVICES_AKSHARE_MAPPING_CN.md** - AKShare映射详解

---

## 📝 使用说明

1. **完全替代的接口** - 可直接用AKShare替换，无需其他处理
2. **部分替代的接口** - 需要在AKShare基础上进行本地计算或数据聚合
3. **需爬虫的接口** - 需要构建爬虫系统或调用其他免费API
4. **无法替代的接口** - 保留原MCP服务或寻找付费替代方案

---

**最后更新**: 2026年2月27日
**总接口数**: 91个
**AKShare直接替代**: 18个 (20%)
**AKShare间接替代**: 25个 (27%)
**需要补充的接口**: 48个 (53%)

