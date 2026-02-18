from __future__ import annotations

VIEW_NAME = "risk_adjusted_return_optimizer"
DESCRIPTION = "为中国投资者构建风险调整后收益最优的A股投资组合，根据资金规模、风险偏好和投资期限进行资产配置。"
PARAMS_SCHEMA = {"type": "object", "properties": {"risk_tolerance": {"type": "string"}, "investment_horizon": {"type": "string"}}, "required": []}


def plan(params: dict) -> list[dict]:
    return [
        {"key": "market_returns", "tool": "index_zh_a_daily", "args": {"symbol": "sh000001", "period": "daily"}},
        {"key": "bond_returns", "tool": "bond_china_daily", "args": {}},
        {"key": "etf_list", "tool": "fund_etf_spot_em", "args": {}},
    ]
