#!/usr/bin/env python3
"""
Test the new data-queries.md approach by running sample queries from the documentation.
"""

import subprocess
import json
import sys

def run_query(description, command):
    """Run a query command and return the result."""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"✅ Success")
            # Show first 5 lines of output
            lines = result.stdout.strip().split('\n')
            print(f"Output (first 5 lines):")
            for line in lines[:5]:
                print(f"  {line}")
            if len(lines) > 5:
                print(f"  ... ({len(lines) - 5} more lines)")
            return True
        else:
            print(f"❌ Failed")
            print(f"Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"❌ Timeout")
        return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def main():
    """Run test queries."""
    print("Testing data-queries.md approach")
    print("="*60)
    
    tests = [
        {
            "description": "查询股票基本信息",
            "command": 'python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn.company" --params \'{"stockCodes": ["600519"]}\' --columns "stockCode,name,ipoDate,exchange"'
        },
        {
            "description": "查询分红数据",
            "command": 'python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn.company.dividend" --params \'{"stockCode": "600519"}\' --columns "date,dividendPerShare,dividendYield" --limit 5'
        },
        {
            "description": "查询股东人数",
            "command": 'python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn.company.shareholders-num" --params \'{"stockCode": "600519"}\' --columns "date,num,shareholdersNumberChangeRate" --limit 5'
        },
        {
            "description": "查询公告信息",
            "command": 'python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn.company.announcement" --params \'{"stockCode": "600519"}\' --columns "date,linkText,types" --limit 3'
        }
    ]
    
    results = []
    for test in tests:
        success = run_query(test["description"], test["command"])
        results.append(success)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Total tests: {len(results)}")
    print(f"  Passed: {sum(results)}")
    print(f"  Failed: {len(results) - sum(results)}")
    print(f"  Success rate: {sum(results) / len(results) * 100:.1f}%")
    print(f"{'='*60}")
    
    return 0 if all(results) else 1

if __name__ == "__main__":
    sys.exit(main())
