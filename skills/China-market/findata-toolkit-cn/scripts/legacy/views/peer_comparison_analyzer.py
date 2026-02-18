from __future__ import annotations

VIEW_NAME = "peer_comparison_analyzer"
DESCRIPTION = "构建同业可比公司对比（估值、成长、盈利能力、杠杆、现金流质量）并解释差异来源。"
PARAMS_SCHEMA = {"type": "object", "properties": {"industry": {"type": "string"}}, "required": []}


def plan(params: dict) -> list[dict]:
    industry = params.get("industry", "银行")
    return [
        {"key": "industry_pe", "tool": "stock_industry_pe_em", "args": {"symbol": industry}},
        {"key": "stock_industry", "tool": "stock_industry_component_em", "args": {"symbol": industry}},
    ]
