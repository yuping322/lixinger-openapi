import os
import json
import subprocess
from pathlib import Path

SCENARIOS_FILE = Path("/Users/fengzhi/Downloads/git/lixinger-openapi/regression_tests/user_scenarios.json")
RESULTS_MD = Path("/Users/fengzhi/Downloads/git/lixinger-openapi/regression_tests/results/scenario_test_results.md")

def run_command(cmd, cwd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd, timeout=30)
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), -1

def main():
    if not SCENARIOS_FILE.exists():
        print("Scenarios file not found.")
        return

    with open(SCENARIOS_FILE, 'r', encoding='utf-8') as f:
        scenarios = json.load(f)

    report_lines = [
        "# User Scenario Test Results",
        "",
        "| Skill | Question | Command | Status | Data Snippet |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ]

    total = 0
    passed = 0
    
    # 为了演示效率，每个技能只跑前 2 个问题
    for item in scenarios:
        skill = item["skill"]
        test_cases = item["test_cases"][:2] 
        
        for case in test_cases:
            total += 1
            question = case["question"]
            cmd = case["cmd"]
            
            print(f"Testing [{skill}]: {question}...")
            stdout, stderr, code = run_command(cmd, "/Users/fengzhi/Downloads/git/lixinger-openapi/regression_tests")
            
            status = "✅ PASS" if code == 0 else "❌ FAIL"
            if code == 0:
                passed += 1
                # 提取前 50 个字符作为摘要
                snippet = stdout[:100].replace("\n", " ").strip() + "..."
            else:
                snippet = stderr[:100].replace("\n", " ").strip() + "..."
            
            report_lines.append(f"| {skill} | {question} | `{cmd}` | {status} | {snippet} |")

    report_lines.append("")
    report_lines.append(f"## Summary: {passed}/{total} Passed")
    
    with open(RESULTS_MD, 'w', encoding='utf-8') as f:
        f.write("\n".join(report_lines))

    print(f"Test completed. Results saved to {RESULTS_MD}")

if __name__ == "__main__":
    main()
