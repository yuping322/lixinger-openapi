from __future__ import annotations

VIEW_NAME = "sector_rotation_detector"
DESCRIPTION = "通过分析中国宏观经济指标和经济周期定位，识别A股市场行业轮动信号，判断未来6–12个月哪些行业可能跑赢或跑输大盘。"
PARAMS_SCHEMA = {"type": "object", "properties": {}, "required": []}


def plan(params: dict) -> list[dict]:
    return [
        {"key": "industry_performance", "view": "industry_board_snapshot", "args": {}},
        {"key": "macro_economy", "tool": "macro_china_gdp_yearly", "args": {}},
        {"key": "market_style", "tool": "stock_market_style_em", "args": {}},
    ]
