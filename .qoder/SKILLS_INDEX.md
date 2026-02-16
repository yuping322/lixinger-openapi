# 📊 理杏仁金融分析技能索引

## 📁 技能分类目录

### 🇨🇳 中国市场分析 (China-market/) - 57个技能
```
基础分析类:
├── financial-statement-analyzer    # 财务报表分析
├── peer-comparison-analyzer       # 同行对比分析
├── equity-research-orchestrator   # 股权研究协调器

风险监控类:
├── equity-pledge-risk-monitor     # 股权质押风险监控
├── st-delist-risk-scanner         # ST退市风险扫描
├── goodwill-risk-monitor          # 商誉风险监控
├── margin-risk-monitor            # 融资融券风险监控

资金流向类:
├── northbound-flow-analyzer       # 北向资金分析
├── fund-flow-monitor              # 资金流向监控
├── hsgt-holdings-monitor          # 沪深港通持股监控

市场分析类:
├── market-breadth-monitor         # 市场宽度监控
├── market-overview-dashboard      # 市场概览面板
├── volatility-regime-monitor      # 波动率状态监控
├── macro-liquidity-monitor        # 宏观流动性监控

事件驱动类:
├── dragon-tiger-list-analyzer     # 龙虎榜分析
├── block-deal-monitor             # 大宗交易监控
├── disclosure-notice-monitor      # 披露公告监控
├── insider-trading-analyzer       # 内幕交易分析

估值分析类:
├── undervalued-stock-screener     # 低估股票筛选
├── valuation-regime-detector      # 估值状态检测
├── high-dividend-strategy         # 高股息策略

量化策略类:
├── quant-factor-screener          # 量化因子筛选
├── factor-crowding-monitor        # 因子拥挤度监控
├── sector-rotation-detector       # 行业轮动检测

特殊主题:
├── industry-board-analyzer        # 行业板块分析
├── concept-board-analyzer         # 概念板块分析
├── industry-chain-mapper          # 产业链映射
├── esg-screener                   # ESG筛选器
```

### 🇺🇸 美国市场分析 (US-market/) - 36个技能
```
├── financial-statement-analyzer   # 财务报表分析
├── peer-comparison-analyzer       # 同行对比分析
├── equity-research-orchestrator   # 股权研究协调器
├── insider-trading-analyzer       # 内幕交易分析
├── earnings-reaction-analyzer     # 盈利反应分析
├── quant-factor-screener          # 量化因子筛选
├── undervalued-stock-screener     # 低估股票筛选
├── options-strategy-analyzer      # 期权策略分析
├── yield-curve-regime-detector    # 收益率曲线状态检测
```

### 🇭🇰 港股市场分析 (HK-market/) - 14个技能
```
├── hk-market-overview             # 港股市场概览
├── hk-market-breadth              # 港股市场宽度
├── hk-foreign-flow                # 港股外资流向
├── hk-southbound-flow             # 港股南向资金
├── hk-sector-rotation             # 港股行业轮动
├── hk-valuation-analyzer          # 港股估值分析
├── hk-liquidity-risk              # 港股流动性风险
├── hk-concentration-risk          # 港股集中度风险
```

### 📡 核心数据查询 (lixinger-data-query/) - 1个技能
```
├── lixinger-data-query            # 理杏仁API数据查询核心工具
```

## 🚀 快速使用命令

### A股市场查询
```bash
# 市场概览
toolkit-cn --market --mode brief

# 个股详细分析
toolkit-cn --stock 600519 --mode full

# 板块分析
toolkit-cn --sector 食品饮料

# 宏观数据
toolkit-cn --macro
```

### 数据筛选
```bash
# 低估值股票筛选
toolkit-cn --screen 'pe_ttm < 15 AND roe > 10'

# 高成长股票筛选  
toolkit-cn --screen 'revenue_growth_yoy > 20 AND net_profit_growth_yoy > 25'
```

### 直接API查询
```bash
# 查询公司基本信息
query-data --suffix 'cn/company' --params '{"stockCodes": ["600519"]}'

# 查询财务指标
query-data --suffix 'cn/stock/fundamental' --params '{"stockCodes": ["600519"], "date": "2024-01-01"}'
```

## 📝 使用流程

1. **启动环境**: 运行 `/Users/fengzhi/Downloads/git/lixinger-openapi/.qoder/setup_qoder_env.sh`
2. **选择技能**: 根据需求选择对应的技能目录
3. **执行命令**: 使用相应的toolkit命令获取数据
4. **分析结果**: 基于获取的数据进行专业分析

## ⚠️ 注意事项

- 确保已配置理杏仁API token
- 部分高频查询可能受到API限流影响
- 建议合理使用缓存避免重复请求
- 数据仅供参考，不构成投资建议