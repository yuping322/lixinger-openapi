#!/usr/bin/env python3
"""测试脚本 - 测试所有 API 接口"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"


def print_response(name: str, response: requests.Response):
    """打印响应结果"""
    print(f"\n{'='*80}")
    print(f"测试: {name}")
    print(f"{'='*80}")
    print(f"状态码: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"响应码: {data['code']}")
        print(f"消息: {data['message']}")
        print(f"数据量: {data['meta']['count']}")
        print(f"数据源: {data['meta']['source']}")

        if data['data']:
            print(f"\n第一条数据示例:")
            print(json.dumps(data['data'][0], indent=2, ensure_ascii=False))
    else:
        print(f"错误: {response.text}")


def test_health():
    """测试健康检查"""
    response = requests.get(f"{BASE_URL}/health")
    print_response("健康检查", response)
    return response.status_code == 200


def test_stock_basic():
    """测试股票基础信息"""
    response = requests.get(f"{BASE_URL}/api/cn/stock/600519/basic")
    print_response("股票基础信息 (600519 贵州茅台)", response)
    return response.status_code == 200


def test_stock_history():
    """测试股票历史行情"""
    response = requests.get(
        f"{BASE_URL}/api/cn/stock/600519/history",
        params={
            "start_date": "2024-01-01",
            "end_date": "2024-01-31",
            "period": "daily",
            "adjust": "ex_rights"
        }
    )
    print_response("股票历史行情 (600519)", response)
    return response.status_code == 200


def test_stock_realtime():
    """测试股票实时行情"""
    response = requests.get(f"{BASE_URL}/api/cn/stock/600519/realtime")
    print_response("股票实时行情 (600519)", response)
    return response.status_code == 200


def test_stock_financial():
    """测试股票财务数据"""
    response = requests.get(
        f"{BASE_URL}/api/cn/stock/600519/financial",
        params={"statement_type": "balance_sheet", "limit": 3}
    )
    print_response("股票财务数据 - 资产负债表 (600519)", response)
    return response.status_code == 200


def test_stock_valuation():
    """测试股票估值指标"""
    response = requests.get(f"{BASE_URL}/api/cn/stock/600519/valuation")
    print_response("股票估值指标 (600519)", response)
    return response.status_code == 200


def test_market_overview():
    """测试市场概览"""
    response = requests.get(f"{BASE_URL}/api/cn/market/overview")
    print_response("市场概览", response)
    return response.status_code == 200


def test_macro_lpr():
    """测试 LPR 数据"""
    response = requests.get(f"{BASE_URL}/api/cn/macro/lpr")
    print_response("LPR 利率", response)
    return response.status_code == 200


def test_macro_cpi():
    """测试 CPI 数据"""
    response = requests.get(f"{BASE_URL}/api/cn/macro/cpi")
    print_response("CPI 数据", response)
    return response.status_code == 200


def test_macro_ppi():
    """测试 PPI 数据"""
    response = requests.get(f"{BASE_URL}/api/cn/macro/ppi")
    print_response("PPI 数据", response)
    return response.status_code == 200


def test_macro_pmi():
    """测试 PMI 数据"""
    response = requests.get(f"{BASE_URL}/api/cn/macro/pmi")
    print_response("PMI 数据", response)
    return response.status_code == 200


def test_macro_m2():
    """测试 M2 数据"""
    response = requests.get(f"{BASE_URL}/api/cn/macro/m2")
    print_response("M2 货币供应", response)
    return response.status_code == 200


def main():
    """运行所有测试"""
    print("\n" + "="*80)
    print("Findata Service API 测试")
    print("="*80)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"服务地址: {BASE_URL}")
    print("="*80)

    tests = [
        ("健康检查", test_health),
        ("股票基础信息", test_stock_basic),
        ("股票历史行情", test_stock_history),
        ("股票实时行情", test_stock_realtime),
        ("股票财务数据", test_stock_financial),
        ("股票估值指标", test_stock_valuation),
        ("市场概览", test_market_overview),
        ("LPR利率", test_macro_lpr),
        ("CPI数据", test_macro_cpi),
        ("PPI数据", test_macro_ppi),
        ("PMI数据", test_macro_pmi),
        ("M2货币供应", test_macro_m2),
    ]

    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, "✓ 成功" if success else "✗ 失败"))
        except Exception as e:
            print(f"\n测试 {name} 时发生错误: {e}")
            results.append((name, f"✗ 错误: {str(e)[:50]}"))

    # 打印总结
    print("\n" + "="*80)
    print("测试总结")
    print("="*80)
    for name, result in results:
        print(f"{name:30s} {result}")

    success_count = sum(1 for _, r in results if "成功" in r)
    print(f"\n总计: {success_count}/{len(tests)} 通过")


if __name__ == "__main__":
    main()
