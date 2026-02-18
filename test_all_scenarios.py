import json
import subprocess
import time
from pathlib import Path

def run_all_tests(scenarios_file):
    with open(scenarios_file, 'r', encoding='utf-8') as f:
        scenarios = json.load(f)

    results = []
    total_tests = 0
    passed = 0
    failed = 0

    print(f"🚀 开始执行所有用户场景测试，共 {len(scenarios)} 个技能模块")
    print("=" * 100)

    for skill in scenarios:
        skill_name = skill['skill']
        skill_desc = skill['description']
        test_cases = skill['test_cases']

        print(f"\n📦 测试技能: {skill_name}")
        print(f"📝 功能描述: {skill_desc}")
        print(f"🧪 测试用例数: {len(test_cases)}")
        print("-" * 80)

        for i, test_case in enumerate(test_cases, 1):
            total_tests += 1
            question = test_case['question']
            cmd = test_case['cmd']

            print(f"\n🔍 测试用例 {i}: {question}")
            print(f"⚙️  执行命令: {cmd}")

            start_time = time.time()
            try:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                elapsed = time.time() - start_time

                if result.returncode == 0:
                    status = "✅ PASS"
                    passed += 1
                    output_preview = result.stdout[:200].strip() + "..." if len(result.stdout) > 200 else result.stdout.strip()
                else:
                    status = "❌ FAIL"
                    failed += 1
                    output_preview = result.stderr[:200].strip() + "..." if len(result.stderr) > 200 else result.stderr.strip()

                print(f"   {status} | 耗时: {elapsed:.2f}s")
                if output_preview:
                    print(f"   输出预览: {output_preview}")

                results.append({
                    'skill': skill_name,
                    'test_case': question,
                    'cmd': cmd,
                    'status': status,
                    'returncode': result.returncode,
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'elapsed': elapsed
                })

            except subprocess.TimeoutExpired:
                status = "⏰ TIMEOUT"
                failed += 1
                elapsed = time.time() - start_time
                print(f"   {status} | 耗时: {elapsed:.2f}s (超时30秒)")
                results.append({
                    'skill': skill_name,
                    'test_case': question,
                    'cmd': cmd,
                    'status': status,
                    'returncode': -1,
                    'stdout': '',
                    'stderr': '执行超时',
                    'elapsed': elapsed
                })
            except Exception as e:
                status = "💥 ERROR"
                failed += 1
                elapsed = time.time() - start_time
                print(f"   {status} | 耗时: {elapsed:.2f}s | 错误: {str(e)}")
                results.append({
                    'skill': skill_name,
                    'test_case': question,
                    'cmd': cmd,
                    'status': status,
                    'returncode': -2,
                    'stdout': '',
                    'stderr': str(e),
                    'elapsed': elapsed
                })

    # 生成报告
    print("\n" + "=" * 100)
    print("📊 测试结果汇总")
    print("=" * 100)
    print(f"总测试用例数: {total_tests}")
    print(f"通过: {passed} | 失败: {failed} | 通过率: {passed/total_tests*100:.1f}%")

    # 保存详细报告
    report_file = Path(__file__).parent / "test_scenario_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n📝 详细报告已保存到: {report_file}")

    # 输出失败用例摘要
    if failed > 0:
        print("\n❌ 失败用例摘要:")
        print("-" * 80)
        for res in results:
            if res['status'] != "✅ PASS":
                print(f"{res['status']} | {res['skill']} | {res['test_case'][:50]}...")

if __name__ == "__main__":
    scenarios_file = "/Users/fengzhi/Downloads/git/lixinger-openapi/regression_tests/user_scenarios.json"
    run_all_tests(scenarios_file)
