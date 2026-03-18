#!/usr/bin/env python3
"""
Generate test cases for skills that don't have tests yet

Version: 2.0.0
Updated: 2026-02-24
"""
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = BASE_DIR.parent
SCENARIOS_FILE = BASE_DIR / "user_scenarios.json"

def get_all_skills():
    """Get all available skills from directories"""
    skills = {}
    
    skills_dir = PROJECT_ROOT / ".claude/skills"
    
    if skills_dir.exists():
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
                # Handle names like China-market_ab-ah-premium-monitor
                if '_' in skill_dir.name:
                    market, skill_name = skill_dir.name.split('_', 1)
                    skills[skill_name] = market
                else:
                    skills[skill_dir.name] = "General"
    
    return skills

def get_tested_skills():
    """Get skills that already have test cases"""
    if not SCENARIOS_FILE.exists():
        return set()
    
    with open(SCENARIOS_FILE, 'r', encoding='utf-8') as f:
        scenarios = json.load(f)
    
    return {s['skill'] for s in scenarios}

def generate_test_questions(skill_name, market):
    """Generate generic test questions for a skill"""
    # Generic questions based on skill name patterns
    questions = []
    
    if 'monitor' in skill_name:
        questions = [
            f"监控{skill_name.replace('-', ' ')}的最新情况",
            f"分析{skill_name.replace('-', ' ')}的风险指标",
            f"生成{skill_name.replace('-', ' ')}的监控报告"
        ]
    elif 'analyzer' in skill_name or 'analysis' in skill_name:
        questions = [
            f"分析{skill_name.replace('-', ' ')}的核心指标",
            f"提供{skill_name.replace('-', ' ')}的详细分析",
            f"评估{skill_name.replace('-', ' ')}的投资价值"
        ]
    elif 'screener' in skill_name or 'scanner' in skill_name:
        questions = [
            f"筛选符合{skill_name.replace('-', ' ')}条件的标的",
            f"扫描{skill_name.replace('-', ' ')}的投资机会",
            f"找出{skill_name.replace('-', ' ')}的候选清单"
        ]
    elif 'tracker' in skill_name:
        questions = [
            f"跟踪{skill_name.replace('-', ' ')}的最新动态",
            f"监控{skill_name.replace('-', ' ')}的变化趋势",
            f"记录{skill_name.replace('-', ' ')}的历史数据"
        ]
    else:
        questions = [
            f"使用{skill_name.replace('-', ' ')}进行分析",
            f"获取{skill_name.replace('-', ' ')}的相关数据",
            f"生成{skill_name.replace('-', ' ')}的报告"
        ]
    
    return questions

def main():
    """Generate missing test cases"""
    print("🔍 Scanning for skills without test cases...\n")
    
    all_skills = get_all_skills()
    tested_skills = get_tested_skills()
    
    missing_skills = set(all_skills.keys()) - tested_skills
    
    if not missing_skills:
        print("✅ All skills have test cases!")
        return
    
    print(f"Found {len(missing_skills)} skills without test cases:\n")
    
    new_scenarios = []
    for skill_name in sorted(missing_skills):
        market = all_skills[skill_name]
        questions = generate_test_questions(skill_name, market)
        
        scenario = {
            "skill": skill_name,
            "description": f"Auto-generated test case for {skill_name}",
            "market": market,
            "questions": questions
        }
        
        new_scenarios.append(scenario)
        print(f"  - {skill_name} ({market})")
    
    # Load existing scenarios
    if SCENARIOS_FILE.exists():
        with open(SCENARIOS_FILE, 'r', encoding='utf-8') as f:
            existing_scenarios = json.load(f)
    else:
        existing_scenarios = []
    
    # Merge
    all_scenarios = existing_scenarios + new_scenarios
    
    # Save
    output_file = BASE_DIR / "user_scenarios_updated.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_scenarios, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Generated {len(new_scenarios)} new test cases")
    print(f"📝 Saved to: {output_file}")
    print(f"\nTo use the updated scenarios:")
    print(f"  mv {output_file} {SCENARIOS_FILE}")

if __name__ == "__main__":
    main()
