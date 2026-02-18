from __future__ import annotations

VIEW_NAME = "high_dividend_strategy"
DESCRIPTION = "分析A股高股息策略，评估红利股的收益可持续性与长期回报。"
PARAMS_SCHEMA = {"type": "object", "properties": {}, "required": []}


def plan(params: dict) -> list[dict]:
    return [
        {"key": "stock_dividend", "tool": "stock_dividend_em", "args": {}},
        {"key": "stock_fhps", "tool": "stock_fhps_em", "args": {}},
    ]
