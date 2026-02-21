#!/usr/bin/env python3
"""
End-to-end test runner that executes user questions directly via Claude CLI
Tests the complete flow: question -> skill triggering -> data fetching -> logic execution
"""
import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

# Configuration
BASE_DIR = Path(__file__).parent.resolve()
SCENARIOS_FILE = BASE_DIR / "user_scenarios.json"
RESULTS_DIR = BASE_DIR / "e2e_results"

def run_question(skill_name: str, question: str, case_index: int):
    """Run a single question through Claude CLI"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    case_id = f"{skill_name}_case_{case_index}_{timestamp}"
    case_dir = RESULTS_DIR / case_id
    case_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*80}")
    print(f"🚀 Testing: {skill_name} - Case {case_index}")
    print(f"📝 Question: {question}")
    print(f"{'='*80}\n")
    
    # Save question
    question_file = case_dir / "question.txt"
    with open(question_file, "w", encoding="utf-8") as f:
        f.write(question)
    
    # Execute via Claude CLI
    try:
        # Remove CLAUDECODE env variable to ensure clean execution
        env = os.environ.copy()
        env.pop('CLAUDECODE', None)
        
        result = subprocess.run(
            ["claude", "chat", question],
            env=env,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        # Save output
        output_file = case_dir / "output.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result.stdout)
        
        # Save stderr if any
        if result.stderr:
            error_file = case_dir / "stderr.log"
            with open(error_file, "w", encoding="utf-8") as f:
                f.write(result.stderr)
        
        # Determine success
        success = result.returncode == 0 and len(result.stdout) > 0
        
        # Save metadata
        metadata = {
            "skill": skill_name,
            "case_index": case_index,
            "question": question,
            "timestamp": timestamp,
            "success": success,
            "return_code": result.returncode,
            "output_length": len(result.stdout),
            "has_stderr": len(result.stderr) > 0
        }
        
        with open(case_dir / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        if success:
            print(f"✅ Success: {case_id}")
        else:
            print(f"❌ Failed: {case_id}")
            if result.stderr:
                print(f"   Error: {result.stderr[:200]}")
        
        return success, case_id, metadata
        
    except subprocess.TimeoutExpired:
        print(f"⏱️  Timeout: {case_id}")
        timeout_file = case_dir / "timeout.log"
        with open(timeout_file, "w") as f:
            f.write("Execution timed out after 5 minutes")
        return False, case_id, {"error": "timeout"}
        
    except Exception as e:
        print(f"💥 Exception: {case_id}")
        print(f"   {str(e)}")
        error_file = case_dir / "exception.log"
        with open(error_file, "w") as f:
            f.write(str(e))
        return False, case_id, {"error": str(e)}

def main():
    """Main execution loop"""
    RESULTS_DIR.mkdir(exist_ok=True)
    
    # Load scenarios
    with open(SCENARIOS_FILE, "r", encoding="utf-8") as f:
        scenarios = json.load(f)
    
    print(f"📊 Loaded {len(scenarios)} skill scenarios")
    
    # Count total test cases
    total_cases = sum(len(s.get("test_cases", [])) for s in scenarios)
    print(f"🎯 Total test cases: {total_cases}\n")
    
    # Execute all test cases
    results = []
    success_count = 0
    failed_count = 0
    
    for scenario in scenarios:
        skill_name = scenario.get("skill", "unknown")
        test_cases = scenario.get("test_cases", [])
        
        print(f"\n{'#'*80}")
        print(f"# Skill: {skill_name}")
        print(f"# Test cases: {len(test_cases)}")
        print(f"{'#'*80}")
        
        for idx, test_case in enumerate(test_cases, 1):
            question = test_case.get("question", "")
            if not question:
                continue
            
            success, case_id, metadata = run_question(skill_name, question, idx)
            
            result_entry = {
                "skill": skill_name,
                "case_index": idx,
                "case_id": case_id,
                "question": question,
                "success": success,
                "metadata": metadata
            }
            results.append(result_entry)
            
            if success:
                success_count += 1
            else:
                failed_count += 1
    
    # Save summary
    summary = {
        "timestamp": datetime.now().isoformat(),
        "total_skills": len(scenarios),
        "total_cases": total_cases,
        "success": success_count,
        "failed": failed_count,
        "success_rate": f"{(success_count/total_cases*100):.2f}%" if total_cases > 0 else "0%",
        "results": results
    }
    
    summary_file = RESULTS_DIR / f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    # Print final summary
    print(f"\n{'='*80}")
    print(f"🎉 Test execution complete!")
    print(f"{'='*80}")
    print(f"✅ Success: {success_count}/{total_cases}")
    print(f"❌ Failed: {failed_count}/{total_cases}")
    print(f"📈 Success Rate: {summary['success_rate']}")
    print(f"📊 Summary saved to: {summary_file}")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
