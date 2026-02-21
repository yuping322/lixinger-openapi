#!/usr/bin/env python3
"""最终测试 - 验证修复"""

import requests
import json

BASE_URL = "http://localhost:8000"
TEST_SYMBOL = "600519"

print("=" * 80)
print("最终测试 - 验证修复")
print("=" * 80)

# 测试实时行情
print("\n1. 测试实时行情接口")
url = f"{BASE_URL}/api/cn/stock/{TEST_SYMBOL}/realtime"
print(f"URL: {url}")
try:
    response = requests.get(url, timeout=10)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response Code: {data.get('code')}")
        print(f"Data Count: {data.get('meta', {}).get('count')}")
        if data.get('data'):
            print(f"Latest Data: {json.dumps(data['data'][0], ensure_ascii=False)[:200]}")
        if data.get('warnings'):
            print(f"Warnings: {data['warnings']}")
        print("✅ 成功")
    else:
        print(f"❌ 失败: {response.text[:200]}")
except Exception as e:
    print(f"❌ 异常: {e}")

# 测试估值指标
print("\n2. 测试估值指标接口")
url = f"{BASE_URL}/api/cn/stock/{TEST_SYMBOL}/valuation"
print(f"URL: {url}")
try:
    response = requests.get(url, timeout=10)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response Code: {data.get('code')}")
        print(f"Data Count: {data.get('meta', {}).get('count')}")
        if data.get('data'):
            print(f"Data: {json.dumps(data['data'], ensure_ascii=False)[:200]}")
        if data.get('warnings'):
            print(f"Warnings: {data['warnings']}")
        print("✅ 成功")
    else:
        print(f"❌ 失败: {response.text[:200]}")
except Exception as e:
    print(f"❌ 异常: {e}")

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)
