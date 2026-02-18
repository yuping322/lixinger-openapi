from __future__ import annotations

VIEW_NAME = "financial_statement_analyzer"
DESCRIPTION = "对单个A股上市公司的财务报表进行深度分析，评估盈利质量、财务健康状况、财务造假风险和运营效率。"
PARAMS_SCHEMA = {"type": "object", "properties": {"stock_code": {"type": "string"}}, "required": []}


def plan(params: dict) -> list[dict]:
    stock_code = params.get("stock_code", "000001")
    return [
        {"key": "stock_financial_report", "tool": "stock_financial_report_sina", "args": {"symbol": stock_code}},
        {"key": "stock_balance_sheet", "tool": "stock_balance_sheet_em", "args": {"symbol": stock_code}},
        {"key": "stock_income_sheet", "tool": "stock_income_sheet_em", "args": {"symbol": stock_code}},
        {"key": "stock_cash_flow", "tool": "stock_cash_flow_sheet_em", "args": {"symbol": stock_code}},
    ]
