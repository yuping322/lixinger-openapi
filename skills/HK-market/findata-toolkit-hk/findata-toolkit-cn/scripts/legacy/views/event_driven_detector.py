from __future__ import annotations

VIEW_NAME = "event_driven_detector"
DESCRIPTION = "识别和分析可能创造定价偏差的A股公司事件，包括并购重组、资产注入、回购增持、管理层变更和指数调整。"
PARAMS_SCHEMA = {"type": "object", "properties": {}, "required": []}


def plan(params: dict) -> list[dict]:
    return [
        {"key": "stock_zt_pool", "tool": "stock_zt_pool_em", "args": {"date": ""}},
        {"key": "stock_stock_owner_inc", "tool": "stock_owner_increase_em", "args": {}},
        {"key": "stock_m_a", "tool": "stock_m_a_info_em", "args": {}},
    ]
