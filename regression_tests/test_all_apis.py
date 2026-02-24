#!/usr/bin/env python3
"""
核心测试 1: 测试所有理杏仁API接口
直接验证所有API接口的可用性和数据返回

Version: 2.0.0
Updated: 2026-02-24
"""
import subprocess
import json
import sys
from pathlib import Path
from datetime import datetime

# Configuration
BASE_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = BASE_DIR.parent
QUERY_TOOL = PROJECT_ROOT / "skills/lixinger-data-query/scripts/query_tool.py"
RESULTS_DIR = BASE_DIR / "api_test_results"

# 所有API测试用例（基于理杏仁162个API）
API_TEST_CASES = [
    # ===== A股公司接口 (cn.company.*) =====
    {"name": "A股公司基本信息", "suffix": "cn.company", "params": {"stockCodes": ["600519", "000858"]}},
    {"name": "A股公司概况", "suffix": "cn.company.profile", "params": {"stockCodes": ["600519"]}},
    {"name": "A股K线数据", "suffix": "cn.company.candlestick", "params": {"stockCode": "600519", "type": "ex_rights", "startDate": "2024-01-01", "endDate": "2024-12-31"}},
    {"name": "A股分红数据", "suffix": "cn.company.dividend", "params": {"stockCode": "600519"}},
    {"name": "A股股东人数", "suffix": "cn.company.shareholders-num", "params": {"stockCode": "600519"}},
    {"name": "A股股本变动", "suffix": "cn.company.equity-change", "params": {"stockCode": "600519"}},
    {"name": "A股公告数据", "suffix": "cn.company.announcement", "params": {"stockCode": "600519", "limit": 10}},
    {"name": "A股大宗交易", "suffix": "cn.company.block-deal", "params": {"stockCode": "600519"}},
    {"name": "A股股权质押", "suffix": "cn.company.equity-pledge", "params": {"stockCode": "600519"}},
    {"name": "A股营收结构", "suffix": "cn.company.revenue-structure", "params": {"stockCode": "600519"}},
    {"name": "A股经营数据", "suffix": "cn.company.operation-data", "params": {"stockCode": "600519"}},
    {"name": "A股关联指数", "suffix": "cn.company.related-index", "params": {"stockCode": "600519"}},
    {"name": "A股关联行业", "suffix": "cn.company.related-industry", "params": {"stockCode": "600519"}},
    {"name": "A股监管信息", "suffix": "cn.company.regulatory-info", "params": {"stockCode": "600519"}},
    {"name": "A股股东信息", "suffix": "cn.company.shareholders", "params": {"stockCode": "600519"}},
    {"name": "A股客户供应商", "suffix": "cn.company.client-supplier", "params": {"stockCode": "600519"}},
    
    # ===== A股指数接口 (cn.index.*) =====
    {"name": "A股指数基本信息", "suffix": "cn.index", "params": {"indexCodes": ["000300", "000001"]}},
    {"name": "A股指数K线", "suffix": "cn.index.candlestick", "params": {"indexCode": "000300", "startDate": "2024-01-01", "endDate": "2024-12-31"}},
    {"name": "A股指数成分股", "suffix": "cn.index.constituents", "params": {"indexCode": "000300"}},
    {"name": "A股指数基本面", "suffix": "cn.index.fundamental", "params": {"indexCode": "000300"}},
    {"name": "A股指数财务", "suffix": "cn.index.financial", "params": {"indexCode": "000300"}},
    {"name": "A股指数估值", "suffix": "cn.index.valuation", "params": {"indexCode": "000300"}},
    
    # ===== A股行业接口 (cn.industry.*) =====
    {"name": "A股行业基本信息", "suffix": "cn.industry", "params": {"industryCodes": ["801010"]}},
    {"name": "A股行业K线", "suffix": "cn.industry.candlestick", "params": {"industryCode": "801010", "startDate": "2024-01-01", "endDate": "2024-12-31"}},
    {"name": "A股行业成分股", "suffix": "cn.industry.constituents", "params": {"industryCode": "801010"}},
    {"name": "A股行业基本面", "suffix": "cn.industry.fundamental", "params": {"industryCode": "801010"}},
    {"name": "A股行业财务", "suffix": "cn.industry.financial", "params": {"industryCode": "801010"}},
    {"name": "A股行业估值", "suffix": "cn.industry.valuation", "params": {"industryCode": "801010"}},
    
    # ===== A股基金接口 (cn.fund.*) =====
    {"name": "A股基金基本信息", "suffix": "cn.fund", "params": {"fundCodes": ["000001"]}},
    {"name": "A股基金K线", "suffix": "cn.fund.candlestick", "params": {"fundCode": "000001", "startDate": "2024-01-01", "endDate": "2024-12-31"}},
    {"name": "A股基金持仓", "suffix": "cn.fund.holdings", "params": {"fundCode": "000001"}},
    {"name": "A股基金净值", "suffix": "cn.fund.net-value", "params": {"fundCode": "000001"}},
    {"name": "A股基金分红", "suffix": "cn.fund.dividend", "params": {"fundCode": "000001"}},
    {"name": "A股基金评级", "suffix": "cn.fund.rating", "params": {"fundCode": "000001"}},
    
    # ===== 港股公司接口 (hk.company.*) =====
    {"name": "港股公司基本信息", "suffix": "hk.company", "params": {"stockCodes": ["00700", "09988"]}},
    {"name": "港股K线数据", "suffix": "hk.company.candlestick", "params": {"stockCode": "00700", "type": "ex_rights", "startDate": "2024-01-01", "endDate": "2024-12-31"}},
    {"name": "港股基本面", "suffix": "hk.company.fundamental", "params": {"stockCode": "00700"}},
    {"name": "港股财务数据", "suffix": "hk.company.financial", "params": {"stockCode": "00700"}},
    {"name": "港股股东信息", "suffix": "hk.company.shareholders", "params": {"stockCode": "00700"}},
    {"name": "港股公告", "suffix": "hk.company.announcement", "params": {"stockCode": "00700", "limit": 10}},
    
    # ===== 港股指数接口 (hk.index.*) =====
    {"name": "港股指数基本信息", "suffix": "hk.index", "params": {"indexCodes": ["HSI"]}},
    {"name": "港股指数K线", "suffix": "hk.index.candlestick", "params": {"indexCode": "HSI", "type": "ex_rights", "startDate": "2024-01-01", "endDate": "2024-12-31"}},
    {"name": "港股指数成分股", "suffix": "hk.index.constituents", "params": {"indexCode": "HSI"}},
    {"name": "港股指数基本面", "suffix": "hk.index.fundamental", "params": {"indexCode": "HSI"}},
    {"name": "港股指数财务", "suffix": "hk.index.financial", "params": {"indexCode": "HSI"}},
    {"name": "港股指数估值", "suffix": "hk.index.valuation", "params": {"indexCode": "HSI"}},
    
    # ===== 港股行业接口 (hk.industry.*) =====
    {"name": "港股行业基本信息", "suffix": "hk.industry", "params": {"industryCodes": ["HK001"]}},
    {"name": "港股行业K线", "suffix": "hk.industry.candlestick", "params": {"industryCode": "HK001", "type": "ex_rights", "startDate": "2024-01-01", "endDate": "2024-12-31"}},
    {"name": "港股行业成分股", "suffix": "hk.industry.constituents", "params": {"industryCode": "HK001"}},
    {"name": "港股行业基本面", "suffix": "hk.industry.fundamental", "params": {"industryCode": "HK001"}},
    
    # ===== 美股指数接口 (us.index.*) =====
    {"name": "美股指数基本信息", "suffix": "us.index", "params": {"indexCodes": ["SPX", "NDX"]}},
    {"name": "美股指数K线", "suffix": "us.index.candlestick", "params": {"indexCode": "SPX", "startDate": "2024-01-01", "endDate": "2024-12-31"}},
    {"name": "美股指数成分股", "suffix": "us.index.constituents", "params": {"indexCode": "SPX"}},
    {"name": "美股指数基本面", "suffix": "us.index.fundamental", "params": {"indexCode": "SPX"}},
    {"name": "美股指数财务", "suffix": "us.index.financial", "params": {"indexCode": "SPX"}},
    {"name": "美股指数回撤", "suffix": "us.index.drawdown", "params": {"indexCode": "SPX"}},
    {"name": "美股指数跟踪基金", "suffix": "us.index.tracking-fund", "params": {"indexCode": "SPX"}},
    
    # ===== 宏观数据接口 (macro.*) =====
    {"name": "宏观-投资者数据", "suffix": "macro.investor", "params": {}},
    {"name": "宏观-信用证券账户", "suffix": "macro.credit-security-account", "params": {}},
    {"name": "宏观-印花税", "suffix": "macro.stamp-duty", "params": {}},
    {"name": "宏观-价格指数", "suffix": "macro.price-index", "params": {}},
    {"name": "宏观-存款准备金率", "suffix": "macro.reserve-requirement-ratio", "params": {}},
    {"name": "宏观-货币供应量", "suffix": "macro.money-supply", "params": {}},
    {"name": "宏观-国债", "suffix": "macro.government-bond", "params": {}},
    {"name": "宏观-利率", "suffix": "macro.interest-rate", "params": {}},
    {"name": "宏观-社会融资", "suffix": "macro.social-financing", "params": {}},
    {"name": "宏观-人民币存贷款", "suffix": "macro.rmb-deposit-loan", "params": {}},
    {"name": "宏观-央行资产负债表", "suffix": "macro.central-bank-balance-sheet", "params": {}},
    {"name": "宏观-官方储备资产", "suffix": "macro.official-reserve-assets", "params": {}},
    {"name": "宏观-外汇资产", "suffix": "macro.foreign-assets", "params": {}},
    {"name": "宏观-国内债券", "suffix": "macro.domestic-bonds", "params": {}},
    {"name": "宏观-杠杆率", "suffix": "macro.leverage-ratio", "params": {}},
    {"name": "宏观-人口", "suffix": "macro.population", "params": {}},
    {"name": "宏观-GDP", "suffix": "macro.gdp", "params": {}},
    {"name": "宏观-失业率", "suffix": "macro.unemployment-rate", "params": {}},
    {"name": "宏观-对外贸易", "suffix": "macro.foreign-trade", "params": {}},
    {"name": "宏观-国际收支", "suffix": "macro.balance-of-payments", "params": {}},
    {"name": "宏观-固定资产投资", "suffix": "macro.fixed-asset-investment", "params": {}},
    {"name": "宏观-社会消费品零售", "suffix": "macro.social-consumer-retail", "params": {}},
    {"name": "宏观-交通运输", "suffix": "macro.transportation", "params": {}},
    {"name": "宏观-房地产", "suffix": "macro.real-estate", "params": {}},
    {"name": "宏观-石油", "suffix": "macro.oil", "params": {}},
    {"name": "宏观-能源", "suffix": "macro.energy", "params": {}},
    {"name": "宏观-大宗商品", "suffix": "macro.commodities", "params": {}},
    {"name": "宏观-美元指数", "suffix": "macro.dollar-index", "params": {}},
    {"name": "宏观-人民币指数", "suffix": "macro.rmb-index", "params": {}},
    {"name": "宏观-汇率", "suffix": "macro.currency-exchange-rate", "params": {}},
    {"name": "宏观-工业", "suffix": "macro.industrial", "params": {}},
]

