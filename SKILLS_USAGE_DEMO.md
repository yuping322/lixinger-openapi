# Skills使用演示

本文档展示如何在Kiro中使用已就绪的金融分析skills。

---

## 🚀 快速开始

### 前提条件
1. ✅ findata-service已启动 (http://localhost:8000)
2. ✅ 理杏仁Token已配置
3. ✅ Skills配置文件已加载 (`.kiro/steering/lixinger-skills.md`)

---

## 💡 使用示例

### 示例1: 分红分析

**用户问题**:
```
帮我分析一下贵州茅台600519的分红情况
```

**Kiro会自动**:
1. 识别到这是分红相关问题
2. 选择 `dividend-corporate-action-tracker` skill
3. 调用findata-service获取数据
4. 生成分红分析报告

**预期输出**:
```
贵州茅台(600519)分红分析报告

一、分红概况
- 近3年分红次数: 9次
- 最新分红: 2025-11-06
- 平均股息率: X.XX%
- 分红增长率: X.XX%

二、分红可持续性
- 分红率: XX%
- 现金流覆盖: X.X倍
- 连续分红年数: X年

三、投资建议
...
```

---

### 示例2: 股东结构分析

**用户问题**:
```
查一下贵州茅台的股东结构变化
```

**Kiro会自动**:
1. 选择 `shareholder-structure-monitor` skill
2. 获取股东人数和股本变动数据
3. 分析筹码集中度变化

**预期输出**:
```
贵州茅台(600519)股东结构分析

一、股东人数变化
- 最新股东数: 238,512户
- 环比变化: +8.09%
- 筹码集中度: 分散

二、股本变动
- 总股本: 12.52亿股
- 流通A股: 12.52亿股
- 最近变动: 股份回购

三、分析结论
...
```

---

### 示例3: 公告监控

**用户问题**:
```
最近有什么重要公告吗？600519
```

**Kiro会自动**:
1. 选择 `disclosure-notice-monitor` skill
2. 获取最新公告数据
3. 识别重要公告

**预期输出**:
```
贵州茅台(600519)最新公告

最近20条公告:
1. [2026-02-04] 关于...
2. [2026-01-28] 关于...
...

重要公告提示:
- 业绩预告: ...
- 分红方案: ...
```

---

### 示例4: 个股研究报告

**用户问题**:
```
给我生成一份贵州茅台的投资分析报告
```

**Kiro会自动**:
1. 选择 `equity-research-orchestrator` skill
2. 整合多个数据源
3. 生成完整研究报告

**预期输出**:
```
贵州茅台(600519)投资分析报告

一、公司概况
- 公司名称: 贵州茅台酒股份有限公司
- 所在地: 贵州省遵义市
- 上市日期: 2001-08-27

二、基本面分析
- 分红情况: ...
- 股东结构: ...
- 股本变动: ...

三、技术面分析
- 价格走势: ...
- 成交量: ...
- 技术指标: ...

四、投资建议
...
```

---

### 示例5: 市场概览

**用户问题**:
```
今天市场怎么样？
```

**Kiro会自动**:
1. 选择 `market-overview-dashboard` skill
2. 获取主要指数数据
3. 生成市场概览

**预期输出**:
```
A股市场概览

一、主要指数
- 上证指数: ...
- 深证成指: ...
- 创业板指: ...

二、市场表现
- 涨跌家数: ...
- 成交金额: ...
- 热点板块: ...
```

---

## 🔧 高级用法

### 组合使用多个Skills

**用户问题**:
```
帮我全面分析一下贵州茅台，包括分红、股东结构、最新公告
```

**Kiro会自动**:
1. 调用 `dividend-corporate-action-tracker`
2. 调用 `shareholder-structure-monitor`
3. 调用 `disclosure-notice-monitor`
4. 整合所有分析结果

---

### 批量分析

**用户问题**:
```
对比分析贵州茅台600519和五粮液000858的分红情况
```

**Kiro会自动**:
1. 对两只股票分别调用 `dividend-corporate-action-tracker`
2. 生成对比分析报告

---

## 📊 数据获取方式

Skills可以通过以下方式获取数据：

### 方式1: 通过findata-service (推荐)
```python
import requests

# 获取分红数据
response = requests.get("http://localhost:8000/api/cn/dividend/600519")
data = response.json()
```

### 方式2: 直接调用理杏仁API
```python
from lixinger_openapi.query import query_json

result = query_json("cn/company/dividend", {
    "stockCode": "600519",
    "startDate": "2023-01-01",
    "endDate": "2026-02-21"
})
```

### 方式3: 使用toolkit脚本
```bash
python skills/China-market/findata-toolkit-cn/scripts/toolkit.py --stock 600519
```

---

## ⚠️ 注意事项

### 1. 数据时效性
- 理杏仁数据有延迟（通常15分钟）
- 财务数据按季度更新
- 建议定期刷新数据

### 2. 数据限制
- 免费版有访问次数限制
- 部分高级数据不可用
- 需要时考虑升级订阅

### 3. 分析局限
- 所有分析仅供参考
- 不构成投资建议
- 投资有风险，决策需谨慎

---

## 🎯 最佳实践

### 1. 数据验证
- 使用前先验证数据可用性
- 检查数据的时间范围
- 注意数据的完整性

### 2. 结果解读
- 结合多个维度分析
- 注意风险提示
- 保持客观中立

### 3. 持续跟踪
- 定期更新分析
- 关注重要变化
- 建立监控机制

---

## 📚 相关资源

- **Skills列表**: `.kiro/steering/lixinger-skills.md`
- **API文档**: `findata-service/API_REFERENCE.md`
- **数据可用性**: `SKILLS_READINESS_REPORT.md`
- **测试脚本**: `test_skills_data_availability.py`

---

## 🎉 总结

现在你可以在Kiro中直接使用以下skills：

1. ✅ dividend-corporate-action-tracker - 分红分析
2. ✅ shareholder-structure-monitor - 股东分析
3. ✅ disclosure-notice-monitor - 公告监控
4. ✅ market-overview-dashboard - 市场概览
5. ✅ equity-research-orchestrator - 研究报告

只需要在Kiro中提出相关问题，系统会自动选择合适的skill进行分析！

---

**文档更新时间**: 2026-02-21  
**作者**: Kiro AI
