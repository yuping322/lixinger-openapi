#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能调用桥接层，让Claude可以通过自然语言直接调用所有量化技能
"""
import json
import subprocess
import sys
from pathlib import Path

def run_skill(skill_name: str, params: dict = None) -> dict:
    """执行指定技能并返回结果"""
    if params is None:
        params = {}

    # 技能到执行命令的映射
    skill_map = {
        "财报分析": f"--skill financial_statement_analyzer --skill-params '{json.dumps(params)}'",
        "市场概览": "--market",
        "个股分析": f"--stock {params.get('stock_code')} --mode {params.get('mode', 'full')}",
        "因子拥挤度": "--skill factor_crowding_monitor --skill-params '{}'",
        "高股息选股": "--skill high_dividend_strategy --skill-params '{}'",
        "ESG筛选": "--skill esg_screener --skill-params '{}'",
        "龙虎榜分析": "--skill dragon_tiger_list_analyzer --skill-params '{}'",
        "北向资金分析": "--skill northbound_flow_analyzer --skill-params '{}'",
        "行业轮动分析": "--skill sector_rotation_detector --skill-params '{}'",
        "商誉风险监控": "--skill goodwill_risk_monitor --skill-params '{}'",
        "股权质押风险": "--skill equity_pledge_risk_monitor --skill-params '{}'",
    }

    if skill_name not in skill_map:
        # 尝试直接匹配skill名称
        command = f"python skills/China-market/findata-toolkit-cn/scripts/toolkit.py --skill {skill_name} --skill-params '{json.dumps(params)}'"
    else:
        # 中文别名映射
        command = f"python skills/China-market/findata-toolkit-cn/scripts/toolkit.py {skill_map[skill_name]}"

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent,
            timeout=30
        )

        if result.returncode == 0:
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                return {"result": result.stdout}
        else:
            return {"error": result.stderr}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python skill_bridge.py <skill_name> [params_json]")
        sys.exit(1)

    skill_name = sys.argv[1]
    params = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}

    result = run_skill(skill_name, params)
    print(json.dumps(result, ensure_ascii=False, indent=2))
