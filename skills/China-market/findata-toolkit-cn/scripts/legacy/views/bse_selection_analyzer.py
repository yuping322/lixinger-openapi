from __future__ import annotations

VIEW_NAME = "bse_selection_analyzer"
DESCRIPTION = "扫描与分析北交所（BSE）标的，按流动性、成长性、行业景气与“专精特新”特征输出候选清单，并给出流动性与波动风险提示。"
PARAMS_SCHEMA = {"type": "object", "properties": {}, "required": []}


def plan(params: dict) -> list[dict]:
    return [
        {"key": "stock_bse_spot", "tool": "stock_bse_spot_em", "args": {}},
        {"key": "stock_bse_daily", "tool": "stock_bse_daily_em", "args": {}},
    ]
