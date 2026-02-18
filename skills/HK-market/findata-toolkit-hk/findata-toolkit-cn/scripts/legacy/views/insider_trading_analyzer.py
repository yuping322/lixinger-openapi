from __future__ import annotations

VIEW_NAME = "insider_trading_analyzer"
DESCRIPTION = "分析A股市场董监高及重要股东增减持行为，识别具有显著管理层信心信号的公司。"
PARAMS_SCHEMA = {"type": "object", "properties": {}, "required": []}


def plan(params: dict) -> list[dict]:
    return [
        {"key": "stock_inside_trade", "tool": "stock_inside_trade_em", "args": {}},
        {"key": "stock_management_change", "tool": "stock_management_change_em", "args": {}},
    ]
