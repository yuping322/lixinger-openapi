#!/usr/bin/env python3
"""测试provider方法 - 修复后"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lixinger_openapi.query import query_json
from lixinger_openapi.token import set_token
from datetime import datetime, timedelta

# 设置token
set_token('ffad9101-8689-4b5d-bd79-763c58522a95', write_token=False)

TEST_SYMBOL = "600519"

print("=" * 80)
print("测试Provider方法 - 修复后")
print("=" * 80)

# 测试实时行情（使用最新K线，带日期）
print("\n1. 测试实时行情（最新K线，带日期）")
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
result = query_json("cn/company/candlestick", {
    "stockCode": TEST_SYMBOL,
    "type": "ex_rights",
    "period": "daily",
    "startDate": start_date,
    "endDate": end_date
})
print(f"Code: {result.get('code')}")
data = result.get('data', [])
if data:
    print(f"Data count: {len(data)}")
    print(f"Latest: {data[-1]}")
else:
    print("Data: None")

# 测试估值指标 - 尝试不同的endpoint
print("\n2. 测试估值指标 - cn/stock/fundamental")
result = query_json("cn/stock/fundamental", {
    "stockCodes": [TEST_SYMBOL],
    "metricsList": ["pe_ttm", "pb", "ps_ttm", "pcf_ttm", "mc"]
})
print(f"Code: {result.get('code')}")
print(f"Message: {result.get('msg', result.get('message', 'N/A'))}")
data = result.get('data', [])
if data:
    print(f"Data: {data[:1]}")
else:
    print("Data: None")

# 测试估值指标 - 尝试另一个endpoint
print("\n3. 测试估值指标 - cn/company/fundamental")
result = query_json("cn/company/fundamental", {
    "stockCodes": [TEST_SYMBOL],
    "metricsList": ["pe_ttm", "pb", "ps_ttm", "pcf_ttm", "mc"]
})
print(f"Code: {result.get('code')}")
print(f"Message: {result.get('msg', result.get('message', 'N/A'))}")
data = result.get('data', [])
if data:
    print(f"Data: {data[:1]}")
else:
    print("Data: None")

print("\n" + "=" * 80)
