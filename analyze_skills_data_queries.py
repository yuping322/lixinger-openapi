#!/usr/bin/env python3
"""
分析 China-market skills 的 data-queries.md 与 SKILL.md 的匹配度
"""
import os
import re
from pathlib import Path
from collections import defaultdict

SKILLS_DIR = "/Users/fengzhi/Downloads/git/lixinger-openapi/skills/China-market"

def extract_api_calls(content):
    """从内容中提取 API 调用"""
    # 匹配 --suffix 参数来提取 API 路径
    pattern = r'--suffix\s+"([^"]+)"'
    apis = re.findall(pattern, content)
    return set(apis)

def extract_data_requirements(skill_content):
    """从 SKILL.md 中提取数据需求关键词"""
    keywords = set()
    
    # 提取常见的数据需求关键词
    patterns = [
        r'基本面',
        r'估值',
        r'财务',
        r'分红',
        r'股东',
        r'交易',
        r'涨停',
        r'龙虎榜',
        r'大宗交易',
        r'北向资金',
        r'沪港通',
        r'概念板块',
        r'行业板块',
        r'指数',
        r'市场情绪',
        r'热度',
        r'公告',
        r'可转债',
        r'质押',
        r'IPO',
        r'解禁',
        r'回购',
        r'内幕交易',
        r'商誉',
        r'融资融券',
        r'ST',
        r'退市',
        r'ESG',
        r'量化因子',
    ]
    
    for pattern in patterns:
        if re.search(pattern, skill_content):
            keywords.add(pattern)
    
    return keywords

def analyze_skill(skill_path):
    """分析单个 skill"""
    skill_name = os.path.basename(skill_path)
    skill_md = os.path.join(skill_path, "SKILL.md")
    data_queries_md = os.path.join(skill_path, "references", "data-queries.md")
    
    result = {
        'name': skill_name,
        'has_skill_md': os.path.exists(skill_md),
        'has_data_queries': os.path.exists(data_queries_md),
        'skill_keywords': set(),
        'api_calls': set(),
        'status': 'unknown'
    }
    
    # 读取 SKILL.md
    if result['has_skill_md']:
        try:
            with open(skill_md, 'r', encoding='utf-8') as f:
                skill_content = f.read()
                result['skill_keywords'] = extract_data_requirements(skill_content)
        except Exception as e:
            result['error'] = f"读取 SKILL.md 失败: {str(e)}"
    
    # 读取 data-queries.md
    if result['has_data_queries']:
        try:
            with open(data_queries_md, 'r', encoding='utf-8') as f:
                queries_content = f.read()
                result['api_calls'] = extract_api_calls(queries_content)
                result['queries_content_length'] = len(queries_content)
        except Exception as e:
            result['error'] = f"读取 data-queries.md 失败: {str(e)}"
    
    # 判断状态
    if not result['has_skill_md']:
        result['status'] = '缺少 SKILL.md'
    elif not result['has_data_queries']:
        result['status'] = '缺少 data-queries.md'
    elif len(result['api_calls']) == 0:
        result['status'] = '无 API 示例'
    elif result['queries_content_length'] < 100:
        result['status'] = '内容过少'
    else:
        result['status'] = '正常'
    
    return result

def main():
    """主函数"""
    print("=" * 80)
    print("China-market Skills Data Queries 分析报告")
    print("=" * 80)
    print()
    
    # 获取所有 skills
    skills = []
    for item in os.listdir(SKILLS_DIR):
        skill_path = os.path.join(SKILLS_DIR, item)
        if os.path.isdir(skill_path) and not item.startswith('.'):
            skills.append(skill_path)
    
    skills.sort()
    
    # 分析每个 skill
    results = []
    for skill_path in skills:
        result = analyze_skill(skill_path)
        results.append(result)
    
    # 统计
    status_count = defaultdict(int)
    all_apis = set()
    
    for result in results:
        status_count[result['status']] += 1
        all_apis.update(result['api_calls'])
    
    # 输出统计
    print(f"总计 Skills: {len(results)}")
    print()
    print("状态分布:")
    for status, count in sorted(status_count.items()):
        print(f"  {status}: {count}")
    print()
    print(f"使用的 API 总数: {len(all_apis)}")
    print()
    
    # 按状态分组输出
    print("=" * 80)
    print("详细分析")
    print("=" * 80)
    print()
    
    for status in sorted(status_count.keys()):
        print(f"\n## {status} ({status_count[status]} 个)")
        print("-" * 80)
        for result in results:
            if result['status'] == status:
                print(f"\n### {result['name']}")
                print(f"  - SKILL.md: {'✓' if result['has_skill_md'] else '✗'}")
                print(f"  - data-queries.md: {'✓' if result['has_data_queries'] else '✗'}")
                if result['api_calls']:
                    print(f"  - API 调用数: {len(result['api_calls'])}")
                    print(f"  - APIs: {', '.join(sorted(result['api_calls']))}")
                if 'error' in result:
                    print(f"  - 错误: {result['error']}")
    
    # 输出 API 使用频率
    print("\n" + "=" * 80)
    print("API 使用频率统计")
    print("=" * 80)
    api_usage = defaultdict(int)
    for result in results:
        for api in result['api_calls']:
            api_usage[api] += 1
    
    for api, count in sorted(api_usage.items(), key=lambda x: x[1], reverse=True):
        print(f"  {api}: {count} 次")

if __name__ == "__main__":
    main()
