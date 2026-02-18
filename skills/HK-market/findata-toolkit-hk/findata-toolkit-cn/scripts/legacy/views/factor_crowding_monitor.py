from __future__ import annotations

VIEW_NAME = "factor_crowding_monitor"
DESCRIPTION = "监控因子拥挤度与因子收益分化，用于识别拥挤交易与风格挤压/轮动风险。"
PARAMS_SCHEMA = {"type": "object", "properties": {}, "required": []}


def plan(params: dict) -> list[dict]:
    return [
        {"key": "stock_style_factor", "tool": "stock_style_factor_em", "args": {}},
        {"key": "market_style", "tool": "stock_market_style_em", "args": {}},
    ]
