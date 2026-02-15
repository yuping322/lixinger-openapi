import os
import re
import json
from pathlib import Path

SKILLS_DIR = Path("/Users/fengzhi/Downloads/git/lixinger-openapi/skills/China-market")
OUTPUT_FILE = Path("/Users/fengzhi/Downloads/git/lixinger-openapi/regression_tests/cases.json")

def generate_cases():
    all_cases = {}
    
    # 首先保留原有的 lixinger-data-query 用例
    all_cases["lixinger-data-query"] = [
        {
          "name": "query_cn_company",
          "cwd": "skills/lixinger-data-query",
          "cmd": "python scripts/query_tool.py --suffix 'cn/company' --params '{\"stockCodes\": [\"600519\"]}' --format json"
        },
        {
          "name": "query_index_valuation",
          "cwd": "skills/lixinger-data-query",
          "cmd": "python scripts/query_tool.py --suffix 'cn/index/fundamental' --params '{\"stockCodes\": [\"000016\"], \"date\": \"2024-12-10\", \"metricsList\": [\"pe_ttm.mcw\"]}' --format json"
        }
    ]

    for skill_name in os.listdir(SKILLS_DIR):
        skill_path = SKILLS_DIR / skill_name
        if not skill_path.is_dir() or skill_name == "findata-toolkit-cn":
            continue
            
        data_queries_path = skill_path / "references" / "data-queries.md"
        if not data_queries_path.exists():
            continue
            
        print(f"Extracting cases from {skill_name}...")
        
        with open(data_queries_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 寻找技能文档中的示例命令 (示例：python ../findata-toolkit-cn/scripts/toolkit.py ...)
        # 我们寻找以 ```bash 开头的块，或者直接寻找匹配模式的行
        matches = re.findall(r"python \.\./findata-toolkit-cn/scripts/toolkit\.py .+", content)
        
        if not matches:
            continue
            
        skill_cases = []
        for i, cmd in enumerate(list(set(matches))[:3]): # 每个技能取前 3 个不同示例
            # 过滤掉带有 --help 的
            if "--help" in cmd:
                continue
                
            skill_cases.append({
                "name": f"case_{i}",
                "cwd": f"skills/China-market/{skill_name}",
                "cmd": cmd
            })
            
        if skill_cases:
            all_cases[skill_name] = skill_cases

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_cases, f, indent=2, ensure_ascii=False)
        
    print(f"\nGenerated cases.json with {len(all_cases)} skills.")

if __name__ == "__main__":
    generate_cases()