def run_api_test(test_case):
    """运行单个API测试"""
    name = test_case["name"]
    suffix = test_case["suffix"]
    params = test_case["params"]
    
    print(f"\n{'='*80}")
    print(f"测试: {name}")
    print(f"接口: {suffix}")
    print(f"参数: {json.dumps(params, ensure_ascii=False)}")
    print('='*80)
    
    # 构建命令
    cmd = [
        "python3",
        str(QUERY_TOOL),
        "--suffix", suffix,
        "--params", json.dumps(params, ensure_ascii=False),
        "--format", "json"
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(PROJECT_ROOT)
        )
        
        # 解析结果
        if result.returncode == 0:
            try:
                output = json.loads(result.stdout)
                if output.get("code") == 1:
                    data = output.get("data", [])
                    data_count = len(data) if isinstance(data, list) else 1
                    print(f"✅ 成功 - 返回 {data_count} 条数据")
                    return {"status": "success", "data_count": data_count}
                else:
                    error_msg = output.get("error", {}).get("message", "Unknown error")
                    print(f"❌ API错误 - {error_msg}")
                    return {"status": "api_error", "message": error_msg}
            except json.JSONDecodeError:
                print(f"❌ JSON解析失败")
                return {"status": "json_error", "message": "Invalid JSON"}
        else:
            print(f"❌ 执行失败 - {result.stderr[:200]}")
            return {"status": "exec_error", "message": result.stderr[:200]}
            
    except subprocess.TimeoutExpired:
        print(f"⏱️  超时")
        return {"status": "timeout"}
    except Exception as e:
        print(f"💥 异常 - {str(e)}")
        return {"status": "exception", "message": str(e)}

