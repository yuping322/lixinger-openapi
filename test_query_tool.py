#!/usr/bin/env python3
"""
测试 query_tool.py 是否能正常工作于所有理杏仁API接口
"""

import subprocess
import json
import sys
from datetime import datetime, timedelta

# 测试用例配置
TEST_CASES = [
    # ===== A股市场接口 =====
    {
        "name": "公司基本信息",
        "suffix": "cn/company",
        "params": {"stockCodes": ["600519"]},
        "expected_fields": ["stockCode", "name"]
    },
    {
        "name": "K线数据",
        "suffix": "cn/company/candlestick",
        "params": {
            "stockCode": "600519",
            "type": "ex_rights",
            "startDate": "2026-01-01",
            "endDate": "2026-02-21"
        },
        "expected_fields": ["date", "open", "close", "high", "low", "volume"]
    },
    {
        "name": "分红数据",
        "suffix": "cn/company/dividend",
        "params": {
            "stockCode": "600519",
            "startDate": "2020-01-01",
            "endDate": "2026-02-21"
        },
        "expected_fields": ["date", "dividendPerShare"]
    },
    {
        "name": "股东人数",
        "suffix": "cn/company/shareholders-num",
        "params": {
            "stockCode": "600519",
            "startDate": "2020-01-01",
            "endDate": "2026-02-21"
        },
        "expected_fields": ["date", "num"]
    },
    {
        "name": "股本变动",
        "suffix": "cn/company/equity-change",
        "params": {
            "stockCode": "600519",
            "startDate": "2020-01-01",
            "endDate": "2026-02-21"
        },
        "expected_fields": ["date", "changeReason"]
    },
    {
        "name": "公告",
        "suffix": "cn/company/announcement",
        "params": {
            "stockCode": "600519",
            "limit": 10
        },
        "expected_fields": ["date", "linkText"]
    },
    {
        "name": "财务报表（预期失败）",
        "suffix": "cn/company/fs",
        "params": {
            "stockCodes": ["600519"],
            "fsTableType": "bank"
        },
        "expected_fields": [],
        "expect_fail": True
    },
    {
        "name": "热度数据（预期失败）",
        "suffix": "cn/company/hot-data",
        "params": {"stockCodes": ["600519"]},
        "expected_fields": [],
        "expect_fail": True
    },
    {
        "name": "资金流向（预期失败）",
        "suffix": "cn/company/fund-flow",
        "params": {"stockCodes": ["600519"]},
        "expected_fields": [],
        "expect_fail": True
    },
    {
        "name": "估值指标（预期失败）",
        "suffix": "cn/company/valuation",
        "params": {"stockCodes": ["600519"]},
        "expected_fields": [],
        "expect_fail": True
    },
    
    # ===== 指数接口 =====
    {
        "name": "指数基本信息",
        "suffix": "cn/index",
        "params": {"indexCodes": ["000001"]},
        "expected_fields": ["indexCode", "name"]
    },
    {
        "name": "指数K线",
        "suffix": "cn/index/candlestick",
        "params": {
            "indexCode": "000001",
            "startDate": "2026-01-01",
            "endDate": "2026-02-21"
        },
        "expected_fields": ["date", "close"]
    },
    
    # ===== 行业接口 =====
    {
        "name": "行业基本信息",
        "suffix": "cn/industry",
        "params": {"industryCodes": ["801010"]},
        "expected_fields": ["industryCode", "industryName"]
    },
    
    # ===== 美股接口 =====
    {
        "name": "美股公司信息（预期失败）",
        "suffix": "us/company",
        "params": {"stockCodes": ["AAPL"]},
        "expected_fields": ["stockCode", "name"],
        "expect_fail": True
    },
    {
        "name": "美股K线（预期失败）",
        "suffix": "us/company/candlestick",
        "params": {
            "stockCode": "AAPL",
            "startDate": "2026-01-01",
            "endDate": "2026-02-21"
        },
        "expected_fields": ["date", "close"],
        "expect_fail": True
    },
    
    # ===== 港股接口 =====
    {
        "name": "港股公司信息",
        "suffix": "hk/company",
        "params": {"stockCodes": ["00700"]},
        "expected_fields": ["stockCode", "name"]
    },
    {
        "name": "港股K线",
        "suffix": "hk/company/candlestick",
        "params": {
            "stockCode": "00700",
            "type": "ex_rights",  # 必需参数
            "startDate": "2026-01-01",
            "endDate": "2026-02-21"
        },
        "expected_fields": ["date", "close"]
    },
]

def run_query_tool(suffix, params, format_type="json"):
    """运行query_tool.py"""
    import os
    
    # 设置PYTHONPATH
    env = os.environ.copy()
    env['PYTHONPATH'] = '/Users/fengzhi/Downloads/git/lixinger-openapi'
    
    cmd = [
        "python3",
        "skills/lixinger-data-query/scripts/query_tool.py",
        "--suffix", suffix,
        "--params", json.dumps(params),
        "--format", format_type,
        "--no-cache"  # 禁用缓存以获取最新数据
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            env=env
        )
        return result
    except subprocess.TimeoutExpired:
        return None
    except Exception as e:
        print(f"执行错误: {e}")
        return None

