from __future__ import annotations

VIEW_NAME = "investment_memo_generator"
DESCRIPTION = "基于结构化输入与数据生成机构风格投资备忘录（观点、估值、催化剂、风险与监控）。"
PARAMS_SCHEMA = {"type": "object", "properties": {"stock_code": {"type": "string"}}, "required": []}


def plan(params: dict) -> list[dict]:
    stock_code = params.get("stock_code", "000001")
    return [
        {"key": "stock_info", "tool": "stock_individual_info_em", "args": {"symbol": stock_code}},
        {"key": "valuation", "tool": "stock_a_stock_general", "args": {}},
        {"key": "news", "tool": "stock_news_em", "args": {"symbol": stock_code}},
    ]
