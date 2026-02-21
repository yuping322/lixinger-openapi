#!/usr/bin/env python3
"""测试理杏仁API接口可用性"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lixinger_openapi.query import query_json
from lixinger_openapi.token import set_token
from datetime import datetime, timedelta
import json

# 设置token
set_token('ffad9101-8689-4b5d-bd79-763c58522a95', write_token=False)

# 测试股票代码
TEST_SYMBOL = "600519"  # 贵州茅台

# 定义所有要测试的接口
API_TESTS = [
    # 基础信息类
    ("公司基本信息", "cn/company", {"stockCodes": [TEST_SYMBOL]}),
    ("公司概况", "cn/company/profile", {"stockCode": TEST_SYMBOL}),
    
    # K线和行情
    ("K线数据", "cn/company/candlestick", {
        "stockCode": TEST_SYMBOL,
        "type": "ex_rights",
        "startDate": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
        "endDate": datetime.now().strftime("%Y-%m-%d")
    }),
    
    # 股东相关
    ("股东人数", "cn/company/shareholders-num", {
        "stockCode": TEST_SYMBOL,
        "startDate": (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"),
        "endDate": datetime.now().strftime("%Y-%m-%d")
    }),
    ("股东信息", "cn/company/shareholders", {"stockCode": TEST_SYMBOL}),
    ("高管增减持", "cn/company/executive-shareholding", {"stockCode": TEST_SYMBOL}),
    ("大股东增减持", "cn/company/major-shareholder-change", {"stockCode": TEST_SYMBOL}),
    
    # 特殊数据
    ("龙虎榜", "cn/company/trading-abnormal", {"stockCode": TEST_SYMBOL}),
    ("大宗交易", "cn/company/block-trade", {"stockCode": TEST_SYMBOL}),
    ("股权质押", "cn/company/equity-pledge", {"stockCode": TEST_SYMBOL}),
    
    # 财务相关
    ("分红送配", "cn/company/dividend-allotment", {"stockCode": TEST_SYMBOL}),
    ("营收构成", "cn/company/revenue-structure", {"stockCode": TEST_SYMBOL}),
    ("经营数据", "cn/company/operation-data", {"stockCode": TEST_SYMBOL}),
    
    # 关系数据
    ("所属行业", "cn/company/related-industry", {"stockCode": TEST_SYMBOL}),
    ("所属指数", "cn/company/related-index", {"stockCode": TEST_SYMBOL}),
    
    # 其他
    ("公告", "cn/company/announcement", {"stockCode": TEST_SYMBOL, "limit": 10}),
    ("热度数据", "cn/company/hot-data", {"stockCode": TEST_SYMBOL}),
    ("资金流向", "cn/company/fund-flow", {"stockCode": TEST_SYMBOL}),
    ("股本变动", "cn/company/share-change", {"stockCode": TEST_SYMBOL}),
]

def test_api(name: str, endpoint: str, params: dict) -> dict:
    """测试单个API接口"""
    try:
        result = query_json(endpoint, params)
        code = result.get('code', 0)
        data = result.get('data', [])
        data_count = len(data) if isinstance(data, list) else (1 if data else 0)
        
        return {
            "name": name,
            "endpoint": endpoint,
            "code": code,
            "success": code == 1,
            "has_data": data_count > 0,
            "data_count": data_count,
            "message": result.get('msg', result.get('message', 'N/A'))
        }
    except Exception as e:
        return {
            "name": name,
            "endpoint": endpoint,
            "code": -1,
            "success": False,
            "has_data": False,
            "data_count": 0,
            "message": str(e)
        }

def main():
    print("=" * 80)
    print(f"理杏仁API接口可用性测试")
    print(f"测试股票: {TEST_SYMBOL} (贵州茅台)")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    results = []
    success_count = 0
    has_data_count = 0
    
    for name, endpoint, params in API_TESTS:
        print(f"\n测试: {name}")
        print(f"  接口: {endpoint}")
        
        result = test_api(name, endpoint, params)
        results.append(result)
        
        if result['success']:
            success_count += 1
            if result['has_data']:
                has_data_count += 1
                print(f"  ✅ 成功 - 有数据 ({result['data_count']}条)")
            else:
                print(f"  ⚠️  成功 - 无数据")
        else:
            print(f"  ❌ 失败 - {result['message']}")
    
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
            print(f"  - {r['name']}")
    
    print("\n❌ 不可用接口:")
    for r in results:
        if not r['success']:
            print(f"  - {r['name']}: {r['message']}")
    
    # 保存详细结果
    output_file = Path(__file__).parent / "lixinger_api_test_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "test_time": datetime.now().isoformat(),
            "test_symbol": TEST_SYMBOL,
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
