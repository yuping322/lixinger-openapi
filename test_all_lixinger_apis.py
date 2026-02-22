#!/usr/bin/env python3
"""
测试所有理杏仁API接口 (113个)
基于 skills/lixinger-data-query/resources/api_catalog.csv
"""

import csv
import json
import sys
from datetime import datetime, timedelta
from lixinger_openapi.query import query_json
from lixinger_openapi.token import set_token

# 设置token
set_token('ffad9101-8689-4b5d-bd79-763c58522a95', write_token=False)

# 测试参数配置
TEST_PARAMS = {
    # A股公司接口
    "cn/company": {
        "basic-info": {"stockCodes": ["600519"]},
        "profile": {"stockCodes": ["600519"]},
        "share-change": {"stockCode": "600519", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "k-line": {"stockCode": "600519", "type": "ex_rights", "startDate": "2026-01-01", "endDate": "2026-02-21"},
        "shareholders-count": {"stockCode": "600519", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "executive-shareholding": {"stockCode": "600519", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "major-shareholder-change": {"stockCode": "600519", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "trading-abnormal": {"stockCode": "600519", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "block-trade": {"stockCode": "600519", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "equity-pledge": {"stockCode": "600519", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "revenue-structure": {"stockCode": "600519", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "operation-data": {"stockCode": "600519", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "related-index": {"stockCode": "600519"},
        "related-industry": {"stockCode": "600519"},
        "announcement": {"stockCode": "600519", "limit": 10},
        "regulatory-info": {"stockCode": "600519", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "shareholders": {"stockCode": "600519", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "dividend-allotment": {"stockCode": "600519", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "client-supplier": {"stockCode": "600519", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "fundamental/other_finance": {"stockCodes": ["600519"]},
        "financial-statement": {"stockCodes": ["600519"]},
        "hot-data": {"stockCodes": ["600519"]},
        "fund-flow": {"stockCodes": ["600519"]},
    },
    # A股指数接口
    "cn/index": {
        "basic-info": {"indexCodes": ["000001"]},
        "k-line": {"indexCode": "000001", "type": "ex_rights", "startDate": "2026-01-01", "endDate": "2026-02-21"},
        "constituents": {"indexCode": "000001"},
        "fundamental": {"indexCode": "000001", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "financial": {"indexCode": "000001", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "valuation": {"indexCode": "000001", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "hot-data": {"indexCodes": ["000001"]},
        "fund-flow": {"indexCodes": ["000001"]},
    },
    # A股行业接口
    "cn/industry": {
        "basic-info": {"industryCodes": ["801010"]},
        "k-line": {"industryCode": "801010", "type": "ex_rights", "startDate": "2026-01-01", "endDate": "2026-02-21"},
        "constituents": {"industryCode": "801010"},
        "fundamental": {"industryCode": "801010", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "financial": {"industryCode": "801010", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "valuation": {"industryCode": "801010", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "hot-data": {"industryCodes": ["801010"]},
        "fund-flow": {"industryCodes": ["801010"]},
    },
    # A股基金接口
    "cn/fund": {
        "basic-info": {"fundCodes": ["000001"]},
        "k-line": {"fundCode": "000001", "startDate": "2026-01-01", "endDate": "2026-02-21"},
        "holdings": {"fundCode": "000001"},
        "net-value": {"fundCode": "000001", "startDate": "2026-01-01", "endDate": "2026-02-21"},
        "dividend": {"fundCode": "000001", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "rating": {"fundCode": "000001"},
        "hot-data": {"fundCodes": ["000001"]},
    },
    # 港股公司接口
    "hk/company": {
        "basic-info": {"stockCodes": ["00700"]},
        "k-line": {"stockCode": "00700", "type": "ex_rights", "startDate": "2026-01-01", "endDate": "2026-02-21"},
        "fundamental": {"stockCode": "00700", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "financial": {"stockCode": "00700", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "shareholders": {"stockCode": "00700", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "announcement": {"stockCode": "00700", "limit": 10},
        "fund-flow": {"stockCodes": ["00700"]},
        "hot-data": {"stockCodes": ["00700"]},
    },
    # 港股指数接口
    "hk/index": {
        "basic-info": {"indexCodes": ["HSI"]},
        "k-line": {"indexCode": "HSI", "type": "ex_rights", "startDate": "2026-01-01", "endDate": "2026-02-21"},
        "constituents": {"indexCode": "HSI"},
        "fundamental": {"indexCode": "HSI", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "financial": {"indexCode": "HSI", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "valuation": {"indexCode": "HSI", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "hot-data": {"indexCodes": ["HSI"]},
        "fund-flow": {"indexCodes": ["HSI"]},
    },
    # 港股行业接口
    "hk/industry": {
        "basic-info": {"industryCodes": ["HK001"]},
        "k-line": {"industryCode": "HK001", "type": "ex_rights", "startDate": "2026-01-01", "endDate": "2026-02-21"},
        "constituents": {"industryCode": "HK001"},
        "fundamental": {"industryCode": "HK001", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "financial": {"industryCode": "HK001", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "valuation": {"industryCode": "HK001", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "hot-data": {"industryCodes": ["HK001"]},
        "fund-flow": {"industryCodes": ["HK001"]},
    },
    # 美股指数接口
    "us/index": {
        "basic-info": {"indexCodes": ["SPX"]},
        "k-line": {"indexCode": "SPX", "startDate": "2026-01-01", "endDate": "2026-02-21"},
        "constituents": {"indexCode": "SPX"},
        "drawdown": {"indexCode": "SPX", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "tracking-fund": {"indexCode": "SPX"},
        "fundamental": {"indexCode": "SPX", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "financial": {"indexCode": "SPX", "startDate": "2020-01-01", "endDate": "2026-02-21"},
        "hot-data": {"indexCodes": ["SPX"]},
        "fund-flow": {"indexCodes": ["SPX"]},
    },
    # 宏观接口 (不需要股票代码)
    "macro": {
        "investor": {},
        "credit-security-account": {},
        "stamp-duty": {},
        "price-index": {},
        "reserve-requirement-ratio": {},
        "money-supply": {},
        "government-bond": {},
        "interest-rate": {},
        "social-financing": {},
        "rmb-deposit-loan": {},
        "central-bank-balance-sheet": {},
        "official-reserve-assets": {},
        "foreign-assets": {},
        "domestic-bonds": {},
        "leverage-ratio": {},
        "population": {},
        "gdp": {},
        "unemployment-rate": {},
        "foreign-trade": {},
        "balance-of-payments": {},
        "fixed-asset-investment": {},
        "social-consumer-retail": {},
        "transportation": {},
        "real-estate": {},
        "oil": {},
        "energy": {},
        "commodities": {},
        "dollar-index": {},
        "rmb-index": {},
        "exchange-rate": {},
        "industrial": {},
    }
}

def get_test_params(url_suffix):
    """根据URL后缀获取测试参数"""
    parts = url_suffix.split('/')
    
    if len(parts) >= 2:
        category = f"{parts[0]}/{parts[1]}"
        endpoint = '/'.join(parts[2:]) if len(parts) > 2 else parts[1]
        
        if category in TEST_PARAMS and endpoint in TEST_PARAMS[category]:
            return TEST_PARAMS[category][endpoint]
    
    # 默认参数
    return {}

def test_api(url_suffix, description, max_retries=3):
    """测试单个API，带重试机制"""
    params = get_test_params(url_suffix)
    
    for attempt in range(max_retries):
        try:
            result = query_json(url_suffix, params)
            
            if result.get('code') == 1:
                data = result.get('data', [])
                data_count = len(data) if isinstance(data, list) else 1
                return {
                    'status': 'success',
                    'data_count': data_count,
                    'message': 'OK'
                }
            elif result.get('code') == 0:
                error_msg = result.get('error', {}).get('message', 'Unknown error')
                
                # 判断是否是预期的失败
                if 'api is not found' in error_msg.lower() or 'api was not found' in error_msg.lower():
                    return {
                        'status': 'not_found',
                        'message': error_msg
                    }
                else:
                    return {
                        'status': 'error',
                        'message': error_msg
                    }
            else:
                return {
                    'status': 'unknown',
                    'message': f"Unknown code: {result.get('code')}"
                }
        except Exception as e:
            error_msg = str(e)
            
            # 如果是SSL错误或连接错误，重试
            if 'SSL' in error_msg or 'Connection' in error_msg or 'Max retries' in error_msg:
                if attempt < max_retries - 1:
                    import time
                    time.sleep(1)  # 等待1秒后重试
                    continue
            
            # 最后一次尝试失败，返回异常
            return {
                'status': 'exception',
                'message': error_msg
            }
    
    # 所有重试都失败
    return {
        'status': 'exception',
        'message': f'Failed after {max_retries} retries'
    }

def main():
    print("=" * 100)
    print("理杏仁API全接口测试 (113个)")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 100)
    print()
    
    # 读取API目录
    apis = []
    with open('skills/lixinger-data-query/resources/api_catalog.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            apis.append(row)
    
    print(f"共发现 {len(apis)} 个API接口")
    print()
    
    # 统计结果
    results = {
        'total': len(apis),
        'success': 0,
        'not_found': 0,
        'error': 0,
        'exception': 0,
        'unknown': 0,
        'details': []
    }
    
    # 按类别分组
    categories = {}
    for api in apis:
        category = api['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(api)
    
    # 测试每个API
    for category_name, category_apis in sorted(categories.items()):
        print(f"\n{'=' * 100}")
        print(f"测试类别: {category_name} ({len(category_apis)}个接口)")
        print('=' * 100)
        
        for i, api in enumerate(category_apis, 1):
            url_suffix = api['url_suffix']
            description = api['description']
            
            print(f"\n[{i}/{len(category_apis)}] {description}")
            print(f"    接口: {url_suffix}")
            
            # 测试API
            test_result = test_api(url_suffix, description)
            
            # 显示结果
            status = test_result['status']
            if status == 'success':
                print(f"    ✅ 成功 - 返回 {test_result['data_count']} 条数据")
                results['success'] += 1
            elif status == 'not_found':
                print(f"    ⚠️  API不存在 - {test_result['message']}")
                results['not_found'] += 1
            elif status == 'error':
                print(f"    ❌ 错误 - {test_result['message']}")
                results['error'] += 1
            elif status == 'exception':
                print(f"    💥 异常 - {test_result['message'][:100]}")  # 限制错误信息长度
                results['exception'] += 1
            else:
                print(f"    ❓ 未知 - {test_result['message']}")
                results['unknown'] += 1
            
            # 保存详细结果
            results['details'].append({
                'category': category_name,
                'url_suffix': url_suffix,
                'description': description,
                'status': status,
                'message': test_result.get('message', ''),
                'data_count': test_result.get('data_count', 0)
            })
    
    # 输出总结
    print("\n" + "=" * 100)
    print("测试总结")
    print("=" * 100)
    print(f"总接口数: {results['total']}")
    print(f"✅ 成功: {results['success']} ({results['success']/results['total']*100:.1f}%)")
    print(f"⚠️  API不存在: {results['not_found']} ({results['not_found']/results['total']*100:.1f}%)")
    print(f"❌ 错误: {results['error']} ({results['error']/results['total']*100:.1f}%)")
    print(f"💥 异常: {results['exception']} ({results['exception']/results['total']*100:.1f}%)")
    print(f"❓ 未知: {results['unknown']} ({results['unknown']/results['total']*100:.1f}%)")
    print()
    
    # 按类别统计
    print("=" * 100)
    print("按类别统计")
    print("=" * 100)
    
    category_stats = {}
    for detail in results['details']:
        cat = detail['category']
        if cat not in category_stats:
            category_stats[cat] = {'total': 0, 'success': 0, 'not_found': 0, 'error': 0}
        
        category_stats[cat]['total'] += 1
        if detail['status'] == 'success':
            category_stats[cat]['success'] += 1
        elif detail['status'] == 'not_found':
            category_stats[cat]['not_found'] += 1
        elif detail['status'] in ['error', 'exception', 'unknown']:
            category_stats[cat]['error'] += 1
    
    for cat, stats in sorted(category_stats.items()):
        success_rate = stats['success'] / stats['total'] * 100 if stats['total'] > 0 else 0
        print(f"\n{cat}:")
        print(f"  总数: {stats['total']}, 成功: {stats['success']}, 不存在: {stats['not_found']}, 错误: {stats['error']}")
        print(f"  成功率: {success_rate:.1f}%")
    
    # 保存详细结果
    with open('all_apis_test_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 100)
    print("详细结果已保存到: all_apis_test_results.json")
    print("=" * 100)
    
    return results

if __name__ == "__main__":
    results = main()
    
    # 如果有错误或异常，返回非0退出码
    if results['error'] > 0 or results['exception'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)
