from __future__ import annotations

VIEW_NAME = "esg_screener"
DESCRIPTION = "从ESG（环境、社会、治理）视角筛选和分析A股上市公司，评估可持续发展实践、争议事件和负责任投资标准。"
PARAMS_SCHEMA = {"type": "object", "properties": {}, "required": []}


def plan(params: dict) -> list[dict]:
    return [
        {"key": "stock_esg_rank", "tool": "stock_esg_rank_em", "args": {}},
        {"key": "stock_esg_score", "tool": "stock_esg_score_sina", "args": {}},
    ]
