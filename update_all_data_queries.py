#!/usr/bin/env python3
"""批量更新所有skills的data-queries.md文件"""

import os
from pathlib import Path
import shutil

# 模板文件路径
TEMPLATE_PATH = "skills/China-market/DATA_QUERIES_TEMPLATE.md"

# 查找所有data-queries.md文件
def find_data_queries_files():
    """查找所有data-queries.md文件"""
    files = []
    for root, dirs, filenames in os.walk("skills/China-market"):
        for filename in filenames:
            if filename == "data-queries.md":
                filepath = os.path.join(root, filename)
                files.append(filepath)
    return files

def update_file(filepath, template_content):
    """更新单个文件"""
    try:
        # 备份原文件
        backup_path = filepath + ".backup"
        if os.path.exists(filepath):
            shutil.copy2(filepath, backup_path)
        
        # 写入新内容
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        return True, "成功"
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 80)
    print("批量更新data-queries.md文件")
    print("=" * 80)
    
    # 读取模板
    print(f"\n读取模板: {TEMPLATE_PATH}")
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    print(f"模板大小: {len(template_content)} 字符")
    
    # 查找所有文件
    print("\n查找所有data-queries.md文件...")
    files = find_data_queries_files()
    print(f"找到 {len(files)} 个文件")
    
    # 更新文件
    print("\n开始更新...")
    success_count = 0
    fail_count = 0
    
    for i, filepath in enumerate(files, 1):
        # 获取skill名称
        skill_name = Path(filepath).parent.parent.name
        
        print(f"\n[{i}/{len(files)}] {skill_name}")
        print(f"  路径: {filepath}")
        
        success, message = update_file(filepath, template_content)
        
        if success:
            print(f"  ✅ {message}")
            success_count += 1
        else:
            print(f"  ❌ {message}")
            fail_count += 1
    
    # 总结
    print("\n" + "=" * 80)
    print("更新完成")
    print("=" * 80)
    print(f"总文件数: {len(files)}")
    print(f"成功: {success_count}")
    print(f"失败: {fail_count}")
    
    if fail_count == 0:
        print("\n✅ 所有文件更新成功！")
    else:
        print(f"\n⚠️  有 {fail_count} 个文件更新失败")
    
    print("\n备份文件已保存为 .backup 后缀")
    print("如需恢复，可以使用备份文件")

if __name__ == "__main__":
    main()
