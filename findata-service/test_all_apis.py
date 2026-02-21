#!/usr/bin/env python3
"""完整API测试脚本"""

import requests
from datetime import datetime

BASE_URL = "http://localhost:8000"


def print_response(name: str, response: requests.Response):
    """打印响应结果"""
    status = "✓" if response.status_code == 200 else "✗"
    print(f"{status} {name:60s} 状态码: {response.status_code}", end="")
    if response.status_code == 200:
        data = response.json()
        print(f"  数据量: {data['meta']['count']}")
    else:
        print(f"  错误: {response.text[:100]}")


def test_all_apis():
    """测试所有API"""
    print("\n" + "="*80)
    print("Findata Service 完整API测试")
    print("="*80)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"服务地址: {BASE_URL}")
    print("="*80 + "\n")

    # 1. 健康检查
    print("【基础接口】")
    response = requests.get(f"{BASE_URL}/health")
    print_response("健康检查", response)

    # 2. 股票接口
    print("\n【股票接口】")
    tests = [
        ("股票基础信息", f"{BASE_URL}/api/cn/stock/600519/basic"),
        ("股票历史行情", f"{BASE_URL}/api/cn/stock/600519/history?start_date=2024-01-01&end_date=2024-01-31"),
        ("股票实时行情", f"{BASE_URL}/api/cn/stock/600519/realtime"),
        ("股票财务数据", f"{BASE_URL}/api/cn/stock/600519/financial?statement_type=balance_sheet&limit=3"),
        ("股票估值指标", f"{BASE_URL}/api/cn/stock/600519/valuation"),
    ]
    for name, url in tests:
        response = requests.get(url)
        print_response(name, response)

    # 3. 市场接口
    print("\n【市场接口】")
    response = requests.get(f"{BASE_URL}/api/cn/market/overview")
    print_response("市场概览", response)

    # 4. 宏观接口
    print("\n【宏观接口】")
    tests = [
        ("LPR利率", f"{BASE_URL}/api/cn/macro/lpr"),
        ("CPI数据", f"{BASE_URL}/api/cn/macro/cpi"),
        ("PPI数据", f"{BASE_URL}/api/cn/macro/ppi"),
        ("PMI数据", f"{BASE_URL}/api/cn/macro/pmi"),
        ("M2货币", f"{BASE_URL}/api/cn/macro/m2"),
    ]
    for name, url in tests:
        response = requests.get(url)
        print_response(name, response)

    # 5. 资金流向接口
    print("\n【资金流向接口】")
    tests = [
        ("个股资金流", f"{BASE_URL}/api/cn/flow/stock/600519"),
        ("指数资金流", f"{BASE_URL}/api/cn/flow/index/000001"),
        ("行业资金流", f"{BASE_URL}/api/cn/flow/industry"),
    ]
    for name, url in tests:
        response = requests.get(url)
        print_response(name, response)

    # 6. 行业板块接口
    print("\n【行业板块接口】")
    tests = [
        ("行业列表", f"{BASE_URL}/api/cn/board/industry/list"),
        ("指数列表", f"{BASE_URL}/api/cn/board/index/list"),
    ]
    for name, url in tests:
        response = requests.get(url)
        print_response(name, response)

    # 7. 特殊数据接口
    print("\n【特殊数据接口】")
    tests = [
        ("龙虎榜", f"{BASE_URL}/api/cn/special/dragon-tiger/600519"),
        ("大宗交易", f"{BASE_URL}/api/cn/special/block-deal/600519"),
        ("股权质押", f"{BASE_URL}/api/cn/special/equity-pledge/600519"),
    ]
    for name, url in tests:
        response = requests.get(url)
        print_response(name, response)

    # 8. 股东信息接口
    print("\n【股东信息接口】")
    tests = [
        ("股东信息", f"{BASE_URL}/api/cn/shareholder/600519"),
        ("股东人数", f"{BASE_URL}/api/cn/shareholder/600519/count"),
        ("高管增减持", f"{BASE_URL}/api/cn/shareholder/600519/executive"),
        ("大股东增减持", f"{BASE_URL}/api/cn/shareholder/600519/major"),
    ]
    for name, url in tests:
        response = requests.get(url)
        print_response(name, response)

    # 9. 分红配股接口
    print("\n【分红配股接口】")
    response = requests.get(f"{BASE_URL}/api/cn/dividend/600519")
    print_response("分红送配", response)

    print("\n" + "="*80)
    print("测试完成！")
    print("="*80)


if __name__ == "__main__":
    test_all_apis()
