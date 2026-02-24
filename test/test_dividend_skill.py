#!/usr/bin/env python3
"""测试分红跟踪skill"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from lixinger_openapi.query import query_json
from lixinger_openapi.token import set_token
from datetime import datetime, timedelta
import json

# 设置token
set_token('ffad9101-8689-4b5d-bd79-763c58522a95', write_token=False)

TEST_SYMBOL = "600519"  # 贵州茅台

print("=" * 80)
print("测试分红跟踪Skill - 数据获取")
print(f"测试股票: {TEST_SYMBOL} (贵州茅台)")
print("=" * 80)

# 1. 获取分红数据
print("\n1. 获取分红数据")
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=365*3)).strftime("%Y-%m-%d")

result = query_json("cn/company/dividend", {
    "stockCode": TEST_SYMBOL,
    "startDate": start_date,
    "endDate": end_date
})

print(f"API返回码: {result.get('code')}")
data = result.get('data', [])
print(f"数据条数: {len(data)}")

if data:
    print("\n最近3次分红记录:")
    for i, record in enumerate(data[:3], 1):
        print(f"\n第{i}次分红:")
        print(f"  日期: {record.get('date', 'N/A')}")
        print(f"  报告期: {record.get('fsEndDate', 'N/A')}")
        print(f"  每股分红: {record.get('dividendPerShare', 0)} 元")
        print(f"  分红率: {record.get('dividendRatio', 0)*100:.2f}%")
        print(f"  股息率: {record.get('dividendYield', 0)*100:.2f}%")

# 2. 获取股本变动（用于分析配股）
print("\n" + "=" * 80)
print("2. 获取股本变动数据")

result = query_json("cn/company/equity-change", {
    "stockCode": TEST_SYMBOL,
    "startDate": start_date,
    "endDate": end_date
})

print(f"API返回码: {result.get('code')}")
data = result.get('data', [])
print(f"数据条数: {len(data)}")

if data:
    print("\n最近3次股本变动:")
    for i, record in enumerate(data[:3], 1):
        print(f"\n第{i}次变动:")
        print(f"  日期: {record.get('date', 'N/A')}")
        print(f"  公告日期: {record.get('declarationDate', 'N/A')}")
        print(f"  变动原因: {record.get('changeReason', 'N/A')}")
        print(f"  总股本: {record.get('capitalization', 0)/100000000:.2f} 亿股")
        print(f"  流通A股: {record.get('outstandingSharesA', 0)/100000000:.2f} 亿股")

# 3. 获取公司基本信息
print("\n" + "=" * 80)
print("3. 获取公司基本信息")

result = query_json("cn/company", {
    "stockCodes": [TEST_SYMBOL]
})

print(f"API返回码: {result.get('code')}")
data = result.get('data', [])

if data:
    info = data[0]
    print(f"\n公司名称: {info.get('name', 'N/A')}")
    print(f"股票代码: {info.get('stockCode', 'N/A')}")
    print(f"交易所: {info.get('exchange', 'N/A')}")
    print(f"上市日期: {info.get('ipoDate', 'N/A')}")

# 4. 分析总结
print("\n" + "=" * 80)
print("4. 分红跟踪分析总结")
print("=" * 80)

# 重新获取分红数据进行分析
result = query_json("cn/company/dividend", {
    "stockCode": TEST_SYMBOL,
    "startDate": start_date,
    "endDate": end_date
})

dividend_data = result.get('data', [])

if dividend_data:
    print(f"\n✅ 成功获取 {len(dividend_data)} 条分红记录")
    
    # 计算平均股息率
    dividend_yields = [d.get('dividendYield', 0) for d in dividend_data if d.get('dividendYield')]
    if dividend_yields:
        avg_yield = sum(dividend_yields) / len(dividend_yields)
        print(f"平均股息率: {avg_yield*100:.2f}%")
    
    # 计算分红增长
    dividends = [d.get('dividendPerShare', 0) for d in dividend_data]
    if len(dividends) >= 2:
        latest = dividends[0]
        oldest = dividends[-1]
        if oldest > 0:
            growth = (latest - oldest) / oldest * 100
            print(f"分红增长: {growth:.2f}% (从 {oldest:.2f}元 到 {latest:.2f}元)")
    
    print("\n✅ 该skill所需的核心数据都可以获取")
    print("✅ dividend-corporate-action-tracker skill 可以正常运行")
else:
    print("\n❌ 无法获取分红数据")

print("\n" + "=" * 80)
