from __future__ import annotations

VIEW_NAME = "ipo_lockup_risk_monitor"
DESCRIPTION = "监控限售解禁、重要股东减持与供给冲击风险，输出时间表与风险提示。"
PARAMS_SCHEMA = {"type": "object", "properties": {}, "required": []}


def plan(params: dict) -> list[dict]:
    return [
        {"key": "restricted_release", "view": "restricted_release_dashboard", "args": {}},
        {"key": "stock_holder_reduction", "tool": "stock_holder_reduction_em", "args": {}},
    ]
