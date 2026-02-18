from __future__ import annotations

VIEW_NAME = "sentiment_reality_gap"
DESCRIPTION = "识别A股市场中被过度看空但基本面稳健的逆向投资机会，寻找市场错误定价的公司。"
PARAMS_SCHEMA = {"type": "object", "properties": {}, "required": []}


def plan(params: dict) -> list[dict]:
    return [
        {"key": "stock_drop_rank", "tool": "stock_drop_rank_em", "args": {}},
        {"key": "stock_valuation", "tool": "stock_a_stock_general", "args": {}},
        {"key": "stock_fundamental", "tool": "stock_financial_report_sina", "args": {"symbol": "000001"}},
    ]
