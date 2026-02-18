from __future__ import annotations

VIEW_NAME = "portfolio_monitor_orchestrator"
DESCRIPTION = "编排组合监控：集中度、相关性/风格暴露、流动性、情景压力等，整合成一份监控报告。"
PARAMS_SCHEMA = {"type": "object", "properties": {"portfolio": {"type": "array", "items": {"type": "object"}}}, "required": []}


def plan(params: dict) -> list[dict]:
    return [
        {"key": "health_check", "view": "portfolio_health_check", "args": params},
        {"key": "risk_check", "view": "shareholder_risk_check", "args": {}},
        {"key": "volatility_check", "view": "volatility_regime_monitor", "args": {}},
    ]
