# 市场情绪监控 - 快速开始指南

## 🚀 立即使用（无需额外配置）

### 分析贵州茅台情绪

```bash
python3 market_sentiment_analysis_600519.py
```

**输出内容**:
- 📈 成交量情绪分析
- 👥 股东结构分析
- 📢 公告频率分析
- 🎯 综合情绪评分（0-100）
- 🔍 交叉验证与矛盾分析
- 💡 投资建议

---

## 📊 分析其他股票

修改脚本中的股票代码：

```python
# 在 market_sentiment_analysis_600519.py 中修改
stock_code = "000858"  # 改为你想分析的股票代码
```

或者创建通用版本：

```bash
python3 -c "
from market_sentiment_analysis_600519 import *
# 修改main()函数中的stock_code
"
```

---

## 🔥 获取真实热度排名（推荐）

### 方法1: 使用AKShare（免费）

```bash
# 1. 安装
pip install akshare

# 2. 获取东方财富人气榜
python3 -c "
import akshare as ak
hot = ak.stock_hot_rank_em()
print('东方财富人气榜 Top 10:')
print(hot.head(10)[['序号', '股票代码', '股票名称', '最新价', '涨跌幅', '人气']])
"

# 3. 获取资金流向
python3 -c "
import akshare as ak
flow = ak.stock_individual_fund_flow_rank(indicator='今日')
print('今日主力资金流向 Top 10:')
print(flow.head(10)[['序号', '代码', '名称', '最新价', '今日主力净流入-净额']])
"

# 4. 查询特定股票
python3 -c "
import akshare as ak
hot = ak.stock_hot_rank_em()
stock = hot[hot['股票代码'] == '600519']
if not stock.empty:
    print(f'贵州茅台排名: 第{stock.iloc[0][\"序号\"]}名')
    print(f'人气值: {stock.iloc[0][\"人气\"]}')
else:
    print('未在Top 100中')
"
```

### 方法2: 创建完整脚本

```bash
# 查看AKShare完整使用指南
cat HOT_RANK_DATA_GUIDE.md

# 里面包含:
# - 完整的AKShare接口说明
# - 集成到findata-service的方法
# - 多数据源对比
# - 最佳实践
```

---

## 📋 常用命令速查

### 理杏仁数据查询

```bash
# K线数据
python3 -c "
from lixinger_openapi.query import query_json
from lixinger_openapi.token import set_token
set_token('ffad9101-8689-4b5d-bd79-763c58522a95', write_token=False)
result = query_json('cn/company/candlestick', {
    'stockCode': '600519',
    'type': 'ex_rights',
    'startDate': '2026-01-01',
    'endDate': '2026-02-21'
})
print(f'获取到 {len(result[\"data\"])} 条K线数据')
"

# 股东人数
python3 -c "
from lixinger_openapi.query import query_json
from lixinger_openapi.token import set_token
set_token('ffad9101-8689-4b5d-bd79-763c58522a95', write_token=False)
result = query_json('cn/company/shareholders-num', {
    'stockCode': '600519',
    'startDate': '2025-01-01',
    'endDate': '2026-02-21'
})
if result['code'] == 1:
    latest = result['data'][-1]
    print(f'股东人数: {latest[\"num\"]} 户')
    print(f'变化率: {latest[\"shareholdersNumberChangeRate\"]*100:.2f}%')
"

# 公告
python3 -c "
from lixinger_openapi.query import query_json
from lixinger_openapi.token import set_token
set_token('ffad9101-8689-4b5d-bd79-763c58522a95', write_token=False)
result = query_json('cn/company/announcement', {
    'stockCode': '600519',
    'limit': 10
})
print(f'最近10条公告:')
for ann in result['data'][:5]:
    print(f'- {ann[\"date\"][:10]}: {ann[\"linkText\"]}')
"
```

### AKShare数据查询

