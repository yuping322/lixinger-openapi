from __future__ import annotations

VIEW_NAME = "equity_research_orchestrator"
DESCRIPTION = "编排完整个股研究流程：按需调用其他技能/工具包视图，并将输出整合为一份一致的研究交付物。"
PARAMS_SCHEMA = {"type": "object", "properties": {"stock_code": {"type": "string"}}, "required": []}


def plan(params: dict) -> list[dict]:
    stock_code = params.get("stock_code", "000001")
    return [
        {"key": "financial_analysis", "view": "financial_statement_analyzer", "args": {"stock_code": stock_code}},
        {"key": "shareholder_analysis", "view": "shareholder_structure_dashboard", "args": {"symbol": stock_code}},
        {"key": "risk_check", "view": "goodwill_dashboard", "args": {"symbol": stock_code}},
    ]
