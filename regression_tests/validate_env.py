#!/usr/bin/env python3
"""
Environment validation script
Checks if all prerequisites are met before running tests

Version: 2.0.0
Updated: 2026-02-24
"""
import os
import sys
import subprocess
from pathlib import Path

# Colors
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
NC = '\033[0m'  # No Color

def print_status(check_name: str, passed: bool, message: str = ""):
    """Print check status with color"""
    status = f"{GREEN}✅{NC}" if passed else f"{RED}❌{NC}"
    print(f"{status} {check_name}")
    if message:
        print(f"   {message}")

def main():
    """Run all validation checks"""
    print("="*80)
    print("🔍 Environment Validation")
    print("="*80)
    print()
    
    all_passed = True
    
    # Get paths
    base_dir = Path(__file__).parent.resolve()
    project_root = base_dir.parent
    
    # 1. Check Python version
    print("1️⃣  Checking Python version...")
    try:
        result = subprocess.run(
            ["python3", "--version"],
            capture_output=True,
            text=True
        )
        version = result.stdout.strip()
        passed = result.returncode == 0
        print_status("Python 3", passed, version)
        all_passed = all_passed and passed
    except FileNotFoundError:
        print_status("Python 3", False, "python3 not found in PATH")
        all_passed = False
    print()
    
    # 2. Check token file
    print("2️⃣  Checking API token...")
    token_file = project_root / "token.cfg"
    if token_file.exists():
        with open(token_file, 'r') as f:
            token = f.read().strip()
        if token:
            print_status("Token file", True, f"Found at {token_file}")
        else:
            print_status("Token file", False, "File exists but is empty")
            all_passed = False
    else:
        print_status("Token file", False, f"Not found at {token_file}")
        all_passed = False
    print()
    
    # 3. Check query tool
    print("3️⃣  Checking query tool...")
    query_tool = project_root / ".claude/skills/lixinger-data-query/scripts/query_tool.py"
    if query_tool.exists():
        print_status("Query tool", True, f"Found at {query_tool}")
    else:
        print_status("Query tool", False, f"Not found at {query_tool}")
        all_passed = False
    print()
    
    # 4. Check test files
    print("4️⃣  Checking test files...")
    test_files = [
        "e2e_runner.py",
        "user_scenarios.json",
        "test_config.json"
    ]
    for test_file in test_files:
        file_path = base_dir / test_file
        if file_path.exists():
            print_status(test_file, True)
        else:
            print_status(test_file, False, f"Not found at {file_path}")
            all_passed = False
    print()
    
    # 5. Check skills directories
    print("5️⃣  Checking skills directories...")
    skills_dir = project_root / ".claude/skills"
    if skills_dir.exists():
        print_status(".claude/skills", True, f"Found at {skills_dir}")
    else:
        print_status(".claude/skills", False, f"Not found at {skills_dir}")
        all_passed = False
    print()
    
    # 6. Test query tool execution
    print("6️⃣  Testing query tool execution...")
    try:
        result = subprocess.run(
            [
                "python3",
                str(query_tool),
                "--help"
            ],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=str(project_root)
        )
        if result.returncode == 0 and "usage:" in result.stdout.lower():
            print_status("Query tool execution", True, "Help command works")
        else:
            print_status("Query tool execution", False, "Help command failed")
            all_passed = False
    except Exception as e:
        print_status("Query tool execution", False, str(e))
        all_passed = False
    print()
    
    # Summary
    print("="*80)
    if all_passed:
        print(f"{GREEN}🎉 All checks passed! Environment is ready for testing.{NC}")
        print()
        print("Next steps:")
        print("  1. Run API tests:      python3 test_all_apis.py")
        print("  2. Run all tests:      ./run_tests.sh")
        print("  3. Run full suite:     ./run_tests.sh --full")
        sys.exit(0)
    else:
        print(f"{RED}❌ Some checks failed. Please fix the issues above.{NC}")
        print()
        print("Common fixes:")
        print("  - Create token.cfg in project root with your API token")
        print("  - Ensure all skill directories are present")
        print("  - Install Python 3.7 or higher")
        sys.exit(1)

if __name__ == "__main__":
    main()
