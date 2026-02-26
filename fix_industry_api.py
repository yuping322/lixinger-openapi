#!/usr/bin/env python3
"""
批量修复 cn/industry 和 hk/industry API 调用中缺少 source 参数的问题
"""
import re
from pathlib import Path

def fix_industry_api_in_file(file_path):
    """修复单个文件中的 industry API 调用"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes = []
    
    # 修复 cn/industry 的空参数
    pattern1 = r'(--suffix "cn/industry"\s+--params\s+\'\{\}\')'
    replacement1 = r'--suffix "cn/industry" --params \'{"source": "sw", "level": "one"}\' --limit 20'
    if re.search(pattern1, content):
        content = re.sub(pattern1, replacement1, content)
        changes.append("cn/industry: 添加 source 参数")
    
    # 修复 hk/industry 的空参数
    pattern2 = r'(--suffix "hk/industry"\s+--params\s+\'\{\}\')'
    replacement2 = r'--suffix "hk/industry" --params \'{"source": "hsi"}\' --limit 50'
    if re.search(pattern2, content):
        content = re.sub(pattern2, replacement2, content)
        changes.append("hk/industry: 添加 source 参数")
    
    # 如果有修改，写回文件
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes
    
    return False, []

def main():
    """主函数"""
    print("=" * 80)
    print("批量修复 industry API 调用")
    print("=" * 80)
    print()
    
    # 查找所有 data-queries.md 文件
    skills_dir = Path("skills")
    files = list(skills_dir.glob("*/*/references/data-queries.md"))
    
    print(f"找到 {len(files)} 个 data-queries.md 文件")
    print()
    
    fixed_count = 0
    for file_path in files:
        modified, changes = fix_industry_api_in_file(file_path)
        if modified:
            fixed_count += 1
            print(f"✅ 修复: {file_path}")
            for change in changes:
                print(f"   - {change}")
    
    print()
    print("=" * 80)
    print(f"修复完成: {fixed_count} 个文件")
    print("=" * 80)

if __name__ == '__main__':
    main()
