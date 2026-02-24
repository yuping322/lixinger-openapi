#!/usr/bin/env python3
"""
分析每个 China-market skill 的数据需求，生成映射表。
"""

from pathlib import Path
import re

# 根据 skill 名称推断需要的数据类型
SKILL_KEYWORDS_MAPPING = {
    "dividend": ["cn.company.dividend", "cn.company.allotment"],
    "shareholder": ["cn.company.shareholders-num", "cn.company.majority-shareholders"],
    "block-deal": ["cn.company.block-deal"],
    "pledge": ["cn.company.pledge"],
    "announcement": ["cn.company.announcement"],
    "fund": ["cn.fund", "cn.fund.shareholdings"],
    "index": ["cn.index", "cn.index.constituents"],
    "industry": ["cn.industry"],
    "macro": ["macro"],
    "margin": ["cn.company.margin-trading-and-securities-lending"],
    "dragon-tiger": ["cn.company.trading-abnormal"],
    "ipo": ["cn.company"],
    "valuation": ["cn.company.fundamental.non_financial"],
    "financial": ["cn.company.fs.non_financial"],
    "insider": ["cn.company.senior-executive-shares-change", "cn.company.major-shareholders-shares-change"],
    "repurchase": ["cn.company"],
    "equity": ["cn.company.equity-change"],
    "candlestick": ["cn.company.candlestick"],
    "hot": ["cn.company.hot"],
}

def analyze_skill(skill_dir):
    """分析单个 skill 的数据需求"""
    skill_name = skill_dir.name
    
    # 读取 SKILL.md 获取描述
    skill_md = skill_dir / "SKILL.md"
    description = ""
    if skill_md.exists():
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
            # 提取 description
            match = re.search(r'description:\s*(.+)', content)
            if match:
                description = match.group(1).strip()
    
    # 根据 skill 名称推断需要的 API
    apis = []
    for keyword, api_list in SKILL_KEYWORDS_MAPPING.items():
        if keyword in skill_name:
            apis.extend(api_list)
    
    # 如果没有匹配到，使用默认 API
    if not apis:
        apis = ["cn.company", "cn.company.candlestick"]
    
    # 去重
    apis = list(set(apis))
    
    return {
        "name": skill_name,
        "description": description,
        "apis": apis
    }

def main():
    """主函数"""
    china_market_dir = Path("skills/China-market")
    
    # 查找所有 skill 目录
    skill_dirs = []
    for skill_dir in china_market_dir.iterdir():
        if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
            data_queries_file = skill_dir / "references" / "data-queries.md"
            if data_queries_file.exists():
                skill_dirs.append(skill_dir)
    
    print(f"找到 {len(skill_dirs)} 个 skills\n")
    print("="*80)
    
    # 分析每个 skill
    results = []
    for skill_dir in sorted(skill_dirs):
        result = analyze_skill(skill_dir)
        results.append(result)
        print(f"\nSkill: {result['name']}")
        print(f"APIs: {', '.join(result['apis'])}")
    
    print("\n" + "="*80)
    print(f"\n共分析 {len(results)} 个 skills")
    
    # 统计 API 使用频率
    api_count = {}
    for result in results:
        for api in result['apis']:
            api_count[api] = api_count.get(api, 0) + 1
    
    print("\nAPI 使用频率（Top 10）:")
    for api, count in sorted(api_count.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {api}: {count} skills")

if __name__ == "__main__":
    main()
