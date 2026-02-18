from __future__ import annotations

VIEW_NAME = "policy_sensitivity_brief"
DESCRIPTION = "将政策/宏观数据发布映射到行业/风格敏感度，输出可监控清单与情景推演。"
PARAMS_SCHEMA = {"type": "object", "properties": {}, "required": []}


def plan(params: dict) -> list[dict]:
    return [
        {"key": "macro_china", "tool": "macro_china_gdp_yearly", "args": {}},
        {"key": "policy_news", "tool": "macro_policy_news_em", "args": {}},
        {"key": "industry_policy", "tool": "stock_industry_policy_em", "args": {}},
    ]
