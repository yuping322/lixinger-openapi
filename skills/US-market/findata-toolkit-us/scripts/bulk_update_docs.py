import os
import re
from pathlib import Path

# 路径配置
SKILLS_DIR = Path("/Users/fengzhi/Downloads/git/lixinger-openapi/skills/China-market")
TOOLKIT_RELATIVE_PATH = "../findata-toolkit-cn/scripts/toolkit.py"

# 指令替换模板
# 指令替换模板
REPLACEMENT_RULES = [
    (r"python \.\./findata-toolkit-cn/scripts/views_runner\.py list", "python ../findata-toolkit-cn/scripts/toolkit.py --help"),
    (r"python \.\./findata-toolkit-cn/scripts/views_runner\.py describe (.+)", "python ../findata-toolkit-cn/scripts/toolkit.py --help"),
    (r"python \.\./findata-toolkit-cn/scripts/views_runner\.py stock_zh_a_spot_em", "python ../findata-toolkit-cn/scripts/toolkit.py --market --mode brief"),
    (r"python \.\./findata-toolkit-cn/scripts/views_runner\.py stock_zh_a_hist --set symbol=(.+) --set period=daily --set start_date=(.+) --set end_date=(.+) --set adjust=qfq", 
     r"python ../findata-toolkit-cn/scripts/toolkit.py --stock \1 --mode full"),
    # 更多特定映射
    (r"stock_sse_summary", "toolkit.py --market"),
    (r"stock_szse_summary", "toolkit.py --market"),
    (r"python \.\./findata-toolkit-cn/scripts/views_runner\.py ([a-zA-Z_0-9]+)", r"python ../findata-toolkit-cn/scripts/toolkit.py --raw \1 --params '{}'"),
]

def update_skill_docs(dry_run=True):
    updated_count = 0
    for skill_name in os.listdir(SKILLS_DIR):
        skill_path = SKILLS_DIR / skill_name
        if not skill_path.is_dir() or skill_name == "findata-toolkit-cn":
            continue
            
        data_queries_path = skill_path / "references" / "data-queries.md"
        if not data_queries_path.exists():
            continue
            
        print(f"Processing {skill_name}...")
        
        with open(data_queries_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = content
        
        # 1. 更新环境准备
        new_content = new_content.replace(
            "python -m pip install -r ../findata-toolkit-cn/requirements.txt",
            "python -m pip install -r ../findata-toolkit-cn/requirements.txt  # Now powered by Lixinger"
        )
        
        # 2. 更新口径说明
        new_content = new_content.replace(
            "`views_runner.py` 输出统一为 JSON",
            "`toolkit.py` 提供实体聚合与原始 API 查询，输出统一为 JSON"
        )
        
        # 3. 批量替换命令
        for pattern, replacement in REPLACEMENT_RULES:
            new_content = re.sub(pattern, replacement, new_content)
            
        if content != new_content:
            if not dry_run:
                with open(data_queries_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            print(f"  [UPDATED] {skill_name}")
            updated_count += 1
        else:
            print(f"  [NO CHANGE] {skill_name}")
            
    print(f"\nTotal skills processed: {updated_count}")

if __name__ == "__main__":
    # 执行真实更新
    print("--- REAL UPDATE ---")
    update_skill_docs(dry_run=False)
