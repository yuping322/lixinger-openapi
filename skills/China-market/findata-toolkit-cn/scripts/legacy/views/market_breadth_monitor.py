from __future__ import annotations

VIEW_NAME = "market_breadth_monitor"
DESCRIPTION = "监控市场宽度与市场内部结构（涨跌家数、新高新低、集中度、宽度动量），用于判断风险偏好与状态切换。"
PARAMS_SCHEMA = {"type": "object", "properties": {}, "required": []}


def plan(params: dict) -> list[dict]:
    return [
        {"key": "market_trade_info", "tool": "stock_zh_a_trade_info", "args": {}},
        {"key": "market_new_high_low", "tool": "stock_new_high_low_em", "args": {}},
        {"key": "market_overview", "view": "market_overview_dashboard", "args": {}},
    ]
