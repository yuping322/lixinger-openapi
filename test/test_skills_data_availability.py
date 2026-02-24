#!/usr/bin/env python3
"""测试各个skill的数据可用性"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from lixinger_openapi.query import query_json
from lixinger_openapi.token import set_token
from datetime import datetime, timedelta

# 设置token
set_token('ffad9101-8689-4b5d-bd79-763c58522a95', write_token=False)

TEST_SYMBOL = "600519"  # 贵州茅台
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=365*3)).strftime("%Y-%m-%d")

# 定义skills及其所需数据
SKILLS_DATA_REQUIREMENTS = [
    {
        "name": "dividend-corporate-action-tracker",
        "description": "分红与配股跟踪器",
        "required_data": [
            ("分红数据", "cn/company/dividend", {"stockCode": TEST_SYMBOL, "startDate": start_date, "endDate": end_date}),
            ("股本变动", "cn/company/equity-change", {"stockCode": TEST_SYMBOL, "startDate": start_date, "endDate": end_date}),
            ("公司基本信息", "cn/company", {"stockCodes": [TEST_SYMBOL]})
        ]
    },
    {
        "name": "shareholder-structure-monitor",
        "description": "股东结构监控",
        "required_data": [
            ("股东人数", "cn/company/shareholders-num", {"stockCode": TEST_SYMBOL, "startDate": start_date, "endDate": end_date}),
            ("股本变动", "cn/company/equity-change", {"stockCode": TEST_SYMBOL, "startDate": start_date, "endDate": end_date}),
            ("公司基本信息", "cn/company", {"stockCodes": [TEST_SYMBOL]})
        ]
    },
    {
        "name": "disclosure-notice-monitor",
        "description": "披露公告监控",
        "required_data": [
            ("公告数据", "cn/company/announcement", {"stockCode": TEST_SYMBOL, "limit": 20}),
            ("公司基本信息", "cn/company", {"stockCodes": [TEST_SYMBOL]})
        ]
    },
    {
        "name": "market-overview-dashboard",
        "description": "市场概览仪表盘",
        "required_data": [
            ("K线数据", "cn/company/candlestick", {"stockCode": TEST_SYMBOL, "type": "ex_rights", "startDate": start_date, "endDate": end_date}),
            ("公司基本信息", "cn/company", {"stockCodes": [TEST_SYMBOL]})
        ]
    },
    {
        "name": "equity-research-orchestrator",
        "description": "个股研究报告生成器",
        "required_data": [
            ("公司基本信息", "cn/company", {"stockCodes": [TEST_SYMBOL]}),
            ("公司概况", "cn/company/profile", {"stockCodes": [TEST_SYMBOL]}),
            ("K线数据", "cn/company/candlestick", {"stockCode": TEST_SYMBOL, "type": "ex_rights", "startDate": start_date, "endDate": end_date}),
            ("分红数据", "cn/company/dividend", {"stockCode": TEST_SYMBOL, "startDate": start_date, "endDate": end_date}),
            ("股东人数", "cn/company/shareholders-num", {"stockCode": TEST_SYMBOL, "startDate": start_date, "endDate": end_date})
        ]
    }
]

def test_data_availability(data_name, endpoint, params):
    """测试单个数据接口的可用性"""
    try:
        result = query_json(endpoint, params)
        code = result.get('code', 0)
        data = result.get('data', [])
        data_count = len(data) if isinstance(data, list) else (1 if data else 0)
        
        return {
            "name": data_name,
            "endpoint": endpoint,
            "code": code,
            "success": code == 1,
            "has_data": data_count > 0,
            "data_count": data_count
        }
    except Exception as e:
        return {
            "name": data_name,
            "endpoint": endpoint,
            "code": -1,
            "success": False,
            "has_data": False,
            "data_count": 0,
            "error": str(e)
        }

def main():
    print("=" * 80)
    print("Skills数据可用性测试")
    print(f"测试股票: {TEST_SYMBOL} (贵州茅台)")
    print("=" * 80)
    
    results = []
    
    for skill in SKILLS_DATA_REQUIREMENTS:
        print(f"\n{'='*80}")
        print(f"Skill: {skill['name']}")
        print(f"描述: {skill['description']}")
        print(f"{'='*80}")
        
        skill_result = {
            "name": skill['name'],
            "description": skill['description'],
            "data_tests": [],
            "all_available": True
        }
        
        for data_name, endpoint, params in skill['required_data']:
            print(f"\n测试: {data_name}")
            print(f"  接口: {endpoint}")
            
            result = test_data_availability(data_name, endpoint, params)
            skill_result['data_tests'].append(result)
            
            if result['success'] and result['has_data']:
                print(f"  ✅ 可用 - {result['data_count']}条数据")
            elif result['success'] and not result['has_data']:
                print(f"  ⚠️  可用但无数据")
                skill_result['all_available'] = False
            else:
                print(f"  ❌ 不可用 - code={result['code']}")
                skill_result['all_available'] = False
        
        results.append(skill_result)
        
        # 总结
        if skill_result['all_available']:
            print(f"\n✅ {skill['name']} - 所有数据可用，可以正常运行")
        else:
            available_count = sum(1 for t in skill_result['data_tests'] if t['success'] and t['has_data'])
            total_count = len(skill_result['data_tests'])
            print(f"\n⚠️  {skill['name']} - {available_count}/{total_count} 数据可用，部分功能受限")
    
    # 最终汇总
    print("\n" + "=" * 80)
    print("测试结果汇总")
    print("=" * 80)
    
    fully_available = [r for r in results if r['all_available']]
    partially_available = [r for r in results if not r['all_available']]
    
    print(f"\n总测试Skills: {len(results)}")
    print(f"完全可用: {len(fully_available)}")
    print(f"部分可用: {len(partially_available)}")
    
    if fully_available:
        print("\n✅ 完全可用的Skills:")
        for r in fully_available:
            print(f"  - {r['name']}: {r['description']}")
    
    if partially_available:
        print("\n⚠️  部分可用的Skills:")
        for r in partially_available:
            available = sum(1 for t in r['data_tests'] if t['success'] and t['has_data'])
            total = len(r['data_tests'])
            print(f"  - {r['name']}: {available}/{total} 数据可用")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
