from __future__ import annotations

VIEW_NAME = "rebalancing_planner"
DESCRIPTION = "设计组合再平衡规则（阈值/定期）、约束条件与执行清单。"
PARAMS_SCHEMA = {"type": "object", "properties": {"portfolio": {"type": "array", "items": {"type": "object"}}}, "required": []}


def plan(params: dict) -> list[dict]:
    return [
        {"key": "portfolio_health", "view": "portfolio_health_check", "args": params},
        {"key": "market_regime", "view": "valuation_regime_detector", "args": {}},
        {"key": "volatility_regime", "view": "volatility_regime_monitor", "args": {}},
    ]
