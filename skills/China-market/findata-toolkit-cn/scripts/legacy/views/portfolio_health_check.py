from __future__ import annotations

VIEW_NAME = "portfolio_health_check"
DESCRIPTION = "诊断现有投资组合的风险和低效问题，评估组合集中度，检查因子暴露，评估相关性风险。"
PARAMS_SCHEMA = {"type": "object", "properties": {"portfolio": {"type": "array", "items": {"type": "object"}}}, "required": []}


def plan(params: dict) -> list[dict]:
    return [
        {"key": "market_overview", "view": "market_overview_dashboard", "args": {}},
        {"key": "risk_free_rate", "tool": "macro_china_lpr", "args": {}},
        {"key": "index_returns", "tool": "index_zh_a_daily", "args": {"symbol": "sh000001", "period": "daily"}},
    ]
