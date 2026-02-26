#!/usr/bin/env python3
"""
测试所有 data-queries.md 文件中的示例命令
一次跑完所有测试，不中途退出，保存完整日志
"""
import os
import re
import json
import subprocess
import random
from pathlib import Path
from datetime import datetime

def find_data_queries_files():
    """查找所有 data-queries.md 文件"""
    files = []
    for root, dirs, filenames in os.walk('skills'):
        for filename in filenames:
            if filename == 'data-queries.md':
                filepath = os.path.join(root, filename)
                files.append(filepath)
    return files

def extract_commands(filepath):
    """从 markdown 文件中提取命令"""
    commands = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取代码块中的命令
    code_blocks = re.findall(r'```bash\n(.*?)\n```', content, re.DOTALL)
    
    for block in code_blocks:
        # 查找 python3 命令
        lines = block.strip().split('\n')
        cmd_lines = []
        in_command = False
        in_for_loop = False
        
        for line in lines:
            line_stripped = line.strip()
            
            # 检测 for 循环
            if line_stripped.startswith('for ') and ' in ' in line_stripped:
                in_for_loop = True
                continue
            
            # 跳过 for 循环中的命令
            if in_for_loop:
                if line_stripped == 'done':
                    in_for_loop = False
                continue
            
            # 开始一个新命令
            if line_stripped.startswith('python3'):
                in_command = True
                cmd_lines.append(line_stripped)
            # 继续当前命令（以 -- 开头或以 \ 结尾的行）
            elif in_command and (line_stripped.startswith('--') or (cmd_lines and cmd_lines[-1].rstrip().endswith('\\'))):
                cmd_lines.append(line_stripped)
            # 命令结束
            elif in_command:
                break
        
        if cmd_lines:
            # 合并命令行，移除反斜杠和多余空格
            cmd = ' '.join(cmd_lines)
            cmd = cmd.replace(' \\', '')  # 移除反斜杠
            cmd = re.sub(r'\s+', ' ', cmd)  # 合并多余空格
            commands.append(cmd.strip())
    
    return commands

def run_command(cmd, timeout=30):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'stdout': '',
            'stderr': 'Command timeout',
            'returncode': -1
        }
    except Exception as e:
        return {
            'success': False,
            'stdout': '',
            'stderr': str(e),
            'returncode': -1
        }

def main():
    start_time = datetime.now()
    timestamp = start_time.strftime('%Y%m%d_%H%M%S')
    
    print("=" * 120)
    print("测试所有 data-queries.md 文件中的示例命令（随机顺序，不中途退出）")
    print("=" * 120)
    
    # 查找所有文件
    files = find_data_queries_files()
    print(f"\n✅ 找到 {len(files)} 个 data-queries.md 文件\n")
    
    # 提取所有命令
    all_tests = []
    for filepath in files:
        commands = extract_commands(filepath)
        for cmd in commands:
            # 提取市场和 skill 名称
            parts = filepath.split(os.sep)
            market = parts[1] if len(parts) > 1 else 'unknown'
            skill = parts[2] if len(parts) > 2 else 'unknown'
            
            all_tests.append({
                'market': market,
                'skill': skill,
                'file': filepath,
                'command': cmd
            })
    
    print(f"✅ 提取到 {len(all_tests)} 个示例命令\n")
    
    # 随机打乱测试顺序
    random.shuffle(all_tests)
    print("✅ 已随机打乱测试顺序\n")
    
    # 运行测试
    results = []
    success_count = 0
    fail_count = 0
    errors_by_type = {}
    
    for i, test in enumerate(all_tests, 1):
        print(f"[{i}/{len(all_tests)}] 测试: {test['market']}/{test['skill']}", end=' ')
        
        result = run_command(test['command'])
        
        test['result'] = result
        test['test_number'] = i
        results.append(test)
        
        if result['success']:
            print("✅")
            success_count += 1
        else:
            print("❌")
            fail_count += 1
            
            # 分类错误
            error_msg = result['stderr']
            if 'ValidationError' in error_msg:
                if 'are invalid' in error_msg:
                    error_type = 'Invalid metrics'
                elif 'is required' in error_msg:
                    error_type = 'Missing required parameter'
                elif 'must contain' in error_msg:
                    error_type = 'Parameter constraint violation'
                else:
                    error_type = 'ValidationError (other)'
            elif 'Api was not found' in error_msg:
                error_type = 'API not found'
            elif 'timeout' in error_msg.lower():
                error_type = 'Timeout'
            else:
                error_type = 'Other error'
            
            if error_type not in errors_by_type:
                errors_by_type[error_type] = []
            errors_by_type[error_type].append({
                'test_number': i,
                'market': test['market'],
                'skill': test['skill'],
                'file': test['file'],
                'command': test['command'],
                'error': error_msg
            })
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # 保存完整结果
    results_file = f'test_results_{timestamp}.json'
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # 生成错误报告
    error_report_file = f'test_errors_{timestamp}.md'
    with open(error_report_file, 'w', encoding='utf-8') as f:
        f.write(f"# 测试错误报告\n\n")
        f.write(f"**测试时间**: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**测试时长**: {duration:.1f} 秒\n")
        f.write(f"**总测试数**: {len(all_tests)}\n")
        f.write(f"**成功**: {success_count} ({success_count/len(all_tests)*100:.1f}%)\n")
        f.write(f"**失败**: {fail_count} ({fail_count/len(all_tests)*100:.1f}%)\n\n")
        
        f.write(f"## 错误分类统计\n\n")
        for error_type, errors in sorted(errors_by_type.items(), key=lambda x: len(x[1]), reverse=True):
            f.write(f"- **{error_type}**: {len(errors)} 个\n")
        
        f.write(f"\n## 详细错误列表\n\n")
        for error_type, errors in sorted(errors_by_type.items(), key=lambda x: len(x[1]), reverse=True):
            f.write(f"### {error_type} ({len(errors)} 个)\n\n")
            for i, error in enumerate(errors, 1):
                f.write(f"#### 错误 {i}: [{error['test_number']}/{len(all_tests)}] {error['market']}/{error['skill']}\n\n")
                f.write(f"**文件**: `{error['file']}`\n\n")
                f.write(f"**命令**:\n```bash\n{error['command']}\n```\n\n")
                f.write(f"**错误信息**:\n```\n{error['error']}\n```\n\n")
                f.write("---\n\n")
    
    # 打印总结
    print("\n" + "=" * 120)
    print("测试完成")
    print("=" * 120)
    print(f"测试时长: {duration:.1f} 秒")
    print(f"总计: {len(all_tests)} 个测试")
    print(f"成功: {success_count} ({success_count/len(all_tests)*100:.1f}%)")
    print(f"失败: {fail_count} ({fail_count/len(all_tests)*100:.1f}%)")
    
    if errors_by_type:
        print(f"\n错误分类:")
        for error_type, errors in sorted(errors_by_type.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"  - {error_type}: {len(errors)} 个")
    
    print(f"\n✅ 完整结果已保存到: {results_file}")
    print(f"✅ 错误报告已保存到: {error_report_file}\n")
    
    return 0 if fail_count == 0 else 1

if __name__ == '__main__':
    exit(main())
