from __future__ import annotations

VIEW_NAME = "industry_chain_mapper"
DESCRIPTION = "构建产业链上下游映射并跟踪景气信号（价格、产能、订单、库存等可得代理）。"
PARAMS_SCHEMA = {"type": "object", "properties": {"industry": {"type": "string"}}, "required": []}


def plan(params: dict) -> list[dict]:
    return [
        {"key": "industry_chain", "tool": "stock_industry_chain_em", "args": {}},
        {"key": "macro_industry", "tool": "macro_industry_data_em", "args": {}},
    ]