```bash
# 热度排名
python3 -c "import akshare as ak; print(ak.stock_hot_rank_em().head())"

# 资金流向
python3 -c "import akshare as ak; print(ak.stock_individual_fund_flow_rank(indicator='今日').head())"

# 龙虎榜
python3 -c "import akshare as ak; print(ak.stock_lhb_detail_em(symbol='600519').head())"
```

---

## 🎯 使用场景

### 场景1: 每日市场情绪监控

```bash
# 早盘前运行
python3 market_sentiment_analysis_600519.py > daily_sentiment_$(date +%Y%m%d).txt

# 查看热度排名
python3 -c "
import akshare as ak
hot = ak.stock_hot_rank_em()
print('今日热度Top 10:')
print(hot.head(10))
"
```

### 场景2: 个股深度分析

```bash
# 1. 情绪分析
python3 market_sentiment_analysis_600519.py

# 2. 资金流向
python3 -c "
import akshare as ak
flow = ak.stock_individual_fund_flow(stock='600519', market='sh')
print(flow.tail(10))
"

# 3. 龙虎榜
python3 -c "
import akshare as ak
lhb = ak.stock_lhb_detail_em(symbol='600519')
print(lhb.head())
"
```

### 场景3: 板块热度监控

```bash
# 获取行业热度
python3 -c "
import akshare as ak
hot = ak.stock_hot_rank_em()
# 统计行业分布
print('热度Top 100行业分布:')
# 需要额外获取行业信息
"
```

---

## 📊 情绪评分解读

| 评分范围 | 情绪状态 | 说明 | 建议 |
|---------|---------|------|------|
| 70-100 | 🔥 热度高涨 | 市场关注度高，交易活跃 | 警惕追高风险 |
| 55-69 | ↗️ 温和积极 | 市场关注度正常，情绪略偏积极 | 可适度参与 |
| 45-54 | ➡️ 中性平稳 | 市场关注度一般，情绪中性 | 观望为主 |
| 30-44 | ↘️ 温和消极 | 市场关注度下降，情绪略偏消极 | 等待机会 |
| 0-29 | ❄️ 冷淡低迷 | 市场关注度低，交易清淡 | 可能是底部 |

---

## ⚠️ 重要提示

### 数据限制

1. **理杏仁免费版不提供**:
   - ❌ 热度数据 (hot-data)
   - ❌ 资金流向 (fund-flow)
   - ❌ 估值指标 (valuation)

2. **股东人数数据**:
   - ⚠️ 更新频率低（季度）
   - ⚠️ 有滞后性

3. **K线数据**:
   - ✅ 可用，但有15分钟延迟

### 使用建议

1. **情绪指标仅供参考**，不构成投资建议
2. **需结合基本面、技术面**综合判断
3. **注意A股交易限制**（T+1、涨跌停）
4. **数据时效性**：注意数据更新时间

---

## 🔧 故障排除

### 问题1: 理杏仁API返回code=0

**原因**: 免费版不支持该接口

**解决**: 使用AKShare或升级订阅

### 问题2: AKShare安装失败

```bash
# 使用国内镜像
pip install akshare -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题3: 数据为空

**检查**:
1. 股票代码是否正确
2. 日期范围是否合理
3. 是否在交易时间

---

## 📚 更多资源

- **完整指南**: `HOT_RANK_DATA_GUIDE.md`
- **任务总结**: `SENTIMENT_MONITORING_SUMMARY.md`
- **技能文档**: `skills/China-market/hot-rank-sentiment-monitor/SKILL.md`
- **AKShare文档**: https://akshare.akfamily.xyz/

---

## 💬 需要帮助？

如有问题，请查看：
1. `HOT_RANK_DATA_GUIDE.md` - 完整的数据获取指南
2. `SENTIMENT_MONITORING_SUMMARY.md` - 任务完成总结
3. AKShare官方文档 - https://akshare.akfamily.xyz/

---

**快速开始版本**: 1.0  
**更新时间**: 2026-02-21  
**适用对象**: 所有用户
