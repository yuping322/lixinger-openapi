# 财报深度分析技能使用说明

## 功能概述
`financial_statement_analyzer` 是一个完整的上市公司财务报表深度分析工具，支持A股所有上市公司的多维度财务分析。

## 主要功能
1. **三大报表完整获取**：自动获取资产负债表、利润表、现金流量表最近N年历史数据
2. **杜邦分析体系**：ROE拆解为净利率 × 资产周转率 × 杠杆率
3. **现金流质量分析**：验证经营现金流与净利润的匹配程度
4. **财务造假风险识别**：存贷双高/商誉减值/应收账款高企/存货积压等风险预警
5. **成长能力分析**：营收/利润/资产同比增长率分析
6. **偿债能力分析**：流动比率/速动比率/资产负债率/现金比率分析
7. **运营效率分析**：应收账款周转天数/存货周转天数/总资产周转率分析
8. **综合评分与评级**：基于多维度指标给出A+到D的综合评级

## 调用方式
### 命令行调用
```bash
# 调用格式
/skill financial_statement_analyzer --stock_code <股票代码> [--years <分析年数>]

# 示例：分析贵州茅台最近3年财报
/skill financial_statement_analyzer --stock_code 600519 --years 3
```

### Python API调用
```python
from skills.financial_statement_analyzer import run_analysis

# 分析贵州茅台最近5年财报
result = run_analysis("600519", years=5)
print(result)
```

## 返回格式说明
返回标准JSON格式，包含以下字段：

```json
{
  "stock_code": "600519",
  "analysis_as_of": "2026-02-18",
  "time_range": "最近5年",
  "financial_statements": {
    "income_statement": [],  // 利润表
    "balance_sheet": [],     // 资产负债表
    "cashflow_statement": [] // 现金流量表
  },
  "dupont_analysis": [],      // 杜邦分析结果
  "cashflow_quality_analysis": [], // 现金流质量分析
  "fraud_risk_identification": {   // 财务风险识别
    "total_risks": 0,
    "risk_level": "低/中/高",
    "risk_details": []
  },
  "operation_efficiency_analysis": [], // 运营效率分析
  "solvency_analysis": [],      // 偿债能力分析
  "growth_analysis": [],        // 成长能力分析
  "comprehensive_score": 89.5,  // 综合评分 (0-100)
  "overall_rating": "A+"        // 综合评级 (A+/A/B+/B/C/D)
}
```

## 指标说明
### 综合评级标准
- **A+**: 得分≥85，财务状况非常优秀
- **A**: 得分≥75，财务状况良好
- **B+**: 得分≥65，财务状况一般偏上
- **B**: 得分≥55，财务状况一般
- **C**: 得分≥45，财务状况较差
- **D**: 得分<45，财务状况糟糕，存在较高风险

### 风险类型说明
- **存贷双高风险**：货币资金远低于有息负债，存在财务造假嫌疑
- **商誉减值风险**：商誉占净资产比例过高，存在大额减值风险
- **应收账款风险**：应收账款占营收比例过高，回款能力弱
- **存货积压风险**：存货占流动资产比例过高，存在积压减值风险

## 注意事项
1. 支持分析的最大年限为10年，默认返回最近5年数据
2. 数据来源为理杏仁(Lixinger)公开API，依赖API token配置
3. 返回数据中的金额单位均为亿元人民币
4. 财报数据更新频率为季度，年报数据通常在次年4月前披露
