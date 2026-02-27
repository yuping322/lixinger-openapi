#!/usr/bin/env python3
"""
测试新增的 data-queries.md 示例
从补充的 7 个 skills 中提取所有 bash 命令并执行测试
"""
import subprocess
import re
import json
import sys
from pathlib import Path
from datetime import datetime

# Configuration
BASE_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = BASE_DIR.parent
RESULTS_DIR = BASE_DIR / "new_examples_test_results"

# 需要测试的 skills
SKILLS_TO_TEST = [
    "skills/China-market/single-stock-health-check/references/data-queries.md",
    "skills/China-market/high-dividend-strategy/references/data-queries.md",
    "skills/China-market/policy-sensitivity-brief/references/data-queries.md",
    "skills/China-market/limit-up-pool-analyzer/references/data-queries.md",
    "skills/China-market/financial-statement-analyzer/references/data-queries.md",
    "skills/China-market/block-deal-monitor/references/data-queries.md",
    "skills/China-market/etf-allocator/references/data-queries.md",
]

def extract_bash_commands(file_path):
    """从 markdown 文件中提取 bash 代码块"""
    commands = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配 ```bash ... ``` 代码块
    pattern = r'```bash\n(.*?)\n```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for match in matches:
        # 跳过注释和循环命令
        if match.strip().startswith('#'):
            continue
        if 'for ' in match or 'while ' in match or 'done' in match:
            continue
        if '|' in match and 'while read' in match:
            continue
        # 跳过包含重定向的命令（会导致测试脚本无法捕获输出）
        if '>' in match and 'csv' in match:
            continue
        
        # 清理命令（移除续行符）
        command = match.replace('\\\n', ' ').strip()
        
        # 只保留 python3 开头的命令
        if command.startswith('python3'):
            commands.append(command)
    
    return commands

def run_command(command, skill_name, cmd_index):
    """运行单个命令并返回结果"""
    print(f"\n{'='*80}")
    print(f"测试: {skill_name} - 命令 #{cmd_index}")
    print(f"命令: {command[:100]}...")
    print('='*80)
    
    try:
        # 添加超时和限制输出
        if '--limit' not in command:
            command += ' --limit 5'
        
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(PROJECT_ROOT)
        )
        
        # 检查结果
        if result.returncode == 0:
            # 检查是否有数据返回
            output_lines = result.stdout.strip().split('\n')
            if len(output_lines) >= 2:  # 至少有表头和一行数据
                print(f"✅ 成功 - 返回 {len(output_lines)-1} 行数据")
                return {
                    "status": "success",
                    "lines": len(output_lines) - 1,
                    "output_preview": result.stdout[:200]
                }
            else:
                print(f"⚠️  成功但无数据")
                return {
                    "status": "no_data",
                    "output": result.stdout[:200]
                }
        else:
            error_msg = result.stderr[:200] if result.stderr else "Unknown error"
            print(f"❌ 失败 - {error_msg}")
            return {
                "status": "failed",
                "error": error_msg,
                "stdout": result.stdout[:200]
            }
            
    except subprocess.TimeoutExpired:
        print(f"⏱️  超时（30秒）")
        return {"status": "timeout"}
    except Exception as e:
        print(f"💥 异常 - {str(e)}")
        return {"status": "exception", "error": str(e)}

