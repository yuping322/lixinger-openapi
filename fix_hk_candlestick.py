#!/usr/bin/env python3
"""
批量修复 hk/company.candlestick API 调用
1. 修复路径格式：hk/company.candlestick → hk/company/candlestick
2. 添加 type 参数
"""
import re
from pathlib import Path

def fix_hk_candlestick_in_file(file_path):
    """修复单个文件中的 hk candlestick API 调用"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes = []
    
    # 修复 API 路径格式和添加 type 参数
    # 匹配模式：--suffix "hk/company.candlestick" --params '{"stockCode": ...}'
    pattern = r'--suffix "hk/company\.candlestick"\s+--params \'(\{[^}]+\})\''
    
    def add_type_param(match):
        params_str = match.group(1)
        # 解析参数，添加 type
        if '"type"' not in params_str:
            # 在参数中添加 type: "normal"
            params_str = params_str.rstrip('}') + ', "type": "normal"}'
        return f'--suffix "hk/company/candlestick" --params \'{params_str}\''
    
    if re.search(pattern, content):
        content = re.sub(pattern, add_type_param, content)
        changes.append("hk/company.candlestick: 修复路径格式并添加 type 参数")
    
    # 修复 API 列表中的路径
    content = content.replace('hk/company.candlestick', 'hk/company/candlestick')
    content = content.replace('- `hk/company/candlestick`', '- `hk/company/candlestick`')
    
    # 如果有修改，写回文件
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes
    
    return False, []

def main():
    """主函数"""
    print("=" * 80)
    print("批量修复 hk/company.candlestick API 调用")
    print("=" * 80)
    print()
    
    # 查找所有 data-queries.md 文件
    skills_dir = Path("skills")
    files = list(skills_dir.glob("*/*/references/data-queries.md"))
    
    print(f"找到 {len(files)} 个 data-queries.md 文件")
    print()
    
    fixed_count = 0
    for file_path in files:
        modified, changes = fix_hk_candlestick_in_file(file_path)
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
