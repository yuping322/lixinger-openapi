import json
import subprocess
import os
import sys
from pathlib import Path

def run_tests():
    base_dir = Path(__file__).resolve().parent.parent
    cases_file = base_dir / "regression_tests" / "cases.json"
    results_dir = base_dir / "regression_tests" / "results"
    results_dir.mkdir(exist_ok=True)

    with open(cases_file, 'r') as f:
        all_cases = json.load(f)

    summary = []

    for skill_name, cases in all_cases.items():
        print(f"Testing skill: {skill_name}")
        for case in cases:
            name = case['name']
            cmd = case['cmd']
            cwd = base_dir / case['cwd']
            
            print(f"  Running case: {name}...")
            
            try:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    cwd=str(cwd),
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                status = "PASS" if result.returncode == 0 else "FAIL"
                
                # Save output
                output_file = results_dir / f"{skill_name}_{name}.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(result.stdout if result.returncode == 0 else result.stderr)
                
                summary.append({
                    "skill": skill_name,
                    "case": name,
                    "status": status,
                    "error": result.stderr if result.returncode != 0 else ""
                })
            except Exception as e:
                summary.append({
                    "skill": skill_name,
                    "case": name,
                    "status": "ERROR",
                    "error": str(e)
                })

    # Save summary
    with open(results_dir / "summary.json", 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print("\n--- Testing Summary ---")
    for item in summary:
        print(f"[{item['status']}] {item['skill']} - {item['case']}")

    # Auto-render Markdown reports
    print("\nGenerating Markdown reports...")
    try:
        subprocess.run(
            [sys.executable, str(base_dir / "regression_tests" / "render_report.py")],
            check=True
        )
        print("Reports generated successfully.")
    except Exception as e:
        print(f"Failed to generate reports: {e}")

if __name__ == "__main__":
    run_tests()
