from __future__ import annotations

VIEW_NAME = "etf_allocator"
DESCRIPTION = "构建 ETF 配置方案并量化暴露（行业/风格/因子）、流动性与跟踪误差等关键约束。"
PARAMS_SCHEMA = {"type": "object", "properties": {}, "required": []}


def plan(params: dict) -> list[dict]:
    return [
        {"key": "fund_etf_spot", "tool": "fund_etf_spot_em", "args": {}},
        {"key": "fund_etf_hist", "tool": "fund_etf_hist_em", "args": {"symbol": "510300", "period": "daily"}},
    ]