def main():
    """主测试流程"""
    print("="*80)
    print("核心测试 1: 理杏仁API接口全量测试")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"测试接口数: {len(API_TEST_CASES)}")
    print("="*80)
    
    RESULTS_DIR.mkdir(exist_ok=True)
    
    # 执行所有测试
    results = {
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "total": len(API_TEST_CASES),
        "success": 0,
        "failed": 0,
        "details": []
    }
    
    for i, test_case in enumerate(API_TEST_CASES, 1):
        print(f"\n[{i}/{len(API_TEST_CASES)}]", end=" ")
        
        test_result = run_api_test(test_case)
        
        detail = {
            "name": test_case["name"],
            "suffix": test_case["suffix"],
            "status": test_result["status"],
            **test_result
        }
        results["details"].append(detail)
        
        if test_result["status"] == "success":
            results["success"] += 1
        else:
            results["failed"] += 1
    
    # 保存结果
    summary_file = RESULTS_DIR / f"api_test_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # 打印总结
    print(f"\n{'='*80}")
    print("测试总结")
    print('='*80)
    print(f"总接口数: {results['total']}")
    print(f"✅ 成功: {results['success']} ({results['success']/results['total']*100:.1f}%)")
    print(f"❌ 失败: {results['failed']} ({results['failed']/results['total']*100:.1f}%)")
    print(f"\n📊 详细结果: {summary_file}")
    print('='*80)
    
    sys.exit(0 if results['failed'] == 0 else 1)

if __name__ == "__main__":
    main()
