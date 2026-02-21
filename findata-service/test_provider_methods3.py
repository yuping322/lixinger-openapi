#!/usr/bin/env python3
"""测试provider方法 - 查看完整返回"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lixinger_openapi.query import query_json
from lixinger_openapi.token import set_token
from datetime import datetime, timedelta
import json

# 设置token
set_token('ffad9101-8689-4b5d-bd79-763c58522a95', write_token=False)

TEST_SYMBOL = "600519"

print("=" * 80)
print("测试Provider方法 - 查看完整返回")
print("=" * 80)

# 测试实时行情（使用最新K线，带日期）
print("\n1. 测试实时行情（最新K线，带日期）")
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
print(f"参数: stockCode={TEST_SYMBOL}, startDate={start_date}, endDate={end_date}")
result = query_json("cn/company/candlestick", {
    "stockCode": TEST_SYMBOL,
    "type": "ex_rights",
    "period": "daily",
    "startDate": start_date,
    "endDate": end_date
})
print(f"完整返回: {json.dumps(result, ensure_ascii=False, indent=2)}")

print("\n" + "=" * 80)
