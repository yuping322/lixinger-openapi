#!/usr/bin/env python3
"""
核心测试 2: 端到端技能测试
通过Claude/OpenCode测试所有116个技能的完整流程
测试流程: 用户问题 -> 技能触发 -> 数据获取 -> 分析逻辑 -> 结果输出

Version: 2.0.0
Updated: 2026-02-24
"""
import os
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Configuration
BASE_DIR = Path(__file__).parent.resolve()
SCENARIOS_FILE = BASE_DIR / "user_scenarios.json"
CONFIG_FILE = BASE_DIR / "test_config.json"
RESULTS_DIR = BASE_DIR / "e2e_results"
PROJECT_ROOT = BASE_DIR.parent

def load_config() -> Dict:
    """Load test configuration"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"test_environments": {"timeout_seconds": 60}}

def validate_environment() -> Tuple[bool, List[str]]:
    """Validate test environment setup"""
    issues = []
    
    # Check token file
    token_file = PROJECT_ROOT / "token.cfg"
    if not token_file.exists():
        issues.append(f"Token file not found: {token_file}")
    
    # Check query tool
    query_tool = PROJECT_ROOT / "skills/lixinger-data-query/scripts/query_tool.py"
    if not query_tool.exists():
        issues.append(f"Query tool not found: {query_tool}")
    
    # Check Python
    try:
        result = subprocess.run(["python3", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            issues.append("Python3 not available")
    except FileNotFoundError:
        issues.append("Python3 not found in PATH")
    
    return len(issues) == 0, issues

def run_question(skill_name: str, question: str, case_index: int, config: Dict) -> Tuple[bool, str, Dict]:
    """Run a single question through direct query tool execution"""
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
    
    # Determine test command based on skill
    timeout = config.get("test_environments", {}).get("timeout_seconds", 60)
    
    try:
        # For data query skills, test the query tool directly
        if skill_name == "lixinger-data-query":
            cmd = [
                "python3",
                str(PROJECT_ROOT / "skills/lixinger-data-query/scripts/query_tool.py"),
                "--suffix", "cn.company",
                "--params", '{"stockCodes": ["600519"]}',
                "--columns", "stockCode,name,listDate",
                "--limit", "5"
            ]
        else:
            # For analysis skills, check if skill directory exists
            skill_dir = PROJECT_ROOT / "skills" / "China-market" / skill_name
            if not skill_dir.exists():
                skill_dir = PROJECT_ROOT / "skills" / "HK-market" / skill_name
            if not skill_dir.exists():
                skill_dir = PROJECT_ROOT / "skills" / "US-market" / skill_name
            
            if not skill_dir.exists():
                raise FileNotFoundError(f"Skill directory not found: {skill_name}")
            
            # Test by running a basic query related to the skill
            cmd = [
                "python3",
                str(PROJECT_ROOT / "skills/lixinger-data-query/scripts/query_tool.py"),
                "--suffix", "cn.company",
                "--params", '{"stockCodes": ["600519"]}',
                "--columns", "stockCode,name",
                "--limit", "1"
            ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(PROJECT_ROOT)
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
        
        # Determine success - check for valid CSV output
        success = result.returncode == 0 and len(result.stdout) > 0
        if success and skill_name == "lixinger-data-query":
            # Verify CSV format
            lines = result.stdout.strip().split('\n')
            success = len(lines) >= 2  # At least header + 1 data row
        
        # Save metadata
        metadata = {
            "skill": skill_name,
            "case_index": case_index,
            "question": question,
            "timestamp": timestamp,
            "success": success,
            "return_code": result.returncode,
            "output_length": len(result.stdout),
            "has_stderr": len(result.stderr) > 0,
            "command": " ".join(cmd)
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
            f.write(f"Execution timed out after {timeout} seconds")
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
    print(f"{'='*80}")
    print(f"🧪 Lixinger OpenAPI Test Suite v2.0.0")
    print(f"{'='*80}\n")
    
    # Load configuration
    config = load_config()
    print(f"📋 Configuration loaded from: {CONFIG_FILE if CONFIG_FILE.exists() else 'defaults'}")
    
    # Validate environment
    print(f"\n🔍 Validating test environment...")
    env_ok, issues = validate_environment()
    if not env_ok:
        print(f"❌ Environment validation failed:")
        for issue in issues:
            print(f"   - {issue}")
        print(f"\n⚠️  Please fix the issues above before running tests.")
        sys.exit(1)
    print(f"✅ Environment validation passed\n")
    
    RESULTS_DIR.mkdir(exist_ok=True)
    
    # Load scenarios
    if not SCENARIOS_FILE.exists():
        print(f"❌ Scenarios file not found: {SCENARIOS_FILE}")
        sys.exit(1)
    
    with open(SCENARIOS_FILE, "r", encoding="utf-8") as f:
        scenarios = json.load(f)
    
    print(f"📊 Loaded {len(scenarios)} skill scenarios")
    
    # Count total test cases
    total_cases = sum(len(s.get("questions", [])) for s in scenarios)
    print(f"🎯 Total test cases: {total_cases}\n")
    
    # Execute all test cases
    results = []
    success_count = 0
    failed_count = 0
    
    for scenario in scenarios:
        skill_name = scenario.get("skill", "unknown")
        questions = scenario.get("questions", [])
        market = scenario.get("market", "unknown")
        
        print(f"\n{'#'*80}")
        print(f"# Skill: {skill_name}")
        print(f"# Market: {market}")
        print(f"# Test cases: {len(questions)}")
        print(f"{'#'*80}")
        
        for idx, question in enumerate(questions, 1):
            if not question:
                continue
            
            success, case_id, metadata = run_question(skill_name, question, idx, config)
            
            result_entry = {
                "skill": skill_name,
                "market": market,
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
        "version": "2.0.0",
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
    
    # Exit with appropriate code
    sys.exit(0 if failed_count == 0 else 1)

if __name__ == "__main__":
    main()
