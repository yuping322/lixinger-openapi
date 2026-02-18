from __future__ import annotations

VIEW_NAME = "convertible_bond_scanner"
DESCRIPTION = "筛选可转债并评估溢价、流动性、条款风险与正股质量联动。"
PARAMS_SCHEMA = {"type": "object", "properties": {}, "required": []}


def plan(params: dict) -> list[dict]:
    return [
        {"key": "bond_cb_spot", "tool": "bond_cb_spot_em", "args": {}},
        {"key": "bond_cb_cov_stock", "tool": "bond_cb_cov_stock_em", "args": {}},
    ]
