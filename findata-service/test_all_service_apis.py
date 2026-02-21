#!/usr/bin/env python3
"""测试findata-service所有API接口"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"
TEST_SYMBOL = "600519"  # 贵州茅台

# 日期参数
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
start_date_30d = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

# 定义所有要测试的接口
API_TESTS = [
    # ========== 股票基础信息 ==========
    {
        "name": "公司基本信息",
        "url": f"{BASE_URL}/api/cn/stock/{TEST_SYMBOL}/basic",
        "method": "GET"
    },
    {
        "name": "公司概况",
        "url": f"{BASE_URL}/api/cn/stock/{TEST_SYMBOL}/profile",
        "method": "GET"
    },
    {
        "name": "K线数据",
        "url": f"{BASE_URL}/api/cn/stock/{TEST_SYMBOL}/history",
        "method": "GET",
        "params": {"start_date": start_date_30d, "end_date": end_date}
    },
    {
        "name": "实时行情",
        "url": f"{BASE_URL}/api/cn/stock/{TEST_SYMBOL}/realtime",
        "method": "GET"
    },
    {
        "name": "估值指标",
        "url": f"{BASE_URL}/api/cn/stock/{TEST_SYMBOL}/valuation",
        "method": "GET"
    },
    {
        "name": "公告",
        "url": f"{BASE_URL}/api/cn/stock/{TEST_SYMBOL}/announcement",
        "method": "GET"
    },
    
    # ========== 股东信息 ==========
    {
        "name": "股东人数",
        "url": f"{BASE_URL}/api/cn/shareholder/{TEST_SYMBOL}/count",
        "method": "GET"
    },
    {
        "name": "股东信息",
        "url": f"{BASE_URL}/api/cn/shareholder/{TEST_SYMBOL}",
        "method": "GET"
    },
    {
        "name": "高管增减持",
        "url": f"{BASE_URL}/api/cn/shareholder/{TEST_SYMBOL}/executive",
        "method": "GET"
    },
    {
        "name": "大股东增减持",
        "url": f"{BASE_URL}/api/cn/shareholder/{TEST_SYMBOL}/major",
        "method": "GET"
    },
    {
        "name": "股本变动",
        "url": f"{BASE_URL}/api/cn/shareholder/{TEST_SYMBOL}/equity-change",
        "method": "GET"
    },
    
    # ========== 特殊数据 ==========
    {
        "name": "龙虎榜",
        "url": f"{BASE_URL}/api/cn/special/dragon-tiger/{TEST_SYMBOL}",
        "method": "GET"
    },
    {
        "name": "大宗交易",
        "url": f"{BASE_URL}/api/cn/special/block-deal/{TEST_SYMBOL}",
        "method": "GET"
    },
    {
        "name": "股权质押",
        "url": f"{BASE_URL}/api/cn/special/equity-pledge/{TEST_SYMBOL}",
        "method": "GET"
    },
    
    # ========== 分红配股 ==========
    {
        "name": "分红送配",
        "url": f"{BASE_URL}/api/cn/dividend/{TEST_SYMBOL}",
        "method": "GET"
    },
]

def test_api(test_case):
    """测试单个API"""
    try:
        if test_case["method"] == "GET":
            params = test_case.get("params", {})
            response = requests.get(test_case["url"], params=params, timeout=10)
        else:
            response = requests.post(test_case["url"], json=test_case.get("data", {}), timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            code = data.get("code", 0)
            data_list = data.get("data", [])
            data_count = len(data_list) if isinstance(data_list, list) else (1 if data_list else 0)
            warnings = data.get("warnings", [])
            
            return {
                "name": test_case["name"],
                "url": test_case["url"],
                "status_code": response.status_code,
                "code": code,
                "success": code == 1,
                "has_data": data_count > 0,
                "data_count": data_count,
                "warnings": warnings,
                "sample": data_list[0] if isinstance(data_list, list) and len(data_list) > 0 else None
            }
        else:
            return {
                "name": test_case["name"],
                "url": test_case["url"],
                "status_code": response.status_code,
                "code": 0,
                "success": False,
                "has_data": False,
                "data_count": 0,
                "warnings": [],
                "error": response.text[:200]
            }
    except Exception as e:
        return {
            "name": test_case["name"],
            "url": test_case["url"],
            "status_code": 0,
            "code": -1,
            "success": False,
            "has_data": False,
            "data_count": 0,
            "warnings": [],
            "error": str(e)
        }

def main():
    print("=" * 80)
    print(f"Findata Service 全面接口测试")
    print(f"测试股票: {TEST_SYMBOL} (贵州茅台)")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"服务地址: {BASE_URL}")
    print("=" * 80)
    
    # 先测试服务是否可用
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ 服务运行正常\n")
        else:
            print("❌ 服务异常\n")
            return
    except Exception as e:
        print(f"❌ 无法连接到服务: {e}\n")
        return
    
    results = []
    success_count = 0
    has_data_count = 0
    
    for test_case in API_TESTS:
        print(f"\n测试: {test_case['name']}")
        print(f"  URL: {test_case['url']}")
        
        result = test_api(test_case)
        results.append(result)
        
        if result['success']:
            success_count += 1
            if result['has_data']:
                has_data_count += 1
                print(f"  ✅ 成功 - 有数据 ({result['data_count']}条)")
                if result.get('sample'):
                    print(f"  样例: {json.dumps(result['sample'], ensure_ascii=False)[:100]}...")
            else:
                print(f"  ⚠️  成功 - 无数据")
                if result['warnings']:
                    print(f"  提示: {result['warnings'][0]}")
        else:
            print(f"  ❌ 失败 - HTTP {result['status_code']}")
            if result.get('error'):
                print(f"  错误: {result['error'][:100]}")
    
    # 生成报告
    print("\n" + "=" * 80)
    print("测试结果汇总")
    print("=" * 80)
    print(f"总接口数: {len(API_TESTS)}")
    print(f"调用成功: {success_count} ({success_count/len(API_TESTS)*100:.1f}%)")
    print(f"有数据返回: {has_data_count} ({has_data_count/len(API_TESTS)*100:.1f}%)")
    print(f"无数据返回: {success_count - has_data_count}")
    print(f"调用失败: {len(API_TESTS) - success_count}")
    
    # 分类统计
    print("\n" + "-" * 80)
    print("✅ 可用接口（有数据）:")
    for r in results:
        if r['success'] and r['has_data']:
            print(f"  - {r['name']}: {r['data_count']}条数据")
    
    print("\n⚠️  可用但无数据:")
    for r in results:
        if r['success'] and not r['has_data']:
            warning = f" - {r['warnings'][0][:50]}" if r['warnings'] else ""
            print(f"  - {r['name']}{warning}")
    
    print("\n❌ 不可用接口:")
    for r in results:
        if not r['success']:
            print(f"  - {r['name']}: HTTP {r['status_code']}")
    
    # 保存详细结果
    output_file = "findata-service/service_api_test_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "test_time": datetime.now().isoformat(),
            "test_symbol": TEST_SYMBOL,
            "base_url": BASE_URL,
            "summary": {
                "total": len(API_TESTS),
                "success": success_count,
                "has_data": has_data_count,
                "no_data": success_count - has_data_count,
                "failed": len(API_TESTS) - success_count
            },
            "results": results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n详细结果已保存到: {output_file}")

if __name__ == "__main__":
    main()
