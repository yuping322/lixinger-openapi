from __future__ import annotations

VIEW_NAME = "tech_hype_vs_fundamentals"
DESCRIPTION = "对比分析A股科技公司的估值泡沫与基本面，识别被高估和被低估的科技股。"
PARAMS_SCHEMA = {"type": "object", "properties": {}, "required": []}


def plan(params: dict) -> list[dict]:
    return [
        {"key": "tech_stock_valuation", "tool": "stock_industry_pe_em", "args": {"symbol": "半导体"}},
        {"key": "tech_company_fundamental", "tool": "stock_financial_report_sina", "args": {"symbol": "000001"}},
        {"key": "tech_concept", "tool": "stock_concept_board_em", "args": {}},
    ]
