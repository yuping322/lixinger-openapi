#!/usr/bin/env python3
"""测试provider方法"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lixinger_openapi.query import query_json
from lixinger_openapi.token import set_token
from datetime import datetime

# 设置token
set_token('ffad9101-8689-4b5d-bd79-763c58522a95', write_token=False)

TEST_SYMBOL = "600519"

print("=" * 80)
print("测试Provider方法")
print("=" * 80)

# 测试实时行情（使用最新K线）
print("\n1. 测试实时行情（最新K线）")
result = query_json("cn/company/candlestick", {
    "stockCode": TEST_SYMBOL,
    "type": "ex_rights",
    "period": "daily",
    "limit": 1
})
print(f"Code: {result.get('code')}")
print(f"Data: {result.get('data', [])[:1] if result.get('data') else 'None'}")

# 测试估值指标
print("\n2. 测试估值指标")
today = datetime.now().strftime("%Y-%m-%d")
result = query_json("cn/company/fundamental/non_financial", {
    "stockCodes": [TEST_SYMBOL],
    "metricsList": ["pe_ttm", "pb", "ps_ttm", "pcf_ttm", "mc"],
    "date": today,
    "limit": 1
})
print(f"Code: {result.get('code')}")
print(f"Data: {result.get('data', [])[:1] if result.get('data') else 'None'}")

# 测试不带日期的估值
print("\n3. 测试估值指标（不带日期）")
result = query_json("cn/company/fundamental/non_financial", {
    "stockCodes": [TEST_SYMBOL],
    "metricsList": ["pe_ttm", "pb", "ps_ttm", "pcf_ttm", "mc"]
})
print(f"Code: {result.get('code')}")
print(f"Data: {result.get('data', [])[:1] if result.get('data') else 'None'}")

print("\n" + "=" * 80)
