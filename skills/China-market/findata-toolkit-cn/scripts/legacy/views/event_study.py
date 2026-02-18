from __future__ import annotations

VIEW_NAME = "event_study"
DESCRIPTION = "对公司/宏观事件进行事件窗研究（事件前后收益、超额收益、同业/基准调整），用于量化事件影响。"
PARAMS_SCHEMA = {"type": "object", "properties": {"stock_code": {"type": "string"}, "event_date": {"type": "string"}}, "required": []}


def plan(params: dict) -> list[dict]:
    stock_code = params.get("stock_code", "000001")
    return [
        {"key": "stock_daily", "tool": "stock_zh_a_daily", "args": {"symbol": stock_code, "period": "daily"}},
        {"key": "index_daily", "tool": "index_zh_a_daily", "args": {"symbol": "sh000001", "period": "daily"}},
    ]
