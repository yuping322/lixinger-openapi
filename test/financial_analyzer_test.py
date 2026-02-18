#!/usr/bin/env python3
"""
财报分析技能测试脚本
"""
import sys
import os
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../skills/China-market/findata-toolkit-cn/scripts'))

from skills.financial_statement_analyzer.analyzer import run_analysis

def test_analyzer():
    # 测试贵州茅台
    print("Testing Financial Statement Analyzer for 600519 (贵州茅台)...")
    result = run_analysis("600519", years=3)

    if "error" in result:
        print(f"Error: {result['error']}")
        return

    print(json.dumps(result, indent=2, ensure_ascii=False))

    # 打印核心指标
    print("\n" + "="*80)
    print("核心分析结果:")
    print(f"股票代码: {result['stock_code']}")
    print(f"综合评分: {result['comprehensive_score']}")
    print(f"综合评级: {result['overall_rating']}")

    print("\n最近一年杜邦分析:")
    latest_dupont = result['dupont_analysis'][0]
    print(f"ROE: {latest_dupont['roe']}%")
    print(f"净利率: {latest_dupont['net_profit_margin']}%")
    print(f"资产周转率: {latest_dupont['asset_turnover']}")
    print(f"杠杆率: {latest_dupont['leverage_ratio']}")

    print("\n最近一年现金流质量:")
    latest_cf = result['cashflow_quality_analysis'][0]
    print(f"经营现金流/净利润: {latest_cf['cash_to_profit_ratio']}%")
    print(f"质量评估: {latest_cf['quality_assessment']}")

    print("\n财务风险识别:")
    risk = result['fraud_risk_identification']
    print(f"风险等级: {risk['risk_level']}")
    print(f"风险数量: {risk['total_risks']}")
    for r in risk['risk_details']:
        print(f"- {r['risk_type']}({r['level']}): {r['description']}")

if __name__ == "__main__":
    test_analyzer()
