#!/usr/bin/env python3
"""
修复 data-queries.md 中的 --params 引号问题
"""
import os
import re

def fix_file(filepath):
    """修复单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 修复 --params \'...\'  为 --params '...'
    content = re.sub(r"--params\s+\\'", "--params '", content)
    content = re.sub(r"\\'\s*\n", "'\n", content)
    content = re.sub(r"\\'\\\\", "' \\\\", content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    fixed_count = 0
    
    for root, dirs, files in os.walk('skills'):
        for filename in files:
            if filename == 'data-queries.md':
                filepath = os.path.join(root, filename)
                if fix_file(filepath):
                    print(f"✅ 修复: {filepath}")
                    fixed_count += 1
    
    print(f"\n总计修复 {fixed_count} 个文件")

if __name__ == '__main__':
    main()
