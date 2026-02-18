from __future__ import annotations

VIEW_NAME = "small_cap_growth_identifier"
DESCRIPTION = "识别A股市场中被忽视的小市值高成长公司，筛选市值小但增长快的标的。"
PARAMS_SCHEMA = {"type": "object", "properties": {}, "required": []}


def plan(params: dict) -> list[dict]:
    return [
        {"key": "stock_small_cap", "tool": "stock_zh_a_spot_em", "args": {}},
        {"key": "stock_growth", "tool": "stock_growth_ability_em", "args": {"symbol": "000001"}},
        {"key": "stock_profit", "tool": "stock_profit_ability_em", "args": {"symbol": "000001"}},
    ]