def main():
    """主测试流程"""
    print("="*80)
    print("测试新增的 data-queries.md 示例")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    RESULTS_DIR.mkdir(exist_ok=True)
    
    # 收集所有命令
    all_tests = []
    for skill_path in SKILLS_TO_TEST:
        full_path = PROJECT_ROOT / skill_path
        if not full_path.exists():
            print(f"⚠️  文件不存在: {skill_path}")
            continue
        
        skill_name = skill_path.split('/')[-3]  # 提取 skill 名称
        commands = extract_bash_commands(full_path)
        
        print(f"\n📋 {skill_name}: 找到 {len(commands)} 个命令")
        
        for cmd in commands:
            all_tests.append({
                "skill": skill_name,
                "command": cmd,
                "file": skill_path
            })
    
    print(f"\n总计: {len(all_tests)} 个命令需要测试\n")
    
    # 执行测试
    results = {
        "timestamp": datetime.now().isoformat(),
        "total": len(all_tests),
        "success": 0,
        "failed": 0,
        "no_data": 0,
        "timeout": 0,
        "exception": 0,
        "details": []
    }
    
    for i, test in enumerate(all_tests, 1):
        print(f"\n[{i}/{len(all_tests)}]", end=" ")
        
        test_result = run_command(test["command"], test["skill"], i)
        
        detail = {
            "index": i,
            "skill": test["skill"],
            "command": test["command"],
            "status": test_result["status"],
            **test_result
        }
        results["details"].append(detail)
        
        # 统计
        status = test_result["status"]
        if status == "success":
            results["success"] += 1
        elif status == "no_data":
            results["no_data"] += 1
        elif status == "timeout":
            results["timeout"] += 1
        elif status == "exception":
            results["exception"] += 1
        else:
            results["failed"] += 1
    
    # 保存结果
    summary_file = RESULTS_DIR / f"test_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # 生成详细报告
    report_file = RESULTS_DIR / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("# 新增示例测试报告\n\n")
        f.write(f"**测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"## 总体统计\n\n")
        f.write(f"- 总命令数: {results['total']}\n")
        f.write(f"- ✅ 成功: {results['success']} ({results['success']/results['total']*100:.1f}%)\n")
        f.write(f"- ⚠️  无数据: {results['no_data']} ({results['no_data']/results['total']*100:.1f}%)\n")
        f.write(f"- ❌ 失败: {results['failed']} ({results['failed']/results['total']*100:.1f}%)\n")
        f.write(f"- ⏱️  超时: {results['timeout']} ({results['timeout']/results['total']*100:.1f}%)\n")
        f.write(f"- 💥 异常: {results['exception']} ({results['exception']/results['total']*100:.1f}%)\n\n")
        
        # 按 skill 分组统计
        f.write("## 按 Skill 统计\n\n")
        skill_stats = {}
        for detail in results["details"]:
            skill = detail["skill"]
            if skill not in skill_stats:
                skill_stats[skill] = {"total": 0, "success": 0, "failed": 0}
            skill_stats[skill]["total"] += 1
            if detail["status"] == "success":
                skill_stats[skill]["success"] += 1
            else:
                skill_stats[skill]["failed"] += 1
        
        for skill, stats in sorted(skill_stats.items()):
            success_rate = stats["success"] / stats["total"] * 100
            f.write(f"### {skill}\n\n")
            f.write(f"- 总数: {stats['total']}\n")
            f.write(f"- 成功: {stats['success']}\n")
            f.write(f"- 失败: {stats['failed']}\n")
            f.write(f"- 成功率: {success_rate:.1f}%\n\n")
        
        # 失败的命令详情
        f.write("## 失败的命令\n\n")
        failed_details = [d for d in results["details"] if d["status"] not in ["success", "no_data"]]
        if failed_details:
            for detail in failed_details:
                f.write(f"### {detail['skill']} - 命令 #{detail['index']}\n\n")
                f.write(f"**状态**: {detail['status']}\n\n")
                f.write(f"**命令**:\n```bash\n{detail['command']}\n```\n\n")
                if "error" in detail:
                    f.write(f"**错误**: {detail['error']}\n\n")
        else:
            f.write("无失败命令 🎉\n\n")
    
    # 打印总结
    print(f"\n{'='*80}")
    print("测试总结")
    print('='*80)
    print(f"总命令数: {results['total']}")
    print(f"✅ 成功: {results['success']} ({results['success']/results['total']*100:.1f}%)")
    print(f"⚠️  无数据: {results['no_data']} ({results['no_data']/results['total']*100:.1f}%)")
    print(f"❌ 失败: {results['failed']} ({results['failed']/results['total']*100:.1f}%)")
    print(f"⏱️  超时: {results['timeout']} ({results['timeout']/results['total']*100:.1f}%)")
    print(f"💥 异常: {results['exception']} ({results['exception']/results['total']*100:.1f}%)")
    print(f"\n📊 详细结果: {summary_file}")
    print(f"📄 测试报告: {report_file}")
    print('='*80)
    
    # 按 skill 显示统计
    print(f"\n按 Skill 统计:")
    for skill, stats in sorted(skill_stats.items()):
        success_rate = stats["success"] / stats["total"] * 100
        status_icon = "✅" if success_rate >= 80 else "⚠️" if success_rate >= 50 else "❌"
        print(f"  {status_icon} {skill}: {stats['success']}/{stats['total']} ({success_rate:.0f}%)")
    
    # 返回退出码
    total_issues = results['failed'] + results['timeout'] + results['exception']
    sys.exit(0 if total_issues == 0 else 1)

if __name__ == "__main__":
    main()
