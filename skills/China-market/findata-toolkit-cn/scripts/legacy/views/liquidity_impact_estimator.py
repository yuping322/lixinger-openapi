from __future__ import annotations

VIEW_NAME = "liquidity_impact_estimator"
DESCRIPTION = "评估个股/组合的流动性与交易冲击成本代理（成交量/换手、价量结构、滑点与冲击成本启发式），用于仓位与交易可行性判断。"
PARAMS_SCHEMA = {"type": "object", "properties": {"stock_code": {"type": "string"}}, "required": []}


def plan(params: dict) -> list[dict]:
    stock_code = params.get("stock_code", "000001")
    return [
        {"key": "stock_daily", "tool": "stock_zh_a_daily", "args": {"symbol": stock_code, "period": "daily"}},
        {"key": "stock_tick", "tool": "stock_tick_em", "args": {"symbol": stock_code}},
        {"key": "stock_deal_detail", "tool": "stock_bid_ask_em", "args": {"symbol": stock_code}},
    ]
