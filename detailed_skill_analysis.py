#!/usr/bin/env python3
"""
详细分析 skills 的数据需求匹配度
"""
import os
import re
from pathlib import Path

SKILLS_DIR = "/Users/fengzhi/Downloads/git/lixinger-openapi/skills/China-market"

# 重点分析的 skills
FOCUS_SKILLS = [
    "single-stock-health-check",
    "high-dividend-strategy",
    "policy-sensitivity-brief",
    "limit-up-pool-analyzer",
    "financial-statement-analyzer",
    "block-deal-monitor",
    "etf-allocator",
    "sector-rotation-detector",
]

def extract_data_needs_from_skill(skill_content):
    """从 SKILL.md 中提取数据需求"""
    needs = {
        'mentioned_apis': set(),
        'data_keywords': set(),
        'output_requirements': [],
    }
    
    # 提取提到的 API 或数据类型
    api_patterns = [
        (r'基本面', 'fundamental'),
        (r'估值', 'valuation'),
        (r'财务报表|资产负债表|利润表|现金流', 'financial_statement'),
        (r'分红|股息', 'dividend'),
        (r'股东|持股', 'shareholder'),
        (r'涨停|跌停', 'limit_up_down'),
        (r'龙虎榜', 'trading_abnormal'),
        (r'大宗交易', 'block_deal'),
        (r'北向资金|沪港通|深港通', 'northbound'),
        (r'概念板块', 'concept'),
        (r'行业板块|行业', 'industry'),
        (r'指数', 'index'),
        (r'K线|价格|成交量', 'candlestick'),
        (r'质押', 'pledge'),
        (r'回购', 'repurchase'),
        (r'解禁', 'lockup'),
        (r'融资融券', 'margin'),
        (r'商誉', 'goodwill'),
        (r'宏观|GDP|货币供应|CPI', 'macro'),
    ]
    
    for pattern, keyword in api_patterns:
        if re.search(pattern, skill_content):
            needs['data_keywords'].add(keyword)
    
    # 提取输出要求部分
    output_section = re.search(r'##\s*输出格式.*?(?=##|$)', skill_content, re.DOTALL)
    if output_section:
        needs['output_requirements'] = output_section.group(0).split('\n')[:10]
    
    return needs

def extract_apis_from_queries(queries_content):
    """从 data-queries.md 中提取 API 调用详情"""
    apis = []
    
    # 提取每个 API 调用块
    blocks = re.findall(r'```bash\n(.*?)\n```', queries_content, re.DOTALL)
    
    for block in blocks:
        # 提取 --suffix
        suffix_match = re.search(r'--suffix\s+"([^"]+)"', block)
        # 提取 --params
        params_match = re.search(r'--params\s+\'({[^}]+})\'', block)
        # 提取 --columns
        columns_match = re.search(r'--columns\s+"([^"]+)"', block)
        
        if suffix_match:
            api_info = {
                'suffix': suffix_match.group(1),
                'params': params_match.group(1) if params_match else None,
                'columns': columns_match.group(1).split(',') if columns_match else [],
                'full_command': block.strip()
            }
            apis.append(api_info)
    
    return apis

def analyze_skill_detail(skill_name):
    """详细分析单个 skill"""
    skill_path = os.path.join(SKILLS_DIR, skill_name)
    skill_md = os.path.join(skill_path, "SKILL.md")
    data_queries_md = os.path.join(skill_path, "references", "data-queries.md")
    
    print(f"\n{'='*80}")
    print(f"Skill: {skill_name}")
    print(f"{'='*80}\n")
    
    # 读取 SKILL.md
    if not os.path.exists(skill_md):
        print("❌ 缺少 SKILL.md")
        return
    
    with open(skill_md, 'r', encoding='utf-8') as f:
        skill_content = f.read()
    
    needs = extract_data_needs_from_skill(skill_content)
    
    print("📋 数据需求关键词:")
    for keyword in sorted(needs['data_keywords']):
        print(f"  - {keyword}")
    
    # 读取 data-queries.md
    if not os.path.exists(data_queries_md):
        print("\n❌ 缺少 data-queries.md")
        return
    
    with open(data_queries_md, 'r', encoding='utf-8') as f:
        queries_content = f.read()
    
    apis = extract_apis_from_queries(queries_content)
    
    print(f"\n📊 提供的 API 示例 ({len(apis)} 个):")
    for i, api in enumerate(apis, 1):
        print(f"\n  {i}. {api['suffix']}")
        if api['columns']:
            print(f"     字段: {', '.join(api['columns'][:5])}{'...' if len(api['columns']) > 5 else ''}")
    
    # 匹配度分析
    print(f"\n🔍 匹配度分析:")
    
    # 检查关键数据类型是否有对应的 API
    api_suffixes = [api['suffix'] for api in apis]
    
    coverage = {
        'fundamental': any('fundamental' in s for s in api_suffixes),
        'candlestick': any('candlestick' in s for s in api_suffixes),
        'dividend': any('dividend' in s for s in api_suffixes),
        'shareholder': any('shareholder' in s for s in api_suffixes),
        'block_deal': any('block-deal' in s for s in api_suffixes),
        'trading_abnormal': any('trading-abnormal' in s for s in api_suffixes),
        'index': any('index' in s for s in api_suffixes),
        'industry': any('industry' in s for s in api_suffixes),
        'macro': any('macro' in s for s in api_suffixes),
        'financial_statement': any('fs/' in s for s in api_suffixes),
        'pledge': any('pledge' in s for s in api_suffixes),
        'margin': any('margin' in s for s in api_suffixes),
    }
    
    matched = []
    missing = []
    
    for keyword in needs['data_keywords']:
        if keyword in coverage and coverage[keyword]:
            matched.append(keyword)
        else:
            missing.append(keyword)
    
    if matched:
        print(f"  ✅ 已覆盖: {', '.join(matched)}")
    if missing:
        print(f"  ⚠️  可能缺失: {', '.join(missing)}")
    
    # 检查示例的完整性
    print(f"\n📝 示例质量评估:")
    
    has_params_example = any(api['params'] for api in apis)
    has_columns_example = any(api['columns'] for api in apis)
    
    print(f"  - 参数示例: {'✅' if has_params_example else '⚠️  缺少'}")
    print(f"  - 字段筛选示例: {'✅' if has_columns_example else '⚠️  缺少'}")
    print(f"  - API 数量: {len(apis)} 个")
    
    if len(apis) < 2:
        print(f"  ⚠️  示例较少，建议增加更多场景")
    elif len(apis) > 5:
        print(f"  ✅ 示例丰富")
    else:
        print(f"  ✅ 示例适中")

def main():
    """主函数"""
    print("="*80)
    print("China-market Skills 详细数据匹配度分析")
    print("="*80)
    
    for skill_name in FOCUS_SKILLS:
        analyze_skill_detail(skill_name)
    
    print(f"\n\n{'='*80}")
    print("分析完成")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
