import os
import json
import re
from pathlib import Path

SKILLS_DIR = Path("/Users/fengzhi/Downloads/git/lixinger-openapi/skills/China-market")
OUTPUT_FILE = Path("/Users/fengzhi/Downloads/git/lixinger-openapi/regression_tests/user_scenarios.json")

def generate_questions(skill_name, description):
    """根据技能描述和名称生成 3-5 个典型用户问题"""
    # 简单的基于关键词的映射
    questions = []
    
    # 通用模板
    if "market" in skill_name or "overview" in skill_name:
        questions = [
            "今天A股整体表现怎么样？有哪些指数涨幅靠前？",
            "市场现在的估值水平在什么程度？在高分位还是低分位？",
            "最近北向资金是流出还是流入？对市场有什么影响？",
            "哪些宽基指数最近表现比较稳健？"
        ]
    elif "stock" in skill_name or "analysis" in skill_name:
        questions = [
            "帮我看看贵州茅台现在的估值合不合理？",
            "宁德时代最近的财务指标有什么亮点或风险？",
            "这支票最近有没有什么大宗交易或者异动情况？",
            "分析一下该股的行业地位和对标公司情况。"
        ]
    elif "fund-flow" in skill_name or "northbound" in skill_name:
        questions = [
            "最近一周北向资金重点扫货了哪些板块？",
            "资金流向显示哪些行业正在被主力资金抛售？",
            "今日大市资金净流入排名靠前的股票有哪些？"
        ]
    elif "risk" in skill_name or "monitor" in skill_name:
        questions = [
            "帮我查一下这几支股票有没有质押风险或者商誉爆雷的可能？",
            "最近有哪些公司触发了退市预警或者ST风险？",
            "监控一下当前的股权质押平仓压力情况。"
        ]
    elif "sector" in skill_name or "industry" in skill_name:
        questions = [
            "现在白酒行业的整体估值分位是多少？",
            "哪些申万二级行业最近出现了明显的资金净流入？",
            "分析一下新能源汽车产业链的上下游景气度。"
        ]
    else:
        # 通用兜底
        questions = [
            f"关于 {skill_name}，你能提供哪些核心数据分析？",
            f"使用这个技能可以帮我监控哪些金融风险？",
            f"针对目前的市场行情，{skill_name} 有什么具体的建议或发现？"
        ]
    
    return questions[:5]

def main():
    scenarios = []
    
    for skill_dir in sorted(os.listdir(SKILLS_DIR)):
        skill_path = SKILLS_DIR / skill_dir
        if not skill_path.is_dir() or skill_dir == "findata-toolkit-cn":
            continue
            
        # 读取 SKILL.md 获取描述
        skill_md_path = skill_path / "SKILL.md"
        description = ""
        if skill_md_path.exists():
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
                match = re.search(r"description:\s*(.*)", content)
                if match:
                    description = match.group(1).strip()
        
        # 读取 data-queries.md 获取可用命令
        dq_path = skill_path / "references" / "data_queries.md"
        if not dq_path.exists():
             dq_path = skill_path / "references" / "data-queries.md"
             
        commands = []
        if dq_path.exists():
            with open(dq_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 提取 toolkit.py 相关命令并转换为绝对路径
                toolkit_abs = "/Users/fengzhi/Downloads/git/lixinger-openapi/skills/China-market/findata-toolkit-cn/scripts/toolkit.py"
                commands = re.findall(r"python \.\./findata-toolkit-cn/scripts/toolkit\.py (.+)", content)
                commands = list(set([f"python {toolkit_abs} {c}" for c in commands if "--help" not in c]))

        questions = generate_questions(skill_dir, description)
        
        # 关联问题与指令
        # 简单匹配：前 N 个问题对应前 M 个指令
        scenarios.append({
            "skill": skill_dir,
            "description": description,
            "test_cases": [
                {
                    "question": q,
                    "cmd": commands[i % len(commands)] if commands else "python ../findata-toolkit-cn/scripts/toolkit.py --help"
                } for i, q in enumerate(questions)
            ]
        })

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(scenarios, f, indent=2, ensure_ascii=False)
        
    print(f"Generated scenarios for {len(scenarios)} skills.")

if __name__ == "__main__":
    main()