def test_query_tool():
    """测试所有接口"""
    print("=" * 80)
    print("测试 query_tool.py 接口兼容性")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()
    
    results = {
        "total": len(TEST_CASES),
        "passed": 0,
        "failed": 0,
        "expected_fail": 0,
        "details": []
    }
    
    for i, test_case in enumerate(TEST_CASES, 1):
        name = test_case["name"]
        suffix = test_case["suffix"]
        params = test_case["params"]
        expected_fields = test_case.get("expected_fields", [])
        expect_fail = test_case.get("expect_fail", False)
        
        print(f"[{i}/{len(TEST_CASES)}] 测试: {name}")
        print(f"    接口: {suffix}")
        print(f"    参数: {json.dumps(params, ensure_ascii=False)}")
        
        # 运行测试
        result = run_query_tool(suffix, params)
        
        if result is None:
            print(f"    ❌ 超时或执行失败")
            results["failed"] += 1
            results["details"].append({
                "name": name,
                "suffix": suffix,
                "status": "timeout",
                "message": "执行超时"
            })
            print()
            continue
        
        # 检查返回码
        if result.returncode != 0:
            if expect_fail:
                print(f"    ✅ 预期失败（符合预期）")
                print(f"    错误信息: {result.stderr.strip()}")
                results["expected_fail"] += 1
                results["details"].append({
                    "name": name,
                    "suffix": suffix,
                    "status": "expected_fail",
                    "message": result.stderr.strip()
                })
            else:
                print(f"    ❌ 执行失败")
                print(f"    错误信息: {result.stderr.strip()}")
                results["failed"] += 1
                results["details"].append({
                    "name": name,
                    "suffix": suffix,
                    "status": "failed",
                    "message": result.stderr.strip()
                })
            print()
            continue
        
        # 解析JSON输出
        try:
            output = json.loads(result.stdout)
            
            # 检查API返回码
            if output.get("code") == 1:
                # 成功
                data = output.get("data", [])
                print(f"    ✅ 成功")
                print(f"    返回数据: {len(data)} 条记录")
                
                # 检查字段
                if expected_fields and data:
                    first_item = data[0] if isinstance(data, list) else data
                    missing_fields = [f for f in expected_fields if f not in first_item]
                    if missing_fields:
                        print(f"    ⚠️  缺少字段: {', '.join(missing_fields)}")
                    else:
                        print(f"    ✅ 字段完整")
                
                results["passed"] += 1
                results["details"].append({
                    "name": name,
                    "suffix": suffix,
                    "status": "success",
                    "data_count": len(data) if isinstance(data, list) else 1
                })
                
            elif output.get("code") == 0:
                # API返回错误
                if expect_fail:
                    print(f"    ✅ 预期失败（符合预期）")
                    print(f"    API错误: {output.get('error', {}).get('message', 'Unknown')}")
                    results["expected_fail"] += 1
                    results["details"].append({
                        "name": name,
                        "suffix": suffix,
                        "status": "expected_fail",
                        "message": output.get('error', {}).get('message', 'Unknown')
                    })
                else:
                    print(f"    ⚠️  API返回错误")
                    print(f"    错误信息: {output.get('error', {}).get('message', 'Unknown')}")
                    results["failed"] += 1
                    results["details"].append({
                        "name": name,
                        "suffix": suffix,
                        "status": "api_error",
                        "message": output.get('error', {}).get('message', 'Unknown')
                    })
            else:
                print(f"    ❌ 未知返回码: {output.get('code')}")
                results["failed"] += 1
                results["details"].append({
                    "name": name,
                    "suffix": suffix,
                    "status": "unknown_code",
                    "code": output.get('code')
                })
                
        except json.JSONDecodeError as e:
            print(f"    ❌ JSON解析失败")
            print(f"    错误: {e}")
            print(f"    输出: {result.stdout[:200]}")
            results["failed"] += 1
            results["details"].append({
                "name": name,
                "suffix": suffix,
                "status": "json_error",
                "message": str(e)
            })
        
        print()
    
    # 输出总结
    print("=" * 80)
    print("测试总结")
    print("=" * 80)
    print(f"总测试数: {results['total']}")
    print(f"✅ 成功: {results['passed']}")
    print(f"✅ 预期失败: {results['expected_fail']}")
    print(f"❌ 失败: {results['failed']}")
    print(f"成功率: {(results['passed'] / results['total'] * 100):.1f}%")
    print()
    
    # 按状态分类显示
    print("=" * 80)
    print("详细结果")
    print("=" * 80)
    
    # 成功的接口
    success_cases = [d for d in results["details"] if d["status"] == "success"]
    if success_cases:
        print(f"\n✅ 成功的接口 ({len(success_cases)}个):")
        for detail in success_cases:
            print(f"  - {detail['name']}: {detail['suffix']}")
            if "data_count" in detail:
                print(f"    返回 {detail['data_count']} 条数据")
    
    # 预期失败的接口
    expected_fail_cases = [d for d in results["details"] if d["status"] == "expected_fail"]
    if expected_fail_cases:
        print(f"\n✅ 预期失败的接口 ({len(expected_fail_cases)}个):")
        for detail in expected_fail_cases:
            print(f"  - {detail['name']}: {detail['suffix']}")
            print(f"    原因: {detail.get('message', 'Unknown')}")
    
    # 失败的接口
    failed_cases = [d for d in results["details"] if d["status"] not in ["success", "expected_fail"]]
    if failed_cases:
        print(f"\n❌ 失败的接口 ({len(failed_cases)}个):")
        for detail in failed_cases:
            print(f"  - {detail['name']}: {detail['suffix']}")
            print(f"    状态: {detail['status']}")
            if "message" in detail:
                print(f"    原因: {detail['message']}")
    
    print()
    print("=" * 80)
    
    # 保存结果
    with open("query_tool_test_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("详细结果已保存到: query_tool_test_results.json")
    
    return results

if __name__ == "__main__":
    results = test_query_tool()
    
    # 如果有失败的测试（不包括预期失败），返回非0退出码
    if results["failed"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)
