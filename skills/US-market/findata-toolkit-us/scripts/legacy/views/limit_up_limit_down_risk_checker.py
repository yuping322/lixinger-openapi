from __future__ import annotations

VIEW_NAME = "limit_up_limit_down_risk_checker"
DESCRIPTION = "评估涨跌停/停牌等制度约束对可交易性的影响，输出风险标签与应对建议。"
PARAMS_SCHEMA = {"type": "object", "properties": {}, "required": []}


def plan(params: dict) -> list[dict]:
    return [
        {"key": "zt_pool", "tool": "stock_zt_pool_em", "args": {"date": ""}},
        {"key": "dt_pool", "tool": "stock_dt_pool_em", "args": {"date": ""}},
        {"key": "suspend_list", "tool": "stock_suspend_list_em", "args": {}},
    ]
