from __future__ import annotations

VIEW_NAME = "quant_factor_screener"
DESCRIPTION = "使用正式因子模型进行系统化多因子A股筛选，识别具有有利因子暴露的个股。"
PARAMS_SCHEMA = {"type": "object", "properties": {}, "required": []}


def plan(params: dict) -> list[dict]:
    return [
        {"key": "factor_exposure", "tool": "stock_factor_exposure_em", "args": {}},
        {"key": "factor_rank", "tool": "stock_factor_rank_em", "args": {}},
        {"key": "quant_screen", "tool": "stock_zh_a_spot_em", "args": {}},
    ]
